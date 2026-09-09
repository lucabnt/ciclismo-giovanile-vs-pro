# Cose da fare

Elenco di lavoro. Ogni voce dice **cosa**, **perché** e **come verificare di averla chiusa**.
Le voci chiuse restano, barrate e con la data: servono a ricostruire perché una scelta è
stata fatta, che è metà del valore di questo file.

## Concluso

| Data | Voce | Esito |
|---|---|---|
| 30 ago | **riscritte le otto bozze in italiano** | la prima stesura era inglese tradotto: 122 trattini lunghi in 15 000 parole, paragrafi di una riga a effetto, «non è X, è Y» 46 volte. Regole in `post/STILE.md`, ricavate dalla prosa italiana dell'autore e dai post del suo blog. Il controllo delle cifre ora normalizza grassetti e a capo, così una riscrittura non lo fa fallire trenta volte |
| 30 ago | registro colloquiale | secondo passaggio, deciso dopo il primo: «tu» al lettore in tutta la serie, prima persona per le scelte di chi scrive, impersonale quasi eliminato. La sintassi italiana del passaggio precedente resta |
| 7 set | **titoli scelti** | Quattro post passano alla versione discorsiva: il terzo diventa «perché il primo anno di categoria sembra un massacro», il quinto «conta dove sei o dove stai andando?», il settimo «il mese di nascita, la squadra, la regione», l'ottavo «il ciclismo femminile». Allineati intestazioni dei file, piano editoriale e note sulle scelte aperte. **Resta da sciogliere l'ottavo**: unito al prefisso della serie ripete la parola *ciclismo*, e in `post/TITOLI.md` ci sono tre modi di toglierla |
| 7 set | **revisione del post 1 applicata** | Sciolte le due note lasciate nel testo: il titolo di sezione non sentenzia più («Cosa questi studi non dicono»), e il paragrafo sulle limitazioni della letteratura ora ammette che **valgono in pieno anche per questo studio**, con la sola differenza di averle misurate invece di lasciarle implicite. Corretti il refuso e le righe fuori misura, ricucito il passaggio rimasto senza attacco dopo i tagli, titolo allineato a «Cosa sappiamo già, e cosa no» in tutti i file. Rimpaginati i nove post, che note e link avevano allungato oltre le novanta colonne. Le due lezioni sono ora regole in `post/STILE.md` |
| 7 set | **riferimenti completi nei post** | Le fonti esterne ora hanno autori, anno, titolo, rivista e DOI cliccabile: completate le schede di Mostaert, Voet, Filipas e Menaspà, e aggiunti i riferimenti che mancavano del tutto (Hasselaar nel post 2, Firth e DeLong nel 4, Harrell nel 9, la tavola Eurostat `demo_fmonth` nel 7 e nell'8). I rimandi interni sono diventati link completi a GitHub, 37 in tutto, tutti verificati contro `git ls-files`. **Corretto anche l'indirizzo del repository**, che in `LICENSE-CONTENT.md` era `ciclismo-giovanile-pro` invece di `ciclismo-giovanile-vs-pro` |
| 7 set | **figure web: sovrapposizioni corrette** | Le legende finivano sulle etichette dell'asse appena i testi venivano ingranditi per il web. Nuovo `gr.legenda()`, che le colloca a distanza sicura sotto il grafico; la rotazione delle etichette scatta ora sopra i dodici caratteri invece che sopra i sette, e non tocca mai quelle su due righe; il salvataggio web usa `bbox_inches="tight"`. Rifatta la figura della concentrazione a barre raggruppate, che aveva dieci etichette lunghe accavallate, e tolte le sigle `U15`/`U17` dalle figure del RAE in favore dei nomi italiani |
| 7 set | **segnaposto delle immagini nei post** | Ogni post ha adesso, nel punto in cui va, un segnaposto con didascalia e testo alternativo proposti: trenta in tutto, cioè le venti figure che l'analisi già produce, otto fotografie da procurare per le copertine e due grafici da disegnare: quello del post 1, che di figure non ne aveva nessuna, e l'apertura del post 5. Le didascalie sono state riscritte perché aggiungessero qualcosa invece di ripetere il paragrafo accanto. La convenzione e la regola sui volti dei minori stanno in `post/STILE.md` |
| 7 set | **le fonti mancanti del post 1** | Tre studi comparivano nel testo senza nota: quello spagnolo e quello belga sui risultati in gara, citati solo nell'elenco dei paesi, e i due che portano una cifra, cioè il 15% italiano di Cesanelli e i cinque su quarantotto di Hasselaar. Ora l'elenco dei paesi ha una nota che dice quale studio è quale, con il riferimento completo dei due che nel testo non tornano più, e le due cifre hanno la loro. Corretta anche l'attribuzione del 15%, che riguarda i primi dieci della classifica Allievi e non gli Allievi in generale, e il futuro «faranno punti» diventato passato come il resto del pezzo. Nel post 2 le iniziali di Hasselaar erano sbagliate |
| 8 set | **niente a capo dentro i paragrafi dei post** | I nove file passano da 2 195 a 1 237 righe: un paragrafo, una riga. Gli a capo servivano a leggere il sorgente, ma i post si incollano in un blog, dove possono diventare interruzioni di riga vere. Tabelle, intestazioni, elenchi, campi dell'intestazione e dei segnaposto e definizioni delle note restano su righe proprie; il testo è identico parola per parola, verificato contro la versione precedente. La regola è in `post/STILE.md`, così una rimpaginazione futura non le rimette |
| 8 set | **ogni output è datato** | Il documento e l'archivio già lo erano; adesso anche le figure e i post. Le figure del documento portano «elaborazione del <data>» in basso a destra, scritta da `gr.salva()`, perché un PNG ritagliato viaggia da solo e la data del documento non lo segue. Le versioni per il web no, per una ragione estetica: stanno dentro un post che ha già la sua data, e lì la riga di servizio si vedrebbe. L'intestazione dei nove post porta la data dell'analisi contro cui sono stati verificati, e la timbra `11_verifica_documenti.py` quando il controllo passa: non si scrive a mano, e se le cifre divergono non avanza. Rigenerate tutte e quarantaquattro le figure |
| 8 set | **il repository pubblica solo la prova** | Fuori dall'indice quattro cose che restano sul disco: `output/figure_web/`, cioè le stesse figure con i testi ingranditi per il blog, che pesavano da sole due megabyte; `archive/`, le quattro guide superate che la storia di git conserva comunque; `docs/post/` e `docs/piano_post.md`, che sono il prodotto e non la prova — ogni loro cifra è controllata contro l'archivio, quindi la prova sono l'archivio e `output/analisi.md`. Da 127 file e 5,1 MB a **89 file e 2,6 MB**. Aggiornati `README.md`, `LICENSE-CONTENT.md` e i link di questo registro; `11_verifica_documenti.py` salta i post se non li trova e non timbra niente, provato su una copia che contiene solo i file tracciati |
| 8 set | **la figura del post 1** | Il primo post non aveva figure proprie, perché non ha dati propri. Ne ha adesso una che ridisegna le due percentuali di Schumacher 2006, il 30% in avanti e il 29,4% all'indietro, con la fonte scritta dentro l'immagine. Sta in `output/esterne/` insieme allo script che la produce, e **né l'una né l'altro entrano nel repository**: non sono un risultato di questo studio e non devono sembrarlo. `output/` è già ignorato tranne le tre eccezioni dichiarate, quindi la cartella resta fuori da sola |
| 9 set | **accolta la revisione consolidata di `analisi.md`** | Tredici voci applicate. **Conteggi**: nuova sezione «Quanti professionisti, e perché i conteggi non coincidono», generata dall'archivio, che mette in fila le sei popolazioni dello studio con il motivo di ciascuna; il 78 di `definizioni.md` è precedente alla verifica manuale degli abbinamenti e la differenza di uno non è ricostruibile, e questo è scritto invece di essere spiegato a posteriori. **Formulazioni**: sui gradini oltre l'ingresso l'associazione «non è distinguibile dal caso», non «non c'è»; nella sopravvivenza domina «il restare nella popolazione osservata» e non «l'esserci»; la concentrazione dei punti non dimostra che si piazzino le stesse persone; le gare stimate diventano «classificazioni di gara»; il guadagno della foresta casuale è dichiarato come non ottenuto a parità di informazione, e modelli annidati e penalizzazione non sono due prove indipendenti. **Dichiarazioni mancanti**: il valore predittivo negativo, che era già in archivio e non veniva stampato; l'assenza di correzione per confronti multipli; il test di Brant sostituito dall'ispezione delle soglie; il percentile che non sa quante gare hai corso; ciclismo.info come aggregatore e non archivio federale. **Due bug di formattazione**: «10%%» in una stringa non formattata e «2,817» prodotto da un separatore delle migliaia fatto a mano che il normalizzatore dei decimali rileggeva come virgola. **Femminile**: l'Under 23 «non esiste» diventa «non esiste nel periodo studiato», perché la categoria si sta strutturando. Aggiornati di conseguenza i post 2, 4 e 8, e aggiunta alla guida la sezione «Aggiornamento successivo alla verifica della fonte», che dichiara superata l'armonizzazione con PCS |
| 9 set | **l'assenza dalla classifica è informativa solo tardi** | Analisi nuova, nata da una voce della revisione: il confronto «l'assenza vale meno di qualunque percentile» esisteva solo per l'Under 19, e ora `scripts/10_sensibilita.py` lo esegue anche in Under 15 primo anno. Il risultato **rovescia il segno**: a diciotto anni trattare l'assenza come «sotto tutti» alza l'AUC da 0,889 a 0,943, a tredici la abbassa da 0,736 a 0,694. Il motivo è nella colonna dei professionisti — a tredici anni ne sono in classifica 59 su 77, a diciotto 74 su 77 — quindi mandare in fondo tutti gli assenti, alle età basse, sbaglia posizione a quasi un quarto di quelli che poi arriveranno. È la misura più precisa che abbiamo del fatto che sparire da una classifica a tredici anni non sia un verdetto. **Correggeva anche un errore già scritto**: il post 4 affermava che includendo gli assenti la separazione a tredici anni sale, ed è falso. Tre nuove cifre entrano nel controllo automatico |
| 9 set | **i post allineati alle correzioni** | Passata in rassegna tutta la serie per vedere dove le correzioni all'analisi lasciavano un post a dire un'altra cosa. Nel **4** la separazione a tredici anni non è più «già grande» ma «sul confine fra media e grande», come dice il documento; nel **6** il coefficiente che domina non è più «l'esserci» ma «il restare in classifica»; nel **9** le conclusioni «reggono a tutte le definizioni che ho provato» invece di non poggiare sulle mie scelte, e il **2** dice ora che ciclismo.info non è l'archivio della federazione. Nel **9** sono entrate due cose che mancavano del tutto: la quarta verifica sull'assenza, che il post 4 prometteva senza che nessuno la mantenesse, e la qualità dell'abbinamento con ProCyclingStats. Sei cifre nuove nel controllo automatico, che adesso sono 122 |
| 9 set | **il 30% di Schumacher non esiste** | L'abstract dello studio del 2006, letto per intero, riporta **34%** in avanti e **29,4%** all'indietro: il 30% veniva dalla letteratura secondaria e nello studio non c'è. Cadono con esso altre due cose che il post ripeteva: la direzione prospettica non porta al Mondiale élite ma alle grandi gare élite, e lo studio non riguarda la sola strada — 27 454 risultati, 8 004 atleti, 108 paesi, più discipline. Riscritti apertura, numero chiave e figura del post 1, corretta la scheda A1 della rassegna e aggiunta l'appendice con la verifica. «Sette predestinati su dieci» diventa «due su tre», anche fra i titoli alternativi |
| 9 set | **accolta la revisione di letteratura e post 1** | Sedici voci. Nella **rassegna**: Svendsen non dimostra il primato della gara sul laboratorio (entrambe le famiglie separano i gruppi, il confronto diretto non esiste) e le sue «ore di allenamento» sono ore di gara; i due ciclisti da 414 punti di Hasselaar sono un esempio costruito e non due casi osservati, il rapporto è 3,6 e non «quasi quattro», e il 5 su 48 è un tasso di popolazione da non mettere in fila con i tassi di transizione; Mostaert spiega il 22,6% del rendimento due anni dopo, non delle differenze fra i ragazzi, e la storia di gare è fra i suoi predittori; allineata la dichiarazione su quali testi integrali sono stati letti, che §1 e appendice davano diversa. Nel **post 1**: i posti al Mondiale non sono sei fissi, Valenzuela entra come eccezione esplicita sui test di laboratorio, i tre tassi hanno ora il loro denominatore attaccato, il RAE separa chi entra da chi arriva, Filipas «trova molto poco» e non «pochissimo», e la nota che lo cita aveva **gli autori sbagliati**. Otto puntate diventano nove |
| 9 set | **opinabili dal 6 in su** | La rivendicazione di originalità ora specifica «su una popolazione ampia e non preselezionata» nella frase che la fa, non in quella dopo. Il collider bias è nominato. Cesanelli legge la stessa fonte di questo studio, e adesso lo dice il corpo e non la nota. «Nessuno è riuscito a smentirlo» diventa «negli studi che ho letto». Aggiunto il tetto dei modelli di apprendimento automatico, che chiude in anticipo l'obiezione sull'intelligenza artificiale. E due cose per il sito: le **meta description** dei nove post in `post/TITOLI.md`, e i **testi alternativi delle venti figure riscritti con i valori dentro** — cambiando la regola in `post/STILE.md`, che diceva il contrario ed era sbagliata |
| 9 set | **applicate le opinabili da 7 in su** | Il delta di Cliff nella sintesi diceva «grande» dove il corpo dice «sul confine fra medio e grande»: allineati. La riga più citabile della sintesi ora dichiara che vale «fra gli atleti osservati in tutte le categorie». I tre metodi non sono più «indipendenti», perché due girano sullo stesso sottocampione. Le conclusioni «reggono a tutte le definizioni che ho provato» invece di non poggiare sulla definizione. Dichiarato perché le finestre d'età dei due esiti sono 25 e 26 anni. Nel post 4, dove si dice che il secondo anno di categoria discrimina meglio del primo, è aggiunto che in Allievi la differenza non regge a un test (p = 0,099): `analisi.md` lo diceva già, il post no. E la qualità dell'abbinamento con ProCyclingStats — 707 esatti su 727, nessun ambiguo, 18 date corrette — passa da `da_fare.md` al documento, calcolata da una query invece che copiata |
| 7 set | **`output/` viene pubblicato** | Era escluso da git, ma i post rimandano al documento tecnico dicendo che è pubblico, e chi clona il repository non può rigenerarlo, dato che il database di partenza resta privato. Ora `analisi.md`, `risultati.db` e le due cartelle di figure sono versionati (3,3 MB) e il controllo privacy li attraversa: 127 file, nessun dato personale |
| 7 set | **contaminazione dell'archivio femminile, trovata e bloccata** | Per la stagione 2026 l'indice `s=women` di PCS ignora il filtro e restituisce le WorldTeam **maschili**: diciotto squadre erano finite in `pcs_F.db` senza che nulla lo segnalasse. Aggiunta la guardia `classi_attese_F` in `config.toml`, che scarta le squadre di classe non attesa e le registra nel log; archivio ripulito. È lo stesso difetto già noto per `--continental` (l'indice ignora l'anno per le stagioni future) |
| 7 set | **sequenza completa di riesecuzione nel README** | Nuova sezione «Rieseguire tutto da zero»: dodici passi in ordine con durata e scopo, le due trappole note, i due controlli pre-commit e la catena femminile con `SESSO=F`. Prima l'ordine si ricostruiva leggendo quattro sezioni diverse |
| 7 set | **verifica di coerenza su tutto il progetto** | Controllati: note a piè di pagina (tutte definite, nessuna orfana), figure citate (tutte esistenti), ancore dell'indice (58, nessuna rotta), apostrofi e accenti nel documento generato, premesse cadute (nessuna), sintassi di 37 file Python, moduli in `config.toml` contro i file presenti, riferimenti incrociati fra i post dopo la rinumerazione a nove. **Trovati e corretti quattro problemi**: la sintesi ripeteva il vecchio meccanismo del crollo («l'accorciarsi della lista») e dichiarava il femminile come «non fatto»; il README contava ancora otto post e dieci documenti a mano; il conteggio delle gare non era confrontabile fra Esordienti (due calendari sommati) e categorie a lista unica, e ora porta la cautela; due figure erano dichiarate nel post sbagliato |
| 30 ago | **nuovo modulo `ragazze` e nona puntata** | La serie passa a nove post: «E le ragazze?» sta fra i falsi indizi e le conclusioni. Il risultato migliore è un esperimento naturale: le Esordienti femminili sono passate da una classifica unica a due separate nel 2022, e la quota dei posti del primo anno è salita **dal 28,5% al 49,6%**. Stessa categoria, stesse ragazze: conferma il meccanismo trovato sui maschi dentro la stessa popolazione. Il movimento femminile è 7,4 volte più piccolo ma corre 8,3 volte meno gare, e il suo calendario **non** cala come quello maschile |
| 30 ago | **scaricato l'archivio PCS femminile** | `data/pcs/pcs_F.db`: 432 squadre-stagione, 6 120 righe di rosa, 8 000 righe di classifica mondiale, 504 richieste in 22 minuti. 150 italiane distinte a ranking, **51 nelle rose di prima e seconda divisione 2020-2025**. |
| 30 ago | **tre problemi della fonte femminile, da decidere prima di procedere** | ① le divisioni nascono nel 2020: prima c'è una categoria sola (`UCI`), quindi l'esito PRO non è definibile allo stesso modo e le coorti utilizzabili partono dalle nate attorno al 1998; ② l'indice `s=women` restituisce **solo la prima divisione** per le stagioni 2020-2024 — la seconda compare solo dal 2025, quindi la seconda divisione è incompleta e servirebbe una passata con un indice diverso; ③ per il 2026 l'indice restituisce 18 squadre **maschili** (`WT`), che vanno escluse. **Proposta**: definire PRO femminile come prima divisione (`WTW`), che è consistente dal 2020 in poi, e dichiarare il resto come limite. |
| 30 ago | **catena femminile collegata** | `config.toml` distingue scaricamento ed esiti per sesso; `04`, `05` e `06` leggono il sesso da `sesso_in_studio()`, che accetta l'override `SESSO=F` per far girare la catena femminile senza toccare la configurazione. Archivio PCS separato (`data/pcs/pcs_F.db`), e il matching filtra per sesso. **Verificato sulle pagine di PCS**: l'indice femminile è `s=women` (uno solo, 22 squadre nel 2025) e le classi sono `WTW` e `PRW` |
| 30 ago | **revisione trasversale dei post** (priorità 3) | definizioni ricordate nel testo alla prima menzione, non in un riquadro (il riquadro era la prima versione, scartata: un glossario prima di aver detto di cosa si parla non si legge); note a piè di pagina con la fonte di ogni tabella, figura e blocco di numeri, che rimandano al modulo o allo script che li produce; citazioni della letteratura con DOI; tolte le formulazioni che attribuivano a qualcuno la mancata pubblicazione dei dati. Regole in `post/STILE.md` |
| 30 ago | tre risposte dentro i post | vittorie a parità di punti (nessun andamento coerente, post 2); continuità dei professionisti (durano molto di più ma non sono più stabili nel livello, post 3); cosa include e cosa non include il 74% a tredici anni (post 4) |
| 30 ago | **i post sono cresciuti oltre il target** | da 1 200-1 800 parole a 1 500-2 280. Le aggiunte sono richieste (definizioni, fonti, risposte), ma il piano editoriale dichiara ancora il vecchio intervallo: **da decidere** se alzare il target o tagliare, e dove |
| 30 ago | preparato lo scaricamento del femminile | `config.toml` ha ora `[scaricamento.M]` e `[scaricamento.F]`: livelli di squadra e parametro della classifica mondiale non sono più cablati in `04_scarica_pcs.py`. **Da fare prima del primo uso**: verificare che gli slug femminili (`womens-worldtour`, `womens-proteams`, `womens-continental`) corrispondano alle pagine di PCS, che hanno cambiato nome più volte dal 2020. Le soglie di qualità femminili sono proposte in `definizioni.md` |
| 30 ago | **da quale porta si entra** (priorità 2) | nuovo modulo `porta`: il 63% dei professionisti debutta in una squadra a maggioranza italiana. Il ranking predice le due porte allo stesso modo (0,863 contro 0,867), quindi la versione forte dell'ipotesi «bacino nazionale» non regge; ma di chi entra da una squadra italiana arriva nel top 500 il 33% contro il 59% di chi entra da una straniera. «Diventare professionista» non è un evento solo |
| 30 ago | **il calendario giovanile si è quasi dimezzato** | trovato contando le gare: fra il 2009 e il 2025 le classificazioni calano del 39,7% in Esordienti e del 58,3% in Under 23, e il calo è cominciato prima del covid. Dal 2018, dove il confronto è possibile, i tesserati Esordienti calano di un decimo e le gare di quasi un quinto. **Da approfondire**: il dato è una stima indiretta dai piazzamenti, e una conferma dal calendario federale lo renderebbe pubblicabile con più forza |
| 30 ago | **struttura delle liste: correzione** | Esordienti ha due classifiche separate per annata, le altre categorie una sola. Le sezioni `passaggi` e `univariati` attribuivano il crollo del primo anno alla scarsità di posti: è concorrenza fra annate. Corrette, insieme ai post 2, 3 e 4 |
| 30 ago | **nuovo modulo `posti`** | quanti posti mette in palio ogni categoria (dai piazzamenti: 640 classificazioni di gara per stagione in Esordienti, 146 in Under 23), come si dividono fra le annate (49,7% al primo anno dove le liste sono separate, 26,7% dove sono unite) e quanto sono concentrati i punti (il decile migliore ne prende il 37-43%, uguale a ogni età) |
| 30 ago | **effetto dell'età relativa sulle atlete** | in `rae`: sulle stesse coorti e con lo stesso atteso, Q1/Q4 vale 1,98 fra i maschi e 1,51 fra le femmine in Esordienti, e in Allieve non si distingue più dall'atteso. Coerente con la maturazione più precoce. **È l'unica analisi femminile possibile**, e non per numerosità: gli esiti di carriera femminili non sono mai stati raccolti da PCS |
| 30 ago | **licenza per la pubblicazione** | MIT per il codice ([`LICENSE`](../LICENSE)), CC BY 4.0 per i contenuti ([`LICENSE-CONTENT.md`](../LICENSE-CONTENT.md)). Dichiarato esplicitamente che i dati di partenza non sono nostri e non vengono ridistribuiti. **Restano due cose da decidere prima di pubblicare**: il nome del titolare del copyright (ora è l'handle `lucabnt`) e la paternità di `guida_metodologica_v5.md` e `docs/literature_review.md`, che sono licenziati come nostri |
| 30 ago | verifica delle nove schede sui testi integrali | **chiusa senza farla**: i testi non sono pubblicamente accessibili. Le schede restano fondate su abstract, la rassegna lo dichiara e nessuna conclusione dello studio vi poggia sopra |
| 30 ago | **bozze di tutti gli otto post** | `docs/post/`: testo per esteso, ciascuno con le proprie «scelte aperte» in fondo. Le cifre citate sono controllate da `11_verifica_documenti.py`, che ora copre anche i post |
| 30 ago | pacchetti R nel `requirements.txt` | mancavano `glmnet`, `lme4` e `randomForest`: chi seguiva il file si fermava a metà catena. Aggiunta anche la riga di `grep` che verifica se la lista è rimasta indietro rispetto al codice |
| 28 ago | **A1** configurazione esterna | `config.toml` letto da tutti gli script tramite `lib_giovanile.cfg()` |
| 28 ago | **B1** `elite_seasons` → `elite_seasons_a_punti` | rinominata anche `racing_after_u23` → `punti_dopo_u23` |
| 28 ago | **C4** coorti dei modelli annidati | coorti diverse per domande diverse; il sottocampione da 94 atleti contiene 43 eventi |
| 28 ago | **C5** verifica manuale del matching | 24 casi annotati, 18 correzioni di data, 0 ambigui residui |
| 28 ago | esiti in `tab_b` | nuovo `06_esiti.py`: `PRO`, `tier`, `team_quality_first` |
| 28 ago | fusioni da refuso | 6 quasi omonimi con data identica, più 1 spezzato da un doppio spazio |
| 28 ago | **D3** R o Python | R per i modelli, Python per preparazione e report, SQLite come confine |
| 28 ago | **D1-D2** livello di produzione | `report/` con archivio dei risultati, libreria grafica, generatore Markdown; primo modulo (`rae`) completo |
| 28 ago | **C1** attesi demografici | `07_riferimenti.py` scarica Eurostat `demo_fmonth` e lo mette in cache |
| 28 ago | **STEP 9** attrito | modulo `attrito`: imbuto, età di uscita, esiti; due figure |
| 28 ago | **STEP 15** effetto dell'età relativa | modulo `rae`: composizione, successo, gradiente per categoria |
| 28 ago | **STEP 11** correlazioni e VIF | modulo `correlazioni`: VIF massimo 2,89, la penalizzazione **non** è obbligatoria |
| 28 ago | **STEP 10** punteggi per gruppo | modulo `punteggi`: delta di Cliff da 0,47 a 0,78; già «grande» a tredici anni |
| 28 ago | **STEP 13-14** contesto e mobilità | modulo `contesto`: il gradiente della mobilità è un artefatto della durata della carriera |
| 28 ago | indice e riquadri metodologici | indice generato dai titoli; nove riquadri «Come si misura» con rimandi verificati |
| 28 ago | accenti nel testo generato | `report/accenti.py`: gli accenti si applicano alla generazione, non a mano sul file |
| 28 ago | **FASE 3** confine verso R | `scripts/08_prepara_modelli.py` costruisce `modelli.db`; `R/lib_risultati.R` scrive nello stesso archivio |
| 28 ago | **STEP 16** modelli univariati | `R/16_univariati.R`: OR da 1,40 a 2,28 per 10 punti; AUC coincidenti con la descrittiva entro 0,0005 |
| 28 ago | la critica di Hasselaar, verificata sui nostri dati | `R/30_misura.R`: la fonte italiana pesa le gare per livello dai Juniores in su (punti per piazzamento da 2,67 a 4,17); i pari merito sono fino al 95%, ma scioglierli non migliora la previsione in nessuna cella |
| 28 ago | **verifica bloccante su Cesanelli** risolta | le età non sono nel paper, ma il «Youth-U16» sono gli Allievi: usano stagioni dal 2007 e la classifica Esordienti esiste solo dal 2009. Il Gap 1 regge |
| 28 ago | rassegna integrata con cinque testi integrali | Cesanelli, Van Bulck, Voet, Valenzuela, Hasselaar: nessun errore di fatto, ma tre schede cambiano di peso e il Gap 3 va riformulato |
| 28 ago | rassegna della letteratura | importata in `docs/literature_review.md` con appendice di revisione: una verifica bloccante su Cesanelli, tre imprecisioni minori, tre studi da valutare, due gap in più |
| 28 ago | figure per il web | `output/figure_web/`: stesse figure con testi ingranditi, linee più spesse, etichette inclinate e doppia risoluzione |
| 28 ago | avvisi sui documenti statici | i file che non si rigenerano lo dichiarano in testa; `scripts/11_verifica_documenti.py` confronta le loro cifre con l'archivio |
| 28 ago | **voce 2 TRIPOD** la sintesi | `report/moduli/sintesi.py`: abstract generato in testa al documento, ogni cifra riletta dall'archivio del modulo che l'ha prodotta |
| 28 ago | piano editoriale | `docs/piano_post.md`: otto post per tema, con il filo conduttore e la mappa verso i moduli |
| 28 ago | **STEP 17** elastic net | `R/17_penalizzato.R`: su 82 atleti con tutte le celle, la penalizzazione trattiene solo U19y2 e U23y1 e guadagna +0,015 di AUC |
| 28 ago | **4a** provenienza dichiarata | nuova sezione «Da dove vengono i dati» nel documento, con conteggi calcolati e limiti espliciti |
| 28 ago | controllo delle cifre TRIPOD | `scripts/11_verifica_tripod.py`: le otto cifre copiate nella checklist vengono confrontate con l'archivio |
| 28 ago | **STEP 24-25** validazione | ottimismo ≤ 0,001, calibrazione 1,01-1,02, e sulle coorti di verifica l'AUC non cala |
| 28 ago | **STEP 26** sensibilità | `scripts/10_sensibilita.py`: gli eventi vanno da 26 a 151 secondo la definizione, l'AUC oscilla di 0,069 |
| 28 ago | **STEP 27** confronto ML | la foresta casuale guadagna +0,013 di AUC con 15 predittori in più, e in parte usando un mediatore |
| 28 ago | **STEP 28** TRIPOD | `docs/tripod.md`: 35 voci, tre non pienamente coperte e tutte reali |
| 28 ago | **STEP 22-23** qualità della carriera | `R/22_qualita_carriera.R`: il rendimento Under 19 predice l'ingresso (OR 2,47) ma non il livello raggiunto una volta dentro (OR 1,20 e 1,28, intervalli che comprendono l'uno) |
| 28 ago | **STEP 21** traiettorie | `R/21_traiettorie.R`: livello e miglioramento contano entrambi, AUC 0,848 → 0,919. Il livello è una condizione, il miglioramento un moltiplicatore |
| 28 ago | **R2** la discontinuità del passaggio di categoria | misurata: il crollo delle presenze è in gran parte l'accorciarsi della lista, non una rottura. Al cambio di fascia la lista di arrivo è fatta per l'88% da chi c'era già, contro il 61% dei passaggi interni |
| 28 ago | **STEP 20** sopravvivenza a tempo discreto | `R/20_sopravvivenza.R`: 121 eventi contro 77, rischio massimo a 23 anni, HR 1,78 per 10 punti di percentile |
| 28 ago | corretta l'età delle celle | `eta_tipica` sbagliava di un anno (U15y1 dava 14, il dato dice 13). Ora l'età si legge da `tab_a` invece che da una formula sulle sigle |
| 28 ago | estrapolare i tesserati all'indietro | **verificato che non si può**: il back-test sbaglia del 27% a due anni, e a dieci anni due modelli difendibili differiscono di 1,6 volte |
| 28 ago | il denominatore esterno | tesserati FCI 2018-2025 in `riferimenti/`: in classifica compare **un tesserato su sette**, stabile fra categorie e anni |
| 28 ago | **C3** STEP 3(b) | risolto: la fonte include già le gare internazionali (15 punti contro 5), il predittore armonizzato non serve |
| 28 ago | cosa significa «essere in classifica» | verificato: tutte le 28.041 righe hanno almeno un piazzamento nei primi 5. Ogni percentuale ha un denominatore già selezionato |
| 28 ago | primo contro secondo anno di categoria | a parità di atleti il **secondo** anno discrimina meglio in tutte le categorie; il tasso pro più alto nelle celle y1 è un effetto dell'ampiezza della lista |
| 28 ago | i cambi di società sono strutturali | 96,3% cambia dai Juniores all'Under 23 contro ~20% dentro una categoria: `n_team_changes` conta transizioni imposte |
| 28 ago | premesse delle affermazioni | `md.afferma()`: ogni commento interpretativo dichiara la condizione numerica che lo sostiene, e se cade il documento lo segnala |
| 28 ago | **STEP 18** modelli annidati | `R/18_annidati.R`: 102 atleti, stesso sottocampione; il salto maggiore è l'Under 19 (ΔAUC +0,151, DeLong p = 0,011) |
| 28 ago | **STEP 19** metriche pratiche | `R/19_metriche.R`: il migliore 10% in U19y2 intercetta il 59% dei futuri pro, e il 52% dei selezionati non lo diventa |
| 28 ago | il ricambio misurato | l'assenza dalla classifica non è abbandono: 30,6% rientra, 50,8% di ricambio in U17 |

