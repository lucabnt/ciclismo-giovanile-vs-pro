"""
Quanta parte del ciclismo giovanile italiano si vede da questa classifica.

LA DOMANDA CHE MANCAVA
    Tutto il resto del documento parla di atleti «in classifica». Ma quanti sono, questi,
    rispetto a tutti i ragazzi tesserati? Finche' il numero dei tesserati non era
    disponibile, la risposta era «meno di tutti, non si sa di quanto», e ogni percentuale
    restava senza scala.

    I dati di tesseramento della Federazione Ciclistica Italiana permettono di
    rispondere, e la risposta cambia il modo di leggere il resto: la popolazione studiata
    e' una **minoranza selezionata**, non l'insieme dei giovani ciclisti.

DUE CONFRONTI, NON UNO
    Il primo e' la copertura: quanti dei tesserati compaiono in classifica in una
    stagione. Dice quanto e' stretto il filtro.

    Il secondo e' la forma dell'imbuto. I tesserati calano di categoria in categoria, e
    anche i classificati calano. Se calassero allo stesso ritmo, l'attrito che si vede
    nella classifica sarebbe l'attrito vero dello sport; se la classifica calasse molto
    piu' in fretta, misurerebbe soprattutto la difficolta' crescente di andare a punti.
    E' la verifica esterna della cautela dichiarata nella sezione sull'attrito.

IL LIMITE CHE NON SI PUO' AGGIRARE
    I dati di tesseramento partono dal 2020, le coorti dello studio hanno corso nelle
    categorie giovanili fra il 2009 e il 2023. La copertura si misura quindi su stagioni
    diverse da quelle studiate, e vale come ordine di grandezza, non come correzione da
    applicare ai numeri delle coorti. Il testo lo dice invece di lasciarlo intuire.
"""
import csv
import math
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

TESSERATI = os.path.join("riferimenti", "tesserati_fci.csv")

# Il 2020 non entra nei confronti: la stagione e' stata dimezzata dalla pandemia e la
# classifica ne risente in modo sproporzionato rispetto al tesseramento, che si paga a
# inizio anno. Tenerla dentro farebbe sembrare la copertura molto piu' bassa di quanto e'.
ANOMALE = set(map(int, cfg("stagioni", "anomale").keys()))

CATEGORIE = ("U15", "U17", "U19", "U23")

# Il tesseramento e' cresciuto durante la pandemia — gli sport all'aperto erano una delle
# poche cose permesse — e le due stagioni successive non rappresentano un regime
# ordinario. Si tengono nei conti, ma separate: mescolarle con le altre farebbe sembrare
# la copertura piu' bassa di quanto e', perche' il denominatore era gonfio.
COVID = (2021, 2022)
NOMI = {"U15": "Esordienti", "U17": "Allievi", "U19": "Juniores", "U23": "Under 23"}


def leggi_tesserati(sesso):
    """Il CSV di riferimento, filtrato sul sesso dello studio.

    Le righe che iniziano con `//` sono la documentazione della fonte: stanno nel file
    perche' un dato trascritto a mano senza la propria provenienza e' inutilizzabile.
    """
    if not os.path.exists(TESSERATI):
        return {}
    with open(TESSERATI, encoding="utf-8") as f:
        righe = [r for r in f if not r.startswith("//")]
    out = {}
    for r in csv.DictReader(righe):
        if r["sesso"] != sesso:
            continue
        out[(int(r["anno"]), r["categoria"])] = {
            "tesserati": int(r["tesserati"]),
            "anni_eta": int(r["anni_eta"]) if r["anni_eta"] else None,
            "fonte": r["fonte"]}
    return out


def _tendenza(punti):
    """Regressione log-lineare: restituisce la funzione stimata e il tasso annuo.

    Log-lineare e non lineare perche' una popolazione cresce o cala in proporzione a se'
    stessa. La scelta non e' innocua e fa parte di cio' che il back-test mette alla prova.
    """
    n = len(punti)
    sx = sum(a for a, _ in punti)
    sy = sum(math.log(v) for _, v in punti)
    sxx = sum(a * a for a, _ in punti)
    sxy = sum(a * math.log(v) for a, v in punti)
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a0 = (sy - b * sx) / n
    return (lambda x: math.exp(a0 + b * x)), b


