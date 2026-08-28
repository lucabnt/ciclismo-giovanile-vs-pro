"""
Scarica da ProCyclingStats gli esiti di carriera: chi e' diventato professionista e a
che livello e' arrivato.

L'IDEA
    Non si cercano i 12.357 ragazzi uno per uno su PCS: la stragrande maggioranza non ha
    mai corso una gara registrata, e chi non e' mai stato professionista contribuisce con
    PRO = 0, che e' gia' il default. Si costruisce invece l'insieme piccolo e
    completamente enumerabile degli atleti RILEVANTI, e lo si proietta sui giovanili.
    Il match diventa qualche centinaio di confronti invece di dodicimila.

I QUATTRO STRATI
    A  rose WorldTeam e ProTeam, stagione per stagione   -> definisce PRO
       (con --continental anche le Continental: distingue chi corre a livello piu' basso)
    B  classifica annuale globale, top 500               -> definisce tier (top 100/500)
    C  classifica annuale filtrata sugli italiani        -> predittore internazionale U19/U23
    D  profili dei candidati emersi da A e C             -> data di nascita, storia squadre

    Nota sulla continuita' agonistica: teams_history() nello strato D restituisce TUTTE
    le stagioni con la classe della squadra, Continental e inferiori comprese. Per gli
    atleti gia' candidati, quindi, "ha corso Continental" si sa senza enumerare le
    squadre CT. L'opzione --continental serve solo a chiudere il caso di chi ha corso
    Continental senza mai fare punti PCS e senza mai passare da WT o PRT.
    Chi ha continuato a correre in Italia da Elite si legge invece da ciclismo.info,
    senza alcuna richiesta: vedi tab_b.elite_seasons e tab_b.racing_after_u23.

    Si eseguono in ordine: ognuno restringe il successivo. Gli strati A e B bastano per
    lo STEP 4, il conteggio degli eventi che decide se la Domanda B e' modellabile.

COME SI USA

    pip install procyclingstats cloudscraper

    python scripts/04_scarica_pcs.py --stato
    python scripts/04_scarica_pcs.py --strati AB     # il minimo per lo STEP 4, ~30 min
    python scripts/04_scarica_pcs.py --strati CD     # il resto, qualche ora
    python scripts/04_scarica_pcs.py --strati A --continental   # aggiunge le Continental
    python scripts/04_scarica_pcs.py                 # tutto

    Ripartibile e interrompibile con Ctrl+C, come 03_scarica_schede.py.

PERCHE' cloudscraper
    PCS sta dietro Cloudflare. La libreria lo supera se cloudscraper e' installato,
    altrimenti puo' rispondere 403. Il robots.txt di PCS consente `User-agent: *` su
    tutto il sito: i divieti riguardano i crawler di addestramento dei modelli, non
    l'uso statistico. La libreria pero' non ha alcuna pausa fra le richieste: la
    mettiamo qui, 2,5 secondi, che su ~2.500 pagine e' un paio d'ore e non pesa sul sito.
"""
import argparse
import os
import re
import sqlite3
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_giovanile import chiave_match

DB_PCS = "data/pcs/pcs.db"
PAUSA = 2.5

# Prima stagione utile: il nato nel 1996 (coorte piu' vecchia dell'analisi principale)
# poteva firmare da neoprofessionista nel 2015. Si parte dal 2011 per coprire con
# margine le estensioni dall'U17, che arrivano alla coorte 1992.
STAGIONI_PRO = range(2011, 2027)
STAGIONI_RANK = range(2007, 2026)
LIVELLI = {"worldtour": "WT", "proteams": "PRT"}
# Le Continental servono a distinguere chi ha smesso da chi corre a un livello piu'
# basso. Sono ~200 squadre per stagione in tutto il mondo, quindi l'enumerazione
# completa costa ore: si abilita con --continental. Per i soli atleti gia' candidati
# non serve, perche' Rider.teams_history() restituisce gia' tutte le classi.
LIVELLI_EXTRA = {"continental": "CT"}
TOP_N = 500                     # profondita' della classifica globale (5 pagine)

