"""
Collega gli atleti giovanili di ciclismo.info ai profili di ProCyclingStats.

L'IDEA
    Si va da PCS verso i giovanili, non viceversa: l'insieme da matchare sono i ~1.000
    italiani profilati su PCS, non i 12.357 ragazzi. Chi non e' mai stato professionista
    contribuisce con PRO = 0, che e' gia' il default.

LA CHIAVE
    Nome normalizzato + data di nascita completa, disponibile su entrambi i lati per la
    quasi totalita' degli atleti. E' molto piu' forte di quanto il piano prevedesse:
    risolve automaticamente gli omonimi della stessa annata, che erano il caso che la
    guida indicava da sciogliere a mano.

    Il nome e' normalizzato con `chiave_match`: maiuscolo, senza accenti, punteggiatura
    rimossa e token ordinati alfabeticamente. L'ordinamento serve perche' PCS e
    ciclismo.info scrivono nome e cognome in ordine diverso, e perche' i nomi doppi
    compaiono in ordine diverso nelle due fonti.

I PASSAGGI, dal piu' sicuro al meno
    1  esatto_data   chiave identica + data di nascita identica
    2  esatto_anno   chiave identica + anno identico (una delle due parti non ha il giorno)
    3  data_forte    data identica + chiave molto simile (refusi: CAPELLI / CAPPELLI)
    4  fuzzy         chiave molto simile + anno entro 1     -> sempre da verificare a mano

    Un abbinamento viene scritto solo se e' univoco in entrambe le direzioni. I casi in
    cui un atleta ha piu' candidati, o un profilo PCS corrisponde a piu' atleti, sono
    marcati `ambiguo` e lasciati alla verifica manuale.

COME SI USA
    python scripts/05_match_pcs.py
    python scripts/05_match_pcs.py --soglia 0.88     # tolleranza del fuzzy

OUTPUT
    data/analisi/analisi.db -> match_pcs   (anonimo: solo athlete_id e pcs_id)
    data/private/match_da_verificare.csv   (con i nomi: NON committare)
"""
import argparse
import csv
import os
import re
import sqlite3
import sys
from collections import defaultdict
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import DB_ANALISI, cfg, sesso_in_studio

# Un archivio per sesso: le due popolazioni non condividono corridori, squadre ne'
# classifica mondiale, e tenerle insieme corromperebbe la classifica annuale.
SESSO = sesso_in_studio()
DB_PCS = "data/pcs/pcs.db" if SESSO == "M" else "data/pcs/pcs_%s.db" % SESSO
CROSSWALK = "data/private/crosswalk_atleti.csv"
AUDIT = "data/private/match_da_verificare.csv"
SOGLIA = 0.90

# Prima e seconda divisione UCI, con i nomi che hanno avuto nel tempo (vedi definizioni.md)
CLASSI_PRO = tuple(cfg("esiti", "classi_pro"))


def dice(*a):
    print(*a)
    sys.stdout.flush()


def norm_data(d):
    """PCS scrive le date senza zero iniziale: 1991-7-20. Qui si uniformano."""
    if not d:
        return None
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", str(d).strip())
    return "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def simile(a, b):
    return SequenceMatcher(None, a, b).ratio()