def calcola():
    sesso = cfg("studio", "sesso")
    tess = leggi_tesserati(sesso)
    if not tess:
        print("   copertura: manca %s, salto il modulo" % TESSERATI)
        return

    db = sqlite3.connect(DB_ANALISI)
    anni = sorted({a for a, _ in tess} - ANOMALE)

    def in_classifica(cat, anno):
        return db.execute("""SELECT COUNT(DISTINCT athlete_id) FROM tab_a
                             WHERE sesso = ? AND category = ? AND season = ?""",
                          (sesso, cat, anno)).fetchone()[0]

    with Archivio("copertura") as ar:
        ar.valore("anni", [min(anni), max(anni)])
        ar.valore("anni_imbuti", [])
        ar.valore("anni_esclusi", sorted(ANOMALE & {a for a, _ in tess}))

        # --- 1. la copertura, categoria per categoria ------------------------
        righe, tutte = [], []
        for cat in CATEGORIE:
            quote, n_tot, t_tot = [], 0, 0
            for anno in anni:
                v = tess.get((anno, cat))
                if not v:
                    continue
                n = in_classifica(cat, anno)
                quote.append(100 * n / v["tesserati"])
                n_tot += n
                t_tot += v["tesserati"]
            if not quote:
                continue
            righe.append([NOMI[cat], round(t_tot / len(quote)), round(n_tot / len(quote)),
                          round(min(quote), 1), round(max(quote), 1),
                          round(100 * n_tot / t_tot, 1)])
            tutte += quote
        ar.tabella("copertura", righe,
                   colonne=["categoria", "tesserati per stagione",
                            "in classifica per stagione", "minimo", "massimo", "media"],
                   titolo="Quanti dei tesserati compaiono in classifica",
                   nota="stagioni %d-%d, escluse quelle anomale; percentuali per stagione"
                        % (min(anni), max(anni)))
        if tutte:
            ar.valore("copertura_min", round(min(tutte), 1))
            ar.valore("copertura_max", round(max(tutte), 1))
            ar.valore("copertura_media", round(sum(tutte) / len(tutte), 1))

        # --- 2. l'imbuto dei tesserati contro quello della classifica --------
        # I conteggi vanno divisi per l'ampiezza della categoria: l'Under 23 dura
        # quattro anni e gli altri due, quindi i totali non sono confrontabili
        # direttamente. Per anno di eta' lo sono.
        # Le categorie non hanno tutte le stesse stagioni: Esordienti e Allievi partono
        # dal 2018, le altre dal 2020. Il confronto fra imbuti si fa solo sulle stagioni
        # comuni, altrimenti si confronterebbero medie di periodi diversi.
        comuni = [a for a in anni
                  if all((a, c) in tess for c in CATEGORIE)]
        confronto = []
        for cat in CATEGORIE:
            per_anno_t, per_anno_n = [], []
            for anno in comuni:
                v = tess.get((anno, cat))
                if not v or not v["anni_eta"]:
                    continue
                per_anno_t.append(v["tesserati"] / v["anni_eta"])
                per_anno_n.append(in_classifica(cat, anno) / v["anni_eta"])
            if per_anno_t:
                confronto.append([NOMI[cat],
                                  round(sum(per_anno_t) / len(per_anno_t)),
                                  round(sum(per_anno_n) / len(per_anno_n))])
        righe_i = []
        for i, (nome, t, n) in enumerate(confronto):
            if i == 0:
                righe_i.append([nome, t, "—", n, "—"])
            else:
                t0, n0 = confronto[i - 1][1], confronto[i - 1][2]
                righe_i.append([nome, t, round(100 * t / t0, 1), n,
                                round(100 * n / n0, 1)])
        ar.tabella("imbuti", righe_i,
                   colonne=["categoria", "tesserati per anno di eta'",
                            "% del livello precedente", "in classifica per anno di eta'",
                            "% del livello precedente"],
                   titolo="Due imbuti a confronto",
                   nota="medie delle stagioni %d-%d, le sole in cui tutte le categorie "
                        "hanno il dato; i conteggi sono divisi per l'ampiezza della "
                        "categoria, altrimenti l'Under 23 non sarebbe confrontabile con "
                        "le altre" % (min(comuni), max(comuni)))
        ar.valore("anni_imbuti", [min(comuni), max(comuni)] if comuni else [])
        if len(confronto) >= 2:
            ar.valore("residuo_tesserati",
                      round(100 * confronto[-1][1] / confronto[0][1], 1),
                      "quota dei tesserati per anno di eta' che resta dall'ingresso "
                      "all'ultima categoria")
            ar.valore("residuo_classifica",
                      round(100 * confronto[-1][2] / confronto[0][2], 1))
            ar.valore("passi", [[confronto[i][0],
                                 round(100 * confronto[i][1] / confronto[i - 1][1], 1),
                                 round(100 * confronto[i][2] / confronto[i - 1][2], 1)]
                                for i in range(1, len(confronto))])

        # --- 3. quanti posti ci sono davvero --------------------------------
        # --- 3. si possono stimare gli anni mancanti? ------------------------
        # La domanda si risolve provandoci su anni di cui la risposta e' nota: si stima
        # la tendenza sulle stagioni recenti e si prova a prevedere le piu' vecchie.
        # L'errore che si ottiene li' e' il minimo che si otterrebbe estrapolando piu'
        # lontano, e serve a decidere se l'estrapolazione sia una misura o un'illusione.
        serie = sorted((a, tess[(a, "U15")]["tesserati"]) for a in
                       {a for a, c in tess if c == "U15"})
        if len(serie) >= 6:
            base = [(a, v) for a, v in serie if a >= 2021]
            da_prevedere = [(a, v) for a, v in serie if a < 2020]
            f, tasso = _tendenza(base)
            errori = [[a, v, round(f(a)), round(100 * (f(a) / v - 1), 1)]
                      for a, v in da_prevedere]
            ar.tabella("backtest", errori,
                       colonne=["stagione", "tesserati reali", "stimati dalla tendenza",
                                "errore %"],
                       titolo="Provare a stimare anni che gia' si conoscono",
                       nota="tendenza stimata sulle stagioni %d-%d ed estrapolata "
                            "all'indietro" % (base[0][0], base[-1][0]))
            ar.valore("backtest_errore", round(max(abs(e[3]) for e in errori), 0))
            ar.valore("backtest_tasso", round(100 * (math.exp(tasso) - 1), 1))

            # Due scelte di modello entrambe difendibili, per mostrare quanto la stima
            # dipenda da una decisione arbitraria invece che dai dati.
            senza_covid = [(a, v) for a, v in serie if a not in COVID and a != 2020]
            f2, _ = _tendenza(senza_covid)
            anno_studio = 2012
            ar.valore("stime_divergenti",
                      [anno_studio, round(f(anno_studio)), round(f2(anno_studio))],
                      "la stessa estrapolazione con e senza gli anni della pandemia")

        prof = [v["tesserati"] for (a, c), v in tess.items() if c == "PROF"]
        if prof:
            ar.valore("prof_licenze", [min(prof), max(prof)])
        elite = [v["tesserati"] for (a, c), v in tess.items()
                 if c == "ELITE" and a not in ANOMALE]
        if elite:
            ar.valore("elite_licenze", round(sum(elite) / len(elite)))

        if not os.environ.get("SENZA_FIGURE"):
            disegna(righe, ar)
    db.close()
    print("   copertura: %s in classifica su cento tesserati, in media"
          % round(sum(tutte) / len(tutte), 1))


