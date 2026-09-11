# Definizioni operative — da congelare

**Data:** 27 agosto 2026
**Stato:** congelato prima di guardare qualunque esito (FASE 0 / STEP 2)

Ogni modifica successiva a questo file va **aggiunta in fondo** con la data, mai sostituita, e riportata come analisi di sensibilità. Se una definizione cambia dopo aver visto i risultati, lo studio ha un problema di p-hacking anche se nessuno lo ha voluto.

---

## Categorie

| Sigla | Denominazione italiana | Slug sorgente | Età | Anni di categoria |
|---|---|---|---|---|
| U15 | Esordienti | `esordienti`, `donne_esordienti` | 13-14 | 1, 2 |
| U17 | Allievi | `allievi`, `donne_allieve` | 15-16 | 1, 2 |
| U19 | Juniores | `juniores`, `donne_juniores` | 17-18 | 1, 2 |
| U23 | Under 23 | `elite_under23` (solo lista `under23`) | 19-22 | 1, 2, 3, 4 |

Gli anni di categoria **non si aggregano mai**.

**Presenze fuori dalla fascia d'età.** Un Under 23 al primo anno può correre alcune gare Juniores, e comparire quindi nel ranking Juniores a 19 anni; esistono i casi speculari in U17 e U23. Sono presenze **legittime**, non errori della fonte, ma quella stagione **non fa parte della popolazione in studio** per quella categoria. Le righe restano in `tab_a` con `cat_year_conf = 'fuori_categoria'` e `cat_year` nullo: non entrano in nessuna cella, né al numeratore né al denominatore. Sono 82 righe su 30.979.

---

## Popolazione e coorti

**Popolazione di riferimento:** atleti che compaiono con **almeno un punto** in almeno una classifica nazionale annuale di ciclismo.info. Non "i tesserati", non "chi ha corso". Verificato: il punteggio minimo in classifica è 1, mai 0.

**L'analisi è sui maschi.** Il femminile va trattato separatamente e in forma descrittiva, per quattro ragioni che non sono di comodo:

- la fonte **non pubblica alcuna classifica Under 23 femminile**, quindi il predittore più informativo secondo la letteratura non esiste e la sequenza dei modelli si ferma all'U19;
- la copertura parte dal **2011**, quindi le coorti con l'U15 primo anno completo e la finestra dell'esito chiusa sono solo **1998-2000**, circa 90 atlete;
- la numerosità complessiva è di un ordine di grandezza inferiore: **1.252 atlete contro 11.105 atleti**, con celle di 20-50 persone contro 150-600;
- su ProCyclingStats cambiano indirizzamento e livelli di squadra (`p=we`, Women's WorldTeam e Women's Continental).

Il **Relative Age Effect** fa eccezione: la data di nascita c'è per il 95,4% delle atlete, e il test confronta distribuzioni invece di stimare modelli, quindi regge la numerosità. Sul femminile è probabilmente l'unica domanda a cui si può rispondere sul serio, e nessuno l'ha mai fatto.

Il progetto deve poter girare sul femminile cambiando un parametro di configurazione. Il livello dati è già pronto: la cella del percentile include il sesso, quindi le atlete sono già confrontate fra loro. Vedi [`da_fare.md`](da_fare.md) §A4bis.

**Coorti diverse per domande diverse.** Non è una comodità: le due domande usano esiti con abbondanza molto diversa, e imporre le stesse coorti a entrambe costringerebbe a sacrificare l'una o l'altra senza guadagno.

| Domanda | Esito | Coorti | Eventi | Perché |
|---|---|---|---|---|
| **A** — diventare professionista | `PRO` | **1996-2000** | 78 | Con 78 eventi la regola dei dieci per variabile consente fino a sette predittori: non c'è ragione di rinunciare all'U15, che è la parte più originale |
| **C** — da che età il risultato informa | `PRO` | **1996-2000** | 78 | La sequenza annidata parte dall'U15, quindi è confinata a queste coorti comunque |
| **B** — qualità della carriera | `tier` | **1992-2000** | 15 in top 100 | Sulle 1996-2000 gli eventi sono 8, sotto la soglia: la Domanda B non sarebbe modellabile affatto |
| Sopravvivenza a tempo discreto | — | tutte, con censura | — | Recupera le coorti 2001+ |

