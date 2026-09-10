"""
Quanto aggiunge ogni categoria a quella precedente.

DA DOVE ARRIVANO I NUMERI
    Da `R/18_annidati.R`. Qui si legge dall'archivio e si scrive il testo; l'unico
    calcolo che resta a Python e' il disegno della figura.

LA FIGURA CENTRALE DELLO STUDIO
    L'asse x e' l'eta' a cui si osserva l'atleta, non il numero del modello: la domanda
    e' "quanto si sa, e a che eta' lo si sa". Le bande sono gli intervalli di confidenza
    dell'AUC, e la linea a 0,5 e' il tirare a indovinare.

    La curva parte dal modello con la sola coorte, che sta per definizione intorno a
    0,5: serve a mostrare da dove si comincia. Senza quel punto, il lettore non ha il
    riferimento per giudicare se 0,82 sia tanto o poco.

IL LIVELLO NON SI CONFRONTA, LA DIFFERENZA SI'
    Queste AUC sono calcolate su chi e' arrivato fino all'Under 23 restando in
    classifica, dove i professionisti sono quasi la meta'. Non vanno messe accanto a
    quelle dei modelli univariati, che girano su tutti. Il testo lo ripete dove serve,
    perche' e' l'errore di lettura piu' facile da fare.
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

COMANDO = "Rscript R/18_annidati.R"


def _serie(t, v):
    """Le coordinate della curva: eta' di osservazione, AUC, estremi dell'intervallo.

    Il primo modello non ha un'eta' — non usa nessuna cella — e si colloca due anni
    prima del primo per dare alla curva un punto di partenza visibile.
    """
    eta = list(v.get("eta_celle") or [])
    if not eta or len(t["righe"]) != len(eta) + 1:
        return None
    x = [eta[0] - 2] + eta
    return x, [r[3] for r in t["righe"]], [r[4] for r in t["righe"]], \
        [r[5] for r in t["righe"]]


def calcola():
    lt = Lettura()
    t = lt.tabella("annidati", "sequenza")
    v = lt.valori("annidati")
    if not t:
        print("   annidati: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    s = _serie(t, v)
    if not s:
        print("   annidati: la sequenza e le eta' non combaciano, salto la figura")
        return
    x, auc, lo, hi = s

    gr.stile()
    with gr.figura("Quanto si sa del futuro, e a che eta'") as (fig, ax):
        ax.fill_between(x, lo, hi, color=gr.COLORI[0], alpha=0.15, linewidth=0)
        ax.plot(x, auc, color=gr.COLORI[0], linewidth=2, marker="o", markersize=6)
        gr.linea_riferimento(ax, 0.5, "tirare a indovinare")
        for xi, yi, etichetta in zip(x[1:], auc[1:], v.get("celle", [])):
            ax.annotate(etichetta, xy=(xi, yi), xytext=(0, 9),
                        textcoords="offset points", ha="center", fontsize=8,
                        color=gr.GRIGIO)
        ax.set_xlabel("eta' a cui si osserva l'atleta (anni)")
        ax.set_ylabel("AUC cumulata")
        ax.set_xticks(x)
        ax.set_xticklabels(["solo\ncoorte"] + [str(e) for e in x[1:]])
        ax.set_ylim(0.4, 1.0)
    percorso = gr.salva("annidati_auc")

    # `pulisci=False`: valori e tabelle li ha scritti R.
    with Archivio("annidati", pulisci=False) as ar:
        ar.figura("auc", percorso,
                  didascalia="Ogni punto aggiunge una categoria alla precedente, sugli "
                             "stessi %s atleti. La banda e' l'intervallo di confidenza "
                             "al 95%% dell'AUC." % md.conta(v.get("n")))


def _p(x):
    """Un p-value come si legge in un testo, non come lo stampa il calcolatore."""
    if x is None:
        return "—"
    if x < 0.001:
        return "< 0,001"
    return md.num(x, 3)


def rendi(lt):
    v = lt.valori("annidati")
    t = lt.tabella("annidati", "sequenza")

    p = [md.sezione("Cosa aggiunge ogni categoria")]

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
        "Sapere come e' andato un ragazzo in Under 15 dice qualcosa. Sapere **anche** "
        "come e' andato in Under 17 dice qualcosa in piu', o e' informazione gia' "
        "contenuta nella precedente? E' la domanda che distingue «la prestazione "
        "giovanile predice» da «la prestazione giovanile predice, e sempre di piu' man "
        "mano che ci si avvicina»."))

    p.append(md.paragrafo(
        "",
        "I modelli si costruiscono per aggiunte successive e girano tutti sugli "
        "**stessi %s atleti**: quelli osservati in tutte le categorie della sequenza. "
        "E' una condizione stretta — restano %s atleti su %s della coorte — ma senza di "
        "essa il confronto misurerebbe il cambio di popolazione invece dell'aggiunta di "
        "informazione."
        % (md.conta(v.get("n")), md.conta(v.get("n")),
           md.conta(v.get("n_coorte")))))

    p.append(md.metodo(
        "Modelli annidati, AUC e test di DeLong",
        "Due modelli sono annidati quando uno contiene tutti i predittori dell'altro "
        "piu' qualcosa. Confrontarli dice quanto vale quel qualcosa.\n\n"
        "L'**AUC** e' la probabilita' che il modello assegni un punteggio piu' alto a "
        "un professionista che a un non professionista, presi a caso: 0,5 e' tirare a "
        "indovinare, 1 e' ordinamento perfetto.\n\n"
        "Il **test di DeLong** chiede se l'aumento di AUC e' distinguibile dal caso, "
        "tenendo conto che le due curve sono calcolate sulle stesse persone e quindi "
        "sono correlate. Il **rapporto di verosimiglianza** chiede invece se il "
        "predittore in piu' migliora l'adattamento del modello. Sono due domande "
        "diverse, e possono rispondere in modo diverso: un predittore puo' migliorare "
        "l'adattamento senza cambiare l'ordine in cui il modello mette le persone.",
        [("Area sotto la curva ROC", W + "Receiver_operating_characteristic#Area_under_the_curve"),
         ("Test del rapporto di verosimiglianza", W + "Likelihood-ratio_test"),
         ("DeLong et al. 1988", "https://doi.org/10.2307/2531595")]))

    righe = [[r[0], md.num(r[3], 3),
              "%s-%s" % (md.num(r[4], 3), md.num(r[5], 3)),
              "—" if r[6] is None else ("%+.3f" % r[6]).replace(".", ","),
              _p(r[7]), _p(r[8])]
             for r in t["righe"]]
    p.append(md.tabella(
        ["modello", "AUC", "IC 95%", "ΔAUC", "p (DeLong)", "p (verosimiglianza)"],
        righe, n=v.get("n"), nota=t["nota"]))

    salto = v.get("salto_maggiore")
    if salto:
        p.append(md.paragrafo(
            "",
            "Il passo che aggiunge di piu' e' **%s**, con un guadagno di AUC di %s. "
            "Nel complesso, passare dal solo Under 15 a tutte le categorie porta "
            "l'AUC da %s a %s."
            % (salto["modello"], md.num(salto["delta"], 3),
               md.num(t["righe"][1][3], 3), md.num(v.get("auc_finale"), 3))))

    f = lt.figura("annidati", "auc")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    # Il caso in cui i due test non concordano va spiegato, non nascosto: e' il punto
    # piu' interessante della tabella e anche il piu' facile da leggere male.
    ultimo = t["righe"][-1]
    if ultimo[7] is not None and ultimo[8] is not None and ultimo[7] > 0.05 >= ultimo[8]:
        p.append(md.paragrafo(
            "",
            "L'ultimo passo merita attenzione: **%s** migliora l'adattamento del "
            "modello in modo netto (p = %s al test di verosimiglianza), ma non migliora "
            "in modo distinguibile la capacita' di ordinare gli atleti (ΔAUC %s, "
            "p = %s al test di DeLong). Non e' una contraddizione: il rendimento in "
            "Under 23 aiuta a stimare *quanto* e' probabile che uno arrivi, ma su chi "
            "e' gia' arrivato fin li' non cambia quasi piu' *chi* mettere davanti. "
            "L'informazione utile per distinguere e' gia' stata spesa prima."
            % (ultimo[0], _p(ultimo[8]),
               ("%+.3f" % ultimo[6]).replace(".", ","), _p(ultimo[7]))))

    p.append(md.paragrafo(
        "",
        "> **Come vanno lette queste AUC.** Non accanto a quelle dei modelli per "
        "singola categoria. Li' il campione erano tutti gli atleti presenti in una "
        "cella; qui e' chi e' arrivato fino all'Under 23 restando in classifica, e fra "
        "loro i professionisti sono il %s%%. Su un gruppo gia' scremato distinguere e' "
        "piu' difficile, e infatti i numeri sono piu' bassi. Di questa tabella conta la "
        "**differenza fra righe**, non il livello."
        % md.num(v.get("tasso_pro", 0), 1)))

    p.append(md.paragrafo(
        "",
        "*Una riserva che si e' rivelata infondata, e vale la pena dirlo.* Il sospetto "
        "era che il salto in Under 19 fosse un artefatto dello strumento: se il ranking "
        "nazionale non contasse le gare internazionali, chi corre all'estero vi "
        "risulterebbe piu' debole di quanto sia, e le categorie non sarebbero "
        "confrontabili fra loro. La verifica dice il contrario — il regolamento della "
        "fonte prevede le gare all'estero in tutte le categorie, e dagli Juniores in su "
        "le pesa di piu': 15 punti per la vittoria in una gara internazionale contro i "
        "10 di una nazionale e i 5 di una regionale. Lo strumento e' lo stesso lungo "
        "tutto il percorso e il salto resta.",
        "",
        "La riserva pero' non si chiude del tutto, ed e' giusto dire dove resta aperta. "
        "I risultati ottenuti all'estero entrano in classifica **solo se il corridore li "
        "segnala**, mandando alla fonte copia dell'ordine di arrivo: sono previsti, non "
        "raccolti d'ufficio. Chi corre molto fuori dall'Italia ha quindi tutto "
        "l'interesse a farlo, e presumibilmente lo fa, ma la copertura delle gare "
        "internazionali dipende da un'iniziativa individuale e non da una procedura.",
        "",
        "Resta infine un limite diverso, che non si corregge ma si dichiara: chi corre "
        "stabilmente all'estero senza gare in Italia non compare affatto in classifica, "
        "e non vi compare nemmeno chi e' tesserato per una societa' straniera. E' un "
        "problema di copertura della popolazione, non di confrontabilita' delle misure."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
