"""
Costruisce il dataset di analisi a partire dal DB ciclismo.info (data/giovanile/ciclismo.db).

Output: data/analisi/analisi.db
  - tab_a          formato lungo: atleta x stagione x categoria x anno di categoria (Sezione 5)
  - tab_b          formato largo: una riga per atleta (predittori; esiti da popolare dopo PCS)
  - anagrafica     anno di nascita stimato + affidabilita'
  - attrito        conteggi per coorte e categoria
  - match_pcs      scheletro della tabella di matching con ProCyclingStats
Chiave di re-identificazione (non anonima) in data/private/crosswalk_atleti.csv

Nessun valore mancante viene imputato (Sezione 5 della guida).
"""
import csv
import os
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from math import log1p

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import (CATEGORIE, DB_ANALISI, DB_GIOVANILE, DB_SCHEDE, LISTE_DISGIUNTE,
                           anonimizza, cfg, chiave_match, connect)

# Tutte le scelte stanno in config.toml. Qui si leggono, non si decidono.
STAGIONE_MAX = cfg("stagioni", "massima")
STAGIONI_ANOMALE = {int(k): v for k, v in cfg("stagioni", "anomale").items()}

# Per ordinare le stagioni di un atleta quando ne ha due nello stesso anno
# (una presenza fuori categoria e una regolare).
ORDINE_CAT = {"U15": 0, "U17": 1, "U19": 2, "U23": 3}


# --------------------------------------------------------------------------
# 1. Estrazione dei record annuali individuali
# --------------------------------------------------------------------------
def presenze_elite(src):
    """Stagioni nella classifica Elite italiana (lista 'promiscua'), per atleta.

    Quella lista era esclusa dalle celle U23 perche' mescola Elite di qualunque eta' con
    gli Under 23, e come denominatore non andava bene. Come segnale invece e' preziosa:
    dice chi ha continuato a correre in Italia dopo l'eta' da U23 senza diventare
    professionista, e permette di distinguere "ha smesso" da "corre a un livello piu'
    basso" senza dipendere da PCS.
    """
    per_atleta = defaultdict(set)
    for r in src.execute("""
            SELECT cp.id_atleta AS id, cp.anno AS anno
            FROM   classifiche_punti cp
            WHERE  cp.id_categoria = 1 AND cp.sotto_gruppo = 'promiscua'
              AND  cp.anno_corso IS NULL AND cp.mese IS NULL
              AND  cp.tipo_soggetto = 'individuale' AND cp.anno <= ?""", (STAGIONE_MAX,)):
        per_atleta[r["id"]].add(r["anno"])
    return per_atleta


def estrai_record(src):
    """Un record per (atleta, anno, categoria)."""
    rows = src.execute("""
        SELECT cp.id_record, cp.id_atleta, cp.id_squadra, cp.nome_squadra_raw,
               cat.slug, cp.anno, cp.anno_corso, cp.sotto_gruppo, cp.posizione, cp.punti,
               cp.vittorie, cp.piazz_2, cp.piazz_3, cp.piazz_4, cp.piazz_5, cp.url_origine
        FROM   classifiche_punti cp
        JOIN   categorie cat ON cat.id_categoria = cp.id_categoria
        WHERE  cp.tipo_soggetto = 'individuale'
          AND  cp.mese IS NULL
          AND  (cat.gruppo IN (1, 2) OR cp.sotto_gruppo = 'under23')
    """).fetchall()

    # indice delle presenze nelle liste "primo anno"
    in_primo = set()
    for r in rows:
        if "primo_anno" in r["url_origine"]:
            in_primo.add((r["id_atleta"], r["anno"], r["slug"]))

    out, scartati = [], defaultdict(int)
    visti = set()
    for r in rows:
        if r["anno"] > STAGIONE_MAX:
            scartati["stagione_non_conclusa"] += 1
            continue
        slug = r["slug"]
        cat, sesso, eta1 = CATEGORIE[slug]
        primo = (r["id_atleta"], r["anno"], slug) in in_primo
        disg = (slug in LISTE_DISGIUNTE
                and LISTE_DISGIUNTE[slug][0] <= r["anno"] <= LISTE_DISGIUNTE[slug][1])

        if disg:
            # liste disgiunte: una riga per atleta/anno, anno_corso dalla sorgente
            cat_year, cy_certo = r["anno_corso"], True
        else:
            # liste annidate: tengo solo la lista generale, deduco l'anno di corso
            if "primo_anno" in r["url_origine"]:
                scartati["riga_primo_anno_ridondante"] += 1
                continue
            if cat == "U23":
                cat_year, cy_certo = None, False   # ricavato dopo dall'anno di nascita
            else:
                cat_year, cy_certo = (1, True) if primo else (2, False)

        chiave = (r["id_atleta"], r["anno"], slug)
        if chiave in visti:
            scartati["duplicato_atleta_anno_categoria"] += 1
            continue
        visti.add(chiave)

        out.append(dict(
            id_atleta=r["id_atleta"], slug=slug, categoria=cat, sesso=sesso, eta_primo=eta1,
            season=r["anno"], cat_year=cat_year, cat_year_certo=cy_certo, in_primo=primo,
            posizione_src=r["posizione"], points_raw=float(r["punti"]),
            vittorie=r["vittorie"], piazz_2=r["piazz_2"], piazz_3=r["piazz_3"],
            piazz_4=r["piazz_4"], piazz_5=r["piazz_5"],
            id_squadra=r["id_squadra"], nome_squadra_raw=r["nome_squadra_raw"],
            url_origine=r["url_origine"],
        ))
    return out, scartati


