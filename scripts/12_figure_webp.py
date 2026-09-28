"""
Converte in WebP le figure destinate al blog, in una cartella fuori dal repository.

PERCHE' ESISTE
    I post pubblicati usano WebP: pesa la meta' di un PNG a parita' di resa, e la
    conversione a mano, fatta una figura per volta al momento di pubblicare, e' il tipo di
    passaggio che prima o poi porta online una figura vecchia. Qui si rifa' tutto insieme,
    e si rifa' da solo alla fine di ogni `report/assembla.py`.

COSA CONVERTE
    - `output/figure_web/`, le figure dell'analisi con i testi ingranditi per il web;
    - `output/esterne/`, le figure che non nascono dai nostri dati (oggi una sola, quella
      dello studio del 2006) e che per questo stanno gia' fuori dal repository.

    La destinazione e' `output/figure_webp/`. Sta sotto `output/`, che git ignora tranne le
    eccezioni dichiarate, quindi non entra nel repository: e' un'esportazione, si rigenera
    con un comando e nel repository sarebbero doppioni.

LOSSY O LOSSLESS
    Non si sceglie a priori. Un grafico a barre, fatto di campiture piatte e testo, spesso
    si comprime meglio senza perdita; una figura con molte sfumature no. Si prova con
    tutti e due i modi e si tiene il file piu' piccolo, che e' l'unico criterio che non
    richiede di indovinare.

USO
    python scripts/12_figure_webp.py            # converte cio' che e' cambiato
    python scripts/12_figure_webp.py --tutto    # riconverte tutto
"""
import os
import sys

SORGENTI = (os.path.join("output", "figure_web"), os.path.join("output", "esterne"))
USCITA = os.path.join("output", "figure_webp")
QUALITA = 92          # per la versione con perdita; sopra i 92 il file cresce e non si vede
METODO = 6            # compressione piu' lenta e piu' efficace, su decine di file non si sente


def _pillow():
    try:
        from PIL import Image, features
    except ImportError:
        raise SystemExit("Serve Pillow per scrivere WebP: pip install -r requirements.txt")
    if not features.check("webp"):
        raise SystemExit("Questa installazione di Pillow non sa scrivere WebP.")
    return Image


def _converti_file(Image, sorgente, destinazione):
    """Scrive il piu' piccolo fra la versione con perdita e quella senza. Torna i byte."""
    with Image.open(sorgente) as im:
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        prova = destinazione + ".tmp"
        migliore = None
        for opzioni in ({"quality": QUALITA, "method": METODO},
                        {"lossless": True, "method": METODO}):
            im.save(prova, "WEBP", **opzioni)
            peso = os.path.getsize(prova)
            if migliore is None or peso < migliore[0]:
                os.replace(prova, destinazione)
                migliore = (peso, opzioni)
            else:
                os.remove(prova)
    return migliore


def converti(tutto=False, dice=print):
    """Aggiorna le WebP. Torna il numero di file scritti."""
    Image = _pillow()
    os.makedirs(USCITA, exist_ok=True)

    da_fare, visti = [], {}
    for cartella in SORGENTI:
        if not os.path.isdir(cartella):
            continue
        for nome in sorted(os.listdir(cartella)):
            if not nome.lower().endswith(".png"):
                continue
            sorgente = os.path.join(cartella, nome)
            if nome in visti:
                raise SystemExit(
                    "Due sorgenti con lo stesso nome, %s e %s: la cartella di uscita e'\n"
                    "piatta, quindi una sovrascriverebbe l'altra. Rinominarne una."
                    % (visti[nome], sorgente))
            visti[nome] = sorgente
            destinazione = os.path.join(USCITA, os.path.splitext(nome)[0] + ".webp")
            if (tutto or not os.path.exists(destinazione)
                    or os.path.getmtime(sorgente) > os.path.getmtime(destinazione)):
                da_fare.append((sorgente, destinazione))

    if not da_fare:
        dice("   WebP gia' aggiornate: %d file in %s" % (len(visti), USCITA.replace(os.sep, "/")))
        return 0

    prima = dopo = 0
    for sorgente, destinazione in da_fare:
        peso, opzioni = _converti_file(Image, sorgente, destinazione)
        prima += os.path.getsize(sorgente)
        dopo += peso
    dice("   WebP: %d file convertiti in %s, da %d a %d kB (%+.0f%%)"
         % (len(da_fare), USCITA.replace(os.sep, "/"), prima // 1024, dopo // 1024,
            100 * (dopo - prima) / prima if prima else 0))
    return len(da_fare)


def main():
    tutto = "--tutto" in sys.argv[1:]
    scritti = converti(tutto=tutto)
    rimasti = len([n for n in os.listdir(USCITA) if n.endswith(".webp")]) if os.path.isdir(USCITA) else 0
    print("   in tutto %d figure WebP pronte per il blog" % rimasti)
    return 0 if (scritti or rimasti) else 1


if __name__ == "__main__":
    sys.exit(main())
