"""
L'archivio dei risultati: il confine fra calcolo e presentazione.

PERCHE' ESISTE
    I moduli di analisi calcolano e scrivono qui. Il generatore del Markdown legge solo
    da qui e non ricalcola nulla. Tre motivi concreti:

    - i modelli sono la parte lenta, il testo e le figure si riscrivono venti volte;
    - lo stesso numero puo' comparire in due sezioni senza essere ricalcolato, e quindi
      senza rischio che le due versioni divergano;
    - quando un numero nel testo sembra sbagliato lo si interroga con una query, invece
      di rileggere il codice che lo ha prodotto.

    E' anche il punto in cui R e Python si incontrano: i modelli girano in R e scrivono
    in questo stesso database SQLite, che Python poi legge per assemblare il report.

COME SI USA

    from lib_risultati import Archivio

    with Archivio("rae") as ar:
        ar.valore("q1_su_q4_u15", 2.08, nota="rapporto fra primo e quarto trimestre")
        ar.tabella("composizione", righe, colonne=["categoria", "Q1", "Q2", "Q3", "Q4"])
        ar.figura("gradiente", "figure/rae_gradiente.png",
                  didascalia="Il vantaggio dei nati a inizio anno svanisce con l'eta'")

    Rieseguendo un modulo, i suoi risultati precedenti vengono sostituiti: non restano
    numeri orfani di un'esecuzione vecchia.
"""
import json
import os
import sqlite3

DB_RISULTATI = "output/risultati.db"

DDL = """
CREATE TABLE IF NOT EXISTS valore (
    modulo   TEXT NOT NULL,
    chiave   TEXT NOT NULL,
    valore   TEXT,          -- serializzato JSON: numeri, stringhe, liste
    nota     TEXT,
    PRIMARY KEY (modulo, chiave)
);

CREATE TABLE IF NOT EXISTS tabella (
    modulo   TEXT NOT NULL,
    chiave   TEXT NOT NULL,
    colonne  TEXT NOT NULL,  -- JSON
    righe    TEXT NOT NULL,  -- JSON: lista di liste
    titolo   TEXT,
    nota     TEXT,
    PRIMARY KEY (modulo, chiave)
);

CREATE TABLE IF NOT EXISTS figura (
    modulo      TEXT NOT NULL,
    chiave      TEXT NOT NULL,
    percorso    TEXT NOT NULL,
    didascalia  TEXT,
    PRIMARY KEY (modulo, chiave)
);

CREATE TABLE IF NOT EXISTS esecuzione (
    modulo     TEXT PRIMARY KEY,
    eseguito_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note       TEXT
);
"""


class Archivio:
    """Scrittura dei risultati di un modulo. Da usare come context manager."""

    def __init__(self, modulo, percorso=DB_RISULTATI, pulisci=True):
        self.modulo = modulo
        self.pulisci = pulisci
        os.makedirs(os.path.dirname(percorso), exist_ok=True)
        self.db = sqlite3.connect(percorso)
        self.db.executescript(DDL)

    def __enter__(self):
        # Si riparte puliti: un modulo rieseguito non deve lasciare in giro i propri
        # risultati vecchi, che altrimenti finirebbero nel report senza che nessuno
        # se ne accorga.
        #
        # `pulisci=False` serve nel solo caso in cui due linguaggi scrivono nello stesso
        # modulo: i modelli in R producono i numeri, Python vi aggiunge la figura. Li'
        # cancellare significherebbe buttare via il lavoro di R.
        if self.pulisci:
            for t in ("valore", "tabella", "figura"):
                self.db.execute("DELETE FROM %s WHERE modulo = ?" % t, (self.modulo,))
        return self

    def __exit__(self, *exc):
        if exc[0] is None:
            self.db.execute("INSERT OR REPLACE INTO esecuzione (modulo, eseguito_il) "
                            "VALUES (?, CURRENT_TIMESTAMP)", (self.modulo,))
            self.db.commit()
        self.db.close()
        return False

    def valore(self, chiave, valore, nota=None):
        """Un singolo numero o stringa, da richiamare nel testo del report."""
        self.db.execute("INSERT OR REPLACE INTO valore VALUES (?,?,?,?)",
                        (self.modulo, chiave, json.dumps(valore), nota))

    def tabella(self, chiave, righe, colonne, titolo=None, nota=None):
        self.db.execute("INSERT OR REPLACE INTO tabella VALUES (?,?,?,?,?,?)",
                        (self.modulo, chiave, json.dumps(colonne),
                         json.dumps([list(r) for r in righe]), titolo, nota))

    def figura(self, chiave, percorso, didascalia=None):
        self.db.execute("INSERT OR REPLACE INTO figura VALUES (?,?,?,?)",
                        (self.modulo, chiave, percorso, didascalia))


class Lettura:
    """Sola lettura, per il generatore del Markdown."""

    def __init__(self, percorso=DB_RISULTATI):
        if not os.path.exists(percorso):
            raise SystemExit("Manca %s: esegui prima i moduli di analisi." % percorso)
        self.db = sqlite3.connect(percorso)

    def valore(self, modulo, chiave, default=None):
        r = self.db.execute("SELECT valore FROM valore WHERE modulo=? AND chiave=?",
                            (modulo, chiave)).fetchone()
        return json.loads(r[0]) if r else default

    def valori(self, modulo):
        return {k: json.loads(v) for k, v in
                self.db.execute("SELECT chiave, valore FROM valore WHERE modulo=?", (modulo,))}

    def tabella(self, modulo, chiave):
        r = self.db.execute("""SELECT colonne, righe, titolo, nota FROM tabella
                               WHERE modulo=? AND chiave=?""", (modulo, chiave)).fetchone()
        if not r:
            return None
        return {"colonne": json.loads(r[0]), "righe": json.loads(r[1]),
                "titolo": r[2], "nota": r[3]}

    def figura(self, modulo, chiave):
        r = self.db.execute("""SELECT percorso, didascalia FROM figura
                               WHERE modulo=? AND chiave=?""", (modulo, chiave)).fetchone()
        return {"percorso": r[0], "didascalia": r[1]} if r else None

    def moduli(self):
        return [r[0] for r in self.db.execute(
            "SELECT modulo FROM esecuzione ORDER BY modulo")]

    def eseguito_il(self, modulo):
        r = self.db.execute("SELECT eseguito_il FROM esecuzione WHERE modulo=?",
                            (modulo,)).fetchone()
        return r[0] if r else None
