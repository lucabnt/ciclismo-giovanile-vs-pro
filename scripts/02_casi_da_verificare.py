"""
Produce le liste di lavoro per la verifica manuale (FASE 1, prerequisito dello STEP 6).

Output in data/private/ (contengono nomi: non vanno committati)
  - casi_omonimia.csv        id_atleta distinti con lo stesso nome e anni di nascita compatibili:
                             candidati a essere la stessa persona spezzata in due
  - casi_quasi_omonimia.csv  stesso nome e cognome a distanza 1: possibili refusi che hanno
                             spezzato un atleta in due. Va rieseguito dopo 03_scarica_schede.py:
                             con la data di nascita completa il filtro diventa molto piu' netto
  - casi_eta_incoerente.csv  atleti le cui presenze si contraddicono fra loro

Le decisioni si registrano in data/private/manual/ (fuori dal repository come tutto data/private/)
  - fusioni_atleti.csv       id_atleta_src, id_canonico, nota
  - esclusioni_atleti.csv    id_atleta_src, motivo
e vengono applicate al prossimo giro di 01_build_tabelle.py.
"""
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import CATEGORIE, DB_ANALISI, DB_GIOVANILE, connect

import sqlite3


def carriera(src, id_atleta):
    """Righe della carriera, con societa' e regione, per la disambiguazione manuale."""
    rows = src.execute("""
        SELECT cat.slug, cp.anno, cp.anno_corso, cp.posizione, cp.punti,
               COALESCE(sq.nome_societa, cp.nome_squadra_raw) AS societa,
               (cp.url_origine LIKE '%primo_anno%') AS primo,
               cp.sotto_gruppo
        FROM   classifiche_punti cp
        JOIN   categorie cat ON cat.id_categoria = cp.id_categoria
        LEFT   JOIN squadre sq ON sq.id_squadra = cp.id_squadra
        WHERE  cp.id_atleta = ? AND cp.mese IS NULL AND cp.tipo_soggetto = 'individuale'
          AND  (cat.gruppo IN (1, 2) OR cp.sotto_gruppo = 'under23')
        ORDER  BY cp.anno, cat.slug
    """, (id_atleta,)).fetchall()
    reg = src.execute("""SELECT regione, COUNT(*) FROM atleti_regioni WHERE id_atleta = ?
                         GROUP BY 1 ORDER BY 2 DESC""", (id_atleta,)).fetchall()
    voci, societa, stagioni = [], [], set()
    for r in rows:
        cat = CATEGORIE[r["slug"]][0]
        marca = "y1" if r["primo"] else ""
        voci.append("%d %s%s p%d/%gpt" % (r["anno"], cat, marca, r["posizione"], r["punti"]))
        stagioni.add(r["anno"])
        if r["societa"]:
            societa.append(r["societa"])
    return {
        "carriera": " | ".join(voci),
        "societa": " ; ".join(dict.fromkeys(societa)),
        "regioni": " ; ".join("%s(%d)" % (a, b) for a, b in reg),
        "stagioni": stagioni,
        "prima": min(stagioni) if stagioni else None,
        "ultima": max(stagioni) if stagioni else None,
    }


def distanza_uno(x, y):
    """Vero se i due cognomi differiscono per una sola lettera (sostituita o mancante)."""
    if abs(len(x) - len(y)) > 1:
        return False
    if len(x) == len(y):
        return sum(p != q for p, q in zip(x, y)) == 1
    lo, hi = (x, y) if len(x) < len(y) else (y, x)
    return any(hi[:i] + hi[i + 1:] == lo for i in range(len(hi)))


