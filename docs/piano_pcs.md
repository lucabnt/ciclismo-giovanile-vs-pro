# Acquisizione dati ProCyclingStats — analisi delle opzioni e piano

**Data:** 27 agosto 2026
**Copre:** FASE 0 / STEP 4 e FASE 1 / STEP 6 del piano operativo

---

## 1. La domanda giusta non è "come scarico PCS"

L'istinto è: abbiamo 12.357 atleti giovanili, cerchiamoli uno per uno su PCS. **È l'approccio sbagliato**, per tre motivi:

- costa ~12.800 ricerche più altrettante pagine profilo, con una percentuale di match molto bassa (la grande maggioranza di quei ragazzi non ha mai corso una gara registrata su PCS);
- la ricerca per nome su PCS è fuzzy e restituisce candidati da tutto il mondo: ogni «Marco Rossi» va disambiguato a mano;
- soprattutto, **non serve**. L'esito che ci interessa è "questo ragazzo è diventato professionista". Chi non è mai stato professionista contribuisce con `PRO = 0`, che è già il default.

L'impostazione corretta è **invertire la direzione del match**: costruire prima l'insieme — piccolo e completamente enumerabile — degli atleti *rilevanti* su PCS, e proiettarlo sui 12.357. Il match diventa qualche centinaio di confronti invece di dodicimila, e la verifica manuale al 100% dei candidati professionisti che la guida richiede allo STEP 6 diventa una giornata di lavoro invece di un progetto a sé.

---

## 2. Cosa serve davvero da PCS

| Dato | Serve per | Dove sta su PCS |
|---|---|---|
| Storia squadre con **classe** (WT / PRT / CT) per stagione | esito `PRO` | rosa squadra per stagione, oppure profilo atleta |
| **Posizione nel ranking annuale** di fine stagione | esito `tier` (top 100 / top 200) | classifica annuale globale |
| **Data di nascita completa** | chiave di match, anno di corso U23, RAE | profilo atleta |
| Presenza / punti da **U19 e U23** | predittore internazionale (Sezione 3 della guida) | classifica annuale filtrata per nazione; profilo atleta |
| Nazionalità | filtro sugli italiani | ovunque |

Nota sul RAE: la guida lo esclude perché la data di nascita completa c'è solo per i professionisti. Resta vero per la coorte intera, ma **fra i matchati** la data completa ci sarà — abbastanza per la parte del confronto Voet (RAE presente fra chi non arriva, assente fra chi arriva) che riguarda chi arriva.

---

## 3. Lo strumento

### Raccomandazione: `procyclingstats` su PyPI

```bash
pip install procyclingstats
```

