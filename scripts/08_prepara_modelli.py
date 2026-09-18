"""
Prepara il rettangolo di dati che i modelli in R leggeranno.

PERCHE' UNO STRATO IN MEZZO
    I modelli stanno in R, la preparazione in Python. Se R leggesse `analisi.db` gli
    toccherebbe conoscere le regole dello studio — quali coorti, quale sesso, quali
    celle, quali classi contano come professionismo — e quelle regole stanno in
    config.toml, che R non legge senza dipendenze aggiuntive.

    Qui le regole si applicano una volta sola, in Python, e il risultato e' un database
    che contiene gia' solo cio' che serve. R apre `modelli.db` e trova un rettangolo
    pronto: nessuna decisione di studio da riprendere, nessun filtro da ricordare. Se un
    giorno le coorti cambiano, si modifica config.toml e si rilancia questo script: i
    file R restano identici.

COSA CONTIENE modelli.db
    campione     un atleta per riga, coorti della Domanda A e C (accesso al pro)
    campione_b   un atleta per riga, coorti della Domanda B (qualita' della carriera)
    panello      forma lunga, una riga per atleta x cella, per i modelli longitudinali
    celle        l'elenco ordinato delle celle, con categoria ed eta' tipica
    config       le scelte dello studio, in JSON, cosi' R le puo' citare nei risultati

ORDINE
    Va lanciato dopo 06_esiti.py: legge tab_b, che 06 completa con gli esiti PCS.

USO
    python scripts/08_prepara_modelli.py
    python scripts/08_prepara_modelli.py --stato
"""
import argparse
import json
import os
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from lib_giovanile import DB_ANALISI, CATEGORIE, cfg   # noqa: E402

USCITA = os.path.join("data", "analisi", "modelli.db")

# Eta' compiuta al primo anno di ciascuna categoria, ricavata dalla tabella condivisa
# invece che riscritta qui: U15y1 -> 14, U23y1 -> 20.
ETA_BASE = {sigla: base for sigla, _sesso, base in CATEGORIE.values()}

# Colonne di tab_b che passano ai modelli cosi' come sono. Non servono tutte a tutti i
# modelli: si portano avanti perche' il costo e' nullo e perche' un modello nuovo non
# debba far ritoccare questo script.
ANAGRAFICHE = [
    "athlete_id", "birth_year", "birth_quarter", "rel_age", "birth_year_conf", "regione",
]
PERCORSO = [
    "best_pct_youth", "best_pct_cat", "n_seasons_youth", "n_wins_youth", "slope_pct",
    "prima_cella", "region_first", "team_first", "n_team_changes", "n_regions",
    "changed_region", "team_quality_first", "team_quality_n",
]
ESITI = [
    "PRO", "tier", "year_turned_pro", "age_turned_pro", "pro_seasons", "best_pcs_rank",
    "censored", "pcs_matched", "elite_seasons_a_punti", "last_racing_age",
    "punti_dopo_u23",
]
# `athlete_id` e' un identificativo anonimizzato, quindi testo: dichiararlo evita che
# chi legge il database lo scambi per un numero e provi a convertirlo.
TESTUALI = {"athlete_id", "regione", "region_first", "team_first", "prima_cella",
            "birth_year_conf", "tier"}


def leggi_celle():
    """Ricava l'elenco delle celle dalle colonne di tab_b, non da una lista scritta qui.

    Se un giorno le categorie cambiano a monte, l'elenco segue senza modifiche. Si
    tengono solo le celle che hanno sia il percentile sia il flag di presenza: le
    varianti sperimentali (per esempio `pct_U19_arm`) non entrano nel campione base.
    """
    with sqlite3.connect(DB_ANALISI) as db:
        colonne = [r[1] for r in db.execute("PRAGMA table_info(tab_b)")]
    celle = []
    for c in colonne:
        if not c.startswith("pct_"):
            continue
        nome = c[len("pct_"):]
        if "present_" + nome in colonne and "y" in nome:
            celle.append(nome)
    return celle