def carica():
    if not os.path.exists(CROSSWALK):
        sys.exit("Serve %s: esegui prima 01_build_tabelle.py" % CROSSWALK)
    if not os.path.exists(DB_PCS):
        sys.exit("Serve %s: esegui prima 04_scarica_pcs.py" % DB_PCS)

    gio = []
    # Il crosswalk contiene entrambi i sessi, l'archivio PCS uno solo: si tengono gli
    # atleti del sesso in studio, altrimenti si cercherebbero i maschi fra le rose
    # femminili con l'unico effetto di produrre abbinamenti spuri.
    dell_sesso = {r[0] for r in sqlite3.connect(DB_ANALISI).execute(
        "SELECT athlete_id FROM tab_b WHERE sesso = ?", (SESSO,))}

    with open(CROSSWALK, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not r["chiave_match"] or r["athlete_id"] not in dell_sesso:
                continue
            gio.append({
                "athlete_id": r["athlete_id"], "src": r["id_atleta_src"],
                "nome": r["nome_completo"], "chiave": r["chiave_match"],
                "data": norm_data(r["birth_date"]),
                "anno": int(r["birth_year"]) if r["birth_year"] else None,
                "regione": r["regione"],
            })

    pcs = []
    con = sqlite3.connect(DB_PCS)
    for pid, ch, bd, by in con.execute("""
            SELECT pcs_id, chiave_match, birthdate, birth_year FROM pcs_rider
            WHERE nazionalita = 'IT' AND chiave_match <> ''"""):
        pcs.append({"pcs_id": pid, "chiave": ch, "data": norm_data(bd), "anno": by})

    # profilo di carriera, per sapere chi e' professionista e a che livello
    prof = {}
    for pid, in con.execute("SELECT pcs_id FROM pcs_rider WHERE nazionalita='IT'"):
        prof[pid] = {"pro": False, "best": None}
    for pid, cl in con.execute("SELECT pcs_id, team_class FROM pcs_rider_team"):
        if pid in prof and cl in CLASSI_PRO:
            prof[pid]["pro"] = True
    for pid, rk in con.execute("SELECT pcs_id, MIN(rank_pos) FROM pcs_rider_points "
                               "WHERE rank_pos IS NOT NULL GROUP BY pcs_id"):
        if pid in prof:
            prof[pid]["best"] = rk
    return gio, pcs, prof


def abbina(gio, pcs, soglia):
    """Quattro passaggi, dal piu' sicuro al meno. Ogni atleta viene assegnato una volta sola."""
    per_chiave = defaultdict(list)
    for g in gio:
        per_chiave[g["chiave"]].append(g)
    per_data = defaultdict(list)
    for g in gio:
        if g["data"]:
            per_data[g["data"]].append(g)

    proposte = defaultdict(list)          # pcs_id -> [(athlete_id, metodo, score)]
    for p in pcs:
        cand = per_chiave.get(p["chiave"], [])

        esatti = [g for g in cand if p["data"] and g["data"] == p["data"]]
        if esatti:
            for g in esatti:
                proposte[p["pcs_id"]].append((g, "esatto_data", 1.0))
            continue

        anno = [g for g in cand if p["anno"] and g["anno"] == p["anno"]]
        if anno:
            for g in anno:
                proposte[p["pcs_id"]].append((g, "esatto_anno", 0.98))
            continue

        # stessa data ma nome leggermente diverso: sono i refusi di una delle due fonti
        if p["data"]:
            forti = [g for g in per_data.get(p["data"], [])
                     if simile(g["chiave"], p["chiave"]) >= 0.80]
            if forti:
                for g in forti:
                    proposte[p["pcs_id"]].append(
                        (g, "data_forte", simile(g["chiave"], p["chiave"])))
                continue

        # ultimo tentativo: nome simile e anno vicino
        for g in gio:
            if not (g["anno"] and p["anno"] and abs(g["anno"] - p["anno"]) <= 1):
                continue
            if abs(len(g["chiave"]) - len(p["chiave"])) > 3:
                continue
            s = simile(g["chiave"], p["chiave"])
            if s >= soglia:
                proposte[p["pcs_id"]].append((g, "fuzzy", s))

    # univocita' nei due sensi: un athlete_id non puo' finire su due pcs_id e viceversa
    per_atleta = defaultdict(list)
    for pid, lista in proposte.items():
        for g, met, sc in lista:
            per_atleta[g["athlete_id"]].append(pid)

    esiti = {}
    for pid, lista in proposte.items():
        lista.sort(key=lambda x: -x[2])
        g, met, sc = lista[0]
        ambiguo = len(lista) > 1 or len(set(per_atleta[g["athlete_id"]])) > 1
        esiti[pid] = {"g": g, "metodo": met, "score": sc, "ambiguo": int(ambiguo),
                      "alternativi": [x[0]["athlete_id"] for x in lista[1:]]}
    return esiti


def annotazioni_precedenti():
    """Verdetti e note scritti a mano nel file di lavoro, per identificativo di origine.

    Si rileggono SOLO 'verdetto' e 'nota': tutte le altre colonne vengono riscritte dai
    database, perche' aprendo il file in Excel le date vengono riformattate nel formato
    locale e non sono piu' attendibili come dato.
    """
    precedenti = {}
    if os.path.exists(AUDIT):
        with open(AUDIT, encoding="utf-8-sig") as f:
            testa = f.readline()
            f.seek(0)
            sep = ";" if testa.count(";") > testa.count(",") else ","
            for r in csv.DictReader(f, delimiter=sep):
                v, n = (r.get("verdetto") or "").strip(), (r.get("nota") or "").strip()
                if v or n:
                    precedenti[r.get("id_src")] = (v, n)
    return precedenti


def main():
    ap = argparse.ArgumentParser(description="Collega gli atleti giovanili ai profili PCS.")
    ap.add_argument("--soglia", type=float, default=SOGLIA,
                    help="similarita' minima per il passaggio fuzzy (default %.2f)" % SOGLIA)
    args = ap.parse_args()

    gio, pcs, prof = carica()
    dice("Giovanili %d | profili PCS italiani %d" % (len(gio), len(pcs)))
    esiti = abbina(gio, pcs, args.soglia)

    dst = sqlite3.connect(DB_ANALISI)
    dst.execute("DELETE FROM match_pcs")
    righe, audit = [], []
    # Le verifiche fatte a mano stanno nel file di lavoro: si portano anche nella tabella,
    # cosi' chi legge match_pcs vede quali abbinamenti sono stati controllati uno per uno.
    # Prima 'verificato' e 'nota' restavano vuoti per tutti, e la prova del lavoro manuale
    # stava solo in un file che la tabella non citava.
    precedenti = annotazioni_precedenti()
    for pid, e in esiti.items():
        g = e["g"]
        verdetto, nota = precedenti.get(str(g["src"]), ("", ""))
        righe.append((g["athlete_id"], pid, e["metodo"], round(e["score"], 3),
                      next((p["anno"] for p in pcs if p["pcs_id"] == pid), None),
                      e["ambiguo"], ",".join(e["alternativi"]) or None,
                      # nel file il giudizio sta quasi sempre nella nota, con il
                      # verdetto vuoto: conta come verificata una riga annotata
                      1 if (verdetto or nota) else 0,
                      "; ".join(x for x in (verdetto, nota) if x) or None))
        audit.append({
            "athlete_id": g["athlete_id"], "id_src": g["src"], "nome_giovanile": g["nome"],
            "pcs_id": pid, "metodo": e["metodo"], "score": round(e["score"], 3),
            "data_giovanile": g["data"] or "",
            "data_pcs": next((p["data"] for p in pcs if p["pcs_id"] == pid), "") or "",
            "regione": g["regione"], "ambiguo": e["ambiguo"],
            "alternativi": ",".join(e["alternativi"]),
            "professionista": int(prof.get(pid, {}).get("pro", False)),
            "miglior_rank_pcs": prof.get(pid, {}).get("best") or "",
            "verdetto": "", "nota": "",
        })
    dst.executemany("INSERT INTO match_pcs (athlete_id, pcs_id, metodo, score, "
                    "birth_year_pcs, ambiguo, candidati, verificato, nota) "
                    "VALUES (?,?,?,?,?,?,?,?,?)", righe)
    dst.commit()

    # --- resoconto ---
    from collections import Counter
    met = Counter(e["metodo"] for e in esiti.values())
    dice("\nABBINAMENTI: %d su %d profili PCS (%.1f%%)"
         % (len(esiti), len(pcs), 100 * len(esiti) / len(pcs)))
    for k in ("esatto_data", "esatto_anno", "data_forte", "fuzzy"):
        if met.get(k):
            dice("   %-14s %4d" % (k, met[k]))
    amb = sum(e["ambiguo"] for e in esiti.values())
    dice("   %-14s %4d  <- da sciogliere a mano" % ("ambigui", amb))
    non = len(pcs) - len(esiti)
    dice("   %-14s %4d  <- profili PCS senza riscontro nei giovanili" % ("non abbinati", non))

    pro_tot = sum(1 for p in prof.values() if p["pro"])
    pro_match = sum(1 for pid, e in esiti.items() if prof.get(pid, {}).get("pro"))
    dice("\nPROFESSIONISTI: %d fra i profili PCS, %d abbinati (%.1f%%)"
         % (pro_tot, pro_match, 100 * pro_match / pro_tot if pro_tot else 0))
    dice("   I non abbinati sono in gran parte atleti che non hanno mai fatto punti nelle")
    dice("   classifiche giovanili italiane: stranieri, o arrivati da altre discipline.")

    # Le annotazioni gia' scritte a mano nel file non vanno perse a ogni riesecuzione:
    # 'precedenti' e' stato letto prima di scrivere la tabella.
    conservate = 0
    for r in audit:
        v, n = precedenti.get(str(r["id_src"]), ("", ""))
        if v or n:
            r["verdetto"], r["nota"] = v, n
            conservate += 1

    with open(AUDIT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, list(audit[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(sorted(audit, key=lambda r: (-r["professionista"], r["metodo"])))
    if precedenti:
        dice("\nAnnotazioni gia' scritte a mano, conservate: %d su %d"
             % (conservate, len(precedenti)))
    dice("\nDa verificare a mano: %s" % AUDIT)
    dice("   La guida chiede la verifica al 100%% dei candidati professionisti: sono %d,"
         % pro_match)
    dice("   e nel file stanno in testa. Poi i %d ambigui e i %d fuzzy."
         % (amb, met.get("fuzzy", 0)))


if __name__ == "__main__":
    main()
