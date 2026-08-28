"""
Stile comune delle figure, e salvataggio in PNG.

DUE SCELTE CHE VALE LA PENA MOTIVARE

    Le figure si rigenerano tutte a ogni esecuzione. Non esiste una figura "vecchia" da
    qualche parte: se i dati cambiano e una figura non viene rigenerata, non compare.
    E' l'unico modo per non ritrovarsi un grafico che contraddice la tabella accanto.

    Il colore non porta informazione da solo. Le serie si distinguono anche per forma
    del marcatore e posizione, cosi' il grafico resta leggibile in bianco e nero e per
    chi non distingue i colori.

USO
    from lib_grafici import figura, salva

    with figura("Il vantaggio di nascere a gennaio") as (fig, ax):
        ax.plot(x, y, marker="o")
        ax.set_ylabel("rapporto Q1/Q4")
    percorso = salva("rae_gradiente")
"""
import contextlib
import os

CARTELLA = "output/figure"

# Palette sobria, leggibile anche in scala di grigi: le tinte hanno luminosita' diverse.
COLORI = ["#1f4e79", "#c0504d", "#4f81bd", "#9bbb59", "#8064a2", "#f79646"]
GRIGIO = "#666666"
RIFERIMENTO = "#999999"


def _plt():
    try:
        import matplotlib
        matplotlib.use("Agg")            # nessuna finestra: si scrive solo su file
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        raise SystemExit("Serve matplotlib per le figure:\n    pip install matplotlib")


def stile():
    plt = _plt()
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "-",
        "legend.frameon": False,
    })
    return plt


@contextlib.contextmanager
def figura(titolo=None, larghezza=7.0, altezza=4.2):
    plt = stile()
    fig, ax = plt.subplots(figsize=(larghezza, altezza))
    if titolo:
        ax.set_title(titolo, loc="left", pad=12)
    try:
        yield fig, ax
    finally:
        pass


def salva(nome, fig=None):
    """Salva la figura corrente e restituisce il percorso, da passare all'archivio."""
    plt = _plt()
    os.makedirs(CARTELLA, exist_ok=True)
    percorso = os.path.join(CARTELLA, nome + ".png")
    (fig or plt.gcf()).savefig(percorso)
    plt.close(fig or plt.gcf())
    return percorso


def linea_riferimento(ax, y=1.0, testo=None):
    """La linea dell'atteso. Va sempre disegnata dove un rapporto ha un valore neutro:
    senza, il lettore non sa da dove si misura lo scostamento."""
    ax.axhline(y, color=RIFERIMENTO, linestyle="--", linewidth=1, zorder=0)
    if testo:
        ax.annotate(testo, xy=(0.995, y), xycoords=("axes fraction", "data"),
                    ha="right", va="bottom", fontsize=8, color=GRIGIO)
