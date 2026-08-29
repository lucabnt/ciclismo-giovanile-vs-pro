"""
Controlla che i numeri citati nei documenti scritti a mano siano ancora quelli
dell'analisi.

PERCHE' ESISTE
    Tutto il resto del progetto ha una regola: nessun numero si scrive a mano, perche' i
    numeri cambiano quando i dati cambiano e un testo fisso diventa falso in silenzio.

    Due documenti violano quella regola, e non per distrazione. `docs/tripod.md` e' prosa
    di controllo, `docs/piano_post.md` e' un piano editoriale: rigenerarli a ogni
    esecuzione non avrebbe senso. Contengono pero' decine di cifre copiate dall'analisi —
    quanti professionisti, quanti eventi, quale percentuale intercettata — che l'anno
    prossimo saranno altre.

    Questo script e' il compromesso: i documenti restano scritti a mano, ma le loro cifre
    vengono confrontate con l'archivio dei risultati. Se divergono lo dice, invece di
    lasciare in giro testi che descrivono un'analisi che non esiste piu'.

COSA NON FA
    Non verifica le affermazioni qualitative, che sono la parte importante di quei
    documenti e vanno riviste da una persona. Verifica solo le cifre, che sono la parte
    che si guasta da sola.

    Non controlla `docs/literature_review.md`: quella non cita cifre dell'analisi, quindi
    non si guasta quando i dati cambiano. Invecchia con la letteratura, che e' un altro
    tipo di manutenzione e ha il suo avviso in testa al file.

USO
    python scripts/11_verifica_documenti.py
"""
import json
import os
import re
import sqlite3
import sys

TRIPOD = os.path.join("docs", "tripod.md")
PIANO = os.path.join("docs", "piano_post.md")
RISULTATI = os.path.join("output", "risultati.db")
ANALISI = os.path.join("output", "analisi.md")

# Il documento generato usa lo spazio stretto insecabile per le migliaia.
SPAZI = (" ", " ", " ")


