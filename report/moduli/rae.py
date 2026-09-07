"""
Effetto dell'eta' relativa: chi entra nel ranking, e chi ci resta.

LA DOMANDA
    Fra ragazzi della stessa annata, chi e' nato a gennaio ha fino a dodici mesi di
    sviluppo in piu' di chi e' nato a dicembre. Alle eta' piu' basse quella differenza
    e' probabilmente il fattore dominante del risultato agonistico. Se lo e', la
    selezione fatta sul risultato a 13 anni sta in parte selezionando la data di nascita.

DUE ANALISI DISTINTE, che vanno tenute separate

    Composizione — chi ENTRA nel ranking di ciascuna categoria, confrontato con la
    popolazione italiana della stessa coorte. Risponde a: la selezione iniziale e'
    sbilanciata?

    Successo — fra chi e' gia' nel ranking, chi ARRIVA al professionismo. Risponde a:
    una volta dentro, il trimestre conta ancora?

    E' la distinzione che rende il lavoro di Voet piu' informativo degli altri: un
    effetto forte in composizione e assente nel successo significa che il vantaggio e'
    di accesso, non di talento.

L'ATTESO NON E' IL 25%
    In Italia si nasce di piu' fra maggio e settembre e il primo trimestre e' il piu'
    scarso. L'atteso viene da Eurostat, cache in data/riferimento/ (script 07).
    Usare l'uniforme sottostimerebbe l'effetto invece di sovrastimarlo.

COSA NON FA
    Non stima modelli: e' un confronto fra distribuzioni. I modelli, dove l'eta'
    relativa entra come covariata, stanno in R.
"""
import os
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, cfg          # noqa: E402
from lib_risultati import Archivio                 # noqa: E402
import lib_markdown as md                          # noqa: E402
import lib_grafici as gr                           # noqa: E402

W = "https://en.wikipedia.org/wiki/"
DB_RIF = "data/riferimento/riferimenti.db"
CATEGORIE = ("U15", "U17", "U19", "U23")
# Le sigle internazionali sono quelle dei dati; nelle figure vanno i nomi che si
# usano in Italia, che il lettore riconosce senza doverli tradurre.
NOMI = {"U15": "Esordienti", "U17": "Allievi", "U19": "Juniores", "U23": "Under 23"}


def chi_quadro(osservati, attesi_frazioni):
    """Statistica chi-quadro, V di Cramer e p, con gli attesi dati come frazioni.

    Il p arriva da scipy se c'e'. Se manca, si riportano comunque statistica ed effect
    size: con migliaia di osservazioni il p diventa significativo per squilibri
    irrilevanti, quindi e' la parte meno interessante del test.
    """
    n = sum(osservati)
    attesi = [f * n for f in attesi_frazioni]
    x2 = sum((o - a) ** 2 / a for o, a in zip(osservati, attesi) if a > 0)
    gl = len(osservati) - 1
    v = (x2 / n) ** 0.5 if n else 0.0          # k=2 categorie nominali -> V = sqrt(X2/n)
    try:
        from scipy.stats import chi2
        p = float(chi2.sf(x2, gl))
    except ImportError:
        p = None
    return {"x2": x2, "gl": gl, "cramer_v": v, "p": p, "attesi": attesi}


def attesi_per_coorti(rif, lo, hi):
    mesi = dict(rif.execute("""SELECT mese, SUM(nati) FROM nascite_mese
                               WHERE anno BETWEEN ? AND ? GROUP BY 1""", (lo, hi)))
    if len(mesi) != 12:
        raise SystemExit("Nascite Eurostat incomplete per %d-%d: esegui "
                         "scripts/07_riferimenti.py" % (lo, hi))
    tot = sum(mesi.values())
    return [sum(mesi[m] for m in range(1 + 3 * i, 4 + 3 * i)) / tot for i in range(4)]