# --------------------------------------------------------------------------
# 2. Anno di nascita: stima gerarchica per affidabilita'
# --------------------------------------------------------------------------
def stima_nascita(record):
    """
    Tier 1 (certo)   : anno di corso noto senza ambiguita'
                       - categorie a liste disgiunte (Esordienti M sempre, F dal 2022)
                       - presenza nella lista 'primo anno' di una categoria a liste annidate
    Tier 2 (presunto): lista generale senza presenza in 'primo anno' -> si assume 2o anno.
                       L'errore possibile e' 'era primo anno ma non compare nella classifica
                       primo anno', che sottostima l'anno di nascita di 1: per questo, in caso
                       di conflitto fra sole stime tier 2, si prende il massimo.
    """
    t1, t2 = defaultdict(set), defaultdict(set)
    for r in record:
        if r["categoria"] == "U23":
            continue                       # U23 non informa: 4 anni di corso indistinguibili
        stima = r["season"] - r["eta_primo"] - (r["cat_year"] - 1)
        (t1 if r["cat_year_certo"] else t2)[r["id_atleta"]].add(stima)

    ana = {}
    for a in set(t1) | set(t2):
        s1, s2 = t1.get(a, set()), t2.get(a, set())
        if len(s1) == 1:
            ana[a] = (next(iter(s1)), "certo", len(s1 | s2))
        elif len(s1) > 1:
            ana[a] = (max(s1), "conflitto_tier1", len(s1))
        elif len(s2) == 1:
            ana[a] = (next(iter(s2)), "presunto", 1)
        else:
            ana[a] = (max(s2), "presunto_conflitto", len(s2))
    return ana


# --------------------------------------------------------------------------
# 3. Percentili entro cella
# --------------------------------------------------------------------------
def _chiave_punti(r):
    return (-r["points_raw"],)


def _chiave_estesa(r):
    """Ordinamento lessicografico punti > vittorie > 2i > 3i > 4i > 5i.

    E' il criterio che la fonte usa per sciogliere i pari punti (verificato: la
    posizione pubblicata e' un ordinamento totale 1..n). Riproducendolo qui
    manteniamo l'informazione dello spareggio ma lasciamo a pari merito chi ha
    davvero lo stesso palmares, cosa che la posizione pubblicata non fa (in coda
    ordina in modo arbitrario atleti con record identico).
    """
    return (-r["points_raw"], -(r["vittorie"] or 0), -(r["piazz_2"] or 0),
            -(r["piazz_3"] or 0), -(r["piazz_4"] or 0), -(r["piazz_5"] or 0))


def _classifica(gruppo, key, chiave):
    """rank competition-style + percentile, come rank(..., ties.method='min') in R."""
    ordinati = sorted(gruppo, key=chiave)
    n = len(ordinati)
    pos, prec, prec_pos = {}, object(), 0
    for i, r in enumerate(ordinati, start=1):
        k = chiave(r)
        if k != prec:
            prec, prec_pos = k, i
        pos[id(r)] = prec_pos
    for r in ordinati:
        p = pos[id(r)]
        r[key + "_pos"] = p
        r[key + "_n"] = n
        r[key + "_pct"] = 100.0 * (1 - (p - 1) / n)
    if key == "cell":
        media = sum(log1p(r["points_raw"]) for r in ordinati) / n
        var = (sum((log1p(r["points_raw"]) - media) ** 2 for r in ordinati) / (n - 1)) if n > 1 else 0.0
        sd = var ** 0.5
        for r in ordinati:
            r["z_log_pts"] = (log1p(r["points_raw"]) - media) / sd if sd > 0 else 0.0
            r["top10"] = int(r["cell_pos"] <= 10)
            r["top25pct"] = int(r["cell_pct"] >= 75)