DDL = """
CREATE TABLE IF NOT EXISTS pcs_team (
    season INTEGER, team_slug TEXT, team_name TEXT, team_class TEXT,
    PRIMARY KEY (season, team_slug));

CREATE TABLE IF NOT EXISTS pcs_roster (
    season INTEGER, team_slug TEXT, pcs_id TEXT, rider_name TEXT, nazionalita TEXT,
    PRIMARY KEY (season, team_slug, pcs_id));
CREATE INDEX IF NOT EXISTS ix_roster_rider ON pcs_roster(pcs_id);

CREATE TABLE IF NOT EXISTS pcs_ranking (
    season INTEGER, pcs_id TEXT, fonte TEXT,   -- 'globale' | 'italia'
    rank_pos INTEGER, points REAL, rider_name TEXT, nazionalita TEXT,
    PRIMARY KEY (season, pcs_id, fonte));
CREATE INDEX IF NOT EXISTS ix_ranking_rider ON pcs_ranking(pcs_id);

CREATE TABLE IF NOT EXISTS pcs_rider (
    pcs_id TEXT PRIMARY KEY, nome TEXT, cognome TEXT, chiave_match TEXT,
    nazionalita TEXT, birthdate TEXT, birth_year INTEGER, scaricato_il TIMESTAMP);
CREATE INDEX IF NOT EXISTS ix_rider_chiave ON pcs_rider(chiave_match, birth_year);

CREATE TABLE IF NOT EXISTS pcs_rider_team (
    pcs_id TEXT, season INTEGER, team_name TEXT, team_class TEXT,
    PRIMARY KEY (pcs_id, season, team_name));

CREATE TABLE IF NOT EXISTS pcs_rider_points (
    pcs_id TEXT, season INTEGER, points REAL, rank_pos INTEGER,
    PRIMARY KEY (pcs_id, season));

CREATE TABLE IF NOT EXISTS pcs_log (
    url TEXT, esito TEXT, n_righe INTEGER, dettaglio TEXT,
    eseguito_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
"""


def dice(*a):
    print(*a)
    sys.stdout.flush()


def durata(sec):
    if sec < 90:
        return "%d s" % sec
    if sec < 5400:
        return "%d min" % round(sec / 60)
    return "%.1f ore" % (sec / 3600)


def carica_libreria():
    try:
        import procyclingstats
    except ImportError:
        sys.exit("Manca la libreria. Installa con:\n    pip install procyclingstats cloudscraper")
    try:
        import cloudscraper       # noqa: F401
    except ImportError:
        dice("ATTENZIONE: cloudscraper non installato. PCS sta dietro Cloudflare e le")
        dice("richieste possono tornare 403. Installa con: pip install cloudscraper\n")
    return procyclingstats


def nome_cognome(intero):
    """PCS scrive 'Cognome Nome' con il cognome in maiuscolo nelle tabelle."""
    if not intero:
        return None, None
    tok = intero.split()
    cog = [t for t in tok if t.isupper() and len(t) > 1]
    nom = [t for t in tok if t not in cog]
    if not cog or not nom:                 # niente maiuscole: si assume 'Cognome Nome'
        return (" ".join(tok[1:]) or None), tok[0]
    return " ".join(nom), " ".join(cog)


def slug(url):
    """'rider/tadej-pogacar' -> 'tadej-pogacar'."""
    if not url:
        return None
    return url.rstrip("/").split("/")[-1]