def suggerisci(a, b, ia, ib, sovrapposte):
    """Verdetto proposto per una coppia di omonimi. Da rivedere, non da applicare al buio.

    La regola sulle nascite entrambe 'certo' si appoggia a un fatto misurato: fra i 5.068
    atleti con almeno due segnali di nascita indipendenti di livello 1, i segnali
    concordano in 5.067 casi (99,98%). Due stime 'certo' diverse sono quindi molto piu'
    probabilmente due persone che un errore.
    """
    if sovrapposte:
        return "diversi", "presenti nella stessa stagione"
    reg_a = ia["regioni"].split("(")[0]
    reg_b = ib["regioni"].split("(")[0]
    if reg_a and reg_b and reg_a != reg_b:
        return "diversi", "regioni diverse (%s / %s)" % (reg_a, reg_b)
    if a["birth_year"] != b["birth_year"]:
        if a["birth_year_conf"] == b["birth_year_conf"] == "certo":
            return "diversi", "due stime di nascita di livello 1 discordanti"
        return "", "nascite discordanti ma almeno una presunta: da decidere"
    contigue = (ia["ultima"] < ib["prima"]) or (ib["ultima"] < ia["prima"])
    if contigue and reg_a == reg_b:
        return "stessa", "stessa nascita, stessa regione, carriere consecutive"
    return "", "da decidere"


