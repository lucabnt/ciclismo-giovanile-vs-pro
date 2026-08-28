"""
Porta gli esiti di carriera da ProCyclingStats dentro `tab_b`.

E' il passo che chiude la costruzione del dataset: fino a qui `tab_b` ha i predittori
ma le colonne di esito sono vuote, e senza quelle non si puo' stimare nulla.

COSA CALCOLA

    PRO                 1 se almeno una stagione in prima o seconda divisione UCI entro
                        l'anno dei 25 anni. Le classi sono WT, PT, PCT e PRT: i nomi
                        delle due divisioni sono cambiati nel tempo (vedi definizioni.md)
    year_turned_pro     prima stagione da professionista
    age_turned_pro      eta' a quella stagione
    pro_seasons         stagioni da professionista osservate, senza limite di eta'
    best_pcs_rank       migliore posizione nel ranking annuale entro i 26 anni
    tier                0 non pro | 1 pro senza top 500 | 2 top 500 | 3 top 100
    censored            1 se la finestra di osservazione non e' ancora chiusa
    team_quality_first  tasso di professionisti della societa' di partenza, calcolato
                        SOLO sulle coorti precedenti a quella dell'atleta
    pcs_u19, pcs_u23    miglior posizione PCS nelle stagioni da U19 e da U23

PRECEDENZA E ORDINE
    Va eseguito dopo 01 (che ricostruisce analisi.db da zero, quindi svuota anche
    match_pcs) e dopo 05 (che ripopola il match). L'ordine e': 01 -> 05 -> 06.

UN LIMITE DA TENERE PRESENTE
    `pcs_u19` e `pcs_u23` valgono solo per gli atleti abbinati, e l'abbinamento parte
    dai profili scaricati, che a loro volta partono dagli strati A e C di
    04_scarica_pcs.py. Lo strato C e' oggi sotto-raccolto (vedi da_fare.md §B2bis),
    quindi un `pcs_u19` nullo significa "non fra i profili raccolti", non
    necessariamente "non ha corso gare registrate".
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import DB_ANALISI, cfg

DB_PCS = "data/pcs/pcs.db"

# Prima e seconda divisione UCI, con i nomi che hanno avuto nel tempo.
CLASSI_PRO = tuple(cfg("esiti", "classi_pro"))

ETA_PRO = cfg("esiti", "eta_massima_pro")        # finestra per l'esito PRO
ETA_QUALITA = cfg("esiti", "eta_massima_qualita")  # finestra per il tier, piu' ampia di uno: vedi definizioni.md
STAGIONE_MAX_PCS = cfg("scaricamento", "stagioni_pro")[1]

SOGLIE = tuple(map(tuple, cfg("esiti", "soglie_tier")))  # posizione massima -> livello del tier

# Sotto questa numerosita' il tasso della societa' non e' una stima, e' rumore.
MIN_COORTI_PRECEDENTI = cfg("contesto", "min_coorti_precedenti")


def dice(*a):
    print(*a)
    sys.stdout.flush()


def main():
    if not os.path.exists(DB_PCS):
        sys.exit("Serve %s: esegui prima 04_scarica_pcs.py" % DB_PCS)
    db = sqlite3.connect(DB_ANALISI)
    db.execute("ATTACH DATABASE ? AS p", (DB_PCS,))

    n_match = db.execute("SELECT COUNT(*) FROM match_pcs").fetchone()[0]
    if not n_match:
        sys.exit("match_pcs e' vuota: esegui prima 05_match_pcs.py\n"
                 "(01_build_tabelle.py ricostruisce analisi.db da zero e la svuota)")

    atleti = db.execute("""SELECT b.athlete_id, b.birth_year, m.pcs_id
                           FROM tab_b b JOIN match_pcs m ON m.athlete_id = b.athlete_id
                           WHERE b.birth_year IS NOT NULL""").fetchall()
    dice("Atleti abbinati con anno di nascita noto: %d" % len(atleti))

    stagioni_pro, punti = {}, {}
    for pid, s, cl in db.execute("SELECT pcs_id, season, team_class FROM p.pcs_rider_team"):
        if cl in CLASSI_PRO:
            stagioni_pro.setdefault(pid, set()).add(s)
    for pid, s, rk in db.execute("""SELECT pcs_id, season, rank_pos FROM p.pcs_rider_points
                                    WHERE rank_pos IS NOT NULL"""):
        punti.setdefault(pid, {})[s] = rk

    agg = []
    for aid, by, pid in atleti:
        sp = sorted(x for x in stagioni_pro.get(pid, ()) if x <= by + ETA_PRO)
        tutte = sorted(stagioni_pro.get(pid, ()))
        pr = punti.get(pid, {})
        best = min((r for s, r in pr.items() if s <= by + ETA_QUALITA), default=None)

        tier = 0
        if sp:
            tier = 1
            for soglia, livello in SOGLIE:
                if best is not None and best <= soglia:
                    tier = livello
                    break

        def miglior(lo, hi):
            v = [r for s, r in pr.items() if lo <= s - by <= hi]
            return min(v) if v else None

        agg.append((pid, 1, int(bool(sp)), tier,
                    sp[0] if sp else None,
                    sp[0] - by if sp else None,
                    len(tutte),
                    best,
                    int(by + ETA_QUALITA > STAGIONE_MAX_PCS),
                    miglior(17, 18), miglior(19, 22),
                    aid))

    db.executemany("""UPDATE tab_b SET pcs_id=?, pcs_matched=?, PRO=?, tier=?,
                      year_turned_pro=?, age_turned_pro=?, pro_seasons=?,
                      best_pcs_rank=?, censored=?, pcs_u19=?, pcs_u23=?
                      WHERE athlete_id=?""", agg)

    # Chi non e' abbinato non e' professionista: e' il default, ma va scritto
    # esplicitamente, altrimenti PRO resta NULL e i modelli perdono le righe.
    db.execute("""UPDATE tab_b SET pcs_matched=0, PRO=0, tier=0, pro_seasons=0
                  WHERE pcs_matched IS NULL""")

    # --- qualita' della societa' di partenza, solo sulle coorti precedenti -----
    righe = db.execute("""SELECT athlete_id, birth_year, team_first, PRO FROM tab_b
                          WHERE team_first IS NOT NULL AND birth_year IS NOT NULL""").fetchall()
    per_societa = {}
    for aid, by, team, pro in righe:
        per_societa.setdefault(team, []).append((by, pro))
    agg2 = []
    for aid, by, team, pro in righe:
        prec = [p for b, p in per_societa[team] if b < by]
        if len(prec) >= MIN_COORTI_PRECEDENTI:
            agg2.append((sum(prec) / len(prec), len(prec), aid))
    db.executemany("UPDATE tab_b SET team_quality_first=?, team_quality_n=? WHERE athlete_id=?",
                   agg2)
    db.commit()

    # --- resoconto ---------------------------------------------------------
    dice("\nESITI SCRITTI IN tab_b")
    for chiave, et in (("domanda_a_c", "Domande A e C"), ("domanda_b", "Domanda B")):
        lo, hi = cfg("coorti", chiave)
        et = "%d-%d (%s)" % (lo, hi, et)
        r = db.execute("""SELECT COUNT(*), SUM(PRO), SUM(tier>=2), SUM(tier=3), SUM(censored)
                          FROM tab_b WHERE sesso=? AND birth_year BETWEEN ? AND ?""",
                       (cfg("studio", "sesso"), lo, hi)).fetchone()
        dice("   %-28s n=%d  PRO=%d  top500=%d  top100=%d  censurati=%d"
             % (et, r[0], r[1], r[2], r[3], r[4] or 0))
    lo, hi = cfg("coorti", "domanda_a_c")
    sesso = cfg("studio", "sesso")
    dice("\n   distribuzione del tier, coorti %d-%d (%s):" % (lo, hi, sesso))
    for t, n in db.execute("""SELECT tier, COUNT(*) FROM tab_b WHERE sesso=?
                              AND birth_year BETWEEN ? AND ? GROUP BY 1 ORDER BY 1""",
                           (sesso, lo, hi)):
        et = ["non pro", "pro senza top 500", "top 500", "top 100"][t]
        dice("      %d  %-20s %5d" % (t, et, n))
    r = db.execute("SELECT COUNT(team_quality_first), ROUND(AVG(team_quality_first),4) "
                   "FROM tab_b").fetchone()
    dice("\n   team_quality_first calcolata per %d atleti (media %.3f)" % (r[0], r[1] or 0))
    dice("   solo dove la societa' ha almeno %d atleti in coorti precedenti"
         % MIN_COORTI_PRECEDENTI)


if __name__ == "__main__":
    main()