def eta_osservate(db):
    """L'eta' di ciascuna cella, letta dai dati invece che calcolata.

    Non e' un dettaglio decorativo: i modelli di sopravvivenza a tempo discreto hanno
    bisogno di un asse temporale, e l'eta' della cella e' quell'asse. Ricavarla da una
    formula sulle sigle e' facile da sbagliare di un anno — e' successo — mentre la
    tabella A contiene l'eta' effettiva di ogni riga, quindi la si chiede a lei.
    """
    out = {}
    for cat, anno, eta in db.execute(
            """SELECT category, cat_year, CAST(AVG(age) AS INTEGER) FROM tab_a
               WHERE sesso = ? AND age IS NOT NULL AND cat_year IS NOT NULL
               GROUP BY 1, 2""", (cfg("studio", "sesso"),)):
        out["%sy%d" % (cat, anno)] = eta
    return out


def eta_tipica(cella, osservate=None):
    """U15y1 -> 13, U23y1 -> 19. Dai dati se ci sono, altrimenti dalla convenzione."""
    if osservate and cella in osservate:
        return osservate[cella]
    categoria, anno = cella.split("y")
    return ETA_BASE[categoria] + int(anno) - 1


def selezione(db, coorti, celle):
    """Le righe di tab_b che rientrano nello studio: sesso scelto, coorti richieste."""
    lo, hi = coorti
    colonne = list(ANAGRAFICHE + PERCORSO + ESITI)
    for c in celle:
        colonne += ["pct_" + c, "pctpt_" + c, "present_" + c]
    # La variante armonizzata dell'U19 non esiste ancora a monte: si porta avanti solo
    # se c'e', cosi' lo STEP 18 potra' girare in entrambe le versioni senza che questo
    # script debba essere ritoccato il giorno in cui la colonna comparira'.
    disponibili = {r[1] for r in db.execute("PRAGMA table_info(tab_b)")}
    arm = "pct_" + cfg("modelli", "cella_u19_armonizzata")
    if arm in disponibili:
        colonne.append(arm)

    sql = ("SELECT %s FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ? "
           "ORDER BY athlete_id" % ", ".join(colonne))
    return colonne, db.execute(sql, (cfg("studio", "sesso"), lo, hi)).fetchall()


def scrivi(out, nome, colonne, righe):
    tipi = ["%s %s" % (c, "TEXT" if c in TESTUALI else "REAL") for c in colonne]
    out.execute("DROP TABLE IF EXISTS %s" % nome)
    out.execute("CREATE TABLE %s (%s)" % (nome, ", ".join(tipi)))
    out.executemany("INSERT INTO %s VALUES (%s)" % (nome, ", ".join("?" * len(colonne))),
                    righe)


def panello(out, colonne, righe, celle, eta):
    """Forma lunga: una riga per atleta x cella.

    Serve ai modelli longitudinali — sopravvivenza a tempo discreto e traiettorie — che
    in forma larga dovrebbero ricostruirsela ogni volta. Costruirla qui significa che
    tutti partono dalla stessa forma lunga, invece che da tante ricostruzioni diverse.
    """
    idx = {c: i for i, c in enumerate(colonne)}
    out.execute("DROP TABLE IF EXISTS panello")
    out.execute("""CREATE TABLE panello (
        athlete_id INTEGER, cella TEXT, ordine INTEGER, eta INTEGER,
        presente INTEGER, pct REAL, punti REAL, PRO INTEGER
    )""")
    dati = []
    for r in righe:
        for ordine, c in enumerate(celle):
            dati.append((r[idx["athlete_id"]], c, ordine, eta.get(c),
                         r[idx["present_" + c]], r[idx["pct_" + c]],
                         r[idx["pctpt_" + c]], r[idx["PRO"]]))
    out.executemany("INSERT INTO panello VALUES (?,?,?,?,?,?,?,?)", dati)
    return len(dati)


