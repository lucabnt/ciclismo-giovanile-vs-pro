"""
La sintesi dello studio, in testa al documento.

PERCHE' E' UN MODULO E NON UN TESTO SCRITTO A MANO
    Una sintesi e' il pezzo che si copia: finisce nei post, nelle presentazioni, nelle
    mail. E' quindi il punto in cui una cifra sbagliata fa piu' danno, ed e' l'ultimo
    posto in cui si vorrebbe scriverla a mano.

    Qui non si calcola niente di nuovo. Ogni numero viene riletto dall'archivio, dal
    modulo che lo ha prodotto, cosi' che rigenerando il documento fra un anno la sintesi
    cambi insieme ai risultati invece di restare indietro.

PERCHE' STA PRIMA DI TUTTO
    E' la voce 2 della checklist TRIPOD, l'unica che era rimasta scoperta. Ma soprattutto
    e' quello che serve a chi apre un documento di centomila caratteri e deve decidere in
    trenta secondi se leggerlo.

COSA CI VA DENTRO
    Contesto, dati, metodi, risultati **positivi e negativi**, solidita', limiti. I
    risultati negativi in particolare: sono meta' di cio' che questo studio ha trovato, e
    una sintesi che li omettesse darebbe un'idea sbagliata di cosa i dati sostengono.
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
import lib_markdown as md                          # noqa: E402


def _p(x, decimali=3):
    """Un p-value dentro una frase."""
    if x is None:
        return "—"
    return "< 0,001" if x < 0.001 else md.num(x, decimali)


def _frase_porte(lt):
    """Le due porte d'ingresso, con tutti i numeri sulla stessa popolazione.

    La quota italiana e' calcolata sugli stessi professionisti del top 500 per porta,
    cioe' quelli presenti in classifica a diciotto anni. Prima era un 63% scritto a
    mano, su una popolazione piu' ampia, che nessuna rigenerazione avrebbe aggiornato.
    """
    porte = lt.valore("porta", "qualita_porte") or {}
    ita, est = porte.get("italiana"), porte.get("internazionale")
    if not (ita and est and ita.get("n") and est.get("n")):
        return ""
    return (" Una parte della spiegazione e' che la soglia non sia una sola: fra i "
            "professionisti presenti in classifica a diciotto anni, il %s%% debutta in "
            "una squadra a maggioranza italiana, e di questi arriva nel top 500 il %s%% "
            "contro il %s%% di chi debutta in una squadra straniera, mentre il "
            "rendimento giovanile predice le due porte allo stesso modo."
            % (md.num(100 * ita["n"] / (ita["n"] + est["n"]), 0),
               md.num(ita["quota"], 0), md.num(est["quota"], 0)))


def rendi(lt):
    # Tutto viene riletto dai moduli che lo hanno prodotto: questa sezione non calcola.
    prov = lt.valori("provenienza")
    att = lt.valori("attrito")
    cop = lt.valori("copertura")
    pas = lt.valori("passaggi")
    pun = lt.valori("punteggi")
    rae = lt.valori("rae")
    cor = lt.valori("correlazioni")
    con = lt.valori("contesto")
    uni = lt.valori("univariati")
    ann = lt.valori("annidati")
    met = lt.valori("metriche")
    sop = lt.valori("sopravvivenza")
    tra = lt.valori("traiettorie")
    qua = lt.valori("qualita")
    val = lt.valori("validazione")
    sen = lt.valori("sensibilita")

    if not att or not uni:
        return ""

    p = [md.sezione("In sintesi")]

    # --- contesto e obiettivo ------------------------------------------------
    p.append(md.paragrafo(
        "**Contesto.** La letteratura sulla transizione dal ciclismo giovanile al "
        "professionismo parte dall'Under 17 e trova che il rendimento diventa "
        "informativo avvicinandosi all'esito. Nessuno ha mai verificato se il risultato "
        "agonistico a tredici-quattordici anni predica l'accesso al professionismo su "
        "una popolazione ampia e non preselezionata — che e' pero' l'eta' in cui si "
        "prendono le prime decisioni di selezione.",
        "",
        "**Obiettivo.** Misurare da che eta' il piazzamento nelle classifiche giovanili "
        "italiane informa sull'accesso al professionismo, quanto informa, e cosa "
        "significherebbe usarlo per selezionare."))

    # --- dati -----------------------------------------------------------------
    st = prov.get("stagioni", ["—", "—"]) if prov else ["—", "—"]
    p.append(md.paragrafo(
        "",
        "**Dati.** Classifiche nazionali giovanili italiane, stagioni %s-%s: %s "
        "piazzamenti stagionali di %s atleti, con la data di nascita osservata per il "
        "%s%% di loro. Gli esiti di carriera vengono da ProCyclingStats, abbinati su "
        "nome e data di nascita. Le coorti principali sono i nati %s: **%s atleti, %s "
        "professionisti** (%s per mille di chi era in classifica da Under 15)."
        % (st[0], st[1], md.conta(prov.get("righe_classifica")) if prov else "—",
           md.conta(prov.get("atleti")) if prov else "—",
           md.num(100 * prov["nascite_osservate"] / prov["nascite_totali"], 1)
           if prov and prov.get("nascite_totali") else "—",
           att.get("coorti"), md.conta(att.get("atleti_totali")),
           md.conta(att.get("pro_totali")), md.num(att.get("pro_su_mille_u15"), 1))))

    # --- il denominatore, che e' il primo risultato ---------------------------
    if cop:
        p.append(md.paragrafo(
            "",
            "**Di chi si parla, e questo e' gia' un risultato.** Comparire in classifica "
            "richiede almeno un piazzamento nei primi cinque in una gara, e vi compare "
            "**circa un tesserato su %s** (media %s%%, stabile fra quattro categorie e "
            "le stagioni %s-%s). Ogni percentuale di questo studio ha quindi come "
            "denominatore un gruppo gia' selezionato, non l'insieme dei tesserati."
            % (md.conta(round(100 / cop["copertura_media"])),
               md.num(cop["copertura_media"], 1),
               cop.get("anni", ["—", "—"])[0], cop.get("anni", ["—", "—"])[1])))

    # --- metodi ---------------------------------------------------------------
    p.append(md.paragrafo(
        "",
        "**Metodi.** Il predittore e' il percentile entro cella `stagione x categoria x "
        "anno di categoria`. Regressione logistica con correzione di Firth per gli "
        "eventi rari; modelli annidati sullo stesso sottocampione con test di DeLong; "
        "modello di sopravvivenza a tempo discreto con legame cloglog ed errori standard "
        "raggruppati per atleta; modello misto per le traiettorie individuali; "
        "regressione ordinale per il livello di carriera raggiunto. Nessuna selezione "
        "automatica delle variabili: i modelli sono specificati dalla domanda."))

    # --- risultati positivi ---------------------------------------------------
    massima = uni.get("auc_massima", {})
    prima = uni.get("auc_prima", {})
    p.append(md.sezione("Cosa il rendimento giovanile predice", 3))
    p.append(md.paragrafo(
        "**Predice, e da subito.** Gia' al primo anno di Under 15 la separazione fra chi "
        "arrivera' e chi no e' appena sopra il confine convenzionale fra «medio» e "
        "«grande» (delta di Cliff %s). Il peso cresce con l'eta': dieci punti di "
        "percentile moltiplicano l'odds di diventare professionista per %s in %s e per "
        "%s in %s."
        % (md.num(pun["delta_primo"][2], 3) if pun else "—",
           md.num(prima.get("or"), 2), prima.get("cella", "—"),
           md.num(massima.get("or"), 2), massima.get("cella", "—"))))

    if ann:
        salto = ann.get("salto_maggiore", {})
        p.append(md.paragrafo(
            "",
            "**Fra gli atleti osservati in tutte le categorie, l'informazione si concentra "
            "nell'ultima misura disponibile.** Costruendo "
            "i modelli per aggiunte successive sugli stessi %s atleti, il salto maggiore "
            "e' **%s** (ΔAUC %s). Tre metodi concordano, e due dei tre girano su quasi lo "
            "stesso sottocampione: i modelli "
            "annidati, una foresta casuale con quindici predittori in piu' (che guadagna "
            "%s di AUC) e una regressione penalizzata su tutte le categorie insieme, che "
            "ne trattiene solo le due piu' vicine all'esito."
            % (md.conta(ann.get("n")), salto.get("modello", "—"),
               ("%+.3f" % salto.get("delta", 0)).replace(".", ","),
               ("%+.3f" % lt.valore("confronto_ml", "differenza", 0)).replace(".", ","))))

    if tra:
        auc_t = tra.get("auc", {})
        p.append(md.paragrafo(
            "",
            "**Il livello e' una condizione, il miglioramento un moltiplicatore.** "
            "Separando la traiettoria individuale in livello e pendenza, entrambi "
            "contano e la pendenza aggiunge informazione: l'AUC passa da %s a %s "
            "(p %s). Fra gli atleti di livello alto, chi stava anche migliorando e' "
            "arrivato al professionismo dieci volte piu' spesso di chi stava peggiorando; "
            "ma nel terzo di livello piu' basso il miglioramento non basta quasi mai."
            % (md.num(auc_t.get("livello"), 3), md.num(auc_t.get("completo"), 3),
               _p(auc_t.get("p")))))

    grezzo = lt.tabella("sopravvivenza", "hazard_grezzo")
    if sop and grezzo:
        cum = sop.get("cumulate", {})
        eta_picco = max(grezzo["righe"], key=lambda r: r[3])[0]
        p.append(md.paragrafo(
            "",
            "**Il passaggio ha una finestra stretta.** Nessuno diventa professionista "
            "prima dei %s anni — e' una regola, non un dato — e il rischio e' massimo a "
            "%s. Per un atleta che resta in classifica ogni stagione, la probabilita' di "
            "arrivare al professionismo vale %s%% con rendimento medio e %s%% con venti "
            "punti di percentile in piu'."
            % (md.conta(sop.get("eta_finestra", [0])[0]),
               md.conta(eta_picco),
               md.num(cum.get("medio"), 1), md.num(cum.get("alto"), 1))))

    # --- risultati negativi ---------------------------------------------------
    p.append(md.sezione("Cosa non predice, e cosa sembra predire senza farlo", 3))

    chiave = met.get("frase_chiave", {}) if met else {}
    if chiave:
        p.append(md.paragrafo(
            "**Predire non e' selezionare.** Selezionando il 10%% migliore della "
            "classifica %s si intercetta il **%s%% dei futuri professionisti**, ma il "
            "**%s%% dei selezionati non lo diventera'**. Con un esito che riguarda "
            "meno del 3%% della coorte, anche un ordinamento accurato produce in maggioranza "
            "falsi positivi: e' aritmetica della base, non un difetto del criterio."
            % (chiave.get("cella", "—"), md.num(chiave.get("sensibilita"), 0),
               md.num(100 - chiave.get("vpp", 0), 0))))

    stadi = lt.tabella("qualita", "stadi")
    if qua and stadi:
        primo_stadio = stadi["righe"][0][3]
        p.append(md.paragrafo(
            "",
            "**Predice l'ingresso, non la profondita' della carriera.** Sulla scala a "
            "quattro livelli il rendimento Under 19 moltiplica per %s l'odds di salire "
            "di gradino (IC 95%% %s-%s). Ma scomponendo il percorso in stadi successivi, "
            "il coefficiente vale %s per diventare professionista e scende a valori il "
            "cui intervallo di confidenza comprende l'uno per entrare nel top 500 fra i "
            "professionisti e nel top 100 fra i top 500: sui gradini successivi "
            "l'associazione non e' distinguibile dal caso, che non e' la stessa cosa "
            "che averne dimostrata l'assenza.%s"
            % (md.num(qua["ordinale"]["or"], 2), md.num(qua["ordinale"]["lo"], 2),
               md.num(qua["ordinale"]["hi"], 2), md.num(primo_stadio, 2),
               _frase_porte(lt))))

    if att and pas:
        p.append(md.paragrafo(
            "",
            "**Uscire dalla classifica non e' smettere.** Il **%s%%** degli atleti salta "
            "almeno una stagione e poi ricompare, e meta' dei classificati al secondo "
            "anno di Allievi non c'era al primo. Il crollo apparente al cambio di "
            "categoria — resta il %s%% contro il %s%% dei passaggi interni — non viene "
            "dalla scarsita' dei posti ma dalla concorrenza fra annate: la classifica di "
            "arrivo e' composta per il %s%% da chi c'era gia', contro il %s%% dei "
            "passaggi interni. Il confronto con i tesserati federali conferma "
            "dall'esterno che la classifica non si restringe piu' in fretta della "
            "popolazione che la genera."
            % (md.num(att.get("rientri_dopo_assenza"), 1),
               md.num(pas.get("resta_fra"), 1), md.num(pas.get("resta_dentro"), 1),
               md.num(pas.get("quota_fra"), 1), md.num(pas.get("quota_dentro"), 1))))

    if rae:
        dec = rae.get("decadimento", {})
        succ = rae.get("successo_professionisti", {})
        tutti = rae.get("successo_tutti_i_classificati", {})
        p.append(md.paragrafo(
            "",
            "**L'effetto dell'eta' relativa e' di accesso, non di talento.** Rispetto "
            "all'atteso demografico italiano — non all'uniforme — i nati nel primo "
            "trimestre sono **%s volte** i nati nel quarto in %s, e il vantaggio si "
            "spegne a **%s** in %s. Fra chi arriva al professionismo il rapporto e' %s, "
            "contro %s di tutti i classificati, e non si distingue dal caso (p %s): su "
            "%s atleti e' un indizio piu' che una prova. Chi seleziona presto premia la "
            "maturita' "
            "anagrafica, e quel vantaggio non si converte in carriera. I modelli lo "
            "confermano dall'altro lato: aggiungere l'eta' relativa non sposta il "
            "coefficiente del percentile in nessuna cella%s, e da sola l'eta' relativa "
            "arriva a un'AUC di %s."
            % (md.num(dec.get("prima_q1_su_q4"), 2), dec.get("prima", "—"),
               md.num(dec.get("ultima_q1_su_q4"), 2), dec.get("ultima", "—"),
               md.num(succ.get("q1_su_q4"), 2), md.num(tutti.get("q1_su_q4"), 2),
               _p(succ.get("p"), 2), md.conta(succ.get("n")),
               ("" if uni.get("rel_age_scarto_auc") is None
                else " (l'AUC si muove al massimo di %s)"
                     % md.num(uni["rel_age_scarto_auc"], 3)),
               md.num((uni.get("rel_age_prima_cella") or {}).get("auc_rel"), 3))))

    if con:
        p.append(md.paragrafo(
            "",
            "**Societa', mobilita' e regione non aggiungono nulla di leggibile.** Il "
            "gradiente della mobilita' sembra enorme — dal %s%% al %s%% di "
            "professionisti secondo il numero di cambi di societa' — ma a parita' di "
            "stagioni corse quasi sparisce. E il **%s%%** cambia societa' passando dagli "
            "Juniores all'Under 23, contro circa il %s%% dei passaggi interni a una "
            "categoria: e' organizzazione dello sport, non una decisione. La societa' di "
            "partenza va dal %s%% al %s%%, la regione non mostra differenze leggibili."
            % (md.num(con["mobilita_grezza_da_a"][0], 2),
               md.num(con["mobilita_grezza_da_a"][1], 2),
               md.num(con.get("cambio_juniores_u23"), 1),
               md.num(con.get("cambio_dentro_categoria"), 0),
               md.num(con["qualita_da_a"][0], 2), md.num(con["qualita_da_a"][1], 2))))

    # --- solidita' ------------------------------------------------------------
    pos = lt.valori("posti")
    rag = lt.valori("ragazze")
    if pos:
        gare = pos.get("gare_per_stagione") or {}
        quote = pos.get("quote_per_annata") or {}
        u15 = (quote.get("U15") or [(1, None)])[0][1]
        u17 = (quote.get("U17") or [(1, None)])[0][1]
        if gare and u15 and u17:
            p.append(md.paragrafo(
                "",
                "**Il primo anno di categoria non sparisce per mancanza di posti.** Dove "
                "ogni annata ha la propria classifica il primo anno ne vince il %s%%, "
                "dove la lista e' unica e le gare sono le stesse il %s%%: e' concorrenza, "
                "non scarsita'. I posti pero' calano davvero salendo di categoria, da %s "
                "classificazioni di gara per stagione in Esordienti a %s in Under 23, e "
                "calano anche nel tempo, con una perdita del %s%% fra la prima e l'ultima "
                "stagione osservata. La concentrazione dei punti invece non cambia mai: "
                "il decile migliore ne prende fra il %s%% e il %s%% a ogni eta'."
                % (md.num(u15, 1), md.num(u17, 1), md.conta(gare.get("U15")),
                   md.conta(gare.get("U23")), md.num(abs(pos.get("calo_massimo") or 0), 1),
                   md.num(pos.get("decile_minimo"), 1),
                   md.num(pos.get("decile_massimo"), 1))))

    if rag:
        sep = rag.get("separazione_quote") or {}
        rap = rag.get("rapporto_gare") or {}
        conf = rag.get("rapporto_gare_confrontabile") or {}
        sessi = (lt.valori("rae") or {}).get("sessi_prima_categoria") or {}
        if sep and sessi:
            p.append(md.paragrafo(
                "",
                "**Sul femminile si e' potuto misurare cio' che non richiede un esito.** "
                "Dove il conteggio e' confrontabile, il movimento corre fra %s e %s volte "
                "meno gare di quello maschile, e non ha una classifica Under 23. L'effetto "
                "dell'eta' relativa e' piu' debole che fra i maschi a tredici anni, %s "
                "contro %s sulle stesse coorti, coerente con una maturazione piu' precoce. "
                "E un cambio di regolamento della fonte conferma il meccanismo dei posti: "
                "separando le classifiche delle Esordienti nel %s, la quota del primo anno "
                "e' passata dal %s%% al %s%%, nella stessa categoria e alle stesse eta'."
                % (md.num(conf.get("minimo"), 1), md.num(conf.get("massimo"), 1),
                   md.num(sessi.get("femmine"), 2),
                   md.num(sessi.get("maschi"), 2), sep.get("anno"),
                   md.num(sep.get("prima"), 1), md.num(sep.get("dopo"), 1))))

    p.append(md.sezione("Quanto sono solidi questi risultati", 3))
    pezzi = []
    if val:
        pezzi.append(
            "L'ottimismo dei modelli, stimato con %s ricampionamenti bootstrap, e' al "
            "massimo di %s punti di AUC contro una soglia di allarme di 0,05, e le "
            "pendenze di calibrazione sono a ridosso di 1. Addestrando sulle coorti piu' "
            "vecchie e verificando sulle piu' recenti la capacita' discriminante non "
            "cala."
            % (md.conta(val.get("ripetizioni")), md.num(val.get("ottimismo_massimo"), 3)))
    if sen:
        pezzi.append(
            "Cambiando la definizione di professionista gli eventi passano da ventisei a "
            "centocinquantuno, ma l'AUC oscilla di %s in tutto; spostare la finestra "
            "d'eta' da ventiquattro a ventisei anni non cambia praticamente nulla."
            % md.num(sen.get("oscillazione_auc"), 3))
    if cor:
        pezzi.append(
            "Il fattore di inflazione della varianza massimo e' %s, sotto la soglia di "
            "5: le categorie portano informazione abbastanza distinta da poter essere "
            "usate insieme." % md.num(cor.get("vif_massimo"), 2))
    if uni.get("scarto_controllo") is not None:
        pezzi.append(
            "Le AUC dei modelli univariati coincidono con quelle ricavate dal delta di "
            "Cliff per via puramente descrittiva entro %s: due strade indipendenti per "
            "la stessa quantita'." % md.num(uni["scarto_controllo"], 4))
    p.append(md.paragrafo(" ".join(pezzi)))

    # --- limiti ---------------------------------------------------------------
    p.append(md.sezione("Limiti", 3))
    p.append(md.paragrafo(
        "**Il limite principale e' cosa la fonte non contiene.** Nessuna delle fonti "
        "pubblica altezza, peso, specialita', volume di allenamento o numero di gare "
        "disputate: di ogni atleta si conosce il piazzamento, non come ci sia arrivato. "
        "Ogni conclusione vale **a parita' di cio' che la classifica registra**, che e' "
        "meno di cio' che un allenatore vede.",
        "",
        "Il livello di carriera piu' alto poggia su pochi casi, e sugli stadi successivi "
        "al professionismo si puo' dire che **non si vede** un effetto, non che non ci "
        "sia. Il denominatore dei tesserati esiste solo dal 2018 e non e' disponibile per "
        "regione, il che lascia aperta l'unica domanda geografica che varrebbe la pena "
        "porre. La parte predittiva dello studio riguarda i **maschi**: sul femminile si "
        "e' misurato tutto cio' che non richiede un esito di carriera, ma l'esito stesso "
        "non e' confrontabile, perche' le divisioni professionistiche femminili nascono "
        "nel 2020 e prima esisteva una categoria sola."))

    # --- conclusione ----------------------------------------------------------
    p.append(md.sezione("Conclusione", 3))
    p.append(md.paragrafo(
        "Il risultato agonistico a tredici anni **non e' rumore**: separa gia' in modo "
        "marcato chi arrivera' al professionismo da chi no, e la separazione cresce fino "
        "all'Under 19, dove si concentra quasi tutta l'informazione utile. Ma la stessa "
        "misura che predice bene **seleziona male**: qualunque soglia si scelga, la "
        "maggioranza dei selezionati non diventera' professionista, e la maggior parte "
        "di chi esce dalla classifica non ha smesso di correre.",
        "",
        "La lettura pratica non riguarda i ragazzi ma chi li guarda: la classifica "
        "giovanile e' uno strumento ragionevole per decidere **chi seguire**, e uno "
        "strumento pessimo per decidere chi lasciare andare."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