class Fonte:
    """Sessione con pausa e registro. La libreria non mette pause: le mettiamo qui."""

    def __init__(self, pcs, db, pausa):
        self.pcs, self.db, self.pausa = pcs, db, pausa
        self.ultimo = 0.0
        self.n = 0

    def _attendi(self):
        d = self.pausa - (time.time() - self.ultimo)
        if d > 0:
            time.sleep(d)
        self.ultimo = time.time()
        self.n += 1

    def scraper(self, classe, url):
        self._attendi()
        try:
            ogg = getattr(self.pcs, classe)(url)
            self.db.execute("INSERT INTO pcs_log (url, esito) VALUES (?,'ok')", (url,))
            return ogg
        except Exception as e:
            self.db.execute("INSERT INTO pcs_log (url, esito, dettaglio) VALUES (?,'errore',?)",
                            (url, str(e)[:300]))
            return None

    def html(self, url):
        """Per le pagine che la libreria non copre, riusando la sua sessione."""
        self._attendi()
        try:
            testo = self.pcs.Scraper._get_session().get(
                url if url.startswith("http") else "https://www.procyclingstats.com/" + url,
                timeout=30).text
            self.db.execute("INSERT INTO pcs_log (url, esito) VALUES (?,'ok')", (url,))
            return testo
        except Exception as e:
            self.db.execute("INSERT INTO pcs_log (url, esito, dettaglio) VALUES (?,'errore',?)",
                            (url, str(e)[:300]))
            return ""


# --------------------------------------------------------------------------
def strato_a(f, db, con_continental=False):
    """Rose WorldTeam e ProTeam: e' l'elenco esaustivo di chi e' stato professionista.

    Per squadra e non per atleta: una rosa costa una richiesta e restituisce 25-30 nomi,
    un profilo ne costa una e ne restituisce uno. E soprattutto e' esaustivo, non
    dipende dall'aver gia' indovinato chi cercare.
    """
    livelli = dict(LIVELLI)
    if con_continental:
        livelli.update(LIVELLI_EXTRA)
    fatte = {(r[0], r[1]) for r in db.execute("SELECT season, team_slug FROM pcs_team")}
    dice("STRATO A — rose %s, %d-%d"
         % ("/".join(livelli.values()), STAGIONI_PRO[0], STAGIONI_PRO[-1]))
    nuove = 0
    for season in STAGIONI_PRO:
        for liv, sigla in livelli.items():
            url = "teams.php?year=%d&filter=Filter&s=%s" % (season, liv)
            body = f.html(url)
            slugs = sorted(set(re.findall(r'href="(team/[a-z0-9\-]+-%d)"' % season, body)))
            if not slugs:
                dice("   %d %-10s nessuna squadra trovata (struttura della pagina cambiata?)"
                     % (season, sigla))
                continue
            for u in slugs:
                ts = slug(u)
                if (season, ts) in fatte:
                    continue
                t = f.scraper("Team", u)
                if t is None:
                    continue
                try:
                    nome, riders = t.name(), t.riders()
                except Exception:
                    nome, riders = None, []
                db.execute("INSERT OR REPLACE INTO pcs_team VALUES (?,?,?,?)",
                           (season, ts, nome, sigla))
                for r in riders:
                    db.execute("INSERT OR REPLACE INTO pcs_roster VALUES (?,?,?,?,?)",
                               (season, ts, slug(r.get("rider_url")),
                                r.get("rider_name"), r.get("nationality")))
                nuove += 1
            db.commit()
            dice("   %d %-10s %2d squadre" % (season, sigla, len(slugs)))
    dice("   nuove squadre scaricate: %d\n" % nuove)


