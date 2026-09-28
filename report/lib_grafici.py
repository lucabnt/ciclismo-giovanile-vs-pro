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
from datetime import date

CARTELLA = "output/figure"
CARTELLA_WEB = "output/figure_web"

# Quanto ingrandire i testi nella versione per il web. Le figure del documento si
# leggono accanto alla tabella che le spiega; quelle di un post si leggono da sole e
# spesso da telefono, dove un'etichetta a otto punti e' illeggibile.
INGRANDIMENTO = 1.45

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


def _accenta(fig):
    """Accenta ogni testo della figura appena prima di scriverla su disco.

    I titoli e le etichette degli assi non passano dal generatore del Markdown, quindi
    senza questo passaggio uscirebbero in ASCII mentre il testo intorno e' accentato.
    Farlo qui, e non in ogni modulo, significa che vale per tutte le figure — comprese
    quelle che verranno scritte in futuro.
    """
    try:
        import accenti
    except ImportError:
        return
    for t in fig.findobj(match=lambda o: hasattr(o, "get_text")):
        testo = t.get_text()
        if testo:
            nuovo = accenti.applica(testo)
            if nuovo != testo:
                t.set_text(nuovo)


def _versione_web(fig, percorso):
    """La stessa figura, rifinita per essere letta da sola e da telefono.

    Non e' una figura diversa: e' la stessa, con i testi piu' grandi, le linee piu'
    spesse e piu' risoluzione. Farne una copia invece di sostituire l'originale ha una
    ragione precisa — nel documento le figure stanno accanto alla tabella che le
    commenta, e li' un testo grande sarebbe sproporzionato; in un post stanno da sole.

    Resta un lavoro che questa funzione non puo' fare: scrivere il messaggio dentro la
    figura. Quello dipende da cosa dice il post attorno, e va fatto post per post.
    """
    salvati = {}
    for t in fig.findobj(match=lambda o: hasattr(o, "get_fontsize")):
        salvati[t] = t.get_fontsize()
        t.set_fontsize(t.get_fontsize() * INGRANDIMENTO)
    for ax in fig.get_axes():
        for linea in ax.get_lines():
            linea.set_linewidth(linea.get_linewidth() * 1.3)
            if linea.get_markersize():
                linea.set_markersize(linea.get_markersize() * 1.2)
    fig.set_size_inches(fig.get_size_inches() * 1.15)

    # Ingrandire i testi senza rifare la disposizione li fa collidere. Le etichette
    # lunghe sull'asse orizzontale si inclinano, e la figura si ricompone.
    for ax in fig.get_axes():
        etichette = [t.get_text() for t in ax.get_xticklabels()]
        # Sotto i dodici caratteri le etichette stanno in orizzontale senza toccarsi,
        # e in orizzontale si leggono meglio: si inclina solo quando serve davvero.
        lunghe = [e for e in etichette if len(e) > 12]
        # Un'etichetta gia' su due righe, ruotata, si sovrappone alla vicina: e' il caso
        # in cui la rotazione peggiora invece di risolvere, quindi si lascia stare.
        if any(chr(10) in e for e in etichette):
            continue
        if len(etichette) > 3 and lunghe:
            for t in ax.get_xticklabels():
                t.set_rotation(25)
                t.set_horizontalalignment("right")
    try:
        fig.tight_layout()
    except Exception:
        pass

    os.makedirs(CARTELLA_WEB, exist_ok=True)
    fig.savefig(os.path.join(CARTELLA_WEB, os.path.basename(percorso)), dpi=200,
                bbox_inches="tight")


def _timbro(fig):
    """La data di generazione, scritta dentro l'immagine. Restituisce il testo aggiunto.

    Serve alla versione del documento, dove una figura puo' essere ritagliata e girare da
    sola: senza la riga, chi se la ritrova davanti non sa piu' di quando siano i numeri.

    Sulla versione per il web non si mette, ed e' una scelta estetica: li' la figura sta
    dentro un post che porta gia' la propria data, e una riga di servizio sotto il grafico
    si vede. Per questo `salva()` la toglie prima di produrla.

    Sta sotto il grafico e fuori dagli assi: `bbox_inches="tight"` allarga l'immagine per
    comprenderla, quindi non copre niente.

    La quota non e' fissa. Alcuni moduli scrivono sotto l'asse una nota lunga quanto tutta
    la figura, e una data ancorata a destra a quota fissa ci finiva sopra: si cerca quindi
    il testo piu' in basso gia' presente e ci si mette sotto.
    """
    quote = [t.get_position()[1] for t in fig.texts if t.get_position()[1] < 0]
    y = min(quote) - 0.035 if quote else -0.02
    return fig.text(1.0, y, "elaborazione del %s" % date.today(), ha="right", va="top",
                    fontsize=7, color=RIFERIMENTO)


def salva(nome, fig=None):
    """Salva la figura corrente e restituisce il percorso, da passare all'archivio.

    Produce due file: quello del documento e, accanto, la versione per il web in
    `output/figure_web/`. L'archivio registra solo il primo — il secondo si prende dal
    nome, quando si scrivono i post.
    """
    plt = _plt()
    os.makedirs(CARTELLA, exist_ok=True)
    percorso = os.path.join(CARTELLA, nome + ".png")
    fig = fig or plt.gcf()
    _accenta(fig)
    timbro = _timbro(fig)
    fig.savefig(percorso)
    timbro.remove()
    _versione_web(fig, percorso)
    plt.close(fig)
    return percorso


def legenda(ax, colonne=None, **kw):
    """La legenda sotto il grafico, a distanza sufficiente dalle etichette.

    Va messa qui e non a mano nei moduli perche' la distanza giusta non e' ovvia: la
    versione web ingrandisce i testi di quasi meta' e allunga le etichette dell'asse, e
    una legenda posizionata a occhio finisce a sovrapporsi appena i caratteri crescono.
    Sopra il grafico non si puo' mettere, perche' li' c'e' il titolo.

    Presuppone etichette dell'asse orizzontale su una riga sola: se servono due righe,
    conviene accorciarle invece di allontanare la legenda.
    """
    voci = len(ax.get_legend_handles_labels()[0])
    ax.legend(frameon=False, fontsize=kw.pop("fontsize", 9),
              ncol=colonne or min(voci, 4), loc="upper center",
              bbox_to_anchor=(0.5, -0.16), borderaxespad=0, **kw)


def linea_riferimento(ax, y=1.0, testo=None, verticale=False):
    """La linea dell'atteso. Va sempre disegnata dove un rapporto ha un valore neutro:
    senza, il lettore non sa da dove si misura lo scostamento.

    `verticale` serve ai grafici a intervalli, dove la grandezza sta sull'asse x e la
    linea del "nessun effetto" e' quindi verticale."""
    if verticale:
        ax.axvline(y, color=RIFERIMENTO, linestyle="--", linewidth=1, zorder=0)
        if testo:
            ax.annotate(testo, xy=(y, 0.99), xycoords=("data", "axes fraction"),
                        ha="left", va="top", fontsize=8, color=GRIGIO)
        return
    ax.axhline(y, color=RIFERIMENTO, linestyle="--", linewidth=1, zorder=0)
    if testo:
        ax.annotate(testo, xy=(0.995, y), xycoords=("axes fraction", "data"),
                    ha="right", va="bottom", fontsize=8, color=GRIGIO)
