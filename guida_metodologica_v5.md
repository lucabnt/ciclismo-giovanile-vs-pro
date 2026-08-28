# Guida metodologica allo studio

## Ranking giovanili italiani e transizione al professionismo: predire l'accesso e la qualità della carriera

*Documento di lavoro — impostazione, metodi statistici spiegati da zero, piano operativo*
*Versione 5 — società e regione disponibili come variabili tempo-varianti*

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
| Esito di qualità | Punti PCS continui | **Esito ordinale**: pro / top 500 / top 100 (PCS) almeno una volta |
| Coorti | 1990-2000 | **1994-2000** (più 1993 parziale, 2001 censurata) |
| Deliverable | Articolo scientifico | **Blog post** con appendice metodologica |
| Comitato etico | Richiesto | Non applicabile; **restano gli obblighi su dati di minori** |

### Cosa è cambiato nella versione 5

Disponiamo di **società e regione**, ma sono variabili che **cambiano nel corso della carriera giovanile**. Questo ha una conseguenza concettuale importante e alcune conseguenze pratiche.

La conseguenza concettuale è che quasi sempre si tratta di **mediatori, non di confondenti**: se un buon risultato a 14 anni fa sì che l'atleta venga ingaggiato da una società migliore, che a sua volta ne favorisce lo sviluppo, allora la società sta sul percorso causale e controllarla significa sottostimare l'effetto che si vuole misurare. L'unica variabile di contesto legittima come controllo è quella misurata **prima** del predittore: la regione al primo anno osservato.

Il rovescio positivo è che, proprio in quanto mediatori, mobilità e cambio di regione sono **esiti intermedi interessanti** che nessuno ha mai misurato.

| Dove | Cosa cambia |
|---|---|
| Problema 7 (nuovo) | Mediatori, over-adjustment, e quali variabili di contesto sono ammissibili |
| Sezione 3 | Società e regione fra i dati disponibili, marcate come tempo-varianti |
| Sezione 5 | Variabili derivate (mobilità, cambio regione, qualità della società) e canonicalizzazione dei nomi |
| Sezione 13 | Come raggruppare per società quando gli atleti cambiano società |
| Sezione 15 | Aggiornata la motivazione per cui Heckman resta sconsigliato |
| Etica | Le combinazioni società × regione × anno × categoria possono identificare singoli minori |

### Cosa era cambiato nella versione 4

Due modifiche, entrambe migliorative.

**① Soglia di qualità al top 500.** Il top 200 lasciava una banda intermedia di 6-8 atleti, troppo sottile per stabilizzare un livello del modello ordinale. Il top 500 ne lascia 25-35 ed è inoltre una **fascia ufficiale di PCS** (che usa gli scaglioni 10/25/50/100/200/500/1000 nella propria scala di qualità), quindi non è una soglia arbitraria come il top 400 di Filipas. Aggiunta anche la gestione dell'esposizione: l'esito si misura **entro i 26 anni**, perché "almeno una volta" premia chi ha avuto più stagioni.

**② Date di nascita complete disponibili.** Torna eseguibile l'analisi del Relative Age Effect, che nella versione 3 avevo dovuto togliere. Non è un semplice ripristino: avendo le date per **tutta la coorte** e non solo per i professionisti, possiamo separare il RAE di composizione da quello di successo — la distinzione che rende il lavoro di Voet più informativo degli altri — e usare l'età relativa come controllo parziale della maturazione biologica nei modelli U15 e U17.

| Dove | Cosa cambia |
|---|---|
| Sezione 1 | Reintrodotta la **Domanda D** sul Relative Age Effect |
| Problema 6 (nuovo) | La maturazione biologica come confondente, e l'età relativa come controllo parziale |
| Sezione 3-4 | Data di nascita fra i dati disponibili; esito ordinale con soglia top 500 e finestra ai 26 anni |
| Sezione 15 | Modello a stadi successivi (pro → top 500 → top 100) invece che a due parti |
| Sezione 17 | Ripristinata la sezione sul chi-quadro, con l'avvertimento sull'atteso ISTAT |
| Step 13 (nuovo) | Analisi RAE: composizione e successo |
| Struttura del blog post | Aggiunta una sezione sul mese di nascita |

#### Versione 3

Una sola informazione, ma con conseguenze estese: **la classifica U23 di ciclismo.info tiene conto dei risultati nelle gare internazionali**, quelle delle categorie inferiori no (o non allo stesso modo).

Questo significa che le categorie non sono misurate con lo stesso strumento, e che parte del gradiente "il segnale cresce con l'età" potrebbe essere un artefatto di misurazione anziché un fenomeno reale. È esattamente la conclusione principale della letteratura, quindi il punto merita attenzione.

Le modifiche conseguenti:

| Dove | Cosa cambia |
|---|---|
| Problema 4 (Sezione 2) | Riscritto: da "punteggi non comparabili fra anni" a "non comparabili né fra anni né fra categorie", con la soluzione dei due predittori paralleli |
| Sezione 3 | La descrizione della fonte specifica la composizione per categoria; PCS serve ad **armonizzare** l'U19 e a **validare** l'U23 |
| Step 3 | Aggiunta la verifica della composizione delle classifiche categoria per categoria |
| Step 12 | Riscritto: costruzione del predittore U19 armonizzato e controllo di qualità sull'U23 |
| Step 16 | L'analisi di incremento va eseguita **due volte**, con misura grezza e armonizzata, e le due curve vanno sovrapposte |
| Limiti e trappole | Aggiornati di conseguenza |

---

# Indice

**PARTE I — Impostazione**
1. Le domande di ricerca (A: accesso · B: qualità · C: età di informatività · D: effetto età relativa)
2. Perché non basta una regressione semplice: i sette problemi
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

**Domanda B — Qualità.** Fra chi arriva, i punteggi giovanili predicono il livello raggiunto nella carriera professionistica, misurato su una scala a più livelli — ruolo pieno nel gruppo di vertice (top 500) e risultati propri (top 100) — piuttosto che su un singolo evento binario?

**Domanda C — Età di informatività.** A partire da quale età il risultato agonistico comincia a contenere informazione *aggiuntiva* rispetto a quella già disponibile? Cioè: sapere come è andato un ragazzo a 14 anni cambia qualcosa, una volta che so come è andato a 18?

### Perché la domanda C è la più importante

Gallo et al. (2022) partono dall'U17. Mostaert et al. (2022) includono l'U15 ma solo per il Relative Age Effect e solo su atleti con almeno un top-10. **Nessuno ha mai verificato se il risultato agonistico a 13-14 anni predica l'accesso al professionismo** su una popolazione ampia.

Se il risultato è "a 13-14 anni il ranking non predice nulla di utile", questo ha implicazioni immediate sui criteri di reclutamento delle società. È un risultato **negativo ma utile**, e va progettato per essere quantificato bene, non liquidato come "non significativo".

### Domanda D — L'effetto dell'età relativa

Ora che disponiamo delle **date di nascita complete** per l'intera coorte, torna eseguibile una quarta domanda, che nella versione precedente della guida avevo dovuto togliere:

**I nati nei primi mesi dell'anno sono avvantaggiati, e fino a quale età?**

Non è una domanda accessoria: è probabilmente il secondo contributo originale dello studio, per tre ragioni.

**È mai stata posta sugli Esordienti italiani.** Mostaert et al. (2022) trovano l'effetto in Belgio proprio nella fascia U15, attenuato in U17 e assente in U19. Gallo et al. (2022) partono dall'U17 e non lo trovano. Nessuno ha guardato l'U15 italiano, che è esattamente la finestra d'età in cui l'effetto belga era più marcato.

**Possiamo distinguere due fenomeni che la letteratura spesso confonde.** Avendo le date per tutti — non solo per i professionisti — possiamo misurare separatamente:

- il **RAE di composizione**: chi entra nel ranking? Se fra i classificati U15 i nati in gennaio-marzo sono sovrarappresentati, significa che la selezione precoce premia la maturità anagrafica;
- il **RAE di successo**: fra chi è nel ranking, il trimestre di nascita predice l'arrivo al professionismo?

