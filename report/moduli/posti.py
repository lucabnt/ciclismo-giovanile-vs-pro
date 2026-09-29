"""
Quanti posti ci sono in classifica, e chi se li prende.

DA DOVE NASCE
    Da una correzione. Le sezioni sull'attrito e sui passaggi di categoria spiegavano il
    crollo delle presenze dicendo che «la classifica si accorcia»: al primo anno di una
    categoria ci sarebbero meno posti che al secondo. La spiegazione e' sbagliata, o
    meglio, e' vera per la ragione sbagliata, e questa sezione la smonta.

LA STRUTTURA DELLE LISTE, CHE CAMBIA TUTTO
    Negli Esordienti maschili la fonte pubblica **due classifiche separate**, una per
    annata: primo e secondo anno non si fanno concorrenza, ognuno corre le proprie gare e
    ha la propria graduatoria. In Allievi, Juniores e Under 23 la classifica e' **una
    sola** e le annate convivono: un Allievo di primo anno prende punti nelle stesse gare
    del secondo anno, e nella stessa lista.

    Il fatto e' documentato in `docs/verifica_dati_giovanile.md` (liste disgiunte contro
    liste annidate) ed e' registrato in `LISTE_DISGIUNTE`. Qui se ne traggono le
    conseguenze, che nessuna sezione aveva tratto.

I DUE MECCANISMI, CHE VANNO SEPARATI
    **I posti calano davvero.** Il numero di classificazioni di gara scende salendo di
    categoria, e questo restringe la lista per ragioni che non riguardano i ragazzi.

    **Ma il crollo del primo anno non viene da li'.** Dove la lista e' unica, le gare
    sono le stesse per le due annate: se il primo anno prende una minoranza dei posti e'
    perche' corre contro ragazzi piu' grandi, non perche' i posti siano meno.

    Gli Esordienti sono il caso di controllo che lo dimostra: dove le liste sono
    separate, le due annate si dividono i posti quasi a meta'.

COME SI CONTANO I POSTI
    Ogni gara assegna cinque piazzamenti a punti, dal primo al quinto. La somma dei
    piazzamenti nei primi cinque di tutti gli atleti di una categoria e' quindi il numero
    di posti messi in palio, e diviso cinque da' il numero di gare. E' una stima
    indiretta: la fonte non pubblica il calendario, ma pubblica i piazzamenti.

    Per l'Under 23 la stima e' un **limite inferiore**, perche' la lista sorgente contiene
    anche gli Elite, che qui sono fuori dalla finestra d'eta' e i cui piazzamenti non
    vengono contati.

E LA CONCENTRAZIONE
    Ultima domanda, che e' quella che si fanno tutti guardando una classifica: si
    piazzano sempre gli stessi? Si misura con la quota dei punti che va al decile
    migliore e con l'indice di Gini, categoria per categoria e annata per annata.
"""
import os
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, LISTE_DISGIUNTE, CATEGORIE, cfg   # noqa: E402
from lib_risultati import Archivio                                      # noqa: E402
import lib_markdown as md                                               # noqa: E402
import lib_grafici as gr                                                # noqa: E402

W = "https://en.wikipedia.org/wiki/"
ORDINE = ("U15", "U17", "U19", "U23")
NOMI = {"U15": "Esordienti", "U17": "Allievi", "U19": "Juniores", "U23": "Under 23"}
MIN_ATLETI = 30          # sotto questa soglia una distribuzione non si legge


def liste_separate(sesso):
    """Le categorie in cui ogni annata ha la propria classifica, dalla fonte."""
    return {CATEGORIE[slug][0] for slug in LISTE_DISGIUNTE
            if slug in CATEGORIE and CATEGORIE[slug][1] == sesso}


def gini(valori):
    """Quanto sono concentrati i punti: 0 tutti uguali, 1 tutti a una persona sola."""
    v = sorted(valori)
    n, s = len(v), sum(valori)
    if n < 2 or s <= 0:
        return None
    cumulata = sum((i + 1) * x for i, x in enumerate(v))
    return 2 * cumulata / (n * s) - (n + 1) / n