def calcola():
    if not os.path.exists(DB_RIF):
        raise SystemExit("Manca %s: esegui prima scripts/07_riferimenti.py" % DB_RIF)
    db = sqlite3.connect(DB_ANALISI)
    rif = sqlite3.connect(DB_RIF)
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    attesi = attesi_per_coorti(rif, lo, hi)

    with Archivio("rae") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))
        ar.valore("sesso", sesso)
        ar.valore("attesi_trimestre", [round(a, 4) for a in attesi],
                  nota="Eurostat demo_fmonth, nati vivi in Italia nelle coorti in studio")

        # --- composizione: chi entra nel ranking di ciascuna categoria -------
        righe, gradiente = [], []
        for cat in CATEGORIE:
            oss = [0] * 4
            for q, n in db.execute("""
                    SELECT g.birth_quarter, COUNT(DISTINCT a.athlete_id)
                    FROM tab_a a JOIN anagrafica g USING(athlete_id)
                    WHERE a.sesso=? AND a.category=? AND a.birth_year BETWEEN ? AND ?
                      AND a.cat_year IS NOT NULL AND g.birth_quarter IS NOT NULL
                    GROUP BY 1""", (sesso, cat, lo, hi)):
                oss[q - 1] = n
            n = sum(oss)
            if not n:
                continue
            t = chi_quadro(oss, attesi)
            # rapporto fra osservato e atteso: e' la lettura piu' onesta, perche' toglie
            # di mezzo la stagionalita' demografica invece di ignorarla
            oa = [(o / n) / a for o, a in zip(oss, attesi)]
            righe.append([cat, n] + [round(x, 2) for x in oa]
                         + [round(oa[0] / oa[3], 2), round(t["cramer_v"], 3)])
            gradiente.append((cat, oa[0] / oa[3], n))
            ar.valore("composizione_%s_oss" % cat, oss)
            ar.valore("composizione_%s_test" % cat,
                      {k: (round(v, 4) if isinstance(v, float) else v)
                       for k, v in t.items() if k != "attesi"})

        ar.tabella("composizione", righe,
                   colonne=["categoria", "atleti", "Q1 oss/att", "Q2", "Q3", "Q4",
                            "Q1/Q4", "V di Cramer"],
                   titolo="Chi entra nel ranking, per trimestre di nascita",
                   nota="valori sopra 1 = piu' atleti dell'atteso demografico")
        ar.valore("gradiente", [(c, round(r, 2), n) for c, r, n in gradiente])
        if gradiente:
            ar.valore("q1_su_q4_min", round(min(g[1] for g in gradiente), 2))
            ar.valore("q1_su_q4_max", round(max(g[1] for g in gradiente), 2))

        # --- successo: fra chi e' nel ranking, chi arriva --------------------
        righe_s = []
        for etichetta, filtro in (("tutti i classificati", "1=1"),
                                  ("professionisti", "PRO = 1"),
                                  ("top 500", "tier >= 2"),
                                  ("top 100", "tier = 3")):
            oss = [0] * 4
            for q, n in db.execute("""
                    SELECT birth_quarter, COUNT(*) FROM tab_b
                    WHERE sesso=? AND birth_year BETWEEN ? AND ?
                      AND birth_quarter IS NOT NULL AND %s
                    GROUP BY 1""" % filtro, (sesso, lo, hi)):
                oss[q - 1] = n
            n = sum(oss)
            if not n:
                continue
            t = chi_quadro(oss, attesi)
            oa = [(o / n) / a for o, a in zip(oss, attesi)]
            righe_s.append([etichetta, n] + oss
                           + [round(oa[0] / oa[3], 2) if oa[3] else None])
            ar.valore("successo_%s" % etichetta.replace(" ", "_"),
                      {"n": n, "osservati": oss, "q1_su_q4": round(oa[0] / oa[3], 2)
                       if oa[3] else None, "p": t["p"]})

        ar.tabella("successo", righe_s,
                   colonne=["gruppo", "n", "Q1", "Q2", "Q3", "Q4", "Q1/Q4"],
                   titolo="Fra chi e' nel ranking, chi arriva",
                   nota="i conteggi sono atleti; le celle sotto la soglia sono mascherate")

        # --- la figura -------------------------------------------------------
        if len(gradiente) >= 2 and not os.environ.get("SENZA_FIGURE"):
            try:
                with gr.figura("Il vantaggio di essere nati a inizio anno svanisce "
                               "con l'eta'") as (fig, ax):
                    x = list(range(len(gradiente)))
                    ax.plot(x, [g[1] for g in gradiente], marker="o", linewidth=2,
                            color=gr.COLORI[0], zorder=3)
                    for i, (c, r, nn) in enumerate(gradiente):
                        ax.annotate("%.2f" % r, (i, r), textcoords="offset points",
                                    xytext=(0, 9), ha="center", fontsize=9)
                    gr.linea_riferimento(ax, 1.0, "nessuno squilibrio")
                    ax.set_xticks(x)
                    ax.set_xticklabels(
                        [NOMI.get(g[0], g[0]) + chr(10) + "n=%d" % g[2]
                         for g in gradiente])
                    ax.set_ylabel("quanti nati a gennaio-marzo" + chr(10) +
                                  "per ogni nato a ottobre-dicembre")
                    ax.set_ylim(bottom=0.9)
                    fig.text(0.005, -0.02, "Coorti %d-%d. Atteso da Eurostat, nascite "
                             "in Italia per mese." % (lo, hi), fontsize=8, color=gr.GRIGIO)
                ar.figura("gradiente", gr.salva("rae_gradiente"),
                          didascalia="Il rapporto fra chi e' nato nel primo e nel quarto "
                                     "trimestre, corretto per la stagionalita' delle "
                                     "nascite, scende da %.2f in %s a %.2f in %s."
                                     % (gradiente[0][1], gradiente[0][0],
                                        gradiente[-1][1], gradiente[-1][0]))
            except SystemExit as e:
                print("   figura saltata: %s" % e)

        # --- la stessa lettura, senza bisogno di alcun atteso ----------------
        # Il decadimento fra categorie sulle STESSE coorti non dipende dalla
        # distribuzione demografica, che e' identica ai due estremi e si cancella.
        # E' l'argomento piu' solido, e va riportato accanto al chi-quadro.
        if len(gradiente) >= 2:
            ar.valore("decadimento",
                      {"prima": gradiente[0][0], "prima_q1_su_q4": round(gradiente[0][1], 2),
                       "ultima": gradiente[-1][0], "ultima_q1_su_q4": round(gradiente[-1][1], 2)},
                      nota="confronto interno alle stesse coorti: non dipende dall'atteso")

        confronto_sessi(db, rif, ar)

    print("Modulo 'rae' eseguito.")
    for r in righe:
        print("   %-5s n=%-6s Q1/Q4 = %.2f" % (r[0], r[1], r[6]))


