"""
Quanto regge tutto questo.

DA DOVE ARRIVANO I NUMERI
    Da tre fonti diverse, che rispondono a tre domande diverse sulla stessa cosa:

        R/24_validazione.R      il modello si giudica meglio di quanto sia?
        scripts/10_sensibilita.py  le conclusioni dipendono dalle scelte di disegno?
        R/27_confronto_ml.R     un modello piu' complicato farebbe meglio?

PERCHE' STANNO IN UNA SEZIONE SOLA
    Perche' un lettore che arriva qui ha gia' visto tutti i risultati e si sta facendo
    una domanda sola — «posso crederci?» — e le tre risposte sono parti della stessa
    risposta. Separarle costringerebbe a leggerle come tre argomenti tecnici invece che
    come un unico argomento sulla solidita'.

UNA CAUTELA SULLE AUC DI QUESTA SEZIONE
    Alcune sono calcolate su tutta la coorte, con l'assenza dalla classifica codificata
    come categoria, e sono percio' piu' alte di quelle delle sezioni precedenti, che
    girano sui soli presenti. Il testo lo dice dove serve: fra sezioni diverse conta la
    stabilita' dei confronti, non il livello.
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

COMANDI = ("Rscript R/24_validazione.R",
           "python scripts/10_sensibilita.py",
           "Rscript R/27_confronto_ml.R",
           "Rscript R/17_penalizzato.R")


def calcola():
    lt = Lettura()
    sens = lt.tabella("sensibilita", "definizione")
    fin = lt.tabella("sensibilita", "finestra")
    if not sens or not fin:
        print("   validazione: mancano i risultati di sensibilita', salto la figura")
        return

    righe = list(sens["righe"]) + list(fin["righe"])
    nomi = [r[0].replace(" (scelta dello studio)", " *") for r in righe]
    auc = [r[4] for r in righe]
    eventi = [r[1] for r in righe]

    gr.stile()
    y = list(range(len(righe)))[::-1]
    with gr.figura("Le conclusioni reggono se si cambiano le scelte?",
                   altezza=3.6) as (fig, ax):
        ax.barh(y, auc, 0.6, color=gr.COLORI[0])
        for i, yy in enumerate(y):
            ax.annotate("%d eventi" % eventi[i], xy=(auc[i], yy), xytext=(6, 0),
                        textcoords="offset points", va="center", fontsize=8,
                        color=gr.GRIGIO)
        ax.set_yticks(y)
        ax.set_yticklabels(nomi, fontsize=8)
        # L'asse parte da 0,5, che e' il tirare a indovinare: una linea di riferimento
        # li' cadrebbe sul bordo e non si vedrebbe. Lo dice l'etichetta.
        ax.set_xlabel("AUC del percentile Under 19 (0,5 = tirare a indovinare)")
        ax.set_xlim(0.5, 1.08)
        ax.grid(axis="y", visible=False)
    percorso = gr.salva("validazione_sensibilita")

    with Archivio("validazione", pulisci=False) as ar:
        ar.figura("sensibilita", percorso,
                  didascalia="Il numero di professionisti cambia da ventisei a "
                             "centocinquantuno a seconda di come li si definisce, ma la "
                             "capacita' del rendimento giovanile di distinguerli resta "
                             "quasi la stessa. L'asterisco indica la scelta dello studio.")


def rendi(lt):
    v = lt.valori("validazione")
    vs = lt.valori("sensibilita")
    vm = lt.valori("confronto_ml")
    ott = lt.tabella("validazione", "ottimismo")
    temp = lt.tabella("validazione", "temporale")

    p = [md.sezione("Quanto regge tutto questo")]

    if not ott:
        p.append(md.paragrafo(
            "*Questa sezione richiede la validazione, non ancora eseguita. Per "
            "produrla:*",
            "",
            "```",
            *COMANDI,
            "```"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "Un modello stimato su un campione e misurato sullo stesso campione si giudica "
        "da solo, e si giudica bene. Una parte della sua bravura e' vera, un'altra e' "
        "adattamento al rumore di quelle particolari righe, e guardando il numero le due "
        "non si distinguono. Questa sezione raccoglie le tre prove che servono a "
        "separarle."))

    # --- riconciliazione dei conteggi ----------------------------------------
    p.append(md.sezione("Quanti professionisti, e perche' i conteggi non coincidono", 3))
    p.append(md.paragrafo(
        "Il numero di professionisti cambia da una sezione all'altra di questo documento, "
        "e la prima cosa che un lettore attento fa e' provare a farlo tornare. Non torna, "
        "e non deve: ogni analisi ha la popolazione che la sua domanda consente. Questa "
        "tabella mette i conteggi uno accanto all'altro con il motivo di ciascuno, che e' "
        "piu' utile di un numero unico ottenuto rinunciando a delle domande."))

    liv = lt.tabella("qualita", "livelli")
    pro_qualita = sum(r[1] for r in liv["righe"][1:]) if liv else None
    definizioni = lt.tabella("sensibilita", "definizione")
    estremi_def = None
    if definizioni:
        conteggi = sorted(r[1] for r in definizioni["righe"])
        estremi_def = "da %s a %s" % (md.conta(conteggi[0]), md.conta(conteggi[-1]))

    def _riga(titolo, modulo, k_atleti, k_eventi, motivo, eventi=None):
        return [titolo, lt.valore(modulo, "coorti"),
                md.conta(lt.valore(modulo, k_atleti)) if k_atleti else "—",
                eventi if eventi is not None
                else md.conta(lt.valore(modulo, k_eventi)), motivo]

    righe_r = [
        _riga("accesso al professionismo", "attrito", "atleti_totali", "pro_totali",
              "tutti i classificati delle coorti: e' la popolazione dello studio"),
        _riga("cosa aggiunge ogni categoria", "annidati", "n", "eventi",
              "solo chi e' osservato in tutte le categorie, per confrontare i modelli "
              "sulle stesse persone"),
        _riga("livello e miglioramento", "traiettorie", "n_atleti", "n_eventi",
              "serve piu' di una stagione per stimare una pendenza"),
        _riga("qualita' della carriera", "qualita", "n", None,
              "coorti piu' larghe, perche' i top 100 sono pochissimi, e solo chi compare "
              "in Under 19 secondo anno", eventi=md.conta(pro_qualita)),
        _riga("quando si diventa professionisti", "sopravvivenza", "n_atleti",
              "n_eventi",
              "tutte le coorti disponibili, con censura: qui si contano gli eventi, non "
              "le persone"),
        _riga("sensibilita' sulle definizioni", "sensibilita", "n", None,
              "cambia cosa conta come professionismo, a parita' di atleti",
              eventi=estremi_def or "—"),
    ]
    p.append(md.tabella(
        ["analisi", "coorti", "atleti", "professionisti", "perche' quel numero"],
        righe_r))

    p.append(md.paragrafo(
        "",
        "Resta un settimo numero, e sta fuori da questa tabella perche' non viene da una "
        "query: `docs/definizioni.md` congela **78 eventi PRO** per le coorti 1996-2000. "
        "Quel file e' stato scritto prima di guardare i dati, come impone la procedura, e "
        "prima della verifica manuale degli abbinamenti — diciotto date corrette, dieci "
        "atleti duplicati riuniti in uno solo. Il conteggio che si rigenera oggi e' quello "
        "della prima riga, e ho provato a ricostruire da dove venga la differenza di uno "
        "senza riuscirci: nessuna delle correzioni manuali sposta un professionista dentro "
        "o fuori quelle coorti. La riporto cosi' com'e' invece di inventarle una causa.",
        "",
        "*Nota sui confronti multipli.* Questo documento riporta decine di stime con il "
        "loro intervallo di confidenza e **non applica nessuna correzione** per la "
        "molteplicita' dei confronti. E' una scelta, e va saputa: gli intervalli vanno "
        "letti uno per uno, e un singolo p-value appena sotto la soglia convenzionale, in "
        "mezzo a tanti, non e' una scoperta. I risultati su cui il documento si appoggia "
        "sono quelli che restano in piedi per ordine di grandezza, non per un decimale."))

    # --- STEP 24 --------------------------------------------------------------
    p.append(md.sezione("Il modello si sta giudicando troppo bene?", 3))
    p.append(md.metodo(
        "Correzione dell'ottimismo e pendenza di calibrazione",
        "Si ricampiona con reimmissione, si ristima il modello sul campione estratto e "
        "si misura la sua AUC due volte: sul campione che lo ha addestrato e sui dati "
        "originali. La differenza e' l'**ottimismo** di quella ripetizione, e la media "
        "degli ottimismi si sottrae all'AUC apparente. E' la procedura di Harrell, la "
        "stessa che usa `rms::validate`.\n\n"
        "La **pendenza di calibrazione** dice un'altra cosa: se le probabilita' previste "
        "sono nella scala giusta. Vale 1 quando lo sono; meno di 1 quando il modello e' "
        "troppo sicuro di se', che e' il sintomo tipico del sovradattamento.",
        [("Bootstrap", W + "Bootstrapping_(statistics)"),
         ("Calibrazione", W + "Calibration_(statistics)"),
         ("Overfitting", W + "Overfitting")]))

    righe = [[r[0], r[1], r[2], md.num(r[3], 3), md.num(r[4], 3), md.num(r[5], 3),
              md.num(r[6], 2)] for r in ott["righe"]]
    p.append(md.tabella(
        ["modello", "atleti", "eventi", "AUC apparente", "ottimismo", "AUC corretta",
         "pendenza di calibrazione"],
        righe, nota=ott["nota"], colonne_conteggio=(1, 2)))

    massimo = v.get("ottimismo_massimo")
    if massimo is not None:
        p.append(md.paragrafo(
            "",
            md.afferma(
                massimo < 0.05,
                "l'ottimismo dei modelli resta ben sotto la soglia di 0,05 oltre la "
                "quale un modello va semplificato",
                "**L'ottimismo e' praticamente nullo**: al massimo %s punti di AUC, "
                "contro una soglia convenzionale di 0,05 oltre la quale un modello "
                "andrebbe semplificato. E le pendenze di calibrazione sono a ridosso di "
                "1. Non e' un caso fortunato: sono modelli con due o tre parametri "
                "stimati su centinaia di atleti, e a quel rapporto non c'e' spazio per "
                "adattarsi al rumore." % md.num(massimo, 3)),
            "",
            "E' anche un argomento a favore della forma che questo studio ha scelto. La "
            "tentazione, con dati longitudinali su migliaia di persone, e' costruire "
            "modelli ricchi; il prezzo sarebbe stato pagarlo qui."))

    # --- STEP 25 --------------------------------------------------------------
    if temp:
        p.append(md.sezione("Funziona su coorti che il modello non ha visto?", 3))
        taglio = v.get("taglio_temporale")
        p.append(md.paragrafo(
            "Il ricampionamento verifica la stabilita' interna, non la "
            "generalizzabilita'. Per quella si addestra sulle coorti piu' vecchie e si "
            "misura su quelle piu' recenti — che e' anche il modo in cui il modello "
            "verrebbe usato davvero: si stima su chi ha gia' finito il percorso e si "
            "applica a chi lo sta facendo."))
        righe_t = [[r[0], r[1], r[2], r[3], r[4], md.num(r[5], 3), md.num(r[6], 3)]
                   for r in temp["righe"]]
        p.append(md.tabella(
            ["modello", "atleti", "eventi", "atleti", "eventi", "AUC", "AUC"],
            righe_t, nota=(temp["nota"] + " — le prime due colonne di numeri sono "
                           "l'addestramento, le altre la verifica"),
            colonne_conteggio=(1, 2, 3, 4)))

        cala = any(r[6] < r[5] for r in temp["righe"])
        p.append(md.paragrafo(
            "",
            md.afferma(
                not cala,
                "sulle coorti di verifica la capacita' discriminante non peggiora "
                "rispetto a quelle di addestramento",
                "**Non cala: se mai migliora.** Addestrando sulle coorti %s-%s e "
                "verificando sulle %s-%s l'AUC sale invece di scendere. Va detto con "
                "prudenza — le coorti di verifica contengono %s eventi soltanto, e con "
                "cosi' pochi casi la stima balla — ma quello che si voleva escludere, "
                "cioe' un crollo, non si vede."
                % (taglio[0], taglio[1], taglio[1] + 1, taglio[2],
                   md.conta(temp["righe"][0][4])))))

    # --- STEP 26 --------------------------------------------------------------
    p.append(md.sezione("Le conclusioni dipendono dalle scelte di disegno?", 3))
    p.append(md.paragrafo(
        "Diverse decisioni di questo studio sono difendibili ma non obbligate: dove "
        "finisce il professionismo, entro quale eta' contarlo, dove mettere la soglia "
        "del «top». Ognuna e' stata presa una volta e poi usata ovunque, e un lettore ha "
        "diritto di sapere quanto le conclusioni ne dipendano."))

    for chiave, titolo in (("definizione", None), ("finestra", None), ("soglia", None)):
        t = lt.tabella("sensibilita", chiave)
        if not t:
            continue
        righe_s = [[r[0], r[1], md.num(r[3], 2) + "%", md.num(r[4], 3)]
                   for r in t["righe"]]
        p.append(md.tabella([t["colonne"][0], t["colonne"][1], t["colonne"][3],
                             t["colonne"][4]], righe_s, nota=t["nota"],
                            colonne_conteggio=(1,)))

    osc = vs.get("oscillazione_auc")
    if osc is not None:
        p.append(md.paragrafo(
            "",
            md.afferma(
                osc < 0.1,
                "cambiando la definizione di professionista e la finestra d'eta' la "
                "capacita' discriminante resta entro un decimo di punto di AUC",
                "**Il numero dei professionisti cambia moltissimo, la loro "
                "distinguibilita' quasi per niente.** A seconda di cosa si conti come "
                "professionismo gli eventi vanno da ventisei a centocinquantuno, ma "
                "l'AUC del percentile Under 19 oscilla di %s in tutto. Le conclusioni "
                "di questo studio non poggiano sulla definizione scelta."
                % md.num(osc, 3)),
            "",
            "La finestra d'eta' e' ancora meno influente: spostarla da ventiquattro a "
            "ventisei anni non cambia praticamente nulla, perche' quasi tutti i "
            "passaggi al professionismo avvengono prima. La soglia del «top» invece "
            "sposta l'AUC in modo sistematico — piu' e' selettiva, piu' il rendimento "
            "giovanile distingue — ed e' un risultato, non un artefatto: le soglie "
            "piu' alte selezionano atleti che erano gia' piu' forti da ragazzi."))

    manc = lt.tabella("sensibilita", "mancanti")
    if manc:
        p.append(md.paragrafo(
            "",
            "> **Sull'imputazione dei percentili mancanti.** La procedura standard "
            "sarebbe confrontare l'analisi sui casi completi con un'imputazione "
            "multipla. Qui non e' appropriata, e la ragione e' sostanziale: un "
            "percentile mancante non e' un dato perduto, e' un atleta che quella "
            "stagione non ha fatto punti. L'informazione c'e', ed e' negativa. Imputarla "
            "significherebbe attribuire un rendimento a chi non ne ha avuto."))
        righe_m = [[r[0], r[1], r[2], md.num(r[3], 2) + "%", md.num(r[4], 3)]
                   for r in manc["righe"]]
        p.append(md.tabella(
            ["popolazione", "professionisti", "atleti", "% pro", "AUC"],
            righe_m, nota=manc["nota"], colonne_conteggio=(1, 2)))
        p.append(md.paragrafo(
            "",
            "Il confronto corretto e' quello qui sopra, e conferma il ragionamento: "
            "trattare l'assenza come «sotto chiunque sia in classifica» **alza** la "
            "capacita' discriminante, perche' aggiunge informazione vera invece di "
            "inventarne. Le sezioni precedenti restano deliberatamente sui soli "
            "presenti, perche' li' la domanda e' quanto il *rendimento* predica, non "
            "quanto predica l'esserci."))

    f = lt.figura("validazione", "sensibilita")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    # --- STEP 27 --------------------------------------------------------------
    conf = lt.tabella("confronto_ml", "confronto")
    imp = lt.tabella("confronto_ml", "importanza")
    if conf:
        p.append(md.sezione("Un modello piu' complicato farebbe meglio?", 3))
        p.append(md.paragrafo(
            "E' l'obiezione piu' prevedibile: con dati longitudinali su migliaia di "
            "persone, una foresta casuale non troverebbe di piu'? La prova si fa sulle "
            "**stesse partizioni** — entrambi i modelli vedono gli stessi dati di "
            "addestramento e vengono misurati sugli stessi dati di verifica — e la "
            "foresta riceve tutte le celle invece di una sola, quindi parte avvantaggiata."))
        righe_c = [[r[0], r[1], md.num(r[2], 3), md.num(r[3], 3)] for r in conf["righe"]]
        p.append(md.tabella(conf["colonne"], righe_c, n=vm.get("n"), nota=conf["nota"]))

        diff = vm.get("differenza")
        if diff is not None:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    diff < 0.05,
                    "la foresta casuale non guadagna piu' di cinque centesimi di AUC "
                    "rispetto al modello a due parametri",
                    "**Guadagna %s di AUC, con %s predittori in piu'.** Il guadagno e' "
                    "costante fra le ripetizioni, ma non e' un confronto a parita' di "
                    "informazione — il paragrafo qui sotto dice perche' — e in ogni caso "
                    "e' piccolo: un "
                    "modello con due parametri cattura quasi tutto quello che c'e' da "
                    "catturare. E' l'argomento a favore della parsimonia, verificato "
                    "invece che affermato."
                    % (("%+.3f" % diff).replace(".", ","),
                       md.conta(conf["righe"][1][1] - conf["righe"][0][1])))))

        if imp:
            p.append(md.paragrafo(
                "",
                "Anche il modo in cui la foresta usa i dati e' istruttivo. In cima alla "
                "sua classifica di importanza c'e' proprio il percentile Under 19, che e' "
                "l'unico predittore del modello parametrico; al secondo posto il numero "
                "di stagioni corse, che questo studio esclude di proposito perche' e' un "
                "mediatore — chi va meglio resta di piu'. **Parte del piccolo vantaggio "
                "della foresta viene dall'usare una variabile che il modello parametrico "
                "rifiuta per ragioni di interpretazione, non di prestazione.**"))
            p.append(md.tabella(imp["colonne"], imp["righe"], nota=imp["nota"],
                                decimali=2))

    # --- STEP 17: la penalizzazione, l'altro modo di chiedere la stessa cosa ---
    pen = lt.tabella("penalizzato", "coefficienti")
    vp = lt.valori("penalizzato")
    if pen and vp:
        p.append(md.sezione("E se si usassero tutte le categorie insieme?", 3))
        p.append(md.paragrafo(
            "La foresta casuale risponde alla domanda «piu' complicato serve?» con un "
            "modello che nessuno saprebbe interpretare. C'e' un modo piu' diretto: "
            "mettere **tutte** le categorie dentro una regressione sola e lasciare che "
            "una penalizzazione decida quali tenere. Se le categorie portassero "
            "informazione distinta, ne sopravviverebbero diverse."))
        p.append(md.metodo(
            "Elastic net",
            "Una regressione con una penalita' sui coefficienti, che li tira verso zero "
            "e ne azzera alcuni del tutto. La forza della penalita' si sceglie per "
            "validazione incrociata, nella versione conservativa: la piu' forte il cui "
            "errore resta entro una deviazione standard dal minimo, cioe' il modello "
            "piu' parsimonioso fra quelli sostanzialmente equivalenti al migliore.\n\n"
            "Mescola due penalita': quella che restringe tutti i coefficienti e quella "
            "che ne azzera alcuni. Con predittori correlati come le categorie giovanili "
            "la miscela e' piu' stabile, perche' evita che il metodo scelga a caso una "
            "fra due variabili quasi identiche.\n\n"
            "Da un modello penalizzato **non si leggono p-value**: i coefficienti sono "
            "distorti verso zero per costruzione. Si guarda quali variabili "
            "sopravvivono e quanto vale la previsione.",
            [("Elastic net", W + "Elastic_net_regularization"),
             ("Regolarizzazione", W + "Regularization_(mathematics)")]))

        righe_p = [[r[0], "—" if r[1] is None else md.num(r[1], 2), r[2]]
                   for r in pen["righe"]]
        p.append(md.tabella(pen["colonne"], righe_p, n=vp.get("n"), nota=pen["nota"]))

        auc_p = vp.get("auc", {})
        p.append(md.paragrafo(
            "",
            md.afferma(
                vp.get("trattenuti", 99) <= 3,
                "la penalizzazione azzera quasi tutte le categorie e ne trattiene solo "
                "le ultime",
                "**Sopravvivono %s coefficienti su %s, e sono le due categorie piu' "
                "vicine al professionismo.** Tutte le altre vengono azzerate: una volta "
                "che si conosce il rendimento in %s, quello delle categorie precedenti "
                "non aggiunge abbastanza da giustificare il proprio posto nel modello."
                % (md.conta(vp.get("trattenuti")), md.conta(vp.get("totali")),
                   auc_p.get("cella", "Under 19"))),
            "",
            "E sulla previsione il guadagno e' minimo: %s di AUC rispetto al modello con "
            "la sola cella %s, sullo stesso sottocampione. E' la terza volta che questo "
            "documento arriva alla stessa conclusione per tre strade diverse — modelli "
            "annidati, foresta casuale, penalizzazione — e conviene prenderla sul serio, "
            "ricordando pero' che non sono tre prove indipendenti: annidati e "
            "penalizzazione girano su quasi lo stesso sottocampione, e solo la foresta "
            "vede tutti gli atleti. Detto questo: "
            "**quasi tutta l'informazione utile sta nell'ultima misura disponibile.**"
            % (("%+.3f" % auc_p.get("differenza", 0)).replace(".", ","),
               auc_p.get("cella", ""))))

        p.append(md.paragrafo(
            "",
            "*Con una riserva che vale piu' del risultato.* Il modello richiede tutte le "
            "categorie osservate sullo stesso atleta, e restano **%s atleti su %s**, fra "
            "cui %s professionisti: circa la meta' del sottocampione. Su un gruppo cosi' "
            "piccolo e cosi' selezionato le AUC non sono confrontabili con nessun altro "
            "numero del documento, e l'azzeramento delle prime categorie potrebbe in "
            "parte riflettere la scarsita' di dati piu' che la loro inutilita'. Resta "
            "che va nella stessa direzione di tutto il resto."
            % (md.conta(vp.get("n")), md.conta(vp.get("n_coorte")),
               md.conta(vp.get("eventi")))))

    p.append(md.paragrafo(
        "",
        "> **Come vanno lette le AUC di questa sezione.** Alcune sono calcolate su tutta "
        "la coorte, codificando l'assenza dalla classifica come una categoria, e sono "
        "percio' piu' alte di quelle delle sezioni precedenti, che girano sui soli "
        "atleti presenti. Non vanno messe a confronto fra sezioni: qui conta la "
        "**stabilita'** dei numeri fra una variante e l'altra, non il loro livello."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
