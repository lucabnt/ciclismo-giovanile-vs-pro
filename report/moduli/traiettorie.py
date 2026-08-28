"""
Conta il livello o il miglioramento?

DA DOVE ARRIVANO I NUMERI
    Da `R/21_traiettorie.R`. Qui si legge dall'archivio e si scrive il testo.

PERCHE' QUESTA SEZIONE E' DIVERSA DALLE ALTRE
    E' l'unica che risponde a una domanda che gli allenatori si fanno davvero, e in
    quella forma. Tutte le altre chiedono se il rendimento predica; questa chiede quale
    dei due rendimenti — dove sei o dove stai andando — predica di piu'.

    E' anche l'unica in cui la risposta si legge bene da una tabella a doppia entrata,
    senza passare da nessun coefficiente. Il grafico e la tabella incrociata fanno quindi
    il lavoro principale, e i modelli servono a dire quanto e' solido cio' che si vede.
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

COMANDO = "Rscript R/21_traiettorie.R"
ORDINE = ("basso", "medio", "alto")


def calcola():
    lt = Lettura()
    inc = lt.tabella("traiettorie", "incrocio")
    if not inc:
        print("   traiettorie: nessun risultato da R, salto la figura"
              " (per averla: %s)" % COMANDO)
        return

    per_cella = {(r[0], r[1]): r for r in inc["righe"]}
    gr.stile()
    x = list(range(len(ORDINE)))
    larghezza = 0.26
    with gr.figura("Il tasso di professionismo per livello e miglioramento") as (fig, ax):
        for k, pend in enumerate(ORDINE):
            y = [per_cella.get((liv, pend), [0] * 5)[4] for liv in ORDINE]
            ax.bar([i + (k - 1) * larghezza for i in x], y, larghezza,
                   color=gr.COLORI[k], label="miglioramento %s" % pend)
        ax.set_xticks(x)
        ax.set_xticklabels(["livello %s" % l for l in ORDINE])
        ax.set_ylabel("% che diventa professionista")
        ax.legend(fontsize=8)
        ax.grid(axis="x", visible=False)
    percorso = gr.salva("traiettorie_incrocio")

    with Archivio("traiettorie", pulisci=False) as ar:
        ar.figura("incrocio", percorso,
                  didascalia="Il miglioramento da solo non basta — a sinistra le barre "
                             "restano schiacciate qualunque sia il colore — e il livello "
                             "da solo nemmeno: e' a destra, dove le due cose coincidono, "
                             "che il tasso si impenna.")


def _p(x):
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, 3)


def rendi(lt):
    v = lt.valori("traiettorie")
    coeff = lt.tabella("traiettorie", "coefficienti")
    inc = lt.tabella("traiettorie", "incrocio")
    stag = lt.tabella("traiettorie", "stagioni")
    shr = lt.tabella("traiettorie", "shrinkage")

    p = [md.sezione("Conta il livello o il miglioramento?")]

    if not coeff:
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
        "Un ragazzo che passa dal quarantesimo al novantesimo percentile in tre anni e' "
        "piu' promettente di uno stabile al settantacinquesimo? E' la domanda che in "
        "societa' si fa piu' spesso, ed e' l'unica di questo studio a cui i dati "
        "longitudinali possono rispondere direttamente."))

    p.append(md.metodo(
        "Modello misto e traiettorie individuali",
        "A ogni atleta si adatta una retta: il suo percentile in funzione dell'eta'. Due "
        "numeri riassumono la traiettoria — il **livello**, cioe' dove passa la retta a "
        "meta' del percorso giovanile, e la **pendenza**, cioe' quanto sale o scende "
        "ogni anno.\n\n"
        "Non si fa una regressione separata per ciascun atleta: chi ha due sole stagioni "
        "avrebbe una pendenza stimata su due punti, cioe' rumore. Il modello misto stima "
        "tutte le rette insieme e applica lo **shrinkage** — le stime individuali "
        "vengono tirate verso la media della popolazione tanto piu' quanto meno dati ha "
        "quell'atleta. E' il comportamento corretto e viene fuori da solo dalla "
        "struttura del modello, ma va saputo: le pendenze di chi ha poche stagioni sono "
        "poco individuali.\n\n"
        "La finestra si ferma a %s anni. Oltre comincia l'Under 23, dove alcuni atleti "
        "sono gia' professionisti: includere quelle stagioni significherebbe prevedere "
        "l'esito con osservazioni raccolte dopo che l'esito si e' verificato.\n\n"
        "Livello e pendenza entrano **sempre insieme** nel modello, perche' sono "
        "correlati per costruzione: il percentile ha un soffitto a 100, quindi chi parte "
        "alto ha meno spazio per salire. Nei dati quella correlazione vale %s."
        % (md.conta(v.get("eta_massima")),
           md.num(v.get("correlazione_livello_pendenza"), 2)),
        [("Modelli a effetti misti", W + "Mixed_model"),
         ("Shrinkage", W + "Shrinkage_(statistics)"),
         ("BLUP", W + "Best_linear_unbiased_prediction")]))

    if stag:
        p.append(md.paragrafo(
            "Le traiettorie sono stimate su **%s osservazioni** di %s atleti, ma le "
            "stagioni osservate per atleta sono poche e molto diseguali."
            % (md.conta(v.get("n_osservazioni")),
               md.conta(sum(r[1] for r in stag["righe"])))))
        p.append(md.tabella(stag["colonne"], stag["righe"], nota=stag["nota"],
                            colonne_conteggio=(1,)))

    p.append(md.paragrafo(
        "",
        "Il modello dell'esito gira sui %s atleti con almeno %s stagioni osservate, fra "
        "cui %s professionisti: sotto le due stagioni la pendenza individuale non esiste "
        "e lo shrinkage la riporta esattamente alla media, quindi quelle righe non "
        "porterebbero informazione sulla domanda che si sta facendo."
        % (md.conta(v.get("n_atleti")), md.conta(v.get("min_stagioni")),
           md.conta(v.get("n_eventi")))))

    righe = [[r[0], md.num(r[1], 2), "%s-%s" % (md.num(r[2], 2), md.num(r[3], 2)),
              _p(r[4])] for r in coeff["righe"]]
    p.append(md.tabella(["variabile", "odds ratio", "IC 95%", "p"], righe,
                        n=v.get("n_atleti"), nota=coeff["nota"]))

    auc = v.get("auc")
    if auc:
        p.append(md.paragrafo(
            "",
            md.afferma(
                auc["differenza"] > 0.02 and (auc["p"] or 1) < 0.05,
                "aggiungere la pendenza al livello migliora in modo distinguibile la "
                "capacita' di ordinare gli atleti",
                "**Contano tutti e due, e il miglioramento aggiunge parecchio.** Un "
                "modello che conosce solo il livello arriva a un'AUC di %s; "
                "aggiungendo la pendenza sale a %s, cioe' %s in piu' (p = %s al test "
                "di DeLong). Non e' informazione ridondante: sapere dove sta andando un "
                "atleta dice qualcosa che il suo livello attuale non dice."
                % (md.num(auc["livello"], 3), md.num(auc["completo"], 3),
                   ("%+.3f" % auc["differenza"]).replace(".", ","), _p(auc["p"])))))

    if inc:
        p.append(md.sezione("La stessa risposta senza coefficienti", 3))
        righe_i = [[r[0], r[1], r[2], r[3], md.num(r[4], 1)] for r in inc["righe"]]
        p.append(md.tabella(
            ["livello", "miglioramento", "atleti", "professionisti", "% pro"],
            righe_i, nota=inc["nota"], colonne_conteggio=(2, 3)))

        per_cella = {(r[0], r[1]): r for r in inc["righe"]}
        alto_alto = per_cella.get(("alto", "alto"))
        alto_basso = per_cella.get(("alto", "basso"))
        medio_alto = per_cella.get(("medio", "alto"))
        if alto_alto and alto_basso:
            p.append(md.paragrafo(
                "",
                "Il gradiente corre in **entrambe** le direzioni, ma non allo stesso "
                "modo. Nel terzo di atleti con il livello piu' alto, chi stava anche "
                "migliorando e' diventato professionista nel %s%% dei casi, chi stava "
                "peggiorando nel %s%%: quasi dieci volte tanto, a parita' di livello. "
                "Nel terzo con livello medio e miglioramento alto si arriva al %s%%, "
                "piu' che nel terzo con livello alto e pendenza in calo."
                % (md.num(alto_alto[4], 1), md.num(alto_basso[4], 1),
                   md.num(medio_alto[4], 1) if medio_alto else "—")))
        p.append(md.paragrafo(
            "",
            "Nel terzo con il livello piu' basso, invece, il miglioramento non salva "
            "quasi nessuno. **Il livello e' una condizione, il miglioramento e' un "
            "moltiplicatore**: senza il primo il secondo non basta, ma con il primo il "
            "secondo cambia molto."))

    f = lt.figura("traiettorie", "incrocio")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    # Il controllo che questo studio ha imparato a fare: e' davvero la traiettoria, o e'
    # ancora una volta la durata della carriera?
    ctrl = v.get("controllo_durata")
    if ctrl and shr:
        p.append(md.sezione("Non sara' di nuovo la durata della carriera?", 3))
        p.append(md.paragrafo(
            "La sezione sulla mobilita' ha mostrato che un gradiente vistoso puo' essere "
            "la durata della carriera vista da un'altra angolazione. Qui il sospetto e' "
            "fondato per un motivo tecnico preciso: lo shrinkage rende meno estreme le "
            "pendenze di chi ha poche stagioni, quindi una pendenza marcata e' anche un "
            "indizio di carriera lunga."))
        p.append(md.tabella(shr["colonne"], shr["righe"], nota=shr["nota"],
                            colonne_conteggio=(), decimali=2))
        p.append(md.paragrafo(
            "",
            md.afferma(
                ctrl["con"] > 0.6 * ctrl["senza"],
                "l'effetto della pendenza sopravvive all'aggiustamento per il numero di "
                "stagioni osservate",
                "Il controllo si fa aggiungendo al modello il numero di stagioni "
                "osservate: l'odds ratio della pendenza passa da %s a %s. Si riduce, ma "
                "resta grande. **Questa volta il gradiente non e' un travestimento della "
                "durata della carriera.**"
                % (md.num(ctrl["senza"], 2), md.num(ctrl["con"], 2))),
            "",
            "Il numero di stagioni non entra pero' nel modello principale, e per la "
            "stessa ragione per cui non ci entrano societa' e regione: chi va meglio "
            "resta di piu', quindi la durata sta sul percorso causale fra rendimento ed "
            "esito. Metterla fra i controlli sottrarrebbe una parte dell'effetto che si "
            "vuole misurare. La si usa come verifica, non come aggiustamento."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