È la distinzione che rende il lavoro di Voet et al. (2022) più informativo degli altri: loro trovano il RAE fra chi non arriva e non fra chi arriva, il che significa che chi seleziona sbaglia sistematicamente. Filipas et al. (2024) hanno potuto guardare solo i professionisti, e infatti non hanno trovato nulla — ma stavano guardando il gruppo sbagliato.

**Serve anche alla Domanda C.** È il punto più importante, e lo sviluppo nel Problema 6 della prossima sezione: il trimestre di nascita è un indicatore grezzo ma reale della **maturazione biologica**, che alle età più basse è probabilmente il fattore dominante del risultato agonistico. Poterlo controllare cambia il significato di ciò che misuriamo a 13-14 anni.

## 2. Perché non basta una regressione semplice: i sette problemi

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

### Problema 6 — La maturazione biologica, e come la data di nascita ci aiuta

A 13-14 anni la differenza fra due ragazzi può essere quasi interamente **anagrafica e biologica**, non di talento. Un nato a gennaio ha fino a undici mesi in più di un nato a dicembre — a quell'età sono una quantità enorme di sviluppo — e a questo si somma la variabilità dello scatto puberale, che può separare due coetanei anagrafici di due o tre anni di età biologica.

Questo è il limite che accomuna tutti gli studi di talent identification giovanile, ed è la ragione per cui Mostaert et al. (2022) trovano che nella coorte U15 **maturità e coordinazione motoria** sono gli unici predittori significativi, ciascuno per circa il 5% della varianza. Non stavano misurando il talento: stavano misurando chi era cresciuto prima.

Non abbiamo dati di maturazione (età scheletrica, picco di crescita staturale), e non li avremo mai da un archivio di classifiche. Ma con la data di nascita abbiamo un **proxy grezzo e gratuito**: il trimestre, o meglio ancora l'età esatta in giorni al 31 dicembre della stagione.

**La conseguenza operativa è importante.** Inserendo l'età relativa come covariata nei modelli U15 e U17, la domanda cambia di significato:

| Modello | Domanda a cui risponde |
|---|---|
| `PRO ~ pct_U15y2` | Il risultato a 14 anni predice il professionismo? |
| `PRO ~ pct_U15y2 + eta_relativa` | Il risultato a 14 anni predice il professionismo, **al netto di quanto un ragazzo è più vecchio dei suoi coetanei di categoria**? |

La seconda è la domanda che interessa davvero a un allenatore, ed è quella che nessuno ha ancora posto sui dati italiani. Se il coefficiente di `pct_U15y2` si riduce sensibilmente introducendo l'età relativa, hai una misura — parziale ma concreta — di quanto il risultato a 14 anni sia sviluppo anziché talento.

**Attenzione a non pretendere troppo.** L'età relativa cattura solo la componente *anagrafica* della maturazione, non quella individuale: due ragazzi nati lo stesso giorno possono avere due anni di differenza biologica. Il controllo è quindi **parziale**, e va presentato come tale. Se dopo l'aggiustamento il coefficiente resta invariato, non hai dimostrato che non c'è confondimento da maturazione: hai dimostrato che non c'è confondimento dalla parte di maturazione spiegata dal mese di nascita, che è una frazione del totale.

Resta comunque il miglior controllo disponibile a costo zero, e non usarlo — avendo il dato — sarebbe uno spreco.

### Problema 7 — Società e regione: confondenti o mediatori?

Abbiamo la società e la regione, ma **cambiano nel corso della carriera**, anche fra le categorie giovanili. Un atleta può correre da U15 per una piccola società di provincia, passare da U17 a una squadra forte di un'altra regione, e cambiare ancora da U19. Questo apre tre questioni distinte, e la terza è la più importante.

**(a) Sono attributi dell'atleta-stagione, non dell'atleta.**
Vanno tenuti nella Tabella A, dove il record è già atleta × stagione, e non nella Tabella B. Se ti servono nella tabella larga, devi derivarne dei riassunti espliciti — società del primo anno U15, società dell'ultimo anno giovanile, numero di cambi, regione prevalente — e ciascuno di questi è una scelta che va dichiarata, non un dato oggettivo.

**(b) La struttura di raggruppamento non è pulita.**
I modelli multilivello classici assumono che ogni atleta appartenga a un solo gruppo. Qui gli atleti attraversano più società, il che tecnicamente configura una struttura a **multiple membership**. Le opzioni, in ordine di complessità, sono nella Sezione 13.

**(c) Il rischio di over-adjustment — il punto serio.**
La tentazione naturale è mettere la società fra le covariate "per controllare il contesto". Nella maggior parte dei casi sarebbe un errore, perché la società non è un confondente ma un **mediatore**:

```
risultato a 14 anni  →  reclutato da una società forte a 16  →  professionista
```

Se un buon risultato da U15 fa sì che l'atleta venga notato e ingaggiato da una squadra migliore, e quella squadra a sua volta ne favorisce lo sviluppo, allora la società a 16 anni sta **sul percorso causale** fra il predittore e l'esito. Controllarla significa bloccare parte dell'effetto che stai cercando di misurare, e sottostimare il coefficiente dell'U15. In letteratura questo si chiama over-adjustment, o *controlling for a post-treatment variable*, ed è un errore frequente e poco riconosciuto.

La regola pratica è semplice: **una variabile misurata dopo il predittore non va inserita come controllo**, a meno che tu non stia deliberatamente stimando un effetto diretto al netto della mediazione — che è una domanda diversa e va dichiarata come tale.

Il che porta a una distinzione da tenere ferma per tutta l'analisi:

| Variabile | Momento | Ruolo | Va nel modello? |
|---|---|---|---|
| Regione al **primo anno U15** | Prima del predittore | Possibile confondente (densità di gare, opportunità di partenza) | **Sì**, legittima |
| Società al primo anno U15 | Contemporanea al predittore | Ambigua | Con cautela, e come sensibilità |
| Società o regione **successive** | Dopo il predittore | **Mediatore** | **No**, se stimi l'effetto totale |
| Numero di cambi di società | Riassunto di tutta la carriera | Mediatore / esito intermedio | No come controllo; **sì come oggetto di studio** |

**Il rovescio positivo.** Proprio perché sono mediatori, queste variabili sono interessanti **come esiti intermedi**, e la letteratura non le ha mai guardate:

- **La mobilità.** Cambiare società può significare essere reclutati (segnale positivo) oppure instabilità e ricerca di una sistemazione (segnale negativo). Sono ipotesi opposte e distinguibili nei dati: se `n_cambi` predice positivamente il professionismo, prevale il reclutamento.
- **Il cambio di regione.** In Italia spostarsi di regione per correre è una scelta impegnativa, che di solito segnala insieme talento riconosciuto e forte investimento familiare. È probabilmente il segnale più forte fra quelli disponibili — e nessuno lo ha misurato.
- **L'ambiente di sviluppo.** Si può costruire un indicatore di qualità della società (quanti suoi atleti sono arrivati al professionismo nelle coorti precedenti) e verificare se, a parità di risultato individuale, l'ambiente aggiunge qualcosa. È una domanda di grande interesse pratico per le società stesse.

Nessuna di queste è la domanda principale dello studio, ma la prima e la seconda costano poco e possono diventare un paragrafo molto letto del blog post.

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
| Data di nascita completa | **Sì**, per l'intera coorte | Rende possibili l'analisi RAE e il controllo parziale della maturazione |
| Numero di gare disputate (giovanili) | **No** | Impossibile calcolare un success rate normalizzato alla Mostaert; impossibile distinguere "poche gare" da "poco rendimento" |
| Elenco completo tesserati FCI | **No** | Il denominatore è la popolazione classificata, non quella tesserata |
| Società | **Sì**, ma **variabile nel tempo** | Va trattata come attributo dell'atleta-stagione, non dell'atleta. Utile come raggruppamento e come misura di mobilità |
| Regione / comitato | **Sì**, ma **variabile nel tempo** (segue la società) | Proxy della densità di gare e delle opportunità locali; attenzione al ruolo di mediatore |
| Status professionistico e squadra | **Sì**, da PCS | Esito primario |
| Ranking annuale PCS da pro | **Sì** | Esito di qualità |
| Ranking PCS U19/U23 | **Sì**, per chi corre gare registrate | Predittore aggiuntivo prezioso, vedi sotto |

