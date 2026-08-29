"""
Lo stesso punteggio non e' lo stesso risultato.

DA DOVE NASCE
    Da una critica esterna. Hasselaar e Elferink-Gemser (2025) mostrano due ciclisti con
    lo stesso identico punteggio in un ranking federale e livelli reali completamente
    diversi, e concludono che quei ranking non sono una misura affidabile della
    prestazione giovanile. La critica colpisce la fonte di questo studio, quindi va
    verificata sui dati invece che accettata o respinta a parole.

DA DOVE ARRIVANO I NUMERI
    Da `R/30_misura.R`. La numerazione dei file R da 30 in su indica le analisi nate dopo
    la guida, da domande che il lavoro ha fatto emergere.

PERCHE' QUESTA SEZIONE STA VICINO ALL'INIZIO
    Perche' riguarda lo strumento, non i risultati. Chi legge una percentuale ha diritto
    di sapere prima quanto e' precisa la misura da cui viene — e in questo caso la
    risposta contiene una sorpresa.
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

COMANDO = "Rscript R/30_misura.R"


def calcola():
    lt = Lettura()
    t = lt.tabella("misura", "rapporto")
    if not t:
        print("   misura: nessun risultato da R, salto la figura (per averla: %s)"
              % COMANDO)
        return

    nomi = [r[0] for r in t["righe"]]
    valori = [r[4] for r in t["righe"]]
    gr.stile()
    x = list(range(len(nomi)))
    with gr.figura("Quanto vale un piazzamento nei primi cinque", altezza=3.4) as (f, ax):
        colori = [gr.COLORI[0] if n in ("U15", "U17") else gr.COLORI[1] for n in nomi]
        ax.bar(x, valori, 0.55, color=colori)
        for i, v in enumerate(valori):
            ax.annotate(md.num(v, 2), xy=(i, v), xytext=(0, 4),
                        textcoords="offset points", ha="center", fontsize=9)
        ax.set_xticks(x)
        ax.set_xticklabels(nomi)
        ax.set_ylabel("punti per piazzamento")
        ax.set_ylim(0, max(valori) * 1.25)
        ax.grid(axis="x", visible=False)
        ax.annotate("in rosso le categorie in cui la fonte\npesa le gare per livello",
                    xy=(0.02, 0.95), xycoords="axes fraction", va="top", fontsize=9,
                    color=gr.GRIGIO)
    percorso = gr.salva("misura_rapporto")

    with Archivio("misura", pulisci=False) as ar:
        ar.figura("rapporto", percorso,
                  didascalia="Il salto avviene fra Allievi e Juniores, che e' esattamente "
                             "dove la fonte comincia a moltiplicare i punti delle gare "
                             "nazionali e internazionali.")


def _p(x):
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, 3)


def rendi(lt):
    v = lt.valori("misura")
    conf = lt.tabella("misura", "confronto")
    rap = lt.tabella("misura", "rapporto")

    p = [md.sezione("Lo stesso punteggio e' lo stesso risultato?")]

    if not conf:
        p.append(md.paragrafo(
            "*Questa sezione richiede i modelli in R, che non risultano ancora "
            "eseguiti. Per produrla:*",
            "", "```", "python scripts/08_prepara_modelli.py", COMANDO, "```"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "Tutto quello che segue si appoggia a una misura: il piazzamento nella classifica "
        "nazionale. Prima di usarla conviene chiedersi quanto sia precisa, e la domanda "
        "non e' oziosa — arriva da fuori."))

    p.append(md.metodo(
        "La critica di Hasselaar, e perche' va presa sul serio",
        "Uno studio olandese del 2025 ha mostrato il problema con un esempio che vale "
        "piu' di qualunque argomento. Due ciclisti, uno che corre gare internazionali e "
        "uno che corre soprattutto gare locali, ottengono **lo stesso identico "
        "punteggio** nel ranking federale: 414 punti. In una metrica costruita apposta "
        "per tenere conto del livello delle gare, gli stessi due valgono 76 e 21.\n\n"
        "La ragione e' che il ranking olandese non conta i risultati internazionali, "
        "quindi assegna zero punti proprio alle gare piu' difficili. E premia chi va "
        "bene nelle tipologie di gara piu' frequenti in calendario: in Olanda i circuiti "
        "piatti e ventosi, dove i velocisti hanno molte piu' occasioni degli scalatori.\n\n"
        "La critica colpisce direttamente la fonte di questo studio, che e' un ranking "
        "federale. Va quindi verificata sui dati invece che accettata o respinta.",
        [("Hasselaar & Elferink-Gemser (2025)",
          "https://doi.org/10.36950/2025.10ciss012")]))

    # --- la prima verifica: la scala pesa le gare? ---------------------------
    if rap:
        p.append(md.sezione("La nostra fonte conta le gare internazionali", 3))
        p.append(md.paragrafo(
            "La prima meta' della critica non si applica. La classifica italiana **pesa "
            "le gare per livello**, ma solo dalle categorie internazionali in su: in "
            "Juniores e Under 23 una gara nazionale vale il doppio di una regionale e "
            "una internazionale il triplo. In Esordienti e Allievi, che non hanno "
            "calendario internazionale, una gara all'estero vale quanto una regionale.",
            "",
            "Non abbiamo il dettaglio delle singole gare, ma la conseguenza si vede lo "
            "stesso: se le gare pesano, un piazzamento vale in media di piu'. Basta "
            "dividere i punti per il numero di piazzamenti nei primi cinque."))
        righe_r = [[r[0], r[1], md.num(r[2], 1), md.num(r[3], 2), md.num(r[4], 2)]
                   for r in rap["righe"]]
        p.append(md.tabella(rap["colonne"], righe_r, nota=rap["nota"],
                            colonne_conteggio=(1,)))

        est = v.get("rapporto_estremi", {})
        p.append(md.paragrafo(
            "",
            md.afferma(
                est.get("valore_alto", 0) > est.get("valore_basso", 1),
                "il rapporto fra punti e piazzamenti cresce passando alle categorie in "
                "cui la fonte pesa le gare per livello",
                "**Il salto e' esattamente dove deve essere.** Un piazzamento vale %s "
                "punti in %s e %s in %s, e la crescita comincia fra Allievi e Juniores "
                "— cioe' dove i moltiplicatori entrano in funzione. E' una conferma "
                "indiretta ma pulita: la scala fa quello che dichiara di fare."
                % (md.num(est.get("valore_basso"), 2), est.get("bassa", "—"),
                   md.num(est.get("valore_alto"), 2), est.get("alta", "—")))))

        f = lt.figura("misura", "rapporto")
        if f:
            p.append(md.figura(f["percorso"], f["didascalia"]))

    # --- la seconda verifica: i pari merito ---------------------------------
    p.append(md.sezione("Ma i pari merito sono moltissimi", 3))
    p.append(md.paragrafo(
        "Resta un problema diverso, e piu' grande di quanto sembri. La scala assegna "
        "cinque punti alla vittoria e uno al quinto posto, quindi i totali possibili "
        "sono pochi e gli atleti tanti: **fino al %s%% dei classificati condivide il "
        "proprio punteggio con qualcun altro**. Guardando solo i punti, quegli atleti "
        "sono indistinguibili."
        % md.num(v.get("pari_merito_massimo"), 1)))

    p.append(md.paragrafo(
        "",
        "Il progetto lo aveva previsto e aveva scelto di scioglierli guardando prima le "
        "vittorie, poi i secondi posti e cosi' via fino al quinto. La scelta era stata "
        "presa **prima di guardare qualunque esito**, il che permette ora di metterla "
        "alla prova senza il sospetto di averla scelta perche' funzionava."))

    righe_c = [[r[0], r[1], r[2], md.num(r[3], 1) + "%", md.num(r[4], 3),
                md.num(r[5], 3), ("%+.3f" % r[6]).replace(".", ","), _p(r[7])]
               for r in conf["righe"]]
    p.append(md.tabella(
        ["cella", "atleti", "professionisti", "pari merito", "AUC sui punti",
         "AUC con il criterio esteso", "differenza", "p"],
        righe_c, nota=conf["nota"], colonne_conteggio=(1, 2)))

    migliorate = v.get("celle_migliorate")
    totali = v.get("celle_confrontate")
    massimo = v.get("guadagno_massimo")
    if totali:
        p.append(md.paragrafo(
            "",
            md.afferma(
                abs(massimo or 0) < 0.02,
                "sciogliere i pari merito con i piazzamenti non cambia in modo "
                "apprezzabile la capacita' di distinguere chi arrivera'",
                "**Non cambia niente.** Il guadagno piu' grande e' di %s punti di AUC, "
                "in %s celle su %s la differenza e' addirittura negativa, e in nessuna "
                "cella e' distinguibile dal caso. A parita' di punti, **il modo in cui "
                "sono stati ottenuti non dice nulla di piu'** su chi diventera' "
                "professionista."
                % (md.num(massimo, 3), md.conta((totali or 0) - (migliorate or 0)),
                   md.conta(totali)))))

    p.append(md.paragrafo(
        "",
        "E' un risultato controintuitivo e vale la pena soffermarsi. Cinque punti si "
        "ottengono con una vittoria oppure con cinque quinti posti, e chiunque direbbe "
        "che la vittoria vale di piu'. Su questi dati non e' cosi': i due atleti hanno "
        "le stesse probabilita' di arrivare. Quello che conta e' **quanto si e' andati a "
        "punti**, non con quale forma."))

    p.append(md.paragrafo(
        "",
        "> **Cosa se ne ricava per lo studio.** Il criterio esteso resta il predittore "
        "principale, perche' e' piu' fine e non fa danno; ma la sezione dice "
        "esplicitamente che i risultati sarebbero gli stessi con i soli punti. E' una "
        "verifica di robustezza su una scelta metodologica presa all'inizio, con "
        "l'esito che rende la scelta irrilevante — che e' il modo migliore in cui una "
        "verifica del genere possa finire."))

    p.append(md.paragrafo(
        "",
        "> **La parte della critica che resta in piedi.** Hasselaar solleva due problemi "
        "e qui se ne e' affrontato uno solo. Il secondo — che un ranking premia chi "
        "eccelle nelle tipologie di gara piu' frequenti in calendario — **vale anche per "
        "i nostri dati e non e' correggibile con quello che abbiamo**: servirebbe il "
        "dettaglio gara per gara, che la fonte non pubblica. Chi va forte in salita, in "
        "un calendario fatto soprattutto di percorsi veloci, ha meno occasioni di andare "
        "a punti. E' un limite dello strumento, e va tenuto presente ogni volta che si "
        "legge un percentile come se fosse una misura del valore dell'atleta."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