def strato_b(f, db):
    """Classifica annuale globale, top 500. Da qui escono le soglie del tier.

    La posizione va letta dalla classifica NON filtrata: se si filtra per nazione, il
    rango che PCS mostra e' quello dentro il filtro, e 'top 100 italiano' non e'
    'top 100'. E' l'errore piu' facile da fare in tutto lo studio.
    """
    dice("STRATO B — classifica annuale globale, top %d" % TOP_N)
    for season in STAGIONI_PRO:
        if db.execute("""SELECT COUNT(*) FROM pcs_ranking WHERE season=? AND fonte='globale'""",
                      (season,)).fetchone()[0] >= TOP_N * 0.9:
            continue
        n = 0
        for offset in range(0, TOP_N, 100):
            url = ("rankings.php?date=%d-12-31&nation=&page=smallerorequal&offset=%d"
                   "&filter=Filter&p=me&s=season-individual" % (season, offset))
            rk = f.scraper("Ranking", url)
            if rk is None:
                break
            try:
                righe = rk.individual_ranking()
            except Exception:
                righe = []
            for r in righe:
                db.execute("INSERT OR REPLACE INTO pcs_ranking VALUES (?,?,'globale',?,?,?,?)",
                           (season, slug(r.get("rider_url")), r.get("rank"), r.get("points"),
                            r.get("rider_name"), r.get("nationality")))
            n += len(righe)
            if len(righe) < 100:
                break
        db.commit()
        dice("   %d  %3d posizioni" % (season, n))
    dice("")


def strato_c(f, db):
    """Classifica annuale filtrata sugli italiani: predittore internazionale U19/U23.

    Attenzione: chi ha corso senza mai fare punti PCS non compare. pcs_present = 0
    significa 'senza punti PCS', non 'non ha corso'.
    """
    dice("STRATO C — italiani a punti, %d-%d" % (STAGIONI_RANK[0], STAGIONI_RANK[-1]))
    for season in STAGIONI_RANK:
        if db.execute("SELECT COUNT(*) FROM pcs_ranking WHERE season=? AND fonte='italia'",
                      (season,)).fetchone()[0]:
            continue
        n, offset = 0, 0
        while offset < 2000:
            url = ("rankings.php?date=%d-12-31&nation=it&page=smallerorequal&offset=%d"
                   "&filter=Filter&p=me&s=season-individual" % (season, offset))
            rk = f.scraper("Ranking", url)
            if rk is None:
                break
            try:
                righe = rk.individual_ranking()
            except Exception:
                righe = []
            for r in righe:
                db.execute("INSERT OR REPLACE INTO pcs_ranking VALUES (?,?,'italia',?,?,?,?)",
                           (season, slug(r.get("rider_url")), r.get("rank"), r.get("points"),
                            r.get("rider_name"), r.get("nationality")))
            n += len(righe)
            if len(righe) < 100:
                break
            offset += 100
        db.commit()
        dice("   %d  %4d italiani a punti" % (season, n))
    dice("")


def candidati(db):
    """Chi vale la pena profilare: italiani emersi dagli strati A e C."""
    ids = {r[0] for r in db.execute(
        "SELECT pcs_id FROM pcs_roster WHERE nazionalita='IT' AND pcs_id IS NOT NULL")}
    ids |= {r[0] for r in db.execute(
        "SELECT pcs_id FROM pcs_ranking WHERE fonte='italia' AND pcs_id IS NOT NULL")}
    return ids


def strato_d(f, db, limite):
    """Profili: data di nascita, storia squadre con la classe, punti e rango per stagione.

    Rider.teams_history() da' in una sola richiesta tutte le stagioni con la classe della
    squadra, che e' esattamente la definizione operativa di PRO.
    """
    ids = candidati(db)
    gia = {r[0] for r in db.execute("SELECT pcs_id FROM pcs_rider")}
    da_fare = sorted(ids - gia)
    if limite:
        da_fare = da_fare[:limite]
    dice("STRATO D — profili: %d candidati, %d gia' presi, %d da scaricare (circa %s)"
         % (len(ids), len(ids & gia), len(da_fare), durata(len(da_fare) * f.pausa)))

    for k, pid in enumerate(da_fare, 1):
        r = f.scraper("Rider", "rider/%s" % pid)
        if r is None:
            continue
        try:
            bd = r.birthdate()
            naz = r.nationality()
            nome_completo = r.name()
        except Exception:
            bd, naz, nome_completo = None, None, None
        nom, cog = nome_cognome(nome_completo)
        db.execute("""INSERT OR REPLACE INTO pcs_rider
                      VALUES (?,?,?,?,?,?,?,CURRENT_TIMESTAMP)""",
                   (pid, nom, cog, chiave_match(nom or "", cog or ""), naz, bd,
                    int(bd[:4]) if bd and re.match(r"^\d{4}", str(bd)) else None))
        try:
            for t in r.teams_history():
                db.execute("INSERT OR REPLACE INTO pcs_rider_team VALUES (?,?,?,?)",
                           (pid, t.get("season"), t.get("team_name"), t.get("class")))
        except Exception:
            pass
        try:
            for p in r.points_per_season_history():
                db.execute("INSERT OR REPLACE INTO pcs_rider_points VALUES (?,?,?,?)",
                           (pid, p.get("season"), p.get("points"), p.get("rank")))
        except Exception:
            pass
        if k % 25 == 0:
            db.commit()
            dice("   %5d/%d" % (k, len(da_fare)))
    db.commit()
    dice("")