---

## A. Rendere il progetto eseguibile senza assistenza

L'obiettivo è che chiunque, con il repository e i due database di partenza, possa rieseguire l'intera analisi leggendo solo la documentazione. Oggi gli script funzionano ma incorporano scelte nel codice.

### A1. ~~Togliere i valori cablati~~ — fatto il 28 agosto 2026

`config.toml` alla radice, letto da tutti gli script tramite `lib_giovanile.cfg()`. Contiene sesso in studio, stagione massima e stagioni anomale, coorti per domanda, classi di squadra che contano come professionista, finestre d'età, soglie del tier, pause di scaricamento e la numerosità minima delle celle pubblicabili.

Il criterio dichiarato in testa al file: *se cambiando questo file e rieseguendo la catena si ottiene un'analisi diversa e coerente, senza aprire un solo `.py`, il file sta facendo il suo lavoro.*

Valori che erano cablati e ora non lo sono più:

| Dove | Valore | Significato |
|---|---|---|
| `01_build_tabelle.py` | `STAGIONE_MAX = 2025` | ultima stagione conclusa |
| `01_build_tabelle.py` | `STAGIONI_ANOMALE = {2020: "covid"}` | stagioni da marcare |
| `01_build_tabelle.py` | `CAMPI_B_PCT` | celle pivotate in `tab_b` |
| `lib_giovanile.py` | `CATEGORIE`, `LISTE_DISGIUNTE` | mappatura categorie e struttura delle liste sorgente |
| `03_scarica_schede.py` | `PAUSA`, `OGNI` | ritmo e frequenza di salvataggio |
| `04_scarica_pcs.py` | `STAGIONI_PRO = range(2011, 2027)` | stagioni delle rose |
| `04_scarica_pcs.py` | `STAGIONI_RANK = range(2007, 2026)` | stagioni delle classifiche |
| `04_scarica_pcs.py` | `TOP_N = 500` | profondità della classifica globale |
| `04_scarica_pcs.py` | `LIVELLI`, `LIVELLI_EXTRA` | classi di squadra da enumerare |

