"""
STEP 26 — le scelte discrezionali del disegno, e quanto cambierebbero le conclusioni.

PERCHE' SERVE
    Diverse decisioni di questo studio sono difendibili ma non obbligate: dove finisce
    il professionismo, entro quale eta' contarlo, dove mettere la soglia del «top».
    Ognuna e' stata presa una volta e poi usata ovunque. Un lettore ha diritto di sapere
    quanto le conclusioni dipendano da quelle scelte invece che dai dati.

    Questo script rifa' i conti cambiando una decisione alla volta e riporta due numeri
    per ciascuna variante: **quanti professionisti risultano** e **quanto il rendimento
    Under 19 li distingue**. Se la seconda quantita' resta stabile, le conclusioni non
    dipendono dalla scelta.

COME SI MISURA LA CAPACITA' DISCRIMINANTE SENZA UN MODELLO
    Con il delta di Cliff, che conta quante volte un professionista sta sopra un non
    professionista, e si converte in AUC con `AUC = (delta + 1) / 2`. E' esatto, non
    richiede assunzioni e non richiede R: qui serve un confronto fra varianti, non una
    stima con intervallo.

LA QUARTA SENSIBILITA' DELLA GUIDA, E PERCHE' NON SI FA COSI'
    La guida chiede di confrontare l'analisi sui casi completi con un'imputazione
    multipla dei percentili mancanti. Qui non e' appropriato, e vale la pena dire perche'
    invece di eseguirla e basta.

    Un percentile mancante non e' un dato perduto: e' un atleta che in quella stagione
    non ha fatto punti. L'informazione c'e' ed e' negativa. Imputarlo significherebbe
    attribuire un rendimento a chi non ne ha avuto, cioe' inventare il dato invece di
    recuperarlo. L'assunzione MAR — che il valore mancante sia indipendente dal valore
    stesso, dato il resto — e' qui manifestamente falsa: chi non entra in classifica e'
    sistematicamente piu' debole di chi ci entra.

    Il confronto corretto e' un altro, e questo script lo fa: l'analisi sui presenti
    contro l'analisi su tutta la coorte trattando l'assenza come una categoria.

USO
    python scripts/10_sensibilita.py
"""
import os
import sqlite3
import sys
from bisect import bisect_left, bisect_right

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.join(QUI, "..", "report"))
from lib_giovanile import DB_ANALISI, cfg           # noqa: E402
from lib_risultati import Archivio                  # noqa: E402

DB_PCS = "data/pcs/pcs.db"
CELLA = "U19y2"          # il predittore su cui si misura la stabilita'

# Il confronto fra chi e' in classifica e tutta la coorte si fa a due eta': l'ultima
# misura giovanile e la prima. La domanda e' se non esserci a tredici anni dica quanto
# non esserci a diciotto — cioe' se l'assenza sia informativa gia' all'inizio.
CELLE_ASSENZA = [("U19y2", "Under 19 secondo anno"),
                 ("U15y1", "Under 15 primo anno")]


def cliff(a, b):
    """delta = P(a > b) - P(a < b)."""
    if not a or not b:
        return None
    b = sorted(b)
    s = sum(bisect_left(b, x) - (len(b) - bisect_right(b, x)) for x in a)
    return s / (len(a) * len(b))


def carica(db):
    """Tutto cio' che serve per ricalcolare gli esiti: squadre e posizioni per stagione."""
    squadre, punti = {}, {}
    for pid, s, cl in db.execute("SELECT pcs_id, season, team_class FROM p.pcs_rider_team"):
        squadre.setdefault(pid, []).append((s, cl))
    for pid, s, rk in db.execute("""SELECT pcs_id, season, rank_pos FROM p.pcs_rider_points
                                    WHERE rank_pos IS NOT NULL"""):
        punti.setdefault(pid, {})[s] = rk
    return squadre, punti


