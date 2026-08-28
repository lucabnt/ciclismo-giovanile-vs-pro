"""
Il rendimento a una data eta', misurato con un modello.

DA DOVE ARRIVANO I NUMERI
    Da `R/16_univariati.R`. Questo file non stima nulla: legge dall'archivio e scrive il
    testo. E' la stessa separazione degli altri moduli, con una differenza — qui il
    calcolo sta in un altro linguaggio.

    `calcola()` quindi non calcola i modelli: disegna soltanto la figura, che e'
    presentazione, e la aggiunge ai risultati che R ha gia' scritto senza cancellarli.

SE R NON E' STATO ESEGUITO
    La sezione non sparisce e non si inventa numeri: dice cosa manca e con quale comando
    ottenerlo. Il documento resta rigenerabile anche su una macchina senza R, ed e'
    evidente che quella parte non c'e'.

PERCHE' UN GRAFICO A INTERVALLI E NON UNA CURVA
    L'odds ratio di una cella non e' un punto di una funzione continua dell'eta': ogni
    cella e' un modello a se', su una popolazione diversa. Unire i punti con una linea
    suggerirebbe una traiettoria che i dati non contengono. Si mostrano quindi stime
    separate con il proprio intervallo di confidenza, che e' la forma in cui vanno
    lette.
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_risultati import Archivio, Lettura        # noqa: E402
import lib_markdown as md                          # noqa: E402
import lib_grafici as gr                           # noqa: E402

W = "https://en.wikipedia.org/wiki/"

COMANDO = "Rscript R/16_univariati.R"


def calcola():
    """Disegna la figura a partire dai risultati che R ha gia' scritto."""
    lt = Lettura()
    t = lt.tabella("univariati", "per_cella")
    if not t:
        print("   univariati: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    celle = [r[0] for r in t["righe"]]
    or_ = [r[4] for r in t["righe"]]
    basso = [r[5] for r in t["righe"]]
    alto = [r[6] for r in t["righe"]]

    plt = gr.stile()
    y = list(range(len(celle)))[::-1]
    with gr.figura("Quanto pesano dieci punti di percentile", altezza=3.4) as (fig, ax):
        for i, yy in enumerate(y):
            ax.plot([basso[i], alto[i]], [yy, yy], color=gr.GRIGIO, linewidth=1.4,
                    solid_capstyle="round", zorder=1)
            ax.plot([or_[i]], [yy], marker="o", markersize=7, color=gr.COLORI[0],
                    zorder=2)
        gr.linea_riferimento(ax, 1.0, "nessun effetto", verticale=True)
        ax.set_yticks(y)
        ax.set_yticklabels(celle)
        ax.set_xlabel("odds ratio per 10 punti di percentile (scala logaritmica)")
        ax.set_xscale("log")
        ax.set_xticks([1, 1.5, 2, 3])
        ax.get_xaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
        ax.grid(axis="y", visible=False)
        # Un po' d'aria sopra e sotto: senza, la prima riga finisce sotto
        # l'etichetta della linea di riferimento.
        ax.margins(y=0.14)
    percorso = gr.salva("univariati_or")

    # `pulisci=False`: i valori e la tabella li ha scritti R, e vanno lasciati stare.
    with Archivio("univariati", pulisci=False) as ar:
        ar.figura("or", percorso,
                  didascalia="Ogni cella e' un modello a se'. Gli intervalli sono al "
                             "95% e la scala e' logaritmica, perche' un odds ratio si "
                             "legge in rapporti e non in differenze.")


def _p(x):
    """Un p-value come si legge in un testo, non come lo stampa il calcolatore."""
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, 3)