**Perché contava.** Gli intervalli di stagione vanno spostati ogni anno, e la profondità del ranking dipende dalla soglia di qualità scelta in `definizioni.md`: prima bisognava sapere che c'era una costante da toccare dentro un file Python. Ora la scelta metodologica sta in un posto solo e si vede.

**Resta da fare**: `CATEGORIE` e `LISTE_DISGIUNTE` in `lib_giovanile.py` sono ancora nel codice. Sono struttura della fonte più che scelte metodologiche, quindi hanno meno urgenza, ma per un cambio di copertura del portale andrebbero anche loro nella configurazione.

### A2. Un comando unico che esegue la catena

**Cosa.** Un `Makefile` o `run.py` che esegue nell'ordine corretto, saltando i passi già fatti e dicendo quali richiedono decisioni manuali o download.

**L'ordine conta, ed è una trappola.** `01_build_tabelle.py` ricostruisce `analisi.db` **da zero**, quindi svuota anche `match_pcs`. La sequenza corretta è:

```
01_build_tabelle  →  05_match_pcs  →  06_esiti
```

Saltare il 05 dopo un 01 lascia `match_pcs` vuota e `06` si ferma con un messaggio esplicito. Ma è il tipo di dipendenza che va resa automatica invece che ricordata.

**Verifica.** Da repository appena clonato e con i database al loro posto, un solo comando produce `data/analisi/analisi.db`.

