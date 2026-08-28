# Cose da fare

Elenco di lavoro. Ogni voce dice **cosa**, **perché** e **come verificare di averla chiusa**.

---

## A. Rendere il progetto eseguibile senza assistenza

L'obiettivo è che chiunque, con il repository e i due database di partenza, possa rieseguire l'intera analisi leggendo solo la documentazione. Oggi gli script funzionano ma incorporano scelte nel codice.

### A1. Togliere i valori cablati e portarli in un file di configurazione

**Cosa.** Un unico `config.toml` (o `config.yaml`) alla radice, letto da tutti gli script. Cablati oggi:

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

**Perché.** Gli intervalli di stagione vanno spostati ogni anno, e `TOP_N` dipende dalla soglia di qualità scelta in `definizioni.md`: se un giorno la soglia cambia, oggi bisogna sapere che c'è una costante da toccare in un file Python. Con la configurazione esterna la scelta metodologica sta in un posto solo e si vede.

**Verifica.** Cambiare `stagione_max` da 2025 a 2026 nel file di configurazione e rieseguire tutta la catena senza aprire un solo `.py`.

### A2. Un comando unico che esegue la catena

**Cosa.** Un `Makefile` o `run.py` che esegue in ordine: `00_check_privacy` → `01_build_tabelle` → `02_casi_da_verificare`, saltando i passi già fatti e dicendo quali richiedono decisioni manuali o download.

**Verifica.** Da repository appena clonato e con i database al loro posto, un solo comando produce `data/analisi/analisi.db`.

### A3. Dipendenze dichiarate

**Cosa.** Un `requirements.txt` con `procyclingstats`, `cloudscraper`, `certifi`. Oggi la pipeline principale usa solo la libreria standard, ma gli script 03 e 04 no, e `certifi` è servito per Eurostat.

### A4. Documentare la provenienza dei dati di partenza

**Cosa.** Il database `data/giovanile/ciclismo.db` non nasce qui: viene da **<https://github.com/lucabnt/risultati-ciclismo-giovanile>**, che contiene lo scraper di ciclismo.info e il database prodotto. Repository privato per ora, potenzialmente pubblico in futuro.

Va scritto nel README e in `docs/verifica_dati_giovanile.md`, con la versione dello schema attesa (`schema_meta.schema_version = 2.1`) e la data di estrazione, perché i numeri riportati nella verifica valgono per quella estrazione e non per un'altra.

**Perché.** Senza, chi legge il repository non sa da dove venga il file più importante, e non può rigenerarlo.

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

### B1. `elite_seasons` misura i punti, non la carriera

**Il problema.** `tab_b.elite_seasons` e `tab_b.racing_after_u23` derivano dalla presenza nella classifica Elite di ciclismo.info. Ma quella classifica include **solo chi ha ottenuto almeno un punto**: un atleta che ha continuato a correre senza mai andare a punti è indistinguibile da uno che ha smesso.

È la stessa limitazione del denominatore che vale per tutto lo studio, ma qui è più insidiosa, perché il nome della variabile suggerisce «ha continuato a correre» mentre il significato è «ha continuato a correre **e a fare punti**».

**Cosa fare.**
1. Rinominare in `elite_seasons_a_punti` e `punti_dopo_u23`, così il nome dice cosa misura.
2. Aggiornare il commento nello schema e la voce in `definizioni.md`.
3. Nel blog post, formulare sempre come «risultava ancora a punti nella classifica Elite», mai come «correva ancora».

**Conseguenza analitica.** La variabile è un limite inferiore della continuità agonistica. Va bene come indicatore di *livello* raggiunto dopo l'età giovanile, non come misura di abbandono. Per l'abbandono vero non abbiamo una fonte, e va dichiarato.

### B2. Le 218 presenze fuori categoria: 87 casi indecidibili

Di 218 atleti con una presenza fuori dalla fascia d'età, 131 hanno altre stagioni tutte coerenti con la data di nascita — quindi la data è corroborata e la collocazione in classifica è errata, tipicamente nell'ultima stagione. Gli **87 che hanno solo quella riga** restano indecidibili: potrebbe essere sbagliata la data o la categoria. Sono già marcati ed esclusi dalle celle; va solo dichiarato nei limiti.

---

## C. Analisi ancora da impostare

### C1. Relative Age Effect (STEP 15) — la distribuzione attesa c'è

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

### C2. `team_quality_first`

La colonna esiste in `tab_b` ma è vuota: richiede il tasso di professionisti prodotti da ciascuna società, calcolabile solo dopo PCS e **solo sulle coorti precedenti** a quella dell'atleta. Senza quel vincolo l'esito entrerebbe nel proprio predittore.

### C3. `pct_U19_arm` e STEP 3(b)

Il predittore U19 armonizzato e la verifica se il ranking Juniores incorpori i risultati internazionali. Entrambi richiedono PCS.

### C4. La decisione sul sottocampione dei modelli annidati

Rimandata. Il sottocampione complete case per la sequenza U17 → U19 → U23y1 è di 94 atleti sulle coorti 1996-2000 e 165 su 1992-2000. Le tre opzioni — fermarsi all'U19, spostarsi sulle coorti dall'U17, appoggiarsi alla sopravvivenza a tempo discreto — vanno valutate dopo il conteggio degli eventi dello STEP 4.
