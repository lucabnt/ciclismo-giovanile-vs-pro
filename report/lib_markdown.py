"""
Da risultato a Markdown, con tre regole imposte dal codice invece che ricordate.

REGOLA 1 — la numerosita' si dichiara sempre
    Una tabella senza il proprio `n` non permette al lettore di capire quando una cella
    e' sottile. `tabella()` accetta un parametro `n` e lo scrive sotto la tabella.

REGOLA 2 — nessuna cella con meno di `min_cella_pubblicabile` atleti
    I dati riguardano minorenni, e una cella con due o tre persone li rende
    identificabili anche in forma aggregata. La soglia sta in config.toml e qui viene
    applicata: le celle troppo piccole diventano "<5" invece del numero esatto.

    E' una scelta deliberata: mascherare invece di omettere la riga, cosi' il lettore
    vede che quella categoria esiste ma e' troppo piccola per essere mostrata.

REGOLA 3 — ogni misura porta con se' la propria definizione
    `metodo()` produce il riquadro che spiega come si calcola una cosa, con rimandi a
    risorse stabili. Un documento destinato a chi non fa statistica di mestiere deve
    poter essere letto senza doversi fidare: una misura senza definizione e' un numero
    di cui fidarsi o no, non un argomento.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from lib_giovanile import cfg

MIN_CELLA = cfg("etica", "min_cella_pubblicabile")


def maschera(v, e_un_conteggio=True):
    """Nasconde i conteggi troppo piccoli per essere pubblicati."""
    if not e_un_conteggio or v is None or isinstance(v, str):
        return v
    if isinstance(v, (int, float)) and 0 < v < MIN_CELLA:
        return "<%d" % MIN_CELLA
    return v


def fmt(v, decimali=1):
    """Numeri all'italiana: la virgola separa i decimali.

    Vale per le tabelle. Per i numeri dentro il testo si usa num(), perche' li' il
    formato lo decide chi scrive la frase.
    """
    if v is None:
        return "—"
    if isinstance(v, float):
        return (("%%.%df" % decimali) % v).replace(".", ",")
    return str(v)


def num(v, decimali=1):
    """Un numero dentro una frase, con la virgola decimale."""
    if v is None:
        return "—"
    return (("%%.%df" % decimali) % float(v)).replace(".", ",")


def tabella(colonne, righe, n=None, nota=None, colonne_conteggio=(), decimali=1):
    """Tabella Markdown.

    `colonne_conteggio` elenca gli indici delle colonne che sono conteggi di persone:
    su quelle si applica la soglia di pubblicabilita'.
    """
    out = ["| " + " | ".join(str(c) for c in colonne) + " |",
           "|" + "|".join("---" for _ in colonne) + "|"]
    mascherate = 0
    for r in righe:
        celle = []
        for i, v in enumerate(r):
            if i in colonne_conteggio:
                m = maschera(v)
                if m != v:
                    mascherate += 1
                v = m
            celle.append(fmt(v, decimali))
        out.append("| " + " | ".join(celle) + " |")

    coda = []
    if n is not None:
        coda.append("n = %s" % (f"{n:,}".replace(",", ".") if isinstance(n, int) else n))
    if mascherate:
        coda.append("%d cella/e con meno di %d atleti sono mascherate" % (mascherate, MIN_CELLA))
    if nota:
        coda.append(nota)
    if coda:
        out.append("")
        out.append("*" + " · ".join(coda) + "*")
    return "\n".join(out)


def _virgola_decimale(testo):
    """Punto decimale in virgola, come si scrive in italiano.

    Si applica solo alla prosa e solo fra due cifre, quindi non tocca date, intervalli
    di coorti o versioni. I tratti fra apici inversi restano intatti: li' dentro ci
    sono formule e nomi di colonna, dove il punto non e' un separatore decimale.
    """
    pezzi = testo.split("`")
    for i in range(0, len(pezzi), 2):          # gli indici dispari sono dentro gli apici
        pezzi[i] = re.sub(r"(?<=\d)\.(?=\d)", ",", pezzi[i])
    return "`".join(pezzi)


def figura(percorso, didascalia=None, radice="output"):
    """Riferimento a un PNG, con percorso relativo al file .md."""
    rel = os.path.relpath(percorso, radice).replace(os.sep, "/")
    if didascalia:
        didascalia = _virgola_decimale(didascalia)
    testo = "![%s](%s)" % (didascalia or "", rel)
    return testo + ("\n\n*" + didascalia + "*" if didascalia else "")


def metodo(nome, spiegazione, fonti=()):
    """Il riquadro che spiega come si misura una cosa, con i rimandi per approfondire.

    I rimandi sono a risorse stabili e verificabili — voci di enciclopedia, manuali di
    istituti di statistica, pagine ufficiali di dataset — non a blog o dispense.
    """
    righe = ["> **Come si misura — %s**" % nome, ">"]
    for par in spiegazione.strip().split("\n\n"):
        righe.append("> " + _virgola_decimale(" ".join(par.split())))
        righe.append(">")
    if fonti:
        righe.append("> Approfondimenti: "
                     + " · ".join("[%s](%s)" % (t, u) for t, u in fonti))
    else:
        righe.pop()
    return "\n".join(righe)


def ancora(titolo):
    """Ancora in stile GitHub: minuscole, punteggiatura via, spazi in trattini."""
    a = titolo.strip().lower()
    a = "".join(c for c in a if c.isalnum() or c in " -_")
    return a.replace(" ", "-")


def indice(testo, livello_max=3):
    """Costruisce l'indice leggendo i titoli del documento gia' generato.

    Si legge dal testo e non da una lista scritta a mano: un titolo cambiato dentro un
    modulo si riflette nell'indice senza che nessuno debba ricordarsene.
    """
    voci = []
    dentro_codice = False
    for riga in testo.split("\n"):
        if riga.startswith("```"):
            dentro_codice = not dentro_codice
            continue
        if dentro_codice or not riga.startswith("##"):
            continue
        livello = len(riga) - len(riga.lstrip("#"))
        if livello > livello_max:
            continue
        titolo = riga[livello:].strip()
        voci.append("%s- [%s](#%s)" % ("  " * (livello - 2), titolo, ancora(titolo)))
    return "\n".join(voci)


def sezione(titolo, livello=2):
    return "\n" + "#" * livello + " " + titolo + "\n"


def paragrafo(*parti):
    """Le stringhe vuote passate fra due blocchi sono separatori di paragrafo, non
    valori da scartare: in Markdown la riga vuota e' significativa."""
    return _virgola_decimale(
        "\n".join(str(p) for p in parti if p is not None)) + "\n"