> **I 78 eventi sono la stima congelata qui, prima di guardare i dati.** Dopo la verifica manuale degli abbinamenti con ProCyclingStats il conteggio che si rigenera è **77**, ed è quello che vale: questo file resta com'era perché è un documento datato e riscriverlo a posteriori toglierebbe senso al congelamento. La riconciliazione fra tutti i conteggi dello studio — 77, 74, 102, 140, 121 — con il motivo di ciascuno sta nella sezione «Quanto regge tutto questo» di `output/analisi.md`.

**L'U15 non si perde allargando le coorti.** Le classifiche Esordienti partono dal 2009, quindi l'U15 esiste solo per le coorti 1996+: dichiarare coorti 1992-2000 non aggiunge un solo atleta ai modelli che usano l'U15 (1.281 in entrambi i casi). Allargare le coorti sposta tutto il resto, non l'U15.

Vincoli di copertura, per riferimento:

| Cella | Prima coorte utilizzabile | Motivo |
|---|---|---|
| U15y1 | 1996 | Esordienti dal 2009 |
| U15y2 | 1995 | |
| U17y1 | 1992 | Allievi dal 2007 |
| U19y1 | 1990 | Juniores dal 2007 |

Limite superiore: nato nel 2000 → compie 25 anni nel 2025, ultima stagione conclusa.

---

## Esiti

**PRO** = almeno una stagione con contratto in una squadra di **prima o seconda divisione UCI**, entro l'anno solare in cui l'atleta compie 25 anni.

I nomi delle due divisioni sono cambiati nel tempo e ProCyclingStats usa quello vigente in ciascuna stagione. Verificato sui dati:

| Sigla PCS | Divisione | Stagioni osservate |
|---|---|---|
| `WT` | prima (WorldTeam) | 2011- |
| `PT` | prima (era UCI ProTour) | 2005-2008 |
| `PCT` | seconda (Professional Continental) | 2005-2019 |
| `PRT` | seconda (UCI ProTeam) | 2020- |

`PCT` sparisce **esattamente** nella stagione in cui compare `PRT`: è la stessa divisione rinominata nel 2020, non due cose diverse. Usare solo `('WT','PRT')` escluderebbe l'intera seconda divisione prima del 2020, cioè gran parte delle carriere delle coorti più vecchie — sulle coorti 1992-2000 farebbe passare i professionisti da 146 a 109.

Le squadre **Continental** (`CT`) e i club (`CLUB`) sono **esclusi** dalla definizione principale e tenuti come analisi di sensibilità.

**QUALITÀ** = livello massimo raggiunto nel **ranking annuale di fine stagione** di ProCyclingStats (non il rolling), **entro l'anno in cui l'atleta compie 26 anni**.

**Esito ordinale `tier`:**

| Livello | Definizione | Numerosità attesa (5 coorti) |
|---|---|---|
| 0 | Mai professionista | migliaia |
| 1 | Professionista (WT o PRT), mai top 500 | 40-50 |
| 2 | Almeno una volta in top 500, mai top 100 | 18-25 |
| 3 | **Almeno una volta in top 100** | 10-15 |

Le posizioni sono quelle del ranking **globale**, non della classifica filtrata per nazione. È l'errore più facile da fare: filtrando per nazione, il rango che PCS mostra è quello dentro il filtro.

**Perché top 500 e non top 200.** La banda fra top 200 e top 100 conterrebbe 5-8 atleti, troppo pochi per stabilizzare un livello del modello ordinale. Inoltre il top 500 è una **fascia ufficiale di PCS**, che usa gli scaglioni 10/25/50/100/200/500/1000: non è una soglia scelta da noi.