def persona_anno(src, out, celle, eta):
    """Una riga per atleta e per stagione a rischio: la forma che i modelli di
    sopravvivenza a tempo discreto richiedono.

    LE TRE REGOLE CHE RENDONO VALIDA LA TABELLA
        Nessuna riga dopo l'evento. Chi diventa professionista a ventidue anni contribuisce
        le stagioni da tredici a ventidue e poi esce dal rischio: tenerlo dentro
        significherebbe chiedergli di diventare professionista una seconda volta.

        Nessuna riga oltre l'osservazione. Un atleta nato nel 2005 nel 2025 ha ventun
        anni: le stagioni successive non sono «senza evento», sono non osservate. E' la
        censura, ed e' proprio cio' che permette di usare anche le coorti recenti.

        Il predittore e' ritardato. La probabilita' di passare professionista in una
        stagione si spiega con il rendimento della stagione **precedente**, non di quella
        in corso: usare la stessa stagione significherebbe spiegare un esito con
        informazione che al momento della decisione non era ancora disponibile.

    L'ASSENZA DALLA CLASSIFICA E' UN'INFORMAZIONE, NON UN BUCO
        Chi non era in classifica l'anno prima non ha un percentile. La colonna
        `presente_prec` distingue questo caso dagli altri, cosi' il modello puo' stimare
        separatamente l'effetto del rendimento e quello dell'esserci.
    """
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_sopravvivenza")
    eta_max = cfg("esiti", "eta_massima_pro")
    ultima = cfg("stagioni", "massima")
    per_eta = {e: c for c, e in eta.items()}
    eta_min = min(eta.values())

    colonne = ["athlete_id", "birth_year", "PRO", "age_turned_pro"]
    for c in celle:
        colonne += ["pct_" + c, "present_" + c]
    righe = src.execute(
        "SELECT %s FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ? "
        "ORDER BY athlete_id" % ", ".join(colonne), (sesso, lo, hi)).fetchall()
    idx = {c: i for i, c in enumerate(colonne)}

    out.execute("DROP TABLE IF EXISTS persona_anno")
    out.execute("""CREATE TABLE persona_anno (
        athlete_id INTEGER, birth_year INTEGER, stagione INTEGER, eta INTEGER,
        evento INTEGER, pct_prec REAL, presente_prec INTEGER, cella_prec TEXT
    )""")

    dati, eventi, censurati = [], 0, 0
    for r in righe:
        nascita = r[idx["birth_year"]]
        if nascita is None:
            continue
        eta_pro = r[idx["age_turned_pro"]]
        eta_pro = int(eta_pro) if r[idx["PRO"]] == 1 and eta_pro else None
        # Fino a quando l'atleta e' osservabile: la finestra dello studio, oppure
        # l'ultima stagione disponibile se la finestra non e' ancora finita.
        limite = min(eta_max, ultima - nascita)
        if eta_pro is not None:
            limite = min(limite, eta_pro)
        if limite < eta_min:
            continue
        for e in range(eta_min, limite + 1):
            cella = per_eta.get(e - 1)
            pct = r[idx["pct_" + cella]] if cella else None
            pres = r[idx["present_" + cella]] if cella else None
            dati.append((r[idx["athlete_id"]], nascita, nascita + e, e,
                         1 if eta_pro == e else 0,
                         pct if pres == 1 else None,
                         int(pres) if pres is not None else None, cella))
        if eta_pro is not None and eta_pro <= limite:
            eventi += 1
        else:
            censurati += 1

    out.executemany("INSERT INTO persona_anno VALUES (?,?,?,?,?,?,?,?)", dati)
    return len(dati), eventi, censurati