### Tre conseguenze da mettere subito in chiaro

**① Il Relative Age Effect è analizzabile, e su una fascia d'età mai studiata.** Avendo le date per tutti e non solo per i professionisti, possiamo separare il RAE di composizione da quello di successo (Domanda D) e usare l'età relativa come controllo parziale della maturazione (Problema 6). Verifica però la **completezza** del campo: se le date mancano per una quota non trascurabile di atleti, controlla che i mancanti non siano sistematici (per esempio concentrati nelle coorti più vecchie o fra i meno classificati) prima di procedere.

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

### Le coorti: perché 1996-2000

**Verificato sui dati (27 agosto 2026).** Le classifiche Esordienti di ciclismo.info **partono dal 2009**, non dal 2007 come le categorie U17, U19 e U23. È l'esito sfavorevole fra i due che lo STEP 1 prevedeva, e sposta in avanti di due anni tutta la finestra.

Con l'U15 coperto dal **2009** e l'esito osservabile fino al **2025**, la finestra utilizzabile è:

| Nato | U15y1 | U15y2 | U19y1 | U23y1 | Compie 25 |
|---|---|---|---|---|---|
| 1994 | 2007 ✗ | 2008 ✗ | 2011 | 2013 | 2019 |
| 1995 | 2008 ✗ | 2009 ✓ | 2012 | 2014 | 2020 |
| **1996** | **2009 ✓** | 2010 | 2013 | 2015 | 2021 |
| **1997** | 2010 | 2011 | 2014 | 2016 | 2022 |
| **1998** | 2011 | 2012 | 2015 | 2017 | 2023 |
| **1999** | 2012 | 2013 | 2016 | 2018 | 2024 |
| **2000** | 2013 | 2014 | 2017 | 2019 | **2025 ✓** |
| 2001 | 2014 | 2015 | 2018 | 2020 | 2026 ✗ |

**Analisi principale: coorti 1996-2000, cinque coorti complete.** Circa 2.800 atleti maschi.

**Estensioni**, tutte più numerose dell'analisi principale perché non richiedono l'U15 primo anno:

| Analisi | Coorti | N coorti | Atleti (M) |
|---|---|---|---|
| Dall'U15y2 | 1995-2000 | 6 | ~3.350 |
| Dall'U17y1 | 1992-2000 | 9 | ~4.740 |
| Dall'U19y1 | 1990-2000 | 11 | ~5.500 |
| Sopravvivenza a tempo discreto, con censura | tutte | — | ~12.400 |

**Conseguenza sulla potenza.** Cinque coorti invece di sette significa circa il 30% di eventi in meno di quanto stimato più avanti in questa sezione: le attese vanno lette al ribasso nella stessa proporzione, ed è il motivo per cui lo STEP 4 va eseguito prima di progettare i modelli e non dopo.

**Contropartita.** I modelli che partono dall'U17 hanno **nove** coorti, non otto: vale la pena costruirli come analisi a sé e non solo come estensione. E il modello di sopravvivenza a tempo discreto, che assorbe le coorti 2001 e successive come censurate, diventa più importante di quanto la Sezione 12 lasci intendere.

### Definizione di PRO

**PRO = almeno una stagione con contratto in squadra UCI WorldTeam o UCI ProTeam, entro l'anno solare in cui l'atleta compie 25 anni.**

Escludiamo le Continental: sono un livello eterogeneo, spesso semi-dilettantistico, e la loro inclusione cambia sensibilmente il tasso di evento. Le terremo come **analisi di sensibilità**.

La finestra ai 25 anni serve a rendere le coorti confrontabili: senza limite, un nato nel 1994 avrebbe avuto dieci anni per firmare e un nato nel 2000 ne avrebbe avuti cinque.

### Definizione di QUALITÀ

**QUALITÀ = livello raggiunto almeno una volta nella carriera, su una scala a soglie: professionista senza mai entrare in top 500 / almeno una volta in top 500 / almeno una volta in top 100 del ranking annuale ProCyclingStats.**

### Perché top 500 e non top 200

La versione precedente di questa guida usava il top 200 come soglia intermedia fra "professionista" e "top 100". Due ragioni per cambiarla.

**Ragione 1 — le soglie non sono equidistanti in numerosità.** Con un centinaio di professionisti attesi nella coorte, la banda fra top 200 e top 100 contiene solo 6-8 atleti: troppo pochi per stabilizzare un livello del modello ordinale. La banda fra top 500 e top 100 ne contiene 20-30: lavorabile.

**Ragione 2 — top 500 non è una soglia arbitraria, è quella usata da PCS stesso.** PCS pubblica una scala ufficiale di fasce per pesare la qualità degli starter di una gara, con questi scaglioni: top 10, top 25, top 50, top 100, top 200, **top 500**, top 1000. Non esistono un top 300 o un top 400 nella loro classificazione: il gradino dopo il 200 è direttamente il 500. Il "top 400" usato da Filipas et al. (2024) è una scelta arbitraria degli autori; il top 500 è invece un punto di riferimento riconosciuto dalla fonte dati, il che rende la soglia più difendibile e più facile da giustificare nel blog post.

**Cosa rappresenta in sostanza.** Le squadre WorldTeam e ProTeam messe insieme schierano circa un migliaio di corridori. Il top 500 corrisponde grossomodo alla metà migliore del professionismo di vertice: non il gregario di fatica che fa una manciata di gare all'anno, ma il corridore con un ruolo pieno nella squadra — chi i Grandi Giri li corre davvero e ci lavora. Il top 100, sopra, individua chi ha risultati propri: capitani, classicomani, velocisti, uomini di classifica.

### Stima preliminare del numero di eventi

Filipas trova 81 professionisti italiani su sei coorti (1990-1995), circa 13-14 per coorte, applicando però un criterio di esclusione (carriera conclusa) che rimuove i più forti ancora in attività. Senza quel criterio, e riportando la stima alle nostre **cinque** coorti anziché sette, ci si può attendere **65-85 professionisti**.

Il tuo dato — 11 italiani attualmente in top 100, 24 in top 200 — è una **fotografia trasversale** su tutte le età in un solo momento. "Entrato almeno una volta" è invece **cumulativo su fino a dieci stagioni e cinque coorti**, quindi il numero atteso è più alto:

| Livello | Definizione | Numerosità attesa |
|---|---|---|
| 0 | Mai professionista | migliaia |
| 1 | Professionista, mai top 500 | 55-65 |
| 2 | Almeno una volta in top 500, mai top 100 | 25-35 |
| 3 | **Almeno una volta in top 100** | 15-20 |

Il livello 3 resta l'esito "titolare" da comunicare nel blog post; i livelli 1 e 2 servono a dare potenza statistica al modello ordinale, e la banda 1-2 ora è abbastanza ampia da essere stabile.

### Il problema dell'esposizione, e come risolverlo

"Almeno una volta in top X" dipende da **quante stagioni un atleta ha avuto a disposizione**. Nella coorte 1996-2000 il più vecchio ha potuto correre fino a otto stagioni da professionista entro il 2025, il più giovane cinque o sei. Un atleta con più occasioni ha semplicemente più probabilità di entrare in top 500 almeno una volta, indipendentemente dal suo livello — e questo si confonde con l'effetto coorte, che nel modello controlliamo già con `birth_year`.

Due soluzioni, da usare insieme come analisi principale e sensibilità:

