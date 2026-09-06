# TRIPOD — checklist di controllo

**STEP 28 della guida.** TRIPOD è la checklist standard per gli studi che sviluppano o
validano modelli predittivi: 22 voci che coprono dati, partecipanti, esito, predittori,
metodi, prestazione, validazione e limiti.

Questo non è un articolo scientifico e nessuno chiederà la checklist. Serve come **lista
di controllo privata**: se ogni voce ha una risposta, il progetto è solido; le voci
senza risposta sono buchi da chiudere o limiti da dichiarare.

Compilata il 28 agosto 2026, sullo stato del documento a 18 sezioni.

**Come si «esegue».** Non si esegue: è una lettura. Il lavoro di compilazione è già
fatto, e quello che resta è verificare le voci che non poggiano sui dati ma sul processo
— chi ha guardato cosa e in che ordine — perché quelle nessuno script può controllarle.

Le cifre citate qui sotto sono invece copiate dall'analisi, che si rigenera. Per
verificare che non siano diventate false:

```bash
python scripts/11_verifica_tripod.py
```

Legenda: ✅ coperto · ⚠️ coperto con riserva dichiarata · ➖ non applicabile

---

## Titolo e sintesi

| # | Voce | Stato | Dove |
|---|---|---|---|
| 1 | Identificare lo studio come sviluppo di un modello predittivo | ✅ | Il documento dichiara in apertura popolazione, coorti, esito e finestra temporale. |
| 2 | Sintesi con obiettivi, dati, metodi, risultati, conclusioni | ✅ | La sezione «In sintesi» apre il documento: contesto, obiettivo, dati, metodi, risultati **positivi e negativi**, solidità, limiti, conclusione. È generata come tutto il resto (`report/moduli/sintesi.py`), rileggendo ogni cifra dall'archivio del modulo che l'ha prodotta: si aggiorna con i dati invece di restare indietro. |

## Introduzione

| # | Voce | Stato | Dove |
|---|---|---|---|
| 3a | Contesto e razionale, riferimenti a modelli esistenti | ✅ | `guida_metodologica_v5.md`, che discute Gallo et al. come termine di confronto. |
| 3b | Obiettivi, specificando sviluppo o validazione | ✅ | Tre domande dichiarate: accesso al professionismo (A), qualità della carriera (B), da che età il risultato informa (C). |

## Metodi

| # | Voce | Stato | Dove |
|---|---|---|---|
| 4a | Fonte dei dati e disegno | ✅ | **Il documento ha una sezione «Da dove vengono i dati»** che descrive per esteso le tre fonti, i loro conteggi, il repository separato da cui deriva il database di partenza con data di estrazione e schema, e soprattutto cosa non contengono. Non è più materiale da README: sta dove lo trova chi legge i risultati. |
| 4b | Date di inizio e fine di raccolta e follow-up | ✅ | Stagioni 2007-2025 per le classifiche, coorti di nascita 1992-2008 secondo la domanda. In `config.toml`, non nel codice. |
| 5a | Contesto e criteri di ammissibilità | ✅ | Atleti con almeno un punto nel ranking nazionale italiano. La sezione «Quanto del ciclismo giovanile si vede da qui» quantifica che è circa un tesserato su sette. |
| 5b | Trattamenti ricevuti | ➖ | Studio osservazionale, nessun trattamento. |
| 6a | Definizione dell'esito, come e quando misurato | ✅ | Sezione «Chi arriva in fondo» e `docs/definizioni.md`: prima o seconda divisione UCI entro i 25 anni; tier dalla migliore posizione nel ranking mondiale entro i 26. |
| 6b | Cecità nella valutazione dell'esito | ✅ | L'esito è estratto automaticamente da PCS senza intervento umano. Le uniche decisioni manuali riguardano l'**identità** degli atleti (matching), non il loro esito, e sono state prese guardando nome e data di nascita — mai la carriera. Registrate per id in `data/private/`. |
| 7a | Definizione dei predittori, come e quando misurati | ✅ | Percentile entro cella `stagione × categoria × anno di categoria × sesso`, con criterio di ordinamento esteso. `docs/definizioni.md`. |
| 7b | Cecità nella valutazione dei predittori | ✅ | I predittori vengono dalla fonte, calcolati prima di conoscere gli esiti: la scelta del percentile esteso è stata registrata il 27 agosto, il matching PCS è arrivato dopo. |
| 8 | Dimensione campionaria | ⚠️ | Non c'è un calcolo di potenza a priori: la dimensione è quella disponibile. Il vincolo reale sono gli **eventi**: 77 professionisti sulle coorti principali, 121 nel modello di sopravvivenza, 15 nel livello top 100. Ogni sezione riporta i propri, e le sezioni sottili lo dichiarano. |
| 9 | Gestione dei dati mancanti | ✅ | Trattata come questione sostanziale, non tecnica: un percentile mancante è un atleta che non ha fatto punti, non un dato perduto. Motivo per cui l'imputazione multipla è stata **rifiutata con argomento** e sostituita dal confronto «presenti soltanto» contro «assenza come categoria». Sezione «Quanto regge tutto questo». |
| 10a | Trattamento dei predittori nell'analisi | ✅ | Percentili in unità da dieci punti, età centrata, coorte centrata. Nessuna dicotomizzazione. |
| 10b | Procedura di costruzione del modello | ✅ | Nessuna selezione automatica delle variabili: i modelli sono specificati in anticipo dalla domanda. Firth per gli eventi rari, cloglog per il tempo discreto, misto per le traiettorie. |
| 10c | Metodi di validazione | ✅ | Bootstrap con correzione dell'ottimismo (500 ricampionamenti) e validazione temporale su coorti successive. |
| 10d | Misure di prestazione | ✅ | AUC con intervalli DeLong, pendenza di calibrazione, sensibilità/VPP a soglie di capienza, decision-analytic non ancora. |
| 10e | Aggiornamento del modello | ➖ | Voce per studi di validazione di modelli esistenti. |
| 11 | Gruppi di rischio | ✅ | Terzili di livello e pendenza nella sezione traiettorie; soglie di capienza (migliore 10% e 25%) nella sezione sulla selezione. |
| 12 | Differenze fra sviluppo e validazione | ➖ | Nessuna validazione esterna: quella temporale usa le stesse fonti su coorti successive, ed è dichiarata come tale. |