def esito(atleti, squadre, punti, classi, eta_pro, soglia=None, eta_qualita=None):
    """Ricalcola l'esito con una definizione alternativa.

    Restituisce due liste di percentili, quella di chi raggiunge l'esito e quella di chi
    no: sono esattamente cio' che serve al delta di Cliff.
    """
    dentro, fuori = [], []
    for by, pid, pct in atleti:
        if soglia is None:
            ok = any(cl in classi and s <= by + eta_pro
                     for s, cl in squadre.get(pid, ()))
        else:
            pro = any(cl in classi and s <= by + eta_pro
                      for s, cl in squadre.get(pid, ()))
            pr = punti.get(pid, {})
            limite = by + eta_qualita if eta_qualita is not None else 9999
            best = min((r for s, r in pr.items() if s <= limite), default=None)
            ok = bool(pro and best is not None and best <= soglia)
        (dentro if ok else fuori).append(pct)
    return dentro, fuori


def riga(nome, dentro, fuori):
    d = cliff(dentro, fuori)
    return [nome, len(dentro), len(dentro) + len(fuori),
            round(100 * len(dentro) / (len(dentro) + len(fuori)), 2) if fuori else None,
            round((d + 1) / 2, 3) if d is not None else None]


def main():
    if not os.path.exists(DB_PCS):
        sys.exit("Serve %s: esegui prima 04_scarica_pcs.py" % DB_PCS)
    db = sqlite3.connect(DB_ANALISI)
    db.execute("ATTACH DATABASE ? AS p", (DB_PCS,))

    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    classi_base = tuple(cfg("esiti", "classi_pro"))
    eta_base = cfg("esiti", "eta_massima_pro")
    eta_qualita = cfg("esiti", "eta_massima_qualita")
    soglia_base = cfg("esiti", "soglie_tier")[1][0]     # la soglia intermedia, 500

    atleti = db.execute("""SELECT b.birth_year, COALESCE(m.pcs_id, ''), b.pct_%s
                           FROM tab_b b LEFT JOIN match_pcs m ON m.athlete_id = b.athlete_id
                           WHERE b.sesso = ? AND b.birth_year BETWEEN ? AND ?
                             AND b.present_%s = 1 AND b.pct_%s IS NOT NULL"""
                        % (CELLA, CELLA, CELLA), (sesso, lo, hi)).fetchall()
    squadre, punti = carica(db)
    print("STEP 26 — sensibilita' su %d atleti presenti in %s, coorti %d-%d"
          % (len(atleti), CELLA, lo, hi))

    with Archivio("sensibilita") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))
        ar.valore("cella", CELLA)
        ar.valore("n", len(atleti))

        # --- 1. cosa conta come professionismo ------------------------------
        varianti = [
            ("prima e seconda divisione (scelta dello studio)", classi_base),
            ("solo prima divisione (WorldTour)", ("WT",)),
            ("includendo anche le Continental", classi_base + ("CT",)),
        ]
        righe = []
        for nome, classi in varianti:
            righe.append(riga(nome, *esito(atleti, squadre, punti, classi, eta_base)))
        ar.tabella("definizione", righe,
                   colonne=["cosa conta come professionismo", "professionisti", "atleti",
                            "% pro", "AUC del percentile Under 19"],
                   titolo="Se si cambia la definizione di professionista",
                   nota="la definizione sposta molto quanti sono, pochissimo quanto il "
                        "rendimento giovanile li distingue")

        # --- 2. entro quale eta' ---------------------------------------------
        righe = []
        for e in (24, eta_base, 26):
            nome = "entro i %d anni%s" % (e, " (scelta dello studio)"
                                          if e == eta_base else "")
            righe.append(riga(nome, *esito(atleti, squadre, punti, classi_base, e)))
        ar.tabella("finestra", righe,
                   colonne=["finestra d'eta'", "professionisti", "atleti", "% pro",
                            "AUC del percentile Under 19"],
                   titolo="Se si sposta la finestra d'eta'")

        # --- 3. dove si mette la soglia del «top» -----------------------------
        righe = []
        for s in (200, 300, soglia_base, 1000):
            nome = "top %d%s" % (s, " (scelta dello studio)" if s == soglia_base else "")
            righe.append(riga(nome, *esito(atleti, squadre, punti, classi_base,
                                           eta_base, soglia=s,
                                           eta_qualita=eta_qualita)))
        righe.append(riga("top %d, senza limite d'eta'" % soglia_base,
                          *esito(atleti, squadre, punti, classi_base, eta_base,
                                 soglia=soglia_base, eta_qualita=None)))
        ar.tabella("soglia", righe,
                   colonne=["soglia del «top»", "atleti che la raggiungono", "atleti",
                            "%", "AUC del percentile Under 19"],
                   titolo="Se si sposta la soglia del «top»",
                   nota="sono le due scelte piu' discrezionali del disegno: dove mettere "
                        "la soglia e se limitare l'eta' entro cui raggiungerla")

        # --- 4. presenti soltanto, oppure tutta la coorte ---------------------
        # Il confronto che sostituisce l'imputazione multipla: chi non e' in classifica
        # non ha un percentile mancante, ha un rendimento che non c'e' stato.
        righe = []
        for cella, etichetta in CELLE_ASSENZA:
            tutti = db.execute("""SELECT b.birth_year, COALESCE(m.pcs_id, ''),
                                         b.present_%s, b.pct_%s
                                  FROM tab_b b LEFT JOIN match_pcs m
                                       ON m.athlete_id = b.athlete_id
                                  WHERE b.sesso = ? AND b.birth_year BETWEEN ? AND ?"""
                               % (cella, cella), (sesso, lo, hi)).fetchall()
            dentro_p, fuori_p, dentro_a, fuori_a = [], [], [], []
            for by, pid, pres, pct in tutti:
                pro = any(cl in classi_base and s <= by + eta_base
                          for s, cl in squadre.get(pid, ()))
                if pres == 1 and pct is not None:
                    (dentro_p if pro else fuori_p).append(pct)
                else:
                    # Assente dalla classifica: sotto chiunque vi compaia.
                    (dentro_a if pro else fuori_a).append(-1.0)
            righe.append(riga("%s, solo chi e' in classifica" % etichetta,
                              dentro_p, fuori_p))
            righe.append(riga("%s, tutta la coorte con l'assenza sotto tutti" % etichetta,
                              dentro_p + dentro_a, fuori_p + fuori_a))
        ar.tabella("mancanti", righe,
                   colonne=["popolazione", "professionisti", "atleti", "% pro", "AUC"],
                   titolo="Chi non e' in classifica",
                   nota="l'assenza non e' un dato mancante da imputare: e' un rendimento "
                        "che non c'e' stato, e trattarla come tale alza l'AUC perche' "
                        "aggiunge un'informazione vera. Le due eta' rispondono alla stessa "
                        "domanda ai due estremi del percorso giovanile")

    # Quanto oscilla la capacita' discriminante fra le varianti: e' il numero che dice
    # se le conclusioni reggono. Si calcola rileggendo dall'archivio, cosi' usa
    # esattamente i valori che sono stati scritti e non una copia in memoria.
    with sqlite3.connect("output/risultati.db") as out:
        import json
        valori = []
        for chiave in ("definizione", "finestra"):
            r = out.execute("SELECT righe FROM tabella WHERE modulo='sensibilita' "
                            "AND chiave=?", (chiave,)).fetchone()
            valori += [x[4] for x in json.loads(r[0]) if x[4] is not None]
        out.execute("INSERT OR REPLACE INTO valore VALUES (?,?,?,?)",
                    ("sensibilita", "oscillazione_auc",
                     json.dumps(round(max(valori) - min(valori), 3)),
                     "differenza fra la piu' alta e la piu' bassa AUC fra le varianti "
                     "di definizione e di finestra"))
        for chiave in ("definizione", "finestra", "soglia", "mancanti"):
            r = out.execute("SELECT colonne, righe FROM tabella WHERE modulo='sensibilita'"
                            " AND chiave=?", (chiave,)).fetchone()
            print("\n%s:" % chiave)
            for x in json.loads(r[1]):
                print("   %-52s %4s eventi  AUC %s" % (x[0], x[1], x[4]))
    db.close()


if __name__ == "__main__":
    main()