### A3. Dipendenze dichiarate

**Cosa.** Un `requirements.txt` con `procyclingstats`, `cloudscraper`, `certifi`. Oggi la pipeline principale usa solo la libreria standard, ma gli script 03 e 04 no, e `certifi` è servito per Eurostat.

### A4. Documentare la provenienza dei dati di partenza

**Cosa.** Il database `data/giovanile/ciclismo.db` non nasce qui: viene da **<https://github.com/lucabnt/risultati-ciclismo-giovanile>**, che contiene lo scraper di ciclismo.info e il database prodotto. Repository privato per ora, potenzialmente pubblico in futuro.

Va scritto nel README e in `docs/verifica_dati_giovanile.md`, con la versione dello schema attesa (`schema_meta.schema_version = 2.1`) e la data di estrazione, perché i numeri riportati nella verifica valgono per quella estrazione e non per un'altra.

**Perché.** Senza, chi legge il repository non sa da dove venga il file più importante, e non può rigenerarlo.

### A4bis. Il sesso come parametro, non come assunzione

**La decisione.** L'analisi è **sui maschi**. Il progetto deve però poter girare anche sul femminile cambiando un parametro, non riscrivendo codice.

**Cosa c'è già.** Il livello dati è già consapevole del sesso: `sesso` è una colonna di `anagrafica`, `tab_a` e `tab_b`, e soprattutto **la cella del percentile include già il sesso** (`stagione × categoria × anno di categoria × sesso`). I percentili femminili sono quindi calcolati fra atlete, non contro i maschi, e sono corretti fin d'ora. Non c'è nulla da rifare in `01_build_tabelle.py`.

