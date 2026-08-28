"""
Scarica la scheda personale di ogni atleta da ciclismo.info.

PERCHE'
    Le classifiche non riportano l'eta'. La scheda personale si', con la data di
    nascita completa. Risolve alla radice tre limiti del dataset:
      - l'anno di nascita ricostruito per inferenza (~2.400 'presunto', 38 in conflitto);
      - i 586 atleti che compaiono solo da U23, per cui l'anno era ignoto e con esso
        l'anno di corso, che senza nascita non e' calcolabile;
      - l'impossibilita' di studiare il Relative Age Effect, che richiede il giorno.

COME SI USA

    python scripts/03_scarica_schede.py --stato          # dove siamo, senza scaricare
    python scripts/03_scarica_schede.py --solo-incerti   # i soli anni non certi (~3.000)
    python scripts/03_scarica_schede.py                  # tutti gli atleti (~13.000)
    python scripts/03_scarica_schede.py --limite 200     # un lotto di prova
    python scripts/03_scarica_schede.py --riparsa        # riestrae dall'HTML in cache

    Si puo' interrompere con Ctrl+C in qualunque momento: il lavoro fatto e' salvato e
    basta rilanciare lo stesso comando per riprendere da dove si era arrivati.

    A 1,2 s di pausa servono circa 60 minuti per --solo-incerti e 4 ore e mezza per
    tutti. La pausa e' regolabile con --pausa, ma non scendere sotto il secondo: e' un
    sito piccolo e non c'e' fretta.

COSA SI OTTIENE
    data/giovanile/schede.db, con l'anno di nascita (presente quasi sempre), la data
    completa (presente in circa quattro casi su cinque, meno per gli atleti piu'
    vecchi), la societa' e l'HTML originale compresso, cosi' cambiare il parsing non
    costa altre richieste. Poi:

    python scripts/01_build_tabelle.py

    che usa le nascite osservate al posto di quelle inferite, senza altre modifiche.

DETTAGLI DELLA FONTE (verificati, vedi docs/verifica_dati_giovanile.md §9)
    URL: http://<sottodominio>.ciclismo.info/scheda_corridore_risultati_gare_<id>_<x>_<y>_<anno>.htm
    Il segmento con il nome e' ignorato dal server: conta solo l'id, quindi non c'e'
    alcun problema di accenti, apostrofi o cognomi doppi. Sottodominio e anno invece
    devono corrispondere a una stagione in cui l'atleta compare davvero, altrimenti la
    risposta e' 200 ma senza dati anagrafici: si usa la sua stagione piu' recente.
    Il sito non espone un robots.txt.
"""
import argparse
import html
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import DB_GIOVANILE, cfg, connect

DB_SCHEDE = "data/giovanile/schede.db"
CROSSWALK = "data/private/crosswalk_atleti.csv"
PAUSA = cfg("scaricamento", "pausa_schede")
OGNI = 25          # righe fra un salvataggio e l'altro
UA = "Mozilla/5.0 (compatibile; ricerca statistica non commerciale su ciclismo giovanile)"

MESI = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
        "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11,
        "dicembre": 12}

CAMPI = ("birth_year", "birth_date", "nazionalita", "societa", "cat_pagina",
         "anno_pagina", "n_piazzamenti")

DDL = """
CREATE TABLE IF NOT EXISTS scheda_atleta (
    id_atleta     INTEGER PRIMARY KEY,
    url           TEXT,
    http_status   INTEGER,
    birth_year    INTEGER,   -- da "COGNOME NOME (AAAA)": presente quasi sempre
    birth_date    TEXT,      -- da "Nato il GG Mese AAAA", AAAA-MM-GG: non sempre presente
    nazionalita   TEXT,      -- codice a due lettere, campo raro della fonte
    societa       TEXT,
    cat_pagina    TEXT,
    anno_pagina   INTEGER,
    n_piazzamenti INTEGER,   -- righe di risultato elencate (piazzamenti, non partenze)
    html_gz       BLOB,      -- pagina originale compressa, per riparsare senza riscaricare
    scaricato_il  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_scheda_nascita ON scheda_atleta(birth_year);
"""


def dice(*a):
    """Stampa subito: senza flush l'avanzamento resta nel buffer e non si vede."""
    print(*a)
    sys.stdout.flush()


def durata(sec):
    if sec < 90:
        return "%d s" % sec
    if sec < 5400:
        return "%d min" % round(sec / 60)
    return "%.1f ore" % (sec / 3600)


