# Guida metodologica allo studio

## Ranking giovanili italiani e transizione al professionismo: predire l'accesso e la qualità della carriera

*Documento di lavoro — impostazione, metodi statistici spiegati da zero, piano operativo*
*Versione 3 — rivista sulla base dei dati effettivamente disponibili e della composizione delle classifiche*

---

## Cosa è cambiato in questa versione

| Punto | Versione 1 | Versione 2 |
|---|---|---|
| Fonte dati giovanili | Ranking FCI ufficiali | **ciclismo.info** (aggregatore terzo) |
| Categorie | Esordienti / Allievi / Juniores / U23 | **U15 / U17 / U19 / U23** |
| Data di nascita | Completa, per tutti | **Solo anno**; data completa solo per i professionisti |
| Relative Age Effect | Analisi principale | **Non eseguibile** sulla coorte; solo eventuale nota sui pro |
| Numero di gare | Variabile disponibile | **Non disponibile** per le categorie giovanili |
| Elenco tesserati FCI | Auspicabile | **Non disponibile**; denominatore = atleti classificati |
| Esito di qualità | Punti PCS continui | **Ingresso almeno una volta nella top 100 PCS** |
| Coorti | 1990-2000 | **1994-2000** (più 1993 parziale, 2001 censurata) |
| Deliverable | Articolo scientifico | **Blog post** con appendice metodologica |
| Comitato etico | Richiesto | Non applicabile; **restano gli obblighi su dati di minori** |

### Cosa è cambiato nella versione 3

Una sola informazione, ma con conseguenze estese: **la classifica U23 di ciclismo.info tiene conto dei risultati nelle gare internazionali**, quelle delle categorie inferiori no (o non allo stesso modo).

Questo significa che le categorie non sono misurate con lo stesso strumento, e che parte del gradiente "il segnale cresce con l'età" potrebbe essere un artefatto di misurazione anziché un fenomeno reale. È esattamente la conclusione principale della letteratura, quindi il punto merita attenzione.

Le modifiche conseguenti:

| Dove | Cosa cambia |
|---|---|
| Problema 4 (Sezione 2) | Riscritto: da "punteggi non comparabili fra anni" a "non comparabili né fra anni né fra categorie", con la soluzione dei due predittori paralleli |
| Sezione 3 | La descrizione della fonte specifica la composizione per categoria; PCS serve ad **armonizzare** l'U19 e a **validare** l'U23 |
| Step 3 | Aggiunta la verifica della composizione delle classifiche categoria per categoria |
| Step 12 | Riscritto: costruzione del predittore U19 armonizzato e controllo di qualità sull'U23 |
| Step 15 | L'analisi di incremento va eseguita **due volte**, con misura grezza e armonizzata, e le due curve vanno sovrapposte |
| Limiti e trappole | Aggiornati di conseguenza |

---

# Indice

**PARTE I — Impostazione**
1. Le domande di ricerca
2. Perché non basta una regressione semplice: i cinque problemi
3. I dati: cosa abbiamo e cosa non abbiamo
4. Coorti, categorie e definizioni operative
5. Costruzione del dataset

**PARTE II — I metodi statistici spiegati**
6. Ripasso: dalla regressione lineare a quella logistica
7. Come si legge un odds ratio
8. Eventi rari e correzione di Firth
9. Predittori correlati e regressione penalizzata
10. Misurare quanto un modello predice
11. Modelli annidati: quanto aggiunge questa informazione?
12. Analisi di sopravvivenza a tempo discreto
13. Modelli misti e traiettorie individuali
14. Regressione logistica ordinale
15. Il problema della selezione
16. Validazione
17. Test statistici di supporto

**PARTE III — Esecuzione**
18. Piano operativo passo-passo
19. Struttura del blog post
20. Trappole da evitare
21. Glossario e riferimenti

---

# PARTE I — IMPOSTAZIONE

## 1. Le domande di ricerca

**Domanda A — Accesso.** I punteggi ottenuti nelle categorie giovanili (U15, U17, U19, U23) predicono la probabilità di diventare professionista?

**Domanda B — Qualità.** Fra chi arriva, i punteggi giovanili predicono il raggiungimento di un livello di eccellenza, definito come l'ingresso almeno una volta nella top 100 del ranking ProCyclingStats?

**Domanda C — Età di informatività.** A partire da quale età il risultato agonistico comincia a contenere informazione *aggiuntiva* rispetto a quella già disponibile? Cioè: sapere come è andato un ragazzo a 14 anni cambia qualcosa, una volta che so come è andato a 18?

### Perché la domanda C è la più importante

Gallo et al. (2022) partono dall'U17. Mostaert et al. (2022) includono l'U15 ma solo per il Relative Age Effect e solo su atleti con almeno un top-10. **Nessuno ha mai verificato se il risultato agonistico a 13-14 anni predica l'accesso al professionismo** su una popolazione ampia.

Se il risultato è "a 13-14 anni il ranking non predice nulla di utile", questo ha implicazioni immediate sui criteri di reclutamento delle società. È un risultato **negativo ma utile**, e va progettato per essere quantificato bene, non liquidato come "non significativo".

### Una domanda che in questa versione non possiamo più fare

Il **Relative Age Effect** — il vantaggio dei nati nei primi mesi dell'anno — richiede il mese o il trimestre di nascita. Sulla coorte generale disponiamo **solo dell'anno**. L'analisi RAE, che nella versione precedente era uno dei tre obiettivi, **non è eseguibile** e va tolta dal piano.

Resta possibile, se PCS fornisce le date complete, una replica limitata ai soli professionisti, come ha fatto Filipas et al. (2024). Ma sarebbe una replica di un risultato già noto (nessun RAE fra i pro italiani) su un campione simile, quindi di scarso valore aggiunto. Consiglio di **rinunciarvi** e di dedicare lo spazio alle domande A, B e C.

---

## 2. Perché non basta una regressione semplice: i cinque problemi

L'istinto naturale sarebbe:

```
pro (sì/no) ~ punti_u19
```

Questa analisi, fatta così, produrrebbe risultati sbagliati o non interpretabili. Ecco perché, uno per uno.

### Problema 1 — L'esito è binario, non continuo

"Diventare pro" è 0 o 1. La regressione lineare classica assume che l'esito sia continuo e che i residui siano distribuiti normalmente. Applicata a un esito 0/1 produce probabilità predette negative o superiori a 1, residui strutturalmente non normali, errori standard sbagliati.

**Soluzione**: regressione logistica (Sezione 6).

### Problema 2 — L'esito è raro

Nel campione di Gallo, 43 professionisti su 1345 atleti = 3,2%. Il nostro sarà simile o più basso, perché includiamo l'U15 dove la platea è molto più larga.

Con eventi rari succedono due cose spiacevoli:

- **Bias di piccolo campione.** I coefficienti della logistica vengono sistematicamente sovrastimati in valore assoluto. Non è rumore: è un bias che non sparisce aumentando il numero totale di osservazioni se gli eventi restano pochi.
- **Separazione (quasi) completa.** Se, per esempio, tutti i professionisti erano nel top 5% da U23, il modello cerca di stimare un coefficiente infinito e il software o non converge o restituisce errori standard enormi.

Il problema si aggrava sulla Domanda B: se i pro sono un centinaio e quelli entrati in top 100 sono venti, siamo nell'ordine di venti eventi.

**Soluzione**: regressione logistica penalizzata di Firth (Sezione 8).

### Problema 3 — I dati sono censurati a destra

Un atleta nato nel 2002 nel 2026 ha 24 anni: non ha ancora esaurito la finestra in cui potrebbe firmare. Se lo classifichi NON-PRO stai dicendo una cosa falsa: non è "non diventato pro", è **"non ancora osservabile"**.

Questo si chiama **censoring a destra**. Ignorarlo produce sottostima del tasso di professionismo e distorsione dei coefficienti se le coorti recenti differiscono dalle precedenti.

**Soluzioni**: (a) restringere l'analisi principale alle coorti con follow-up completo; (b) usare l'analisi di sopravvivenza, che gestisce il censoring in modo nativo (Sezione 12) e permette di recuperare la coorte 2001. Useremo entrambe.

### Problema 4 — I punteggi non sono comparabili: né fra anni, né fra categorie

Ci sono due livelli distinti, e il secondo è più insidioso del primo.

**(a) Fra stagioni.** I punti riportati da ciclismo.info dipendono dal regolamento FCI di attribuzione vigente in quella stagione, dal numero di gare in calendario e dal numero di atleti classificati. Cento punti nel 2009 non sono cento punti nel 2019.

Questo si corregge facilmente: normalizzare **dentro** ogni combinazione categoria × anno di categoria × stagione, trasformando i punti in **percentile** (Sezione 5).

**(b) Fra categorie — il problema serio.** La classifica U23 di ciclismo.info **tiene conto dei risultati nelle gare internazionali**. Quelle delle categorie più giovani, per quanto ne sappiamo, no — o comunque non allo stesso modo. Non stiamo quindi misurando la stessa cosa a età diverse: stiamo misurando **il rendimento nazionale a 13-18 anni e il rendimento complessivo a 19-22 anni**.

Perché è un problema, e non un dettaglio: la Domanda C chiede *da quale età il risultato diventa informativo*. Se il segnale cresce passando dall'U19 all'U23, ci sono due spiegazioni possibili e i dati grezzi non le distinguono:

