"""
Scarica i riferimenti esterni che servono all'analisi, e li mette in cache.

OGGI SERVE UNA COSA SOLA: la distribuzione attesa delle nascite per mese.

    Il test sull'effetto dell'eta' relativa confronta il trimestre di nascita dei
    classificati con quello della popolazione. L'atteso NON e' il 25% per trimestre:
    in Italia si nasce di piu' fra maggio e settembre, e il primo trimestre e' il piu'
    scarso. Usare l'uniforme sottostimerebbe l'effetto invece di sovrastimarlo.

PERCHE' EUROSTAT E NON ISTAT
    Le serie mensili delle nascite di ISTAT partono dal 2003, e le coorti in studio sono
    del 1992-2000. Eurostat `demo_fmonth` copre l'Italia dal 1960 al 2025 con tutti i
    dodici mesi. API aperta, senza chiave, formato JSON-stat.

    https://ec.europa.eu/eurostat/databrowser/view/demo_fmonth/default/table

USO
    python scripts/07_riferimenti.py
    python scripts/07_riferimenti.py --mostra     # legge la cache, senza rete
"""
import argparse
import json
import os
import sqlite3
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import cfg

DB_RIF = "data/riferimento/riferimenti.db"
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_fmonth"
       "?format=JSON&lang=en&geo=IT")

DDL = """
CREATE TABLE IF NOT EXISTS nascite_mese (
    anno  INTEGER NOT NULL,
    mese  INTEGER NOT NULL,
    nati  INTEGER NOT NULL,
    PRIMARY KEY (anno, mese)
);
CREATE TABLE IF NOT EXISTS riferimento_meta (chiave TEXT PRIMARY KEY, valore TEXT);
"""


def dice(*a):
    print(*a)
    sys.stdout.flush()


def contesto_ssl():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def scarica(db):
    dice("Scarico Eurostat demo_fmonth (nascite per mese, Italia)...")
    req = urllib.request.Request(URL, headers={"User-Agent": "ricerca statistica"})
    with urllib.request.urlopen(req, timeout=90, context=contesto_ssl()) as r:
        d = json.load(r)

    ids, size = d["id"], d["size"]
    inv = {k: {v: k2 for k2, v in d["dimension"][k]["category"]["index"].items()}
           for k in ids}
    righe = []
    for k, v in d["value"].items():
        rest, pos = int(k), {}
        for nome, s in zip(reversed(ids), reversed(size)):
            pos[nome] = rest % s
            rest //= s
        mese = inv["month"][pos["month"]]
        if not mese.startswith("M"):          # TOTAL, UNK
            continue
        righe.append((int(inv["time"][pos["time"]]), int(mese[1:]), int(v)))

    db.executemany("INSERT OR REPLACE INTO nascite_mese VALUES (?,?,?)", righe)
    db.execute("INSERT OR REPLACE INTO riferimento_meta VALUES ('fonte_nascite', ?)",
               ("Eurostat demo_fmonth, geo=IT",))
    db.execute("INSERT OR REPLACE INTO riferimento_meta VALUES ('scaricato_il', "
               "datetime('now'))")
    db.commit()
    anni = sorted({r[0] for r in righe})
    dice("   %d righe, anni %d-%d" % (len(righe), anni[0], anni[-1]))


def mostra(db):
    for chiave, valore in db.execute("SELECT chiave, valore FROM riferimento_meta"):
        dice("   %-16s %s" % (chiave, valore))
    for etichetta in ("domanda_a_c", "domanda_b"):
        lo, hi = cfg("coorti", etichetta)
        mesi = dict(db.execute("""SELECT mese, SUM(nati) FROM nascite_mese
                                  WHERE anno BETWEEN ? AND ? GROUP BY 1""", (lo, hi)))
        if len(mesi) != 12:
            dice("\n   %s: dati incompleti (%d mesi)" % (etichetta, len(mesi)))
            continue
        tot = sum(mesi.values())
        q = [sum(mesi[m] for m in range(1 + 3 * i, 4 + 3 * i)) for i in range(4)]
        dice("\n   coorti %d-%d (%s): %s nati vivi" % (lo, hi, etichetta,
                                                       f"{tot:,}".replace(",", ".")))
        dice("      atteso per trimestre: " + "  ".join(
            "Q%d %.2f%%" % (i + 1, 100 * x / tot) for i, x in enumerate(q)))
        dice("      vettore R: attesi <- c(%s)"
             % ", ".join("%.4f" % (x / tot) for x in q))


def main():
    ap = argparse.ArgumentParser(description="Scarica i riferimenti esterni.")
    ap.add_argument("--mostra", action="store_true", help="legge la cache, senza rete")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(DB_RIF), exist_ok=True)
    db = sqlite3.connect(DB_RIF)
    db.executescript(DDL)
    if not args.mostra:
        if db.execute("SELECT COUNT(*) FROM nascite_mese").fetchone()[0]:
            dice("Gia' in cache. Per riscaricare, cancella %s" % DB_RIF)
        else:
            scarica(db)
    mostra(db)


if __name__ == "__main__":
    main()