def disegna(righe, ar):
    gr.stile()
    nomi = [r[0] for r in righe]
    medie = [r[5] for r in righe]
    minimi = [r[3] for r in righe]
    massimi = [r[4] for r in righe]
    x = list(range(len(nomi)))
    with gr.figura("Chi si vede, su cento tesserati", altezza=3.6) as (fig, ax):
        ax.bar(x, medie, 0.55, color=gr.COLORI[0])
        for i in x:
            ax.plot([i, i], [minimi[i], massimi[i]], color=gr.GRIGIO, linewidth=1.4)
        ax.set_xticks(x)
        ax.set_xticklabels(nomi)
        ax.set_ylabel("% dei tesserati presenti in classifica")
        ax.set_ylim(0, 100)
        ax.annotate("gli altri 85 su cento corrono senza mai andare a punti,\n"
                    "oppure non corrono su strada",
                    xy=(0.02, 0.92), xycoords="axes fraction", fontsize=9,
                    color=gr.GRIGIO, va="top")
        ax.grid(axis="x", visible=False)
    ar.figura("copertura", gr.salva("copertura_tesserati"),
              didascalia="La barra e' la media delle stagioni, la linea l'intervallo fra "
                         "la stagione piu' bassa e la piu' alta. La stabilita' fra "
                         "categorie e fra anni e' il dato piu' notevole.")