# --------------------------------------------------------------------------
def stato(db):
    def n(q, *a):
        return db.execute(q, a).fetchone()[0]

    dice("STRATO A — rose")
    dice("   squadre %d | righe di rosa %d | atleti distinti %d | italiani %d"
         % (n("SELECT COUNT(*) FROM pcs_team"), n("SELECT COUNT(*) FROM pcs_roster"),
            n("SELECT COUNT(DISTINCT pcs_id) FROM pcs_roster"),
            n("SELECT COUNT(DISTINCT pcs_id) FROM pcs_roster WHERE nazionalita='IT'")))
    dice("STRATO B — classifica globale")
    dice("   stagioni %d | righe %d"
         % (n("SELECT COUNT(DISTINCT season) FROM pcs_ranking WHERE fonte='globale'"),
            n("SELECT COUNT(*) FROM pcs_ranking WHERE fonte='globale'")))
    dice("STRATO C — italiani a punti")
    dice("   stagioni %d | righe %d | atleti distinti %d"
         % (n("SELECT COUNT(DISTINCT season) FROM pcs_ranking WHERE fonte='italia'"),
            n("SELECT COUNT(*) FROM pcs_ranking WHERE fonte='italia'"),
            n("SELECT COUNT(DISTINCT pcs_id) FROM pcs_ranking WHERE fonte='italia'")))
    dice("STRATO D — profili")
    dice("   scaricati %d | con data di nascita %d"
         % (n("SELECT COUNT(*) FROM pcs_rider"),
            n("SELECT COUNT(*) FROM pcs_rider WHERE birthdate IS NOT NULL")))

    # --- scala di uscita: distingue chi ha smesso da chi corre a un livello piu' basso ---
    if n("SELECT COUNT(*) FROM pcs_rider_team"):
        dice("")
        dice("SCALA DI USCITA (italiani profilati, per classe massima raggiunta)")
        for classe, etichetta in (("WT", "WorldTeam"), ("PRT", "ProTeam"),
                                  ("CT", "Continental")):
            dice("   %-12s %4d" % (etichetta, n("""
                SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_rider r
                JOIN pcs_rider_team t ON t.pcs_id = r.pcs_id
                WHERE r.nazionalita='IT' AND t.team_class = ?""", classe)))
        dice("   altre classi %4d" % n("""
            SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_rider r
            JOIN pcs_rider_team t ON t.pcs_id = r.pcs_id
            WHERE r.nazionalita='IT' AND t.team_class NOT IN ('WT','PRT','CT')"""))
        dice("")
        dice("Chi non compare affatto qui non ha necessariamente smesso: la continuita'")
        dice("   agonistica in Italia si legge da tab_b.elite_seasons e racing_after_u23,")
        dice("   che vengono dalla classifica Elite di ciclismo.info e non costano richieste.")

    err = n("SELECT COUNT(*) FROM pcs_log WHERE esito='errore'")
    if err:
        dice("\n   %d richieste fallite; le ultime:" % err)
        for r in db.execute("""SELECT url, dettaglio FROM pcs_log WHERE esito='errore'
                               ORDER BY eseguito_il DESC LIMIT 3"""):
            dice("     %s\n       %s" % (r[0][:80], (r[1] or "")[:90]))

    # --- STEP 4: il conteggio che decide se la Domanda B e' modellabile ---
    if n("SELECT COUNT(*) FROM pcs_team") and n("SELECT COUNT(*) FROM pcs_rider"):
        dice("\nSTEP 4 — eventi per coorte di nascita (italiani)")
        dice("   %-12s %6s %8s %9s %9s" % ("coorte", "pro", "top 500", "top 100", "cumulato"))
        tot = [0, 0, 0]
        for anno in range(1992, 2002):
            pro = n("""SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_rider r
                       JOIN pcs_rider_team t ON t.pcs_id=r.pcs_id
                       WHERE r.nazionalita='IT' AND r.birth_year=?
                         AND t.team_class IN ('WT','PRT') AND t.season <= r.birth_year+25""",
                    anno)
            t500 = n("""SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_rider r
                        JOIN pcs_rider_points p ON p.pcs_id=r.pcs_id
                        WHERE r.nazionalita='IT' AND r.birth_year=?
                          AND p.rank_pos <= 500 AND p.season <= r.birth_year+26""", anno)
            t100 = n("""SELECT COUNT(DISTINCT r.pcs_id) FROM pcs_rider r
                        JOIN pcs_rider_points p ON p.pcs_id=r.pcs_id
                        WHERE r.nazionalita='IT' AND r.birth_year=?
                          AND p.rank_pos <= 100 AND p.season <= r.birth_year+26""", anno)
            if anno >= 1996:
                tot = [tot[0] + pro, tot[1] + t500, tot[2] + t100]
            dice("   %-12d %6d %8d %9d" % (anno, pro, t500, t100))
        dice("   %-12s %6d %8d %9d   <- coorti dell'analisi principale"
             % ("1996-2000", tot[0], tot[1], tot[2]))
        dice("\n   Sotto i 10 eventi in top 100 la Domanda B va ridimensionata a descrittiva,")
        dice("   e il numero di eventi fissa il numero massimo di predittori (10 per variabile).")