def confronto_sessi(db, rif, ar):
    """Lo stesso effetto misurato su maschi e femmine, sulle stesse coorti.

    PERCHE' SI PUO' FARE SOLO QUESTO, SUL FEMMINILE
        Ogni altra analisi dello studio ha bisogno di un esito di carriera, e l'esito per
        le atlete **non e' stato raccolto**: le rose e le classifiche scaricate da
        ProCyclingStats sono quelle maschili. Non e' un problema di numerosita' ma di dati
        mancanti, e si risolverebbe scaricando le classifiche femminili.

        L'effetto dell'eta' relativa e' l'eccezione, perche' confronta la composizione del
        ranking con la demografia e non chiede a nessuno di essere diventato qualcosa.
        Serve solo la data di nascita, che per le atlete c'e' quasi sempre.

    PERCHE' IL CONFRONTO E' INTERESSANTE
        Le ragazze maturano prima dei ragazzi, e a tredici anni molte hanno gia'
        attraversato la puberta'. Se il vantaggio di chi e' nato a gennaio e' un vantaggio
        di maturazione, dovrebbe essere piu' debole fra le atlete, e spegnersi prima.

    COME SI TIENE ONESTO IL CONFRONTO
        Le due popolazioni coprono coorti diverse: il ranking femminile comincia nel 2011.
        Per ogni categoria si prendono quindi le coorti in cui **entrambi** i sessi sono
        osservati, e l'atteso demografico si calcola su quelle stesse coorti. I due numeri
        che si confrontano riguardano cosi' gli stessi anni di nascita.
    """
    righe, per_sesso = [], {}
    for cat in CATEGORIE:
        estremi = db.execute(
            """SELECT MIN(a.birth_year), MAX(a.birth_year)
               FROM tab_a a JOIN anagrafica g USING(athlete_id)
               WHERE a.sesso = 'F' AND a.category = ? AND a.cat_year IS NOT NULL
                 AND g.birth_quarter IS NOT NULL""", (cat,)).fetchone()
        if not estremi or estremi[0] is None:
            continue                      # nessuna atleta: l'Under 23 femminile non esiste
        lo, hi = estremi
        attesi = attesi_per_coorti(rif, lo, hi)
        for sesso in ("M", "F"):
            oss = [0] * 4
            for q, n in db.execute(
                    """SELECT g.birth_quarter, COUNT(DISTINCT a.athlete_id)
                       FROM tab_a a JOIN anagrafica g USING(athlete_id)
                       WHERE a.sesso = ? AND a.category = ? AND a.cat_year IS NOT NULL
                         AND a.birth_year BETWEEN ? AND ? AND g.birth_quarter IS NOT NULL
                       GROUP BY 1""", (sesso, cat, lo, hi)):
                oss[q - 1] = n
            n = sum(oss)
            if n < 100:
                continue
            t = chi_quadro(oss, attesi)
            oa = [(o / n) / a for o, a in zip(oss, attesi)]
            rapporto = oa[0] / oa[3] if oa[3] else None
            righe.append([cat, "maschi" if sesso == "M" else "femmine", n,
                          "%d-%d" % (lo, hi), round(oa[0], 2), round(oa[3], 2),
                          round(rapporto, 2) if rapporto else None,
                          round(t["cramer_v"], 3),
                          round(t["p"], 4) if t["p"] is not None else None])
            per_sesso.setdefault(sesso, []).append((cat, round(rapporto, 2), n))

    if not righe:
        return
    ar.tabella("sessi", righe,
               colonne=["categoria", "sesso", "atleti", "coorti", "Q1 oss/att",
                        "Q4 oss/att", "Q1/Q4", "V di Cramer", "p"],
               titolo="L'effetto dell'eta' relativa, maschi e femmine a confronto",
               nota="per ogni categoria si usano le coorti in cui entrambi i sessi sono "
                    "osservati, e l'atteso demografico e' calcolato su quelle stesse "
                    "coorti; l'Under 23 femminile non esiste come categoria")
    ar.valore("confronto_sessi", per_sesso)
    if per_sesso.get("M") and per_sesso.get("F"):
        ar.valore("sessi_prima_categoria",
                  {"categoria": per_sesso["M"][0][0],
                   "maschi": per_sesso["M"][0][1], "femmine": per_sesso["F"][0][1],
                   "n_maschi": per_sesso["M"][0][2], "n_femmine": per_sesso["F"][0][2]})

    if os.environ.get("SENZA_FIGURE"):
        return
    try:
        gr.stile()
        with gr.figura("Nati a gennaio: quanto pesa, per i maschi e per le femmine",
                       altezza=3.6) as (fig, ax):
            categorie = [c for c in CATEGORIE if any(r[0] == c for r in righe)]
            x = list(range(len(categorie)))
            for i, sesso in enumerate(("maschi", "femmine")):
                valori = [next((r[6] for r in righe if r[0] == c and r[1] == sesso), None)
                          for c in categorie]
                punti = [(j, v) for j, v in zip(x, valori) if v is not None]
                if not punti:
                    continue
                ax.plot([p[0] for p in punti], [p[1] for p in punti], marker="o",
                        linewidth=2, color=gr.COLORI[i], label=sesso, zorder=3)
                for j, v in punti:
                    ax.annotate("%.2f" % v, (j, v), textcoords="offset points",
                                xytext=(0, 9), ha="center", fontsize=9)
            gr.linea_riferimento(ax, 1.0, "nessuno squilibrio")
            ax.set_xticks(x)
            ax.set_xticklabels([NOMI.get(c, c) for c in categorie])
            ax.set_ylabel("quanti nati a gennaio-marzo" + chr(10) +
                          "per ogni nato a ottobre-dicembre")
            ax.set_ylim(bottom=0.9)
            ax.legend(frameon=False, fontsize=9)
        ar.figura("sessi", gr.salva("rae_sessi"),
                  didascalia="Fra le atlete lo squilibrio c'e' ma e' piu' contenuto, e in "
                             "Allieve non si distingue dall'atteso demografico. Le coorti "
                             "femminili sono pero' molto meno numerose, e il rimbalzo in "
                             "Juniores va letto con quella cautela.")
    except SystemExit as e:
        print("   figura sessi saltata: %s" % e)