def estrai(s):
    """Campi anagrafici dalla scheda. None dove il dato manca."""
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    out = dict.fromkeys(CAMPI)

    m = re.search(r"\(((?:19|20)\d\d)\)\s*Classifica", t)
    if m:
        out["birth_year"] = int(m.group(1))

    m = re.search(r"Nat[oa]\s+il\s+(\d{1,2})\s+([A-Za-z]+)\s+((?:19|20)\d\d)", t)
    if m and m.group(2).lower() in MESI:
        out["birth_date"] = "%s-%02d-%02d" % (m.group(3), MESI[m.group(2).lower()],
                                              int(m.group(1)))
        if out["birth_year"] is None:
            out["birth_year"] = int(m.group(3))

    m = re.search(r"\b([A-Z]{2})\s+Nat[oa]\s+il", t)
    if m:
        out["nazionalita"] = m.group(1)

    m = re.search(r"^\s*(.+?)\s+-\s+Categoria\s+([A-Z_\- ]+?)\s+-\s+Stagione\s+(\d{4})", t)
    if m:
        pezzi = m.group(1).split(" - ", 1)
        out["societa"] = pezzi[1].strip() if len(pezzi) > 1 else None
        out["cat_pagina"] = m.group(2).strip()
        out["anno_pagina"] = int(m.group(3))

    out["n_piazzamenti"] = len(re.findall(r"\b20\d\d-\d\d-\d\d\b", t))
    return out


def bersagli(src, solo_incerti):
    """id_atleta -> (sottodominio, anno) della stagione piu' recente in cui compare."""
    loc = {}
    for r in src.execute("""
            SELECT cp.id_atleta AS id, cat.subdomain AS sub, MAX(cp.anno) AS anno
            FROM   classifiche_punti cp
            JOIN   categorie cat ON cat.id_categoria = cp.id_categoria
            WHERE  cp.mese IS NULL AND cp.tipo_soggetto = 'individuale'
            GROUP  BY cp.id_atleta, cat.subdomain"""):
        prec = loc.get(r["id"])
        if prec is None or r["anno"] > prec[1]:
            loc[r["id"]] = (r["sub"], r["anno"])

    if solo_incerti:
        import csv
        if not os.path.exists(CROSSWALK):
            sys.exit("Serve %s: esegui prima 01_build_tabelle.py" % CROSSWALK)
        with open(CROSSWALK, encoding="utf-8") as f:
            incerti = {int(r["id_atleta_src"]) for r in csv.DictReader(f)
                       if r["birth_year_conf"] not in ("certo", "sorgente", "scheda")}
        loc = {k: v for k, v in loc.items() if k in incerti}
    return loc


