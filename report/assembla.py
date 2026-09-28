"""
Assembla il documento unico a partire dai risultati gia' calcolati.

COME FUNZIONA
    Ogni modulo di analisi ha due funzioni:

        calcola()      interroga i database e scrive nell'archivio dei risultati
        rendi(lettura) legge SOLO dall'archivio e restituisce il testo della sezione

    Questo file esegue `rendi` e concatena. Non tocca mai `analisi.db` ne' `pcs.db`:
    se un numero non e' nell'archivio non puo' finire nel testo, e quindi non puo'
    essere scritto a mano.

L'ORDINE DELLE SEZIONI STA IN config.toml
    Non nei nomi dei file. Riorganizzare il documento, o dividerlo in piu' post, non
    comporta rinominare moduli.

USO
    python report/assembla.py                # esegue i calcoli e scrive il documento
    python report/assembla.py --solo-testo   # riusa i risultati in archivio
    python report/assembla.py --moduli rae   # solo alcuni moduli
"""
import argparse
import importlib
import os
import sys
from datetime import date

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.join(QUI, "moduli"))
sys.path.insert(0, os.path.join(QUI, "..", "scripts"))
from lib_giovanile import cfg           # noqa: E402
from lib_risultati import Lettura       # noqa: E402
import lib_markdown as md              # noqa: E402
import accenti                         # noqa: E402

USCITA = "output/analisi.md"


def dice(*a):
    print(*a)
    sys.stdout.flush()


def intestazione(lt, moduli):
    lo, hi = cfg("coorti", "domanda_a_c")
    lo_b, hi_b = cfg("coorti", "domanda_b")
    return "\n".join([
        "# Ranking giovanili italiani e transizione al professionismo",
        "",
        "*Documento generato da `report/assembla.py` il %s. "
        "Ogni numero viene da una query: non c'e' nulla scritto a mano.*" % date.today(),
        "",
        "| | |",
        "|---|---|",
        "| Popolazione | atleti con almeno un punto nel ranking nazionale di ciclismo.info |",
        "| Coorti, accesso al professionismo | nati %d-%d |" % (lo, hi),
        "| Coorti, qualita' della carriera | nati %d-%d |" % (lo_b, hi_b),
        "| Sesso | %s |" % cfg("studio", "sesso"),
        "| Ultima stagione | %d |" % cfg("stagioni", "massima"),
        "| Sezioni | %s |" % ", ".join(moduli),
        "",
        "> I risultati riguardano **gruppi, non persone**. Le celle con meno di %d atleti "
        "sono mascherate: i dati riguardano minorenni." % cfg("etica", "min_cella_pubblicabile"),
        "",
        "---",
    ])


def aggiorna_webp():
    """Riconverte in WebP le figure per il blog, che stanno fuori dal repository.

    Sta qui e non a parte perche' una conversione da fare a mano, una figura per volta al
    momento di pubblicare, prima o poi manda online una figura vecchia. Se qualcosa non va
    lo si dice e si prosegue: il documento e' gia' scritto, e le WebP servono solo ai post.
    """
    try:
        sys.path.insert(0, "scripts")
        from importlib import import_module
        import_module("12_figure_webp").converti(dice=dice)
    except Exception as e:
        dice("   WebP non aggiornate (%s). Si rifanno con: python scripts/12_figure_webp.py"
             % e)


def main():
    ap = argparse.ArgumentParser(description="Assembla il documento delle analisi.")
    ap.add_argument("--solo-testo", action="store_true",
                    help="non ricalcola, riusa i risultati gia' in archivio")
    ap.add_argument("--moduli", nargs="+", help="esegue solo questi moduli")
    args = ap.parse_args()

    ordine = args.moduli or cfg("report", "sezioni")
    os.makedirs("output", exist_ok=True)

    caricati = {}
    for nome in ordine:
        try:
            caricati[nome] = importlib.import_module(nome)
        except ImportError as e:
            dice("   modulo '%s' non trovato, salto (%s)" % (nome, e))

    if not args.solo_testo:
        for nome, mod in caricati.items():
            if hasattr(mod, "calcola"):
                dice("calcolo: %s" % nome)
                mod.calcola()

    lt = Lettura()
    md.azzera_premesse()
    parti = [intestazione(lt, list(caricati))]
    for nome, mod in caricati.items():
        if not hasattr(mod, "rendi"):
            dice("   '%s' non ha rendi(): salto nel documento" % nome)
            continue
        parti.append(mod.rendi(lt))

    # Gli accenti si applicano qui, in un punto solo. I moduli possono scrivere il testo
    # in ASCII e il documento esce accentato: la correzione sta nel codice che produce
    # il file, non nel file, e vale anche quando verra' rigenerato fra anni.
    #
    # Prima dell'indice e non dopo: le ancore si ricavano dai titoli, e accentare un
    # titolo dopo aver costruito l'indice darebbe rimandi che non arrivano da nessuna
    # parte.
    parti = [accenti.applica(p) for p in parti]
    mancanti = accenti.residui("\n".join(parti))
    if mancanti:
        dice("   parole con apostrofo non riconosciute (se sono accenti, aggiungerle a "
             "report/accenti.py): " + ", ".join(mancanti))

    # L'indice si costruisce leggendo i titoli del testo gia' prodotto, non da una lista
    # scritta a mano: un titolo cambiato dentro un modulo si riflette da solo.
    corpo = "\n\n".join(parti[1:]).rstrip()
    documento = parti[0] + "\n\n## Indice\n\n" + md.indice(corpo) + "\n\n---\n\n" + corpo

    # Le premesse cadute vanno dette in testa al documento, non solo sul terminale: chi
    # rigenera puo' non essere chi legge, e un avviso solo a schermo si perde.
    cadute = md.premesse_fallite()
    if cadute:
        documento = documento.replace("\n\n## Indice\n\n",
                                      "\n\n" + md.avviso_premesse(cadute) +
                                      "\n\n## Indice\n\n", 1)
        dice("\n   ATTENZIONE: %d osservazione/i non sono piu' sostenute dai dati:"
             % len(cadute))
        for c in cadute:
            dice("     - %s" % c)
        dice("   Il documento e' stato scritto lo stesso, con l'avviso in testa e i "
             "paragrafi segnalati,")
        dice("   ma questo comando esce con codice 1: un commento interpretativo "
             "invecchiato e' un errore")
        dice("   da correggere, non una nota a schermo che scorre via.")

    with open(USCITA, "w", encoding="utf-8") as f:
        f.write(documento + "\n")
    dice("\nScritto %s (%d sezioni, %d caratteri)"
         % (USCITA, len(parti) - 1, os.path.getsize(USCITA)))
    aggiorna_webp()
    return 1 if cadute else 0


if __name__ == "__main__":
    sys.exit(main())