**① Finestra fissa (analisi principale).** Definire l'esito come *miglior posizione raggiunta entro i 26 anni compiuti*, non "mai" senza limite. Rende le coorti pienamente confrontabili, allo stesso modo in cui la Sezione 4 fissa la finestra dei 25 anni per l'esito PRO. Il costo è che si tagliano fuori le maturazioni tardive — sappiamo da Kholkine et al. (2023) che il picco di rendimento arriva verso i 27 anni, quindi qualche atleta ancora in crescita a 26 anni verrà classificato più in basso di quanto sarà in seguito. È un compromesso, non un errore: va dichiarato nei limiti.

**② Esposizione come covariata (sensibilità).** In alternativa, mantenere "mai" senza limite di età ma inserire `pro_seasons` (numero di stagioni da professionista osservate) come covariata nel modello. Più semplice da costruire, ma `pro_seasons` è essa stessa una conseguenza del livello dell'atleta — chi è più forte tende a restare professionista più a lungo — quindi il suo coefficiente non ha un'interpretazione causale pulita. Usalo solo per verificare che i risultati principali non cambino, non come stima primaria.

**Precisazione tecnica da fissare adesso**: PCS pubblica sia un ranking rolling (aggiornato in continuo) sia classifiche annuali di fine stagione. Usa il **ranking annuale di fine stagione**, che è stabile e replicabile, e dichiaralo. Il sistema di punteggio PCS ha subito revisioni nel tempo, ma il "top 100" e il "top 500" restano confrontabili fra stagioni perché sono posizioni relative, non punteggi assoluti — è la stessa ragione per cui PCS li usa nella propria scala ufficiale invece dei punti grezzi, ed è una conferma indipendente che la tua scelta di lavorare per soglie di posizione è quella giusta.

### Cosa dire nel blog post per rendere il numero concreto

Il top 500 come categoria statistica dice poco a un lettore non addetto ai lavori. Per dargli corpo, accompagnalo con una descrittiva semplice e comprensibile a fianco, per esempio: *"dei N atleti entrati almeno una volta in top 500, M hanno corso almeno un Grande Giro"*.

Non usare però la partecipazione a un Grande Giro **come predittore o come livello del modello**: dipende dalle scelte di startlist delle squadre, e le squadre italiane danno storicamente più posti a corridori italiani ai propri Grandi Giri di quanti gliene darebbero altre nazionalità a parità di livello. È una variabile confusa da nazionalità e convenienza commerciale, buona solo come descrizione, non come misura.

### Riepilogo delle definizioni da congelare

Scrivile in un file `definizioni.md` datato, **prima** di guardare i dati. Se decidi le definizioni dopo aver visto i risultati, stai facendo p-hacking anche senza volerlo: scegli inconsciamente le versioni che danno risultati più belli.