def scarica(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return None, ""


# --------------------------------------------------------------------------
def stato(db, src):
    """Dove siamo, e i due numeri che decidono cosa e' analizzabile."""
    import csv
    tutti = bersagli(src, False)
    fatte = {r[0] for r in db.execute("SELECT id_atleta FROM scheda_atleta WHERE http_status=200")}
    n_anno, n_data = db.execute("""SELECT SUM(birth_year IS NOT NULL), SUM(birth_date IS NOT NULL)
                                   FROM scheda_atleta WHERE http_status=200""").fetchone()
    dice("SCHEDE SCARICATE")
    dice("  atleti totali            %6d" % len(tutti))
    dice("  schede valide            %6d  (%.1f%%)" % (len(fatte), 100 * len(fatte) / len(tutti)))
    if fatte:
        dice("  con anno di nascita      %6d  (%.1f%%)" % (n_anno, 100 * n_anno / len(fatte)))
        dice("  con data completa        %6d  (%.1f%%)" % (n_data, 100 * n_data / len(fatte)))
    manca = len(set(tutti) - fatte)
    if manca:
        dice("  ancora da scaricare      %6d  (circa %s a %.1f s di pausa)"
             % (manca, durata(manca * PAUSA), PAUSA))

    righe = db.execute("""SELECT birth_year, COUNT(*), SUM(birth_date IS NOT NULL)
                          FROM scheda_atleta WHERE http_status=200 AND birth_year IS NOT NULL
                          GROUP BY 1 HAVING COUNT(*) >= 20 ORDER BY 1""").fetchall()
    if righe:
        dice("\nCOPERTURA DELLA DATA COMPLETA PER COORTE")
        dice("  e' il numero che decide se il Relative Age Effect e' analizzabile,")
        dice("  perche' il RAE ha bisogno del giorno e non del solo anno")
        for y, n, c in righe:
            barra = "#" * round(20 * c / n)
            dice("   %d  %4d schede  %3.0f%%  %s" % (y, n, 100 * c / n, barra))

    if os.path.exists(CROSSWALK):
        with open(CROSSWALK, encoding="utf-8") as f:
            cw = {int(r["id_atleta_src"]): r for r in csv.DictReader(f)}
        conta = {}
        for i, by in db.execute("""SELECT id_atleta, birth_year FROM scheda_atleta
                                   WHERE http_status=200 AND birth_year IS NOT NULL"""):
            r = cw.get(i)
            if not r:
                continue
            conf = r["birth_year_conf"]
            if conf in ("scheda", "sorgente"):
                continue                      # gia' preso dalla scheda: nulla da confrontare
            if not r["birth_year"]:
                esito = "risolve un ignoto"
            elif int(r["birth_year"]) == by:
                esito = "concorda"
            else:
                esito = "smentisce (%+d)" % (by - int(r["birth_year"]))
            conta.setdefault(conf, {}).setdefault(esito, 0)
            conta[conf][esito] += 1
        if conta:
            dice("\nCONFRONTO CON L'ANNO INFERITO")
            for conf in sorted(conta):
                voci = ", ".join("%s %d" % (k, v) for k, v in sorted(conta[conf].items()))
                dice("   %-20s %s" % (conf, voci))


def main():
    ap = argparse.ArgumentParser(
        description="Scarica le schede personali di ciclismo.info per la data di nascita.")
    ap.add_argument("--stato", action="store_true", help="mostra l'avanzamento e esce")
    ap.add_argument("--solo-incerti", action="store_true",
                    help="solo gli atleti il cui anno di nascita non e' certo")
    ap.add_argument("--limite", type=int, help="scarica al massimo N schede e si ferma")
    ap.add_argument("--riparsa", action="store_true",
                    help="riestrae i campi dall'HTML in cache, senza alcuna richiesta")
    ap.add_argument("--pausa", type=float, default=PAUSA,
                    help="secondi fra una richiesta e l'altra (default %.1f)" % PAUSA)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(DB_SCHEDE), exist_ok=True)
    db = sqlite3.connect(DB_SCHEDE)
    db.executescript(DDL)
    src = connect(DB_GIOVANILE)

    if args.stato:
        stato(db, src)
        return

    if args.riparsa:
        n = 0
        for i, gz in db.execute("SELECT id_atleta, html_gz FROM scheda_atleta "
                                "WHERE html_gz IS NOT NULL").fetchall():
            d = estrai(zlib.decompress(gz).decode("utf-8", "ignore"))
            db.execute("UPDATE scheda_atleta SET %s WHERE id_atleta=?"
                       % ", ".join("%s=?" % c for c in CAMPI),
                       tuple(d[c] for c in CAMPI) + (i,))
            n += 1
        db.commit()
        dice("Riparsate %d schede dalla cache, nessuna richiesta di rete." % n)
        return

    loc = bersagli(src, args.solo_incerti)
    gia = {r[0] for r in db.execute("SELECT id_atleta FROM scheda_atleta WHERE http_status=200")}
    da_fare = sorted(set(loc) - gia)
    if args.limite:
        da_fare = da_fare[:args.limite]

    dice("Bersaglio %d atleti | gia' fatti %d | da scaricare %d"
         % (len(loc), len(gia & set(loc)), len(da_fare)))
    if not da_fare:
        dice("Niente da fare. Per il quadro completo: --stato")
        return
    dice("Tempo stimato %s a %.1f s di pausa. Ctrl+C per interrompere: "
         "il lavoro fatto resta e il comando riprende da solo.\n"
         % (durata(len(da_fare) * args.pausa), args.pausa))

    ok = senza = falliti = 0
    avvio = time.time()
    interrotto = False
    try:
        for k, i in enumerate(da_fare, 1):
            sub, anno = loc[i]
            url = ("http://%s.ciclismo.info/scheda_corridore_risultati_gare_%d_x_y_%d.htm"
                   % (sub, i, anno))
            st, body = scarica(url)
            d = estrai(body) if st == 200 else dict.fromkeys(CAMPI)

            db.execute("""INSERT OR REPLACE INTO scheda_atleta
                (id_atleta, url, http_status, %s, html_gz, scaricato_il)
                VALUES (?,?,?,%s,?,CURRENT_TIMESTAMP)"""
                % (", ".join(CAMPI), ",".join("?" * len(CAMPI))),
                (i, url, st) + tuple(d[c] for c in CAMPI)
                + (zlib.compress(body.encode("utf-8"), 6) if st == 200 else None,))

            if st != 200:
                falliti += 1
            elif d["birth_year"] is None:
                senza += 1
            else:
                ok += 1

            if k % OGNI == 0:
                db.commit()
                trascorso = time.time() - avvio
                resta = trascorso / k * (len(da_fare) - k)
                dice("  %5d/%d (%2.0f%%)  con nascita %d, senza %d, falliti %d  "
                     "| mancano %s" % (k, len(da_fare), 100 * k / len(da_fare),
                                       ok, senza, falliti, durata(resta)))
            time.sleep(args.pausa)
    except KeyboardInterrupt:
        interrotto = True
    finally:
        db.commit()

    if interrotto:
        dice("\nInterrotto. Le schede prese sono salvate: rilancia lo stesso comando "
             "per riprendere.")
    else:
        dice("\nFatto in %s." % durata(time.time() - avvio))
    dice("  con anno di nascita %d | senza %d | richieste fallite %d" % (ok, senza, falliti))
    dice("\nOra: python scripts/03_scarica_schede.py --stato")
    dice("Poi: python scripts/01_build_tabelle.py")


if __name__ == "__main__":
    main()