def valore(db, modulo, chiave):
    r = db.execute("SELECT valore FROM valore WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def tabella(db, modulo, chiave):
    r = db.execute("SELECT righe FROM tabella WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def _numero(testo):
    """Da «2 817» o «30,6» al numero. Restituisce None se non e' un numero."""
    if testo is None:
        return None
    ripulito = testo
    for s in SPAZI:
        ripulito = ripulito.replace(s, "")
    try:
        return float(ripulito.replace(",", "."))
    except ValueError:
        return None


def attesi_tripod(db):
    """Le cifre che la checklist cita, ricavate dall'archivio.

    Ogni voce e' (descrizione, valore atteso, espressione che lo cerca nel testo). Il
    primo gruppo non vuoto dell'espressione deve catturare il numero.
    """
    livelli = tabella(db, "qualita", "livelli") or []
    top100 = next((r[1] for r in livelli if "top 100" in str(r[0])), None)
    temporale = tabella(db, "validazione", "temporale") or []
    chiave = valore(db, "metriche", "frase_chiave") or {}

    sezioni = None
    if os.path.exists(ANALISI):
        with open(ANALISI, encoding="utf-8") as f:
            # L'indice e' una sezione del documento ma non una sezione di analisi.
            sezioni = len(re.findall(r"^## ", f.read(), re.M)) - 1

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
        ("futuri professionisti intercettati",
         round(chiave["sensibilita"]) if chiave.get("sensibilita") else None,
         r"il (\d+)% dei futuri professionisti"),
        ("selezionati che non arrivano",
         round(100 - chiave["vpp"]) if chiave.get("vpp") else None,
         r"il (\d+)% dei selezionati che non ce la far"),
        ("sezioni del documento", sezioni,
         r"documento a (\d+) sezioni"),
    ]


def attesi_piano(db):
    """Le cifre che il piano editoriale cita, ricavate dall'archivio."""
    curva = valore(db, "attrito", "curva") or []
    chiave = valore(db, "metriche", "frase_chiave") or {}
    tra = valore(db, "traiettorie", "auc") or {}
    uni_max = valore(db, "univariati", "auc_massima") or {}
    ann = valore(db, "annidati", "salto_maggiore") or {}
    return [
        ("classificati in Under 15", curva[0][1] if curva else None,
         r"da ([\d  ]+) classificati in Under 15"),
        ("professionisti", valore(db, "attrito", "pro_totali"),
         r"classificati in Under 15 a\s+(\d+)\s"),
        ("rientri dopo un'assenza",
         valore(db, "attrito", "rientri_dopo_assenza"),
         r"\*\*(\d+,\d)%\*\* degli atleti salta almeno una stagione"),
        ("resta in classifica al cambio di categoria",
         valore(db, "passaggi", "resta_fra"),
         r"resta in classifica il (\d+)% contro"),
        ("quota della lista di arrivo che c'era gia'",
         valore(db, "passaggi", "quota_fra"),
         r"composta per l'\*\*(\d+)%\*\* da persone"),
        ("cambio di societa' fra Juniores e Under 23",
         valore(db, "contesto", "cambio_juniores_u23"),
         r"il \*\*(\d+,\d)%\*\* cambia societ"),
        ("futuri professionisti intercettati",
         round(chiave["sensibilita"]) if chiave.get("sensibilita") else None,
         r"si intercetta il \*\*(\d+)% dei\s+futuri"),
        ("selezionati che non arrivano",
         round(100 - chiave["vpp"]) if chiave.get("vpp") else None,
         r"il\s+\*\*(\d+)% dei selezionati non lo diventer"),
        ("odds ratio piu' alto", uni_max.get("or"),
         r"per (\d,\d\d) in Under 19"),
        ("AUC con livello e pendenza", tra.get("completo"),
         r"da 0,848 a (\d,\d+)"),
        ("salto maggiore nei modelli annidati", ann.get("delta"),
         r"\(ΔAUC \+(\d,\d+)\)"),
    ]


def controlla(testo, voci, problemi):
    for descrizione, atteso, pattern in voci:
        m = re.search(pattern, testo)
        citato = next((g for g in m.groups() if g), None) if m else None
        if atteso is None:
            stato = "NON CALCOLATO: eseguire l'analisi"
        elif m is None:
            stato = "NON CITATO nel documento"
        elif _numero(citato) is None:
            stato = "non interpretabile: %r" % citato
        elif abs(_numero(citato) - float(atteso)) > _tolleranza(citato):
            stato = "il documento dice %s" % citato
        else:
            stato = "ok"
        if stato != "ok":
            problemi.append(descrizione)
        print("  %-44s analisi %-9s %s"
              % (descrizione, "—" if atteso is None else _mostra(atteso), stato))


def _tolleranza(citato):
    """Quanto puo' discostarsi il valore citato da quello dell'archivio.

    Dipende da come e' scritto: chi arrotonda a numero intero non sta sbagliando, sta
    arrotondando, e la tolleranza deve essere mezza unita' dell'ultima cifra scritta.
    Confrontare «32» con 32,4 pretendendo l'uguaglianza segnalerebbe un errore che non
    c'e' — e un controllo che grida al lupo smette di essere letto.
    """
    decimali = len(citato.split(",")[1]) if "," in citato else 0
    return 0.5 * 10 ** (-decimali) + 1e-9


def _mostra(v):
    return ("%g" % v).replace(".", ",") if isinstance(v, float) else str(v)


def main():
    if not os.path.exists(RISULTATI):
        sys.exit("Manca %s: eseguire prima l'analisi." % RISULTATI)
    db = sqlite3.connect(RISULTATI)
    problemi = []

    for percorso, voci in ((TRIPOD, attesi_tripod), (PIANO, attesi_piano)):
        if not os.path.exists(percorso):
            continue
        print(percorso.replace(os.sep, "/"))
        with open(percorso, encoding="utf-8") as f:
            controlla(f.read(), voci(db), problemi)
        print()

    db.close()
    if problemi:
        print("%d cifra/e non corrispondono piu' all'analisi." % len(problemi))
        print("Aggiornare il documento, e rileggere le affermazioni che vi si "
              "appoggiano: quando i numeri cambiano, di solito cambia anche cosa se ne "
              "puo' dire.")
        return 1
    print("Le cifre dei documenti scritti a mano corrispondono all'analisi corrente.")
    print("Le affermazioni qualitative restano da rivedere a mano: sono la parte che "
          "questo controllo non puo' fare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
