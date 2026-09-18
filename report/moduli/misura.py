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
        "per tenere conto del livello delle gare, gli stessi due valgono 76 e 21, cioe' "
        "un fattore 3,6. I due ciclisti sono **costruiti dagli autori**, non due casi "
        "osservati, e vanno citati come tali: il meccanismo che illustrano e' pero' "
        "reale e documentato nello stesso articolo.\n\n"
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
            "le gare per livello**, ma solo dalle categorie internazionali in su. I "
            "regolamenti della fonte, che sono pubblici, danno la scala esatta:"))
        p.append(md.tabella(
            ["tipo di gara", "Esordienti e Allievi", "Juniores (e Under 23)"],
            [["regionale", "5-4-3-2-1", "5-4-3-2-1"],
             ["nazionale", "5-4-3-2-1", "10-8-6-4-2"],
             ["internazionale", "non in calendario", "15-12-9-6-3"],
             ["campionato italiano in linea", "15-12-9-6-3", "15-12-9-6-3"],
             ["campionato italiano a cronometro", "15-12-9-6-3, ma solo Allievi",
              "15-12-9-6-3"],
             ["campionato europeo", "non in calendario", "20-16-12-8-4"],
             ["campionato del mondo", "non in calendario", "30-24-18-12-6"]],
            nota="punti dal primo al quinto arrivato. Il campionato italiano a "
                 "cronometro Esordienti non si disputa, quindi per quella categoria la "
                 "riga e' lettera morta. Il regolamento Under 23 non e' stato reperito: "
                 "qui si assume che ricalchi quello Juniores, come categoria "
                 "internazionale, e l'assunzione va tenuta presente"))
        p.append(md.paragrafo(
            "In Esordienti e Allievi, quindi, la scala e' piatta salvo i campionati "
            "italiani, che valgono il triplo: due in Allievi, la gara in linea e quella "
            "a cronometro, e **uno solo in Esordienti**, perche' il campionato a "
            "cronometro per quella categoria non si disputa. Il regolamento della fonte "
            "lo elenca lo stesso, ricalcando il fascicolo degli Allievi, ma e' lettera "
            "morta. Per il resto, a quelle eta' una gara all'estero vale quanto una gara "
            "sotto casa. Dagli Juniores in su i moltiplicatori compaiono, e sono piu' di "
            "due — il campionato europeo vale quattro volte una gara regionale e quello "
            "del mondo sei.",
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

        p.append(md.metodo(
            "Cosa entra in classifica, e cosa no",
            "I regolamenti della fonte delimitano la popolazione e il calendario in "
            "modo piu' stretto di quanto si direbbe, e ognuno dei quattro limiti che "
            "seguono lascia un segno nei dati.\n\n"
            "**Solo strada.** Contano le gare su strada, in circuito e a cronometro, di "
            "qualunque lunghezza; le gare su pista sono escluse per regolamento. Chi "
            "corre altre specialita' e' tesserato ma non puo' comparire, ed e' una delle "
            "ragioni per cui la copertura calcolata piu' avanti e' un limite inferiore."
            "\n\n"
            "**Solo tesserati con societa' italiane.** Chi e' tesserato per una societa' "
            "affiliata all'estero non entra in classifica nemmeno quando ottiene "
            "risultati in gare che si corrono in Italia. Un atleta che passa a una "
            "squadra straniera esce quindi dalla classifica senza aver smesso di "
            "correre, ed e' un meccanismo in piu' fra quelli che fanno sparire un nome."
            "\n\n"
            "**I risultati all'estero li segnala l'atleta.** Il regolamento chiede a chi "
            "corre fuori dall'Italia di far pervenire copia dell'ordine di arrivo perche' "
            "il risultato venga conteggiato. Le gare internazionali sono quindi incluse, "
            "ma per iniziativa del corridore: e' ragionevole che a segnalarle siano "
            "soprattutto quelli che ci vanno spesso e che ne ricavano punti pesanti.\n\n"
            "**Anche in Italia la raccolta e' a impegno di mezzi.** Il comitato dichiara "
            "che fara' il possibile per conoscere tutti i risultati e che segnalera' le "
            "gare mancanti al momento della pubblicazione. Non e' un archivio "
            "ufficiale della federazione, ed e' bene ricordarlo ogni volta che si legge "
            "un'assenza come un'informazione."))

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
        "vittorie, poi i secondi posti e cosi' via fino al quinto. La scelta e' "
        "registrata in `docs/definizioni.md` fin dal primo commit del repository ed e' "
        "stata presa **prima di guardare qualunque esito**, il che permette ora di "
        "metterla alla prova senza il sospetto di averla scelta perche' funzionava. "
        "Quest'ultima parte e' una dichiarazione e non una prova: del lavoro precedente "
        "al repository non resta traccia.",
        "",
        "C'e' di piu', ed e' emerso dopo: quel criterio non e' una nostra invenzione ma "
        "**la regola di spareggio che il regolamento della fonte dichiara**, nelle stesse "
        "parole e nello stesso ordine. Ricostruendo il percentile con esso non stiamo "
        "quindi imponendo un ordinamento nostro, stiamo riproducendo quello pubblicato. "
        "Il regolamento prosegue con due criteri ulteriori che qui non si applicano: a "
        "parita' anche di piazzamenti vince chi ha raggiunto per primo il punteggio, e "
        "in ultimo il piu' giovane. Il primo chiederebbe la data di ogni gara, che non "
        "abbiamo; il secondo introdurrebbe l'eta' dentro la misura, che e' esattamente "
        "cio' che non vogliamo. Chi resta a pari merito qui ha lo stesso identico "
        "palmares, e la tabella qui sotto mostra che spingersi oltre non servirebbe."))

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
