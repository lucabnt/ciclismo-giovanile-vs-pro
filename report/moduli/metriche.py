"""
Cosa succede se il ranking si usa davvero per selezionare.

DA DOVE ARRIVANO I NUMERI
    Da `R/19_metriche.R`. Qui si legge dall'archivio e si scrive il testo.

PERCHE' QUESTA SEZIONE ESISTE
    Un'AUC di 0,89 sembra ottima, e detta cosi' autorizza chiunque a concludere che a
    diciannove anni si capisce chi ce la fara'. Il valore predittivo positivo dice
    l'altra meta': con un esito che riguarda meno del 3% della coorte, anche un
    ordinamento quasi perfetto seleziona in maggioranza persone che non diventeranno
    professioniste. E' il numero che quasi nessuno riporta, ed e' quello che decide se
    una soglia si puo' usare per prendere decisioni su dei ragazzi.

LA SCELTA DELLE SOGLIE
    Oltre alla soglia di Youden, che e' il riferimento statistico, si riportano il
    migliore 10% e il migliore 25% della cella: sono soglie di capienza, cioe' quelle
    che una societa' userebbe davvero, e si leggono senza sapere cosa sia Youden.
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

COMANDO = "Rscript R/19_metriche.R"
CRITERIO_GRAFICO = "migliore 10%"


def calcola():
    lt = Lettura()
    t = lt.tabella("metriche", "soglie")
    if not t:
        print("   metriche: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    righe = [r for r in t["righe"] if r[1] == CRITERIO_GRAFICO]
    if not righe:
        print("   metriche: nessuna riga con criterio '%s'" % CRITERIO_GRAFICO)
        return
    celle = [r[0] for r in righe]
    sens = [r[6] for r in righe]
    vpp = [r[8] for r in righe]

    plt = gr.stile()
    x = range(len(celle))
    larghezza = 0.38
    with gr.figura("Selezionando il migliore 10% di ogni categoria") as (fig, ax):
        ax.bar([i - larghezza / 2 for i in x], sens, larghezza,
               color=gr.COLORI[0], label="futuri professionisti intercettati")
        ax.bar([i + larghezza / 2 for i in x], vpp, larghezza,
               color=gr.COLORI[1], label="selezionati che ce la faranno")
        ax.set_xticks(list(x))
        ax.set_xticklabels(celle)
        ax.set_ylabel("percentuale")
        ax.set_ylim(0, 100)
        ax.legend(loc="upper left")
        ax.grid(axis="x", visible=False)
    percorso = gr.salva("metriche_soglie")
    plt.close("all")

    with Archivio("metriche", pulisci=False) as ar:
        ar.figura("soglie", percorso,
                  didascalia="Le due barre rispondono a due domande diverse. La prima: "
                             "quanti dei futuri professionisti finiscono nella "
                             "selezione. La seconda: quanti dei selezionati lo "
                             "diventeranno. Salgono insieme solo in apparenza.")


def rendi(lt):
    v = lt.valori("metriche")
    t = lt.tabella("metriche", "soglie")

    p = [md.sezione("Se il ranking si usasse per selezionare")]

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
        "Fin qui si e' misurato quanto il rendimento giovanile predice. Questa sezione "
        "traduce la misura in cio' che una societa' si trova davanti: se si guardassero "
        "solo gli atleti sopra una certa soglia, **quanti futuri professionisti si "
        "intercetterebbero, e quanti dei selezionati non lo diventeranno**."))

    p.append(md.metodo(
        "Sensibilita', specificita' e valori predittivi",
        "Fissata una soglia, ogni atleta cade in una di quattro caselle: selezionato e "
        "diventato professionista, selezionato e no, non selezionato e diventato "
        "professionista, non selezionato e no.\n\n"
        "La **sensibilita'** e' la quota di futuri professionisti che finisce dentro la "
        "selezione: quanti non ne perdo. Il **valore predittivo positivo** e' la quota "
        "di selezionati che diventera' professionista: quanti ne prendo a vuoto.\n\n"
        "Il **valore predittivo negativo** e' la quarta casella letta dall'altra "
        "parte: fra gli scartati, quanti davvero non sarebbero arrivati. Con un esito "
        "raro e' sempre altissimo, e proprio per questo non va usato come prova che la "
        "selezione funzioni: dire che il 99% degli scartati non ce l'avrebbe fatta e' "
        "quasi una tautologia, visto che non ce la fa il 97% di chiunque. Serve pero' "
        "a rendere leggibile l'altra meta' del compromesso, ed e' la metrica che "
        "nessuno studio di questo campo riporta.\n\n"
        "I due numeri non sono simmetrici, e la differenza dipende da quanto l'esito e' "
        "raro. Se i professionisti sono il 3% della coorte, anche una selezione molto "
        "buona resta composta in gran parte da persone che non lo diventeranno: e' "
        "aritmetica della base, non un difetto del criterio. E' la stessa ragione per "
        "cui uno screening accurato su una malattia rara produce molti falsi allarmi.\n\n"
        "La **soglia di Youden** e' quella che massimizza sensibilita' + specificita' - "
        "1. Serve da riferimento, ma le soglie di capienza — il migliore 10%, il "
        "migliore 25% — sono quelle che corrispondono a una decisione reale.",
        [("Sensibilita' e specificita'", W + "Sensitivity_and_specificity"),
         ("Valore predittivo positivo", W + "Positive_and_negative_predictive_values"),
         ("Indice di Youden", W + "Youden%27s_J_statistic")]))

    righe = [[r[0], r[1], md.num(r[2], 1), r[3], r[4], r[5],
              md.num(r[6], 0) + "%", md.num(r[8], 0) + "%", md.num(r[9], 1) + "%"]
             for r in t["righe"]]
    p.append(md.tabella(
        ["cella", "criterio", "soglia", "selezionati", "di cui pro", "a vuoto",
         "intercettati", "successo dei selezionati", "scartati che non arrivano"],
        righe, nota=t["nota"], colonne_conteggio=(3, 4, 5)))

    chiave = v.get("frase_chiave")
    if chiave:
        p.append(md.paragrafo(
            "",
            "Il caso migliore e' **%s**: selezionando il 10%% piu' forte di quella "
            "categoria — %s atleti su %s — si intercetta il **%s%% dei futuri "
            "professionisti**, ma il **%s%% dei selezionati non lo diventera'**. "
            "Entrambe le meta' della frase sono vere, e citarne una sola e' il modo "
            "piu' comune di usare male questi dati."
            % (chiave["cella"], md.conta(chiave["selezionati"]), md.conta(chiave["n"]),
               md.num(chiave["sensibilita"], 0),
               md.num(100 - chiave["vpp"], 0))))

    f = lt.figura("metriche", "soglie")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.paragrafo(
        "",
        "> **Attenzione a leggere la colonna del successo dei selezionati come una "
        "misura di bravura del criterio.** Cresce con l'eta' soprattutto perche' "
        "cresce la quota di professionisti nella cella: in Under 23 chi e' ancora in "
        "classifica ha gia' superato tre selezioni. Un criterio applicato a un gruppo "
        "gia' scremato sembra piu' preciso senza esserlo di piu'."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
