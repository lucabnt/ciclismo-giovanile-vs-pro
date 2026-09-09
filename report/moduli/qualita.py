"""
Non solo se si arriva, ma fino a dove.

DA DOVE ARRIVANO I NUMERI
    Da `R/22_qualita_carriera.R`, che copre gli STEP 22 e 23 della guida.

PERCHE' LE DUE ANALISI STANNO IN UNA SEZIONE SOLA
    Il modello ordinale e quello a stadi rispondono alla stessa domanda da due lati, e
    separarli renderebbe incomprensibile la cosa piu' interessante che dicono — che sono
    d'accordo su un punto e apparentemente in disaccordo su un altro. Il disaccordo e'
    solo apparente, ed e' il risultato principale della sezione.

IL PUNTO DA NON SBAGLIARE NELLA LETTURA
    Le soglie cumulate («almeno top 500») confrontano chi ha raggiunto quel livello con
    **tutti gli altri**, professionisti mancati compresi. Gli stadi condizionati
    («top 500 fra i professionisti») confrontano solo dentro il gruppo che ce l'ha gia'
    fatta. I primi ereditano il segnale del primo gradino, i secondi no — ed e' per
    questo che dicono cose diverse.
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

COMANDO = "Rscript R/22_qualita_carriera.R"


def calcola():
    lt = Lettura()
    curve = lt.tabella("qualita", "curve")
    if not curve:
        print("   qualita: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    x = [r[0] for r in curve["righe"]]
    serie = [("professionista", [r[1] for r in curve["righe"]]),
             ("almeno top 500", [r[2] for r in curve["righe"]]),
             ("top 100 mondiale", [r[3] for r in curve["righe"]])]

    gr.stile()
    with gr.figura("Dove si arriva, partendo da un dato percentile") as (fig, ax):
        for i, (nome, y) in enumerate(serie):
            ax.plot(x, y, color=gr.COLORI[i], linewidth=2, label=nome)
        ax.set_xlabel("percentile nella classifica Under 19, secondo anno")
        ax.set_ylabel("probabilita' (%, scala logaritmica)")
        ax.set_yscale("log")
        ax.set_yticks([0.01, 0.1, 1, 10, 100])
        ax.get_yaxis().set_major_formatter(
            gr.stile().matplotlib.ticker.FuncFormatter(
                lambda v, _: ("%g" % v).replace(".", ",")))
        # Sotto il centesimo di punto percentuale il grafico non dice piu' niente di
        # utile e la scala logaritmica sprecherebbe meta' dell'altezza.
        ax.set_ylim(0.01, 100)
        ax.legend(loc="upper left", fontsize=9)
    percorso = gr.salva("qualita_catena")

    with Archivio("qualita", pulisci=False) as ar:
        ar.figura("catena", percorso,
                  didascalia="Le tre curve restano quasi parallele: salendo di "
                             "percentile aumentano insieme, il che vuol dire che il "
                             "rendimento giovanile sposta la probabilita' di entrare, "
                             "non quella di andare lontano una volta entrati.")


def _p(x):
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, 3)


def rendi(lt):
    v = lt.valori("qualita")
    livelli = lt.tabella("qualita", "livelli")
    soglie = lt.tabella("qualita", "soglie")
    stadi = lt.tabella("qualita", "stadi")
    comp = lt.tabella("qualita", "composte")

    p = [md.sezione("Non solo se si arriva, ma fino a dove")]

    if not livelli:
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
        "Fin qui il professionismo e' stato trattato come una porta: dentro o fuori. Ma "
        "fra i professionisti c'e' chi corre qualche stagione in una squadra di seconda "
        "divisione e chi entra fra i primi cento al mondo. La domanda di questa sezione "
        "e' se il rendimento giovanile dica qualcosa anche su **quanto lontano** si "
        "arriva."))

    p.append(md.tabella(livelli["colonne"], livelli["righe"], n=v.get("n"),
                        nota=livelli["nota"], colonne_conteggio=(1,)))

    p.append(md.metodo(
        "Regressione ordinale e odds proporzionali",
        "I quattro livelli non sono categorie qualsiasi: sono gradini di un'unica scala. "
        "La regressione ordinale ne tiene conto e stima **un solo coefficiente** per "
        "tutta la scala, invece di uno per ogni confronto. Usa tutta l'informazione e "
        "non spezza il campione.\n\n"
        "Il prezzo e' un'assunzione: che l'effetto del predittore sia lo stesso su ogni "
        "gradino — gli **odds proporzionali**. Si controlla stimando le soglie una per "
        "una e confrontando i coefficienti. Se si somigliano, il coefficiente unico e' "
        "un buon riassunto; se divergono, e' una media che nasconde andamenti diversi.\n\n"
        "Il confronto fra le soglie sostituisce il **test di Brant**, che non e' stato "
        "eseguito: con tre soglie e pochi eventi ai gradini alti un test formale avrebbe "
        "poca potenza, e guardare i coefficienti uno accanto all'altro dice la stessa "
        "cosa in modo piu' leggibile. Vale come ispezione, non come verifica formale.\n\n"
        "Il predittore e' il percentile in Under 19 secondo anno. La guida propone di "
        "usare anche l'Under 23, ma in quelle coorti la classifica Under 23 contiene "
        "poche centinaia di atleti gia' selezionatissimi: chiederli entrambi "
        "reintrodurrebbe proprio il problema di selezione che il modello ordinale serve "
        "a evitare.",
        [("Regressione ordinale", W + "Ordinal_regression"),
         ("Odds proporzionali", W + "Ordered_logit"),
         ("Odds ratio", W + "Odds_ratio")]))

    ordinale = v.get("ordinale")
    if ordinale:
        p.append(md.paragrafo(
            "",
            "Il modello ordinale dice che **dieci punti di percentile in Under 19 "
            "moltiplicano per %s** l'odds di salire di livello sulla scala (IC 95%% "
            "%s-%s, p %s)."
            % (md.num(ordinale["or"], 2), md.num(ordinale["lo"], 2),
               md.num(ordinale["hi"], 2), _p(ordinale["p"]))))

    if soglie:
        righe_s = [[r[0], r[1], md.num(r[2], 2),
                    "%s-%s" % (md.num(r[3], 2), md.num(r[4], 2))]
                   for r in soglie["righe"]]
        p.append(md.tabella(["soglia", "casi", "odds ratio", "IC 95%"], righe_s,
                            nota=soglie["nota"], colonne_conteggio=(1,)))

        div = v.get("divario_soglie")
        if div:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    div < 2,
                    "i coefficienti delle tre soglie cumulate restano dello stesso "
                    "ordine di grandezza",
                    "I tre coefficienti crescono salendo di soglia, ma restano dello "
                    "stesso ordine — il piu' grande e' %s volte il piu' piccolo — e gli "
                    "intervalli si sovrappongono ampiamente. L'assunzione di odds "
                    "proporzionali regge abbastanza da poter riportare un coefficiente "
                    "unico, tenendo presente che la soglia piu' alta poggia su quindici "
                    "casi." % md.num(div, 2))))

    # --- gli stadi condizionati: qui sta il risultato -------------------------
    if stadi:
        p.append(md.sezione("Dove il rendimento giovanile smette di contare", 3))
        p.append(md.paragrafo(
            "Le soglie qui sopra confrontano chi ha raggiunto un livello con **tutti gli "
            "altri**, professionisti mancati compresi: ereditano quindi il segnale del "
            "primo gradino. Per sapere se il rendimento giovanile conti anche *dentro* "
            "il gruppo di chi ce l'ha fatta bisogna chiedere un'altra cosa — fra i "
            "professionisti, chi arriva al top 500? E fra questi, chi al top 100?"))
        righe_st = [[r[0], r[1], r[2],
                     "—" if r[3] is None else md.num(r[3], 2),
                     "—" if r[4] is None else "%s-%s" % (md.num(r[4], 2), md.num(r[5], 2))]
                    for r in stadi["righe"]]
        p.append(md.tabella(
            ["passaggio", "chi ci prova", "chi ci riesce", "odds ratio", "IC 95%"],
            righe_st, nota=stadi["nota"], colonne_conteggio=(1, 2)))

        primo = stadi["righe"][0]
        dopo = [r for r in stadi["righe"][1:] if r[3] is not None]
        if dopo and primo[3]:
            non_sig = [r for r in dopo if r[4] is not None and r[4] <= 1 <= r[5]]
            p.append(md.paragrafo(
                "",
                md.afferma(
                    len(non_sig) == len(dopo),
                    "negli stadi successivi al professionismo gli intervalli di "
                    "confidenza del rendimento giovanile comprendono l'uno",
                    "**Il rendimento in Under 19 predice l'ingresso e quasi nulla di "
                    "cio' che viene dopo.** Per diventare professionista l'odds ratio e' "
                    "%s; per arrivare al top 500 **fra i professionisti** scende a %s, e "
                    "per il top 100 fra i top 500 a %s. In entrambi i casi l'intervallo "
                    "di confidenza comprende l'uno: su questi numeri non si distingue "
                    "dal caso."
                    % (md.num(primo[3], 2), md.num(dopo[0][3], 2),
                       md.num(dopo[1][3], 2) if len(dopo) > 1 else "—")),
                "",
                "E' il risultato piu' interessante della sezione, e conviene dirlo con "
                "le parole giuste. Non significa che fra i professionisti il talento non "
                "conti, e nemmeno che la soglia sia una sola: la sezione «Da quale porta "
                "si entra» mostra che l'ingresso avviene per due vie con esiti molto "
                "diversi. Significa che **la classifica giovanile italiana non lo misura "
                "piu'**. A diciotto anni distingue bene chi entrera' nel professionismo "
                "da chi no; una volta dentro, quello che decide se si arriva fra i primi "
                "cento al mondo e' qualcosa che quella classifica non ha registrato."))

    if comp:
        p.append(md.sezione("La catena delle probabilita'", 3))
        righe_c = [[md.conta(r[0]) + "°", md.num(r[1], 1) + "%",
                    md.num(r[2], 1) + "%", md.num(r[3], 2) + "%"]
                   for r in comp["righe"]]
        p.append(md.tabella(
            ["percentile in Under 19", "professionista", "almeno top 500", "top 100"],
            righe_c, nota=comp["nota"]))

        alto = comp["righe"][-1]
        medio = comp["righe"][0]
        p.append(md.paragrafo(
            "",
            "In una frase sola: **un atleta al %s° percentile della classifica Under 19 "
            "ha circa il %s%% di probabilita' di diventare professionista e il %s%% di "
            "arrivare almeno nel top 500 mondiale**; uno al %s° percentile ha "
            "rispettivamente %s%% e %s%%."
            % (md.conta(alto[0]), md.num(alto[1], 0), md.num(alto[2], 0),
               md.conta(medio[0]), md.num(medio[1], 1), md.num(medio[2], 1))))

    f = lt.figura("qualita", "catena")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    cond = v.get("condizionato")
    if cond:
        p.append(md.paragrafo(
            "",
            "> **Il modello con anche l'Under 23, per completezza.** Sui %s atleti "
            "presenti in entrambe le classifiche, l'Under 19 vale %s e l'Under 23 %s. "
            "Sono valori molto piu' bassi di quelli dell'analisi principale, e non "
            "perche' il rendimento conti meno: quel sottocampione e' fatto di "
            "sopravvissuti fra loro simili, e su un gruppo gia' scremato ogni predittore "
            "sembra piu' debole. E' la ragione per cui questo modello resta secondario."
            % (md.conta(cond["n"]), md.num(cond["u19"], 2), md.num(cond["u23"], 2))))

    p.append(md.paragrafo(
        "",
        "> **Un limite da tenere presente.** Il livello piu' alto poggia su quindici "
        "atleti. Bastano due o tre casi in piu' o in meno per spostare i coefficienti "
        "dell'ultimo gradino, e infatti i suoi intervalli di confidenza sono larghissimi. "
        "Le conclusioni robuste di questa sezione riguardano il primo gradino; sugli "
        "altri si puo' dire soprattutto che **non si vede** un effetto, che non e' la "
        "stessa cosa che dire che non c'e'."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