def normalizza(record):
    # cella principale: stagione x categoria x anno di categoria x sesso
    celle = defaultdict(list)
    for r in record:
        if r["cat_year"] is not None:
            celle[(r["season"], r["categoria"], r["cat_year"], r["sesso"])].append(r)
    for g in celle.values():
        _classifica(g, "cell", _chiave_punti)     # solo punti (versione della guida)
        _classifica(g, "ext", _chiave_estesa)     # punti + spareggi (raccomandata)
    # cella di ripiego: stagione x categoria x sesso (sempre calcolabile)
    celle2 = defaultdict(list)
    for r in record:
        if r["cat_year_conf"] != "fuori_categoria":
            celle2[(r["season"], r["categoria"], r["sesso"])].append(r)
    for g in celle2.values():
        _classifica(g, "cat", _chiave_punti)


# --------------------------------------------------------------------------
# 4. Schema di destinazione
# --------------------------------------------------------------------------
DDL = """
CREATE TABLE anagrafica (
    athlete_id      TEXT PRIMARY KEY,
    birth_year      INTEGER,
    birth_date      TEXT,      -- AAAA-MM-GG quando osservata; serve per il Relative Age Effect
    birth_quarter   INTEGER,   -- 1-4, trimestre di nascita
    birth_year_conf TEXT,      -- sorgente | scheda (osservate) ; certo | presunto |
                               -- conflitto_tier1 | presunto_conflitto | ignoto (inferite)
    n_stime         INTEGER,
    sesso           TEXT,
    regione         TEXT,      -- regione modale nelle stagioni giovanili
    n_regioni       INTEGER,
    prima_stagione  INTEGER,
    ultima_stagione INTEGER,
    n_stagioni      INTEGER,
    categorie       TEXT
);

CREATE TABLE tab_a (
    athlete_id     TEXT NOT NULL,
    birth_year     INTEGER,
    season         INTEGER NOT NULL,
    age            INTEGER,
    category       TEXT NOT NULL,        -- U15 U17 U19 U23
    cat_year       INTEGER,              -- 1..2 (U15/U17/U19), 1..4 (U23)
    cat_year_conf  TEXT,                 -- da_nascita_certa | da_lista_primo_anno | presunto
                                         -- | da_nascita_presunta | incoerente | ignoto
    sesso          TEXT,
    points_raw     REAL,
    rank_pos       INTEGER,              -- ricalcolato entro cella
    n_ranked       INTEGER,
    pct_rank       REAL,                 -- percentile su soli punti (versione della guida)
    rank_pos_ext   INTEGER,              -- rango con spareggio punti>vittorie>2i>3i>4i>5i
    pct_rank_ext   REAL,                 -- percentile raccomandato come predittore
    z_log_pts      REAL,
    top10          INTEGER,
    top25pct       INTEGER,
    rank_pos_cat   INTEGER,              -- entro stagione x categoria (tutti gli anni di corso)
    n_ranked_cat   INTEGER,
    pct_rank_cat   REAL,
    posizione_src  INTEGER,              -- posizione dichiarata dalla fonte
    vittorie       INTEGER,
    podi           INTEGER,
    top5           INTEGER,
    team_id        INTEGER,
    team_raw       TEXT,
    regione        TEXT,
    eta_coerente   INTEGER,              -- 0 = contraddizione non spiegata; NULL = non applicabile
    flag_stagione  TEXT,                 -- 'covid' per il 2020; NULL altrimenti
    url_origine    TEXT,
    PRIMARY KEY (athlete_id, season, category)
);
CREATE INDEX ix_tab_a_cella  ON tab_a(season, category, cat_year);
CREATE INDEX ix_tab_a_atleta ON tab_a(athlete_id);

CREATE TABLE qualita_dati (voce TEXT, valore TEXT);

CREATE TABLE attrito (
    sesso TEXT, birth_year INTEGER, categoria TEXT, n_atleti INTEGER
);

-- Scheletro del ponte ciclismo.info <-> ProCyclingStats (Sezione 5, Step 6).
CREATE TABLE match_pcs (
    athlete_id     TEXT PRIMARY KEY REFERENCES anagrafica(athlete_id),
    pcs_id         TEXT,          -- slug PCS, es. 'filippo-baroncini'
    metodo         TEXT,          -- esatto | fuzzy | manuale | assente
    score          REAL,          -- similarita' 0-1 per il fuzzy
    birth_year_pcs INTEGER,       -- anno di nascita da PCS (verifica incrociata)
    ambiguo        INTEGER DEFAULT 0,
    candidati      TEXT,          -- JSON dei candidati scartati, per l'audit
    verificato     INTEGER DEFAULT 0,
    nota           TEXT
);
CREATE INDEX ix_match_pcs_id ON match_pcs(pcs_id);
"""