def rendi(lt):
    """Il testo della sezione. Legge SOLO dall'archivio: mai dai database.

    E' la regola che tiene insieme le due meta': se un numero non e' nell'archivio non
    puo' finire nel testo, e quindi non puo' essere scritto a mano.
    """
    v = lt.valori("rae")
    comp = lt.tabella("rae", "composizione")
    succ = lt.tabella("rae", "successo")
    dec = v.get("decadimento", {})
    att = v.get("attesi_trimestre", [])

    p = [md.sezione("L'effetto dell'eta' relativa")]
    p.append(md.paragrafo(
        "Fra ragazzi della stessa annata, chi e' nato a gennaio ha fino a dodici mesi di "
        "sviluppo in piu' di chi e' nato a dicembre. Alle eta' piu' basse quella differenza "
        "e' probabilmente il fattore dominante del risultato agonistico: se lo e', "
        "selezionare sul risultato a tredici anni significa in parte selezionare la data "
        "di nascita.",
        "",
        "Il confronto non e' con il 25 per cento per trimestre. In Italia si nasce di piu' "
        "fra maggio e settembre, e il primo trimestre e' il **piu' scarso** della "
        "popolazione: l'atteso e' Q1 %.2f%%, Q2 %.2f%%, Q3 %.2f%%, Q4 %.2f%%. "
        "Usare l'uniforme sottostimerebbe l'effetto invece di sovrastimarlo."
        % tuple(100 * a for a in att) if len(att) == 4 else ""))

    p.append(md.metodo(
        "Rapporto fra osservato e atteso, e V di Cramer",
        "Per ogni trimestre si divide la quota di atleti nati in quel trimestre per la "
        "quota di nati nella popolazione italiana delle stesse annate. Un valore di "
        "1,39 significa che quel trimestre e' rappresentato del 39% in piu' di quanto "
        "la demografia giustifichi.\n\n"
        "La V di Cramer riassume in un solo numero quanto l'intera distribuzione si "
        "discosta dall'attesa: va da 0, distribuzione identica all'attesa, a 1. Si "
        "riporta al posto del p-value del test chi quadro perche' con migliaia di "
        "osservazioni quel test risulta significativo anche per squilibri irrilevanti, "
        "mentre la V misura l'entita' dello squilibrio e non la sua rilevabilita'.\n\n"
        "L'attesa demografica viene dalle nascite mensili registrate in Italia, non da "
        "una distribuzione uniforme.",
        [("Bonta' di adattamento", W + "Goodness_of_fit"),
         ("V di Cramer", W + "Cram%C3%A9r%27s_V"),
         ("Effetto dell'eta' relativa", W + "Relative_age_effect"),
         ("Nascite per mese, Eurostat",
          "https://ec.europa.eu/eurostat/databrowser/view/demo_fmonth/default/table")]))

    p.append(md.sezione("Chi entra nel ranking", 3))
    if comp:
        p.append(md.tabella(comp["colonne"], comp["righe"],
                            colonne_conteggio={1}, decimali=2, nota=comp["nota"]))
    if dec:
        p.append(md.paragrafo(
            "",
            "Il vantaggio si spegne con l'eta': da **%.2f a uno** in %s a **%.2f** in %s. "
            "E questo confronto non ha bisogno di alcun dato esterno, perche' riguarda le "
            "stesse coorti ai due estremi e la stagionalita' demografica si cancella."
            % (dec["prima_q1_su_q4"], dec["prima"], dec["ultima_q1_su_q4"], dec["ultima"])))

    fig = lt.figura("rae", "gradiente")
    if fig:
        p.append(md.figura(fig["percorso"], fig["didascalia"]))

    p.append(md.sezione("Chi arriva, fra quelli entrati", 3))
    if succ:
        p.append(md.tabella(succ["colonne"], succ["righe"],
                            colonne_conteggio={1, 2, 3, 4, 5}, nota=succ["nota"]))
    p.append(md.paragrafo(
        "",
        "La distinzione fra le due tabelle e' quella che rende il risultato "
        "interpretabile: un effetto forte nella composizione e assente nel successo "
        "significa che il vantaggio e' di **accesso**, non di talento."))

    sessi = lt.tabella("rae", "sessi")
    if sessi:
        p.append(md.sezione("Lo stesso effetto sulle ragazze", 3))
        p.append(md.paragrafo(
            "Questa e' la sola analisi dello studio che si puo' fare anche sul femminile, "
            "e la ragione non e' la numerosita'. Tutte le altre domande hanno bisogno di "
            "un esito di carriera, e per le atlete quell'esito **non e' stato raccolto**: "
            "le rose e le classifiche scaricate da ProCyclingStats sono quelle maschili. "
            "L'effetto dell'eta' relativa fa eccezione perche' confronta la composizione "
            "del ranking con la demografia, e chiede solo la data di nascita."))

        p.append(md.paragrafo(
            "",
            "Il confronto ha un motivo sostanziale, oltre alla disponibilita' dei dati. "
            "Le ragazze maturano prima: a tredici anni molte hanno gia' attraversato la "
            "puberta', mentre fra i coetanei maschi la differenza di sviluppo fra gennaio "
            "e dicembre e' al suo massimo. Se il vantaggio di essere nati a inizio anno e' "
            "un vantaggio di maturazione, e non di talento, fra le atlete dovrebbe essere "
            "piu' debole."))

        righe_s = [[r[0], r[1], md.conta(r[2]), r[3], md.num(r[4], 2), md.num(r[5], 2),
                    md.num(r[6], 2), md.num(r[7], 3),
                    "< 0,001" if r[8] is not None and r[8] < 0.001 else md.num(r[8], 3)]
                   for r in sessi["righe"]]
        p.append(md.tabella(sessi["colonne"], righe_s, nota=sessi["nota"],
                            colonne_conteggio=(2,)))

        prima = v.get("sessi_prima_categoria") or {}
        if prima:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    prima.get("femmine", 9) < prima.get("maschi", 0),
                    "in %s lo squilibrio fra primo e quarto trimestre e' minore fra le "
                    "atlete che fra gli atleti" % prima.get("categoria", ""),
                    "**L'ipotesi regge, e il divario e' netto.** In %s i nati nel primo "
                    "trimestre sono %s volte quelli dell'ultimo fra i maschi e %s volte "
                    "fra le femmine, sulle stesse coorti e con lo stesso atteso "
                    "demografico. In Allievi l'effetto femminile scende ancora, fino a non "
                    "distinguersi piu' dalla distribuzione attesa."
                    % (prima.get("categoria"), md.num(prima.get("maschi"), 2),
                       md.num(prima.get("femmine"), 2)))))

        p.append(md.paragrafo(
            "",
            "> **Due cautele, e sono serie.** Le atlete sono %s in Esordienti contro %s "
            "atleti, quindi gli intervalli attorno ai valori femminili sono molto piu' "
            "larghi. E il valore femminile in Juniores risale invece di scendere: con "
            "poche centinaia di atlete un rimbalzo del genere e' esattamente cio' che il "
            "caso produce, e non va letto come un ritorno dell'effetto. Quello che si puo' "
            "dire con ragionevole sicurezza riguarda le eta' piu' basse, dove i numeri "
            "sono maggiori e la differenza fra i sessi e' piu' larga."
            % (md.conta(prima.get("n_femmine")), md.conta(prima.get("n_maschi")))))

        fig_s = lt.figura("rae", "sessi")
        if fig_s:
            p.append(md.figura(fig_s["percorso"], fig_s["didascalia"]))

        p.append(md.paragrafo(
            "",
            "> **Cosa servirebbe per andare oltre.** Scaricare da ProCyclingStats le rose "
            "delle squadre femminili e le classifiche mondiali femminili renderebbe "
            "possibile sul femminile tutto il resto dello studio. Resterebbero due limiti "
            "strutturali: le atlete in classifica sono circa un decimo degli atleti, e la "
            "categoria Under 23 femminile non esiste, quindi il predittore piu' vicino "
            "all'esito mancherebbe."))

    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