**Perché la finestra ai 26 anni.** «Almeno una volta» premia chi ha avuto più stagioni a disposizione, e l'esposizione si confonde con l'effetto coorte. La finestra fissa rende le coorti confrontabili.

**Quanto costa, misurato.** Distribuzione dell'età al primo ingresso in top 100 fra gli italiani profilati:

| Età | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30+ |
|---|---|---|---|---|---|---|---|---|---|
| Atleti | 7 | 15 | 19 | 12 | 15 | 9 | 10 | 9 | 13 |

Il picco è a 24 anni, ma **circa il 30% entra in top 100 a 27 anni o dopo**. La finestra ai 26 taglia quella coda: sulle coorti 1992-2000 gli eventi passano da 21 a 15. Un caso reale nel dataset: un atleta nato nel 1997, 186° a 26 anni, chiude 14° a 28. Con la finestra non è un evento; senza, lo è.

**Perché non una finestra più larga.** Non è una scelta di gusto: **una finestra a 28 anni non è osservabile** per le coorti che arrivano al 2000, perché servirebbe la stagione 2028. I 26 anni sono la finestra più ampia interamente osservabile per la coorte 2000. Una finestra a 28 diventa possibile solo fermando le coorti al 1998.

Come sensibilità si riporta anche la versione «mai» con `pro_seasons` come covariata.

### Il conteggio degli eventi — STEP 4, eseguito il 28 agosto 2026