CAMPI_B_PCT = ["U15y1", "U15y2", "U17y1", "U17y2", "U19y1", "U19y2",
               "U23y1", "U23y2", "U23y3", "U23y4"]


def crea_tab_b(dst):
    cols = []
    for c in CAMPI_B_PCT:
        cols.append("pct_%s REAL" % c)          # percentile esteso (raccomandato)
        cols.append("pctpt_%s REAL" % c)        # percentile su soli punti
        cols.append("present_%s INTEGER NOT NULL DEFAULT 0" % c)
    dst.execute("""
        CREATE TABLE tab_b (
            athlete_id TEXT PRIMARY KEY,
            birth_year INTEGER,
            birth_date TEXT,
            birth_quarter INTEGER,
            rel_age INTEGER,          -- giorni fra la nascita e il 31/12 di quell'anno
            birth_year_conf TEXT,
            sesso TEXT,
            regione TEXT,             -- regione modale su tutta la carriera (descrittiva)
            %s,
            best_pct_youth REAL,
            best_pct_cat TEXT,
            n_seasons_youth INTEGER,
            n_wins_youth INTEGER,
            slope_pct REAL,
            -- Contesto. Solo region_U15y1 e' ammissibile come controllo, perche' e' l'unica
            -- misurata prima del predittore. Le altre sono mediatori: usarle come oggetto
            -- di studio (STEP 14), mai come controlli nei modelli principali.
            prima_cella TEXT,         -- cella della prima stagione osservata, es. 'U15y1'
            region_first TEXT,        -- regione alla prima stagione osservata
            team_first TEXT,          -- societa' alla prima stagione osservata
            team_last_youth TEXT,     -- societa' nell'ultima stagione giovanile (<= U19)
            n_team_changes INTEGER,   -- cambi di societa' nelle categorie giovanili
            n_regions INTEGER,
            changed_region INTEGER,
            team_quality_first REAL,  -- tasso di pro della societa' di partenza, calcolato
            team_quality_n INTEGER,   -- SOLO sulle coorti precedenti: da popolare dopo PCS
            -- Continuita' agonistica dopo l'eta' giovanile, dalla classifica Elite italiana.
            -- Serve a distinguere chi ha smesso da chi corre a un livello piu' basso.
            elite_seasons_a_punti INTEGER,  -- stagioni in cui l'atleta e' andato A PUNTI nella
                                -- classifica Elite a 23 anni o piu'. Chi ha continuato
                                -- a correre senza mai fare punti e' indistinguibile
                                -- da chi ha smesso: e' un limite inferiore.
            last_racing_age INTEGER,  -- eta' dell'ultima presenza in una qualunque classifica
            punti_dopo_u23 INTEGER,   -- 1 se e' andato a punti in una classifica dopo i 22 anni
            -- esiti: da popolare dopo il matching con ProCyclingStats
            pcs_id TEXT, pcs_matched INTEGER,
            pcs_u19 INTEGER, pcs_u23 INTEGER,
            PRO INTEGER, tier INTEGER,
            year_turned_pro INTEGER, age_turned_pro INTEGER, pro_seasons INTEGER,
            best_pcs_rank INTEGER, censored INTEGER
        )""" % ", ".join(cols))


def decisioni_manuali(record, scartati):
    """Applica le risoluzioni scritte a mano in data/private/manual/ (vedi 02_casi_da_verificare.py).

    I due file contengono solo id numerici e motivazioni impersonali, ma un id resta un
    riferimento a una persona reale: stanno sotto data/private/ e non entrano in git.
    Sono la traccia di come sono stati risolti i casi ambigui, da conservare a parte.
    """
    fusioni, esclusi = {}, {}
    p = "data/private/manual/fusioni_atleti.csv"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("id_canonico"):
                    fusioni[int(r["id_atleta_src"])] = int(r["id_canonico"])
    p = "data/private/manual/esclusioni_atleti.csv"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                esclusi[int(r["id_atleta_src"])] = r.get("motivo", "")

    out, visti = [], {}
    for r in record:
        if r["id_atleta"] in esclusi:
            scartati["esclusi_a_mano"] += 1
            continue
        r["id_atleta"] = fusioni.get(r["id_atleta"], r["id_atleta"])
        chiave = (r["id_atleta"], r["season"], r["categoria"])
        if chiave in visti:
            # la fusione puo' creare due righe per la stessa cella: tengo la migliore
            scartati["doppioni_da_fusione"] += 1
            if r["points_raw"] > visti[chiave]["points_raw"]:
                out[out.index(visti[chiave])] = r
                visti[chiave] = r
            continue
        visti[chiave] = r
        out.append(r)
    return out, len(fusioni), len(esclusi)