1. **la predittività cresce davvero** con l'avvicinarsi dell'esito (l'ipotesi sostanziale, quella di Gallo);
2. **la misura diventa più buona**, perché a 19 anni cattura anche il livello internazionale che a 17 ignorava (un artefatto di misurazione).

È lo stesso meccanismo denunciato da Hasselaar & Elferink-Gemser (2025) per i ranking nazionali: se una classifica ignora i risultati internazionali, penalizza sistematicamente gli atleti migliori, che corrono poche gare nazionali e molte all'estero. Gli autori mostrano un caso in cui due atleti di livello molto diverso ottengono lo stesso punteggio nel ranking tradizionale. Nel nostro caso questo difetto è **presente nelle categorie giovanili e assente nell'U23**, ed è esattamente il tipo di eterogeneità che gonfia artificialmente il gradiente per età.

**Soluzione — rendere le misure comparabili, invece di ignorare il problema.**

Non possiamo togliere l'informazione internazionale dall'U23 (non sappiamo scomporre il punteggio). Possiamo però fare l'operazione simmetrica: **aggiungerla alle categorie inferiori**, usando ProCyclingStats, che copre chiunque abbia disputato almeno una gara registrata dall'U19 in poi.

Costruisci quindi **due versioni del predittore** e riporta entrambe:

| Versione | U15 | U17 | U19 | U23 |
|---|---|---|---|---|
| **Grezza** | percentile nazionale | percentile nazionale | percentile nazionale | percentile (già comprensivo di internazionale) |
| **Armonizzata** | percentile nazionale | percentile nazionale | percentile nazionale **+ indicatori PCS** | invariato |

Se la curva dell'AUC per età (Sezione 11) si appiattisce passando dalla versione grezza a quella armonizzata, hai dimostrato che parte del gradiente era misurazione e non sostanza. È un risultato metodologico interessante di per sé, e nessuno lo ha mai verificato.

Se invece la curva regge, la conclusione di Gallo esce rafforzata.

**Verifica preliminare da fare comunque** (Step 3 del piano operativo): accertare per **ciascuna categoria** se e come ciclismo.info incorpori i risultati internazionali. Sappiamo che l'U23 lo fa. Per l'U19 va verificato: esiste un calendario internazionale Juniores, quindi la domanda è aperta. Per l'U17 il problema quasi non si pone, perché un calendario internazionale strutturato non esiste — è un'osservazione esplicita di Hasselaar & Elferink-Gemser, che la citano come effetto collaterale della loro stessa metrica. Per l'U15 non esiste affatto.

Documenta la risposta nel file delle definizioni: determina se serve la versione armonizzata per l'U19 o solo per l'U23.

### Problema 5 — La selezione, su due livelli

Questo è il problema più insidioso, e nella nostra configurazione ha due facce distinte.

**(a) Selezione nella popolazione osservata.**
Su ciclismo.info compaiono gli atleti **classificati nel ranking**, non tutti i tesserati. Su ProCyclingStats compaiono gli atleti che hanno disputato **almeno una gara nazionale o internazionale dalla categoria U19 in poi**.

Questo significa due cose:

1. Il denominatore non è la popolazione dei tesserati, ma quella dei **già competitivi**. Ogni probabilità stimata è condizionata a questo. Un atleta che a 13 anni corre solo gare locali e non entra in classifica non esiste nei nostri dati, e la probabilità assoluta di professionismo calcolata su tutta la platea sarebbe considerevolmente più bassa di quella che stimeremo.
2. La copertura PCS dall'U19 in poi è però **molto più ampia dei soli professionisti**. Questa è una notizia buona, ed è ciò che rende possibile la Domanda B in una forma non distorta (vedi punto b).

**(b) Selezione sul predittore, per la Domanda B.**
I punti PCS da professionista si osservano solo per chi è diventato professionista. Ma diventare professionista non è casuale: dipende proprio dai risultati giovanili che vogliamo usare come predittore.

Questo produce due effetti:

- **Restrizione del range.** Fra i pro, la varianza dei punteggi giovanili è molto più piccola che nella popolazione generale. Le correlazioni calcolate su un range ristretto sono sistematicamente attenuate.
- **Distorsione da collider.** Condizionare su una variabile (essere pro) causata sia dal predittore (punti giovanili) sia da fattori non osservati (fisiologia, contatti, occasioni) crea una correlazione artificiale negativa fra il predittore e quei fattori. Concretamente: fra i professionisti, chi aveva punteggi giovanili bassi deve necessariamente avere avuto qualcos'altro di eccezionale per arrivarci — quindi il legame fra punti giovanili e qualità da pro appare più debole di quanto sia realmente.

È esattamente ciò che si vede in Filipas et al. (2024): odds ratio del miglior ranking giovanile pari a 0,97, con intervallo di confidenza [0,94-1,00] che tocca l'unità, su un campione di soli professionisti.

**Soluzione**: non stimare mai la Domanda B su un modello ristretto ai soli professionisti. Usare invece un **esito ordinale su tutta la coorte** (Sezione 14) o un **modello hurdle a due parti** (Sezione 15). Poiché l'esito di qualità che abbiamo scelto — top 100 PCS — è definibile per tutti (chi non è pro semplicemente non ci entra), l'esito ordinale è naturale e risolve il problema alla radice.

---

## 3. I dati: cosa abbiamo e cosa non abbiamo

Questa sezione è la più importante di tutta la guida, perché ogni scelta successiva discende da qui.

### Le due fonti

**ciclismo.info** — classifiche di ranking per le categorie giovanili italiane, dal 2007. È un **aggregatore terzo**, non una fonte federale ufficiale. Conseguenze pratiche:

- la copertura può avere lacune non documentate;
- i criteri di inclusione nelle classifiche possono essere cambiati nel tempo senza che ne esista un registro pubblico;
- non c'è un supporto tecnico a cui chiedere chiarimenti sistematici.

**Punto importante sulla composizione delle classifiche.** La classifica **U23 tiene conto anche dei risultati nelle gare internazionali**, mentre quelle delle categorie inferiori sono (per quanto sappiamo) nazionali. Questo è un vantaggio per la validità della misura U23 — evita il difetto denunciato da Hasselaar & Elferink-Gemser — ma introduce **eterogeneità di misura fra categorie**, che è un problema per la Domanda C. Vedi il Problema 4 nella Sezione 2 e la soluzione dei due predittori paralleli.

Filipas et al. (2024), che hanno usato la stessa fonte, dichiarano di aver incontrato **stagioni mancanti** per alcuni atleti, e di averle riempite riportando l'ultima posizione di ranking disponibile dell'anno competitivo. Quella scelta è discutibile — introduce un dato inventato — e **non la replicherei**: meglio codificare il mancante come mancante e gestirlo esplicitamente (Sezione 5).

**ProCyclingStats** — risultati e ranking annuali dalla categoria U19 in poi, per gli atleti che hanno disputato almeno una gara nazionale o internazionale registrata. Fornisce l'esito (status professionistico, squadra, posizione nel ranking annuale) e, per i professionisti, anche le date di nascita complete.

### Tabella della disponibilità

| Variabile | Disponibile? | Conseguenza |
|---|---|---|
| Punti/posizione ranking U15-U23 | **Sì**, da ciclismo.info dal 2007 | Predittore principale |
| Risultati internazionali nel ranking | **Sì per U23**; no (o da verificare) per U15-U19 | Misura non omogenea fra categorie: confonde la Domanda C |
| Anno di nascita | **Sì**, per tutti | Unica covariata demografica utilizzabile |
| Data di nascita completa | **Solo per i professionisti** (via PCS) | **RAE non analizzabile** sulla coorte |
| Numero di gare disputate (giovanili) | **No** | Impossibile calcolare un success rate normalizzato alla Mostaert; impossibile distinguere "poche gare" da "poco rendimento" |
| Elenco completo tesserati FCI | **No** | Il denominatore è la popolazione classificata, non quella tesserata |
| Squadra/società giovanile | Da verificare | Se disponibile, utile come effetto di raggruppamento |
| Regione / comitato | Da verificare | Se disponibile, possibile covariata |
| Status professionistico e squadra | **Sì**, da PCS | Esito primario |
| Ranking annuale PCS da pro | **Sì** | Esito di qualità |
| Ranking PCS U19/U23 | **Sì**, per chi corre gare registrate | Predittore aggiuntivo prezioso, vedi sotto |

### Tre conseguenze da mettere subito in chiaro

**① Niente Relative Age Effect.** Va tolto dalle domande di ricerca. Nel blog post si può citare il risultato della letteratura (Mostaert: presente sotto i 15 anni; Voet: presente fra chi non arriva, assente fra chi arriva) senza replicarlo.

**② Niente normalizzazione per numero di gare.** Il percentile del ranking resta l'unica normalizzazione praticabile. Questo significa che un atleta forte che corre poco e un atleta medio che corre molto possono risultare simili. È un limite reale, va dichiarato.

**③ Il denominatore è la popolazione classificata.** Ogni risultato va formulato come: *"fra gli atleti che compaiono nel ranking nazionale della loro categoria..."*. Non "fra i giovani ciclisti italiani". La differenza è sostanziale e va ripetuta nel blog post, non nascosta in una nota.

### Un'opportunità che vale la pena sfruttare: armonizzare la misura U19

Ora che sappiamo che l'U23 incorpora i risultati internazionali, PCS serve a due scopi diversi a seconda della categoria.

**Per l'U19: colmare una lacuna.** Se il ranking Juniores è solo nazionale, PCS fornisce l'informazione mancante — chi ha corso all'estero e come è andato. Costruendo un predittore U19 **combinato** (percentile nazionale + indicatori PCS) si ottiene una misura strutturalmente analoga a quella U23, e il confronto fra le due categorie diventa legittimo. È l'operazione che rende interpretabile la curva della Domanda C, ed è nello spirito dello YSCPS di Hasselaar & Elferink-Gemser, adattato ai dati che abbiamo.

**Per l'U23: validare.** Qui l'informazione internazionale è già dentro il ranking, quindi PCS non aggiunge dati nuovi ma permette un controllo di qualità: quanto il percentile di ciclismo.info concorda con il piazzamento PCS della stessa stagione? Un accordo alto conferma che la fonte fa quello che dice; un accordo basso è un segnale che va indagato prima di procedere.

Sono due mini-analisi a costo quasi zero, e la prima è un contributo originale: nessuno studio italiano ha mai messo le categorie giovanili su una scala di misura omogenea prima di confrontarle.

---

## 4. Coorti, categorie e definizioni operative

### Le categorie, in nomenclatura internazionale

| Sigla | Denominazione italiana | Età | Anni di categoria |
|---|---|---|---|
| **U15** | Esordienti | 13-14 | U15y1, U15y2 |
| **U17** | Allievi | 15-16 | U17y1, U17y2 |
| **U19** | Juniores | 17-18 | U19y1, U19y2 |
| **U23** | Under 23 / Elite-Sport | 19-22 | U23y1 … U23y4 |

L'anno di categoria è **fondamentale**: Gallo trova che il primo anno da U23 è il momento più informativo, e la distinzione fra primo e secondo anno è quella che produce il risultato più interessante della letteratura. Non aggregare mai i due anni di una categoria.

### Le coorti: perché 1994-2000

Con ciclismo.info che parte dal **2007** e l'esito osservabile fino al **2025**, la finestra utilizzabile si ricava così:

| Nato | U15y1 | U15y2 | U19y1 | U23y1 | Compie 25 |
|---|---|---|---|---|---|
| 1993 | 2006 ✗ | 2007 ✓ | 2010 | 2012 | 2018 |
| **1994** | **2007 ✓** | 2008 | 2011 | 2013 | 2019 |
| **1995** | 2008 | 2009 | 2012 | 2014 | 2020 |
| **1996** | 2009 | 2010 | 2013 | 2015 | 2021 |
| **1997** | 2010 | 2011 | 2014 | 2016 | 2022 |
| **1998** | 2011 | 2012 | 2015 | 2017 | 2023 |
| **1999** | 2012 | 2013 | 2016 | 2018 | 2024 |
| **2000** | 2013 | 2014 | 2017 | 2019 | **2025 ✓** |
| 2001 | 2014 | 2015 | 2018 | 2020 | 2026 ✗ |

**Analisi principale: coorti 1994-2000, sette coorti complete.** È il compromesso corretto fra il limite inferiore (copertura U15 dal primo anno) e quello superiore (finestra di osservazione dell'esito chiusa).

**Estensioni:**

- **Coorte 1993**: utilizzabile in tutte le analisi che non richiedono l'U15 primo anno, cioè per U15y2, U17, U19, U23. Vale la pena includerla nei modelli che partono dall'U17, dichiarandolo.
- **Coorte 2001 e successive**: utilizzabili solo nel **modello di sopravvivenza a tempo discreto** (Sezione 12), come osservazioni censurate. È esattamente il vantaggio di quel modello: recupera informazione che altrimenti butteresti.

**Verifica preliminare obbligatoria.** Filipas documenta l'inizio dei dati al 2007 per le categorie U19 e U23. **Non è documentato che le classifiche U15 partano dallo stesso anno.** Prima di fissare le coorti, va verificato direttamente su ciclismo.info qual è la prima stagione con classifiche Esordienti disponibili. Se fosse più tarda (poniamo 2009), tutta la finestra slitta e le coorti diventano 1996-2000, cioè cinque. È il primo controllo da fare, perché determina la dimensione del campione e quindi la potenza statistica di tutto lo studio.

### Definizione di PRO

**PRO = almeno una stagione con contratto in squadra UCI WorldTeam o UCI ProTeam, entro l'anno solare in cui l'atleta compie 25 anni.**

Escludiamo le Continental: sono un livello eterogeneo, spesso semi-dilettantistico, e la loro inclusione cambia sensibilmente il tasso di evento. Le terremo come **analisi di sensibilità**.

La finestra ai 25 anni serve a rendere le coorti confrontabili: senza limite, un nato nel 1994 avrebbe avuto dieci anni per firmare e un nato nel 2000 ne avrebbe avuti cinque.

### Definizione di QUALITÀ

**QUALITÀ = ingresso almeno una volta nella top 100 del ranking annuale ProCyclingStats.**

È una definizione più stringente di quella di Filipas (top 400 almeno una volta, che dava 22 atleti su 81). Va bene, purché si verifichi che produca un numero di eventi lavorabile.

**Stima preliminare del numero di eventi.** Filipas trova 81 professionisti italiani su sei coorti (1990-1995), circa 13-14 per coorte, ma applicando un criterio di esclusione (carriera conclusa) che rimuove i più forti ancora in attività. Senza quel criterio, sulle nostre sette coorti ci si può attendere **90-120 professionisti**. Di questi, quanti sono entrati almeno una volta in top 100?

Il tuo dato — 11 italiani attualmente in top 100, 24 in top 200 — è **trasversale** (una fotografia su tutte le età), mentre "entrato almeno una volta" è **cumulativo su otto stagioni e sette coorti**, quindi un numero maggiore. Una stima ragionevole è **15-25 atleti**. Non di più.

**Conseguenza operativa.** Con 15-25 eventi, un modello con più di due predittori non è stimabile in modo affidabile (regola dei 10 eventi per variabile, Sezione 8). Due contromisure:

1. **Verificare il conteggio prima di progettare il modello.** È lo Step 4 del piano operativo. Se gli eventi risultano meno di 15, la Domanda B va ridimensionata a descrittiva.
2. **Usare un esito ordinale a più livelli** invece di un binario, così da non buttare l'informazione intermedia:

| Livello | Definizione | Numerosità attesa |
|---|---|---|
| 0 | Mai professionista | migliaia |
| 1 | Professionista (WT o PRT), mai top 200 | 60-90 |
| 2 | Almeno una volta in top 200, mai top 100 | 15-25 |
| 3 | **Almeno una volta in top 100** | 15-25 |

Il livello 3 resta l'esito "titolare" da comunicare nel blog post; i livelli intermedi servono a dare potenza statistica al modello.

**Precisazione tecnica da fissare adesso**: PCS pubblica sia un ranking rolling (aggiornato in continuo) sia classifiche annuali di fine stagione. Usa il **ranking annuale di fine stagione**, che è stabile e replicabile, e dichiaralo. Verifica inoltre se il sistema di punteggio PCS ha subito revisioni nel periodo 2012-2025: in tal caso il "top 100" resta comunque confrontabile, perché è una posizione relativa e non un punteggio assoluto. È una delle ragioni per cui la tua scelta di usare la posizione anziché i punti è metodologicamente buona.

### Riepilogo delle definizioni da congelare

Scrivile in un file `definizioni.md` datato, **prima** di guardare i dati. Se decidi le definizioni dopo aver visto i risultati, stai facendo p-hacking anche senza volerlo: scegli inconsciamente le versioni che danno risultati più belli.

| Concetto | Definizione operativa |
|---|---|
| Categorie | U15, U17, U19, U23, sempre distinte per anno di categoria |
| Coorti (analisi principale) | Nati 1994-2000 |
| Coorti (modelli dall'U17) | Nati 1993-2000 |
| Coorti (sopravvivenza) | Tutte, con censoring |
| PRO | ≥1 stagione WT o PRT entro l'anno dei 25 anni |
| QUALITÀ | ≥1 ingresso in top 100 del ranking annuale PCS |
| Esito ordinale | 0 = non pro; 1 = pro; 2 = top 200; 3 = top 100 |
| Predittore | Percentile del ranking entro stagione × categoria × anno di categoria |
| Covariata demografica | Anno di nascita (unica disponibile) |
| Esclusioni | Atleti stranieri; anno di nascita mancante; discipline non stradali |

---

## 5. Costruzione del dataset

### Principio generale: due tabelle

Servono due formati degli stessi dati, perché metodi diversi richiedono strutture diverse.

### Tabella A — formato "lungo" (atleta × stagione)

È la struttura naturale dei dati e quella richiesta dai modelli misti (Sezione 13) e dall'analisi di sopravvivenza (Sezione 12).

```
athlete_id      identificativo anonimo stabile
birth_year      anno di nascita (unica informazione anagrafica disponibile)
season          anno solare della stagione
age             età compiuta nell'anno (= season − birth_year)
category        U15 / U17 / U19 / U23
cat_year        1, 2 (per U23: 1-4)
points_raw      punti nel ranking nazionale (da ciclismo.info)
rank_pos        posizione in classifica
n_ranked        numero totale di atleti classificati in quella cella
pcs_present     1 se l'atleta compare su PCS quella stagione (solo U19+)
pcs_rank        posizione nel ranking annuale PCS, se presente
team_id         società (se disponibile)
```

Esempio:

| athlete_id | birth_year | season | age | category | cat_year | points_raw | rank_pos | n_ranked |
|---|---|---|---|---|---|---|---|---|
| A0417 | 1996 | 2009 | 13 | U15 | 1 | 34 | 88 | 610 |
| A0417 | 1996 | 2010 | 14 | U15 | 2 | 120 | 41 | 540 |
| A0417 | 1996 | 2011 | 15 | U17 | 1 | 310 | 12 | 528 |
| A0417 | 1996 | 2013 | 17 | U19 | 1 | 95 | 60 | 480 |

Nota la riga mancante: nel 2012 (U17y2) l'atleta non compare. **Non riempirla.** Vedi sotto.

### Tabella B — formato "largo" (una riga per atleta)

Derivata dalla A tramite pivot. È la struttura richiesta dai modelli di regressione classici.

```
athlete_id, birth_year

--- predittori ---
pct_U15y1, pct_U15y2
pct_U17y1, pct_U17y2
pct_U19y1, pct_U19y2
pct_U23y1 ... pct_U23y4
best_pct_youth        miglior percentile in assoluto
slope_pct             pendenza della traiettoria (Sezione 13)
n_seasons_youth       numero di stagioni giovanili in cui compare
pcs_u19, pcs_u23      indicatori di presenza/piazzamento internazionale
pct_U19_arm           percentile U19 armonizzato (nazionale + internazionale)

--- esiti ---
PRO                   0/1
tier                  0 = non pro, 1 = pro, 2 = top 200, 3 = top 100
year_turned_pro
age_turned_pro
pro_seasons
best_pcs_rank         miglior posizione nel ranking annuale PCS
censored              1 se la finestra di osservazione non è chiusa
```

### La normalizzazione dei punteggi

Trasforma i punti grezzi in **percentile all'interno della cella** `stagione × categoria × anno di categoria`.

Il percentile risponde alla domanda: *quale percentuale di coetanei diretti questo atleta ha superato in quella stagione?*. È immune ai cambi di regolamento, interpretabile, e ha scala fissa 0-100.

```r
library(dplyr)

dfA <- dfA |>
  group_by(season, category, cat_year) |>
  mutate(
    n_ranked  = n(),
    rank_pos  = rank(-points_raw, ties.method = "min"),
    pct_rank  = 100 * (1 - (rank_pos - 1) / n_ranked),
    z_log_pts = as.numeric(scale(log1p(points_raw))),
    top10     = as.integer(rank_pos <= 10),
    top25pct  = as.integer(pct_rank >= 75)
  ) |>
  ungroup()
```

**Perché `log1p` per lo z-score**: i punti sono distribuiti in modo estremamente asimmetrico (moltissimi atleti con pochi punti, pochissimi con tantissimi). La trasformazione log(1+x) comprime la coda. Si usa `log1p` e non `log` perché log(0) non esiste.

**Quale usare come predittore principale?** Il `pct_rank`. Riporta anche i risultati con `top10` come analisi di sensibilità: è la codifica usata da Mostaert e rende i risultati confrontabili con la letteratura.

**Attenzione a un'insidia specifica di questa fonte.** Se ciclismo.info include in classifica solo chi ha ottenuto almeno un punto, allora `n_ranked` varia nel tempo per ragioni che non hanno a che fare con la partecipazione reale. Controlla l'andamento di `n_ranked` per stagione e categoria: se vedi salti bruschi, è un cambio di criterio della fonte, e va documentato. Il percentile resta comunque la scelta migliore, ma il lettore va avvisato.

### Il matching ciclismo.info ↔ ProCyclingStats

È il punto in cui si perdono più dati e si introducono più errori.

1. Match automatico su **cognome + nome + anno di nascita**, normalizzando accenti, maiuscole, doppi nomi, apostrofi.
2. Match fuzzy (distanza di Levenshtein) sui residui, con soglia conservativa.
3. **Verifica manuale al 100% dei candidati PRO.** Sono un centinaio: vale assolutamente la pena controllarli uno per uno. Un falso negativo qui pesa moltissimo, perché gli eventi sono rari.
4. Documenta il tasso di match e verifica che i non matchati non siano sistematicamente diversi.

**Nota specifica**: avendo solo l'anno di nascita, gli omonimi della stessa annata sono indistinguibili automaticamente. Con nomi comuni (ci saranno diversi "Marco Rossi 1997") il match va risolto a mano usando la società di appartenenza. Quantifica quanti casi ambigui trovi e come li hai risolti.

### La tabella di attrito

Costruiscila subito, prima di qualunque modello. È descrittiva ma è già un risultato pubblicabile, ed è probabilmente il grafico più eloquente del blog post.

| | U15 | U17 | U19 | U23 | PRO | Top 100 |
|---|---|---|---|---|---|---|
| n atleti presenti | | | | | | |
| % dei partenti U15 | 100% | | | | | |
| % del livello precedente | — | | | | | |

Questa tabella dice al lettore, in un colpo d'occhio, che la maggior parte dell'attrito avviene **prima** del punto in cui la performance diventa predittiva. È il contesto in cui va letto tutto il resto.

### Codificare i valori mancanti: cosa possiamo e cosa non possiamo distinguere

Nella versione precedente della guida distinguevo tre situazioni. **Con i dati effettivamente disponibili, non possiamo distinguerle.**

Un atleta assente dal ranking U17 può esserlo perché:
- ha smesso di correre;
- correva ma non ha ottenuto punti;
- non era tesserato quell'anno (infortunio, altro sport);
- la fonte ha una lacuna.

Senza il numero di gare e senza l'elenco tesserati, queste quattro situazioni sono **indistinguibili**. È una limitazione seria e va gestita con onestà, non aggirata.

**Cosa fare:**

```
present   = 1 se l'atleta compare nel ranking di quella cella, 0 altrimenti
pct_rank  = valore se present == 1, NA se present == 0
```

E poi due strategie in parallelo, riportando entrambe:

1. **Complete case**: analizzare solo gli atleti presenti nelle celle richieste dal modello. Semplice, interpretabile, ma riduce il campione e condiziona su "essere rimasto".
2. **Presenza come variabile**: usare `present` come predittore a sé stante. La domanda "essere ancora classificato a 16 anni predice qualcosa?" è legittima e interessante, e con questi dati è l'unica forma in cui la continuità di carriera è misurabile.

**Cosa non fare**: riempire i mancanti con l'ultimo valore disponibile, come hanno fatto Filipas et al. È un dato inventato che gonfia artificialmente la continuità delle traiettorie e distorce i modelli longitudinali.

L'imputazione multipla (Sezione 18, Step 23) resta un'analisi di robustezza possibile, ma richiede l'assunzione MAR — che qui è dubbia, perché chi smette non smette a caso.

### Aspetti etici e di trattamento dei dati

Non c'è un comitato etico universitario da coinvolgere e non ci sarà una pubblicazione scientifica. Restano però obblighi sostanziali, e sono più stringenti del solito perché **i dati riguardano minori**.

**Cosa vale comunque:**

- **Anonimizzazione all'origine.** Sostituisci nomi e cognomi con `athlete_id` non reversibile nella fase di costruzione del dataset. La chiave di corrispondenza, se ti serve per la verifica manuale, va tenuta in un file separato, non condiviso, e cancellata a lavoro finito.
- **Solo aggregati nella pubblicazione.** Nessun risultato individuale, nessun esempio nominativo, nessuna tabella con celle di numerosità così bassa da rendere identificabile una persona. Regola pratica: non pubblicare celle con meno di 5 atleti.
- **Nessuna classifica o "lista di promesse".** Anche in forma anonima, la pubblicazione di punteggi predetti individuali è esattamente l'uso improprio che i tuoi stessi risultati sconsigliano.
- **Il fatto che i dati siano pubblici non è una licenza illimitata.** Sono pubblici per una finalità (la classifica sportiva); riutilizzarli per un'analisi aggregata è legittimo, riutilizzarli per profilare individui non lo è.

**Un paragrafo da mettere nel blog post.** Dichiara apertamente la fonte, l'anonimizzazione, l'aggregazione, e il fatto che l'analisi riguarda gruppi e non persone. Costa tre righe e previene fraintendimenti prevedibili, soprattutto trattandosi di ragazzini.

---
# PARTE II — I METODI STATISTICI SPIEGATI

Questa parte spiega ogni metodo che useremo, partendo da ciò che già conosci (regressione lineare e correlazione) e costruendo per aggiunte successive. Ogni sezione ha la stessa struttura: **il problema** → **l'idea** → **come si legge il risultato** → **quando usarlo nel nostro studio**.

---

## 6. Ripasso: dalla regressione lineare a quella logistica

### Cosa fa la regressione lineare

Nella regressione che conosci:

```
y = β0 + β1·x + errore
```

`β1` risponde a: "di quanto cambia y quando x aumenta di un'unità?". Se `y` = punti PCS e `x` = percentile junior, e ottieni `β1 = 3,2`, leggi: ogni punto percentile in più da junior si associa a 3,2 punti PCS in più.

### Perché non funziona con un esito 0/1

Se `y` è "diventato pro" (0 o 1), la retta non è limitata tra 0 e 1. Con un percentile di 98 il modello potrebbe predire una probabilità di 1,4. Non ha senso.

### L'idea della logistica: cambiare scala

Il trucco è non modellare direttamente la probabilità `p`, ma una sua **trasformazione** che vive su tutta la retta reale.

**Passo 1 — dalle probabilità agli odds.**
Gli odds (quote) sono il rapporto tra probabilità dell'evento e probabilità del non-evento:

```
odds = p / (1 - p)
```

| p | odds | lettura |
|---|---|---|
| 0,50 | 1,0 | 1 a 1 |
| 0,10 | 0,111 | 1 a 9 |
| 0,03 | 0,031 | ~1 a 32 |
| 0,90 | 9,0 | 9 a 1 |

Gli odds vanno da 0 a infinito. Meglio della probabilità (limitata a 0-1), ma ancora asimmetrici.

**Passo 2 — dal logaritmo degli odds, il logit.**

```
logit(p) = log(p / (1-p))
```

Ora la scala va da meno infinito a più infinito, ed è simmetrica intorno a 0 (che corrisponde a p = 0,5). Su questa scala si può mettere una retta:

```
logit(p) = β0 + β1·x
```

E per tornare alla probabilità si inverte:

```
p = 1 / (1 + exp(-(β0 + β1·x)))
```

Questa funzione è la **curva logistica**: una S che si appiattisce vicino a 0 e a 1, quindi non esce mai dai limiti.

### Come si stima

Non con i minimi quadrati, ma con la **massima verosimiglianza** (maximum likelihood). L'idea: fra tutti i possibili valori di β0 e β1, scegli quelli che rendono più probabili i dati che hai effettivamente osservato. Il software lo fa iterativamente. Non serve che tu sappia fare i conti, ma serve sapere che è un metodo diverso da OLS, e che eredita da questo alcuni comportamenti (per esempio il bias con eventi rari, Sezione 8).

### In R

```r
fit <- glm(PRO ~ pct_U19y2, family = binomial(link = "logit"), data = dfB)
summary(fit)
```

L'output ti dà `Estimate` (i coefficienti β, **sulla scala logit**), errore standard, z-value, p-value.

**Attenzione**: i coefficienti grezzi della logistica non sono direttamente interpretabili come "aumento di probabilità". Sono aumenti di log-odds. Per interpretarli si esponenziano — ed è la prossima sezione.

---

## 7. Come si legge un odds ratio (senza sbagliare)

### Definizione

```
OR = exp(β1)
```

L'OR è il fattore per cui gli **odds** dell'evento vengono moltiplicati quando `x` aumenta di un'unità.

Esempio concreto. Supponi di stimare, su `pct_U19y2`:

```
β1 = 0,048   →   OR = exp(0,048) = 1,049
```

Lettura: ogni punto percentile in più da Junior 2° anno moltiplica gli odds di diventare pro per 1,049 (+4,9%).

### Riscalare per rendere il numero leggibile

Un OR di 1,049 per un punto percentile è poco espressivo. Meglio riportarlo **per 10 punti percentile**:

```
OR(10 punti) = exp(0,048 × 10) = exp(0,48) = 1,62
```

Lettura: 10 punti percentile in più moltiplicano gli odds per 1,62 (+62%). Molto più comunicabile.

Nel codice, basta dividere il predittore per 10 prima di stimare, così l'OR esce già nella scala giusta:

```r
dfB$pct_U19y2_10 <- dfB$pct_U19y2 / 10
fit <- logistf(PRO ~ pct_U19y2_10, data = dfB)
exp(coef(fit))
```

### L'errore da non fare: OR ≠ rischio relativo

Questa è la confusione più diffusa nella letteratura sportiva applicata.

Un OR di 1,62 **non** significa "il 62% di probabilità in più di diventare pro". Significa "gli *odds* aumentano del 62%".

Con eventi rari, per fortuna, OR e rischio relativo sono numericamente vicini. Con p = 0,03, un OR di 1,62 corrisponde a un rischio relativo di circa 1,58 — differenza trascurabile. Ma con eventi frequenti divergono molto, e la formulazione va comunque tenuta corretta.

### Il modo migliore di comunicare i risultati

Per lettori non statistici (allenatori, dirigenti federali), converti gli OR in **probabilità predette**:

> "Un atleta al 50° percentile da Junior ha una probabilità stimata dell'1,1% di diventare professionista. Al 90° percentile la probabilità è del 5,4%. Al 99° percentile è del 18%."

Questo si ottiene direttamente dal modello:

```r
nd <- data.frame(pct_U19y2 = c(50, 75, 90, 95, 99))
nd$prob <- predict(fit, newdata = nd, type = "response")
```

Questi numeri comunicano due cose insieme: che la performance conta (aumento di 16 volte), e che anche nel migliore dei casi la maggior parte non ce la fa (l'82% dei top-1% non diventa pro). Entrambi i messaggi sono importanti e onesti.

### Intervalli di confidenza

Riporta sempre l'IC 95% dell'OR, mai solo il p-value. L'IC si ottiene esponenziando gli estremi dell'IC del coefficiente:

```r
exp(confint(fit))     # profile likelihood, più accurato con n piccolo
```

Se l'IC include 1, l'associazione non è statisticamente distinguibile da nulla. Ma — punto importante per la tua domanda C — **la larghezza dell'IC conta quanto la sua posizione**: un IC [0,98–1,03] dice "nessun effetto, e lo sappiamo con precisione"; un IC [0,7–1,9] dice "non ne abbiamo idea". Sono conclusioni completamente diverse, spesso riportate entrambe come "non significativo".

---

## 8. Il problema degli eventi rari e la correzione di Firth

### Il problema

Con poche decine di eventi su qualche migliaio di osservazioni, la massima verosimiglianza soffre di due patologie.

**Bias di piccolo campione.** I coefficienti stimati sono sistematicamente **troppo grandi in valore assoluto**. L'entità del bias dipende dal numero di eventi, non dal numero totale di osservazioni. Con qualche decina di eventi il bias può essere del 10-20%.

**Separazione.** Se esiste un valore soglia del predittore che separa perfettamente (o quasi) i casi dai non-casi — per esempio se nessun atleta sotto il 60° percentile U23 è mai diventato pro — la verosimiglianza non ha un massimo finito. Il coefficiente "vero" secondo il modello sarebbe infinito. Il software restituisce coefficienti enormi (tipo 18,4) con errori standard giganteschi (tipo 2400). È un segnale di allarme da riconoscere.

Nel tuo studio la separazione è realistica, soprattutto per i modelli U23 e per qualunque modello sull'esito top 100.

### La regola degli eventi per variabile (EPV)

Regola pratica classica: servono almeno **10 eventi per ogni predittore** stimato. Le versioni più recenti della letteratura (Riley et al.) sono più sofisticate, ma la regola dei 10 EPV resta un'ottima guida.

Nel nostro studio i due esiti hanno budget molto diversi, ed è essenziale tenerli distinti:

| Esito | Eventi attesi | Predittori massimi |
|---|---|---|
| **Domanda A** — diventare professionista | 90-120 | 9-12, ma restare sotto per prudenza |
| **Domanda B** — entrare in top 100 | 15-25 | **1 o 2** |

La Domanda A ha un budget confortevole. La Domanda B è al limite: **due predittori sono il massimo**, e vanno scelti a priori (verosimilmente `pct_U19y2` e `pct_U23y1`), non selezionati guardando i dati. È anche la ragione per cui l'esito ordinale a quattro livelli (Sezione 14) è preferibile al binario: recupera potenza usando i livelli intermedi.

I numeri attesi sono stime da confermare allo Step 4 del piano operativo. Se gli eventi in top 100 risultassero meno di 15, la Domanda B va ridotta a descrittiva.

### La soluzione: Firth

Firth (1993) ha proposto di **penalizzare** la verosimiglianza aggiungendo un termine (il jeffreys prior, per chi conosce l'inferenza bayesiana) che tira i coefficienti leggermente verso zero.

Effetti:
- rimuove (al primo ordine) il bias di piccolo campione;
- **garantisce sempre stime finite**, anche in caso di separazione completa;
- funziona bene con campioni piccoli e eventi rari;
- è ormai lo standard raccomandato in epidemiologia per queste situazioni.

Il costo: le stime sono leggermente "conservative" (tirate verso l'assenza di effetto). È un costo accettabile, e comunque preferibile a stime distorte al rialzo.

### In pratica

```r
library(logistf)

fit <- logistf(PRO ~ pct_U19y2_10 + birth_year_c,
               data = dfB)
summary(fit)

# odds ratio e IC
data.frame(
  OR    = exp(coef(fit)),
  lower = exp(fit$ci.lower),
  upper = exp(fit$ci.upper)
)
```

`logistf` calcola gli intervalli di confidenza per profile penalized likelihood, che sono più affidabili degli intervalli di Wald quando il campione è piccolo.

**Regola operativa per il tuo studio**: usa `logistf` come default per tutti i modelli logistici, non `glm`. Confronta i due nell'appendice metodologica del blog post per mostrare l'effetto della correzione.

---

## 9. Predittori correlati: multicollinearità e regressione penalizzata

### Il problema

I tuoi predittori sono fortemente correlati fra loro: chi è forte da Allievo tende a essere forte da Junior. Ti aspetti correlazioni r = 0,5-0,8 fra categorie adiacenti.

Quando due predittori sono molto correlati, il modello **non riesce a distinguere il contributo dell'uno da quello dell'altro**. Sintomi tipici:
- coefficienti instabili, che cambiano molto togliendo o aggiungendo una variabile;
- errori standard grandi, quindi p-value alti anche se il blocco di variabili è complessivamente predittivo;
- talvolta segni "assurdi" (coefficiente negativo per una variabile che dovrebbe avere effetto positivo).

Nota bene: la multicollinearità **non danneggia la capacità predittiva complessiva del modello**. Danneggia l'interpretabilità dei singoli coefficienti. Distinzione importante, perché determina se devi preoccupartene o no a seconda dell'obiettivo.

### Come diagnosticarla

Il **VIF** (Variance Inflation Factor) misura di quanto la varianza di un coefficiente è gonfiata dalla correlazione con gli altri predittori.

```r
library(car)
vif(glm(PRO ~ pct_U17y2 + pct_U19y1 + pct_U19y2 + pct_U23y1,
        family = binomial, data = dfB))
```

Interpretazione convenzionale: VIF > 5 attenzione, VIF > 10 problema serio.

### Soluzione 1 — Regressione penalizzata (ridge, lasso, elastic net)

L'idea: invece di massimizzare solo la verosimiglianza, si massimizza la verosimiglianza **meno una penalità** proporzionale alla dimensione dei coefficienti.

```
obiettivo = log-verosimiglianza − λ · penalità(β)
```

Tre varianti, che differiscono nella forma della penalità:

| Metodo | Penalità | Comportamento |
|---|---|---|
| **Ridge** (L2) | somma dei β² | Restringe tutti i coefficienti verso zero, nessuno esattamente a zero. Ottimo con predittori correlati: li "spalma" equamente |
| **Lasso** (L1) | somma dei \|β\| | Porta alcuni coefficienti **esattamente a zero**: fa selezione di variabili. Con predittori correlati sceglie arbitrariamente uno del gruppo |
| **Elastic net** | mix delle due (α controlla il mix) | Compromesso: selezione, ma tratta i gruppi correlati in modo più stabile |

Il parametro `λ` controlla quanta penalità applicare: λ = 0 è la regressione normale, λ grande schiaccia tutto a zero. **Si sceglie per cross-validation**, non a occhio.

Per il tuo caso, con predittori correlati e pochi eventi, **elastic net con α = 0,5** è una scelta ragionevole; ridge se ti interessa più la predizione che la selezione.

```r
library(glmnet)

X <- model.matrix(~ pct_U15y2 + pct_U17y1 + pct_U17y2 + pct_U19y1 +
                    pct_U19y2 + pct_U23y1 + birth_year_c, data = dfB)[, -1]
y <- dfB$PRO

set.seed(42)
cv <- cv.glmnet(X, y, family = "binomial", alpha = 0.5,
                nfolds = 10, type.measure = "auc")

plot(cv)
coef(cv, s = "lambda.1se")   # 1se = versione più parsimoniosa
```

**Nota importante**: nella regressione penalizzata i p-value e gli intervalli di confidenza classici non sono validi (l'inferenza post-selezione è un problema aperto). Quindi usa questi modelli per la **predizione**, non per fare affermazioni sui singoli coefficienti. Per quelle, usa i modelli non penalizzati/Firth con pochi predittori scelti a priori.

### Soluzione 2 — Composito o riduzione dimensionale

Alternativa: costruire una singola variabile riassuntiva. Per esempio la prima componente principale (PCA) dei percentili giovanili, oppure semplicemente la media dei percentili. Perde informazione sulle differenze fra categorie, ma è stabile e parsimoniosa.

### Soluzione 3 — Modelli separati per categoria (l'approccio di Gallo)

Stimare un modello per categoria evita del tutto il problema. È l'approccio più semplice e va fatto comunque, ma non risponde alla domanda C (il contributo *incrementale*), perché ogni modello ignora le altre categorie. Serve la Sezione 11.

---

## 10. Misurare quanto un modello predice

Un p-value significativo **non** significa che il modello predice bene. Con n grande, associazioni minuscole diventano significative. Serve misurare la qualità predittiva, che ha due dimensioni distinte: **discriminazione** e **calibrazione**.

### 10.1 Discriminazione: la curva ROC e l'AUC

**La domanda**: il modello assegna probabilità più alte a chi effettivamente diventa pro rispetto a chi non lo diventa?

**Sensibilità** (recall, true positive rate): fra chi è diventato pro, quale frazione il modello aveva segnalato?
**Specificità** (true negative rate): fra chi non è diventato pro, quale frazione il modello aveva correttamente non segnalato?

C'è un trade-off: abbassando la soglia di segnalazione aumenti la sensibilità e riduci la specificità. La **curva ROC** traccia sensibilità (asse y) contro 1−specificità (asse x) per tutte le soglie possibili.

**L'AUC** (Area Under the Curve) è l'area sotto questa curva. Ha un'interpretazione bellissima e intuitiva:

> **L'AUC è la probabilità che, prendendo a caso un futuro pro e un futuro non-pro, il modello assegni la probabilità più alta al pro.**

| AUC | Interpretazione |
|---|---|
| 0,50 | Come tirare a caso |
| 0,60-0,70 | Discriminazione debole |
| 0,70-0,80 | Accettabile |
| 0,80-0,90 | Buona |
| > 0,90 | Eccellente (in questo campo, sospetta: controlla l'overfitting) |

```r
library(pROC)
p_hat <- predict(fit, type = "response")
roc_obj <- roc(dfB$PRO, p_hat)
auc(roc_obj)
ci.auc(roc_obj)
plot(roc_obj)
```

### 10.2 Il problema che l'AUC nasconde: il valore predittivo positivo

Questo è il punto **più importante di tutto lo studio** dal punto di vista pratico, ed è quello che quasi tutti gli studi di talent identification sottovalutano.

**PPV** (Positive Predictive Value): fra quelli che il modello segnala, quale frazione diventa davvero pro?

Con eventi rari, il PPV è drammaticamente basso anche con un'AUC eccellente. Esempio numerico realistico:

- 1300 atleti, 43 pro (3,3%)
- Modello con sensibilità 80% e specificità 85% (AUC ≈ 0,88, ottima)

| | PRO reali | NON-PRO reali | Totale |
|---|---|---|---|
| **Segnalati** | 34 (veri positivi) | 189 (falsi positivi) | 223 |
| **Non segnalati** | 9 (falsi negativi) | 1068 (veri negativi) | 1077 |
| **Totale** | 43 | 1257 | 1300 |

- **PPV = 34 / 223 = 15%.** Su 100 atleti segnalati come "futuri pro", 85 non lo diventeranno.
- **NPV = 1068 / 1077 = 99,2%.** Su 100 non segnalati, 99 effettivamente non diventeranno pro.

Il messaggio scientifico e pratico è asimmetrico:
- il modello è **bravo a escludere** ma **pessimo a confermare**;
- ma il NPV alto è in gran parte dovuto alla rarità dell'evento, non alla bravura del modello (se dicessi "nessuno diventerà pro" avrei NPV del 96,7% senza alcun modello);
- usarlo per **deselezionare** un ragazzo di 14 anni è statisticamente ingiustificabile.

Questa tabella, con i tuoi numeri reali, deve stare nel blog post. È il contributo più utile che lo studio possa dare.

**Sull'esito di qualità il quadro è ancora più severo.** Se in top 100 entrano 20 atleti su qualche migliaio, il tasso di evento scende sotto lo 0,5%. Con quella base, anche un modello con AUC 0,90 produce un PPV nell'ordine di pochi punti percentuali. Quando presenterai i risultati sulla Domanda B, calcola e riporta il PPV **separatamente** da quello della Domanda A: sono numeri molto diversi e vanno comunicati come tali.

### 10.3 Scegliere una soglia: l'indice di Youden

Se devi indicare una soglia operativa, l'indice di Youden massimizza `sensibilità + specificità − 1`.

```r
coords(roc_obj, "best", best.method = "youden",
       ret = c("threshold","sensitivity","specificity","ppv","npv"))
```

Ma la soglia "ottimale" statisticamente non è quella ottimale praticamente: dipende da quanto costa un falso positivo rispetto a un falso negativo. Da cui la sezione successiva.

### 10.4 Decision curve analysis

La DCA valuta il **beneficio netto** di usare il modello a diverse soglie, pesando falsi positivi e falsi negativi secondo le preferenze dell'utilizzatore. Confronta tre strategie: usare il modello, selezionare tutti, selezionare nessuno.

```r
library(dcurves)
dca(PRO ~ p_hat, data = dfB, thresholds = seq(0, 0.3, 0.01)) |> plot()
```

Nel tuo contesto risponde alla domanda concreta: *"a una federazione che può inserire 30 atleti in un progetto elite, il modello serve davvero rispetto a prendere i primi 30 del ranking?"*. Spesso la risposta è "poco", e dirlo è un risultato.

### 10.5 Calibrazione

La discriminazione dice se il modello ordina bene. La **calibrazione** dice se i numeri sono giusti in valore assoluto: quando il modello dice "5% di probabilità", quel gruppo diventa pro nel 5% dei casi?

Si valuta con un **calibration plot**: si dividono i soggetti in decili di probabilità predetta e si confronta probabilità media predetta vs frequenza osservata. Sulla diagonale = calibrazione perfetta.

Due indici:
- **calibration-in-the-large**: le probabilità sono mediamente giuste, o sistematicamente alte/basse?
- **calibration slope**: idealmente 1. Se < 1 (tipico) il modello è troppo "estremo" — segno di overfitting.

```r
library(rms)
val <- val.prob(p_hat, dfB$PRO)
```

Il test di Hosmer-Lemeshow, citato nel lavoro di Gallo, è la versione classica: raggruppa in decili e fa un chi-quadro. È superato (dipende dal numero di gruppi, poco potente), ma resta accettabile riportarlo per continuità con la letteratura. Meglio affiancargli il calibration plot.

---

## 11. Modelli annidati: "quanto aggiunge questa informazione?"

Questa è la sezione che risponde alla tua domanda C, la più originale dello studio.

### L'idea

Costruisci una sequenza di modelli in cui ciascuno aggiunge un blocco di informazione al precedente:

| Modello | Contenuto | Domanda |
|---|---|---|
| M0 | Anno di nascita (coorte) | Baseline demografico |
| M1 | M0 + percentile U15 | Sapere com'è andato a 13-14 anni aggiunge? |
| M2 | M1 + percentile U17 | ...a 15-16? |
| M3 | M2 + percentile U19 | ...a 17-18? |
| M4 | M3 + percentile U23 1° anno | ...a 19? |

**Vincolo tecnico assoluto**: tutti i modelli vanno stimati sullo **stesso identico sottocampione** (solo atleti con dati completi in tutte le categorie). Altrimenti confronti modelli su dati diversi e i confronti non hanno senso. Questo riduce il campione — riportalo esplicitamente.

### Tre modi di misurare il guadagno

**(a) Likelihood ratio test.** Confronta la verosimiglianza dei due modelli. Se il modello più ricco spiega significativamente meglio i dati, il test è significativo.

```r
anova(M2, M3, test = "LRT")
```

Limite: risponde a "c'è un effetto?", non a "quanto è utile?". Con n grande diventa significativo per effetti irrilevanti.

**(b) ΔAUC con test di DeLong.** Quanto aumenta l'AUC aggiungendo il blocco? Il test di DeLong confronta due AUC calcolate sugli stessi soggetti (dati appaiati, va tenuto conto della correlazione).

```r
roc.test(roc_M2, roc_M3, method = "delong")
```

Limite noto: l'AUC è poco sensibile — aggiungere un predittore anche buono spesso la muove di 0,01-0,02. Non concludere "inutile" solo perché il ΔAUC è piccolo.

**(c) IDI e NRI.** Progettati proprio per superare il limite precedente.

- **IDI** (Integrated Discrimination Improvement): di quanto aumenta la separazione media fra le probabilità predette dei casi e quelle dei non-casi. In pratica: `(media p̂ nei casi − media p̂ nei non-casi)` nel modello nuovo meno la stessa quantità nel modello vecchio.
- **NRI** (Net Reclassification Improvement): quanti soggetti vengono riclassificati **correttamente** in categorie di rischio diverse. Esiste in versione categorica (con soglie definite) e continua.

```r
library(PredictABEL)
reclassification(data = dfB, cOutcome = which(names(dfB) == "PRO"),
                 predrisk1 = p_M2, predrisk2 = p_M3,
                 cutoff = c(0, 0.02, 0.10, 1))
```

L'NRI è stato criticato (può essere positivo anche per predittori casuali se mal calcolato), quindi riportalo insieme a ΔAUC e IDI, non da solo.

### Il grafico centrale del blog post

Un grafico con l'**età di osservazione sull'asse x** e l'**AUC cumulata sull'asse y**, con bande di confidenza. Mostra visivamente da che età il segnale emerge.

La mia previsione, basata sulla letteratura: curva sostanzialmente piatta intorno a 0,55-0,60 per U15 e U17, salita marcata dall'U19 secondo anno, plateau intorno a 0,80-0,85 con l'U23 primo anno. Gallo et al. hanno trovato che il valore predittivo cresce con la categoria d'età e che il piazzamento nel primo anno da U23 è il miglior predittore: il tuo studio estenderebbe la curva verso il basso, dove nessuno l'ha ancora misurata.

---

## 12. Analisi di sopravvivenza a tempo discreto

### Perché serve

Finora abbiamo trattato "diventare pro" come uno stato finale (sì/no). Ma è un **evento che accade a un certo momento**, e alcuni atleti sono ancora "in gioco" alla fine dell'osservazione (censoring, Problema 3).

L'analisi di sopravvivenza modella il *tempo all'evento* e gestisce nativamente i censurati. "Sopravvivenza" è il nome storico (nasce in medicina, dove l'evento era la morte); qui l'evento è positivo — firmare da pro.

### Perché "a tempo discreto"

Il modello di Cox, che forse conosci di nome, assume tempo continuo. Qui il tempo è naturalmente discreto: la firma avviene a stagioni, non a giorni. Con tempo discreto e molti eventi simultanei (tanti atleti firmano "nello stesso anno"), il modello a tempo discreto è più appropriato e — sorpresa gradita — **si stima con una normale regressione logistica** sulla tabella persona-anno.

### Come funziona, concretamente

**Passo 1 — costruisci il dataset persona-anno "a rischio".**
Ogni atleta contribuisce una riga per ogni anno in cui è "a rischio" di diventare pro, dal primo anno giovanile fino a: l'anno in cui firma (riga con evento = 1), oppure l'ultimo anno osservabile (tutte righe con evento = 0, atleta censurato).

| athlete_id | age | pro_event | lag_pct | at_risk |
|---|---|---|---|---|
| A0417 | 17 | 0 | 62 | sì |
| A0417 | 18 | 0 | 71 | sì |
| A0417 | 19 | 0 | 80 | sì |
| A0417 | 20 | 1 | 92 | evento! |
| A0511 | 17 | 0 | 45 | sì |
| A0511 | 18 | 0 | 40 | sì |
| A0511 | 19 | 0 | 38 | censurato qui |

Dopo l'evento l'atleta esce dal dataset (non è più a rischio).

**Passo 2 — stima una logistica su questa tabella.**

```r
fit_surv <- glm(pro_event ~ splines::ns(age, 3) + lag_pct_rank + birth_year_c,
                family = binomial(link = "cloglog"),
                data = person_year)
```

Il coefficiente di `lag_pct_rank` risponde a: "a parità di età, avere un percentile più alto l'anno scorso aumenta la probabilità di firmare **quest'anno**?".

### Dettagli tecnici da conoscere

**Il link cloglog.** `cloglog` (complementary log-log) invece di `logit`: con questo link il modello a tempo discreto è l'equivalente esatto di un modello a rischi proporzionali in tempo continuo, quindi i coefficienti si interpretano come **hazard ratio**, confrontabili con la letteratura che usa Cox. Con `logit` ottieni odds ratio della probabilità condizionata. Entrambi vanno bene; dichiara quale usi.

**La funzione dell'età.** `ns(age, 3)` è una spline naturale con 3 gradi di libertà: permette alla probabilità di base di variare con l'età in modo flessibile (non lineare), senza imporre una forma. È l'equivalente della "baseline hazard" del modello di Cox, ma stimata esplicitamente.

**Covariate tempo-varianti.** Questo è il grande vantaggio: puoi usare il percentile **dell'anno precedente** (`lag_pct_rank`), aggiornato ogni stagione, invece di una singola misura fissa. È molto più vicino a come funziona realmente la selezione.

**Errori standard.** Le righe dello stesso atleta non sono indipendenti. Usa errori standard robusti a cluster:

```r
library(sandwich); library(lmtest)
coeftest(fit_surv, vcov = vcovCL(fit_surv, cluster = person_year$athlete_id))
```

### Cosa ci guadagni

1. Recuperi le coorti recenti (2001-2003) come censurate, invece di buttarle.
2. Stimi anche **quando** avviene la transizione, non solo se. Rilevante, perché i professionisti di successo tendono a passare meno tempo nelle categorie giovanili e a transitare alla categoria PRO in età più precoce.
3. Puoi produrre **curve di incidenza cumulata** per gruppi (per esempio: top 10% junior vs resto), che sono grafici molto comunicativi.

---

## 13. Modelli misti e traiettorie individuali

### La domanda

Conta di più il **livello** raggiunto o il **miglioramento** nel tempo? Un atleta che passa dal 40° al 90° percentile in tre anni è più promettente di uno stabile al 75°?

È una domanda che gli allenatori si fanno costantemente e che i dati longitudinali possono affrontare.

### Cos'è un modello misto

Nella regressione ordinaria, ogni osservazione è indipendente. Ma le tue osservazioni sono **annidate**: più stagioni per lo stesso atleta. Le stagioni dello stesso atleta si somigliano fra loro più di quanto si somiglino stagioni di atleti diversi.

Il modello misto (o multilivello, o a effetti misti) gestisce questo dando a ogni atleta i propri parametri:

```
pct_rank[i,t] = (β0 + u0[i]) + (β1 + u1[i]) · age[i,t] + errore
```

- `β0`, `β1`: **effetti fissi** — l'intercetta e la pendenza media della popolazione;
- `u0[i]`, `u1[i]`: **effetti casuali** — di quanto l'atleta *i* devia dalla media, in livello (`u0`) e in pendenza (`u1`).

Gli effetti casuali si assume siano distribuiti normalmente attorno a zero. Il modello stima la loro varianza, e produce una previsione individuale per ciascun atleta (BLUP: best linear unbiased predictor).

```r
library(lme4)
m_traj <- lmer(pct_rank ~ age_c + (age_c | athlete_id), data = dfA)

re <- coef(m_traj)$athlete_id
traj <- data.frame(athlete_id = rownames(re),
                   intercept  = re[, "(Intercept)"],
                   slope      = re[, "age_c"])
```

(`age_c` = età centrata, per rendere l'intercetta interpretabile come livello a un'età di riferimento invece che a età 0.)

### Lo shrinkage: perché questo è meglio di una regressione per atleta

Potresti pensare: "faccio una regressione separata per ogni atleta e prendo la pendenza". Sarebbe peggio, perché un atleta con 2 sole stagioni avrebbe una pendenza stimata su 2 punti — rumore puro.

Il modello misto applica lo **shrinkage**: le stime individuali vengono tirate verso la media della popolazione, e tanto più quanto meno dati ha quell'atleta. Un atleta con 6 stagioni mantiene quasi la sua pendenza; uno con 2 stagioni viene tirato molto verso la media. È esattamente il comportamento corretto, e viene fuori automaticamente dalla struttura del modello.

### Come usarlo nello studio

**Approccio a due stadi (semplice, consigliato):**
1. Stima il modello misto sulla Tabella A → estrai `intercept` e `slope` per ciascun atleta.
2. Inserisci `slope` come predittore nel modello del professionismo (Tabella B).

Limite: al secondo stadio si ignora l'incertezza delle stime del primo. Accettabile, ma va dichiarato.

**Approccio joint model (rigoroso, complesso):**
Stima simultaneamente il modello longitudinale e quello di sopravvivenza (pacchetto `JMbayes2`). Tecnicamente superiore, ma richiede molto più lavoro. Consiglio: fallo solo se il two-stage produce un risultato interessante che vale la pena consolidare.

**Attenzione a un artefatto**: la pendenza è correlata negativamente con l'intercetta per costruzione (chi parte alto ha meno spazio per salire — effetto soffitto sul percentile, che è limitato a 100). Includi sempre entrambe nel modello e considera l'interazione.

---

## 14. Regressione logistica ordinale

### Il problema che risolve

"Diventare pro" è binario, ma il successo è graduato: non-pro < ProTeam < WorldTeam < WorldTeam di alto livello.

Le opzioni sarebbero:
- **trattarlo come binario** → butti via informazione;
- **trattarlo come continuo** → assumi che le distanze fra i livelli siano uguali, il che è falso;
- **fare più modelli binari separati** → moltiplichi i test, perdi potenza;
- **logistica ordinale** → usa l'ordine senza assumere distanze uguali. La scelta giusta.

Il vantaggio pratico è grosso: usi **tutta la coorte** in un solo modello, e ottieni una risposta unificata alle domande A e B, aggirando in buona parte il problema della selezione (Sezione 15).

### Come funziona: proportional odds

Il modello stima una serie di **logistiche cumulative**:

```
logit P(Y ≥ 1) = α1 + β·x      (pro almeno ProTeam vs non pro)
logit P(Y ≥ 2) = α2 + β·x      (almeno WorldTeam vs meno)
logit P(Y ≥ 3) = α3 + β·x      (WT top vs meno)
```

Nota il punto cruciale: **le intercette α cambiano, ma il coefficiente β è unico**. Questa è l'assunzione di *proportional odds* (odds proporzionali): l'effetto del predittore è lo stesso a tutti i livelli di taglio della scala.

Interpretazione dell'OR: `exp(β)` è il fattore per cui aumentano gli odds di trovarsi in una categoria **più alta anziché più bassa**, qualunque sia il punto di taglio.

```r
library(MASS)

dfB$tier_f <- factor(dfB$tier, levels = 0:3,
                     labels = c("non_pro","pro","top200","top100"), ordered = TRUE)

fit_ord <- polr(tier_f ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c,
                data = dfB, Hess = TRUE)

ctable <- coef(summary(fit_ord))
p <- 2 * (1 - pnorm(abs(ctable[, "t value"])))
cbind(ctable, "p value" = p, OR = exp(ctable[, "Value"]))
```

### Verificare l'assunzione

Il **Brant test** verifica se l'assunzione di proportional odds regge:

```r
library(brant)
brant(fit_ord)
```

Se il test è significativo, l'assunzione cade. Non è un disastro: usa un modello a **odds parziali** (`VGAM::vglm` con `cumulative(parallel = FALSE)`), che lascia variare il coefficiente fra i livelli per le variabili problematiche.

### Un avvertimento realistico

Con 43 pro divisi in tre livelli, i livelli più alti avranno pochissimi casi (magari 5 atleti nella categoria "WT top"). La stima sarà instabile. Opzioni:
- ridurre a 3 livelli (non-pro / PRT / WT);
- usare Firth anche qui, o una penalizzazione;
- riportare esplicitamente la numerosità di ogni livello e l'ampiezza degli IC.

---

## 15. Il problema della selezione

Torniamo al Problema 5. Con l'esito che abbiamo scelto — ingresso in top 100 PCS — il problema si risolve in modo più pulito che nella versione precedente della guida. Vediamo perché, e cosa resta da fare.

### 15.1 Perché l'esito top-100 elimina gran parte del problema

Nella versione precedente l'esito di qualità erano i **punti PCS**, osservabili solo per chi era diventato professionista. Da qui la necessità di modelli complicati per correggere la selezione.

Con l'esito **"entrato almeno una volta in top 100"** la situazione cambia: l'esito è definito **per tutti gli atleti della coorte**. Chi non è mai diventato professionista semplicemente non ci è mai entrato, e vale 0. Non c'è nessun condizionamento, nessun collider, nessuna attenuazione.

Questo è il motivo principale per cui la tua scelta di definire la qualità come soglia di ranking anziché come punteggio è metodologicamente buona, al di là della comodità.

**Raccomandazione**: la Domanda B va affrontata con la **logistica ordinale su tutta la coorte** (Sezione 14), con `tier` a quattro livelli. È l'analisi principale, ed è già corretta per costruzione.

### 15.2 Cosa resta comunque selezionato

Un livello di selezione rimane, e va dichiarato: la coorte osservata non è la popolazione dei tesserati, ma quella **classificata nel ranking nazionale** (e, dall'U19, quella con almeno una gara nazionale o internazionale registrata su PCS).

Tutte le probabilità stimate sono quindi condizionate a "essere già competitivo". La formulazione corretta di ogni risultato è: *"fra gli atleti presenti nel ranking U15, il X% è poi entrato in top 100"*, mai *"fra i giovani ciclisti italiani"*.

Non c'è una correzione statistica per questo: non conoscendo il denominatore reale, non possiamo stimarlo. L'unica risposta corretta è la trasparenza, ripetuta anche nel testo divulgativo.

### 15.3 Il modello hurdle, se ti serve il valore atteso

Se vuoi comunque una stima del tipo *"dato questo profilo giovanile, quanta probabilità ho di arrivare in top 100"* scomposta nelle sue due componenti, il modello a due parti resta utile — non per correggere una distorsione, ma per **interpretare**:

```
Parte 1:  P(PRO = 1 | x)                    →  logistica su tutta la coorte
Parte 2:  P(top100 = 1 | PRO = 1, x)        →  logistica sui soli pro
Prodotto: P(top100 = 1 | x)
```

```r
# Parte 1 — probabilità di diventare professionista
p1 <- logistf(PRO ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c, data = dfB)

# Parte 2 — probabilità di eccellere, condizionata all'esserci arrivati
p2 <- logistf(top100 ~ pct_U19y2_10 + pct_U23y1_10,
              data = subset(dfB, PRO == 1))

# combinazione
nd$p_pro    <- predict(p1, newdata = nd, type = "response")
nd$p_top    <- predict(p2, newdata = nd, type = "response")
nd$p_totale <- nd$p_pro * nd$p_top
```

La Parte 2 **è** condizionata sui selezionati, quindi il suo coefficiente soffre dell'attenuazione descritta nel Problema 5. Va letto e presentato come *"fra chi è arrivato"*, mai come effetto assoluto. È esattamente l'errore di lettura che rende difficile interpretare l'OR di 0,97 di Filipas et al.

Con 15-25 eventi in top 100 fra i pro, la Parte 2 tollera **un solo predittore**. Non forzarla.

### 15.4 Heckman: perché in questo studio non serve

Il modello di selezione di Heckman corregge la selezione su variabili **non osservate**, inserendo nell'equazione di esito un termine calcolato dall'equazione di selezione (l'*inverse Mills ratio*). Richiede una *exclusion restriction*: una variabile che influenzi la probabilità di firmare da professionista ma non la qualità della prestazione successiva.

Nella versione precedente della guida lo suggerivo come analisi di robustezza. **Ora lo sconsiglio**, per tre ragioni:

1. con l'esito ordinale su tutta la coorte il problema che Heckman risolve non si presenta;
2. non disponiamo di covariate plausibili per la exclusion restriction (regione e società andrebbero verificate, e sarebbero comunque discutibili);
3. con poche decine di eventi il modello è notoriamente instabile.

Lo lascio citato perché, se qualcuno obiettasse che "state guardando solo chi ce l'ha fatta", la risposta corretta è: no, l'analisi principale include tutti, ed è proprio per questo che non serve una correzione di Heckman.

### 15.5 Una nota sugli esiti continui

Se in futuro volessi usare come esito la **miglior posizione raggiunta nel ranking PCS** invece della soglia top-100, tieni presente che è una variabile fortemente asimmetrica e limitata inferiormente. In quel caso non usare la regressione lineare sui valori grezzi, ma una di queste:

| Approccio | Quando |
|---|---|
| `log(posizione)` con regressione lineare | Semplice, interpretabile in variazioni percentuali |
| Regressione quantile sulla mediana | Se pochi campionissimi dominano la coda |
| Percentile del ranking + regressione beta | Se vuoi la stessa scala del predittore |

Resta comunque valido l'avvertimento della Sezione 15.3: stimata sui soli professionisti, qualunque di queste è condizionata alla selezione.

---

## 16. Validazione: cross-validation, bootstrap, validazione temporale

### Il problema dell'ottimismo

Un modello valutato **sugli stessi dati su cui è stato stimato** appare sempre migliore di quanto sia. Ha "imparato" anche il rumore specifico di quel campione. L'AUC apparente sovrastima quella reale, e la sovrastima è tanto maggiore quanto più il modello è complesso e il campione piccolo. Con 43 eventi, la sovrastima può essere sostanziale.

Esistono tre modi per correggere.

### 16.1 Cross-validation (k-fold)

1. Dividi il campione in k parti (tipicamente 10).
2. Stima il modello su k−1 parti, valutalo sulla parte esclusa.
3. Ripeti k volte, ruotando la parte esclusa.
4. Media le k performance.

**Stratificazione obbligatoria**: con eventi rari, ogni fold deve contenere una proporzione simile di pro, altrimenti alcuni fold avranno 0 eventi e l'AUC non è calcolabile. Usa `createFolds(y, k = 10)` di `caret`, che stratifica automaticamente.

**Ripetizione**: fai *repeated* CV (per esempio 10 fold × 20 ripetizioni) e media, perché con pochi eventi il risultato di una singola CV è instabile.

**Errore critico da evitare — data leakage**: se fai selezione di variabili, imputazione o normalizzazione **prima** della CV, i fold di test hanno già "visto" i dati di training. La CV va costruita in modo che *ogni passaggio dell'analisi* sia dentro il ciclo. Con `caret` o `tidymodels` questo si gestisce con recipe/pipeline.

### 16.2 Bootstrap con correzione dell'ottimismo (metodo di Harrell)

È il metodo raccomandato quando il campione è piccolo, perché usa tutti i dati per il modello finale.

Procedura:
1. Stima il modello sul campione completo → AUC apparente.
2. Estrai un campione bootstrap (n osservazioni con reinserimento).
3. Ristima il modello **da zero** sul campione bootstrap → AUC sul bootstrap.
4. Applica quel modello al campione originale → AUC sull'originale.
5. Ottimismo di questa replica = (3) − (4).
6. Ripeti 500-1000 volte, media gli ottimismi.
7. **AUC corretta = AUC apparente − ottimismo medio.**

```r
library(rms)
fit_rms <- lrm(PRO ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c,
               data = dfB, x = TRUE, y = TRUE)
validate(fit_rms, B = 1000)
```

L'output ti dà il Dxy corretto (`AUC = Dxy/2 + 0.5`), lo slope di calibrazione corretto, e l'R² di Nagelkerke.

### 16.3 Validazione temporale

La più convincente per un revisore, perché imita l'uso reale del modello: **addestri sul passato e predici sul futuro**.

```
Training:   coorti di nascita 1990-1996
Validation: coorti di nascita 1997-2000
```

Se la performance regge, il modello è robusto ai cambiamenti nel tempo (regolamenti, struttura del ciclismo giovanile, mercato pro). Se crolla, hai scoperto qualcosa di importante: i pattern non sono stabili nel tempo, e va discusso.

**Fai tutti e tre.** Non sono alternativi: bootstrap per la stima interna corretta, validazione temporale come test di generalizzabilità, CV per la scelta di λ nei modelli penalizzati.

---

## 17. Test statistici di supporto

Riepilogo dei test minori che compaiono nel piano, con la loro logica.

### Mann-Whitney U (Wilcoxon rank-sum)

Confronta due gruppi indipendenti senza assumere normalità. Lavora sui **ranghi** anziché sui valori.

Verifica: la probabilità che un'osservazione presa a caso dal gruppo A superi una presa a caso dal gruppo B è 0,5?

Serve perché i punteggi giovanili sono estremamente asimmetrici e il t-test non è appropriato.

```r
wilcox.test(pct_U19y2 ~ PRO, data = dfB)
```

**Ma non fermarti al p-value.** Con 1300 vs 43, qualunque differenza minima risulta significativa. Riporta l'effect size.

### Cliff's delta

Effect size non parametrico, compagno naturale di Mann-Whitney. Va da −1 a +1:

```
δ = P(X_A > X_B) − P(X_A < X_B)
```

δ = 0 significa distribuzioni completamente sovrapposte; δ = 1 significa separazione totale.

Soglie convenzionali: |δ| < 0,15 trascurabile; < 0,33 piccolo; < 0,47 medio; ≥ 0,47 grande.

```r
library(effsize)
cliff.delta(pct_U19y2 ~ PRO, data = dfB)
```

Nota elegante: Cliff's delta è legato all'AUC dalla relazione `AUC = (δ + 1)/2`. Quindi un δ = 0,6 corrisponde a un'AUC univariata di 0,80. Comodo per collegare la descrittiva ai modelli.

### Chi-quadro: perché in questo studio non serve

Nella versione precedente della guida questa sezione descriveva il test chi-quadro di bontà di adattamento per il Relative Age Effect. **Con i dati disponibili non è applicabile**: il RAE richiede il mese o il trimestre di nascita, e per la coorte generale disponiamo solo dell'anno.

Lo lascio segnalato per due ragioni. La prima è che, se in futuro riuscissi a ottenere le date complete (per esempio da un'estrazione FCI), il RAE tornerebbe eseguibile e sarebbe interessante proprio nella fascia U15, dove Mostaert ha trovato l'effetto più marcato in Belgio. La seconda è che, se decidessi di farlo, l'errore da non commettere è usare come distribuzione attesa 25/25/25/25: le nascite non sono uniformi nell'anno e variano fra coorti, quindi il riferimento corretto sono i dati **ISTAT** delle coorti effettive. È esattamente l'errore commesso da Filipas et al. (2024), il cui picco osservato nel terzo trimestre è verosimilmente stagionalità delle nascite italiane e non un effetto sportivo.

Il chi-quadro resta comunque utile nello studio per un altro scopo: confrontare distribuzioni osservate e attese in tabelle di contingenza, per esempio la distribuzione delle coorti fra atleti matchati e non matchati nel collegamento con PCS.

### Test di DeLong

Confronta due AUC calcolate **sugli stessi soggetti** (dati appaiati). Tiene conto della correlazione fra le due curve, che un test naïve ignorerebbe.

```r
roc.test(roc_M2, roc_M3, method = "delong")
```

### Brant test

Verifica l'assunzione di proportional odds nella logistica ordinale (Sezione 14).

### Test di Hosmer-Lemeshow

Test di calibrazione classico: raggruppa in decili di rischio predetto e confronta osservati vs attesi con un chi-quadro. È il test citato nel lavoro di Gallo. Oggi è considerato superato (il risultato dipende arbitrariamente dal numero di gruppi, ed è poco potente), ma riportarlo mantiene la continuità con la letteratura. Affiancalo sempre al calibration plot.


---


# PARTE III — ESECUZIONE

## 18. Piano operativo passo-passo

Ogni step indica: **cosa fare**, **perché**, **come verificare di averlo fatto bene**.

---

### FASE 0 — Verifiche preliminari

**STEP 1. Verificare da quale anno ciclismo.info riporta le classifiche U15**

*Cosa*: aprire ciclismo.info e risalire indietro nel tempo sulle classifiche Esordienti, annotando la prima stagione disponibile.
*Perché*: **determina le coorti utilizzabili e quindi la dimensione dell'intero studio.** Filipas documenta il 2007 per U19 e U23, ma non è detto che le categorie più giovani partano dallo stesso anno.
*Verifica*: se la prima stagione U15 è il 2007, le coorti sono 1994-2000 (sette). Se è il 2009, diventano 1996-2000 (cinque), e la potenza statistica cala sensibilmente. Aggiorna il piano di conseguenza prima di procedere.

---

**STEP 2. Congelare le definizioni**

*Cosa*: scrivere `definizioni.md` con la tabella della Sezione 4, datarlo, non modificarlo più.
*Perché*: evita scelte post-hoc che gonfiano i falsi positivi.
*Verifica*: se devi modificarlo dopo aver visto i dati, documenta la modifica e riporta entrambe le versioni nell'analisi di sensibilità.

---

**STEP 3. Verificare la struttura e la composizione delle classifiche**

*Cosa*: due controlli distinti.

**(a) Il denominatore.** Per due o tre stagioni campione: quanti atleti compaiono in classifica per categoria; se compaiono anche atleti con zero punti; se il criterio di inclusione sembra cambiato nel tempo.

**(b) La composizione, categoria per categoria.** Quali gare confluiscono nel punteggio? Sappiamo che l'**U23 include le gare internazionali**. Va accertato se e in che misura lo facciano U19, U17 e U15. Modo pratico per verificarlo: prendere due o tre atleti che sappiamo aver corso all'estero da Juniores (rintracciabili su PCS) e controllare se il loro punteggio nel ranking italiano riflette quei risultati.

*Perché*: (a) determina come vanno formulate tutte le conclusioni; (b) determina **se serve costruire il predittore armonizzato** per l'U19 (Problema 4, Sezione 2). Senza questa verifica, la curva della Domanda C è ambigua fra crescita reale della predittività e cambio di strumento di misura.

*Verifica*: annota entrambe le risposte nel file delle definizioni, con la data e il metodo usato per accertarle.

---

**STEP 4. Contare gli eventi disponibili, prima di progettare i modelli**

*Cosa*: costruire l'elenco dei professionisti italiani nati 1994-2000 e contare quanti sono entrati almeno una volta in top 100 e in top 200 del ranking annuale PCS.
*Perché*: con meno di 15 eventi in top 100 la Domanda B non è modellabile e va ridimensionata a descrittiva. È meglio saperlo adesso.
*Verifica*: riporta i tre numeri (pro totali, top 200, top 100) e decidi di conseguenza il numero massimo di predittori (regola dei 10 eventi per variabile, Sezione 8).

---

### FASE 1 — Costruzione del dataset

**STEP 5. Estrarre e costruire la Tabella A (atleta × stagione)**

*Cosa*: un record per atleta e stagione, con `athlete_id` anonimo e stabile, secondo lo schema della Sezione 5.
*Verifica*:

```r
dfA |> count(athlete_id, season) |> filter(n > 1)              # duplicati
dfA |> filter(category == "U15" & !age %in% 13:14)             # età incoerenti
dfA |> group_by(athlete_id) |> arrange(season) |>
       summarise(salto = any(diff(season) > 1))                # buchi di carriera
dfA |> count(season, category, cat_year)                       # copertura per cella
```

L'ultimo controllo è quello che rivela le lacune della fonte: se una cella ha molti meno atleti delle celle adiacenti, è un problema di copertura, non un fenomeno reale.

---

**STEP 6. Matching con ProCyclingStats**

*Cosa*: match automatico su cognome + nome + anno di nascita, poi fuzzy sui residui, poi **verifica manuale al 100% dei candidati professionisti**.
*Perché*: è il punto di massima perdita di dati e di massimo impatto degli errori.
*Verifica*: riporta il tasso di match; confronta la distribuzione dei percentili fra matchati e non matchati; conta e documenta i casi di omonimia risolti a mano.

---

**STEP 7. Normalizzare i punteggi**

*Cosa*: calcolare `pct_rank`, `z_log_pts`, `top10` dentro ogni cella stagione × categoria × anno di categoria.
*Verifica*: plotta media e mediana dei punti grezzi per stagione. I salti che vedrai giustificano la normalizzazione, e vanno mostrati in una figura di appendice.

---

**STEP 8. Costruire la Tabella B e codificare i mancanti**

*Cosa*: pivot da lungo a largo, join con gli esiti PCS, codifica `present` / `pct_rank = NA` secondo la Sezione 5.
*Verifica*: il numero di righe deve essere uguale al numero di `athlete_id` unici; il conteggio dei professionisti deve corrispondere alla verifica manuale dello Step 6.
*Da non fare*: riempire i mancanti con l'ultimo valore disponibile.

---

### FASE 2 — Descrittiva

*Questa fase vale il 40% del valore dello studio, e nel blog post sarà probabilmente la parte più letta.*

---

**STEP 9. Tabella e grafico di attrito**

*Cosa*: quanti atleti entrano in ogni categoria, quanti proseguono, quanti arrivano al professionismo e alla top 100.
*Perché*: contestualizza tutto il resto. Nel blog post è la prima figura.

---

**STEP 10. Descrittive dei punteggi per gruppo**

*Cosa*: mediana e IQR di `pct_rank` per categoria, separatamente per livello di `tier`. Test di Mann-Whitney **con Cliff's delta** (Sezione 17).
*Verifica*: con campioni molto sbilanciati, qualunque differenza risulta significativa. Guarda gli effect size, non i p-value.

---

**STEP 11. Correlazioni fra categorie e VIF**

*Cosa*: matrice di correlazione di Spearman fra `pct_U15y1 … pct_U23y1`; calcolo dei VIF.
*Perché*: determina se puoi usare modelli non penalizzati (Sezione 9).
*Verifica*: se VIF > 5 su più variabili, la penalizzazione dello Step 14 diventa obbligatoria.

---

**STEP 12. Armonizzare la misura U19 e validare quella U23**

*Cosa*: incrociare `pct_rank` da ciclismo.info con `pcs_present` / `pcs_rank` per le stesse stagioni, con due obiettivi diversi a seconda della categoria.

**(a) U19 — costruire il predittore armonizzato.** Se il ranking Juniores risulta solo nazionale (Step 3b), costruire `pct_U19_arm`, che combina il percentile nazionale con l'informazione internazionale da PCS. La forma più semplice e robusta:

```r
dfB <- dfB |>
  mutate(
    pcs_u19_pct = ifelse(is.na(pcs_rank_u19), 0,
                         100 * (1 - (rank(pcs_rank_u19) - 1) / sum(!is.na(pcs_rank_u19)))),
    pct_U19_arm = pmax(pct_U19y2, pcs_u19_pct)   # il migliore dei due
  )
```

Il `pmax` — prendere il migliore fra rendimento nazionale e internazionale — è la scelta più difendibile: risolve proprio il caso dell'atleta forte che corre poco in Italia. Alternative da valutare: media dei due percentili, oppure percentile nazionale più un indicatore binario di presenza internazionale. Prova almeno due varianti e verifica che le conclusioni non cambino.

**(b) U23 — validare la fonte.** Qui l'informazione internazionale è già nel ranking. Calcola la correlazione di Spearman fra `pct_U23y1` e il percentile PCS della stessa stagione. Un accordo alto conferma che ciclismo.info fa quello che dichiara; un accordo basso è un campanello d'allarme sulla qualità della fonte, e va chiarito prima di procedere.

*Perché*: la parte (a) è ciò che rende interpretabile la curva della Domanda C; la parte (b) è controllo di qualità.

*Output*: uno scatter plot per categoria, con le correlazioni. Nel blog post basta il caso U19, che è quello con il messaggio comprensibile: *"alcuni ragazzi che il ranking italiano collocava a metà classifica erano fra i migliori quando correvano all'estero."*

---

### FASE 3 — Domanda A: diventare professionista

**STEP 13. Modelli univariati per categoria-anno**

```r
library(logistf)
celle <- c("pct_U15y1","pct_U15y2","pct_U17y1","pct_U17y2",
           "pct_U19y1","pct_U19y2","pct_U23y1","pct_U23y2")

res <- lapply(celle, function(v) {
  d <- dfB[!is.na(dfB[[v]]), ]
  d$x <- d[[v]] / 10
  f <- logistf(PRO ~ x + birth_year_c, data = d)
  data.frame(cella = v, n = nrow(d), eventi = sum(d$PRO),
             OR = exp(coef(f)["x"]),
             lo = exp(f$ci.lower[2]), hi = exp(f$ci.upper[2]),
             p  = f$prob[2],
             auc = as.numeric(pROC::auc(d$PRO, predict(f, type = "response"))))
})
do.call(rbind, res)
```

*Perché*: è il ponte con Gallo et al. e dà il quadro d'insieme.
*Verifica*: controlla `eventi` per ogni cella; sotto i 10 la stima è esplorativa e va dichiarata tale.

---

**STEP 14. Modello multivariato penalizzato**

*Cosa*: elastic net su tutte le categorie insieme, λ scelto per cross-validation (Sezione 9).
*Verifica*: riporta di quanto si riduce il campione (solo chi ha dati completi in tutte le celle). Usa `lambda.1se` per la parsimonia. Niente p-value da questo modello.

---

**STEP 15. Analisi di incremento (Domanda C)**

*Cosa*: sequenza M0 → M1 → M2 → M3 → M4, tutti sullo **stesso sottocampione**, con LR test, ΔAUC (DeLong) e IDI (Sezione 11).

**Da eseguire due volte**, una per ciascuna versione del predittore U19 (Problema 4, Sezione 2):

| Versione | U19 usato | Cosa misura |
|---|---|---|
| **Grezza** | `pct_U19y2` (solo nazionale) | Il gradiente così come appare nei dati di partenza |
| **Armonizzata** | `pct_U19_arm` (nazionale + PCS) | Il gradiente a parità di strumento di misura |

*Perché*: è il contributo originale dello studio, e il confronto fra le due versioni è ciò che lo rende difendibile. Se il salto U19 → U23 si riduce nella versione armonizzata, parte del gradiente era artefatto di misurazione. Se regge, la conclusione di Gallo esce rafforzata su basi più solide di quelle su cui poggiava.

*Verifica*: controlla esplicitamente con `nobs()` che il sottocampione sia identico in tutti i modelli **e fra le due versioni**. Altrimenti stai confrontando cose diverse due volte.

*Output*: il **grafico centrale** — AUC cumulata in funzione dell'età di osservazione, con bande di confidenza bootstrap, e **le due curve sovrapposte**.

```r
plot_df <- data.frame(
  eta      = rep(c(13, 15, 17, 19), 2),
  modello  = rep(c("M1 (U15)","M2 (+U17)","M3 (+U19)","M4 (+U23y1)"), 2),
  versione = rep(c("grezza","armonizzata"), each = 4),
  auc = auc_vec, lo = auc_lo, hi = auc_hi
)

ggplot(plot_df, aes(eta, auc, colour = versione, fill = versione)) +
  geom_ribbon(aes(ymin = lo, ymax = hi), alpha = .15, colour = NA) +
  geom_line() + geom_point() +
  geom_hline(yintercept = .5, linetype = 2) +
  labs(x = "Età di osservazione (anni)",
       y = "AUC cumulata per la predizione del professionismo",
       colour = "Misura U19", fill = "Misura U19")
```

---

**STEP 16. Metriche pratiche e decision curve**

*Cosa*: alla soglia di Youden, tabella 2×2 completa con sensibilità, specificità, PPV, NPV (Sezione 10.2). Più la decision curve analysis.
*Perché*: è il messaggio che arriva a società e famiglie.
*Output*: la frase-chiave del blog post. Qualcosa come: *"selezionando gli atleti sopra il 90° percentile U19 si intercetta il 74% dei futuri professionisti, ma l'88% dei selezionati non lo diventerà."*

---

**STEP 17. Modello di sopravvivenza a tempo discreto**

*Cosa*: logistica cloglog sulla tabella persona-anno, con spline dell'età, percentile ritardato, errori standard cluster-robusti (Sezione 12).
*Perché*: recupera la coorte 2001 e successive come censurate, aggiunge la dimensione temporale, permette di stimare anche l'età di transizione.
*Verifica*: nessun record dopo l'evento; censoring codificato correttamente.

---

**STEP 18. Traiettorie**

*Cosa*: modello misto sulla Tabella A → estrarre intercetta e pendenza individuali → inserirle nel modello del professionismo (Sezione 13).
*Perché*: risponde a "conta il livello o il miglioramento?", che è la domanda che gli allenatori si fanno più spesso.
*Verifica*: includi sempre intercetta **e** pendenza insieme; considera l'effetto soffitto sul percentile.
*Nota*: con i mancanti codificati onestamente, molti atleti avranno poche stagioni osservate. Lo shrinkage del modello misto gestisce la cosa correttamente, ma riporta la distribuzione del numero di stagioni per atleta.

---

### FASE 4 — Domanda B: la qualità della carriera

**STEP 19. Logistica ordinale su tutta la coorte** *(analisi principale)*

```r
dfB$tier_f <- factor(dfB$tier, levels = 0:3,
                     labels = c("non_pro","pro","top200","top100"), ordered = TRUE)

fit_ord <- MASS::polr(tier_f ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c,
                      data = dfB, Hess = TRUE)
brant::brant(fit_ord)
```

*Perché*: evita il problema di selezione, usa tutta l'informazione, un solo modello (Sezione 15.1).
*Verifica*: numerosità di ogni livello; se il livello più alto ha meno di 10 casi, accorpa top 200 e top 100 e usa tre livelli.

---

**STEP 20. Modello a due parti** *(approfondimento interpretativo)*

*Cosa*: probabilità di diventare professionista × probabilità di entrare in top 100 fra i professionisti (Sezione 15.3).
*Verifica*: la seconda parte tollera **un solo predittore**. Presenta il suo coefficiente sempre come condizionato a "fra chi è arrivato".

---

### FASE 5 — Validazione e scrittura

**STEP 21. Bootstrap con correzione dell'ottimismo**

*Cosa*: `rms::validate(fit, B = 1000)` (Sezione 16).
*Verifica*: riporta sempre AUC apparente **e** corretta. Se la differenza supera 0,05, il modello è troppo complesso per il campione: semplificalo.

---

**STEP 22. Validazione temporale**

*Cosa*: addestrare sulle coorti 1994-1997, validare sulle 1998-2000.
*Perché*: è la prova più convincente di generalizzabilità, e imita l'uso reale.
*Verifica*: se la performance crolla, non nasconderlo. Significa che i pattern cambiano nel tempo, ed è un risultato.

---

**STEP 23. Analisi di sensibilità**

Almeno queste quattro:

1. **PRO includendo le squadre Continental** — cambia il tasso di evento e forse le conclusioni;
2. **Finestra a 24 e a 26 anni** invece di 25;
3. **Qualità definita come top 200** invece di top 100;
4. **Complete case contro imputazione multipla** dei percentili mancanti (`mice`), dichiarando che l'assunzione MAR è qui discutibile.

---

**STEP 24. Confronto con machine learning** *(controllo, non analisi principale)*

*Cosa*: random forest e gradient boosting in nested cross-validation.
*Come leggerlo*: se l'AUC non migliora — esito probabile con poche decine di eventi — è un argomento a favore della parsimonia, e va scritto. Se migliora, guarda i valori SHAP per capire dove, e aggiungi il termine corrispondente al modello parametrico.
*Attenzione*: il modello finale deve restare quello parametrico e interpretabile.

---

**STEP 25. Rileggere la checklist TRIPOD**

TRIPOD è la checklist standard per gli studi di modelli predittivi: 22 voci che coprono fonte dei dati, partecipanti, esito, predittori, dimensione campionaria, gestione dei mancanti, metodi, performance, validazione, limiti.

Non stai scrivendo un articolo scientifico e nessuno te la chiederà. Usala comunque come **lista di controllo privata**: se riesci a rispondere a tutte le voci, il blog post è solido. Se ce ne sono che non sai come riempire, hai trovato un buco. Richiede un'ora e si scarica da equator-network.org.

---

### Priorità se hai tempo limitato

| Priorità | Step |
|---|---|
| **Irrinunciabili** | 1-9, 13, 15, 16, 19, 21 |
| **Molto raccomandati** | 10-12, 17, 22, 23 |
| **Valore aggiunto** | 14, 18, 20, 24, 25 |

Lo Step 1 e lo Step 4 vengono prima di tutto: determinano se lo studio, nella forma progettata, è fattibile.

---

## 19. Struttura del blog post

Il deliverable non è un articolo scientifico, e questo cambia la forma ma non il rigore. Il pubblico è misto: allenatori, dirigenti, famiglie, forse qualche addetto ai lavori.

### Struttura consigliata

**1. L'apertura — la domanda concreta** (150 parole)
Non partire dal metodo. Parti dalla scena: una società deve decidere su chi investire, un genitore si chiede se il figlio "ce la farà". Poi la domanda: i risultati a 13-14 anni dicono qualcosa?

**2. Cosa si sapeva già** (300 parole)
Gallo, Mostaert, Cesanelli, Filipas in poche righe ciascuno, con i numeri chiave. Il punto di arrivo: nessuno ha guardato sotto i 15 anni.

**3. Cosa abbiamo fatto** (250 parole)
Fonti, coorti, definizioni. In linguaggio piano. Qui vanno anche le tre righe su anonimizzazione e trattamento dei dati.

**4. Il primo risultato: l'imbuto** (200 parole + figura)
La tabella di attrito. È il contesto di tutto il resto e si capisce senza spiegazioni.

**5. Da che età il risultato inizia a contare** (400 parole + figura)
Il grafico AUC per età di osservazione. È il cuore del pezzo.

**6. Quanto ci si può fidare** (300 parole + tabella)
Il PPV. Se selezioni i primi X, quanti ne prendi e quanti ne sbagli.

**7. Chi arriva più in alto** (300 parole)
La Domanda B, con la cautela sui numeri piccoli.

**8. Cosa ne facciamo** (250 parole)
Le implicazioni pratiche, formulate come indicazioni e non come regole.

**9. I limiti** (200 parole)
In chiaro, nel corpo del testo, non in fondo in piccolo.

**10. Appendice metodologica** (in fondo o in pagina separata)
Definizioni operative, modelli, codice, tabelle complete. Serve a chi vuole controllare, e serve a te fra sei mesi.

### Regole di scrittura per questo pubblico

- **Ogni numero accompagnato dal suo margine di incertezza**, tradotto in parole: "fra il 12% e il 28%" invece di "IC 95% [0,12-0,28]".
- **Mai un odds ratio nel corpo del testo.** Traducilo in probabilità: "passa dall'1% al 5%", non "OR = 5,2".
- **Il risultato nullo va detto per esteso.** Non "non significativo", ma "non abbiamo trovato alcun effetto, e con questo campione un effetto anche piccolo lo avremmo visto" — se è vero.
- **Nessuna classifica, nessun nome, nessun esempio individuabile.** Anche in forma anonima.
- **Il messaggio pratico deve essere onesto in entrambe le direzioni**: i risultati contano davvero, e allo stesso tempo non bastano a decidere di un ragazzino.

### I limiti da dichiarare esplicitamente

1. **La fonte è un aggregatore terzo**, non una banca dati federale ufficiale: possibili lacune non documentate.
2. **Il denominatore è la popolazione classificata**, non quella tesserata. Tutte le probabilità sono condizionate.
3. **La misura non è la stessa a tutte le età.** Il ranking U23 include i risultati internazionali, quelli delle categorie inferiori no o non allo stesso modo. Abbiamo costruito una versione armonizzata dell'U19 e riportiamo entrambi i risultati, ma per U15 e U17 il limite resta: chi corre poche gare nazionali di alto livello viene sottovalutato (Hasselaar & Elferink-Gemser, 2025).
4. **Nessun dato sul numero di gare**: impossibile distinguere poco rendimento da poca attività.
5. **Nessun dato fisiologico né di maturazione**: non possiamo distinguere il talento dallo sviluppo biologico precoce, che alle età più basse è probabilmente il fattore dominante.
6. **Assenza dal ranking ambigua**: ritiro, mancato punteggio e lacuna della fonte sono indistinguibili.
7. **Solo maschi** (se è così) e **solo Italia**.
8. **Eventi rari**: intervalli ampi, potenza bassa per gli effetti piccoli.
9. **Nessun Relative Age Effect**: manca la data di nascita completa.

---

## 20. Trappole da evitare

**1. Confondere significatività statistica e rilevanza pratica.**
Con migliaia di osservazioni quasi tutto diventa significativo. Riporta sempre effect size e intervalli.

**2. Interpretare "non significativo" come "nessun effetto".**
Con poche decine di eventi la potenza è bassa. Un intervallo [0,9-2,4] non dice "nessun effetto", dice "non lo sappiamo". La distinzione è cruciale proprio per la Domanda C: il risultato interessante è un nullo **stretto**, non un nullo qualsiasi.

**3. Selezionare le variabili guardando i p-value.**
La selezione stepwise produce modelli instabili e p-value invalidi. Scegli i predittori a priori o usa la penalizzazione.

**4. Data leakage nella validazione.**
Qualunque operazione fatta sull'intero dataset prima della cross-validation — selezione variabili, imputazione, standardizzazione — contamina i fold di test.

**5. Riempire i mancanti con l'ultimo valore disponibile.**
Lo hanno fatto Filipas et al., ed è la scelta che replicherei meno volentieri. Inventa continuità dove non c'è.

**6. Usare i punti grezzi.**
Ripetuto perché è l'errore più probabile e più dannoso.

**6-bis. Confrontare categorie misurate in modo diverso.**
Il ranking U23 include le gare internazionali, quelli giovanili no. Mettere i due percentili sullo stesso grafico senza dirlo significa attribuire alla predittività una differenza che è di strumento. È l'errore specifico che questa versione della guida serve a evitare.

**7. Ignorare l'effetto coorte.**
Il ciclismo giovanile italiano del 2007 non è quello del 2019. `birth_year` va sempre nel modello.

**8. Dimenticare che il denominatore è già selezionato.**
Ogni volta che scrivi una percentuale, chiediti: percentuale di chi?

**9. Presentare i risultati come strumento di selezione individuale.**
Statisticamente ingiustificabile con quel PPV, ed eticamente problematico su minori. Il framing corretto è: *comprendere il percorso di sviluppo*, non *identificare i predestinati*.

**10. Quantificare male il risultato nullo.**
Se l'U15 non predice, non scrivere "nessuna associazione significativa". Scrivi: *"OR per +10 percentile = 1,03, intervallo 0,97-1,09; guadagno in AUC rispetto al modello base = 0,004"*. Il primo è un non-risultato, il secondo è un risultato.

---

## 21. Glossario e riferimenti

### Glossario

**AUC / ROC** — Area sotto la curva ROC. Probabilità che il modello assegni un punteggio più alto a un caso rispetto a un non-caso presi a caso.

**Bootstrap** — Ricampionamento con reinserimento dal campione osservato, per stimare l'incertezza o correggere l'ottimismo.

**Calibrazione** — Corrispondenza fra probabilità predette e frequenze osservate.

**Censoring (a destra)** — Si sa che l'evento non è ancora accaduto, ma non se accadrà dopo.

**Cliff's delta** — Effect size non parametrico per il confronto fra due gruppi.

**Cloglog** — Funzione di link che rende il modello a tempo discreto equivalente a un modello a rischi proporzionali.

**Collider bias** — Distorsione introdotta condizionando su una variabile causata da due o più fattori.

**Cross-validation** — Divisione ripetuta del campione in training e test per stimare la performance fuori campione.

**DCA** — Decision curve analysis: beneficio netto di un modello a diverse soglie decisionali.

**Effetti fissi / casuali** — Nei modelli misti: parametri comuni a tutti / deviazioni individuali.

**Elastic net** — Regressione penalizzata che combina ridge e lasso.

**EPV** — Eventi per variabile. Minimo raccomandato: 10.

**Firth** — Correzione penalizzata della verosimiglianza per eventi rari e separazione.

**Hurdle model** — Modello a due parti: probabilità dell'evento × intensità condizionata.

**IDI** — Guadagno nella separazione media fra casi e non casi.

**Imputazione multipla** — Generazione di più dataset completi per gestire i mancanti, con combinazione via regole di Rubin.

**Leakage** — Contaminazione dei dati di test con informazione dei dati di training.

**Logit** — Logaritmo degli odds; scala su cui la logistica è lineare.

**MAR** — Missing at random: la mancanza è spiegabile con le variabili osservate.

**Multicollinearità** — Correlazione elevata fra predittori; instabilizza i coefficienti.

**NPV / PPV** — Valore predittivo negativo / positivo.

**Odds ratio** — Rapporto fra odds; `exp(β)` nella logistica.

**Ottimismo** — Sovrastima della performance dovuta alla valutazione sugli stessi dati usati per la stima.

**Percentile** — Posizione relativa in una distribuzione, 0-100.

**Proportional odds** — Assunzione della logistica ordinale: effetto costante a tutti i punti di taglio.

**Shrinkage** — Contrazione delle stime verso la media, per stabilizzarle.

**Spline** — Funzione flessibile a tratti per modellare relazioni non lineari.

**TRIPOD** — Checklist di reporting per studi di modelli predittivi.

**VIF** — Variance inflation factor, indice di multicollinearità.

### Riferimenti essenziali

**Nel dominio**
- Gallo G. et al. (2022). Do race results in youth competitions predict future success as a road cyclist? *Int J Sports Physiol Perform*, 17(4), 621-626.
- Filipas L. et al. (2024). Performance trajectories of Italian professional cyclists. *Int J Performance Analysis in Sport*.
- Mostaert M. et al. (2022). The importance of performance in youth competitions. *Eur J Sport Sci*, 22(4), 481-490.
- Cesanelli L. et al. (2022). Transition from youth categories to elite cycling. *J Sports Med Phys Fitness*, 62(12), 1577-1583.
- Hasselaar J.J. & Elferink-Gemser M.T. (2025). How to quantify youth cycling performance? *Current Issues in Sport Science*, 10(1), art. 012. **Accesso libero** — è il riferimento chiave sui limiti dei ranking nazionali.

**Metodologia**
- Harrell F.E. *Regression Modeling Strategies*, 2ª ed., Springer 2015 — validazione, ottimismo, spline, penalizzazione.
- Steyerberg E.W. *Clinical Prediction Models*, 2ª ed., Springer 2019 — il più leggibile sui modelli predittivi.
- Hosmer, Lemeshow & Sturdivant. *Applied Logistic Regression*, 3ª ed., Wiley 2013.
- Heinze G. & Schemper M. (2002). A solution to the problem of separation in logistic regression. *Stat Med*, 21(16), 2409-2419.
- Singer J.D. & Willett J.B. *Applied Longitudinal Data Analysis*, Oxford 2003 — capitoli 10-12 sulla sopravvivenza a tempo discreto.
- Collins G.S. et al. (2015). TRIPOD statement. *BMJ*, 350, g7594. **Accesso libero**.

**Pacchetti R**
`dplyr`, `tidyr` · `logistf` (Firth) · `glmnet` (penalizzazione) · `pROC` (ROC, DeLong) · `rms` (validazione, calibrazione) · `MASS` (`polr`) · `brant` · `lme4` (modelli misti) · `splines`, `sandwich`, `lmtest` (sopravvivenza a tempo discreto ed errori robusti) · `mice` (imputazione) · `dcurves` (DCA) · `effsize` (Cliff's delta)
