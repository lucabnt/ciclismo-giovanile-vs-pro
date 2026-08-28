"""Utilita' condivise per la costruzione del dataset dal DB ciclismo.info."""
import hashlib
import os
import re
import secrets
import sqlite3
import unicodedata

DB_GIOVANILE = "data/giovanile/ciclismo.db"
DB_ANALISI = "data/analisi/analisi.db"
DB_SCHEDE = "data/giovanile/schede.db"

# slug ciclismo.info -> (categoria internazionale, sesso, eta' al 1o anno)
CATEGORIE = {
    "esordienti":       ("U15", "M", 13),
    "donne_esordienti": ("U15", "F", 13),
    "allievi":          ("U17", "M", 15),
    "donne_allieve":    ("U17", "F", 15),
    "juniores":         ("U19", "M", 17),
    "donne_juniores":   ("U19", "F", 17),
    "elite_under23":    ("U23", "M", 19),
}

# Convenzione delle liste sorgente, verificata empiricamente (vedi docs/verifica_dati_giovanile.md)
#   'disgiunte'  = lista generale e lista primo_anno non si sovrappongono
#                  -> anno_corso della sorgente e' affidabile
#   'annidate'   = lista primo_anno e' un sottoinsieme della generale
#                  -> anno_corso = 1 se presente in primo_anno, altrimenti 2 (presunto)
LISTE_DISGIUNTE = {"esordienti": (2009, 2026), "donne_esordienti": (2022, 2026)}

FILE_SALT = "data/private/salt.txt"
_salt_cache = None


def _salt() -> str:
    """Segreto di anonimizzazione, tenuto fuori dal repository.

    Con il salt nel sorgente l'anonimizzazione sarebbe solo apparente: gli
    id_atleta della sorgente sono interi fra 1 e 37.704, quindi chiunque abbia
    il codice puo' ricalcolare l'intera tabella athlete_id -> id_atleta per
    forza bruta in pochi secondi. Da li' bastano le classifiche di
    ciclismo.info, che sono pubbliche, per risalire ai nomi.

    Il salt viene generato una sola volta e conservato in data/private/, che e'
    escluso da git. Va trattato come una chiave: se lo si perde, tutti gli
    athlete_id cambiano al primo ricalcolo.
    """
    global _salt_cache
    if _salt_cache is None:
        if os.path.exists(FILE_SALT):
            _salt_cache = open(FILE_SALT, encoding="utf-8").read().strip()
        else:
            os.makedirs(os.path.dirname(FILE_SALT), exist_ok=True)
            _salt_cache = secrets.token_hex(32)
            with open(FILE_SALT, "w", encoding="utf-8") as f:
                f.write(_salt_cache + "\n")
            print("Generato un nuovo salt di anonimizzazione in %s" % FILE_SALT)
            print("Non committarlo e non perderlo: da esso dipendono gli athlete_id.")
    return _salt_cache


def anonimizza(id_atleta: int) -> str:
    h = hashlib.sha256(f"{_salt()}|{id_atleta}".encode()).hexdigest()
    return "A" + h[:10].upper()


def normalizza_nome(s: str) -> str:
    """Chiave di match: maiuscolo, senza accenti, senza punteggiatura, token ordinati."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper().replace("'", " ").replace("`", " ").replace("-", " ")
    s = re.sub(r"[^A-Z ]", " ", s)
    return " ".join(s.split())


def chiave_match(nome: str, cognome: str) -> str:
    """Chiave insensibile all'ordine nome/cognome e ai doppi nomi."""
    tok = sorted(normalizza_nome(f"{cognome} {nome}").split())
    return " ".join(tok)


def connect(path=DB_GIOVANILE) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con