def rendi(lt):
    v = lt.valori("copertura")
    cop = lt.tabella("copertura", "copertura")
    imb = lt.tabella("copertura", "imbuti")

    p = [md.sezione("Quanto del ciclismo giovanile si vede da qui")]

    if not cop:
        p.append(md.paragrafo(
            "*Sezione non disponibile: manca il file dei tesserati FCI "
            "(`riferimenti/tesserati_fci.csv`).*"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    a0, a1 = v.get("anni", [None, None])
    p.append(md.paragrafo(
        "Tutto il resto del documento parla di atleti «in classifica». Quanti sono, "
        "rispetto a tutti i ragazzi tesserati? La domanda non e' retorica: senza la "
        "risposta, ogni percentuale di questo studio resta senza scala."))

    p.append(md.metodo(
        "Da dove viene il numero dei tesserati",
        "Dalla Federazione Ciclistica Italiana, che pubblica i tesserati per categoria "
        "nel documento «I numeri della Federazione Ciclistica Italiana». La serie usata "
        "qui copre le stagioni %s-%s; il valore 2020 proviene da una fonte secondaria "
        "che riporta il confronto 2020-2022 e i cui valori 2021 e 2022 coincidono con "
        "quelli ufficiali.\n\n"
        "Quattro avvertenze, tutte importanti. Il tesseramento e' **per categoria, non "
        "per specialita'**: un Esordiente tesserato puo' correre solo fuoristrada e non "
        "comparire mai in una classifica su strada, e il regolamento della classifica "
        "esclude esplicitamente anche le gare su pista — quindi la copertura calcolata "
        "qui e' un **limite inferiore**. Il numeratore inoltre non comprende chi e' "
        "tesserato per una societa' affiliata all'estero, che il regolamento tiene "
        "fuori dalla classifica anche quando corre in Italia. Le categorie coprono un "
        "numero diverso di anni di eta' — due per Esordienti, Allievi e Juniores, "
        "quattro per l'Under 23 — e i conteggi vanno divisi per l'ampiezza prima di "
        "confrontarli. Le stagioni anomale sono escluse: il tesseramento si paga a "
        "inizio anno, le gare no.\n\n"
        "I dati sono in `riferimenti/tesserati_fci.csv`, con la provenienza di ogni "
        "riga."
        % (a0, a1),
        [("Federazione Ciclistica Italiana", "https://www.federciclismo.it/")]))

    p.append(md.tabella(cop["colonne"], cop["righe"], nota=cop["nota"],
                        colonne_conteggio=(1, 2), decimali=1))

    lo, hi, media = (v.get("copertura_min"), v.get("copertura_max"),
                     v.get("copertura_media"))
    if media:
        p.append(md.paragrafo(
            "",
            md.afferma(
                hi < 25,
                "meno di un tesserato su quattro compare nella classifica nazionale in "
                "una stagione",
                "**In classifica compare circa un tesserato su sette.** La quota sta fra "
                "il %s%% e il %s%%, con una media del %s%%, ed e' notevolmente stabile: "
                "quattro categorie, cinque stagioni, sempre lo stesso ordine di "
                "grandezza. Non e' un effetto di una categoria o di un anno particolare, "
                "e' come funziona il sistema."
                % (md.num(lo, 1), md.num(hi, 1), md.num(media, 1))),
            "",
            "Gli altri sei su sette **corrono senza mai entrare a punti**, oppure "
            "corrono in una specialita' diversa dalla strada. La classifica non e' un "
            "censimento del ciclismo giovanile: e' la punta che emerge, e questo studio "
            "parla di quella punta."))

    f = lt.figura("copertura", "copertura")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.paragrafo(
        "",
        "> **Conseguenza sulla lettura di tutto il documento.** Quando si legge che il "
        "%s per mille dei classificati in Esordienti diventa professionista, il "
        "denominatore e' "
        "quel settimo. Rapportata a tutti i tesserati la quota sarebbe circa sette volte "
        "piu' bassa. Non si e' fatta la moltiplicazione nel testo, per una ragione "
        "precisa: la copertura si misura su stagioni recenti, mentre le coorti studiate "
        "hanno corso prima, e trasferire il rapporto da un periodo all'altro sarebbe una "
        "stima travestita da misura."
        % md.num(lt.valore("attrito", "pro_su_mille_u15"), 1)))

    # --- i due imbuti ------------------------------------------------------
    if imb:
        p.append(md.sezione("L'attrito della classifica e quello vero", 3))
        p.append(md.paragrafo(
            "La sezione sull'attrito diceva che uscire dalla classifica non significa "
            "smettere, e che la differenza non era quantificabile perche' mancava "
            "l'elenco dei tesserati. Ora una parte di quella differenza si vede: i "
            "tesserati calano di categoria in categoria, e si puo' confrontare il loro "
            "calo con quello dei classificati."))
        p.append(md.tabella(imb["colonne"], imb["righe"], nota=imb["nota"],
                            colonne_conteggio=(1, 3)))

        rt, rn = v.get("residuo_tesserati"), v.get("residuo_classifica")
        individuale = None
        curva = lt.valore("attrito", "curva")
        if curva and len(curva) >= 2:
            individuale = curva[1][2]        # % di chi era in U15 e si ritrova in U17
        if rt and rn:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    abs(rt - rn) < 5,
                    "dall'ingresso all'ultima categoria giovanile la classifica si "
                    "restringe quanto la popolazione dei tesserati, non di piu'",
                    "**I due imbuti arrivano quasi allo stesso punto**: dall'ingresso "
                    "in Esordienti all'Under 23 resta il %s%% dei tesserati per anno di "
                    "eta' e il %s%% dei classificati. La classifica non si restringe "
                    "piu' in fretta della popolazione che la genera."
                    % (md.num(rt, 1), md.num(rn, 1))),
                "",
                "I singoli passi differiscono — fra Esordienti e Allievi calano piu' i "
                "classificati, fra Allievi e Juniores calano piu' i tesserati — ma il "
                "risultato complessivo e' lo stesso, e sono differenze su medie di "
                "cinque stagioni che non vale la pena interpretare una per una.",
                "",
                "Il confronto interessante e' con il **terzo** numero, quello delle "
                "persone. Questi due imbuti contano teste per stagione; seguendo invece "
                "i singoli atleti, solo il %s%% di chi era in Esordienti si ritrova in "
                "Allievi. La distanza fra i conteggi aggregati e quella percentuale "
                "**e' il ricambio**: la classifica mantiene la propria dimensione "
                "sostituendo le persone, non trattenendole."
                % md.num(individuale, 1) if individuale else "",
                "",
                "E' la conferma esterna di cio' che la sezione sull'attrito aveva gia' "
                "misurato dall'interno con i rientri e il rinnovo delle liste. Due fonti "
                "indipendenti, la stessa conclusione: **l'imbuto individuale che si "
                "osserva nella classifica e' molto piu' ripido dell'abbandono reale "
                "dello sport.**"))

    # --- si possono stimare gli anni mancanti? -------------------------------
    bt = lt.tabella("copertura", "backtest")
    # Il contro-argomento poggia su un numero calcolato altrove: quanto l'aggiustamento
    # per coorte sposta gli odds ratio. Si legge dall'archivio invece di riscriverlo.
    sposta = lt.valore("univariati", "spostamento_coorte")
    if bt:
        p.append(md.sezione("Si possono stimare gli anni che mancano?", 3))
        p.append(md.paragrafo(
            "La tentazione e' evidente: la serie dei tesserati parte dal %s, le coorti "
            "studiate hanno corso prima, e una tendenza si estrapola in due righe. La "
            "domanda giusta non e' se si possa fare, ma **se il risultato valga "
            "qualcosa** — e si puo' rispondere con una prova invece che con un'opinione: "
            "si stima la tendenza sulle stagioni recenti e si prova a prevedere quelle "
            "vecchie, di cui la risposta si conosce gia'."
            % v.get("anni", [0])[0]))
        p.append(md.tabella(bt["colonne"], bt["righe"], nota=bt["nota"],
                            colonne_conteggio=(1, 2)))

        err = v.get("backtest_errore")
        div = v.get("stime_divergenti")
        if err:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    err > 10,
                    "estrapolare la tendenza del tesseramento all'indietro sbaglia in "
                    "modo rilevante gia' su due o tre anni",
                    "**Sbaglia fino al %s%%, e a soli due o tre anni di distanza.** "
                    "L'estrapolazione all'indietro fino agli anni delle coorti studiate "
                    "sarebbe quattro o cinque volte piu' lunga: l'errore non puo' che "
                    "essere maggiore." % md.num(err, 0))))
        if div:
            anno, a, b = div
            p.append(md.paragrafo(
                "",
                "E c'e' di peggio della semplice imprecisione. Stimando la stessa "
                "tendenza in due modi entrambi difendibili — includendo o escludendo le "
                "stagioni della pandemia — i tesserati Esordienti del %s risultano %s "
                "oppure %s. Le due stime differiscono di **%s volte**, e la differenza "
                "non viene dai dati: viene da una decisione di chi fa il calcolo. Un "
                "numero che dipende cosi' tanto da una scelta arbitraria non e' una "
                "misura."
                % (anno, md.conta(max(a, b)), md.conta(min(a, b)),
                   md.num(max(a, b) / min(a, b), 1))))

        p.append(md.paragrafo(
            "",
            "C'e' anche una ragione sostanziale, oltre a quella statistica. Il "
            "tesseramento di una federazione non segue un andamento inerziale: risponde "
            "a politiche, a risultati sportivi, a mode. Nello stesso periodo la Gran "
            "Bretagna e' passata da quindicimila a centosessantacinquemila tesserati. "
            "Una serie di otto anni non contiene l'informazione per sapere cosa "
            "succedeva quindici anni prima.",
            "",
            "**Quindi no: gli anni mancanti non si stimano.** Quello che si puo' fare, e "
            "che questo documento fa, e' dichiarare la copertura misurata dove esiste e "
            "trattare il periodo studiato come non misurato. La differenza fra le due "
            "cose e' esattamente la differenza fra un dato e una supposizione."))

        p.append(md.paragrafo(
            "",
            "> **Perche' questo non intacca le conclusioni.** La copertura serve a dare "
            "scala alle percentuali assolute, non entra in nessun modello. I confronti "
            "fra categorie, i coefficienti, le AUC e i test sono tutti calcolati "
            "*dentro* la popolazione dei classificati, e non cambiano se il denominatore "
            "esterno e' un settimo o un quinto. L'unico rischio sarebbe che la "
            "selettivita' fosse cambiata **fra una coorte e l'altra** dello studio: ma "
            "questo si controlla, e i modelli aggiustati per anno di nascita danno "
            "coefficienti che differiscono da quelli grezzi %s."
            % ("di meno di 0,01" if (sposta or 1) < 0.01
               else "di al massimo " + md.num(sposta, 2))))

    prof = v.get("prof_licenze")
    if prof:
        p.append(md.paragrafo(
            "",
            "Un'ultima cifra, per dare la misura del bersaglio: le licenze da "
            "professionista rilasciate dalla federazione sono state fra **%s e %s** "
            "nelle stagioni osservate. Non e' il numero di posti che si liberano ogni "
            "anno — e' l'intera popolazione professionistica italiana, di ogni eta', in "
            "un dato momento."
            % (md.conta(min(prof)), md.conta(max(prof)))))

    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