def rendi(lt):
    v = lt.valori("univariati")
    t = lt.tabella("univariati", "per_cella")

    p = [md.sezione("Quanto vale il rendimento, misurato")]

    if not t:
        p.append(md.paragrafo(
            "*Questa sezione richiede i modelli in R, che non risultano ancora "
            "eseguiti. Per produrla:*",
            "",
            "```",
            "python scripts/08_prepara_modelli.py",
            COMANDO,
            "```"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "La descrittiva ha mostrato che chi e' arrivato al professionismo andava gia' "
        "meglio degli altri. Un modello permette di dire **di quanto**: a quanto "
        "ammonta il vantaggio di dieci punti di percentile, e con quale incertezza."))

    p.append(md.metodo(
        "Regressione logistica con correzione di Firth",
        "La regressione logistica stima come cambia la probabilita' di un esito "
        "binario — qui diventare professionista — al variare di un predittore. Il "
        "risultato si legge come odds ratio: quanto si moltiplica il rapporto fra "
        "probabilita' di riuscire e di non riuscire per ogni aumento del predittore.\n\n"
        "La correzione di Firth serve perche' l'esito e' raro: i professionisti sono "
        "meno del 3%% del campione. Con eventi rari la stima ordinaria e' distorta verso "
        "l'alto, e quando un gruppo e' perfettamente separato dall'altro non converge "
        "affatto. La penalizzazione di Jeffreys mantiene le stime finite e riduce la "
        "distorsione di piccolo campione.\n\n"
        "Qui l'odds ratio e' riferito a **%s punti di percentile**: un punto solo e' una "
        "differenza che nessuno percepisce, dieci punti sono il salto fra un "
        "piazzamento e quello successivo."
        % md.num(v.get("passo", 10), 0),
        [("Regressione logistica", W + "Logistic_regression"),
         ("Correzione di Firth", W + "Logistic_regression#Firth_logistic_regression"),
         ("Odds ratio", W + "Odds_ratio")]))

    # La tabella da mostrare si compone qui: R ha scritto numeri grezzi, la forma in cui
    # si leggono — quante cifre, come si scrive un intervallo — e' presentazione.
    righe = [[r[0], r[1], r[2], md.num(r[3], 1), md.num(r[4], 2),
              "%s-%s" % (md.num(r[5], 2), md.num(r[6], 2)), md.num(r[7], 3)]
             for r in t["righe"]]
    p.append(md.tabella(
        ["cella", "atleti", "professionisti", "% pro", "OR per 10 punti", "IC 95%", "AUC"],
        righe, nota=t["nota"], colonne_conteggio=(1, 2)))

    # L'andamento si descrive leggendo la tabella, non affermandolo: se un anno i dati
    # cambiassero e la crescita sparisse, il testo cambierebbe con loro.
    ors = [(r[0], r[4]) for r in t["righe"]]
    cella_max, or_max = max(ors, key=lambda x: x[1])
    cella_min, or_min = ors[0][0], ors[0][1]
    contro = [ors[i][0] for i in range(1, len(ors)) if ors[i][1] < ors[i - 1][1]]

    frase = ("Il peso del rendimento cresce con l'eta': si va da un odds ratio di %s in "
             "%s a %s in %s, cioe' un coefficiente %s volte piu' grande."
             % (md.num(or_min, 2), cella_min, md.num(or_max, 2), cella_max,
                md.num(or_max / or_min, 1)))
    if contro:
        frase += (" La crescita non e' pero' regolare: in %s il coefficiente scende "
                  "rispetto alla cella precedente. Non e' un'anomalia da spiegare con "
                  "la prestazione — e' composizione della popolazione, perche' a ogni "
                  "passaggio di categoria cambia chi resta nel gruppo confrontato."
                  % " e ".join(contro))
    p.append(md.paragrafo("", frase))

    sposta = v.get("spostamento_coorte")
    if sposta is not None:
        p.append(md.paragrafo(
            "",
            "I modelli sono aggiustati per anno di nascita, perche' le coorti piu' "
            "recenti hanno avuto meno tempo per arrivare al professionismo e senza quel "
            "termine la differenza di osservazione finirebbe attribuita al rendimento. "
            "L'aggiustamento sposta pochissimo: la differenza massima rispetto al "
            "modello grezzo e' %s sull'odds ratio. Il gradiente non e' un effetto di "
            "coorte." % ("inferiore a 0,01" if sposta < 0.01
                         else "di " + md.num(sposta, 2))))

    p.append(md.paragrafo(
        "",
        "Resta la trappola gia' segnalata nella descrittiva: **gli odds ratio di celle "
        "diverse non sono confrontabili come misure della stessa cosa**. Il modello in "
        "Under 23 e' stimato su chi e' sopravvissuto a tre selezioni, dove i "
        "professionisti sono oltre un terzo del gruppo; quello in Under 15 su tutti. "
        "Sono due domande diverse, non due misure della stessa domanda."))

    # La selezione all'ingresso dell'Under 23 ha anche un verso opposto, meno ovvio:
    # chi passa professionista prestissimo potrebbe non comparire affatto in quelle
    # classifiche. Va quantificato, non solo ipotizzato.
    mai, tot = v.get("pro_mai_in_u23"), v.get("pro_totali")
    if mai is not None and tot:
        p.append(md.paragrafo(
            "",
            md.afferma(
                mai / tot < 0.10,
                "i professionisti che non compaiono mai nelle classifiche Under 23 "
                "sono una quota trascurabile del totale",
                "C'e' un secondo verso della selezione, meno ovvio: un atleta molto "
                "forte puo' passare professionista subito dopo gli Juniores e non "
                "comparire mai nelle classifiche Under 23. Se fosse frequente, i "
                "modelli sull'Under 23 sarebbero stimati su un gruppo da cui i "
                "migliori sono usciti, e ne sottostimerebbero la predittivita'. "
                "Succede a **%s professionisti su %s**: %s hanno debuttato entro i "
                "vent'anni, ma quasi tutti erano comunque a punti nel ranking Under 23 "
                "di quella stagione, perche' in Italia si continua a correre da "
                "Under 23 anche con un contratto da professionista. La distorsione "
                "esiste, ma e' piccola."
                % (md.conta(mai), md.conta(tot), md.conta(v.get("pro_precoci"))))))

    # --- il tasso di professionismo per cella non e' un segnale ---------------
    amp = lt.tabella("univariati", "ampiezza_liste")
    anni = lt.tabella("univariati", "primo_contro_secondo")

    if amp:
        p.append(md.sezione("Perche' la colonna «% pro» non va letta come un segnale", 3))
        larghezze = {r[0]: r[1] for r in amp["righe"]}
        # I due esempi si pescano dalla tabella, non si riscrivono: se un anno i tassi
        # cambiassero, cambierebbe anche la frase che li cita.
        tassi = {r[0]: r[3] for r in t["righe"]}
        esempi = [c for c in ("U17", "U19")
                  if tassi.get(c + "y1") and tassi.get(c + "y2")]
        elenco = ", ".join(
            "%s%% contro %s%% in %s" % (md.num(tassi[c + "y1"], 1),
                                        md.num(tassi[c + "y2"], 1), c)
            for c in esempi)
        p.append(md.paragrafo(
            "Nella tabella qui sopra il tasso di professionismo e' piu' alto nelle celle "
            "del **primo** anno di categoria che in quelle del secondo: %s. Sembra "
            "suggerire che il primo anno selezioni meglio. Non e' cosi', ed e' un buon "
            "esempio di come un denominatore possa produrre un segnale che non c'e'."
            % elenco,
            "",
            "Le classifiche del primo anno sono **molto piu' corte**: in media %s "
            "classificati contro %s in Under 17, %s contro %s in Under 19. Entrare in "
            "una lista piu' corta e' piu' difficile, quindi chi c'e' e' gia' piu' "
            "selezionato, e un gruppo piu' selezionato contiene per forza una quota "
            "maggiore di futuri professionisti. Il tasso misura la selettivita' della "
            "lista, non la qualita' della previsione."
            % (md.conta(larghezze.get("U17y1")), md.conta(larghezze.get("U17y2")),
               md.conta(larghezze.get("U19y1")), md.conta(larghezze.get("U19y2")))))

    if anni:
        p.append(md.paragrafo(
            "",
            "La domanda giusta — *il primo anno predice meglio del secondo?* — si "
            "risponde solo confrontando le due misure **sulle stesse persone**: gli "
            "atleti presenti in entrambe le classifiche della categoria."))
        righe_a = [[r[0], r[1], r[2], md.num(r[3], 3), md.num(r[4], 3),
                    ("%+.3f" % r[5]).replace(".", ","), _p(r[6])]
                   for r in anni["righe"]]
        p.append(md.tabella(
            ["categoria", "atleti", "professionisti", "AUC primo anno",
             "AUC secondo anno", "differenza", "p (DeLong)"],
            righe_a, nota=anni["nota"], colonne_conteggio=(1, 2)))

        meglio = sum(1 for r in anni["righe"] if r[5] > 0)
        p.append(md.paragrafo(
            "",
            md.afferma(
                meglio == len(anni["righe"]),
                "a parita' di atleti, il secondo anno di categoria discrimina meglio "
                "del primo in tutte le categorie",
                "La risposta e' netta e va nella direzione opposta all'impressione: **il "
                "secondo anno discrimina meglio del primo in tutte le categorie**, e in "
                "Under 15 e Under 19 la differenza non e' attribuibile al caso. Ha "
                "senso: al secondo anno l'atleta corre contro i propri pari da un anno "
                "in piu', e la classifica ne misura il rendimento con meno rumore.")))

    f = lt.figura("univariati", "or")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    scarto = v.get("scarto_controllo")
    if scarto is not None:
        p.append(md.paragrafo(
            "",
            "> **Controllo.** L'AUC di questi modelli e quella ricavata dal delta di "
            "Cliff nella sezione descrittiva devono coincidere: misurano la stessa "
            "quantita' per due strade indipendenti. Lo scarto massimo osservato e' "
            "%s, cioe' arrotondamento. Se le due strade divergessero, uno dei due "
            "percorsi avrebbe un errore." % md.num(scarto, 4)))

    saltate = v.get("celle_saltate")
    if saltate:
        p.append(md.paragrafo(
            "",
            "*Celle escluse per numerosita' insufficiente: %s.*" % ", ".join(saltate)))

    return (chr(10) * 2).join(x.strip() for x in p if x)