def calcola():
    sesso = cfg("studio", "sesso")
    db = sqlite3.connect(DB_ANALISI)
    separate = liste_separate(sesso)

    stagioni = [r[0] for r in db.execute(
        """SELECT DISTINCT season FROM tab_a
           WHERE sesso = ? AND cat_year IS NOT NULL AND flag_stagione IS NULL
           ORDER BY 1""", (sesso,))]
    if not stagioni:
        print("   posti: nessuna stagione utilizzabile, salto il modulo")
        return

    with Archivio("posti") as ar:
        ar.valore("stagioni", [min(stagioni), max(stagioni)])
        ar.valore("categorie_liste_separate", sorted(separate))

        # --- 1. quanti posti mette in palio ogni categoria -------------------
        righe, gare_cat = [], {}
        for cat in ORDINE:
            r = db.execute(
                """SELECT COUNT(*), SUM(top5), COUNT(DISTINCT season)
                   FROM tab_a WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL
                     AND flag_stagione IS NULL""", (sesso, cat)).fetchone()
            n, posti, n_stagioni = r
            if not posti:
                continue
            annate = db.execute(
                """SELECT COUNT(DISTINCT cat_year) FROM tab_a
                   WHERE sesso = ? AND category = ?""", (sesso, cat)).fetchone()[0]
            gare = posti / 5 / n_stagioni
            gare_cat[cat] = gare
            righe.append([NOMI[cat], annate,
                          "sì" if cat in separate else "no",
                          round(gare), round(posti / n_stagioni),
                          round(n / n_stagioni), round(posti / n, 2)])
        ar.tabella(
            "disponibili", righe,
            colonne=["categoria", "annate", "una lista per annata",
                     "classificazioni di gara per stagione", "posti a punti per stagione",
                     "atleti in classifica per stagione", "posti per atleta"],
            titolo="Quanti posti mette in palio ogni categoria",
            nota="i posti sono stimati dai piazzamenti nei primi cinque, cinque per gara; "
                 "negli Esordienti, che hanno una classifica per annata, il conteggio somma "
                 "i due calendari; per l'Under 23 sono un limite inferiore, perche' la "
                 "lista sorgente contiene anche gli Elite, esclusi dalla finestra d'eta'")
        if gare_cat:
            ar.valore("gare_per_stagione",
                      {c: round(g) for c, g in gare_cat.items()})

        # --- 2. come si dividono i posti fra le annate -----------------------
        righe_q, quote = [], {}
        for cat in ORDINE:
            per_anno = list(db.execute(
                """SELECT cat_year, COUNT(*), SUM(top5) FROM tab_a
                   WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL
                     AND flag_stagione IS NULL
                   GROUP BY 1 ORDER BY 1""", (sesso, cat)))
            totale = sum(p for _, _, p in per_anno)
            if not totale:
                continue
            for anno, n, posti in per_anno:
                q = 100 * posti / totale
                righe_q.append([NOMI[cat], anno, n, posti, round(q, 1),
                                round(posti / n, 2)])
                quote.setdefault(cat, []).append((anno, round(q, 1)))
        ar.tabella(
            "quote", righe_q,
            colonne=["categoria", "anno di categoria", "atleti", "posti presi",
                     "quota dei posti", "posti per atleta"],
            titolo="Come si dividono i posti fra le annate",
            nota="dove la classifica e' unica le gare sono le stesse per tutte le "
                 "annate, quindi la quota misura la concorrenza e non la disponibilita'")
        ar.valore("quote_per_annata", quote)
        for cat in ORDINE:
            if cat in quote and quote[cat]:
                ar.valore("quota_primo_anno_%s" % cat, quote[cat][0][1])

        # --- 3. si piazzano sempre gli stessi? -------------------------------
        righe_c = []
        for cat in ORDINE:
            for anno in sorted({r[0] for r in db.execute(
                    """SELECT DISTINCT cat_year FROM tab_a
                       WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL""",
                    (sesso, cat))}):
                decili, gini_v, n_tot = [], [], 0
                for stagione in stagioni:
                    punti = [r[0] for r in db.execute(
                        """SELECT points_raw FROM tab_a
                           WHERE sesso = ? AND category = ? AND cat_year = ?
                             AND season = ? AND points_raw > 0""",
                        (sesso, cat, anno, stagione))]
                    if len(punti) < MIN_ATLETI:
                        continue
                    punti.sort(reverse=True)
                    k = max(1, len(punti) // 10)
                    decili.append(100 * sum(punti[:k]) / sum(punti))
                    g = gini(punti)
                    if g is not None:
                        gini_v.append(g)
                    n_tot += len(punti)
                if not decili:
                    continue
                righe_c.append([NOMI[cat], anno, len(decili), round(n_tot / len(decili)),
                                round(sum(decili) / len(decili), 1),
                                round(sum(gini_v) / len(gini_v), 3)])
        ar.tabella(
            "concentrazione", righe_c,
            colonne=["categoria", "anno di categoria", "stagioni", "atleti per stagione",
                     "punti presi dal 10% migliore", "Gini"],
            titolo="Quanto sono concentrati i punti",
            nota="medie sulle stagioni; il Gini vale 0 se tutti hanno gli stessi punti e "
                 "1 se li ha una persona sola")
        if righe_c:
            decili = [r[4] for r in righe_c]
            gini_tutti = [r[5] for r in righe_c]
            ar.valore("decile_minimo", min(decili))
            ar.valore("decile_massimo", max(decili))
            ar.valore("gini_minimo", min(gini_tutti))
            ar.valore("gini_massimo", max(gini_tutti))

        # --- 4. il calendario si accorcia, di stagione in stagione -----------
        # E' la domanda che viene naturale dopo aver contato i posti: quei posti sono
        # sempre stati tanti? La risposta e' no, e vale la pena separarla dal confronto
        # fra categorie, che riguarda le eta' e non gli anni.
        righe_t, serie = [], {}
        for cat in ORDINE:
            per_stagione = {st: n for st, n in db.execute(
                """SELECT season, SUM(top5) / 5.0 FROM tab_a
                   WHERE sesso = ? AND category = ? AND cat_year IS NOT NULL
                   GROUP BY 1""", (sesso, cat))}
            if len(per_stagione) < 5:
                continue
            serie[cat] = per_stagione
        anni = sorted(set.intersection(*[set(s.keys()) for s in serie.values()])) if serie else []
        anni = [a for a in anni if a in stagioni]          # niente stagioni anomale
        if len(anni) >= 5:
            primo, ultimo = anni[0], anni[-1]
            for cat in ORDINE:
                if cat not in serie:
                    continue
                a0, a1 = serie[cat][primo], serie[cat][ultimo]
                righe_t.append([NOMI[cat], round(a0), round(a1),
                                round(100 * (a1 - a0) / a0, 1)])
            ar.tabella(
                "andamento", righe_t,
                colonne=["categoria", "gare nel %d" % primo, "gare nel %d" % ultimo,
                         "variazione"],
                titolo="Quante gare c'erano, e quante ce ne sono",
                nota="stime dai piazzamenti; le stagioni anomale sono escluse dagli "
                     "estremi ma non dal grafico")
            ar.valore("andamento_estremi", {"primo": primo, "ultimo": ultimo})
            ar.valore("calo_massimo", min(r[3] for r in righe_t))
            ar.valore("serie_gare",
                      {c: {str(k): round(v) for k, v in s.items()} for c, s in serie.items()})

        # --- 5. quanta parte dei posti va a chi arrivera' --------------------
        righe_p = []
        for cat in ORDINE:
            r = db.execute(
                """SELECT SUM(CASE WHEN b.PRO = 1 THEN a.top5 ELSE 0 END) * 100.0 / SUM(a.top5),
                          SUM(CASE WHEN b.PRO = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
                   FROM tab_a a JOIN tab_b b USING(athlete_id)
                   WHERE a.sesso = ? AND a.category = ? AND a.cat_year IS NOT NULL
                     AND a.birth_year BETWEEN ? AND ?""",
                (sesso, cat) + tuple(cfg("coorti", "domanda_a_c"))).fetchone()
            if not r or r[0] is None:
                continue
            righe_p.append([NOMI[cat], round(r[1], 1), round(r[0], 1),
                            round(r[0] / r[1], 1) if r[1] else None])
        if righe_p:
            ar.tabella(
                "futuri_pro", righe_p,
                colonne=["categoria", "quota dei classificati", "quota dei posti presi",
                         "rapporto"],
                titolo="Quanta parte dei posti va a chi diventera' professionista",
                nota="coorti in studio; il rapporto dice quante volte i futuri "
                     "professionisti sono sovrarappresentati nei piazzamenti a punti")
            ar.valore("pro_quota_posti", {r[0]: r[2] for r in righe_p})

        disegna(righe_q, righe_c, separate, ar,
                {c: {str(k): round(x) for k, x in st.items()}
                 for c, st in serie.items()})

    print("   posti: gare per stagione %s; il primo anno prende il %s%% dei posti in %s"
          % (", ".join("%s %d" % (c, round(g)) for c, g in gare_cat.items()),
             quote.get("U17", [(1, None)])[0][1], NOMI["U17"]))


def disegna(righe_q, righe_c, separate, ar, ar_serie=None):
    gr.stile()
    inverso = {v: k for k, v in NOMI.items()}

    # --- quota dei posti per annata: la figura che smonta «meno posti» -------
    categorie = [c for c in ORDINE if any(r[0] == NOMI[c] for r in righe_q)]
    x = list(range(len(categorie)))
    with gr.figura("Quanta parte dei posti prende ogni annata", altezza=3.8) as (f, ax):
        base = [0.0] * len(categorie)
        for anno in (1, 2, 3, 4):
            valori = []
            for cat in categorie:
                v = [r[4] for r in righe_q if r[0] == NOMI[cat] and r[1] == anno]
                valori.append(v[0] if v else 0.0)
            if not any(valori):
                continue
            ax.bar(x, valori, 0.55, bottom=base,
                   color=gr.COLORI[(anno - 1) % len(gr.COLORI)],
                   label="%d° anno" % anno)
            for i, (v, b) in enumerate(zip(valori, base)):
                if v >= 8:
                    ax.annotate(md.num(v, 1) + "%", xy=(i, b + v / 2), ha="center",
                                va="center", fontsize=9, color="white")
            base = [b + v for b, v in zip(base, valori)]
        ax.set_xticks(x)
        ax.set_xticklabels([NOMI[c] for c in categorie])
        ax.set_ylabel("% dei posti a punti")
        ax.set_ylim(0, 100)
        gr.legenda(ax)
        # Quale categoria abbia le classifiche separate lo dice la didascalia: dentro la
        # barra il testo sarebbe piu' largo della barra stessa e verrebbe tagliato, e
        # sotto l'etichetta si accavallerebbe alla vicina.
        ax.grid(axis="x", visible=False)
    ar.figura("quote", gr.salva("posti_quote"),
              didascalia="Gli Esordienti sono l'unica categoria in cui ogni annata ha la "
                         "propria classifica, e infatti i posti si dividono quasi a meta'. "
                         "Nelle altre la lista e' una sola e le gare sono le stesse per "
                         "tutti: li' il primo anno ne prende una minoranza, che e' "
                         "concorrenza e non scarsita' di posti.")

    # --- concentrazione: uguale dappertutto ---------------------------------
    categorie_c = [NOMI[c] for c in ORDINE if any(r[0] == NOMI[c] for r in righe_c)]
    annate = sorted({r[1] for r in righe_c})
    x = list(range(len(categorie_c)))
    larghezza = 0.8 / max(len(annate), 1)
    with gr.figura("Quanta parte dei punti va al dieci per cento migliore",
                   altezza=3.6) as (f, ax):
        # Ogni categoria ha un numero diverso di annate: il gruppo va centrato sulle sue,
        # altrimenti le categorie con due annate risultano spostate a sinistra rispetto
        # all'etichetta.
        etichettate = set()
        for i, cat in enumerate(categorie_c):
            sue = [r for r in righe_c if r[0] == cat]
            for j, r in enumerate(sorted(sue, key=lambda r: r[1])):
                pos = i + (j - (len(sue) - 1) / 2) * larghezza
                colore = gr.COLORI[(r[1] - 1) % len(gr.COLORI)]
                ax.bar(pos, r[4], larghezza * 0.9, color=colore,
                       label=("%d° anno" % r[1]) if r[1] not in etichettate else None)
                etichettate.add(r[1])
        ax.axhline(10, color=gr.GRIGIO, linewidth=1.2, linestyle="--")
        ax.annotate("con i punti divisi in parti uguali sarebbe 10%",
                    xy=(0.02, 0.21), xycoords="axes fraction", ha="left", va="bottom",
                    fontsize=9, color=gr.GRIGIO)
        ax.set_xticks(x)
        ax.set_xticklabels(categorie_c)
        ax.set_ylabel("% dei punti della categoria")
        ax.set_ylim(0, 60)
        gr.legenda(ax)
        ax.grid(axis="x", visible=False)
    serie = ar_serie or {}
    if serie:
        with gr.figura("Quante gare, stagione per stagione", altezza=3.6) as (f, ax):
            for i, cat in enumerate(c for c in ORDINE if c in serie):
                anni = sorted(int(a) for a in serie[cat])
                ax.plot(anni, [serie[cat][str(a)] for a in anni], marker="o",
                        markersize=3, linewidth=1.8,
                        color=gr.COLORI[i % len(gr.COLORI)], label=NOMI[cat])
            ax.set_ylabel("classificazioni di gara stimate")
            ax.legend(frameon=False, fontsize=9)
            ax.grid(axis="x", visible=False)
        ar.figura("andamento", gr.salva("posti_andamento"),
                  didascalia="Il calo e' comune a tutte le categorie e comincia molto "
                             "prima della pandemia. Il 2020 e' la stagione dimezzata dal "
                             "covid, e dopo di essa il calendario non e' tornato ai "
                             "valori precedenti.")

    ar.figura("concentrazione", gr.salva("posti_concentrazione"),
              didascalia="La concentrazione e' quasi la stessa a tredici e a ventidue "
                         "anni: salendo di categoria i punti non si concentrano in meno "
                         "mani.")


def rendi(lt):
    v = lt.valori("posti")
    disp = lt.tabella("posti", "disponibili")
    quote = lt.tabella("posti", "quote")
    conc = lt.tabella("posti", "concentrazione")

    p = [md.sezione("Quanti posti ci sono, e chi se li prende")]

    if not disp:
        p.append(md.paragrafo("*Sezione non disponibile: manca `tab_a`.*"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    separate = set(v.get("categorie_liste_separate") or [])
    nomi_sep = ", ".join(NOMI[c] for c in ORDINE if c in separate) or "nessuna categoria"

    p.append(md.paragrafo(
        "Le sezioni precedenti hanno mostrato che al cambio di categoria la classifica si "
        "svuota. La spiegazione naturale e' che ci siano meno posti, ed e' la lettura che "
        "circola di solito. Vale la pena controllarla, perche' i posti si possono contare."))

    p.append(md.metodo(
        "Due strutture diverse, e la differenza cambia la lettura",
        "La fonte non pubblica una classifica sola per tutte le categorie giovanili. In "
        "**%s** ogni annata ha la propria graduatoria: primo e secondo anno corrono gare "
        "distinte e non si fanno concorrenza. In tutte le altre categorie la classifica e' "
        "**una sola** e le annate convivono, per cui un atleta al primo anno prende punti "
        "nelle stesse gare dei piu' grandi.\n\n"
        "La differenza non e' un dettaglio di archivio: rende le due situazioni non "
        "confrontabili, e permette di usare la prima come **caso di controllo** per "
        "capire cosa succeda nella seconda.\n\n"
        "I posti si contano cosi': ogni gara assegna cinque piazzamenti a punti, quindi "
        "la somma dei piazzamenti nei primi cinque e' il numero di posti messi in palio, e "
        "diviso cinque stima il numero di **classificazioni di gara**: non le gare "
        "davvero corse, ma quelle che hanno lasciato una traccia nella fonte. La fonte "
        "non pubblica il calendario, ma pubblica i piazzamenti." % nomi_sep,
        [("La verifica sulla struttura delle liste",
          "../docs/verifica_dati_giovanile.md")]))

    righe_d = [[r[0], md.conta(r[1]), r[2], md.conta(r[3]), md.conta(r[4]),
                md.conta(r[5]), md.num(r[6], 2)] for r in disp["righe"]]
    p.append(md.tabella(disp["colonne"], righe_d, nota=disp["nota"]))

    gare = v.get("gare_per_stagione") or {}
    if gare:
        p.append(md.paragrafo(
            "",
            md.afferma(
                gare.get("U23", 0) < gare.get("U15", 1),
                "il numero di classificazioni di gara cala salendo di categoria",
                "**Una parte della lettura corrente e' giusta: i posti calano davvero.** "
                "Si passa da %s classificazioni di gara per stagione in Esordienti a %s in "
                "Under 23. Il calendario si accorcia, e con esso la lista, per ragioni che "
                "non hanno nulla a che vedere con il valore dei ragazzi."
                % (md.conta(gare.get("U15")), md.conta(gare.get("U23"))))))

    p.append(md.paragrafo(
        "",
        "> **Un confronto da fare con una cautela.** Negli Esordienti le due annate hanno "
        "classifiche distinte e corrono gare distinte, quindi il conteggio somma i due "
        "calendari; nelle altre categorie la classifica e' una sola e le annate corrono "
        "insieme. Il numero degli Esordienti e' quindi comparabile agli altri solo "
        "accettando che a quell'eta' si corra davvero separati. Non e' piu' un'assunzione: le "
        "Norme Attuative della federazione prevedono che le due annate corrano "
        "separatamente, e che anche quando la gara e' unica la classifica sia distinta per "
        "fascia d'eta' (art. 4.2.1 e 4.2.5, con l'eccezione dei meno di dieci partenti "
        "all'art. 4.2.4). La verifica sui regolamenti sta in "
        "`docs/verifica_dati_giovanile.md`. Chi preferisce comunque la lettura prudente "
        "puo' dimezzare il conteggio: resta un calo anche partendo da meta'."))

    p.append(md.sezione("Ma il primo anno non sparisce per mancanza di posti", 3))

    righe_q = [[r[0], md.conta(r[1]), md.conta(r[2]), md.conta(r[3]),
                md.num(r[4], 1) + "%", md.num(r[5], 2)] for r in quote["righe"]]
    p.append(md.tabella(quote["colonne"], righe_q, nota=quote["nota"],
                        colonne_conteggio=(2, 3)))

    per_annata = v.get("quote_per_annata") or {}
    u15 = per_annata.get("U15") or []
    u17 = per_annata.get("U17") or []
    if u15 and u17:
        p.append(md.paragrafo(
            "",
            md.afferma(
                abs(u15[0][1] - 50) < 5 and u17[0][1] < 40,
                "dove le liste sono separate le annate si dividono i posti quasi a meta', "
                "dove la lista e' unica il primo anno ne prende una minoranza",
                "**Il confronto e' netto.** In Esordienti, dove ogni annata ha la propria "
                "classifica, il primo anno prende il **%s%%** dei posti: praticamente "
                "meta', come dev'essere quando nessuno fa concorrenza a nessuno. In "
                "Allievi, dove la lista e' una sola e le gare sono le stesse, il primo "
                "anno ne prende il **%s%%**."
                % (md.num(u15[0][1], 1), md.num(u17[0][1], 1)))))

        p.append(md.paragrafo(
            "",
            "Quei due numeri, messi uno accanto all'altro, dicono che il crollo del primo "
            "anno **non e' una questione di posti disponibili**. I posti sono gli stessi "
            "per le due annate, perche' sono le stesse gare: quello che cambia e' chi li "
            "vince. Un Allievo al primo anno corre contro ragazzi che hanno un anno di "
            "sviluppo in piu', e i piazzamenti a punti se li prendono loro."))

    u23 = per_annata.get("U23") or []
    if len(u23) >= 3:
        p.append(md.paragrafo(
            "",
            "L'Under 23 lo mostra su quattro annate invece che su due: la quota dei posti "
            "sale da %s%% al primo anno fino a %s%% al quarto. E' lo stesso meccanismo, "
            "osservato piu' a lungo."
            % (md.num(u23[0][1], 1), md.num(max(q for _, q in u23), 1))))

    f = lt.figura("posti", "quote")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.paragrafo(
        "",
        "> **Cosa se ne ricava per il resto del documento.** Dove si legge che al primo "
        "anno di una categoria «la lista e' piu' corta», la frase va intesa cosi': la "
        "lista di quell'annata e' piu' corta perche' i suoi atleti vincono meno posti, non "
        "perche' la fonte pubblichi meno righe. Nelle categorie a lista unica non esiste "
        "una classifica del primo anno: esiste una classifica sola, che noi dividiamo per "
        "annata quando calcoliamo il percentile."))

    # --- concentrazione ------------------------------------------------------
    p.append(md.sezione("Quanto sono concentrati i punti", 3))

    p.append(md.paragrafo(
        "Chi guarda una classifica giovanile ha spesso l'impressione che i punti se li "
        "dividano sempre le stesse facce. Quello che si misura qui e' meta' di quella "
        "impressione: quanta parte del totale finisce al decile migliore, chiunque esso "
        "sia. La concentrazione dei punti e la persistenza delle stesse persone sono due "
        "cose diverse, e una classifica puo' essere concentratissima e rinnovare i volti "
        "ogni stagione: chi resta di anno in anno lo dice la correlazione fra stagioni "
        "consecutive, misurata piu' avanti, non questa tabella."))

    righe_c = [[r[0], md.conta(r[1]), md.conta(r[2]), md.conta(r[3]),
                md.num(r[4], 1) + "%", md.num(r[5], 3)] for r in conc["righe"]]
    p.append(md.tabella(conc["colonne"], righe_c, nota=conc["nota"],
                        colonne_conteggio=(2, 3)))

    dmin, dmax = v.get("decile_minimo"), v.get("decile_massimo")
    gmin, gmax = v.get("gini_minimo"), v.get("gini_massimo")
    if dmin is not None:
        p.append(md.paragrafo(
            "",
            md.afferma(
                (dmax - dmin) < 15,
                "la quota dei punti presa dal decile migliore varia poco fra categorie e "
                "annate",
                "**Il dieci per cento migliore prende fra il %s%% e il %s%% dei punti**, e "
                "la cosa notevole e' che questa quota non cambia salendo di categoria: e' "
                "la stessa a tredici anni e a ventidue. Il Gini si muove fra %s e %s, che "
                "e' un intervallo stretto per una misura che potrebbe andare da 0 a 1."
                % (md.num(dmin, 1), md.num(dmax, 1), md.num(gmin, 3), md.num(gmax, 3)))))

        p.append(md.paragrafo(
            "",
            "E' un risultato che vale come risposta a due domande diverse. Alla prima, se "
            "si piazzino sempre gli stessi, la risposta e' si': i punti sono molto "
            "concentrati, e un decile che ne prende quattro volte la propria quota e' "
            "molta concentrazione. Alla seconda, se la selezione si stringa con l'eta', la "
            "risposta e' no: la forma della distribuzione e' gia' quella a tredici anni e "
            "resta quella fino all'Under 23."))

    f = lt.figura("posti", "concentrazione")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    # --- il calendario nel tempo --------------------------------------------
    and_ = lt.tabella("posti", "andamento")
    estremi = v.get("andamento_estremi") or {}
    if and_:
        p.append(md.sezione("Quanti posti c'erano prima", 3))
        p.append(md.paragrafo(
            "Contati i posti, viene naturale chiedersi se siano sempre stati tanti. La "
            "risposta e' no, ed e' la cosa piu' inattesa di questa sezione."))
        righe_t = [[r[0], md.conta(r[1]), md.conta(r[2]),
                    ("%+.1f%%" % r[3]).replace(".", ",")] for r in and_["righe"]]
        p.append(md.tabella(and_["colonne"], righe_t, nota=and_["nota"],
                            colonne_conteggio=(1, 2)))
        calo = v.get("calo_massimo")
        if calo is not None:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    calo < -10,
                    "il numero di gare stimate cala in tutte le categorie fra la prima e "
                    "l'ultima stagione osservata",
                    "**Il calendario giovanile italiano osservabile nella fonte si e' quasi "
                    "dimezzato.** Fra il %s "
                    "e il %s le classificazioni di gara calano in ogni categoria, fino a "
                    "%s%% in Under 23. Non e' un effetto della pandemia: il 2020 e' un "
                    "crollo a se', e dopo di esso il calendario non e' tornato ai valori "
                    "precedenti."
                    % (estremi.get("primo"), estremi.get("ultimo"),
                       md.num(calo, 1)))))
            p.append(md.paragrafo(
                "",
                "Prima di prenderlo per buono va considerata l'alternativa piu' ovvia, "
                "cioe' che a calare sia la copertura della fonte e non il calendario "
                "vero. Il controllo si puo' fare solo dove esistono i tesserati "
                "federali, cioe' dal 2018: in quella finestra i tesserati Esordienti "
                "calano di circa un decimo e le gare stimate di quasi un quinto. Il "
                "movimento si sta restringendo, e il calendario si restringe piu' in "
                "fretta del movimento."))
            p.append(md.paragrafo(
                "",
                "> **Perche' riguarda il resto dello studio.** Le coorti in esame hanno "
                "corso quando le gare erano di piu'. Un ragazzo di oggi ha meno occasioni "
                "di andare a punti di quante ne avesse un suo pari di quindici anni fa, "
                "il che rende la classifica di oggi un filtro piu' stretto. I confronti "
                "fra coorti di questo documento sono aggiustati per anno di nascita, ma "
                "vale la pena saperlo quando si legge un percentile recente accanto a uno "
                "vecchio."))

        f_and = lt.figura("posti", "andamento")
        if f_and:
            p.append(md.figura(f_and["percorso"], f_and["didascalia"]))

    # --- quanta parte dei posti prendono i futuri professionisti ------------
    pro = lt.tabella("posti", "futuri_pro")
    if pro:
        p.append(md.paragrafo(
            "",
            "Un'ultima domanda, che lega questa sezione al resto del documento: quanta "
            "parte dei posti va a chi poi diventera' professionista?"))
        righe_p = [[r[0], md.num(r[1], 1) + "%", md.num(r[2], 1) + "%",
                    md.num(r[3], 1) + " volte"] for r in pro["righe"]]
        p.append(md.tabella(pro["colonne"], righe_p, nota=pro["nota"]))
        quote_pro = v.get("pro_quota_posti") or {}
        esord = next((r for r in pro["righe"] if r[0] == "Esordienti"), None)
        if quote_pro and esord:
            p.append(md.paragrafo(
                "",
                "Gia' in Esordienti i futuri professionisti prendono il **%s%%** dei "
                "posti pur essendo il %s%% dei classificati, cioe' %s volte la loro "
                "quota. E' la stessa cosa che le sezioni sui punteggi mostrano con i "
                "percentili, vista dal lato dei posti invece che da quello degli atleti: "
                "a tredici anni il vantaggio si vede gia'."
                % (md.num(quote_pro.get("Esordienti"), 1), md.num(esord[1], 1),
                   md.num(esord[3], 1))))

    p.append(md.paragrafo(
        "",
        "> **Un limite della stima dei posti.** Contare le gare dai piazzamenti assume "
        "che ogni gara assegni cinque posti e che tutti i piazzamenti finiscano in "
        "classifica. Per l'Under 23 il conto e' un limite inferiore, perche' la lista "
        "sorgente comprende anche gli Elite, che qui restano fuori dalla finestra d'eta': "
        "le gare vere sono di piu' di quelle stimate, e i posti che i giovani non prendono "
        "vanno in parte a corridori piu' grandi che questo studio non conta."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