## Risultati

| # | Voce | Stato | Dove |
|---|---|---|---|
| 13a | Flusso dei partecipanti | ✅ | Sezione «Quanti restano»: l'imbuto con i numeri a ogni passaggio, più le esclusioni documentate in `docs/da_fare.md`. |
| 13b | Caratteristiche dei partecipanti | ⚠️ | Ci sono coorti, regione, società, età relativa. **Non** ci sono altezza, peso, specialità né volume di allenamento: la fonte non li pubblica. |
| 13c | Numero di partecipanti ed eventi | ✅ | Ogni tabella dichiara il proprio `n`, per regola imposta dal codice. |
| 14a | Specificazione del modello finale | ✅ | Tutti i coefficienti sono riportati con intervalli. |
| 14b | Spiegazione di come usare il modello | ✅ | Sezione «Se il ranking si usasse per selezionare» e la catena di probabilità della sezione sulla qualità della carriera. |
| 15 | Prestazione del modello | ✅ | AUC apparente **e** corretta per l'ottimismo, pendenza di calibrazione, validazione temporale. |
| 16 | Aggiornamento del modello | ➖ | Nessun modello preesistente da aggiornare. |
| 17 | Risultati dell'aggiornamento | ➖ | Come sopra. |

## Discussione

| # | Voce | Stato | Dove |
|---|---|---|---|
| 18 | Limiti | ✅ | Dichiarati dove nascono invece che raccolti in fondo: copertura del denominatore, assenza di dati regionali, 15 casi nel livello più alto, finestra della sopravvivenza che si chiude dove finisce il predittore, coorti anomale. |
| 19a | Interpretazione della validazione | ✅ | Sezione «Quanto regge tutto questo»: ottimismo nullo, calibrazione a ridosso di 1, nessun crollo temporale — con la riserva dei 27 eventi nelle coorti di verifica. |
| 19b | Interpretazione complessiva | ✅ | Le sezioni si chiudono con quello che i dati dicono **e** con quello che non dicono. Diversi risultati sono negativi e restano tali. |
| 20 | Implicazioni pratiche | ✅ | «Il livello è una condizione, il miglioramento un moltiplicatore»; il 59% dei futuri professionisti intercettato selezionando il migliore 10%, con il 52% dei selezionati che non ce la farà. |

## Altre informazioni

| # | Voce | Stato | Dove |
|---|---|---|---|
| 21 | Materiale supplementare | ✅ | Tutto il codice è nel repository; ogni numero del documento viene da una query e nessuno è scritto a mano. |
| 22 | Finanziamento | ➖ | Nessun finanziamento, nessun conflitto di interesse. |

---

## Cosa la checklist ha fatto emergere

Tre voci non pienamente coperte, tutte reali, più una che era una decisione da prendere:

**Voce 2 — manca una sintesi.** Il documento è una raccolta di analisi, non ha un
abstract. Non è un problema finché resta materiale di lavoro, lo diventa nel momento in
cui i post vengono scritti: ognuno avrà bisogno del proprio «cosa si è trovato» in tre
righe. Da fare in fase di scrittura.

**Voce 4a era una decisione, non un buco.** La provenienza è ora descritta senza reticenze nel documento stesso, repository di origine compreso.

**Voce 8 — nessun calcolo di dimensione campionaria.** Non si poteva fare diversamente,
i dati sono quelli che sono. Ma la conseguenza va detta: le sezioni con pochi eventi —
il livello top 100 con quindici casi, gli stadi condizionati — permettono di dire che
*non si vede* un effetto, non che non c'è. Il documento lo scrive già dove serve.

**Voce 13b — caratteristiche dei partecipanti incomplete.** Mancano antropometria,
specialità e carico di allenamento. È il limite più serio dell'intero studio, ed è
strutturale: il rendimento in classifica è l'unica cosa che questa fonte misura. Ogni
conclusione va letta come «a parità di ciò che la classifica registra».

Nessuna delle due è una svista da correggere: sono limiti da dichiarare, e il documento
li dichiara dove nascono.

## Riferimento

Collins GS, Reitsma JB, Altman DG, Moons KGM (2015). *Transparent reporting of a
multivariable prediction model for individual prognosis or diagnosis (TRIPOD).* La
checklist si scarica da [equator-network.org](https://www.equator-network.org/reporting-guidelines/tripod-statement/).