**Cosa manca.** Il filtro `sesso='M'` oggi è sparso nelle query ad hoc dell'analisi, mai dichiarato in un posto solo. Va portato nella configurazione (§A1) insieme alle coorti, che per il femminile sono diverse.

**Il femminile non è "gli stessi script con un filtro".** Quattro differenze sostanziali:

**① Non esiste la categoria U23.** La fonte pubblica `donne_esordienti`, `donne_allieve`, `donne_juniores` e basta: nessuna classifica Under 23 femminile. Il predittore che Gallo indica come il più informativo — il primo anno da U23 — semplicemente non c'è. La sequenza dei modelli annidati si ferma all'U19, e la Domanda C perde il suo estremo superiore.

**② La copertura parte dal 2011**, non dal 2009 come gli Esordienti maschili né dal 2007 come le altre. Le coorti slittano:

| Analisi | Coorti femminili | N | Atlete |
|---|---|---|---|
| Dall'U15y1 | 1998-2000 | 3 | ~90 |
| Dall'U15y2 | 1997-2000 | 4 | ~185 |
| Dall'U17y1 | 1996-2000 | 5 | ~165 |
| Dall'U19y1 | 1994-2000 | 7 | ~145 |

**③ La numerosità è di un ordine di grandezza inferiore**: 1.252 atlete contro 11.105 atleti, con celle di 20-50 persone contro 150-600. Con questi numeri la Domanda A è al limite e la Domanda B quasi certamente non è modellabile: il femminile va impostato come **descrittivo**, e va detto prima di cominciare, non dopo aver visto che i modelli non convergono.

**④ Su PCS cambia tutto l'indirizzamento.** Le classifiche sono `p=we` invece di `p=me`, e i livelli di squadra sono Women's WorldTeam e UCI Women's Continental, non WorldTeam e ProTeam. Nello script 04 questo tocca `LIVELLI` e la costruzione degli URL delle classifiche: due parametri, ma vanno previsti.

**Quello che invece regge senza modifiche**: la copertura della data di nascita è **1.195 atlete su 1.252 (95,4%)**, in linea con il maschile, quindi il Relative Age Effect è analizzabile anche sul femminile. Ed è l'analisi in cui la numerosità pesa meno, perché confronta distribuzioni e non stima modelli. Sul femminile potrebbe essere l'unica domanda a cui si può rispondere sul serio — e non l'ha mai fatto nessuno.

**Verifica.** Cambiare `sesso = "F"` nella configurazione e ottenere l'attrito, le descrittive e il RAE femminili senza toccare un `.py`.

---

### A5. Passare allo schema v2.2 del repository a monte — la nascita è alla fonte

**Cosa è successo.** Il repository a monte ha aggiunto la raccolta delle date di nascita (`scraper/nascite.py`) e lo **schema v2.2**, che estende `atleti` con tre colonne nullable:

| Colonna | Contenuto |
|---|---|
| `data_nascita` | data dalla scheda corridore, NULL se non pubblicata |
| `anno_nascita` | anche quando c'è il solo anno fra parentesi |
| `nascita_controllata_il` | quando la scheda è stata letta |

**La buona notizia: non serve toccare il codice.** `nascite_osservate()` cerca già `data_nascita` e `anno_nascita` in `atleti`, e la precedenza è **sorgente → scheda → inferenza**. Rigenerando il database a monte, `birth_year_conf` passerà da `scheda` a `sorgente` da solo. Lo schema v2.2 aggiunge solo colonne nullable e viene applicato in place, quindi il file resta compatibile anche se lo si aggiorna senza rifare la raccolta.

**Cosa verificare quando arriva il database nuovo**, in quest'ordine:

1. **Il formato della data.** Accettiamo solo `AAAA-MM-GG`: qualunque altro formato fa cadere il valore sull'anno soltanto, silenziosamente. Controllo: `SELECT data_nascita FROM atleti WHERE data_nascita IS NOT NULL LIMIT 5`.
2. **La copertura**, confrontata con quella che abbiamo già (12.976 anni su 12.978, 12.360 date complete). Se la sorgente copre meno, conviene tenere `schede.db` come secondo livello — cosa che la precedenza fa già da sola.
3. **La concordanza fra le due fonti.** Abbiamo `schede.db` con 12.976 schede lette in proprio: confrontarle con `atleti.data_nascita` è una validazione incrociata gratuita di entrambe le raccolte. Attese zero divergenze, essendo la stessa pagina; se ce ne fossero, il problema è nel parsing di uno dei due.
4. **La versione di schema.** La pipeline oggi non la controlla: aggiungere un avviso se `schema_meta.schema_version` non è fra quelle note, così un cambio di schema non passa inosservato.

