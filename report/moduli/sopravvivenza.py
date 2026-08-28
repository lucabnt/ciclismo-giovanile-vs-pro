"""
Quando si diventa professionisti.

DA DOVE ARRIVANO I NUMERI
    Da `R/20_sopravvivenza.R`. Qui si legge dall'archivio e si scrive il testo; l'unico
    calcolo che resta a Python e' il disegno della figura.

PERCHE' QUESTA SEZIONE STA IN FONDO E NON ALL'INIZIO
    Risponde a una domanda diversa da tutte le altre. Le sezioni precedenti chiedono
    «chi arrivera'»; questa chiede «quando», e la risposta e' una curva sull'eta' invece
    che un numero. E' anche l'unica che usa le coorti recenti, quelle che non hanno
    ancora finito la finestra dei venticinque anni: contribuiscono le stagioni gia'
    osservate e poi escono, il che quasi raddoppia gli eventi disponibili.

LE DUE CURVE DA NON CONFONDERE
    Il rischio **grezzo** e' quanti passaggi al professionismo avvengono per ogni mille
    atleti ancora in gioco a una data eta'. Comprende tutti, anche chi da anni non
    compare in classifica.

    Il rischio **stimato** e' quello di un atleta che in classifica c'e', con rendimento
    medio. E' molto piu' alto, e la differenza fra le due curve non e' un errore: e'
    esattamente quanto pesa l'essere ancora nel gruppo osservato.
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

COMANDO = "Rscript R/20_sopravvivenza.R"


def calcola():
    lt = Lettura()
    grezzo = lt.tabella("sopravvivenza", "hazard_grezzo")
    curva = lt.tabella("sopravvivenza", "curva")
    if not grezzo or not curva:
        print("   sopravvivenza: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    eta_g = [r[0] for r in grezzo["righe"]]
    h_g = [r[3] for r in grezzo["righe"]]
    eta_c = [r[0] for r in curva["righe"]]
    h_c = [r[1] for r in curva["righe"]]
    lo = [r[2] for r in curva["righe"]]
    hi = [r[3] for r in curva["righe"]]

    gr.stile()
    with gr.figura("Il rischio di passare professionista, per eta'") as (fig, ax):
        ax.fill_between(eta_c, lo, hi, color=gr.COLORI[0], alpha=0.15, linewidth=0)
        ax.plot(eta_c, h_c, color=gr.COLORI[0], linewidth=2, marker="o", markersize=6,
                label="chi e' in classifica, con rendimento medio")
        ax.plot(eta_g, h_g, color=gr.COLORI[1], linewidth=1.8, marker="s", markersize=5,
                linestyle="--", label="tutti gli atleti ancora in gioco")
        ax.set_xlabel("eta' (anni)")
        ax.set_ylabel("passaggi al professionismo per mille")
        ax.set_xticks(eta_c)
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(bottom=0)
    percorso = gr.salva("sopravvivenza_hazard")

    with Archivio("sopravvivenza", pulisci=False) as ar:
        ar.figura("hazard", percorso,
                  didascalia="La distanza fra le due curve e' quanto pesa l'essere "
                             "ancora nella classifica nazionale: a parita' di eta', "
                             "chi c'e' ha un rischio molte volte maggiore.")


def _p(x):
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, 3)


def rendi(lt):
    v = lt.valori("sopravvivenza")
    grezzo = lt.tabella("sopravvivenza", "hazard_grezzo")
    coeff = lt.tabella("sopravvivenza", "coefficienti")

    p = [md.sezione("Quando si diventa professionisti")]

    if not grezzo:
        p.append(md.paragrafo(
            "*Questa sezione richiede i modelli in R, che non risultano ancora "
            "eseguiti. Per produrla:*",
            "",
            "```",
            "python scripts/08_prepara_modelli.py",
            COMANDO,
            "```"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    eta = v.get("eta_finestra", [None, None])
    p.append(md.paragrafo(
        "Tutte le sezioni precedenti chiedono **chi** arrivera' al professionismo. "
        "Questa chiede **quando**, e la risposta e' una curva sull'eta' invece che un "
        "numero. E' anche l'unica che usa le coorti recenti: chi non ha ancora "
        "completato la finestra dei venticinque anni contribuisce le stagioni gia' "
        "osservate e poi esce dal conteggio, e questo porta gli eventi utilizzabili da "
        "77 a **%s**."
        % md.conta(v.get("n_eventi"))))

    p.append(md.metodo(
        "Modello di sopravvivenza a tempo discreto",
        "I dati si riorganizzano in **stagioni a rischio**: una riga per ogni atleta e "
        "per ogni stagione in cui poteva diventare professionista e non lo era ancora. "
        "Chi lo diventa esce dal rischio, chi non ha ancora finito la finestra viene "
        "**censurato** — cioe' contribuisce le stagioni osservate senza che il silenzio "
        "successivo venga scambiato per un no.\n\n"
        "Su questa tabella si stima la probabilita' che l'evento accada in una data "
        "stagione. Il legame usato e' il **complementare log-log**, che discende da un "
        "processo continuo osservato a intervalli: la decisione di ingaggiare un "
        "corridore matura in un momento qualunque dell'anno, noi la vediamo per "
        "stagione. Il suo coefficiente si legge come rapporto fra rischi.\n\n"
        "Gli errori standard sono **raggruppati per atleta**: le stagioni dello stesso "
        "corridore non sono osservazioni indipendenti, e ignorarlo restringerebbe gli "
        "intervalli di confidenza di una quantita' arbitraria.\n\n"
        "Il predittore e' il percentile della stagione **precedente**. Usare quello "
        "della stagione in corso significherebbe spiegare una decisione con "
        "informazione che al momento di prenderla non esisteva ancora.",
        [("Analisi di sopravvivenza", W + "Survival_analysis"),
         ("Censura", W + "Censoring_(statistics)"),
         ("Legame complementare log-log", W + "Generalized_linear_model#Link_function")]))

    righe = [[r[0], r[1], r[2], md.num(r[3], 1)] for r in grezzo["righe"]]
    p.append(md.tabella(
        ["eta'", "atleti a rischio", "passaggi al professionismo", "per mille"],
        righe, nota=grezzo["nota"], colonne_conteggio=(1, 2)))

    if eta[0]:
        p.append(md.paragrafo(
            "",
            "**Prima dei %s anni la casella e' vuota, e non per caso**: il regolamento "
            "internazionale non permette di correre da professionista prima. Il rischio "
            "poi cresce, e il massimo osservato cade a %s anni."
            % (md.conta(eta[0]),
               md.conta(max(grezzo["righe"], key=lambda r: r[3])[0]))))

    fuori = v.get("eventi_fuori_finestra")
    if fuori:
        p.append(md.paragrafo(
            "",
            "*La finestra si ferma a %s anni perche' li' finisce il predittore: il "
            "ranking giovanile arriva all'Under 23 e oltre non esiste piu' alcuna "
            "classifica nazionale da cui misurare il rendimento. I %s passaggi al "
            "professionismo avvenuti dopo restano fuori dal modello, ed e' meglio "
            "dichiararlo che includerli trattando un dato mancante come un'assenza.*"
            % (md.conta(eta[1]), md.conta(fuori))))

    if coeff:
        p.append(md.sezione("Cosa sposta il rischio", 3))
        righe_c = [[r[0], md.num(r[1], 3),
                    "%s-%s" % (md.num(r[2], 3), md.num(r[3], 3)), _p(r[4])]
                   for r in coeff["righe"]]
        p.append(md.tabella(
            ["variabile", "rapporto fra rischi", "IC 95%", "p"],
            righe_c, n=v.get("n_righe"), nota=coeff["nota"]))

        assente = next((r for r in coeff["righe"] if "assente" in r[0]), None)
        pct = next((r for r in coeff["righe"] if "percentile" in r[0]), None)
        if assente and pct:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    assente[1] < 0.2,
                    "essere assenti dalla classifica l'anno prima riduce il rischio di "
                    "passare professionista di piu' di cinque volte",
                    "Il coefficiente che domina non e' il rendimento: e' **l'esserci**. "
                    "Chi non era in classifica l'anno precedente ha un rischio pari a "
                    "%s di chi c'era, cioe' circa **%s volte piu' basso**. Fra chi c'e', "
                    "dieci punti di percentile in piu' moltiplicano il rischio per %s."
                    % (md.num(assente[1], 3), md.conta(round(1 / assente[1])),
                       md.num(pct[1], 2))),
                "",
                "Va letto con la cautela che merita. Le sezioni precedenti hanno "
                "mostrato che sparire dalla classifica significa smettere di fare punti, "
                "non smettere di correre, e che al cambio di categoria il posto in lista "
                "sparisce per ragioni che riguardano la lunghezza della classifica. "
                "Questo coefficiente misura quindi in buona parte **quanto e' difficile "
                "rientrare** una volta usciti dal gruppo osservato, non quanto sia "
                "compromessa la carriera di chi esce."))

        quota = v.get("quota_assenti")
        if quota:
            p.append(md.paragrafo(
                "",
                "Un dato di contesto che rende la cifra meno sorprendente: su cento "
                "stagioni a rischio, in %s casi l'atleta **non** era in classifica l'anno "
                "prima. La classifica Under 23 ha poche decine di posti, quindi "
                "l'assenza e' la condizione normale e non l'eccezione."
                % md.num(quota, 0)))

    f = lt.figura("sopravvivenza", "hazard")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    cum = v.get("cumulate")
    if cum:
        p.append(md.paragrafo(
            "",
            "Messo in forma leggibile: per un atleta che resta in classifica **ogni** "
            "stagione fino ai %s anni, la probabilita' di arrivare al professionismo "
            "vale **%s%%** con un rendimento nella media della classifica, sale a "
            "**%s%%** con %s punti di percentile in piu' e scende a **%s%%** con %s "
            "punti in meno."
            % (md.conta(eta[1]), md.num(cum["medio"], 1), md.num(cum["alto"], 1),
               md.conta(cum["scarto"]), md.num(cum["basso"], 1),
               md.conta(cum["scarto"])),
            "",
            "> **Attenzione al condizionamento.** Queste probabilita' valgono per chi "
            "resta in classifica tutti gli anni, che e' una minoranza molto selezionata: "
            "non sono la probabilita' di un ragazzo qualunque che comincia a correre. "
            "Quella resta quella dell'imbuto, di gran lunga piu' bassa."))

    coorte = next((r for r in coeff["righe"] if "nascita" in r[0]), None) if coeff else None
    if coorte:
        p.append(md.paragrafo(
            "",
            md.afferma(
                coorte[4] > 0.05,
                "l'anno di nascita non sposta il rischio di passare professionista",
                "> **Un controllo che vale la pena riportare.** L'anno di nascita non "
                "sposta il rischio (rapporto %s, p = %s). Le tredici coorti qui incluse "
                "si comportano allo stesso modo, il che vuol dire che i risultati non "
                "dipendono da quale periodo si guardi — ed e' la stessa conclusione a "
                "cui era arrivato, per un'altra strada, il modello per singola categoria."
                % (md.num(coorte[1], 3), _p(coorte[4])))))

    return (chr(10) * 2).join(x.strip() for x in p if x)