def misure(src, out, celle, eta):
    """Le due misure alternative dello stesso risultato, per ogni atleta e cella.

    PERCHE' SERVE UNA TABELLA A PARTE
        Il resto del progetto usa un solo predittore, il percentile con ordinamento
        esteso. Per chiedersi se quella scelta fosse giusta serve anche l'altra: il
        percentile sui soli punti. Le due stanno una accanto all'altra solo qui, perche'
        altrove si userebbe per sbaglio quella sbagliata.

    COSA C'E' DENTRO
        Oltre alle due misure, i punti grezzi e il numero di piazzamenti nei primi
        cinque. Il loro rapporto dice quanto vale in media un piazzamento, ed e' l'unico
        modo che questi dati offrono per accorgersi che le categorie internazionali
        pesano le gare per livello mentre le altre no.
    """
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    out.execute("DROP TABLE IF EXISTS misure")
    out.execute("""CREATE TABLE misure (
        athlete_id TEXT, cella TEXT, eta INTEGER, categoria TEXT,
        pct_punti REAL, pct_esteso REAL, punti REAL, top5 REAL, PRO INTEGER,
        stagione INTEGER, pari INTEGER
    )""")
    # Un pari merito esiste solo dentro la stessa classifica: si conta sul campo completo
    # della stagione e della cella, tutte le coorti comprese, e non fra i soli atleti in
    # studio ne' sommando stagioni diverse. R legge il flag e ne fa soltanto la media.
    from collections import Counter
    campo = Counter(tuple(r) for r in src.execute(
        """SELECT season, category, cat_year, points_raw FROM tab_a
           WHERE sesso = ? AND cat_year IS NOT NULL""", (sesso,)))
    righe = []
    for c in celle:
        cat, anno = c.split("y")
        for r in src.execute(
                """SELECT a.athlete_id, a.pct_rank, a.pct_rank_ext, a.points_raw,
                          a.top5, b.PRO, a.season
                   FROM tab_a a JOIN tab_b b ON b.athlete_id = a.athlete_id
                   WHERE a.sesso = ? AND a.category = ? AND a.cat_year = ?
                     AND b.birth_year BETWEEN ? AND ?
                     AND a.pct_rank IS NOT NULL AND a.pct_rank_ext IS NOT NULL
                     AND b.PRO IS NOT NULL""",
                (sesso, cat, int(anno), lo, hi)):
            pari = int(campo[(r[6], cat, int(anno), r[3])] > 1)
            righe.append((r[0], c, eta.get(c), cat) + tuple(r[1:]) + (pari,))
    out.executemany("INSERT INTO misure VALUES (?,?,?,?,?,?,?,?,?,?,?)", righe)
    return len(righe)


def scrivi_celle(src, out, celle, eta=None):
    """L'elenco delle celle, con quanto e' larga la classifica di ciascuna.

    L'ampiezza media della lista non e' un dettaglio: le classifiche del primo anno di
    categoria sono molto piu' corte di quelle del secondo, quindi esservi dentro e' piu'
    selettivo. Senza questo numero, il tasso di professionismo piu' alto nelle celle
    del primo anno sembra un segnale mentre e' un effetto del denominatore.
    """
    ampiezza = {}
    for cat, anno, media in src.execute(
            """SELECT category, cat_year, AVG(n_ranked) FROM tab_a
               WHERE sesso = ? AND cat_year IS NOT NULL GROUP BY 1, 2""",
            (cfg("studio", "sesso"),)):
        ampiezza["%sy%d" % (cat, anno)] = round(media) if media else None

    out.execute("DROP TABLE IF EXISTS celle")
    out.execute("""CREATE TABLE celle (
        cella TEXT PRIMARY KEY, ordine INTEGER, categoria TEXT,
        anno_categoria INTEGER, eta INTEGER, ampiezza_lista INTEGER
    )""")
    out.executemany("INSERT INTO celle VALUES (?,?,?,?,?,?)",
                    [(c, i, c.split("y")[0], int(c.split("y")[1]),
                      eta_tipica(c, eta), ampiezza.get(c))
                     for i, c in enumerate(celle)])


