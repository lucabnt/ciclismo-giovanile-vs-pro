"""
Il ciclismo giovanile femminile, per quello che i dati permettono di dirne.

PERCHE' UNA SEZIONE A SE'
    Tutto il resto del documento gira sui maschi, e non per scelta di merito: gli esiti di
    carriera femminili non erano stati raccolti, quindi ogni domanda che finisca con «e
    poi chi ce l'ha fatta?» non aveva risposta. Restano pero' molte domande che non hanno
    bisogno di un esito, e su quelle il femminile si puo' studiare eccome.

    Questa sezione raccoglie cio' che si puo' dire adesso: quanto e' grande il movimento,
    come sono fatte le sue classifiche, e cosa succede confrontando le stesse misure con
    quelle maschili.

L'ESPERIMENTO NATURALE
    Il risultato piu' bello arriva da un cambio di regolamento della fonte. Nelle
    Esordienti femminili la classifica e' stata **unica** fino al 2021 e **separata per
    annata** dal 2022. Stessa categoria e stesse eta', in due periodi diversi: cambia
    la struttura della lista, e si puo' vedere cosa fa.

    Nel documento la stessa cosa era stata mostrata confrontando maschi e femmine, che
    pero' sono popolazioni diverse. Qui il confronto resta dentro la stessa categoria
    e alle stesse eta', ed e' piu' stringente.

UN AVVISO SUL CONTEGGIO DELLE GARE
    Quando le liste si separano, la stessa giornata di gara produce **due** classifiche
    invece di una, quindi i posti a punti raddoppiano per costruzione. Il salto che si
    vede nelle Esordienti femminili dal 2022 e' quello, non un calendario improvvisamente
    raddoppiato: per l'andamento nel tempo si guardano quindi le categorie che non hanno
    cambiato struttura.
"""
import os
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, LISTE_DISGIUNTE               # noqa: E402
from lib_giovanile import CATEGORIE as CATEGORIE_FONTE             # noqa: E402
from lib_risultati import Archivio                             # noqa: E402
import lib_markdown as md                                      # noqa: E402
import lib_grafici as gr                                       # noqa: E402

CATEGORIE = ("U15", "U17", "U19")
NOMI = {"U15": "Esordienti", "U17": "Allievi", "U19": "Juniores", "U23": "Under 23"}
# L'anno in cui la fonte ha separato le classifiche delle Esordienti femminili.
ANNO_SEPARAZIONE = LISTE_DISGIUNTE.get("donne_esordienti", (2022, 2026))[0]
MIN_ATLETI = 30


def liste(sesso, cat, stagione):
    """Quante classifiche pubblica la fonte: una, o una per annata.

    Serve a contare le gare e non le classifiche. Dove ogni annata ha la propria lista la
    stessa giornata di gara lascia cinque piazzamenti per annata, ma un'atleta ne corre una
    sola, quindi il conteggio va diviso. Nelle Esordienti femminili la separazione comincia
    nel %d, percio' il divisore cambia da una stagione all'altra.
    """ % ANNO_SEPARAZIONE
    for slug, (da, a) in LISTE_DISGIUNTE.items():
        voce = CATEGORIE_FONTE.get(slug)
        if voce and voce[0] == cat and voce[1] == sesso and da <= stagione <= a:
            return 2
    return 1


def gare_per_stagione(db, sesso, cat):
    """Media per stagione delle gare che un atleta poteva correre."""
    somma, n = 0.0, 0
    for st, p in db.execute(
            """SELECT season, SUM(top5) FROM tab_a
               WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL
                 AND flag_stagione IS NULL GROUP BY 1""", (sesso, cat)):
        if p:
            somma += p / 5 / liste(sesso, cat, st)
            n += 1
    return somma / n if n else 0


