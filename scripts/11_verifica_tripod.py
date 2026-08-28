"""
Controlla che i numeri citati in docs/tripod.md siano ancora quelli dell'analisi.

PERCHE' ESISTE
    Tutto il resto del progetto ha una regola: nessun numero si scrive a mano, perche' i
    numeri cambiano quando i dati cambiano e un testo fisso diventa falso in silenzio.

    `docs/tripod.md` viola quella regola, e non per distrazione: e' prosa di controllo,
    non un documento generato, e riscriverla a ogni esecuzione non avrebbe senso.
    Contiene pero' una dozzina di cifre copiate dall'analisi — quanti professionisti,
    quanti eventi, quante ripetizioni bootstrap — che l'anno prossimo saranno altre.

    Questo script e' il compromesso: la checklist resta scritta a mano, ma le sue cifre
    vengono confrontate con l'archivio dei risultati. Se divergono lo dice, invece di
    lasciare in giro una checklist che descrive un'analisi che non esiste piu'.

COSA NON FA
    Non verifica le affermazioni qualitative, che sono la parte importante della
    checklist e vanno riviste da una persona. Verifica solo le cifre, che sono la parte
    che si guasta da sola.

USO
    python scripts/11_verifica_tripod.py
"""
import json
import os
import re
import sqlite3
import sys

TRIPOD = os.path.join("docs", "tripod.md")
RISULTATI = os.path.join("output", "risultati.db")
ANALISI = os.path.join("output", "analisi.md")


def valore(db, modulo, chiave):
    r = db.execute("SELECT valore FROM valore WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def tabella(db, modulo, chiave):
    r = db.execute("SELECT righe FROM tabella WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def attesi(db):
    """Le cifre che la checklist cita, ricavate dall'archivio.

    Ogni voce e' (descrizione, valore atteso, espressione che lo cerca nel testo). Il
    gruppo 1 dell'espressione deve catturare il numero.
    """
    livelli = tabella(db, "qualita", "livelli") or []
    top100 = next((r[1] for r in livelli if "top 100" in str(r[0])), None)
    temporale = tabella(db, "validazione", "temporale") or []
    chiave = valore(db, "metriche", "frase_chiave") or {}

    sezioni = None
    if os.path.exists(ANALISI):
        with open(ANALISI, encoding="utf-8") as f:
            testo = f.read()
        # L'indice e' una sezione del documento ma non una sezione di analisi.
        sezioni = len(re.findall(r"^## ", testo, re.M)) - 1

    return [
        ("professionisti nelle coorti principali",
         valore(db, "attrito", "pro_totali"),
         r"(\d+) professionisti sulle coorti principali"),
        ("eventi nel modello di sopravvivenza",
         valore(db, "sopravvivenza", "n_eventi"),
         r"(\d+) nel modello di sopravvivenza"),
        ("atleti nel livello top 100", top100,
         r"(\d+) nel livello top 100"),
        ("ripetizioni del bootstrap",
         valore(db, "validazione", "ripetizioni"),
         r"\((\d+) ricampionamenti\)"),
        ("eventi nelle coorti di verifica",
         temporale[0][4] if temporale else None,
         r"riserva dei (\d+) eventi"),
        ("quota di futuri professionisti intercettati",
         round(chiave.get("sensibilita")) if chiave.get("sensibilita") else None,
         r"il (\d+)% dei futuri professionisti"),
        ("quota di selezionati che non arriva",
         round(100 - chiave["vpp"]) if chiave.get("vpp") else None,
         r"il (\d+)% dei selezionati che non ce la far"),
        ("sezioni del documento", sezioni,
         r"documento a (\d+) sezioni"),
    ]


def main():
    for percorso in (TRIPOD, RISULTATI):
        if not os.path.exists(percorso):
            sys.exit("Manca %s." % percorso)
    with open(TRIPOD, encoding="utf-8") as f:
        testo = f.read()
    db = sqlite3.connect(RISULTATI)

    problemi = []
    for descrizione, atteso, pattern in attesi(db):
        m = re.search(pattern, testo)
        if atteso is None:
            stato = "NON CALCOLATO: eseguire l'analisi"
        elif not m:
            stato = "NON CITATO nella checklist"
        elif int(m.group(1)) != int(atteso):
            stato = "la checklist dice %d" % int(m.group(1))
        else:
            stato = "ok"
        if stato != "ok":
            problemi.append(descrizione)
        print("  %-46s analisi %-6s %s"
              % (descrizione, "—" if atteso is None else int(atteso), stato))

    db.close()
    if problemi:
        print("\n%d cifra/e della checklist non corrispondono piu' all'analisi." %
              len(problemi))
        print("Aggiornare docs/tripod.md, e rileggere le voci che ci si appoggiano: "
              "quando i numeri cambiano di solito cambia anche cosa se ne puo' dire.")
        return 1
    print("\nLe cifre di docs/tripod.md corrispondono all'analisi corrente.")
    print("Le affermazioni qualitative restano da rivedere a mano: sono la parte che "
          "questo controllo non puo' fare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