def main():
    src = connect(DB_GIOVANILE)
    an = sqlite3.connect(DB_ANALISI)
    an.row_factory = sqlite3.Row
    os.makedirs("data/private", exist_ok=True)
    os.makedirs("data/private/manual", exist_ok=True)

    cross = {}
    with open("data/private/crosswalk_atleti.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cross[int(r["id_atleta_src"])] = r

    # ---- 1. omonimi con anni di nascita compatibili -----------------------
    per_nome = defaultdict(list)
    for i, r in cross.items():
        per_nome[r["nome_completo"].upper()].append(i)

    righe = []
    for nome, ids in sorted(per_nome.items()):
        if len(ids) < 2:
            continue
        info = {i: carriera(src, i) for i in ids}
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                i, j = ids[a], ids[b]
                by_i = cross[i]["birth_year"]
                by_j = cross[j]["birth_year"]
                if not (by_i and by_j) or abs(int(by_i) - int(by_j)) > 1:
                    continue
                sovrapposte = info[i]["stagioni"] & info[j]["stagioni"]
                sugg, perche = suggerisci(cross[i], cross[j], info[i], info[j], sovrapposte)
                righe.append({
                    "nome": nome,
                    "id_a": i, "id_b": j,
                    "nascita_a": by_i, "nascita_b": by_j,
                    "conf_a": cross[i]["birth_year_conf"], "conf_b": cross[j]["birth_year_conf"],
                    # una sovrapposizione di stagioni esclude che siano la stessa persona
                    "stagioni_sovrapposte": ",".join(map(str, sorted(sovrapposte))) or "",
                    "verdetto_suggerito": sugg, "motivo_suggerito": perche,
                    "regioni_a": info[i]["regioni"], "regioni_b": info[j]["regioni"],
                    "societa_a": info[i]["societa"], "societa_b": info[j]["societa"],
                    "carriera_a": info[i]["carriera"], "carriera_b": info[j]["carriera"],
                    "verdetto": "", "nota": "",
                })

    campi = list(righe[0].keys()) if righe else []
    with open("data/private/casi_omonimia.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, campi, delimiter=";")
        w.writeheader()
        w.writerows(righe)

    # ---- 1b. quasi omonimi: refusi che possono aver spezzato un atleta -----
    per_primo_nome = defaultdict(list)
    for i, r in cross.items():
        per_primo_nome[r["nome"].upper()].append(i)

    righe_q = []
    for nome, ids in sorted(per_primo_nome.items()):
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                i, j = ids[a], ids[b]
                ca, cb = cross[i]["cognome"].upper(), cross[j]["cognome"].upper()
                if ca == cb or not distanza_uno(ca, cb):
                    continue
                ia, ib = carriera(src, i), carriera(src, j)
                if ia["stagioni"] & ib["stagioni"]:
                    continue                       # stagioni sovrapposte: persone diverse
                da, db = cross[i]["birth_date"], cross[j]["birth_date"]
                ya, yb = cross[i]["birth_year"], cross[j]["birth_year"]
                if da and db:
                    # con la data completa la decisione e' netta in entrambi i versi
                    if da != db:
                        continue
                    forza = "data di nascita identica"
                elif ya and yb and abs(int(ya) - int(yb)) <= 1:
                    forza = "solo anno di nascita, entro 1"
                else:
                    continue
                ra = ia["regioni"].split("(")[0]
                rb = ib["regioni"].split("(")[0]
                if ra and rb and ra != rb:
                    continue
                righe_q.append({
                    "nome": nome, "cognome_a": ca, "cognome_b": cb,
                    "id_a": i, "id_b": j, "nascita_a": da or ya, "nascita_b": db or yb,
                    "forza_indizio": forza, "regione": ra or rb,
                    "societa_a": ia["societa"], "societa_b": ib["societa"],
                    "carriera_a": ia["carriera"], "carriera_b": ib["carriera"],
                    "verdetto": "", "nota": "",
                })

    with open("data/private/casi_quasi_omonimia.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        if righe_q:
            w = csv.DictWriter(f, list(righe_q[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(righe_q)

    # ---- 2. atleti con presenze contraddittorie ---------------------------
    inc = an.execute("""
        SELECT DISTINCT athlete_id FROM tab_a WHERE eta_coerente = 0
    """).fetchall()
    inv = {r["athlete_id"]: i for i, r in cross.items()}
    righe2 = []
    for r in inc:
        i = inv.get(r["athlete_id"])
        if i is None:
            continue
        c = carriera(src, i)
        motivi = []
        anni = defaultdict(set)
        for x in src.execute("""SELECT cat.slug, cp.anno FROM classifiche_punti cp
                JOIN categorie cat ON cat.id_categoria = cp.id_categoria
                WHERE cp.id_atleta=? AND cp.mese IS NULL AND cp.tipo_soggetto='individuale'
                  AND (cat.gruppo IN (1,2) OR cp.sotto_gruppo='under23')""", (i,)):
            anni[x["anno"]].add(CATEGORIE[x["slug"]][0])
        for a, cats in anni.items():
            if len(cats) > 1:
                motivi.append("%d in %s" % (a, "+".join(sorted(cats))))
        righe2.append({
            "nome": cross[i]["nome_completo"], "id": i,
            "nascita": cross[i]["birth_year"], "conf": cross[i]["birth_year_conf"],
            "categorie_stessa_stagione": " ; ".join(motivi),
            "omonimi": len(per_nome[cross[i]["nome_completo"].upper()]) - 1,
            "regioni": c["regioni"], "societa": c["societa"], "carriera": c["carriera"],
            "verdetto": "", "nota": "",
        })
    righe2.sort(key=lambda r: (-r["omonimi"], r["nome"]))
    with open("data/private/casi_eta_incoerente.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, list(righe2[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(righe2)

    # ---- 3. file delle decisioni, se non esistono -------------------------
    for nome, intestazione in (("fusioni_atleti.csv", ["id_atleta_src", "id_canonico", "nota"]),
                               ("esclusioni_atleti.csv", ["id_atleta_src", "motivo"])):
        p = os.path.join("data/private/manual", nome)
        if not os.path.exists(p):
            with open(p, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(intestazione)

    print("data/private/casi_omonimia.csv        %d coppie da decidere" % len(righe))
    print("   di cui con stagioni sovrapposte:   %d  (persone diverse, nessuna azione)"
          % sum(1 for r in righe if r["stagioni_sovrapposte"]))
    print("   di cui senza sovrapposizione:      %d  (da guardare uno per uno)"
          % sum(1 for r in righe if not r["stagioni_sovrapposte"]))
    print("data/private/casi_quasi_omonimia.csv  %d coppie da decidere (refusi nel cognome)"
          % len(righe_q))
    print("   con data di nascita identica:      %d"
          % sum(1 for r in righe_q if r["forza_indizio"].startswith("data")))
    print("data/private/casi_eta_incoerente.csv  %d atleti da decidere" % len(righe2))
    print("   di cui con un omonimo:             %d" % sum(1 for r in righe2 if r["omonimi"]))
    print("   di cui in due categorie lo stesso anno: %d"
          % sum(1 for r in righe2 if r["categorie_stessa_stagione"]))
    print("\ndecisioni da scrivere in data/private/manual/fusioni_atleti.csv e esclusioni_atleti.csv")


if __name__ == "__main__":
    main()