def main():
    ap = argparse.ArgumentParser(description="Scarica gli esiti di carriera da ProCyclingStats.")
    ap.add_argument("--stato", action="store_true", help="mostra l'avanzamento e esce")
    ap.add_argument("--strati", default="ABCD",
                    help="quali strati eseguire, es. AB (default tutti)")
    ap.add_argument("--limite", type=int, help="massimo profili nello strato D")
    ap.add_argument("--continental", action="store_true",
                    help="nello strato A enumera anche le squadre Continental "
                         "(~200 per stagione: aggiunge un paio d'ore)")
    ap.add_argument("--pausa", type=float, default=PAUSA)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(DB_PCS), exist_ok=True)
    db = sqlite3.connect(DB_PCS)
    db.executescript(DDL)

    if args.stato:
        stato(db)
        return

    pcs = carica_libreria()
    f = Fonte(pcs, db, args.pausa)
    avvio = time.time()
    try:
        if "A" in args.strati.upper():
            strato_a(f, db, args.continental)
        if "B" in args.strati.upper():
            strato_b(f, db)
        if "C" in args.strati.upper():
            strato_c(f, db)
        if "D" in args.strati.upper():
            strato_d(f, db, args.limite)
    except KeyboardInterrupt:
        dice("\nInterrotto: quanto scaricato e' salvato, rilancia per riprendere.")
    finally:
        db.commit()

    dice("%d richieste in %s." % (f.n, durata(time.time() - avvio)))
    dice("Ora: python scripts/04_scarica_pcs.py --stato")


if __name__ == "__main__":
    main()