| Concetto | Definizione operativa |
|---|---|
| Categorie | U15, U17, U19, U23, sempre distinte per anno di categoria |
| Coorti (analisi principale) | Nati 1996-2000 |
| Coorti (modelli dall'U17) | Nati 1992-2000 |
| Coorti (sopravvivenza) | Tutte, con censoring |
| PRO | ≥1 stagione WT o PRT entro l'anno dei 25 anni |
| QUALITÀ | livello massimo raggiunto entro i 26 anni: pro / top 500 / top 100 |
| Esito ordinale | 0 = non pro; 1 = pro senza top 500; 2 = top 500; 3 = top 100 |
| Predittore | Percentile del ranking entro stagione × categoria × anno di categoria |
| Covariate demografiche | Anno di nascita (coorte) ed età relativa entro la categoria (giorni al 31/12 o trimestre) |
| Esclusioni | Atleti stranieri; anno di nascita mancante; discipline non stradali |

---

## 5. Costruzione del dataset

### Principio generale: due tabelle

Servono due formati degli stessi dati, perché metodi diversi richiedono strutture diverse.

### Tabella A — formato "lungo" (atleta × stagione)

È la struttura naturale dei dati e quella richiesta dai modelli misti (Sezione 13) e dall'analisi di sopravvivenza (Sezione 12).

```
athlete_id      identificativo anonimo stabile
birth_date      data di nascita completa
birth_year      anno di nascita (coorte)
birth_quarter   trimestre di nascita: 1 = gen-mar ... 4 = ott-dic
rel_age         età relativa entro la categoria: giorni fra la nascita e il
                1 gennaio dell'anno di riferimento, normalizzata 0-1
season          anno solare della stagione
age             età compiuta nell'anno (= season − birth_year)
category        U15 / U17 / U19 / U23
cat_year        1, 2 (per U23: 1-4)
points_raw      punti nel ranking nazionale (da ciclismo.info)
rank_pos        posizione in classifica
n_ranked        numero totale di atleti classificati in quella cella
pcs_present     1 se l'atleta compare su PCS quella stagione (solo U19+)
pcs_rank        posizione nel ranking annuale PCS, se presente
team_id         società di appartenenza in quella stagione (canonicalizzata)
region          regione del comitato di appartenenza in quella stagione
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
athlete_id, birth_year, birth_quarter, rel_age

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

--- contesto: da usare con le cautele del Problema 7 ---
region_U15y1          regione al primo anno osservato (l'unica pre-predittore)
team_U15y1            società al primo anno osservato
team_last_youth       società nell'ultima stagione giovanile
n_team_changes        numero di cambi di società nelle categorie giovanili
changed_region        1 se ha cambiato regione durante il percorso giovanile
team_quality_U15y1    tasso storico di professionisti prodotti dalla società
                      di partenza, calcolato sulle coorti PRECEDENTI

--- esiti ---
PRO                   0/1
tier                  0 = non pro, 1 = pro senza top 500, 2 = top 500, 3 = top 100
best_pcs_pos_26       migliore posizione PCS raggiunta entro i 26 anni (finestra fissa)
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

### Il problema dei pari punti, e come la fonte lo risolve già

**Verificato sui dati.** I punteggi sono piccoli e molto discreti — mediana 7-8 punti, primo quartile 3 — e l'ordinamento per soli punti lascia a pari merito **il 92% degli atleti** in U15 e U17, l'88% in U19. Una cella U17 con 229 atleti produce appena 43 valori distinti di percentile: il predittore principale dello studio diventa una variabile a 43 livelli con enormi ammassi.

La fonte però pubblica anche vittorie e piazzamenti dal 2° al 5° posto, e li usa per sciogliere i pari punti: la posizione pubblicata è un ordinamento **totale** 1..n, senza ex aequo. Ricostruendo lo stesso criterio — punti, poi vittorie, poi 2i, 3i, 4i, 5i — con `ties.method = "min"`:

| | ex aequo, soli punti | ex aequo, criterio esteso | valori distinti per cella |
|---|---|---|---|
| U15 | 92,2% | **52,7%** | 58,6 → **160,4** |
| U17 | 93,1% | **59,4%** | 43,4 → **118,5** |
| U19 | 87,9% | **51,0%** | 43,4 → **95,6** |
| U23 | 59,6% | **28,9%** | 21,0 → **28,0** |

La granularità quasi triplica e la correlazione con la versione a soli punti resta **r = 0,996-0,998**: non è una variabile diversa, è la stessa misurata meglio. Usa `pct_rank_ext` come predittore principale e `pct_rank` come sensibilità — costa zero riportarli entrambi.

**Non usare invece la posizione pubblicata dalla fonte.** In coda alla classifica ordina in modo arbitrario atleti con record identico: nella cella U15 2015 primo anno le ultime venti posizioni sono tutte «1 punto, un quinto posto». Prenderle per buone significa inventare un ordinamento dove non ce n'è uno.

**Quale usare come predittore principale?** Il `pct_rank`. Riporta anche i risultati con `top10` come analisi di sensibilità: è la codifica usata da Mostaert e rende i risultati confrontabili con la letteratura.

**Attenzione a un'insidia specifica di questa fonte.** Se ciclismo.info include in classifica solo chi ha ottenuto almeno un punto, allora `n_ranked` varia nel tempo per ragioni che non hanno a che fare con la partecipazione reale. Controlla l'andamento di `n_ranked` per stagione e categoria: se vedi salti bruschi, è un cambio di criterio della fonte, e va documentato. Il percentile resta comunque la scelta migliore, ma il lettore va avvisato.

### Canonicalizzare i nomi delle società

I nomi delle società sono stringhe instabili: cambiano con lo sponsor, si accorpano, si abbreviano in modo incoerente da una stagione all'altra. Trattarli come identificativi grezzi produce centinaia di società fantasma e rende inutilizzabile qualunque analisi di raggruppamento o di mobilità.

Prima di qualunque uso, costruisci una tabella di corrispondenza `nome_grezzo → team_id` canonico:

1. normalizza maiuscole, accenti, punteggiatura, sigle ricorrenti (`A.S.D.`, `G.S.`, `S.C.`, `Team`);
2. raggruppa con distanza di stringa le varianti evidenti;
3. **rivedi a mano** l'elenco delle società che compaiono con più di N atleti: sono poche e sono quelle che contano.

Un cambio di sponsor **non** è un cambio di società: se non lo gestisci, ogni atleta risulterà aver cambiato squadra ogni volta che lo sponsor è cambiato, e la variabile `n_team_changes` misurerà il mercato pubblicitario invece della mobilità degli atleti.

**Attenzione a `team_quality`.** Se lo costruisci come "quanti professionisti ha prodotto questa società", calcolalo **solo sulle coorti precedenti** a quella dell'atleta. Usare le coorti in analisi significherebbe far entrare l'esito nel predittore: una forma di leakage che gonfia le prestazioni del modello e non è replicabile in un uso reale.

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

L'imputazione multipla (Sezione 18, Step 26) resta un'analisi di robustezza possibile, ma richiede l'assunzione MAR — che qui è dubbia, perché chi smette non smette a caso.

### Aspetti etici e di trattamento dei dati

Non c'è un comitato etico universitario da coinvolgere e non ci sarà una pubblicazione scientifica. Restano però obblighi sostanziali, e sono più stringenti del solito perché **i dati riguardano minori**.

**Cosa vale comunque:**

- **Anonimizzazione all'origine.** Sostituisci nomi e cognomi con `athlete_id` non reversibile nella fase di costruzione del dataset. La chiave di corrispondenza, se ti serve per la verifica manuale, va tenuta in un file separato, non condiviso, e cancellata a lavoro finito.
- **Solo aggregati nella pubblicazione.** Nessun risultato individuale, nessun esempio nominativo, nessuna tabella con celle di numerosità così bassa da rendere identificabile una persona. Regola pratica: non pubblicare celle con meno di 5 atleti.
- **Attenzione alle combinazioni identificanti.** Società, regione, anno di nascita e categoria messi insieme identificano spesso una singola persona, anche senza nome: in una società piccola c'è un solo Esordiente del 1997. Non pubblicare mai incroci di queste variabili con celle piccole, e non pubblicare risultati riferiti a società nominate.
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
| **Domanda B** — entrare in top 100 (livello 3) | 15-20 | **1, al massimo 2** |

La Domanda A ha un budget confortevole. La Domanda B è al limite: **due predittori sono il massimo**, e vanno scelti a priori (verosimilmente `pct_U19y2` e `pct_U23y1`), non selezionati guardando i dati. È anche la ragione per cui l'esito ordinale a quattro livelli (Sezione 14) è preferibile al binario: recupera potenza usando i livelli intermedi.

I numeri attesi sono stime da confermare allo Step 4 del piano operativo. Se gli eventi al livello 3 (top 100) risultassero meno di 15, accorpa i livelli 2 e 3 e usa un esito a tre soli livelli; se anche così la numerosità resta troppo bassa, la Domanda B va ridotta a descrittiva.

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

**Sull'esito di qualità il quadro è ancora più severo.** Se in top 100 entrano 15-20 atleti su qualche migliaio, il tasso di evento scende sotto lo 0,5%. Con quella base, anche un modello con AUC 0,90 produce un PPV nell'ordine di pochi punti percentuali. Il top 500, avendo più eventi (25-35), dà un PPV meno estremo ma comunque basso. Quando presenterai i risultati sulla Domanda B, calcola e riporta il PPV **separatamente per ciascun livello e separatamente da quello della Domanda A**: sono numeri molto diversi e vanno comunicati come tali.

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

### Raggruppare per società, quando gli atleti cambiano società

Gli atleti della stessa società si somigliano più di atleti presi a caso: stesso allenatore, stesso calendario di gare, stessa selezione in ingresso. Ignorarlo produce errori standard troppo stretti, cioè intervalli di confidenza ottimisticamente ristretti.

Il problema è che, come nota il Problema 7, **gli atleti attraversano più società**, quindi la struttura non è un annidamento pulito. Tre opzioni, in ordine crescente di complessità:

**① Errori standard cluster-robusti sulla società di partenza.** La soluzione più semplice e quasi sempre sufficiente. Non modella l'effetto società, ma corregge l'incertezza per il fatto che le osservazioni non sono indipendenti.

```r
library(sandwich); library(lmtest)
coeftest(fit, vcov = vcovCL(fit, cluster = dfB$team_U15y1))
```

**② Intercetta casuale sulla società di riferimento.** Scegli un momento (tipicamente la prima società osservata) e trattalo come gruppo di appartenenza. Approssimazione accettabile se la maggior parte degli atleti cambia poco, da verificare guardando la distribuzione di `n_team_changes`.

```r
lme4::glmer(PRO ~ pct_U19y2_10 + (1 | team_U15y1), family = binomial, data = dfB)
```

**③ Modello a multiple membership.** La soluzione corretta: ogni atleta contribuisce a tutte le società che ha attraversato, con pesi proporzionali alle stagioni trascorse in ciascuna. Si stima in `brms`:

```r
brms::brm(PRO ~ pct_U19y2_10 + (1 | mm(team1, team2, team3)),
          family = bernoulli(), data = dfB)
```

È tecnicamente superiore, ma richiede tempo di calcolo e una comprensione bayesiana che va oltre lo scopo di questo studio.

**Raccomandazione**: usa l'opzione ① come default. Passa alla ② solo se ti interessa quantificare **quanta** varianza sta al livello società — che è una domanda legittima e interessante per le società stesse, ma è secondaria rispetto alle Domande A-D. La ③ solo se il lavoro diventasse un articolo vero.

**Un avvertimento sulla numerosità.** Molte società avranno pochissimi atleti nella coorte, e alcune uno solo. Un'intercetta casuale stimata su un singolo atleta non contiene informazione: lo shrinkage la riporterà semplicemente alla media generale. Prima di stimare il modello, guarda la distribuzione degli atleti per società e valuta di accorpare in "altre" tutte quelle sotto una soglia minima.

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
                     labels = c("non_pro","pro","top500","top100"), ordered = TRUE)

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

Torniamo al Problema 5. Con l'esito che abbiamo scelto — livello ordinale pro / top 500 / top 100 — il problema si risolve in modo più pulito che nella versione precedente della guida. Vediamo perché, e cosa resta da fare.

### 15.1 Perché questo esito elimina gran parte del problema

Nella prima versione l'esito di qualità erano i **punti PCS**, osservabili solo per chi era diventato professionista. Da qui la necessità di modelli complicati per correggere la selezione.

Con l'esito ordinale a quattro livelli la situazione cambia: è definito **per tutti gli atleti della coorte**. Chi non è mai diventato professionista vale 0. Chi lo è diventato ma non ha mai raggiunto il top 500 vale 1. Non c'è nessun condizionamento, nessun collider, nessuna attenuazione, a nessuno dei tre gradini.

Questo è il motivo principale per cui definire la qualità per soglie di posizione, anziché come punteggio continuo, è metodologicamente buono al di là della comodità — ed è coerente con il fatto che PCS stesso usa soglie di posizione (10/25/50/100/200/500/1000) invece dei punti grezzi nella propria scala ufficiale di qualità.

**Raccomandazione**: la Domanda B va affrontata con la **logistica ordinale su tutta la coorte** (Sezione 14), con `tier` a quattro livelli (0 = non pro, 1 = pro senza top 500, 2 = top 500, 3 = top 100). È l'analisi principale, ed è già corretta per costruzione.

### 15.2 Cosa resta comunque selezionato

Un livello di selezione rimane, e va dichiarato: la coorte osservata non è la popolazione dei tesserati, ma quella **classificata nel ranking nazionale** (e, dall'U19, quella con almeno una gara nazionale o internazionale registrata su PCS).

Tutte le probabilità stimate sono quindi condizionate a "essere già competitivo". La formulazione corretta di ogni risultato è: *"fra gli atleti presenti nel ranking U15, il X% è poi entrato in top 100"*, mai *"fra i giovani ciclisti italiani"*.

Non c'è una correzione statistica per questo: non conoscendo il denominatore reale, non possiamo stimarlo. L'unica risposta corretta è la trasparenza, ripetuta anche nel testo divulgativo.

### 15.3 Il modello hurdle, se ti serve il valore atteso

Se vuoi comunque una stima del tipo *"dato questo profilo giovanile, quanta probabilità ho di raggiungere il top 100"* scomposta nelle sue componenti, il modello a più parti resta utile — non per correggere una distorsione, ma per **interpretare**. Con tre livelli oltre al non-pro ha senso scomporlo in due stadi successivi:

```
Parte 1:  P(PRO = 1 | x)                          →  logistica su tutta la coorte
Parte 2:  P(top500 = 1 | PRO = 1, x)              →  logistica sui soli pro
Parte 3:  P(top100 = 1 | top500 = 1, x)           →  logistica sui soli top 500
```

```r
# Parte 1 — probabilità di diventare professionista
p1 <- logistf(PRO ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c, data = dfB)

# Parte 2 — probabilità di raggiungere il top 500, condizionata all'esserci arrivati
p2 <- logistf(top500 ~ pct_U19y2_10 + pct_U23y1_10,
              data = subset(dfB, PRO == 1))

# Parte 3 — probabilità di raggiungere il top 100, condizionata al top 500
p3 <- logistf(top100 ~ pct_U19y2_10,
              data = subset(dfB, top500 == 1))

# combinazione
nd$p_pro    <- predict(p1, newdata = nd, type = "response")
nd$p_500    <- predict(p2, newdata = nd, type = "response")
nd$p_100    <- predict(p3, newdata = nd, type = "response")
nd$p_totale_500 <- nd$p_pro * nd$p_500
nd$p_totale_100 <- nd$p_totale_500 * nd$p_100
```

Le Parti 2 e 3 **sono** condizionate sui selezionati, quindi i loro coefficienti soffrono dell'attenuazione descritta nel Problema 5, tanto più quanto più si sale (la Parte 3, condizionata al top 500, è la più soggetta). Vanno lette e presentate sempre come *"fra chi è arrivato a quel livello"*, mai come effetto assoluto. È esattamente l'errore di lettura che rende difficile interpretare l'OR di 0,97 di Filipas et al. sui soli professionisti.

Con 25-35 eventi disponibili, la Parte 2 tollera **due predittori**. Con 15-20 eventi, la Parte 3 tollera **un solo predittore**. Non forzarle oltre.

### 15.4 Heckman: perché in questo studio non serve

Il modello di selezione di Heckman corregge la selezione su variabili **non osservate**, inserendo nell'equazione di esito un termine calcolato dall'equazione di selezione (l'*inverse Mills ratio*). Richiede una *exclusion restriction*: una variabile che influenzi la probabilità di firmare da professionista ma non la qualità della prestazione successiva.

Nella versione precedente della guida lo suggerivo come analisi di robustezza. **Ora lo sconsiglio**, per tre ragioni:

1. con l'esito ordinale su tutta la coorte il problema che Heckman risolve non si presenta;
2. avendo ora la regione, una *exclusion restriction* sarebbe in linea di principio costruibile (per esempio la presenza di una squadra Continental nella regione di appartenenza, o la densità del calendario regionale), ma resterebbe discutibile: è difficile sostenere che quelle variabili influenzino la firma del contratto **senza** influenzare anche lo sviluppo dell'atleta, che è proprio ciò che la exclusion restriction richiede;
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

### Chi-quadro di bontà di adattamento (per il Relative Age Effect)

Confronta una distribuzione osservata per trimestre di nascita con quella attesa. È il test standard per il RAE, ed è tornato utilizzabile ora che disponiamo delle date complete.

**L'errore da non commettere: usare 25/25/25/25 come distribuzione attesa.** Le nascite non sono uniformi nell'arco dell'anno, e la stagionalità varia fra coorti. Il riferimento corretto sono i dati **ISTAT** delle nascite per gli anni effettivi del campione.

È esattamente l'errore commesso da Filipas et al. (2024), che usano l'uniforme come atteso: il picco che osservano nel terzo trimestre (32,0% del campione totale) è verosimilmente stagionalità delle nascite italiane, non un fenomeno sportivo.

```r
# proporzioni attese: da ISTAT, per gli anni di nascita effettivi della coorte
attesi <- c(0.245, 0.256, 0.262, 0.237)   # esempio, da sostituire con i dati reali

# (a) RAE di composizione: chi entra nel ranking U15?
oss_u15 <- table(dfB$birth_quarter[!is.na(dfB$pct_U15y1)])
chisq.test(oss_u15, p = attesi)

# (b) RAE di successo: fra i classificati, chi arriva al professionismo?
oss_pro <- table(dfB$birth_quarter[dfB$PRO == 1])
chisq.test(oss_pro, p = attesi)
```

**Riporta sempre l'effect size** accanto al p-value: con migliaia di osservazioni il chi-quadro diventa significativo per squilibri irrilevanti. La **V di Cramer** è la scelta convenzionale in questa letteratura (Filipas la usa), con soglie: ≤ 0,06 trascurabile, ≤ 0,17 piccolo, < 0,29 medio, ≥ 0,29 grande.

Affianca l'**odds ratio Q1 contro Q4**, che quantifica l'entità in modo più leggibile del chi-quadro ed è direttamente comunicabile: *"un nato in gennaio-marzo ha X volte le probabilità di comparire nel ranking U15 rispetto a un nato in ottobre-dicembre"*.

**Il confronto (a) contro (b) è il risultato interessante**, non i due test presi singolarmente. Se il RAE è forte nella composizione e assente nel successo, la conclusione è quella di Voet et al. (2022): la selezione precoce premia sistematicamente la maturità anagrafica, e lo fa **sbagliando**, perché quel vantaggio non si traduce in maggiori probabilità di arrivare.

### Il RAE come covariata, non solo come oggetto di studio

Oltre al test descrittivo, l'età relativa va inserita nei modelli predittivi per le categorie più giovani (Problema 6):

```r
fit <- logistf(PRO ~ pct_U15y2_10 + rel_age + birth_year_c, data = dfB)
```

Preferisci `rel_age` continua (giorni normalizzati) al trimestre categoriale: usa tutta l'informazione, costa un solo grado di libertà invece di tre, e non impone soglie arbitrarie ai confini dei trimestri. Il trimestre resta utile per la comunicazione e per il confronto con la letteratura, non per la stima.

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

**STEP 1. Verificare da quale anno ciclismo.info riporta le classifiche U15** — ✅ **fatto**

*Cosa*: risalire indietro nel tempo sulle classifiche Esordienti, annotando la prima stagione disponibile.
*Perché*: **determina le coorti utilizzabili e quindi la dimensione dell'intero studio.**

*Esito*: le classifiche Esordienti partono dal **2009**; Allievi, Juniores ed Elite-Under23 dal 2007; tutte le categorie femminili dal 2011. Le coorti dell'analisi principale sono quindi **1996-2000**, cinque e non sette (Sezione 4). Dettagli in `docs/verifica_dati_giovanile.md` §1.

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

*Esito (a), verificato il 27 agosto 2026*: il punteggio minimo in classifica è **1, mai 0**, in tutte le categorie e tutte le stagioni. Il denominatore è quindi «chi ha ottenuto almeno un punto», e ogni conclusione va formulata così. Chi ha corso una stagione intera senza mai entrare a punti è indistinguibile da chi non ha corso affatto. Verificata anche l'assenza di gradini nella copertura: `n_ranked` decresce in modo regolare dal 2007 al 2025, senza cambi di criterio della fonte, con l'unica eccezione del **2020** (−50% in tutte le categorie).

*Esito (b)*: **ancora da fare.** Richiede PCS: serve prendere atleti che sappiamo aver corso all'estero da Juniores e controllare se il ranking italiano ne tiene conto.

---

**STEP 4. Contare gli eventi disponibili, prima di progettare i modelli**

*Cosa*: costruire l'elenco dei professionisti italiani nati 1996-2000 e contare la numerosità di ciascun livello dell'esito ordinale, **usando la finestra fissa dei 26 anni**:

```r
dfB <- dfB |>
  mutate(
    best_pos_26 = best_pcs_pos_entro_26,
    tier = case_when(
      is.na(best_pos_26)   ~ 0L,   # mai professionista
      best_pos_26 <= 100   ~ 3L,
      best_pos_26 <= 500   ~ 2L,
      TRUE                 ~ 1L
    )
  )
table(dfB$tier)
```

Calcola le numerosità anche con soglie alternative (200, 300, 1000) e senza finestra di età, per vedere quanto la scelta sposta i numeri.

*Perché*: determina il budget di predittori per ciascun livello e conferma o smentisce la scelta del top 500 come soglia intermedia. Le attese sono: livello 1 ≈ 55-65, livello 2 ≈ 25-35, livello 3 ≈ 15-20.
*Verifica*: se il livello 3 ha meno di 15 casi, accorpa i livelli 2 e 3. Se il livello 2 ne ha meno di 20, valuta il top 1000 come soglia intermedia al posto del top 500 — resta una fascia PCS ufficiale, quindi ugualmente difendibile.

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

*Cosa*: quanti atleti entrano in ogni categoria, quanti proseguono, e quanti arrivano a ciascun livello dell'esito: professionismo, top 500, top 100.
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

**STEP 13. Costruire e descrivere le variabili di contesto**

*Cosa*: canonicalizzare i nomi delle società (Sezione 5), poi derivare `n_team_changes`, `changed_region`, `region_U15y1`, `team_quality_U15y1`.

*Verifica preliminare*: quante società uniche risultano prima e dopo la canonicalizzazione? Se il numero non cala sensibilmente, la normalizzazione non ha funzionato e `n_team_changes` misurerà i cambi di sponsor.

*Descrittive da produrre*:

```r
# quanto si muovono gli atleti
table(dfB$n_team_changes)
mean(dfB$changed_region)

# distribuzione degli atleti per società: serve a decidere se un modello
# a intercetta casuale sulla società è sostenibile (Sezione 13)
dfB |> count(team_U15y1, sort = TRUE) |> summary()

# densità regionale: quanti classificati per regione e categoria
dfA |> count(region, category)
```

*Perché*: la distribuzione degli atleti per società determina quale strategia di raggruppamento è praticabile; la densità regionale dice quanto la regione pesi sulle opportunità di fare punti, che è un pezzo del Problema 4.

*Attenzione*: `team_quality` va calcolata **solo sulle coorti precedenti** a quella dell'atleta, altrimenti l'esito entra nel predittore.

---

**STEP 14. Mobilità e cambio di regione come esiti intermedi** *(esplorativo)*

*Cosa*: verificare se mobilità e cambio di regione predicono il professionismo, **al netto del percentile**.

```r
logistf(PRO ~ pct_U19y2_10 + n_team_changes + changed_region +
              birth_year_c, data = dfB)
```

*Perché*: sono due ipotesi opposte e distinguibili. Se `n_team_changes` ha coefficiente positivo prevale il reclutamento — cambiare squadra significa essere notati. Se negativo prevale l'instabilità. Nessuno lo ha mai misurato sul ciclismo giovanile italiano.

*Come leggerlo — e questo è il punto delicato*: sono **mediatori**, non controlli (Problema 7). Il coefficiente del percentile in questo modello è un effetto **diretto**, al netto della mediazione, e non va confrontato con quello dei modelli principali né presentato come "l'effetto vero". Tienilo come analisi separata e dichiarala esplicitamente come tale.

*Nel blog post*: se il cambio di regione risultasse un segnale forte, è materiale molto concreto — ma va raccontato con cautela, perché rischia di essere letto come "conviene mandare il figlio in un'altra regione", che non è ciò che il dato dimostra.

---

**STEP 15. Relative Age Effect: composizione e successo** *(Domanda D)*

*Cosa*: due analisi distinte, con la distribuzione attesa presa dai dati **ISTAT** delle nascite per gli anni della coorte (Sezione 17).

**(a) Composizione.** Distribuzione per trimestre di nascita fra i classificati di ciascuna categoria, dall'U15 all'U23. Chi entra nel ranking?

**(b) Successo.** Distribuzione fra chi raggiunge ciascun livello dell'esito: professionista, top 500, top 100. Fra chi è già nel ranking, il trimestre predice l'arrivo?

```r
attesi <- c(0.245, 0.256, 0.262, 0.237)   # da ISTAT, da sostituire

# composizione, categoria per categoria
for (cat in c("U15","U17","U19","U23")) {
  oss <- table(dfA$birth_quarter[dfA$category == cat])
  print(cat); print(chisq.test(oss, p = attesi))
}

# successo
chisq.test(table(dfB$birth_quarter[dfB$PRO == 1]), p = attesi)
```

*Perché*: è il secondo contributo originale dello studio. La fascia U15 italiana non è mai stata analizzata, ed è quella in cui Mostaert trova l'effetto più marcato in Belgio.

*Verifica*: riporta sempre V di Cramer e odds ratio Q1 contro Q4 accanto al p-value. Con migliaia di osservazioni il chi-quadro diventa significativo per squilibri irrilevanti.

*Output atteso*: una curva del RAE per categoria, che secondo la letteratura dovrebbe essere marcata in U15, attenuarsi in U17 e sparire da U19 in poi. Se la trovi, è il grafico più immediato di tutto il blog post — e il più utile, perché indica un errore di selezione correggibile a costo zero.

---

### FASE 3 — Domanda A: diventare professionista

**STEP 16. Modelli univariati per categoria-anno**

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

**STEP 17. Modello multivariato penalizzato**

*Cosa*: elastic net su tutte le categorie insieme, λ scelto per cross-validation (Sezione 9).
*Verifica*: riporta di quanto si riduce il campione (solo chi ha dati completi in tutte le celle). Usa `lambda.1se` per la parsimonia. Niente p-value da questo modello.

---

**STEP 18. Analisi di incremento (Domanda C)**

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

**STEP 19. Metriche pratiche e decision curve**

*Cosa*: alla soglia di Youden, tabella 2×2 completa con sensibilità, specificità, PPV, NPV (Sezione 10.2). Più la decision curve analysis.
*Perché*: è il messaggio che arriva a società e famiglie.
*Output*: la frase-chiave del blog post. Qualcosa come: *"selezionando gli atleti sopra il 90° percentile U19 si intercetta il 74% dei futuri professionisti, ma l'88% dei selezionati non lo diventerà."*

---

**STEP 20. Modello di sopravvivenza a tempo discreto**

*Cosa*: logistica cloglog sulla tabella persona-anno, con spline dell'età, percentile ritardato, errori standard cluster-robusti (Sezione 12).
*Perché*: recupera la coorte 2001 e successive come censurate, aggiunge la dimensione temporale, permette di stimare anche l'età di transizione.
*Verifica*: nessun record dopo l'evento; censoring codificato correttamente.

---

**STEP 21. Traiettorie**

*Cosa*: modello misto sulla Tabella A → estrarre intercetta e pendenza individuali → inserirle nel modello del professionismo (Sezione 13).
*Perché*: risponde a "conta il livello o il miglioramento?", che è la domanda che gli allenatori si fanno più spesso.
*Verifica*: includi sempre intercetta **e** pendenza insieme; considera l'effetto soffitto sul percentile.
*Nota*: con i mancanti codificati onestamente, molti atleti avranno poche stagioni osservate. Lo shrinkage del modello misto gestisce la cosa correttamente, ma riporta la distribuzione del numero di stagioni per atleta.

---

### FASE 4 — Domanda B: la qualità della carriera

**STEP 22. Logistica ordinale su tutta la coorte** *(analisi principale)*

```r
dfB$tier_f <- factor(dfB$tier, levels = 0:3,
                     labels = c("non_pro","pro","top500","top100"), ordered = TRUE)

fit_ord <- MASS::polr(tier_f ~ pct_U19y2_10 + pct_U23y1_10 + birth_year_c,
                      data = dfB, Hess = TRUE)
brant::brant(fit_ord)
```

*Perché*: evita il problema di selezione, usa tutta l'informazione, un solo modello (Sezione 15.1).
*Verifica*: numerosità di ogni livello (Step 4); se il livello più alto ha meno di 15 casi, accorpa top 500 e top 100 e usa tre livelli. Controlla l'assunzione di proportional odds con il Brant test: qui è particolarmente plausibile, perché i livelli sono soglie successive su un'unica variabile sottostante (la miglior posizione raggiunta), che è esattamente la situazione per cui il modello a odds proporzionali è stato pensato.

---

**STEP 23. Modello a stadi successivi** *(approfondimento interpretativo)*

*Cosa*: scomposizione in tre stadi successivi — professionismo, poi top 500 fra i pro, poi top 100 fra i top 500 (Sezione 15.3).
*Verifica*: la seconda parte tollera due predittori, la terza uno solo. Presenta ogni coefficiente sempre come condizionato a "fra chi è arrivato a quel livello".
*Output per il blog post*: la probabilità composta è il numero più comunicabile dell'intero studio. Del tipo: *"un atleta al 90° percentile da U19 ha il X% di probabilità di diventare professionista, e complessivamente il Y% di arrivare almeno al top 500."*

---

### FASE 5 — Validazione e scrittura

**STEP 24. Bootstrap con correzione dell'ottimismo**

*Cosa*: `rms::validate(fit, B = 1000)` (Sezione 16).
*Verifica*: riporta sempre AUC apparente **e** corretta. Se la differenza supera 0,05, il modello è troppo complesso per il campione: semplificalo.

---

**STEP 25. Validazione temporale**

*Cosa*: addestrare sulle coorti 1994-1997, validare sulle 1998-2000.
*Perché*: è la prova più convincente di generalizzabilità, e imita l'uso reale.
*Verifica*: se la performance crolla, non nasconderlo. Significa che i pattern cambiano nel tempo, ed è un risultato.

---

**STEP 26. Analisi di sensibilità**

Almeno queste quattro:

1. **PRO includendo le squadre Continental** — cambia il tasso di evento e forse le conclusioni;
2. **Finestra a 24 e a 26 anni** invece di 25;
3. **Soglia intermedia a 200, 300 e 1000** invece di 500, e **assenza di finestra di età** invece del limite ai 26 anni: sono le due scelte più discrezionali dell'intero disegno, e vanno mostrate entrambe;
4. **Complete case contro imputazione multipla** dei percentili mancanti (`mice`), dichiarando che l'assunzione MAR è qui discutibile.

---

**STEP 27. Confronto con machine learning** *(controllo, non analisi principale)*

*Cosa*: random forest e gradient boosting in nested cross-validation.
*Come leggerlo*: se l'AUC non migliora — esito probabile con poche decine di eventi — è un argomento a favore della parsimonia, e va scritto. Se migliora, guarda i valori SHAP per capire dove, e aggiungi il termine corrispondente al modello parametrico.
*Attenzione*: il modello finale deve restare quello parametrico e interpretabile.

---

**STEP 28. Rileggere la checklist TRIPOD**

TRIPOD è la checklist standard per gli studi di modelli predittivi: 22 voci che coprono fonte dei dati, partecipanti, esito, predittori, dimensione campionaria, gestione dei mancanti, metodi, performance, validazione, limiti.

Non stai scrivendo un articolo scientifico e nessuno te la chiederà. Usala comunque come **lista di controllo privata**: se riesci a rispondere a tutte le voci, il blog post è solido. Se ce ne sono che non sai come riempire, hai trovato un buco. Richiede un'ora e si scarica da equator-network.org.

---

### Priorità se hai tempo limitato

| Priorità | Step |
|---|---|
| **Irrinunciabili** | 1-9, 15, 16, 18, 19, 22, 24 |
| **Molto raccomandati** | 10-13, 20, 25, 26 |
| **Valore aggiunto** | 14, 17, 21, 23, 27, 28 |

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

**7. Il mese di nascita** (300 parole + figura)
Il RAE per categoria. Se l'effetto c'è negli Esordienti e sparisce dopo, è il messaggio più immediatamente azionabile del pezzo: chi seleziona sta premiando la maturità anagrafica, e quel vantaggio non dura.

**8. Chi arriva più in alto** (300 parole)
La Domanda B, con la cautela sui numeri piccoli.

**9. Cosa ne facciamo** (250 parole)
Le implicazioni pratiche, formulate come indicazioni e non come regole.

**10. I limiti** (200 parole)
In chiaro, nel corpo del testo, non in fondo in piccolo.

**11. Appendice metodologica** (in fondo o in pagina separata)
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
9. **Il controllo della maturazione è parziale.** L'età relativa cattura la componente anagrafica dello sviluppo, non quella individuale: due ragazzi nati lo stesso giorno possono avere due anni di differenza biologica. Non disponiamo di misure di maturazione vera.

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

**7-bis. Usare la distribuzione uniforme come attesa nel test del RAE.**
Le nascite non sono uniformi nell'anno. Con 25/25/25/25 come riferimento si finisce per interpretare la stagionalità demografica italiana come un effetto sportivo. Usa i dati ISTAT delle coorti effettive.

**7-ter. Controllare per la società o la regione "per sicurezza".**
Sono variabili misurate dopo il predittore e quasi certamente mediatori: inserirle blocca parte dell'effetto che stai stimando e lo fa apparire più debole di quanto sia (Problema 7). Se le usi, usale come oggetto di studio, non come controllo.

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

**Mediatore** — Variabile che sta fra causa ed effetto sul percorso causale. Da non confondere con un confondente, che li precede entrambi.

**Multicollinearità** — Correlazione elevata fra predittori; instabilizza i coefficienti.

**NPV / PPV** — Valore predittivo negativo / positivo.

**Odds ratio** — Rapporto fra odds; `exp(β)` nella logistica.

**Ottimismo** — Sovrastima della performance dovuta alla valutazione sugli stessi dati usati per la stima.

**Percentile** — Posizione relativa in una distribuzione, 0-100.

**Proportional odds** — Assunzione della logistica ordinale: effetto costante a tutti i punti di taglio.

**V di Cramer** — Effect size per le tabelle di contingenza, compagno del chi-quadro. Soglie: ≤0,06 trascurabile, ≤0,17 piccolo, <0,29 medio, ≥0,29 grande.

**Multiple membership** — Struttura in cui un'unità appartiene a più gruppi nel corso del tempo (un atleta a più società), non gestibile con un modello multilivello classico.

**Over-adjustment** — Errore che consiste nell'inserire come controllo una variabile che sta sul percorso causale fra predittore ed esito, sottostimando così l'effetto.

**RAE (Relative Age Effect)** — Vantaggio sistematico dei nati nei primi mesi dell'anno di selezione, dovuto alla maggiore maturità anagrafica a parità di categoria.

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