def calcola():
    db = sqlite3.connect(DB_ANALISI)

    def conta(sesso, cat, extra="", par=()):
        return db.execute(
            """SELECT COUNT(DISTINCT athlete_id), SUM(top5), COUNT(DISTINCT season),
                      COUNT(*)
               FROM tab_a WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL
                 AND flag_stagione IS NULL """ + extra,
            (sesso, cat) + par).fetchone()

    with Archivio("ragazze") as ar:
        # --- 1. quanto e' grande il movimento -------------------------------
        righe = []
        for cat in CATEGORIE:
            f = conta("F", cat)
            m = conta("M", cat)
            if not f[1] or not m[1]:
                continue
            gf, gm = gare_per_stagione(db, "F", cat), gare_per_stagione(db, "M", cat)
            righe.append([NOMI[cat], f[0], m[0], round(m[0] / f[0], 1),
                          round(gf), round(gm), round(gm / gf, 1) if gf else None])
        ar.tabella(
            "dimensione", righe,
            colonne=["categoria", "atlete", "atleti", "rapporto",
                     "gare per stagione, femminili", "maschili", "rapporto fra le gare"],
            titolo="Quanto e' grande il movimento femminile, in rapporto",
            nota="atlete e atleti distinti su tutte le stagioni disponibili; le gare sono "
                 "stimate dai piazzamenti nei primi cinque, cinque per gara, e dove ogni "
                 "annata ha la propria classifica si divide per il numero di liste, perche' "
                 "un atleta corre comunque una gara sola per giornata")
        if righe:
            ar.valore("rapporto_atleti", {r[0]: r[3] for r in righe})
            ar.valore("rapporto_gare", {r[0]: r[6] for r in righe})
            # Il rapporto fra le gare regge solo dove entrambi i sessi hanno una lista
            # unica: negli Esordienti maschili il conteggio somma due calendari.
            tutti = [r[6] for r in righe if r[6]]
            if tutti:
                ar.valore("rapporto_gare_confrontabile",
                          {"minimo": min(tutti), "massimo": max(tutti)},
                          "tutte le categorie: il conteggio divide per il numero di liste")

        # --- 2. l'esperimento naturale delle Esordienti ----------------------
        quote = []
        for etichetta, lo, hi in (
                ("classifica unica", 2000, ANNO_SEPARAZIONE - 1),
                ("classifiche separate", ANNO_SEPARAZIONE, 2100)):
            per_anno = list(db.execute(
                """SELECT cat_year, COUNT(*), SUM(top5) FROM tab_a
                   WHERE sesso = 'F' AND category = 'U15' AND cat_year IS NOT NULL
                     AND season BETWEEN ? AND ? AND flag_stagione IS NULL
                   GROUP BY 1 ORDER BY 1""", (lo, hi)))
            totale = sum(p for _, _, p in per_anno)
            if not totale or len(per_anno) < 2:
                continue
            quote.append([etichetta,
                          "%d-%d" % (lo if lo > 2000 else 2011,
                                     min(hi, 2025)),
                          per_anno[0][1], round(100 * per_anno[0][2] / totale, 1),
                          round(100 * per_anno[1][2] / totale, 1)])
        if len(quote) == 2:
            ar.tabella(
                "separazione", quote,
                colonne=["struttura della classifica", "stagioni", "atlete al primo anno",
                         "quota dei posti, primo anno", "secondo anno"],
                titolo="Cosa succede quando le annate smettono di farsi concorrenza",
                nota="Esordienti femminili: la fonte ha separato le due classifiche dal "
                     "%d, e prima ne pubblicava una sola" % ANNO_SEPARAZIONE)
            ar.valore("separazione_quote",
                      {"prima": quote[0][3], "dopo": quote[1][3],
                       "anno": ANNO_SEPARAZIONE})

        # --- 3. la concentrazione, a confronto -------------------------------
        conc = []
        for cat in CATEGORIE:
            riga = [NOMI[cat]]
            for sesso in ("F", "M"):
                quote_d = []
                for (st,) in db.execute(
                        """SELECT DISTINCT season FROM tab_a
                           WHERE sesso = ? AND category = ? AND flag_stagione IS NULL""",
                        (sesso, cat)):
                    punti = [r[0] for r in db.execute(
                        """SELECT points_raw FROM tab_a WHERE sesso = ? AND category = ?
                           AND season = ? AND points_raw > 0""", (sesso, cat, st))]
                    if len(punti) < MIN_ATLETI:
                        continue
                    punti.sort(reverse=True)
                    k = max(1, len(punti) // 10)
                    quote_d.append(100 * sum(punti[:k]) / sum(punti))
                riga.append(round(sum(quote_d) / len(quote_d), 1) if quote_d else None)
            conc.append(riga)
        ar.tabella(
            "concentrazione", conc,
            colonne=["categoria", "femminile", "maschile"],
            titolo="Quanto prende il dieci per cento migliore, nei due movimenti",
            nota="medie sulle stagioni; e' la stessa misura della sezione sui posti")
        if conc:
            valide = [x for r in conc for x in r[1:] if x is not None]
            ar.valore("concentrazione_estremi",
                      {"minimo": min(valide), "massimo": max(valide)})

        # --- 4. il calendario nel tempo, dove la struttura non e' cambiata ---
        serie = {}
        for cat in CATEGORIE:
            per_stagione = {st: n / 5 / liste("F", cat, st) for st, n in db.execute(
                """SELECT season, SUM(top5) FROM tab_a
                   WHERE sesso = 'F' AND category = ? AND cat_year IS NOT NULL
                   GROUP BY 1 ORDER BY 1""", (cat,)) if n}
            if len(per_stagione) >= 8:
                serie[cat] = per_stagione
        if serie:
            anni = sorted(set.intersection(*[set(s) for s in serie.values()]))
            anni = [a for a in anni if a != 2020]
            righe_c = []
            for cat, per_stagione in serie.items():
                a0, a1 = per_stagione[anni[0]], per_stagione[anni[-1]]
                righe_c.append([NOMI[cat], round(a0), round(a1),
                                round(100 * (a1 - a0) / a0, 1)])
            ar.tabella(
                "calendario", righe_c,
                colonne=["categoria", "gare nel %d" % anni[0], "gare nel %d" % anni[-1],
                         "variazione"],
                titolo="Il calendario femminile, dove la struttura delle liste non e' cambiata",
                nota="le Esordienti ci sono: dal %d hanno due classifiche invece di una, e "
                     "il conteggio ne tiene conto dividendo per il numero di liste, cosi' "
                     "la serie resta confrontabile prima e dopo il cambio"
                     % ANNO_SEPARAZIONE)
            ar.valore("calendario_estremi",
                      {"prima": anni[0], "ultima": anni[-1],
                       "variazioni": {r[0]: r[3] for r in righe_c}})

        # --- 5. l'archivio degli esiti femminili, solo in forma aggregata ------
        # Le rose vengono da profili di persone identificabili e restano fuori dal
        # repository; qui se ne ricavano soltanto tre conteggi, perche' i numeri che il
        # post cita passino dal controllo automatico come tutti gli altri.
        pcs = os.path.join("data", "pcs", "pcs_F.db")
        if os.path.exists(pcs):
            dp = sqlite3.connect(pcs)
            try:
                squadre = dp.execute("SELECT COUNT(*) FROM pcs_team").fetchone()[0]
                righe_rosa = dp.execute("SELECT COUNT(*) FROM pcs_roster").fetchone()[0]
                italiane = dp.execute(
                    """SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_roster r
                       JOIN pcs_team t ON t.season = r.season AND t.team_slug = r.team_slug
                       WHERE t.team_class IN ('WTW', 'PRW')
                         AND r.season BETWEEN 2020 AND 2025 AND r.nazionalita = 'IT'"""
                ).fetchone()[0]
                ar.valore("pcs_femminile",
                          {"squadre_stagione": squadre, "righe_rosa": righe_rosa,
                           "italiane_2020_2025": italiane},
                          "conteggi aggregati dell'archivio PCS femminile, che resta privato")
            finally:
                dp.close()

        disegna(quote, ar)

    print("Modulo 'ragazze' eseguito.")
    if len(quote) == 2:
        print("   Esordienti femminili: il primo anno passa dal %.1f%% al %.1f%% dei posti "
              "quando le classifiche si separano" % (quote[0][3], quote[1][3]))


def disegna(quote, ar):
    if os.environ.get("SENZA_FIGURE") or len(quote) != 2:
        return
    gr.stile()
    with gr.figura("Esordienti femminili: prima e dopo la separazione delle classifiche",
                   altezza=3.4) as (f, ax):
        x = [0, 1]
        primo = [q[3] for q in quote]
        secondo = [q[4] for q in quote]
        ax.bar(x, primo, 0.5, color=gr.COLORI[0], label="primo anno")
        ax.bar(x, secondo, 0.5, bottom=primo, color=gr.COLORI[1], label="secondo anno")
        for i, v in enumerate(primo):
            ax.annotate(md.num(v, 1) + "%", xy=(i, v / 2), ha="center", va="center",
                        color="white", fontsize=10)
        ax.set_xticks(x)
        # Etichette su una riga sola: con due righe la legenda sottostante finirebbe
        # sopra la seconda, e qui i valori sono due, quindi in orizzontale ci stanno.
        ax.set_xticklabels(["%s, %s" % (q[0], q[1]) for q in quote])
        ax.set_ylabel("% dei posti a punti")
        ax.set_ylim(0, 100)
        gr.legenda(ax)
        ax.grid(axis="x", visible=False)
    ar.figura("separazione", gr.salva("ragazze_separazione"),
              didascalia="Stessa categoria e stesse eta', prima e dopo la separazione "
                         "delle liste: con la lista condivisa il primo anno prende poco piu' "
                         "di un quarto dei posti, con le liste separate la meta', che li' e' "
                         "quasi automatica.")


def _dettaglio_pcs(v):
    c = v.get("pcs_femminile") or {}
    if not c:
        return ""
    return (" — %s squadre-stagione e %s righe di rosa, con %s atlete italiane "
            "distinte nelle squadre di prima e seconda divisione fra il 2020 e il 2025 —"
            % (md.conta(c.get("squadre_stagione")), md.conta(c.get("righe_rosa")),
               md.conta(c.get("italiane_2020_2025"))))


def _coda_calendario(ce):
    var = list((ce.get("variazioni") or {}).values())
    if var and all(x > 0 for x in var):
        return ": e' anzi cresciuto in tutte e due"
    if var and any(x > 0 for x in var):
        return ": in una categoria e' cresciuto, nell'altra ha perso poco"
    return ""


def rendi(lt):
    v = lt.valori("ragazze")
    dim = lt.tabella("ragazze", "dimensione")
    sep = lt.tabella("ragazze", "separazione")
    conc = lt.tabella("ragazze", "concentrazione")
    cal = lt.tabella("ragazze", "calendario")

    p = [md.sezione("Le ragazze")]
    if not dim:
        p.append(md.paragrafo("*Sezione non disponibile: manca `tab_a`.*"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "Tutto il resto di questo documento riguarda i maschi, e la ragione non e' una "
        "scelta di merito: gli esiti di carriera femminili non erano stati raccolti, quindi "
        "ogni domanda che finisca con «e poi chi ce l'ha fatta?» restava senza risposta. "
        "Molte domande pero' non hanno bisogno di un esito, e su quelle il femminile si "
        "studia eccome."))

    p.append(md.tabella(
        dim["colonne"],
        [[r[0], md.conta(r[1]), md.conta(r[2]), md.num(r[3], 1) + "×",
          md.conta(r[4]), md.conta(r[5]), md.num(r[6], 1) + "×"] for r in dim["righe"]],
        nota=dim["nota"], colonne_conteggio=(1, 2, 4, 5)))

    rap_a = v.get("rapporto_atleti") or {}
    rap_g = v.get("rapporto_gare") or {}
    conf_g = v.get("rapporto_gare_confrontabile") or {}
    if rap_a and conf_g:
        p.append(md.paragrafo(
            "",
            "Il movimento femminile e' piu' piccolo di quello maschile di circa **%s volte** "
            "in Esordienti, e corre da **%s a %s volte** meno gare: le ragazze non sono "
            "semplicemente meno, corrono anche molto meno spesso. Il divario fra i "
            "calendari cresce con l'eta', ed e' piu' largo del divario fra le popolazioni."
            % (md.num(rap_a.get("Esordienti"), 1), md.num(conf_g.get("minimo"), 1),
               md.num(conf_g.get("massimo"), 1))))

    # --- l'esperimento naturale ---------------------------------------------
    if sep:
        p.append(md.sezione("Un cambio di regolamento che vale un esperimento", 3))
        p.append(md.paragrafo(
            "La sezione sui posti ha mostrato che dove le due annate condividono la "
            "classifica il primo anno ne vince una minoranza, e ha usato come controllo il "
            "confronto fra categorie maschili. Le Esordienti femminili permettono un "
            "controllo molto piu' stretto, perche' la fonte ha **cambiato struttura in "
            "corsa**: fino al %s una classifica sola, dal %s due separate."
            # Gli anni non prendono il separatore delle migliaia: e' l'errore che questo
            # progetto ha gia' commesso quattro volte, ed e' documentato in md.conta().
            % ((v.get("separazione_quote") or {}).get("anno", 0) - 1,
               (v.get("separazione_quote") or {}).get("anno"))))
        p.append(md.tabella(
            sep["colonne"],
            [[r[0], r[1], md.conta(r[2]), md.num(r[3], 1) + "%", md.num(r[4], 1) + "%"]
             for r in sep["righe"]], nota=sep["nota"], colonne_conteggio=(2,)))

        sq = v.get("separazione_quote") or {}
        if sq:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    sq.get("dopo", 0) - sq.get("prima", 0) > 10,
                    "separando le classifiche per annata la quota dei posti del primo anno "
                    "sale in modo netto",
                    "**Stessa categoria e stesse eta', in due periodi diversi e quindi con "
                    "ragazze diverse: cambia la struttura della lista, e il primo anno passa "
                    "dal %s%% al %s%% dei posti.** Dei due numeri e' il primo a portare "
                    "l'informazione: con le liste separate ogni annata ha i propri posti, e "
                    "la meta' e' quasi automatica. Con la lista condivisa, invece, il primo "
                    "anno ne prende poco piu' di un quarto, lo stesso ordine del %s%% degli "
                    "Allievi maschi. Il confronto e' piu' stretto di quello fra categorie "
                    "maschili, perche' categoria ed eta' restano le stesse: dove le annate "
                    "condividono la classifica, il primo anno non sparisce perche' ci siano "
                    "meno posti, ma perche' quei posti li vincono le piu' grandi."
                    % (md.num(sq.get("prima"), 1), md.num(sq.get("dopo"), 1),
                       md.num((lt.valori("posti") or {}).get("quota_primo_anno_U17"), 1)))))
        f = lt.figura("ragazze", "separazione")
        if f:
            p.append(md.figura(f["percorso"], f["didascalia"]))

    # --- concentrazione ------------------------------------------------------
    if conc:
        p.append(md.sezione("Le cose che non cambiano", 3))
        p.append(md.tabella(
            conc["colonne"],
            [[r[0]] + [md.num(x, 1) + "%" if x is not None else "—" for x in r[1:]]
             for r in conc["righe"]], nota=conc["nota"]))
        est = v.get("concentrazione_estremi") or {}
        if est:
            p.append(md.paragrafo(
                "",
                "La concentrazione dei punti e' **dello stesso ordine nei due movimenti**: il "
                "decile "
                "migliore ne prende fra il %s%% e il %s%%, che e' l'intervallo gia' visto "
                "confrontando le categorie maschili fra loro. Cambia tutto — la "
                "numerosita', il numero di gare, la struttura delle liste — e la forma "
                "della distribuzione resta molto simile."
                % (md.num(est.get("minimo"), 1), md.num(est.get("massimo"), 1))))

    # --- calendario ----------------------------------------------------------
    if cal:
        ce = v.get("calendario_estremi") or {}
        p.append(md.paragrafo(
            "",
            "Un'ultima differenza, e va nella direzione opposta a quella che ci si "
            "aspetterebbe. Il calendario maschile si e' quasi dimezzato; quello femminile, "
            "nelle categorie che non hanno cambiato struttura, molto meno%s."
            % _coda_calendario(ce)))
        p.append(md.tabella(
            cal["colonne"],
            [[r[0], md.conta(r[1]), md.conta(r[2]),
              ("%+.1f%%" % r[3]).replace(".", ",")] for r in cal["righe"]],
            nota=cal["nota"], colonne_conteggio=(1, 2)))

    p.append(md.paragrafo(
        "",
        "> **Cosa manca, e cosa servirebbe.** Nel periodo studiato la fonte non pubblica "
        "una classifica Under 23 femminile, anche se la categoria esiste nel regolamento "
        "federale e corre insieme alle Elite (Norme Attuative 2027, art. 11.5), "
        "quindi il predittore piu' vicino all'esito, quello che nel maschile porta quasi "
        "tutta l'informazione, qui non c'e'. Gli esiti di carriera sono ora "
        "scaricati%s, ma le divisioni professionistiche femminili nascono nel 2020: prima "
        "esisteva una categoria sola, quindi «professionista» non e' definibile allo stesso "
        "modo e le coorti utilizzabili sono solo le piu' recenti. Finche' quel nodo non e' "
        "sciolto, questa sezione resta descrittiva." % _dettaglio_pcs(v)))

    return (chr(10) * 2).join(x.strip() for x in p if x)
