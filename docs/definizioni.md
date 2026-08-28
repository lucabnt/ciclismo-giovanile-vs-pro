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

**Analisi principale ristretta al maschile.** Il femminile ha copertura dal 2011 e numerosità 5-8 volte inferiore; va trattato separatamente e in forma descrittiva.

| Analisi | Coorti di nascita | N coorti | Vincolo |
|---|---|---|---|
| **Principale (dall'U15y1)** | **1996-2000** | 5 | Esordienti coperti dal 2009 |
| Dall'U15y2 | 1995-2000 | 6 | |
| Dall'U17y1 | 1992-2000 | 9 | Allievi coperti dal 2007 |
| Dall'U19y1 | 1990-2000 | 11 | Juniores coperti dal 2007 |
| Sopravvivenza a tempo discreto | tutte, con censura | — | recupera 2001+ |

Limite superiore: nato nel 2000 → compie 25 anni nel 2025, ultima stagione conclusa.

---

## Esiti

**PRO** = almeno una stagione con contratto in squadra **UCI WorldTeam o UCI ProTeam**, entro l'anno solare in cui l'atleta compie 25 anni.

Le squadre Continental sono **escluse** dalla definizione principale e tenute come analisi di sensibilità.

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

**Perché la finestra ai 26 anni.** «Almeno una volta» premia chi ha avuto più stagioni a disposizione, e l'esposizione si confonde con l'effetto coorte. La finestra fissa rende le coorti confrontabili. Costo dichiarato: taglia fuori le maturazioni tardive, e sappiamo da Kholkine et al. che il picco arriva verso i 27 anni. Come sensibilità si riporta anche la versione «mai» con `pro_seasons` come covariata.

Le numerosità attese sono quelle della guida ridotte di circa un terzo, perché le coorti sono cinque e non sette. **Vanno ricontate allo STEP 4 prima di progettare qualunque modello**: sotto i 10 eventi in top 100 la Domanda B va ridimensionata a descrittiva.

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

Un'assenza dalla cella può voler dire quattro cose — ha smesso, ha corso senza fare punti, non era tesserato, la fonte ha una lacuna — e **con questi dati sono indistinguibili**. Si riportano in parallelo:

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
| 2026-08-27 | **Il Relative Age Effect rientra fra le domande di ricerca** | La guida lo escludeva perché la data di nascita completa era disponibile solo per i professionisti. Le schede personali di ciclismo.info la riportano per circa l'82% di tutti i classificati. Aggiunte `birth_date` e `birth_quarter`. |
| 2026-08-28 | Recepita la **v5** della guida: soglia di qualità **top 500** invece di top 200, esito misurato **entro i 26 anni**, età relativa fra le covariate, variabili di contesto come mediatori | Le numerosità attese sono ridotte di un terzo rispetto alla guida, perché le coorti sono cinque e non sette. |
| 2026-08-28 | Guida v5 allineata ai dati | Coorti 1994-2000 → 1996-2000 in Sezione 4, STEP 1 e STEP 4; registrati gli esiti verificati di STEP 1 e STEP 3(a); aggiunta la sezione sui pari punti in Sezione 5. |
| 2026-08-27 | Anno di nascita: **osservato prima che inferito** | Precedenza sorgente → scheda → inferenza. Il confronto ha mostrato che l'inferenza sbaglia nel 4% dei casi `presunto` e nel 100% dei `presunto_conflitto`. |