**Dopo la verifica**, `03_scarica_schede.py` diventa superfluo per la produzione. Vale la pena tenerlo ugualmente: è la seconda fonte del punto 3, e conserva l'HTML compresso.

**Nota di merito al repository a monte**: documenta le stesse due cose che avevamo trovato in modo indipendente qui — che il portale ignora lo slug del nome nell'URL e risolve sull'ID, e che una stagione sbagliata restituisce HTTP 500 invece di 404, per cui l'anno va preso dall'ultima stagione in cui l'atleta compare. Anche la copertura della data completa concorda: là 6 schede su 25 senza data nel 2008, qui una copertura che scende al 38-51% sulle coorti dei primi anni Novanta.

---

## B. Correzioni note, da fare

### B1. ~~`elite_seasons` misura i punti, non la carriera~~ — fatto il 28 agosto 2026

Rinominata in **`elite_seasons_a_punti`**, e `racing_after_u23` in **`punti_dopo_u23`**. Il commento nello schema ora dice esplicitamente che chi ha continuato a correre senza mai fare punti è indistinguibile da chi ha smesso, e che la variabile è un limite inferiore della continuità agonistica.

Il problema originale, per memoria:

**Il problema.** `tab_b.elite_seasons` e `tab_b.racing_after_u23` derivano dalla presenza nella classifica Elite di ciclismo.info. Ma quella classifica include **solo chi ha ottenuto almeno un punto**: un atleta che ha continuato a correre senza mai andare a punti è indistinguibile da uno che ha smesso.

È la stessa limitazione del denominatore che vale per tutto lo studio, ma qui è più insidiosa, perché il nome della variabile suggerisce «ha continuato a correre» mentre il significato è «ha continuato a correre **e a fare punti**».

**Cosa fare.**
1. Rinominare in `elite_seasons_a_punti` e `punti_dopo_u23`, così il nome dice cosa misura.
2. Aggiornare il commento nello schema e la voce in `definizioni.md`.
3. Nel blog post, formulare sempre come «risultava ancora a punti nella classifica Elite», mai come «correva ancora».

**Conseguenza analitica.** La variabile è un limite inferiore della continuità agonistica. Va bene come indicatore di *livello* raggiunto dopo l'età giovanile, non come misura di abbandono. Per l'abbandono vero non abbiamo una fonte, e va dichiarato.

### B2bis. Lo strato C è sotto-raccolto

**Il sintomo.** Lo script ha contato 19.400 righe scaricate ma ne ha salvate **3.974**, circa 200 per stagione, mentre la guida ne attende 400-900. Le righe salvate sono tutte distinte e con `pcs_id` valorizzato, quindi non è un problema di scrittura: le pagine successive restituiscono in larga parte gli **stessi** atleti, e `INSERT OR REPLACE` li sovrascrive.

**L'ipotesi.** Con `nation=it` il parametro `offset` sembra paginare la classifica **globale** e non quella filtrata, per cui offset diversi ricadono su sottoinsiemi sovrapposti di italiani. Il rango massimo osservato è ~2.660, coerente con il tetto `offset < 2000` dello script.

**Cosa fare.** Verificare il comportamento reale del filtro con due richieste a mano (`offset=0` e `offset=100` con `nation=it`) e confrontare i `rider_url` restituiti. Se si sovrappongono, la paginazione va fatta diversamente: o si scarica la classifica globale completa e si filtra a valle, o si usa `Ranking(...).pages_select()` per leggere gli offset validi invece di costruirli.

**Quanto è grave.** Lo strato C serve al predittore internazionale U19/U23 (STEP 12) e ad allargare l'insieme dei candidati dello strato D. **Non** tocca gli esiti: `PRO` viene dalle rose e dai profili, e il rango annuale viene da `points_per_season_history()`. Il conteggio dello STEP 4 è quindi solido anche con lo strato C incompleto.

### B3. Quattro richieste fallite per Cloudflare

`cloudscraper` non era installato: sono cadute la classifica globale 2015 e 2016 e due pagine italiane 2008-2009. Installarlo e rilanciare `--strati BC` recupera tutto, perché lo script salta ciò che è già a posto.

**Quanto è grave: poco.** Verificato che il rango annuale dei profili coincide esattamente con la classifica globale dello strato B (59/59 confronti nel 2019, 61/61 nel 2024), quindi lo strato B è di conferma e il buco 2015-2016 non tocca il `tier`.

### B4. `--continental` funziona solo per la stagione in corso

La pagina indice delle Continental ha restituito 200 squadre per il 2026 e nulla per tutte le altre stagioni: **ignora il parametro `year`**. Da capire se esista un indirizzo diverso per lo storico, altrimenti l'opzione va tolta e documentata come non praticabile.

**Quanto è grave: poco.** Per gli atleti già profilati la classe Continental si legge da `teams_history()`, che infatti riporta 1.482 stagioni `CT`. L'enumerazione serviva solo a chiudere il caso di chi ha corso Continental senza mai fare punti PCS.

### B2. Le 218 presenze fuori categoria: 87 casi indecidibili

Di 218 atleti con una presenza fuori dalla fascia d'età, 131 hanno altre stagioni tutte coerenti con la data di nascita — quindi la data è corroborata e la collocazione in classifica è errata, tipicamente nell'ultima stagione. Gli **87 che hanno solo quella riga** restano indecidibili: potrebbe essere sbagliata la data o la categoria. Sono già marcati ed esclusi dalle celle; va solo dichiarato nei limiti.

---

## D. Il livello di produzione: dai dati ai blog post

**L'obiettivo finale del progetto è una serie di blog post.** In produzione, uno script deve poter generare un `.md` completo con testo, tabelle e grafici in PNG, e deve essere aggiornabile senza assistenza. Oggi questo livello **non esiste**: abbiamo la preparazione dei dati (script 01-05) e nulla che produca output.

### D1. ~~Struttura~~ — fatta il 28 agosto 2026

Realizzata come descritto sotto, con una differenza: `calcola()` e `rendi()` stanno **nello stesso file** invece che in moduli separati. La separazione fra calcolo e presentazione è garantita dalla regola che `rendi()` riceve solo un oggetto `Lettura` e non ha accesso ai database, non dal fatto di stare in file diversi. Un file per analisi invece di due tiene insieme ciò che si legge insieme.

Resta da fare: gli altri moduli (`attrito`, `descrittive`, `contesto`, e i moduli R per i modelli).

Struttura originariamente proposta:

```
report/
  lib_grafici.py        stile comune: palette, dimensioni, salvataggio PNG
  lib_tabelle.py        da risultato SQL a tabella Markdown
  post_1_attrito.py     un modulo per post: produce il .md e i propri PNG
  post_2_rae.py
  post_3_predittivita.py
  ...
  assembla.py           esegue i moduli richiesti e scrive in output/

output/
  post_1_attrito.md
  post_1_attrito/       i PNG del post, riferiti dal .md con percorsi relativi
```

Un modulo per post e non un unico script monolitico, perché i post si scrivono e si correggono uno alla volta, e rigenerare tutto per cambiare una figura è uno spreco.

### D2. I requisiti che rendono il progetto autonomo

| Requisito | Perché |
|---|---|
| Ogni numero nel `.md` viene da una query, mai scritto a mano | Rigenerando dopo un aggiornamento dei dati, il testo resta vero |
| I PNG si rigenerano da zero a ogni esecuzione | Nessuna figura orfana che non corrisponde più ai dati |
| Le soglie e le coorti vengono dalla configurazione (§A1) | Cambiare `stagione_max` aggiorna testo, tabelle e grafici insieme |
| Ogni tabella dichiara la propria numerosità | Il lettore deve poter vedere quando una cella è sottile |
| Nessuna cella con meno di 5 atleti | Vincolo etico già in `definizioni.md`: va imposto dal codice, non ricordato |
| Un `requirements.txt` e un comando solo | Il criterio di «funziona senza assistenza» |

### D3. ~~R o Python per i modelli~~ — deciso il 28 agosto 2026

**R per i modelli, Python per preparazione e report**, SQLite come confine. Gli script R scriveranno in `output/risultati.db` con lo stesso schema che usa `lib_risultati.py`.