def data_valida(birth_date):
    """La data esiste davvero? La fonte contiene qualche 29 febbraio di anni non bisestili."""
    if not birth_date:
        return False
    try:
        a, m, g = (int(x) for x in birth_date.split("-"))
        date(a, m, g)
        return True
    except (ValueError, AttributeError):
        return False


def eta_relativa(birth_date):
    """Giorni fra la nascita e il 31 dicembre di quell'anno, 0-364.

    E' l'eta' relativa entro la coorte: 364 per chi nasce il 1o gennaio, 0 per chi nasce
    il 31 dicembre. Piu' fine del trimestre e usabile come variabile continua, mentre il
    trimestre resta per il test del RAE, che in letteratura si fa per quartili.
    """
    if not data_valida(birth_date):
        return None
    a, m, g = (int(x) for x in birth_date.split("-"))
    return (date(a, 12, 31) - date(a, m, g)).days


def nascite_osservate(src):
    """Date di nascita osservate, non inferite, in ordine di preferenza.

    1. Le correzioni decise a mano, che vincono su tutto: nascono dal confronto fra
       ciclismo.info e ProCyclingStats, dove le due fonti divergono e si e' stabilito
       quale abbia ragione. Serve perche' nessuna delle due e' sistematicamente giusta:
       sul campione confrontato PCS ha ragione 5 volte su 7 e ciclismo.info 2.
    2. La sorgente stessa, se un giorno esporra' la nascita: si cerca una colonna
       plausibile in `atleti` e la si usa senza altre domande. E' la via giusta, e
       questa funzione esiste perche' il giorno in cui ci sara' il resto del codice
       non debba cambiare.
    3. Le schede personali scaricate da 03_scarica_schede.py.

    Restituisce {id_atleta: (birth_date | None, birth_year, fonte)}.
    """
    out = {}

    colonne = {r[1].lower() for r in src.execute("PRAGMA table_info(atleti)")}
    col_data = next((c for c in ("data_nascita", "birth_date", "nato_il") if c in colonne), None)
    col_anno = next((c for c in ("anno_nascita", "birth_year") if c in colonne), None)
    if col_data or col_anno:
        campi = ", ".join(x for x in (col_data, col_anno) if x)
        for r in src.execute("SELECT id_atleta, %s FROM atleti" % campi):
            d = r[col_data] if col_data else None
            a = r[col_anno] if col_anno else None
            if d and re.match(r"^\d{4}-\d{2}-\d{2}$", str(d)):
                out[r["id_atleta"]] = (str(d), int(str(d)[:4]), "sorgente")
            elif a:
                out[r["id_atleta"]] = (None, int(a), "sorgente")

    if os.path.exists(DB_SCHEDE):
        sc = sqlite3.connect(DB_SCHEDE)
        for i, bd, by in sc.execute("""SELECT id_atleta, birth_date, birth_year
                                       FROM scheda_atleta WHERE birth_year IS NOT NULL"""):
            if i not in out:                       # la sorgente ha la precedenza
                out[i] = (bd, by, "scheda")

    # Le correzioni manuali sovrascrivono qualunque fonte automatica.
    p = "data/private/manual/date_corrette.csv"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                d = (r.get("data_corretta") or "").strip()
                if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
                    out[int(r["id_atleta_src"])] = (d, int(d[:4]), "corretta_a_mano")
    return out


def rimappa_elite(elite):
    """Applica le stesse fusioni manuali alle presenze Elite."""
    fusioni = {}
    p = "data/private/manual/fusioni_atleti.csv"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("id_canonico"):
                    fusioni[int(r["id_atleta_src"])] = int(r["id_canonico"])
    out = defaultdict(set)
    for a, anni in elite.items():
        out[fusioni.get(a, a)] |= anni
    return out


def coerente(r, by):
    """L'eta' implicata dall'anno di nascita e' compatibile con l'anno di corso assegnato?

    NULL quando la domanda non si pone: anno di nascita ignoto, oppure presenza fuori
    categoria (cat_year nullo), che e' un caso spiegato e non una contraddizione.
    0 segnala invece una contraddizione non spiegata, quasi sempre un id_atleta che
    fonde o spezza due persone: va esclusa o controllata a mano, non corretta d'ufficio.
    """
    if by is None or r["cat_year"] is None:
        return None
    return int(r["season"] - by == r["eta_primo"] + r["cat_year"] - 1)