| Coorti | PRO | top 500 | **top 100** |
|---|---|---|---|
| **1996-2000** (analisi principale) | 78 | 39 | **8** |
| 1992-2000 (dall'U17) | 146 | 77 | **15** |

### Gli eventi dentro il sottocampione — STEP 6 eseguito, 28 agosto 2026

Il conteggio qui sopra è sul lato PCS. Quello che conta per i modelli è quanti eventi cadano **dentro il sottocampione** su cui il modello gira, perché i modelli annidati richiedono lo stesso sottocampione per tutti i livelli. Dopo il matching:

| Coorti | Celle richieste | n | Eventi `PRO` | Predittori (10 EPV) |
|---|---|---|---|---|
| 1996-2000 | nessuna | 2.818 | 77 | 7 |
| 1996-2000 | U15y1+y2 | 1.281 | 56 | 5 |
| 1996-2000 | U15+U17 | 587 | 53 | 5 |
| 1996-2000 | U17+U19 | 364 | 58 | 5 |
| **1996-2000** | **U17+U19+U23y1** | **94** | **43** | **4** |
| 1992-2000 | U17+U19+U23y1 | 165 | 77 | 7 |

**La sequenza annidata è stimabile anche sul sottocampione più stretto.** I 94 atleti che compaiono in tutte le celle da U17 a U23y1 contengono 43 professionisti: sono i sopravvissuti, quindi fortemente arricchiti — il 46% di loro è diventato professionista, contro il 2,7% della coorte intera.

**Ma è un campione selezionato, e va detto.** Il modello su quel sottocampione risponde a «*fra chi è ancora classificato al primo anno da Under 23*, il rendimento giovanile predice il professionismo?», che non è la stessa domanda del modello sulla coorte intera. Vanno riportati entrambi.

Nel sottocampione di 94 atleti gli eventi in top 100 sono **6**: visibili, non modellabili. Conferma che la Domanda B va tenuta separata e su coorti più larghe.

**Conseguenza: sulle coorti 1996-2000 la Domanda B non è modellabile** e va ridimensionata a descrittiva. Otto eventi sono sotto la soglia dei dieci fissata dalla guida, e con la regola dei dieci eventi per variabile non reggerebbero nemmeno un predittore.

Sulle coorti **1992-2000** i quindici eventi in top 100 la rendono marginalmente modellabile, con **un solo predittore** più eventualmente l'anno di nascita. È la ragione più forte emersa finora per spostare l'analisi principale sulle coorti dall'U17, e va valutata insieme all'altra — il sottocampione complete case che passa da 94 a 165 atleti.

I professionisti osservati (78 su cinque coorti) sono in linea con l'attesa della guida riportata alle cinque coorti; è la coda di qualità a essere più sottile del previsto.

---

## Predittore principale

`pct_rank_ext` — percentile entro la cella `stagione × categoria × anno di categoria × sesso`, calcolato su un ordinamento lessicografico **punti → vittorie → 2i posti → 3i → 4i → 5i**, con `ties.method = "min"`.

```
pct_rank_ext = 100 * (1 - (rank_pos_ext - 1) / n_ranked)
```

Scala 0-100, dove 100 = primo della cella.

**Perché il criterio esteso.** L'ordinamento per soli punti lascia il 92% degli atleti a pari merito (i punteggi sono piccoli e discreti: mediana 7-8). Il criterio esteso è quello che la fonte stessa usa per compilare le classifiche, dimezza gli ex aequo e triplica la granularità, correlando r = 0,996-0,998 con la versione a soli punti. Dettagli e numeri in [`verifica_dati_giovanile.md`](verifica_dati_giovanile.md), §7.

**Varianti da riportare come sensibilità** (già calcolate, costo zero):

| Variabile | Definizione |
|---|---|
| `pct_rank` | percentile su **soli punti** — versione della guida |
| `z_log_pts` | z-score di `log1p(punti)` entro cella |
| `top10` | 1 se `rank_pos ≤ 10` — codifica di Mostaert, confrontabile con la letteratura |
| `top25pct` | 1 se `pct_rank ≥ 75` |
| `pct_rank_cat` | percentile entro `stagione × categoria` (senza anno di corso) — **unica opzione per l'U23** finché mancano le date di nascita |

---

## Covariate

| Variabile | Definizione | Uso |
|---|---|---|
| `birth_year` | anno di nascita | coorte, sempre nei modelli |
| `birth_quarter` | trimestre di nascita, 1-4 | Domanda D (RAE) |
| `rel_age` | giorni fra la nascita e il 31 dicembre di quell'anno, 0-364 | età relativa entro la coorte; controllo parziale della maturazione biologica nei modelli U15 e U17 |
| `regione` al primo anno osservato | `region_U15y1` | **unica variabile di contesto ammissibile come controllo**, perché misurata prima del predittore |

**Le variabili di contesto sono mediatori, non confondenti.** Se un buon risultato a 14 anni porta a essere ingaggiato da una società migliore, che a sua volta favorisce lo sviluppo, la società sta sul percorso causale: controllarla sottostima l'effetto che si vuole misurare. Società, mobilità e cambio di regione vanno quindi usate **come oggetto di studio** (esiti intermedi, STEP 14) e mai come controlli nei modelli principali.

| Variabile derivata | Definizione | Natura |
|---|---|---|
| `team_U15y1`, `team_last_youth` | società alla prima e all'ultima stagione giovanile | descrittiva |
| `n_team_changes` | numero di cambi di società nelle categorie giovanili | mediatore |
| `changed_region` | 1 se ha cambiato regione durante il percorso giovanile | mediatore |
| `team_quality_U15y1` | tasso di professionisti prodotti dalla società di partenza, calcolato **solo sulle coorti precedenti** a quella dell'atleta | mediatore |

Il vincolo sulle coorti precedenti in `team_quality` non è formale: senza, l'esito dell'atleta entrerebbe nel proprio predittore.

---

## Valori mancanti

```
present   = 1 se l'atleta compare nella cella, 0 altrimenti
pct_rank  = valore se present == 1, NA se present == 0
```

**Non si imputa nulla.** In particolare non si riporta l'ultimo valore disponibile (scelta di Filipas et al.): è un dato inventato che gonfia la continuità delle traiettorie.

Un'assenza dalla cella può voler dire quattro cose — ha smesso, ha corso senza fare punti, non era tesserato, la fonte ha una lacuna — e **con questi dati sono indistinguibili**.

**La seconda non è un caso di scuola: è la più frequente.** Passando di categoria si corre contro avversari di uno o due anni più grandi, ed è normale smettere di andare a punti pur continuando a correre. Quello che le classifiche mostrano è quindi in larga parte un **ricambio fra chi sta ai livelli alti**, non un abbandono. Due misure lo confermano sulle coorti 1996-2000:

- il **30,6%** degli atleti salta almeno una stagione e poi ricompare, il 6,7% dopo due stagioni o più. Se l'assenza fosse abbandono, non ci sarebbero rientri;
- il **50,8%** dei classificati al secondo anno di Allievi non era nella classifica del primo anno — stessa categoria, un anno dopo.

Ne segue una regola di formulazione: si dice sempre «uscito dalla classifica», mai «ha smesso». E i numeri dell'attrito vanno presentati come **mobilità dell'insieme di chi va a punti**, non come tasso di abbandono dello sport. Si riportano in parallelo:

1. **Complete case** sugli atleti presenti nelle celle richieste dal modello;
2. **`present` come predittore a sé stante**, che è l'unica forma in cui la continuità di carriera è misurabile qui.

---

## Anno di nascita

Si usa la prima fonte disponibile fra queste tre, e `birth_year_conf` dichiara quale è stata:

| Ordine | Fonte | `birth_year_conf` |
|---|---|---|
| 1 | colonna della sorgente, quando il database di partenza la esporrà | `sorgente` |
| 2 | **scheda personale dell'atleta** su ciclismo.info (§9 della verifica) | `scheda` |
| 3 | inferenza dall'anno di corso, come ripiego | `certo`, `presunto`, … |

Le prime due sono osservate, la terza è inferita. `birth_date` (AAAA-MM-GG) e `birth_quarter` sono valorizzati solo dalle fonti osservate.

L'inferenza usa `stagione − età_primo_anno − (anno_di_corso − 1)`:

| Valore | Significato | Atleti |
|---|---|---|
| `certo` | da liste disgiunte (Esordienti) o da presenza in lista "primo anno" | 9.207 |
| `presunto` | solo lista generale → assunto 2° anno; errore possibile: anticipa di 1 | 2.525 |
| `conflitto_tier1` / `presunto_conflitto` | stime incompatibili | 39 |
| `ignoto` | compare solo da U23 | 586 |

Il livello `certo` è stato validato: fra i 5.068 atleti con almeno due segnali di livello 1 indipendenti, i segnali concordano nel **99,98%** dei casi.

Le analisi principali si limitano a `certo` + `presunto`; il confronto con i soli `certo` è un'analisi di robustezza.

Le date di nascita da ProCyclingStats, quando disponibili, **sostituiscono** la stima per gli atleti matchati e vanno usate per ricalcolare l'anno di corso U23.

---

## Esclusioni

| Cosa | Perché |
|---|---|
| Stagione **2026** | in corso al momento dell'estrazione (10 agosto 2026). Esclusa alla fonte da `STAGIONE_MAX = 2025` in `01_build_tabelle.py`; l'analisi si replica a stagione chiusa cambiando quella costante e riscaricando i dati |
| Stagione **2020** nell'analisi principale | copertura −50% per COVID; **resta nel dataset** con `flag_stagione = 'covid'`, esclusa dall'analisi principale e riportata in sensibilità |
| Presenze **fuori categoria** | vedi sopra: legittime ma fuori popolazione |
| Classifiche **regionali** e **mensili** | fuori perimetro |
| Classifiche **a squadre** | fuori perimetro |
| Lista Elite-Under23 **promiscua** | contiene Elite di qualunque età; la lista `under23` è completa (aggiunge 4 atleti su 1.481) |
| Atleti con anno di nascita **ignoto** | nelle analisi che richiedono la coorte |
| Femminile | nell'analisi principale; trattato a parte |

---

## Trattamento dei dati e aspetti etici

I dati riguardano **minorenni**. Valgono, indipendentemente dal fatto che siano pubblici:

- **Anonimizzazione all'origine.** `athlete_id` = SHA-256 di `id_atleta` con un salt segreto. Tutte le tabelle di analisi usano solo `athlete_id`.
- **Il salt sta fuori dal repository** (`data/private/salt.txt`, generato al primo avvio). Nel sorgente l'anonimizzazione sarebbe solo apparente: con 37.704 valori possibili di `id_atleta`, la mappa inversa si calcola per forza bruta in pochi secondi.
- **Nel repository entra solo cio' che e' anonimo.** `.gitignore` nega tutto sotto `data/` e autorizza per eccezione; `scripts/00_check_privacy.py` lo verifica prima di ogni commit e cerca nomi di atleti nei file destinati a git.
- **La chiave di corrispondenza** (`data/private/crosswalk_atleti.csv`) contiene nomi e cognomi, serve solo per il matching e la verifica manuale, **non va committata** e va cancellata a lavoro finito.
- **Solo aggregati nella pubblicazione.** Nessun risultato individuale, nessun esempio nominativo, nessuna cella con meno di 5 atleti.
- **Nessuna classifica di "promesse"**, nemmeno anonima. È esattamente l'uso improprio che i risultati dello studio sconsigliano.
- Nel blog post va dichiarato apertamente: fonte, anonimizzazione, aggregazione, e che l'analisi riguarda gruppi e non persone.

---

## Registro delle modifiche

| Data | Modifica | Motivo |
|---|---|---|
| 2026-08-27 | Versione iniziale | — |
| 2026-08-27 | Coorti principali 1994-2000 → **1996-2000** | Verifica STEP 1: le classifiche Esordienti partono dal 2009, non dal 2007. Fatta prima di guardare qualunque esito. |
| 2026-08-27 | Predittore principale: percentile su soli punti → **percentile esteso** | Verifica STEP 3: 92% di ex aequo con i soli punti. Fatta prima di guardare qualunque esito. La versione a soli punti resta come sensibilità. |
| 2026-08-27 | Aggiunta la regola sulle **presenze fuori categoria** | Un U23 primo anno può correre gare Juniores: le 82 righe interessate sono legittime ma fuori popolazione. Prima erano classificate come contraddizioni; la riclassificazione porta le contraddizioni residue da 124 atleti a 39. |
| 2026-08-27 | Risolti a mano i casi di **omonimia** | 3 fusioni, il resto omonimi genuini. Registrate per id in `data/private/manual/fusioni_atleti.csv`. |
| 2026-08-27 | Congelato il trattamento di **2020 e 2026** | 2026 esclusa alla fonte; 2020 tenuta con flag ed esclusa dall'analisi principale. |
| 2026-08-27 | Salt di anonimizzazione spostato **fuori dal sorgente** | Nel codice committato era reversibile per forza bruta. Gli `athlete_id` sono cambiati: nessun risultato pubblicato vi faceva ancora riferimento. |
| 2026-08-27 | **Il Relative Age Effect rientra fra le domande di ricerca** | La guida lo escludeva perché la data di nascita completa era disponibile solo per i professionisti. Le schede personali di ciclismo.info la riportano per circa l'82% di tutti i classificati. *Cifra superata, 11 settembre: era un conteggio fatto prima dello scaricamento completo delle schede. Oggi le schede danno 10 544 date complete, e l'anno di nascita letto da una scheda invece che dedotto per 11 079 classificati su 11 098.* Aggiunte `birth_date` e `birth_quarter`. |
| 2026-08-28 | **Il denominatore esterno: tesserati FCI** | Acquisiti i tesserati per categoria 2018-2025 (documento ufficiale FCI per 2021-2025, due fonti secondarie indipendenti e concordi per 2018-2020) in `riferimenti/tesserati_fci.csv`. In classifica compare il 12-17% dei tesserati, stabile fra le quattro categorie e le otto stagioni. Gli anni mancanti **non si stimano per estrapolazione**: il back-test sbaglia del 27% già a due anni di distanza, e a dieci anni due specificazioni entrambe difendibili danno stime che differiscono di 1,6 volte. Non copre il periodo delle coorti studiate (2009-2023): vale come ordine di grandezza, non come correzione. Il tesseramento è per categoria e non per specialità, quindi la copertura è un limite inferiore. |
| 2026-08-30 | **Cosa dice davvero la fonte sul femminile, dopo lo scaricamento** | Le divisioni femminili non esistono da sempre, e questo vincola le coorti studiabili. **2011-2019**: una categoria sola, che PCS marca `UCI` (con otto squadre-stagione del 2011-2013 marcate `WTW`, probabilmente la classe attuale applicata a ritroso: precisato l'11 settembre) — non esiste una prima divisione da cui distinguere una seconda, quindi l'analogo maschile «prima o seconda divisione» non è definibile. **Dal 2020**: nasce la Women's WorldTeam (`WTW`). **Dal 2025** nei dati compare anche la Women's ProTeam (`PRW`). Ne segue che l'esito PRO femminile sia osservabile **solo dal 2020**, e che le coorti utilizzabili siano quelle che potevano passare professioniste da quell'anno, cioè le nate dal 1998 circa, con finestre d'età parziali per le più vecchie. Nelle rose di prima e seconda divisione 2020-2025 ci sono **51 italiane distinte**. |
| 2026-08-30 | **Come si definirebbe l'esito sul femminile** | `PRO` resta l'analogo esatto: aver corso in una squadra **Women's WorldTeam o UCI Women's ProTeam** entro i venticinque anni. Le soglie di qualità invece **non si trasferiscono**: il gruppo professionistico femminile è molto più piccolo di quello maschile, e un «top 500 mondiale» comprenderebbe quasi tutte le professioniste, cioè non distinguerebbe niente. Al loro posto si propone di usare **la divisione invece della profondità di classifica**: livello alto = aver corso in una squadra di prima divisione (Women's WorldTeam), livello altissimo = top 100 della classifica mondiale femminile, da tenere solo se i casi lo permettono. La ragione è che nel femminile il salto di qualità coincide con il salto di divisione, mentre la coda della classifica mondiale è troppo sottile per reggere una soglia. I valori esatti vanno ricalibrati dopo lo scaricamento, scegliendoli in modo che selezionino **la stessa quota di professioniste** che le soglie maschili selezionano di professionisti. |
| 2026-08-30 | **Come si stimano le gare e i posti** | La fonte non pubblica il calendario, quindi il numero di gare è **stimato dai piazzamenti**: ogni gara assegna cinque posti a punti, dal primo al quinto, per cui la somma dei piazzamenti nei primi cinque di tutti gli atleti di una categoria è il numero di posti messi in palio, e diviso cinque dà il numero di classificazioni di gara. Due limiti dichiarati: la stima assume che ogni gara assegni esattamente cinque posti e che tutti i piazzamenti finiscano in classifica; per l'Under 23 è un **limite inferiore**, perché la lista sorgente contiene anche gli Elite, i cui piazzamenti restano fuori dalla finestra d'età. |
| 2026-09-07 | **Le divisioni professionistiche femminili, e da quando esistono** | Verificato sull'archivio scaricato: fino al 2019 PCS classifica come `UCI`, categoria unica, quasi tutte le squadre femminili — fanno eccezione otto squadre-stagione del 2011-2013 marcate `WTW`, probabilmente con la classe attuale applicata a ritroso, che non toccano le 51 italiane perché quel conteggio parte dal 2020; dal 2020 compaiono le Women's WorldTeam (`WTW`, prima divisione) e solo dal 2025 le Women's ProTeam (`PRW`, seconda). Ne segue che l'esito «professionista» definito come prima o seconda divisione non è costruibile per le coorti femminili precedenti al 2020, e che il confronto con il maschile è possibile solo sulle annate più recenti. |
| 2026-08-30 | **Le classifiche non hanno tutte la stessa struttura** | Negli Esordienti maschili la fonte pubblica due classifiche separate, una per annata: le due annate non si fanno concorrenza. In Allievi, Juniores e Under 23 la classifica è una sola e le annate convivono nelle stesse gare. Il fatto era già in `LISTE_DISGIUNTE` e in `verifica_dati_giovanile.md`, ma non se ne erano tratte le conseguenze: la cella del percentile (`stagione × categoria × anno di categoria`) è una lista vera negli Esordienti e una nostra suddivisione altrove. Ne segue che il primo anno di una categoria a lista unica non ha «meno posti»: ne vince meno, il 26,7% in Allievi contro il 49,7% degli Esordienti. |
| 2026-08-28 | **La scala punti della fonte, per esteso** | Cinque punti alla vittoria e uno al quinto posto. Le gare sono pesate per livello, ma **solo nelle categorie internazionali**: in Juniores e Under 23 una gara nazionale vale il doppio di una regionale e una internazionale il triplo; in Esordienti e Allievi una gara all'estero vale quanto una regionale. Fonte: verifica del gestore del progetto. Corroborato dai dati: il rapporto fra punti e piazzamenti nei primi cinque sale da 2,67 in U15 a 4,17 in U23, con il salto esattamente fra Allievi e Juniores. |
| 2026-08-28 | **STEP 3(b) risolto: il predittore U19 armonizzato non serve** | Le classifiche di ciclismo.info includono già i risultati internazionali in tutte le categorie, con una scala punti più alta (15 punti per la vittoria in una gara internazionale contro 5 in una nazionale). Il timore che l'U19 misurasse una cosa diversa dall'U23 era infondato: lo strumento è lo stesso lungo tutto il percorso. Fonte: verifica del gestore del progetto sulla scala punti della fonte. Resta fuori solo chi corre stabilmente all'estero senza gare in Italia, che non compare in classifica affatto — un problema di copertura, non di armonizzazione. |
| 2026-08-28 | **Cosa significa «essere in classifica»** | La scala punti assegna 5-4-3-2-1 ai primi cinque: un solo punto richiede già un piazzamento nei primi cinque. Verificato sui dati: tutte le 28.041 righe di classifica maschili hanno almeno un top 5. Ogni percentuale del documento ha quindi come denominatore un gruppo già selezionato, non l'insieme dei tesserati. |
| 2026-08-28 | Tutte le scelte spostate in **`config.toml`** | Coorti, soglie, classi di squadra e finestre d'età non sono più cablate nel codice: la scelta metodologica sta in un posto solo. |
| 2026-08-28 | **Coorti diverse per domande diverse**: A e C su 1996-2000, B su 1992-2000 | Gli esiti hanno abbondanza molto diversa (78 eventi `PRO` contro 8 in top 100 sulle stesse coorti). Decisa dopo il conteggio dello STEP 4 e **confermata dal matching**: il sottocampione più stretto della sequenza annidata contiene 43 eventi, quindi la Domanda C è stimabile su 1996-2000 senza rinunciare all'U15. |
| 2026-08-28 | Definizione di **PRO** estesa a `PCT` e `PT` | Sono i nomi storici di prima e seconda divisione: usare solo `WT`/`PRT` escludeva l'intera seconda divisione prima del 2020. Sulle coorti 1992-2000 i professionisti passano da 109 a 146. |
| 2026-08-28 | Recepita la **v5** della guida: soglia di qualità **top 500** invece di top 200, esito misurato **entro i 26 anni**, età relativa fra le covariate, variabili di contesto come mediatori | Le numerosità attese sono ridotte di un terzo rispetto alla guida, perché le coorti sono cinque e non sette. |
| 2026-08-28 | Guida v5 allineata ai dati | Coorti 1994-2000 → 1996-2000 in Sezione 4, STEP 1 e STEP 4; registrati gli esiti verificati di STEP 1 e STEP 3(a); aggiunta la sezione sui pari punti in Sezione 5. |
| 2026-08-27 | Anno di nascita: **osservato prima che inferito** | Precedenza sorgente → scheda → inferenza. Il confronto ha mostrato che l'inferenza sbaglia nel 4% dei casi `presunto` e nel 100% dei `presunto_conflitto`. |