Il ragionamento che ha portato lì:

La guida è scritta **in R**, con pacchetti specifici: `logistf` per la regressione di Firth, `pROC` per l'AUC e il test di DeLong, `glmnet` per l'elastic net, `ordinal` per la logistica ordinale, `rms` per la validazione con bootstrap.

| | R | Python |
|---|---|---|
| Firth | `logistf`, maturo | `firthlogist`, meno usato |
| Test di DeLong | `pROC::roc.test` | va scritto a mano |
| Elastic net con CV | `glmnet` | `scikit-learn`, equivalente |
| Logistica ordinale | `ordinal::clm` | `mord`, meno completo |
| Sopravvivenza a tempo discreto | `glm` binomiale su dati espansi | uguale |
| Lettura di SQLite | `RSQLite` | nativo |
| Grafici | `ggplot2` | `matplotlib` |

**Raccomandazione: R per i modelli, Python per la preparazione dei dati e l'assemblaggio del report.** Il confine è netto — SQLite in mezzo — e ogni linguaggio fa ciò in cui è più forte. Il costo è avere due ambienti da installare.

L'alternativa tutto-Python è praticabile e riduce le dipendenze a una sola, ma su Firth e DeLong si finisce a scrivere codice statistico proprio, che è esattamente ciò che non si vuole dover mantenere senza assistenza.

**È una decisione da prendere prima di scrivere la FASE 3**, non dopo.

---

## Domande aperte, da qui in avanti

### R1. Le regioni, oltre la descrittiva — ancora aperta, ma si sa cosa manca

La tabella regionale usa nove coorti (4.827 atleti), ma i tassi restano illeggibili: poche decine di professionisti su venti regioni.

**Cosa i dati FCI hanno risolto e cosa no.** Il documento federale pubblica i tesserati *per categoria* (nazionali) e le società affiliate *per regione*, ma **mai i due incrociati**: il numero di tesserati per regione non c'è. Il denominatore regionale resta quindi mancante, ed è la ragione per cui questa voce non si chiude.

Le società per regione sono in `riferimenti/societa_fci.csv` e sono l'unica base regionale disponibile. Non sono un denominatore accettabile — una società può avere tre tesserati o duecento, copre tutte le categorie dai Giovanissimi ai Master e tutte le specialità — quindi non sono state usate per normalizzare nessun tasso. Restano in repository perché servirebbero subito se arrivasse il dato mancante.

**Cosa chiedere, con precisione.** Alla FCI (o al comitato regionale) serve una sola tabella: *tesserati per anno, regione e categoria*. Con quella, la domanda «a parità di corridori, la regione aggiunge qualcosa?» diventa rispondibile. Senza, no. Il calendario gare per regione sarebbe un secondo passo, non il primo.

### R2. ~~La discontinuità del passaggio di categoria~~ — misurata il 28 agosto 2026

Modulo `report/moduli/passaggi.py`. Il risultato ribalta la lettura di partenza: al cambio di categoria resta in classifica il 32% degli atleti contro il 80% dei passaggi interni, ma **la lista di arrivo è composta per l'88% da chi c'era già**, contro il 61% dei passaggi interni. Il crollo è nel numero di posti, non nelle persone che li occupano — le classifiche del primo anno di categoria sono circa la metà di quelle del secondo. Fra chi resta, la correlazione dei percentili scende da 0,591 a 0,471: un rimescolamento reale ma modesto.

**Cosa resterebbe da fare.** La misura è condizionata alla presenza in entrambe le liste, quindi dice poco su chi esce. Per andare oltre servirebbe sapere se chi esce ha continuato a correre, che è di nuovo il dato dei tesserati per anno e atleta — non pubblico.

---

## FASE 3. I modelli in R: cosa c'è e cosa manca

| STEP | Stato | File |
|---|---|---|
| 16 univariati per cella | fatto | `R/16_univariati.R` |
| 17 multivariato penalizzato | fatto, come controllo di robustezza | `R/17_penalizzato.R` |
| 18 incremento annidato, versione grezza | fatto | `R/18_annidati.R` |
| 18 incremento annidato, versione armonizzata | **non serve** — §C3 chiuso | la fonte include già i risultati internazionali |
| 19 metriche pratiche | fatto (manca la decision curve) | `R/19_metriche.R` |
| 20 sopravvivenza a tempo discreto | fatto | `R/20_sopravvivenza.R`, tabella `persona_anno` |
| 21 traiettorie | fatto | `R/21_traiettorie.R` |
| 22-23 Domanda B, ordinale | fatto | `R/22_qualita_carriera.R` |
| 24-25 validazione interna e temporale | fatto | `R/24_validazione.R` |
| 26 sensibilità | fatto | `scripts/10_sensibilita.py` |
| 27 confronto ML | fatto | `R/27_confronto_ml.R` |
| 28 TRIPOD | fatto | `docs/tripod.md` |

**Lo STEP 17 è rimandato in coda, deciso il 28 agosto 2026.** Il VIF massimo è 2,89 (§C6): la penalizzazione non è obbligata e i modelli non penalizzati sono stimabili, quindi l'elastic net non aggiungerebbe una stima che manca — aggiungerebbe un confronto. Va fatto dopo la validazione (STEP 24-28), dove il suo posto naturale è fra i controlli di robustezza, non prima.

**Come si esegue la catena dei modelli.**

```bash
python scripts/08_prepara_modelli.py
Rscript R/16_univariati.R
Rscript R/18_annidati.R
Rscript R/19_metriche.R
python report/assembla.py
```

Se R non c'è, `assembla.py` produce lo stesso il documento: le sezioni modellistiche dichiarano cosa manca e con quale comando ottenerlo.

---

## C. Analisi ancora da impostare

### C1. ~~Relative Age Effect~~ — modulo scritto il 28 agosto 2026

Il modulo `report/moduli/rae.py` calcola composizione e successo e produce la figura del gradiente. Gli attesi vengono da Eurostat via `scripts/07_riferimenti.py`.

**Resta aperta una scelta di interpretazione**: la parte «successo» ha 8 eventi in top 100, tutti in celle mascherate. Il rapporto Q1/Q4 fra i professionisti è 1,5, cioè non molto sotto l'1,7 di tutti i classificati — ma con 77 eventi l'intervallo di confidenza è largo e non si può concludere granché. Quando ci saranno i modelli in R, l'età relativa come covariata dirà qualcosa di più solido di questo confronto fra proporzioni.

Il ragionamento originale:

**La fonte.** Non ISTAT: le serie mensili di ISTAT partono dal 2003 e le nostre coorti sono 1996-2000. Usare **Eurostat `demo_fmonth`**, «Live births (total) by month», che copre l'Italia dal **1960 al 2025** con tutti i dodici mesi.

```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_fmonth?format=JSON&lang=en&geo=IT
```

API aperta, nessuna chiave, formato JSON-stat. Serve `certifi` per la verifica del certificato.

**Distribuzione attesa già calcolata**, nati vivi in Italia 1996-2000, totale 2.674.394:

```r
attesi <- c(0.2395, 0.2524, 0.2630, 0.2450)   # Q1, Q2, Q3, Q4
```

Il primo trimestre è demograficamente il **più scarso**, non il 25%: usare l'uniforme sottostimerebbe il RAE invece di sovrastimarlo.

| | atteso | osservato U15 | rapporto |
|---|---|---|---|
| Q1 | 23,95% | 33,4% | **1,39** |
| Q2 | 25,24% | 28,3% | 1,12 |
| Q3 | 26,30% | 22,3% | 0,85 |
| Q4 | 24,50% | 16,0% | **0,65** |

**Da fare**: uno script che scarica il vettore da Eurostat e lo salva in `data/riferimento/`, invece di lasciarlo scritto a mano qui.

**Test che non dipende da nessun dato esterno.** Il decadimento del rapporto Q1/Q4 fra categorie sulle **stesse coorti** — 2,08 in U15, 1,71 in U17, 1,32 in U19, 1,07 in U23 — non ha bisogno della distribuzione attesa, perché la stagionalità demografica è identica ai due estremi e si cancella. È l'argomento più solido, e va riportato accanto al chi-quadro.

### C7. Cosa la descrittiva ha già anticipato dei modelli

Il delta di Cliff si traduce in AUC con `AUC = (delta + 1) / 2`, quindi i modelli univariati dello STEP 16 dovranno ritrovare **circa questi valori**:

| cella | AUC attesa |
|---|---|
| U15y1 | 0,74 |
| U15y2 | 0,79 |
| U17y1 | 0,81 |
| U17y2 | 0,86 |
| U19y1 | 0,81 |
| U19y2 | 0,89 |
| U23y1 | 0,70 |

Se i modelli daranno numeri sensibilmente diversi, il posto in cui cercare l'errore è il modello, non la descrittiva: qui non ci sono covariate né assunzioni, solo il conteggio di quante volte un professionista sta sopra un non professionista.

**Esito, 28 agosto 2026.** Lo STEP 16 ha ritrovato esattamente questi valori: scarto massimo 0,0005, che è arrotondamento. Il controllo non è stato lasciato alla lettura di una tabella — `R/16_univariati.R` rilegge l'AUC descrittiva dall'archivio e segnala da solo se le due strade divergono di più di 0,01. Resta valido per le rigenerazioni future.

**L'anomalia dell'U23 va spiegata, non nascosta.** L'AUC di 0,70 in U23y1 è la più bassa di tutte, ma in quella cella i professionisti sono il 37% contro il 3,5% dell'U15: si confrontano fra loro atleti già selezionati. È l'effetto della selezione descritto nel Problema 5 della guida, e va tenuto presente quando lo STEP 18 confronterà i modelli annidati — che girano proprio su quel sottocampione.

---

### C6. Il verdetto sulla penalizzazione, da tenere presente nella FASE 3

Il VIF massimo sulle sei celle giovanili è **2,89**, sotto la soglia di 5. La regressione penalizzata dello STEP 17 **non è obbligata**: resta utile come confronto, ma i modelli non penalizzati sono stimabili.

Due cautele:

- il VIF è calcolato sui **291 atleti** presenti in tutte e sei le celle, che è un campione selezionato. Su un campione diverso i valori cambierebbero;
- non copre l'U23: aggiungendo `U23y1` gli atleti scendono a poche decine, e il VIF non sarebbe calcolabile. Se un modello userà anche l'U23, la collinearità di quel blocco va valutata a parte.

---

### C2. ~~`team_quality_first`~~ — calcolata il 28 agosto 2026

Popolata da `06_esiti.py` per 6.783 atleti, solo dove la società ha almeno cinque atleti in coorti precedenti. **Porta pochissima informazione**: il tasso di professionismo va dal 2,90% fra chi parte da una società che non ne aveva mai prodotti al 3,79% fra chi parte dalle migliori, e il 67% degli atleti ricade nella prima fascia. Come predittore non promette nulla.

### C8. La mobilità non predice: è la durata della carriera

Il modulo `contesto` documenta un risultato negativo che vale la pena non perdere. Il tasso di professionismo passa dallo 0,68% fra chi non ha mai cambiato società al 7,32% fra chi ha cambiato tre volte — un fattore dieci. Ma chi non ha mai cambiato ha corso 1,8 stagioni in media, chi ha cambiato tre volte ne ha corse 6,0.

**Stratificando per durata della carriera il gradiente sparisce**, e a sei e sette stagioni si inverte. Lo STEP 14 della guida propone di leggere `n_team_changes` come reclutamento (coefficiente positivo) o instabilità (negativo): con questi dati non si legge in nessuno dei due modi, perché il segnale grezzo è confondimento. Se lo si stima comunque in un modello, la durata della carriera va inclusa.

### C3. ~~`pct_U19_arm` e STEP 3(b)~~ — chiuso il 28 agosto 2026

**La domanda era**: il ranking Juniores incorpora i risultati internazionali? Se non lo facesse, l'U19 misurerebbe una cosa diversa dall'U23 e parte del gradiente della Domanda C sarebbe un artefatto dello strumento.

**La risposta è sì.** Le classifiche di ciclismo.info includono le gare internazionali in tutte le categorie, con una scala punti più alta: 15 punti per la vittoria in una gara internazionale contro 5 in una nazionale. Lo strumento di misura è quindi lo stesso lungo tutto il percorso, e **il predittore armonizzato non serve**.

**Cosa resta, e non è la stessa cosa.** Chi corre stabilmente all'estero senza disputare gare in Italia non compare affatto nel ranking: è un problema di *copertura della popolazione*, non di armonizzazione della misura, e riguarda pochi atleti in Juniores. Non si corregge con un predittore alternativo, si dichiara.

La macchinaria in `R/18_annidati.R` che eseguirebbe la seconda passata resta al suo posto e costa nulla: se un giorno servisse una variante del predittore U19, basta creare la colonna.

### C4. ~~La decisione sul sottocampione~~ — decisa il 28 agosto 2026

**Coorti diverse per domande diverse**: A e C su 1996-2000, B su 1992-2000. Motivazione e numeri in `definizioni.md`.

Il timore che il sottocampione di 94 atleti fosse troppo piccolo era infondato: contiene **43 professionisti**, perche' e' fatto di sopravvissuti — il 46% di loro e' arrivato al professionismo, contro il 2,7% della coorte intera. La sequenza annidata e' stimabile con quattro predittori.

**Cosa resta da fare qui**: riportare in parallelo il modello sulla coorte intera e quello sul sottocampione, senza presentarli come la stessa stima. Il secondo risponde a «*fra chi e' ancora classificato al primo anno da Under 23*, il rendimento giovanile predice il professionismo?», che e' una domanda condizionata.

---

### C5. Verifica manuale del matching

Il matching ha abbinato **727 profili PCS su 1.022**, di cui 703 esatti su nome piu' data di nascita completa. I non abbinati sono quasi tutti fuori copertura: **279 su 295 sono nati prima del 1988**, quando ciclismo.info non pubblicava ancora.

Tasso di abbinamento dei professionisti, coorte per coorte dal 1990 al 2002: fra il **90% e il 100%**. E' la validazione che lo STEP 6 chiede.

Restano tre cose da guardare a mano, tutte in `data/private/match_da_verificare.csv`:

1. **I 392 candidati professionisti**, come chiede lo STEP 6. Stanno in testa al file. Con 703 abbinamenti esatti su nome piu' data completa la verifica dovrebbe essere rapida.
2. **Tre professionisti delle coorti in studio senza riscontro** nei giovanili, nati 1995, 1999 e 1999. Da capire se abbiano corso in un'altra federazione, siano arrivati da un'altra disciplina, o se il nome differisca troppo.
3. **Un ambiguo e cinque fuzzy**, i soli abbinamenti non fondati su una corrispondenza esatta.

Le decisioni si registrano come per le omonimie, e vanno riportate nel blog post: tasso di match, casi risolti a mano e criterio usato.

**Primo giro di verifica fatto il 28 agosto 2026**, dieci casi annotati:

- tre erano differenze di grafia del nome (un secondo nome che PCS omette, `Cristian`/`Christian`, `Nicolo`/`Niccolò`): abbinamenti confermati, nessuna azione;
- sette erano divergenze di data, risolte una per una e registrate in `data/private/manual/date_corrette.csv`, che ha la precedenza su ogni fonte automatica.

Dopo le correzioni gli abbinamenti esatti su nome più data passano da 703 a 708.

**Verifica sostanzialmente chiusa il 28 agosto 2026.** Ventiquattro casi annotati, diciotto correzioni di data applicate. Il bilancio finale: **ciclismo.info aveva ragione 11 volte, PCS 7** — nessuna regola automatica è possibile.

Su 727 abbinamenti, **707 sono esatti su nome più data di nascita completa** e non richiedono verifica: due persone diverse con lo stesso nome normalizzato e la stessa data al giorno sono un'eventualità trascurabile. I 20 non esatti o ambigui sono stati guardati tutti.

L'unico ambiguo, due profili con la stessa data e la stessa regione e stagioni consecutive, era **un atleta spezzato in due da un doppio spazio nel nome**. Ha rivelato un difetto del controllo omonimie, che raggruppava sul nome grezzo invece che sulla chiave normalizzata: corretto in `02_casi_da_verificare.py`.

**Restano da decidere**, emersi dal controllo corretto:

- **6 coppie di quasi omonimi con data di nascita identica** — stesso nome, cognome a una lettera di distanza, stessa regione, stagioni non sovrapposte. Sono quasi certamente refusi che hanno spezzato un atleta in due. In `data/private/casi_quasi_omonimia.csv`.
- **6 coppie di omonimi** senza verdetto suggerito, in `data/private/casi_omonimia.csv`.