def scrivi_config(out, celle):
    """Le scelte dello studio viaggiano insieme ai dati.

    Un risultato prodotto in R deve poter dichiarare su quali coorti e' stato calcolato
    senza che nessuno lo riscriva a mano nel testo.
    """
    voci = {
        "sesso": cfg("studio", "sesso"),
        "coorti_a_c": cfg("coorti", "domanda_a_c"),
        "coorti_b": cfg("coorti", "domanda_b"),
        "stagione_massima": cfg("stagioni", "massima"),
        "classi_pro": cfg("esiti", "classi_pro"),
        "celle": celle,
        "celle_modello": cfg("modelli", "celle_correlazione"),
        "celle_annidate": cfg("modelli", "celle_annidate"),
        "coorti_sopravvivenza": cfg("coorti", "domanda_sopravvivenza"),
        "eta_massima_pro": cfg("esiti", "eta_massima_pro"),
        "eta_minima_pro": cfg("esiti", "eta_minima_pro"),
        "cella_u19_armonizzata": cfg("modelli", "cella_u19_armonizzata"),
        "min_cella_pubblicabile": cfg("etica", "min_cella_pubblicabile"),
        "predittore": cfg("predittore", "principale"),
    }
    out.execute("DROP TABLE IF EXISTS config")
    out.execute("CREATE TABLE config (chiave TEXT PRIMARY KEY, valore TEXT)")
    out.executemany("INSERT INTO config VALUES (?,?)",
                    [(k, json.dumps(v)) for k, v in voci.items()])


def stato():
    if not os.path.exists(USCITA):
        print("modelli.db non esiste: lanciare lo script senza --stato per costruirlo.")
        return
    with sqlite3.connect(USCITA) as db:
        for t in ("campione", "campione_b", "panello", "persona_anno", "misure",
                  "celle"):
            n = db.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
            print("%-12s %7d righe" % (t, n))
        tot, pro = db.execute(
            "SELECT COUNT(*), SUM(PRO) FROM campione").fetchone()
        print("\nprofessionisti nel campione: %d su %d (%.1f%%)"
              % (pro or 0, tot, 100.0 * (pro or 0) / tot if tot else 0))
        print("celle:", ", ".join(r[0] for r in db.execute(
            "SELECT cella FROM celle ORDER BY ordine")))


def main():
    ap = argparse.ArgumentParser(description="Prepara i dati per i modelli in R.")
    ap.add_argument("--stato", action="store_true",
                    help="riepiloga cosa contiene modelli.db")
    args = ap.parse_args()
    if args.stato:
        return stato()

    celle = leggi_celle()
    with sqlite3.connect(DB_ANALISI) as src, sqlite3.connect(USCITA) as out:
        colonne, righe = selezione(src, cfg("coorti", "domanda_a_c"), celle)
        scrivi(out, "campione", colonne, righe)
        eta = eta_osservate(src)
        n_pan = panello(out, colonne, righe, celle, eta)

        colonne_b, righe_b = selezione(src, cfg("coorti", "domanda_b"), celle)
        scrivi(out, "campione_b", colonne_b, righe_b)

        n_pa, eventi, censurati = persona_anno(src, out, celle, eta)
        n_mis = misure(src, out, celle, eta)
        scrivi_celle(src, out, celle, eta)
        scrivi_config(out, celle)

    a_lo, a_hi = cfg("coorti", "domanda_a_c")
    b_lo, b_hi = cfg("coorti", "domanda_b")
    print("Scritto %s" % USCITA)
    print("  campione   %5d atleti (coorti %d-%d)" % (len(righe), a_lo, a_hi))
    print("  campione_b %5d atleti (coorti %d-%d)" % (len(righe_b), b_lo, b_hi))
    print("  panello    %5d righe su %d celle" % (n_pan, len(celle)))
    s_lo, s_hi = cfg("coorti", "domanda_sopravvivenza")
    print("  persona_anno %5d righe (coorti %d-%d): %d eventi, %d censurati"
          % (n_pa, s_lo, s_hi, eventi, censurati))
    print("  misure     %5d righe (le due versioni dello stesso piazzamento)" % n_mis)


if __name__ == "__main__":
    main()