[PyPI](https://pypi.org/project/procyclingstats/) · [docs](https://procyclingstats.readthedocs.io/) · [sorgente](https://github.com/themm1/procyclingstats) · ultimo rilascio marzo 2026, quindi mantenuto.

È un parser HTML, non una API: PCS non ne ha una pubblica. Espone classi `Rider`, `Team`, `Ranking`, `RiderResults`, `Race`, `RaceStartlist`, `Stage`. Quelle che servono a noi:

| Classe | URL | Cosa restituisce |
|---|---|---|
| `Team("team/bora-hansgrohe-2022")` | rosa stagionale | `riders()` → nome, `rider_url`, nazionalità, età; `status()` → classe squadra |
| `Rider("rider/tadej-pogacar")` | profilo | `birthdate()`, `nationality()`, `teams_history()` (stagione + **classe**), `points_per_season_history()` (stagione, punti, **rank**) |
| `Ranking("rankings/me/season-individual")` | classifica | `individual_ranking()` → rank, nome, `rider_url`, nazionalità, punti; filtri via query string `date`, `nation`, `offset`, `teamlevel` |

`Rider.teams_history()` è il metodo chiave: dà in **una sola richiesta** tutte le stagioni con la classe della squadra, che è esattamente la definizione operativa di `PRO`.

### Le alternative, e perché no

| Opzione | Verdetto |
|---|---|
| `pcs-scraper` (PyPI) | Stessa idea, meno mantenuto e meno documentato. Ripiego se `procyclingstats` si rompe. |
| Scraper proprio con `requests` + `selectolax` | Ha senso solo per le pagine che la libreria non copre (l'elenco squadre per stagione). Per il resto è riscrivere codice già scritto. |
| Attore Apify «Procyclingstats.com Scraper» | A consumo, e comunque uno scraper. Nessun vantaggio qui. |
| Dump PCS su Kaggle/GitHub | Tentante ma da evitare: fermi a stagioni vecchie, provenienza non verificabile, nessun controllo su come sono stati costruiti. Per uno studio che verrà pubblicato, la catena di provenienza deve essere tua. |
| FirstCycling | **Utile, ma come controllo incrociato**, non come fonte primaria: ottimo per validare a mano i casi di omonimia dubbia. |

### Due avvertenze operative

**La libreria non ha throttling.** Guardando il sorgente di `Scraper._make_request`, non c'è alcuna pausa fra le richieste: solo un retry con backoff esponenziale sui fallimenti. **La pausa va messa tu**, e va messa una cache su disco: durante lo sviluppo del parsing rifarai le stesse richieste decine di volte.

**PCS sta dietro Cloudflare** e la libreria, se trova `cloudscraper` installato, lo usa per superare il challenge. Il `robots.txt` di PCS consente `User-agent: *` su tutto il sito (i divieti riguardano i crawler di training dei modelli), quindi lo scraping per un'analisi statistica rientra in quanto consentito. Resta buona pratica: 2-3 secondi fra le richieste, uno user agent che ti identifica con un contatto, e nessuna concorrenza. Il volume totale (§5) è dell'ordine di 1.500-2.500 pagine: a quel ritmo è un paio d'ore, e non pesa sul sito.

---

## 4. Il piano di raccolta, in quattro strati

Ogni strato è indipendente e riutilizzabile; si esegue in ordine perché ognuno restringe il successivo.

### Strato A — L'universo dei professionisti (definisce `PRO`)

Per ogni stagione **2011-2026** e ogni livello **WorldTeam** e **ProTeam**:

1. elenco squadre della stagione → `https://www.procyclingstats.com/teams.php?year=YYYY&filter=Filter&s=worldtour` (e `s=proteams`);
2. per ogni squadra, `Team("team/<slug>-YYYY").riders()` → rosa completa con nazionalità.

Questo produce **l'elenco esaustivo di chi è stato WT o PRT in ogni stagione**, che è la definizione operativa di `PRO`. Filtrando `nationality == "IT"` si ottiene l'insieme dei candidati da matchare: attese **250-450 persone** su 16 stagioni.

Perché per squadra e non per atleta: una rosa costa una richiesta e restituisce 25-30 atleti; il profilo atleta ne costa una e ne restituisce uno. Trenta volte più efficiente, e soprattutto **esaustivo** — non dipende dall'aver già indovinato chi cercare.

2011 come punto di partenza: il primo nato del 1993 (coorte più vecchia utile) poteva firmare da neoprofessionista nel 2013, ma un anticipo di due stagioni copre i casi precoci senza costare quasi nulla.

### Strato B — Le classifiche annuali globali (definiscono `tier`)

Per ogni stagione 2011-2026, la **top 200 del ranking annuale di fine stagione**, non filtrato per nazione:

```
rankings.php?date=YYYY-12-31&nation=&page=smallerorequal&offset=0&filter=Filter&p=me&s=season-individual
```

Due pagine per stagione (100 righe l'una), 32 richieste in tutto. Da qui escono direttamente le soglie top-100 e top-200 del `tier`.

> **Attenzione**: la posizione va letta dalla classifica **globale**. Se filtri per nazione, il rango che PCS mostra è quello dentro il filtro, e «top 100 italiano» non è «top 100». È l'errore più facile da fare in tutto lo studio.

> **Da verificare alla prima richiesta**: fino a quale stagione indietro PCS espone la classifica annuale di fine anno, e se `date=YYYY-12-31` è il valore giusto per ogni anno o va letto da `dates_select()`. `Ranking(...).dates_select()` restituisce l'elenco delle date disponibili: usare quello invece di costruire la data a mano.

### Strato C — Gli italiani a punti (predittore internazionale U19/U23)

Per ogni stagione **2007-2025**, la classifica annuale filtrata `nation=it`, tutte le pagine. Restituisce ogni italiano che abbia ottenuto punti PCS quell'anno — comprese le stagioni da U19 e U23.

È il materiale dello STEP 12 (confronto ranking nazionale vs presenza internazionale), che la guida indica come piccolo contributo originale dello studio. Attesi 400-900 nomi per stagione, 4-9 pagine, ~130 richieste.

Limite da dichiarare: chi ha corso senza mai fare punti PCS non compare. `pcs_present = 0` significa "senza punti PCS", non "non ha corso".

### Strato D — I profili dei candidati

Solo per gli atleti emersi da A e C (unione, italiani, nati 1988-2005): `Rider("rider/<slug>")`.

Restituisce in una richiesta `birthdate()`, `nationality()`, `teams_history()` (stagione + classe, tutte le stagioni) e `points_per_season_history()` (stagione, punti, rank). Copre insieme la conferma di `PRO`, la data di nascita per il match, e il ranking per stagione.

Attese **1.000-2.000 richieste**. È lo strato più pesante, ed è per questo che va fatto per ultimo, sull'insieme già ristretto.

---

## 5. Costo complessivo

| Strato | Richieste |
|---|---|
| A — elenchi squadre + rose WT/PRT 2011-2026 | ~650 |
| B — top 200 globale 2011-2026 | ~32 |
| C — italiani a punti 2007-2025 | ~130 |
| D — profili dei candidati | 1.000-2.000 |
| **Totale** | **~1.800-2.800** |

A 2,5 secondi di pausa: **1,5-2 ore**, una volta sola. Con la cache su disco, i rifacimenti del parsing costano zero.

---

## 6. Schema di destinazione

Il lato PCS va in un database separato — `data/pcs/pcs.db` — non dentro `analisi.db`, che viene ricostruito da zero a ogni esecuzione della pipeline giovanile. Il ponte fra i due è `analisi.db → match_pcs`, già creato.

```sql
CREATE TABLE pcs_rider (
    pcs_id        TEXT PRIMARY KEY,   -- slug, es. 'filippo-baroncini'
    nome          TEXT,
    cognome       TEXT,
    chiave_match  TEXT,               -- normalizzata, vedi lib_giovanile.chiave_match
    nazionalita   TEXT,
    birthdate     TEXT,               -- YYYY-MM-DD
    birth_year    INTEGER,
    scaricato_il  TIMESTAMP
);

CREATE TABLE pcs_team_season (       -- strato A
    pcs_id       TEXT NOT NULL,
    season       INTEGER NOT NULL,
    team_slug    TEXT,
    team_name    TEXT,
    team_class   TEXT,                -- WT | PRT | CT | ...
    since        TEXT, until TEXT,
    PRIMARY KEY (pcs_id, season, team_slug)
);

CREATE TABLE pcs_ranking_season (    -- strati B e C
    season       INTEGER NOT NULL,
    pcs_id       TEXT NOT NULL,
    rank_global  INTEGER,             -- posizione nella classifica NON filtrata
    points       REAL,
    nazionalita  TEXT,
    fonte        TEXT,                -- 'globale_top200' | 'nazione_it'
    PRIMARY KEY (season, pcs_id, fonte)
);

CREATE TABLE pcs_log (               -- tracciabilita' dello scraping
    url TEXT, esito TEXT, http_status INTEGER,
    n_righe INTEGER, dettaglio TEXT, eseguito_il TIMESTAMP
);
```

`pcs_log` non è burocrazia: sul lato giovanile è stato proprio il log di scraping a permettere di dimostrare che nessuna classifica nazionale maschile mancava.

---

## 7. La tabella di matching

Già creata in `analisi.db` come `match_pcs`, una riga per atleta giovanile:

```sql
CREATE TABLE match_pcs (
    athlete_id     TEXT PRIMARY KEY REFERENCES anagrafica(athlete_id),
    pcs_id         TEXT,
    metodo         TEXT,     -- esatto | fuzzy | manuale | assente
    score          REAL,     -- similarita' 0-1 per il fuzzy
    birth_year_pcs INTEGER,  -- verifica incrociata con la stima giovanile
    ambiguo        INTEGER DEFAULT 0,
    candidati      TEXT,     -- JSON dei candidati scartati, per l'audit
    verificato     INTEGER DEFAULT 0,
    nota           TEXT
);
```

La chiave di match è `chiave_match` (in `data/private/crosswalk_atleti.csv` e in `pcs_rider`): maiuscolo, accenti rimossi, apostrofi e trattini normalizzati, **token ordinati alfabeticamente**. L'ordinamento dei token serve perché PCS scrive `Cognome Nome` e ciclismo.info a volte l'inverso, e perché i doppi nomi compaiono in ordine diverso nelle due fonti.

### Procedura in quattro passaggi

1. **Match esatto** su `chiave_match` + anno di nascita. Con `birth_year_conf = 'presunto'` accettare anche uno scarto di ±1 anno, marcando `nota`: la stima giovanile può anticipare di uno (vedi `verifica_dati_giovanile.md` §4).
2. **Match esatto sul solo nome**, quando l'anno di nascita giovanile è ignoto o in conflitto. Se produce un solo candidato, accettarlo con `ambiguo = 0`; se più d'uno, `ambiguo = 1` e in coda alla verifica manuale.
3. **Fuzzy** (Levenshtein normalizzata) sui residui, **soglia conservativa ≥ 0,90**, vincolato allo stesso anno di nascita ±1. Tutti i fuzzy vanno in verifica manuale: sono qualche decina.
4. **Verifica manuale al 100% dei candidati professionisti.** Sono un centinaio e non sono negoziabili — con eventi rari, un falso negativo pesa quanto dieci falsi positivi. Disambiguare con società giovanile e regione (che ci sono per il 98,3% degli atleti) e, se serve, con FirstCycling. Segnare `verificato = 1` e la motivazione in `nota`.

### Due cose da fare prima di iniziare

- ~~Risolvere i candidati frammento~~ — **fatto** (`verifica_dati_giovanile.md` §5): tre fusioni applicate, il resto sono omonimi genuini. La lista si rigenera con `scripts/02_casi_da_verificare.py` se emergono nuovi casi dopo il matching.
- **Sostituire la stima dell'anno di nascita con la data PCS** per gli atleti matchati, e ricalcolare l'anno di corso U23 e i percentili delle celle U23.

### Cosa riportare nel blog post

Non è materiale interno: la guida lo chiede esplicitamente allo STEP 6.

- tasso di match complessivo e per coorte;
- confronto della distribuzione dei percentili fra matchati e non matchati (se i non matchati sono sistematicamente più deboli va bene, se non lo sono c'è un problema);
- numero di omonimie risolte a mano e con quale criterio;
- numero di casi in cui l'anno di nascita PCS smentisce la stima giovanile — è la validazione esterna, gratuita, della ricostruzione descritta in `verifica_dati_giovanile.md` §4.

---

## 8. Il primo output atteso: STEP 4

Appena chiusi gli strati A e B, prima di scrivere una riga di modello, si conta:

| | Coorti 1996-2000 | Coorti 1992-2000 |
|---|---|---|
| Professionisti (WT o PRT entro i 25 anni) | ? | ? |
| Di cui almeno una volta in top 200 | ? | ? |
| Di cui almeno una volta in **top 100** | ? | ? |

Con meno di 15 eventi in top 100, la Domanda B non è modellabile e va ridimensionata a descrittiva. Con cinque coorti invece di sette, questo esito è concretamente possibile: meglio saperlo prima di costruirci sopra.

Il numero di eventi decide anche il numero massimo di predittori (regola dei 10 eventi per variabile). È il vincolo che governa tutta la FASE 3.