# --------------------------------------------------------------------------
# 5. Main
# --------------------------------------------------------------------------
def main():
    os.makedirs("data/analisi", exist_ok=True)
    os.makedirs("data/private", exist_ok=True)
    src = connect(DB_GIOVANILE)

    elite = presenze_elite(src)
    record, scartati = estrai_record(src)
    record, n_fusioni, n_esclusi = decisioni_manuali(record, scartati)
    elite = rimappa_elite(elite)

    # L'inferenza resta il ripiego; dove la nascita e' osservata, quella vince.
    ana = stima_nascita(record)
    osservate = nascite_osservate(src)
    date_nascita, smentite, date_non_valide = {}, [], []
    for a, (bd, by, fonte) in osservate.items():
        inferita = ana.get(a)
        if inferita and inferita[1] != "ignoto" and inferita[0] != by:
            smentite.append((a, inferita[0], by, inferita[1]))
        ana[a] = (by, fonte, 1)
        if bd and not data_valida(bd):
            date_non_valide.append((a, bd))
            bd = None                       # l'anno resta buono, il giorno no
        date_nascita[a] = bd

    # Anno di corso definitivo.
    #
    # Dove l'anno di nascita e' attendibile lo si ricava da li', perche' e' piu' affidabile
    # dell'appartenenza alla lista 'primo anno', che sottostima i primi anni (chi non fa
    # punti nelle gare di primo anno finisce nella sola lista generale e verrebbe letto
    # come secondo anno). Per l'U23 e' l'unica via: la fonte non pubblica i quattro anni.
    #
    # Attendibile = osservata (scheda o sorgente) oppure inferita di livello 1. Le prime
    # due non sono in discussione; per la terza la deduzione non e' circolare, perche' il
    # livello 1 viene da Esordienti a liste disgiunte o da una presenza in 'primo anno'.
    ATTENDIBILI = ("sorgente", "scheda", "certo")
    for r in record:
        by, conf = ana.get(r["id_atleta"], (None, "ignoto"))[:2]
        cy_nascita = (r["season"] - by - r["eta_primo"] + 1) if by is not None else None
        limite = 4 if r["categoria"] == "U23" else 2

        # Presenza fuori dalla fascia d'eta' della categoria: e' legittima, non un errore.
        # Un Under 23 al primo anno puo' correre alcune gare Juniores e comparire quindi
        # nel ranking Juniores a 19 anni. Quella stagione pero' non appartiene alla
        # popolazione in studio per quella categoria: la riga resta in tab_a come
        # documentazione, con cat_year nullo, e non entra in nessuna cella.
        fuori = cy_nascita is not None and not (1 <= cy_nascita <= limite)

        if fuori and (conf in ATTENDIBILI or r["categoria"] == "U23"):
            r["cat_year"], r["cat_year_conf"] = None, "fuori_categoria"
        elif cy_nascita is not None and not fuori and conf in ATTENDIBILI:
            r["cat_year"] = cy_nascita
            r["cat_year_conf"] = "da_nascita" if conf in ("sorgente", "scheda") \
                else "da_nascita_certa"
        elif r["categoria"] == "U23":
            if cy_nascita is None:
                r["cat_year_conf"] = "ignoto"
            else:
                r["cat_year"], r["cat_year_conf"] = cy_nascita, "da_nascita_presunta"
        elif r["cat_year_certo"]:
            r["cat_year_conf"] = "da_lista_primo_anno"
        else:
            r["cat_year_conf"] = "presunto"

    normalizza(record)

    nome_squadra = {r["id_squadra"]: r["nome_societa"]
                    for r in src.execute("SELECT id_squadra, nome_societa FROM squadre")}
    regioni = defaultdict(lambda: defaultdict(int))
    reg_anno = {}
    for r in src.execute("SELECT id_atleta, anno, regione FROM atleti_regioni"):
        regioni[r["id_atleta"]][r["regione"]] += 1
        reg_anno.setdefault((r["id_atleta"], r["anno"]), r["regione"])

    if os.path.exists(DB_ANALISI):
        os.remove(DB_ANALISI)
    dst = sqlite3.connect(DB_ANALISI)
    dst.executescript(DDL)
    crea_tab_b(dst)

    per_atleta = defaultdict(list)
    for r in record:
        per_atleta[r["id_atleta"]].append(r)
    nomi = {r["id_atleta"]: (r["nome_completo"], r["nome"], r["cognome"])
            for r in src.execute("SELECT id_atleta, nome_completo, nome, cognome FROM atleti")}

    # --- anagrafica + crosswalk ---
    ana_rows, cross = [], []
    for a, rs in per_atleta.items():
        by, conf, ns = ana.get(a, (None, "ignoto", 0))
        rg = regioni.get(a)
        reg = max(rg.items(), key=lambda kv: kv[1])[0] if rg else None
        aid = anonimizza(a)
        stagioni = sorted({r["season"] for r in rs})
        cats = sorted({r["categoria"] for r in rs})
        bd = date_nascita.get(a)
        ana_rows.append((aid, by, bd, (int(bd[5:7]) - 1) // 3 + 1 if bd else None,
                         conf, ns, rs[0]["sesso"], reg, len(rg) if rg else 0,
                         stagioni[0], stagioni[-1], len(stagioni), ",".join(cats)))
        nc, nm, cg = nomi.get(a, ("", "", ""))
        cross.append((aid, a, nc, nm, cg, chiave_match(nm or "", cg or ""),
                      by, date_nascita.get(a), conf, reg))
    dst.executemany("INSERT INTO anagrafica VALUES (%s)" % ",".join("?" * 13), ana_rows)

    # --- tab_a ---
    ta = []
    for r in record:
        aid = anonimizza(r["id_atleta"])
        by = ana.get(r["id_atleta"], (None,))[0]
        podi = sum(x or 0 for x in (r["vittorie"], r["piazz_2"], r["piazz_3"]))
        top5 = podi + sum(x or 0 for x in (r["piazz_4"], r["piazz_5"]))
        ta.append((aid, by, r["season"], (r["season"] - by) if by else None,
                   r["categoria"], r["cat_year"], r["cat_year_conf"], r["sesso"],
                   r["points_raw"], r.get("cell_pos"), r.get("cell_n"), r.get("cell_pct"),
                   r.get("ext_pos"), r.get("ext_pct"), r.get("z_log_pts"), r.get("top10"), r.get("top25pct"),
                   r.get("cat_pos"), r.get("cat_n"), r.get("cat_pct"), r["posizione_src"],
                   r["vittorie"], podi, top5, r["id_squadra"], r["nome_squadra_raw"],
                   reg_anno.get((r["id_atleta"], r["season"])), coerente(r, by),
                   STAGIONI_ANOMALE.get(r["season"]), r["url_origine"]))
    dst.executemany("INSERT INTO tab_a VALUES (%s)" % ",".join("?" * 30), ta)

    # --- tab_b ---
    b_cols = ["athlete_id", "birth_year", "birth_date", "birth_quarter", "rel_age",
              "birth_year_conf", "sesso", "regione",
              "prima_cella", "region_first", "team_first", "team_last_youth",
              "n_team_changes", "n_regions", "changed_region"]
    for c in CAMPI_B_PCT:
        b_cols += ["pct_%s" % c, "pctpt_%s" % c, "present_%s" % c]
    b_cols += ["best_pct_youth", "best_pct_cat", "n_seasons_youth", "n_wins_youth", "slope_pct",
               "elite_seasons_a_punti", "last_racing_age", "punti_dopo_u23"]
    b_rows = []
    for a, rs in per_atleta.items():
        aid = anonimizza(a)
        by, conf, _ = ana.get(a, (None, "ignoto", 0))
        rg = regioni.get(a)
        reg = max(rg.items(), key=lambda kv: kv[1])[0] if rg else None
        cellmap = {"%sy%d" % (r["categoria"], r["cat_year"]): r for r in rs if r["cat_year"]}
        bd = date_nascita.get(a)

        # --- contesto: si guarda alla sequenza delle stagioni, non alle celle ---
        ordinate = sorted((r for r in rs if r["cat_year"]),
                          key=lambda r: (r["season"], ORDINE_CAT[r["categoria"]]))
        giovanili = [r for r in ordinate if r["categoria"] != "U23"]
        primo = ordinate[0] if ordinate else None
        squadre_gio = [r["id_squadra"] for r in giovanili if r["id_squadra"]]
        regioni_gio = [reg_anno.get((a, r["season"])) for r in giovanili]
        regioni_gio = [x for x in regioni_gio if x]

        vals = [aid, by, bd, (int(bd[5:7]) - 1) // 3 + 1 if bd else None,
                eta_relativa(bd), conf, rs[0]["sesso"], reg,
                "%sy%d" % (primo["categoria"], primo["cat_year"]) if primo else None,
                reg_anno.get((a, primo["season"])) if primo else None,
                nome_squadra.get(primo["id_squadra"]) if primo else None,
                nome_squadra.get(giovanili[-1]["id_squadra"]) if giovanili else None,
                # cambi consecutivi: due stagioni nella stessa societa' non sono un cambio
                sum(1 for x, y in zip(squadre_gio, squadre_gio[1:]) if x != y),
                len(set(regioni_gio)),
                int(len(set(regioni_gio)) > 1) if regioni_gio else None]
        for c in CAMPI_B_PCT:
            r = cellmap.get(c)
            vals += [r["ext_pct"] if r else None,
                     r["cell_pct"] if r else None, 1 if r else 0]
        pcts = {c: cellmap[c]["ext_pct"] for c in CAMPI_B_PCT if c in cellmap}
        best_c = max(pcts, key=pcts.get) if pcts else None
        # pendenza OLS del percentile sull'eta' (serve almeno 3 stagioni con eta' nota)
        slope = None
        if by is not None and len(pcts) >= 3:
            pts = [(cellmap[c]["season"] - by, pcts[c]) for c in pcts]
            mx = sum(p[0] for p in pts) / len(pts)
            my = sum(p[1] for p in pts) / len(pts)
            den = sum((p[0] - mx) ** 2 for p in pts)
            if den > 0:
                slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / den
        anni_elite = elite.get(a, set())
        eta_elite = {y - by for y in anni_elite} if by is not None else set()
        tutte = {r["season"] for r in rs} | anni_elite
        vals += [max(pcts.values()) if pcts else None, best_c,
                 len({r["season"] for r in rs}),
                 sum(r["vittorie"] or 0 for r in rs), slope,
                 sum(1 for e in eta_elite if e >= 23) if by is not None else None,
                 (max(tutte) - by) if by is not None else None,
                 int(max(tutte) - by > 22) if by is not None else None]
        b_rows.append(vals)
    dst.executemany("INSERT INTO tab_b (%s) VALUES (%s)"
                    % (",".join(b_cols), ",".join("?" * len(b_cols))), b_rows)

    dst.execute("""INSERT INTO attrito
        SELECT sesso, birth_year, category, COUNT(DISTINCT athlete_id)
        FROM tab_a WHERE birth_year IS NOT NULL GROUP BY 1,2,3""")

    # --- diagnostica ---
    qd = [("record_estratti", len(record)),
          ("fusioni_applicate", n_fusioni),
          ("esclusioni_applicate", n_esclusi),
          ("atleti", len(per_atleta)),
          ("righe_tab_a", len(ta)),
          ("righe_tab_b", len(b_rows))]
    qd += [("scartati__%s" % k, v) for k, v in sorted(scartati.items())]
    qd.append(("righe_eta_incoerente",
               dst.execute("SELECT COUNT(*) FROM tab_a WHERE eta_coerente = 0").fetchone()[0]))
    qd.append(("righe_fuori_categoria",
               dst.execute("SELECT COUNT(*) FROM tab_a WHERE cat_year_conf='fuori_categoria'")
               .fetchone()[0]))
    qd.append(("atleti_eta_incoerente",
               dst.execute("SELECT COUNT(DISTINCT athlete_id) FROM tab_a "
                           "WHERE eta_coerente = 0").fetchone()[0]))
    qd.append(("nascita_osservata", len(osservate)))
    qd.append(("nascita_con_data_completa", sum(1 for v in date_nascita.values() if v)))
    qd.append(("nascita_inferenza_smentita", len(smentite)))
    qd.append(("nascita_data_non_valida", len(date_non_valide)))
    for conf in ("sorgente", "scheda", "corretta_a_mano", "certo", "presunto",
                 "conflitto_tier1", "presunto_conflitto"):
        qd.append(("nascita__%s" % conf, sum(1 for v in ana.values() if v[1] == conf)))
    qd.append(("nascita__ignoto", sum(1 for a in per_atleta if a not in ana)))
    dst.executemany("INSERT INTO qualita_dati VALUES (?,?)", [(k, str(v)) for k, v in qd])

    dst.commit()

    with open("data/private/crosswalk_atleti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["athlete_id", "id_atleta_src", "nome_completo", "nome", "cognome",
                    "chiave_match", "birth_year", "birth_date", "birth_year_conf",
                    "regione"])
        w.writerows(sorted(cross, key=lambda r: r[2]))

    print("OK  %s" % DB_ANALISI)
    for k, v in qd:
        print("    %-38s %s" % (k, v))
    print("    %-38s %s" % ("crosswalk (NON anonimo)", "data/private/crosswalk_atleti.csv"))


if __name__ == "__main__":
    main()
