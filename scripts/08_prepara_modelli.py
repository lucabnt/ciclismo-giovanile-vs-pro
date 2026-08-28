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
TESTUALI = {"regione", "region_first", "team_first", "prima_cella", "birth_year_conf",
            "tier"}


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


def eta_tipica(cella):
    """U15y1 -> 14, U23y1 -> 20.

    Non e' un dettaglio decorativo: i modelli di sopravvivenza a tempo discreto hanno
    bisogno di un asse temporale, e l'eta' della cella e' quell'asse.
    """
    categoria, anno = cella.split("y")
    return ETA_BASE[categoria] + int(anno)


def selezione(db, coorti, celle):
    """Le righe di tab_b che rientrano nello studio: sesso scelto, coorti richieste."""
    lo, hi = coorti
    colonne = list(ANAGRAFICHE + PERCORSO + ESITI)
    for c in celle:
        colonne += ["pct_" + c, "pctpt_" + c, "present_" + c]
    sql = ("SELECT %s FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ? "
           "ORDER BY athlete_id" % ", ".join(colonne))
    return colonne, db.execute(sql, (cfg("studio", "sesso"), lo, hi)).fetchall()


def scrivi(out, nome, colonne, righe):
    tipi = ["%s %s" % (c, "TEXT" if c in TESTUALI else "REAL") for c in colonne]
    out.execute("DROP TABLE IF EXISTS %s" % nome)
    out.execute("CREATE TABLE %s (%s)" % (nome, ", ".join(tipi)))
    out.executemany("INSERT INTO %s VALUES (%s)" % (nome, ", ".join("?" * len(colonne))),
                    righe)


def panello(out, colonne, righe, celle):
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
            dati.append((r[idx["athlete_id"]], c, ordine, eta_tipica(c),
                         r[idx["present_" + c]], r[idx["pct_" + c]],
                         r[idx["pctpt_" + c]], r[idx["PRO"]]))
    out.executemany("INSERT INTO panello VALUES (?,?,?,?,?,?,?,?)", dati)
    return len(dati)


def scrivi_celle(out, celle):
    out.execute("DROP TABLE IF EXISTS celle")
    out.execute("""CREATE TABLE celle (
        cella TEXT PRIMARY KEY, ordine INTEGER, categoria TEXT,
        anno_categoria INTEGER, eta INTEGER
    )""")
    out.executemany("INSERT INTO celle VALUES (?,?,?,?,?)",
                    [(c, i, c.split("y")[0], int(c.split("y")[1]), eta_tipica(c))
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
        for t in ("campione", "campione_b", "panello", "celle"):
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
        n_pan = panello(out, colonne, righe, celle)

        colonne_b, righe_b = selezione(src, cfg("coorti", "domanda_b"), celle)
        scrivi(out, "campione_b", colonne_b, righe_b)

        scrivi_celle(out, celle)
        scrivi_config(out, celle)

    a_lo, a_hi = cfg("coorti", "domanda_a_c")
    b_lo, b_hi = cfg("coorti", "domanda_b")
    print("Scritto %s" % USCITA)
    print("  campione   %5d atleti (coorti %d-%d)" % (len(righe), a_lo, a_hi))
    print("  campione_b %5d atleti (coorti %d-%d)" % (len(righe_b), b_lo, b_hi))
    print("  panello    %5d righe su %d celle" % (n_pan, len(celle)))


if __name__ == "__main__":
    main()
