# Guida metodologica completa allo studio

## Ranking giovanili FCI e transizione al professionismo: predire l'accesso e la qualità della carriera PRO

*Documento di lavoro — impostazione, metodi statistici spiegati da zero, piano operativo*

---

# Indice

**PARTE I — Impostazione dello studio**
1. Le domande di ricerca
2. Perché non basta una regressione semplice: i cinque problemi
3. Disegno dello studio e definizioni operative
4. Costruzione del dataset

**PARTE II — I metodi statistici spiegati**
5. Ripasso: dalla regressione lineare a quella logistica
6. Come si legge un odds ratio (senza sbagliare)
7. Il problema degli eventi rari e la correzione di Firth
8. Predittori correlati: multicollinearità e regressione penalizzata
9. Misurare quanto un modello predice: AUC, sensibilità, PPV, calibrazione
10. Modelli annidati: "quanto aggiunge questa informazione?"
11. Analisi di sopravvivenza a tempo discreto
12. Modelli misti e traiettorie individuali
13. Regressione logistica ordinale
14. Il problema della selezione: modelli hurdle e Heckman
15. Modelli per esiti continui asimmetrici
16. Validazione: cross-validation, bootstrap, validazione temporale
17. Test statistici di supporto

**PARTE III — Esecuzione**
18. Piano operativo passo-passo con codice
19. Struttura del manoscritto e checklist TRIPOD
20. Trappole da evitare
21. Glossario

---

# PARTE I — IMPOSTAZIONE DELLO STUDIO

## 1. Le domande di ricerca

Hai due domande, che è importante tenere distinte perché richiedono metodi diversi:

**Domanda A — Accesso.** I punteggi ottenuti nelle categorie giovanili (Esordienti, Allievi, Juniores, Under 23) predicono la probabilità di diventare professionista?

**Domanda B — Qualità.** Fra chi è diventato professionista, i punteggi giovanili predicono il livello raggiunto (misurato dai punti ProCyclingStats)?

A queste ne aggiungo una terza, che è quella con più valore scientifico e pratico e che la letteratura esistente non ha risolto:

**Domanda C — Età di informatività.** A partire da quale età il risultato agonistico comincia a contenere informazione *aggiuntiva* rispetto a quella già disponibile? Cioè: sapere come è andato un ragazzo a 14 anni cambia qualcosa, una volta che so come è andato a 18?

La domanda C è quella che il tuo dataset può affrontare meglio di Gallo et al. (2022), perché tu hai gli **Esordienti** (13-14 anni) che loro non avevano — partivano dall'U17 (Allievi).

### Perché la domanda C è la più importante

Se il risultato è "a 13-14 anni il ranking non predice nulla", questo ha implicazioni immediate sulla selezione precoce, sui criteri di reclutamento delle società e sui progetti federali. È un risultato **negativo ma utile**, e va progettato per essere quantificato bene, non liquidato come "non significativo". Torneremo su questo punto più volte.

---

## 2. Perché non basta una regressione semplice: i cinque problemi

Hai esperienza con regressioni semplici. L'istinto naturale sarebbe:

```
punti_pro ~ punti_junior
```

oppure

```
pro (sì/no) ~ punti_junior
```

Entrambe queste analisi, fatte così, produrrebbero risultati **sbagliati o non interpretabili**. Ecco perché, uno per uno.

### Problema 1 — L'esito è binario, non continuo

"Diventare pro" è 0 o 1. La regressione lineare classica (OLS, minimi quadrati) assume che l'esito sia continuo e che i residui siano distribuiti normalmente. Applicata a un esito 0/1 produce:
- probabilità predette negative o superiori a 1 (assurde);
- residui strutturalmente non normali;
- errori standard sbagliati.

**Soluzione**: regressione logistica (Sezione 5).

### Problema 2 — L'esito è raro

Nel campione di Gallo, 43 professionisti su 1345 atleti = 3,2%. Il tuo sarà simile, forse più basso se includi gli Esordienti (dove la platea è molto più larga).

Con eventi rari succedono due cose spiacevoli:
- **La stima di massima verosimiglianza è distorta**: i coefficienti della logistica vengono sistematicamente sovrastimati in valore assoluto. Non è un problema di rumore, è un bias sistematico che non sparisce aumentando il campione se gli eventi restano pochi.
- **Separazione (quasi) completa**: se, per esempio, *tutti* i professionisti erano nel top 5% da Junior, il modello cerca di stimare un coefficiente infinito e il software o non converge o restituisce errori standard enormi.

**Soluzione**: regressione logistica penalizzata di Firth (Sezione 7).

### Problema 3 — I dati sono censurati a destra

Un atleta nato nel 2003 nel 2026 ha 23 anni. Non ha ancora avuto il tempo di firmare un contratto professionistico. Se lo classifichi come NON-PRO, stai dicendo una cosa falsa: non è "non diventato pro", è **"non ancora osservabile"**.

Questo si chiama **censoring a destra** (right censoring): sai che l'evento non è ancora accaduto al momento dell'osservazione, ma non sai se accadrà dopo.

Ignorarlo produce due distorsioni: sottostima del tasso di professionismo, e — peggio — distorsione dei coefficienti se le coorti recenti hanno caratteristiche diverse (per esempio punteggi normalizzati diversamente, o un sistema di ranking cambiato).

**Soluzioni**: (a) restringere il campione alle coorti con follow-up completo; (b) usare l'analisi di sopravvivenza, che gestisce il censoring in modo nativo (Sezione 11). Nel piano operativo useremo entrambe.

### Problema 4 — I punteggi non sono comparabili tra anni

I punti del ranking FCI dipendono da: regolamento di attribuzione punti (cambiato più volte dal 2008), numero di gare in calendario, numero di atleti tesserati, tipologia di gare. Cento punti nel 2009 non sono cento punti nel 2019.

Se metti i punti grezzi come predittore, il modello confonde "essere stato bravo" con "aver corso in un anno in cui si assegnavano più punti".

**Soluzione**: normalizzare **dentro** ogni combinazione categoria × anno di categoria × stagione, trasformando i punti in **percentile** (Sezione 4).

### Problema 5 — La selezione (il problema più insidioso)

I punti PCS li osservi **solo per chi è diventato professionista**. Ma diventare professionista non è casuale: dipende proprio dai risultati giovanili che vuoi usare come predittore.

Questo si chiama **selezione sul predittore** e produce due effetti:

- **Restrizione del range**: fra i pro, la varianza dei punteggi giovanili è molto più piccola che nella popolazione generale. Le correlazioni calcolate su un range ristretto sono sistematicamente attenuate (più vicine a zero) rispetto alla vera correlazione nella popolazione.
- **Distorsione da collider**: condizionare su una variabile (essere pro) che è causata sia dal predittore (punti giovanili) sia da altri fattori non osservati (fisiologia, contatti, fortuna) crea una correlazione *artificiale negativa* fra il predittore e quei fattori. Concretamente: fra i professionisti, chi aveva punteggi giovanili bassi deve necessariamente avere avuto qualcos'altro di eccezionale per arrivarci — quindi il legame tra punti giovanili e qualità da pro appare più debole, o addirittura invertito, di quanto sia realmente.

Questa è la ragione per cui, in molti sport, "fra i professionisti quelli che erano più forti da giovani non sono i migliori" è un risultato ricorrente che viene spesso **interpretato male**. Non significa che i risultati giovanili non contino: significa che stai guardando un campione già filtrato.

**Soluzioni**: modelli a due parti (hurdle), logistica ordinale su tutta la coorte, o correzione di Heckman (Sezione 14). E, in ogni caso, dichiarare esplicitamente il limite.

---

## 3. Disegno dello studio e definizioni operative

### Tipo di disegno

**Studio di coorte retrospettivo su dati d'archivio.** "Coorte" perché segui nel tempo un gruppo definito di persone; "retrospettivo" perché l'esposizione (i risultati giovanili) e l'esito (il professionismo) sono entrambi già accaduti quando inizi lo studio.

Non è uno studio sperimentale: non puoi concludere causalità in senso stretto. Puoi concludere **associazione predittiva**, che per una domanda di talent identification è comunque esattamente ciò che serve (l'obiettivo non è capire *perché*, è capire *se posso prevedere*).

### Aspetti etici e formali

Anche su dati d'archivio anonimizzati serve:
- autorizzazione formale della FCI all'uso dei dati di ranking;
- approvazione del comitato etico dell'ateneo (procedura semplificata per dati retrospettivi anonimi, ma va richiesta);
- anonimizzazione: sostituisci nomi con `athlete_id`, e conserva la chiave di corrispondenza in un file separato e protetto;
- dichiarazione nel manoscritto che lo studio è conforme alla Dichiarazione di Helsinki.

Nota specifica: stai lavorando su **minori** (Esordienti = 13-14 anni). Questo rende l'approvazione etica più stringente e va gestita per tempo. I dati devono essere presentati solo in forma aggregata.

### Definizioni operative — da fissare PRIMA di guardare i dati

Questo punto è metodologicamente cruciale. Se decidi le definizioni dopo aver visto i risultati, stai facendo (anche senza volerlo) *p-hacking*: scegli inconsciamente le definizioni che danno risultati più belli. La soluzione è scrivere le definizioni in un documento datato prima dell'analisi, e — se vuoi essere rigoroso — **pre-registrare** lo studio su OSF (osf.io), che è gratuito e sempre più apprezzato dai revisori.

Definizioni proposte:

| Concetto | Definizione operativa |
|---|---|
| **PRO** | Almeno una stagione con contratto in team UCI WorldTeam o UCI ProTeam |
| **Finestra di osservazione** | Il contratto deve essere firmato entro l'anno solare in cui l'atleta compie 25 anni |
| **Coorti incluse (analisi principale)** | Anni di nascita per cui la finestra è completa: con dati PCS al 2025, coorti fino al 2000 |
| **Coorti incluse (analisi di sopravvivenza)** | Tutte, con censoring per le più recenti |
| **Categorie** | ESO (Esordienti, 13-14) → ALL (Allievi, 15-16) → JUN (Juniores, 17-18) → U23 (19-22) |
| **Anno di categoria** | 1° o 2° anno (per U23: 1°-4°) — variabile fondamentale, non aggregare |
| **Livello PRO (esito ordinale)** | 0 = non PRO; 1 = ProTeam; 2 = WorldTeam; 3 = WorldTeam con ≥1 stagione nei top 100 PCS |
| **Qualità PRO (esito continuo)** | Punti PCS per stagione da pro; in alternativa miglior stagione entro i 26 anni |
| **Esclusioni** | Atleti stranieri tesserati FCI; atleti con dati di nascita mancanti; ciclocross/MTB/pista puri |

**Perché escludere Continental dalla definizione di PRO**: le squadre Continental sono un livello molto eterogeneo, spesso semi-dilettantistico, e l'inclusione o esclusione cambia sensibilmente il tasso di evento. Lo terrai come **analisi di sensibilità** (Sezione 18, Step 19).

**Perché la finestra a 25 anni**: senza un limite temporale, un atleta della coorte 1990 ha avuto 15 anni per firmare e uno della coorte 2000 ne ha avuti 5. Fissare la finestra rende le coorti confrontabili. La scelta di 25 è convenzionale ma difendibile: la grande maggioranza delle transizioni al professionismo avviene entro quell'età.

---

## 4. Costruzione del dataset

### Principio generale: due tabelle, non una

Servono due formati diversi degli stessi dati, perché metodi diversi richiedono strutture diverse.

### Tabella A — formato "lungo" (persona-anno)

Una riga per **atleta × stagione**. È la struttura naturale dei dati FCI, ed è quella richiesta dai modelli misti (Sezione 12) e dall'analisi di sopravvivenza (Sezione 11).

```
athlete_id     identificativo anonimo stabile
birth_year     anno di nascita
birth_date     data completa (serve per birth_quarter)
birth_quarter  trimestre di nascita: 1 = gen-mar, ..., 4 = ott-dic
season         anno solare della stagione
age            età al 31 dicembre della stagione
category       ESO / ALL / JUN / U23
cat_year       1, 2 (per U23: 1-4)
points_raw     punti grezzi nel ranking annuale FCI
rank_pos       posizione in classifica
n_ranked       numero totale di atleti classificati in quella cella
n_races        numero di gare disputate (se disponibile — molto prezioso)
team_id        società di appartenenza
region         comitato regionale
```

Esempio di alcune righe:

| athlete_id | birth_year | season | age | category | cat_year | points_raw | rank_pos | n_ranked |
|---|---|---|---|---|---|---|---|---|
| A0417 | 1996 | 2010 | 14 | ESO | 2 | 34 | 88 | 610 |
| A0417 | 1996 | 2011 | 15 | ALL | 1 | 120 | 41 | 540 |
| A0417 | 1996 | 2012 | 16 | ALL | 2 | 310 | 12 | 528 |
| A0417 | 1996 | 2013 | 17 | JUN | 1 | 95 | 60 | 480 |

### Tabella B — formato "largo" (una riga per atleta)

Derivata dalla A tramite pivot. È la struttura richiesta dai modelli di regressione classici.

```
athlete_id, birth_year, birth_quarter

--- esposizione (predittori) ---
pct_ESO1, pct_ESO2         percentile nel 1° e 2° anno Esordienti
pct_ALL1, pct_ALL2
pct_JUN1, pct_JUN2
pct_U23_1 ... pct_U23_4
best_pct_youth             miglior percentile in assoluto
slope_pct                  pendenza della traiettoria (vedi Sezione 12)
n_seasons_youth            numero di stagioni giovanili disputate
n_races_tot                gare totali

--- esito ---
PRO                        0/1
tier                       0 = non pro, 1 = PRT, 2 = WT, 3 = WT top-100
year_turned_pro
age_turned_pro
pro_seasons                numero di stagioni da pro osservate
pcs_points_total
pcs_points_per_season
pcs_points_best
pcs_points_by_age26
censored                   1 se la finestra di osservazione non è completa
```

### La normalizzazione dei punteggi (passaggio critico)

Trasformi i punti grezzi in **percentile all'interno della cella** `stagione × categoria × anno di categoria`.

Il percentile risponde alla domanda: "quale percentuale di coetanei diretti questo atleta ha superato in quella stagione?". È immune ai cambi di regolamento, interpretabile, e ha una scala fissa 0-100.

```r
library(dplyr)

df <- df |>
  group_by(season, category, cat_year) |>
  mutate(
    n_ranked  = n(),
    rank_pos  = rank(-points_raw, ties.method = "min"),
    pct_rank  = 100 * (1 - (rank_pos - 1) / n_ranked),
    z_log_pts = as.numeric(scale(log1p(points_raw))),
    scored    = as.integer(points_raw > 0),
    top10     = as.integer(rank_pos <= 10),
    top25pct  = as.integer(pct_rank >= 75)
  ) |>
  ungroup()
```

**Perché `log1p` per lo z-score**: i punti sono distribuiti in modo estremamente asimmetrico (moltissimi atleti con pochi punti, pochissimi con tantissimi). La trasformazione log(1+x) comprime la coda e rende la distribuzione più simmetrica. Si usa `log1p` e non `log` perché log(0) è meno infinito.

**Quale usare come predittore principale?** Il `pct_rank`. Ma riporta anche i risultati con `scored` e `top10` come analisi di sensibilità: sono le codifiche usate nella letteratura precedente e rendono i tuoi risultati confrontabili con quelli di Gallo e Mostaert.

### Un avvertimento sul denominatore

Il percentile è calcolato sugli atleti **classificati**. Ma quanti tesserati non entrano mai in classifica? Se il ranking FCI include solo chi ha ottenuto almeno un punto, la tua popolazione è già filtrata, e tutti i risultati vanno interpretati come **condizionati all'aver ottenuto almeno un punto in carriera**.

Se invece riesci a ottenere dalla FCI l'elenco completo dei tesserati per anno e categoria, il valore dello studio aumenta molto: puoi stimare probabilità assolute su tutta la popolazione, e la tabella di attrito (sotto) diventa un risultato di per sé.

Verifica questo punto con la FCI **prima** di iniziare l'analisi.

### Il matching FCI ↔ ProCyclingStats

È il punto in cui si perdono più dati e si introducono più errori. Procedura consigliata:

1. Match automatico su `cognome + nome + anno_nascita`, normalizzando accenti, maiuscole, doppi nomi, apostrofi.
2. Match fuzzy (distanza di Levenshtein) sui residui, con soglia conservativa.
3. **Verifica manuale al 100% dei candidati PRO.** Sono poche decine: vale assolutamente la pena controllarli uno per uno. Un falso negativo qui (un pro classificato come non-pro) pesa moltissimo, perché gli eventi sono rari.
4. Documenta il tasso di match e verifica che i non-matchati non siano sistematicamente diversi (per esempio più forti). Se lo sono, hai un problema di bias da riportare.

### La tabella di attrito

Costruiscila subito, prima di qualunque modello. È descrittiva ma è già un risultato pubblicabile.

| | Esordienti | Allievi | Juniores | U23 | PRO |
|---|---|---|---|---|---|
| n atleti presenti | 2000 | 1300 | 800 | 400 | 45 |
| % dei partenti | 100% | 65% | 40% | 20% | 2,3% |
| % del livello precedente | — | 65% | 62% | 50% | 11% |

(numeri inventati a scopo illustrativo)

Questa tabella dice al lettore, in un colpo d'occhio, che la maggior parte dell'attrito avviene **prima** del punto in cui la performance diventa predittiva. È il contesto in cui va letto tutto il resto.

### Codificare correttamente i valori mancanti

Un atleta assente dal ranking Allievi può esserlo per tre ragioni molto diverse:

| Situazione | Codifica corretta |
|---|---|
| Ha smesso di correre | `NA` + flag `dropout = 1` |
| Correva ma non ha fatto punti | `points_raw = 0`, `pct_rank` calcolato (basso) |
| Non era tesserato quell'anno (infortunio, altro sport) | `NA` + flag `absent = 1` |

Trattare le tre situazioni allo stesso modo è uno degli errori più comuni e più dannosi in questo tipo di studio. La prima e la terza sono dati mancanti; la seconda è un dato osservato di valore basso.

---

# PARTE II — I METODI STATISTICI SPIEGATI

Questa parte spiega ogni metodo che useremo, partendo da ciò che già conosci (regressione lineare e correlazione) e costruendo per aggiunte successive. Ogni sezione ha la stessa struttura: **il problema** → **l'idea** → **come si legge il risultato** → **quando usarlo nel nostro studio**.

---

## 5. Ripasso: dalla regressione lineare a quella logistica

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

Non con i minimi quadrati, ma con la **massima verosimiglianza** (maximum likelihood). L'idea: fra tutti i possibili valori di β0 e β1, scegli quelli che rendono più probabili i dati che hai effettivamente osservato. Il software lo fa iterativamente. Non serve che tu sappia fare i conti, ma serve sapere che è un metodo diverso da OLS, e che eredita da questo alcuni comportamenti (per esempio il bias con eventi rari, Sezione 7).

### In R

```r
fit <- glm(PRO ~ pct_JUN2, family = binomial(link = "logit"), data = dfB)
summary(fit)
```

L'output ti dà `Estimate` (i coefficienti β, **sulla scala logit**), errore standard, z-value, p-value.

**Attenzione**: i coefficienti grezzi della logistica non sono direttamente interpretabili come "aumento di probabilità". Sono aumenti di log-odds. Per interpretarli si esponenziano — ed è la prossima sezione.

---

## 6. Come si legge un odds ratio (senza sbagliare)

### Definizione

```
OR = exp(β1)
```

L'OR è il fattore per cui gli **odds** dell'evento vengono moltiplicati quando `x` aumenta di un'unità.

Esempio concreto. Supponi di stimare, su `pct_JUN2`:

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
dfB$pct_JUN2_10 <- dfB$pct_JUN2 / 10
fit <- logistf(PRO ~ pct_JUN2_10, data = dfB)
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
nd <- data.frame(pct_JUN2 = c(50, 75, 90, 95, 99))
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

## 7. Il problema degli eventi rari e la correzione di Firth

### Il problema

Con ~40 eventi su ~1300 osservazioni, la massima verosimiglianza soffre di due patologie.

**Bias di piccolo campione.** I coefficienti stimati sono sistematicamente **troppo grandi in valore assoluto**. L'entità del bias dipende dal numero di eventi, non dal numero totale di osservazioni. Con 40 eventi il bias può essere del 10-20%.

**Separazione.** Se esiste un valore soglia del predittore che separa perfettamente (o quasi) i casi dai non-casi — per esempio se nessun atleta sotto il 60° percentile U23 è mai diventato pro — la verosimiglianza non ha un massimo finito. Il coefficiente "vero" secondo il modello sarebbe infinito. Il software restituisce coefficienti enormi (tipo 18,4) con errori standard giganteschi (tipo 2400). È un segnale di allarme da riconoscere.

Nel tuo studio la separazione è realistica, soprattutto per i modelli U23.

### La regola degli eventi per variabile (EPV)

Regola pratica classica: servono almeno **10 eventi per ogni predittore** stimato. Con 43 eventi puoi permetterti 4, al massimo 5 predittori. Le versioni più recenti della letteratura (Riley et al.) sono più sofisticate ma la regola dei 10 EPV resta un'ottima guida.

Questa regola vincola pesantemente il tuo studio ed è la ragione principale per cui useremo modelli parsimoniosi e penalizzazione.

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

fit <- logistf(PRO ~ pct_JUN2_10 + birth_quarter + factor(birth_cohort),
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

**Regola operativa per il tuo studio**: usa `logistf` come default per tutti i modelli logistici, non `glm`. Confronta i due nell'appendice per mostrare l'effetto della correzione — è un dettaglio che i revisori metodologicamente attenti apprezzano.

---

## 8. Predittori correlati: multicollinearità e regressione penalizzata

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
vif(glm(PRO ~ pct_ALL2 + pct_JUN1 + pct_JUN2 + pct_U23_1,
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

X <- model.matrix(~ pct_ESO2 + pct_ALL1 + pct_ALL2 + pct_JUN1 +
                    pct_JUN2 + pct_U23_1 + birth_quarter, data = dfB)[, -1]
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

Stimare un modello per categoria evita del tutto il problema. È l'approccio più semplice e va fatto comunque, ma non risponde alla domanda C (il contributo *incrementale*), perché ogni modello ignora le altre categorie. Serve la Sezione 10.

---

## 9. Misurare quanto un modello predice

Un p-value significativo **non** significa che il modello predice bene. Con n grande, associazioni minuscole diventano significative. Serve misurare la qualità predittiva, che ha due dimensioni distinte: **discriminazione** e **calibrazione**.

### 9.1 Discriminazione: la curva ROC e l'AUC

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

### 9.2 Il problema che l'AUC nasconde: il valore predittivo positivo

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

Questa tabella, con i tuoi numeri reali, deve stare nel manoscritto. È il contributo più utile che lo studio possa dare.

### 9.3 Scegliere una soglia: l'indice di Youden

Se devi indicare una soglia operativa, l'indice di Youden massimizza `sensibilità + specificità − 1`.

```r
coords(roc_obj, "best", best.method = "youden",
       ret = c("threshold","sensitivity","specificity","ppv","npv"))
```

Ma la soglia "ottimale" statisticamente non è quella ottimale praticamente: dipende da quanto costa un falso positivo rispetto a un falso negativo. Da cui la sezione successiva.

### 9.4 Decision curve analysis

La DCA valuta il **beneficio netto** di usare il modello a diverse soglie, pesando falsi positivi e falsi negativi secondo le preferenze dell'utilizzatore. Confronta tre strategie: usare il modello, selezionare tutti, selezionare nessuno.

```r
library(dcurves)
dca(PRO ~ p_hat, data = dfB, thresholds = seq(0, 0.3, 0.01)) |> plot()
```

Nel tuo contesto risponde alla domanda concreta: *"a una federazione che può inserire 30 atleti in un progetto elite, il modello serve davvero rispetto a prendere i primi 30 del ranking?"*. Spesso la risposta è "poco", e dirlo è un risultato.

### 9.5 Calibrazione

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

## 10. Modelli annidati: "quanto aggiunge questa informazione?"

Questa è la sezione che risponde alla tua domanda C, la più originale dello studio.

### L'idea

Costruisci una sequenza di modelli in cui ciascuno aggiunge un blocco di informazione al precedente:

| Modello | Contenuto | Domanda |
|---|---|---|
| M0 | Trimestre di nascita + coorte | Baseline demografico |
| M1 | M0 + percentile Esordienti | Sapere com'è andato a 13-14 anni aggiunge? |
| M2 | M1 + percentile Allievi | ...a 15-16? |
| M3 | M2 + percentile Juniores | ...a 17-18? |
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

### Il grafico centrale del tuo paper

Un grafico con l'**età di osservazione sull'asse x** e l'**AUC cumulata sull'asse y**, con bande di confidenza. Mostra visivamente da che età il segnale emerge.

La mia previsione, basata sulla letteratura: curva sostanzialmente piatta intorno a 0,55-0,60 per Esordienti e Allievi, salita marcata da Juniores 2° anno, plateau intorno a 0,80-0,85 con U23 1° anno. Gallo et al. hanno trovato che il valore predittivo cresce con la categoria d'età e che il piazzamento nel primo anno da U23 è il miglior predittore: il tuo studio estenderebbe la curva verso il basso, dove nessuno l'ha ancora misurata.

---

## 11. Analisi di sopravvivenza a tempo discreto

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
fit_surv <- glm(pro_event ~ splines::ns(age, 3) + lag_pct_rank + birth_quarter,
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

## 12. Modelli misti e traiettorie individuali

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

## 13. Regressione logistica ordinale

### Il problema che risolve

"Diventare pro" è binario, ma il successo è graduato: non-pro < ProTeam < WorldTeam < WorldTeam di alto livello.

Le opzioni sarebbero:
- **trattarlo come binario** → butti via informazione;
- **trattarlo come continuo** → assumi che le distanze fra i livelli siano uguali, il che è falso;
- **fare più modelli binari separati** → moltiplichi i test, perdi potenza;
- **logistica ordinale** → usa l'ordine senza assumere distanze uguali. La scelta giusta.

Il vantaggio pratico è grosso: usi **tutta la coorte** in un solo modello, e ottieni una risposta unificata alle domande A e B, aggirando in buona parte il problema della selezione (Sezione 14).

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
                     labels = c("non_pro","PRT","WT","WT_top"), ordered = TRUE)

fit_ord <- polr(tier_f ~ pct_JUN2_10 + pct_U23_1_10 + birth_quarter,
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

## 14. Il problema della selezione: modelli hurdle e Heckman

Torniamo al Problema 5, il più insidioso. Vediamo le tre soluzioni in ordine di complessità crescente.

### 14.1 Modello hurdle (a due parti)

L'idea: il processo che genera i punti PCS ha **due stadi distinti**, e li modelli separatamente.

```
Parte 1:  P(PRO = 1 | x)              →  logistica su TUTTA la coorte
Parte 2:  E[punti PCS | PRO = 1, x]   →  GLM sui SOLI pro
```

Il valore atteso non condizionato si ottiene moltiplicando:

```
E[punti PCS | x] = P(PRO = 1 | x) × E[punti | PRO = 1, x]
```

**Perché è utile**: risponde alla domanda che interessa davvero — *"dato il profilo giovanile di questo atleta, quanti punti PCS mi aspetto in valore atteso?"* — includendo sia la probabilità di arrivarci sia il livello atteso una volta arrivato.

**Perché non risolve tutto**: la Parte 2 è comunque stimata sui selezionati. Se la selezione avviene solo su variabili che hai osservato (i punti giovanili), il modello è corretto. Se avviene anche su variabili non osservate (VO2max, contatti, opportunità), resta distorta. Questa assunzione si chiama *selection on observables* e va dichiarata.

```r
# Parte 1
p1 <- logistf(PRO ~ pct_JUN2_10 + pct_U23_1_10, data = dfB)

# Parte 2 (solo pro)
p2 <- glm(pcs_points_per_season ~ pct_JUN2_10 + pct_U23_1_10,
          family = Gamma(link = "log"), data = subset(dfB, PRO == 1))

# combinazione
E_pro   <- predict(p1, newdata = nd, type = "response")
E_pts   <- predict(p2, newdata = nd, type = "response")
E_total <- E_pro * E_pts
```

### 14.2 Modello di selezione di Heckman

Affronta il caso in cui la selezione avviene su **non osservabili**. Struttura in due equazioni:

```
Equazione di selezione:   PRO*  = γ·z + u     (osservi PRO = 1 se PRO* > 0)
Equazione di esito:       punti = β·x + ε     (osservi punti solo se PRO = 1)
```

Se `u` e `ε` sono correlati (cioè: le stesse cose non osservate che aiutano a diventare pro aiutano anche a fare punti), la stima OLS sui soli pro è distorta. Heckman corregge inserendo nell'equazione di esito un termine aggiuntivo — l'**inverse Mills ratio** — calcolato dalla prima equazione, che cattura la parte sistematica della selezione.

**Il punto critico: la exclusion restriction.** Serve almeno una variabile che entra nell'equazione di selezione ma **non** in quella di esito: qualcosa che influenza la probabilità di firmare un contratto ma non la qualità della prestazione da pro. Senza di essa il modello è identificato solo dalla forma funzionale, ed è notoriamente fragile.

Candidati per il tuo caso:
- presenza di una squadra Continental/development nella regione di residenza;
- numerosità della coorte regionale (competizione per i posti);
- appartenenza a una società storicamente "feeder" di team pro;
- congiuntura del mercato: numero di squadre italiane attive quell'anno.

Il quarto candidato è probabilmente il più difendibile: il numero di posti disponibili in un dato anno influenza chiaramente la probabilità di firmare, ma non la qualità intrinseca dell'atleta.

```r
library(sampleSelection)

fit_heck <- selection(
  selection = PRO ~ pct_JUN2_10 + pct_U23_1_10 + n_italian_teams,
  outcome   = log1p(pcs_points_per_season) ~ pct_JUN2_10 + pct_U23_1_10,
  data = dfB, method = "ml"
)
summary(fit_heck)
```

Guarda il parametro `rho`: se non è significativamente diverso da zero, la selezione su non osservabili non è rilevabile e puoi usare tranquillamente il modello più semplice.

**Consiglio pratico**: usa Heckman come **analisi di robustezza**, mai come analisi principale. Con un campione di 40-60 pro è fragile, e i revisori chiederanno giustamente conto della exclusion restriction.

### 14.3 La soluzione più semplice ed elegante: logistica ordinale su tutta la coorte

Rileggi la Sezione 13. Modellando `tier` (0-3) su tutta la coorte, **non condizioni mai sulla selezione**: i non-pro sono nel modello come livello 0. Il problema di selezione semplicemente non si presenta.

Costo: perdi la granularità del punteggio PCS continuo.
Beneficio: stime non distorte, un solo modello, molta più potenza statistica.

**Raccomandazione**: fai questo come analisi principale della Domanda B. Il modello hurdle come approfondimento, Heckman come robustezza.

---

## 15. Modelli per esiti continui asimmetrici

Se vuoi comunque modellare i punti PCS come variabile continua (parte 2 dell'hurdle, o analisi secondaria), la regressione lineare classica non va bene: i punti PCS sono conteggi fortemente asimmetrici, con molti valori bassi e pochissimi altissimi.

| Modello | Quando usarlo | Comando R |
|---|---|---|
| **OLS su log(1+y)** | Semplice, coefficienti interpretabili come variazioni percentuali. Attenzione: E[log y] ≠ log E[y], quindi la ritrasformazione richiede correzione | `lm(log1p(y) ~ x)` |
| **GLM Gamma con log link** | Esito continuo positivo e asimmetrico. Modella direttamente E[y], niente problemi di ritrasformazione | `glm(y ~ x, family = Gamma(link="log"))` |
| **Binomiale negativa** | Se tratti i punti come conteggi, gestisce la sovradispersione (varianza > media) | `MASS::glm.nb(y ~ x)` |
| **Regressione beta** | Se usi il *percentile* PCS (0-100 → riscalato 0-1) invece dei punti grezzi. Molto robusta e interpretabile | `betareg::betareg(y ~ x)` |
| **Regressione quantile** | Modella la mediana (o altri quantili) invece della media. Insensibile agli outlier. Utile se pochi campionissimi dominano | `quantreg::rq(y ~ x, tau = 0.5)` |

**La mia raccomandazione per il tuo caso**: usa il **percentile del ranking PCS entro coorte** come esito, con regressione beta o semplicemente OLS sul percentile. Motivi:
- stessa scala del predittore (percentile → percentile), quindi il coefficiente è immediatamente leggibile: *"+10 percentile da junior si associa a +X percentile da pro"*;
- robusto a outlier e a cambi di sistema punti PCS negli anni;
- confrontabile fra coorti.

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
fit_rms <- lrm(PRO ~ pct_JUN2_10 + pct_U23_1_10 + birth_quarter,
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
wilcox.test(pct_JUN2 ~ PRO, data = dfB)
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
cliff.delta(pct_JUN2 ~ PRO, data = dfB)
```

Nota elegante: Cliff's delta è legato all'AUC dalla relazione `AUC = (δ + 1)/2`. Quindi un δ = 0,6 corrisponde a un'AUC univariata di 0,80. Comodo per collegare la descrittiva ai modelli.

### Chi-quadro di bontà di adattamento (per il RAE)

Confronta la distribuzione osservata per trimestre di nascita con quella attesa.

**L'errore da non fare**: usare come distribuzione attesa 25/25/25/25. Le nascite non sono uniformi nell'anno, e variano fra coorti. Usa i dati **ISTAT** delle nascite per le coorti effettive del tuo campione.

```r
attesi_prop <- c(0.248, 0.256, 0.259, 0.237)   # da ISTAT, coorti 1990-2000
osservati   <- table(dfB$birth_quarter[dfB$PRO == 1])
chisq.test(osservati, p = attesi_prop)
```

Affianca gli **odds ratio Q1 vs Q4**, che sono più informativi del chi-quadro perché quantificano l'entità.

Gallo et al. hanno mostrato che il RAE non influenzava il success rate dei ciclisti italiani in U17, U19 e U23, mentre uno studio su ciclisti belgi aveva trovato che il RAE influenzava il success rate nella categoria U15 e in misura minore nella U17, ma non nella U19. Con gli Esordienti (13-14 anni) sei esattamente nella finestra d'età dove l'effetto belga era più forte: **è plausibile che tu trovi un RAE marcato negli Esordienti che poi svanisce**. Sarebbe un risultato pulito e importante.

### Test di DeLong

Confronta due AUC calcolate **sugli stessi soggetti** (dati appaiati). Tiene conto della correlazione fra le due curve, che un test naïve ignorerebbe.

```r
roc.test(roc_M2, roc_M3, method = "delong")
```

### Brant test

Verifica l'assunzione di proportional odds nella logistica ordinale (Sezione 13).

### Test di Hosmer-Lemeshow

Test di calibrazione classico: raggruppa in decili di rischio predetto e confronta osservati vs attesi con un chi-quadro. È il test citato nel lavoro di Gallo. Oggi è considerato superato (il risultato dipende arbitrariamente dal numero di gruppi, ed è poco potente), ma riportarlo mantiene la continuità con la letteratura. Affiancalo sempre al calibration plot.


---

# PARTE III — ESECUZIONE

## 18. Piano operativo passo-passo

Ogni step indica: **cosa fare**, **perché**, **come verificare di averlo fatto bene**.

### FASE 0 — Preparazione

---

**STEP 1. Fissare e congelare le definizioni**

*Cosa*: scrivi un documento `definitions.md` con tutte le definizioni della Sezione 3, datalo, non modificarlo più.
*Perché*: evita scelte post-hoc che gonfiano i falsi positivi.
*Verifica*: se hai bisogno di modificarlo dopo aver visto i dati, documenta la modifica e la ragione, e riporta entrambe le versioni nell'analisi di sensibilità.
*Bonus*: pre-registra su OSF. Gratis, 30 minuti, e i revisori lo notano.

---

**STEP 2. Ottenere e verificare i dati FCI**

*Cosa*: ranking annuali 2008-2025 per ESO, ALL, JUN, U23, con nome, data di nascita, società, punti, posizione, e — se possibile — **numero di gare disputate** e **elenco tesserati completo** (non solo i classificati).
*Perché*: le due informazioni extra cambiano il valore dello studio (vedi Sezione 4).
*Verifica*: conta gli atleti per stagione. Se il numero salta bruscamente da un anno all'altro, c'è un cambio di regolamento o un problema di estrazione. Indagalo prima di procedere.

---

**STEP 3. Costruire la Tabella A (persona-anno)**

*Cosa*: un record per atleta × stagione, con `athlete_id` anonimo e stabile.
*Perché*: è la struttura base da cui deriva tutto.
*Verifica*: nessun atleta deve avere due record nella stessa stagione e categoria; l'età deve essere coerente con la categoria (un ESO deve avere 13-14 anni); le transizioni di categoria devono essere sequenziali senza salti impossibili.

```r
# controlli di integrità
dfA |> count(athlete_id, season) |> filter(n > 1)          # duplicati
dfA |> filter(category == "ESO" & !age %in% 13:14)          # età incoerenti
dfA |> group_by(athlete_id) |> arrange(season) |>
       summarise(gap = any(diff(season) > 1))               # buchi di carriera
```

---

**STEP 4. Matching con ProCyclingStats**

*Cosa*: match automatico + fuzzy + verifica manuale al 100% dei PRO.
*Perché*: è il punto di massima perdita di dati e di massimo impatto degli errori.
*Verifica*: riporta il tasso di match. Confronta le distribuzioni di percentile fra matchati e non matchati: se differiscono sistematicamente, hai un bias di selezione da dichiarare.

---

**STEP 5. Normalizzare i punteggi**

*Cosa*: calcola `pct_rank`, `z_log_pts`, `scored`, `top10` dentro ogni cella stagione × categoria × anno di categoria.
*Perché*: rende i punteggi confrontabili tra anni (Problema 4).
*Verifica*: plotta media e mediana dei punti grezzi per stagione. I salti che vedrai giustificano la normalizzazione nel manoscritto — mettili in figura supplementare.

---

**STEP 6. Costruire la Tabella B (una riga per atleta)**

*Cosa*: pivot da lungo a largo, join con gli esiti PCS, codifica corretta dei mancanti (tre tipi diversi, vedi Sezione 4).
*Perché*: è la struttura per i modelli di regressione.
*Verifica*: il numero di righe deve essere uguale al numero di `athlete_id` unici; il conteggio dei PRO deve corrispondere alla verifica manuale dello Step 4.

---

### FASE 1 — Descrittiva e diagnostica

*Questa fase vale il 40% del valore dello studio. Non saltarla per correre ai modelli.*

---

**STEP 7. Tabella di attrito**

*Cosa*: quanti atleti entrano in ogni categoria, quanti proseguono, quanti arrivano al professionismo (Sezione 4).
*Perché*: contestualizza tutto il resto. È il Table 1 del paper.
*Verifica*: le percentuali devono essere coerenti; le uscite devono essere spiegabili.

---

**STEP 8. Descrittive dei punteggi per gruppo**

*Cosa*: mediana e IQR di `pct_rank` per categoria, separatamente PRO e NON-PRO. Test di Mann-Whitney **con Cliff's delta**.
*Perché*: replica il confronto di Gallo e dà l'ordine di grandezza dell'effetto.
*Verifica*: con n così sbilanciato, controlla che i p-value non ti facciano perdere di vista gli effect size. Se δ è piccolo ma p < 0,001, il messaggio è "differenza reale ma piccola".

---

**STEP 9. Correlazioni fra categorie e VIF**

*Cosa*: matrice di correlazione (Spearman, perché non lineari) fra `pct_ESO2 ... pct_U23_1`. Calcola i VIF.
*Perché*: determina se puoi usare modelli non penalizzati (Sezione 8).
*Verifica*: se VIF > 5 su più variabili, la penalizzazione dello Step 13 diventa obbligatoria, non opzionale.

---

**STEP 10. Relative Age Effect**

*Cosa*: distribuzione per trimestre di nascita in PRO e NON-PRO, chi-quadro con attesi ISTAT, OR Q1 vs Q4. Calcolalo separatamente **per categoria** (l'effetto può esistere negli Esordienti e sparire dopo).
*Perché*: replica e estende Gallo e Mostaert verso il basso di età.
*Verifica*: assicurati di usare la distribuzione ISTAT delle coorti giuste, non l'uniforme.

---

**STEP 11. Distribuzione degli esiti PCS**

*Cosa*: istogramma dei punti PCS per stagione fra i pro; verifica asimmetria; decidi la trasformazione (Sezione 15).
*Perché*: determina la scelta del modello per la Domanda B.
*Verifica*: se pochi campionissimi dominano (probabile), considera la regressione quantile o il percentile come esito.

---

### FASE 2 — Modelli per la Domanda A (accesso)

---

**STEP 12. Modelli univariati per categoria-anno**

*Cosa*: una logistica Firth per ogni cella categoria × anno.

```r
library(logistf)
cells <- c("pct_ESO1","pct_ESO2","pct_ALL1","pct_ALL2",
           "pct_JUN1","pct_JUN2","pct_U23_1","pct_U23_2")

res <- lapply(cells, function(v) {
  d <- dfB[!is.na(dfB[[v]]), ]
  d$x <- d[[v]] / 10
  f <- logistf(PRO ~ x + birth_quarter + birth_cohort_c, data = d)
  data.frame(cell = v, n = nrow(d), events = sum(d$PRO),
             OR = exp(coef(f)["x"]),
             lo = exp(f$ci.lower[2]), hi = exp(f$ci.upper[2]),
             p  = f$prob[2],
             auc = as.numeric(pROC::auc(d$PRO, predict(f, type = "response"))))
})
do.call(rbind, res)
```

*Perché*: è il ponte con la letteratura esistente e dà il quadro d'insieme.
*Verifica*: controlla `events` per ogni cella. Sotto 10 eventi, la stima è puramente esplorativa: dichiaralo.
*Output*: una tabella OR per +10 percentile, con IC e AUC, categoria per categoria. È il Table 2 del paper.

---

**STEP 13. Modello multivariato penalizzato**

*Cosa*: elastic net su tutte le categorie insieme, λ scelto per CV (Sezione 8).
*Perché*: stima la predittività congiunta gestendo la collinearità.
*Verifica*: riporta il sottocampione (solo chi ha dati completi) e quanto si riduce n. Usa `lambda.1se` per la parsimonia.
*Attenzione*: niente p-value da questo modello. Serve per la predizione, non per l'inferenza sui singoli coefficienti.

---

**STEP 14. Analisi di incremento (la tua domanda C)**

*Cosa*: sequenza M0 → M1 → M2 → M3 → M4, tutti sullo stesso sottocampione, con LR test, ΔAUC (DeLong), IDI (Sezione 10).
*Perché*: è il contributo originale dello studio.
*Verifica*: che il sottocampione sia identico in tutti i modelli. Controllalo esplicitamente con `nobs()`.
*Output*: il **grafico centrale** — AUC cumulata in funzione dell'età di osservazione, con bande di confidenza bootstrap.

```r
# schema del grafico
plot_df <- data.frame(
  eta_osservazione = c(14, 16, 18, 19),
  modello = c("M1 (ESO)","M2 (+ALL)","M3 (+JUN)","M4 (+U23-1)"),
  auc = auc_vec, lo = auc_lo, hi = auc_hi
)
ggplot(plot_df, aes(eta_osservazione, auc)) +
  geom_ribbon(aes(ymin = lo, ymax = hi), alpha = .2) +
  geom_line() + geom_point() +
  geom_hline(yintercept = .5, linetype = 2) +
  labs(x = "Età di osservazione (anni)",
       y = "AUC cumulata per la predizione del professionismo")
```

---

**STEP 15. Metriche pratiche e decision curve**

*Cosa*: alla soglia di Youden, la tabella 2×2 completa con sensibilità, specificità, PPV, NPV (Sezione 9.2). Più la DCA.
*Perché*: è il messaggio che arriva a federazione e società.
*Verifica*: fai il calcolo a mano su un esempio per assicurarti di aver capito i numeri prima di scriverli.
*Output*: la frase-chiave del paper. Qualcosa come: *"selezionando gli atleti sopra il 90° percentile Junior si intercetta il 74% dei futuri professionisti, ma l'88% dei selezionati non diventerà professionista."*

---

**STEP 16. Modello di sopravvivenza a tempo discreto**

*Cosa*: logistica cloglog sulla tabella persona-anno, con spline dell'età, percentile ritardato, errori standard cluster-robusti (Sezione 11).
*Perché*: recupera le coorti censurate, aggiunge la dimensione temporale, produce curve di incidenza cumulata.
*Verifica*: controlla che la costruzione del dataset "a rischio" sia corretta — nessun record dopo l'evento, censoring codificato bene.

---

**STEP 17. Traiettorie**

*Cosa*: modello misto sulla Tabella A → estrai intercetta e pendenza individuali → inseriscile nel modello del professionismo (Sezione 12).
*Perché*: risponde a "conta il livello o il miglioramento?".
*Verifica*: includi sempre intercetta E pendenza insieme (sono correlate per costruzione); considera l'effetto soffitto sul percentile.

---

### FASE 3 — Modelli per la Domanda B (qualità)

---

**STEP 18. Verifica preliminare di potenza statistica**

*Cosa*: conta i PRO. Se sono meno di 30, **non fare un modello separato per la qualità**: vai direttamente allo Step 19.
*Perché*: con meno di 30 casi e range ristretto, qualunque stima è rumore.
*Verifica*: fai un calcolo di potenza o una simulazione. Meglio scrivere "il campione non consente" che pubblicare un risultato instabile.

---

**STEP 19. Logistica ordinale su tutta la coorte** *(analisi principale della Domanda B)*

*Cosa*: `polr(tier ~ predittori)` su tutti gli atleti, con Brant test (Sezione 13).
*Perché*: evita del tutto il problema della selezione, usa tutta l'informazione, un solo modello.
*Verifica*: numerosità di ogni livello; se il livello più alto ha <10 casi, accorpa.

---

**STEP 20. Modello hurdle** *(approfondimento)*

*Cosa*: logistica su tutti × GLM Gamma sui pro, combinati (Sezione 14.1).
*Perché*: produce il valore atteso non condizionato dei punti PCS, che è il numero più interessante per un dirigente.
*Verifica*: dichiara l'assunzione di *selection on observables*.

---

**STEP 21. Heckman** *(robustezza, opzionale)*

*Cosa*: modello di selezione con exclusion restriction (Sezione 14.2).
*Perché*: verifica se la selezione su non osservabili distorce le stime.
*Verifica*: guarda `rho`. Se non è significativo, la correzione non serve e il modello semplice è adeguato — che è già un risultato utile da riportare.

---

### FASE 4 — Validazione e scrittura

---

**STEP 22. Bootstrap con correzione dell'ottimismo**

*Cosa*: `validate(fit_rms, B = 1000)` (Sezione 16.2).
*Perché*: l'AUC apparente sovrastima quella reale.
*Verifica*: riporta sempre AUC apparente E corretta. Se la differenza è grande (>0,05), il modello è troppo complesso per il campione: semplificalo.

---

**STEP 23. Validazione temporale**

*Cosa*: training su coorti 1990-1996, validation su 1997-2000 (Sezione 16.3).
*Perché*: è la prova più convincente di generalizzabilità.
*Verifica*: se la performance crolla, non nasconderlo — discutilo. Significa che i pattern cambiano nel tempo, che è un risultato.

---

**STEP 24. Analisi di sensibilità pre-specificate**

Minimo quattro:
1. **PRO includendo le squadre Continental** (cambia il tasso di evento e forse le conclusioni);
2. **Finestra a 24 vs 26 anni** invece di 25;
3. **Esclusione degli atleti con meno di 2 stagioni giovanili**;
4. **Imputazione multipla** dei percentili mancanti (`mice`) vs analisi complete-case.

Sull'imputazione multipla, in breve: invece di eliminare le righe incomplete o riempirle con la media, si generano m dataset completi (tipicamente 20) in cui i mancanti sono riempiti con valori plausibili estratti da un modello, si analizzano tutti e m, e si combinano i risultati con le **regole di Rubin** (che sommano l'incertezza entro-imputazione e quella tra-imputazioni). Richiede l'assunzione MAR — *missing at random*, cioè che la mancanza sia spiegabile con le variabili osservate. Nel tuo caso l'assunzione è discutibile (chi smette non è casuale), quindi presenta l'imputazione come robustezza, non come analisi principale.

---

**STEP 25. Confronto con machine learning** *(controllo, non analisi principale)*

*Cosa*: random forest e gradient boosting in **nested cross-validation** (CV interna per gli iperparametri, esterna per la performance).
*Perché*: verifica se esistono non-linearità o interazioni che il modello parametrico perde.
*Come leggerlo*:
- se l'AUC **non migliora** (esito probabile con 43 eventi), è un argomento a favore della parsimonia — scrivilo;
- se migliora, guarda i **valori SHAP** per capire dove, e aggiungi il termine corrispondente al modello parametrico.

*Attenzione*: con eventi rari il ML overfitta molto. Il modello finale dello studio deve restare quello parametrico, interpretabile.

---

**STEP 26. Scrittura secondo TRIPOD**

TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) è la checklist standard per gli studi di modelli predittivi. 22 item che coprono: fonte dei dati, partecipanti, esito, predittori, dimensione campionaria, gestione dei mancanti, metodi statistici, performance, validazione, limiti.

Scaricala da `equator-network.org`, compilala, e allegala come materiale supplementare. Richiede due ore e migliora sensibilmente le probabilità di accettazione.

---

### Priorità se hai tempo limitato

Non tutto è ugualmente essenziale. In ordine:

| Priorità | Step |
|---|---|
| **Irrinunciabili** | 1-7, 12, 14, 15, 19, 22 |
| **Molto raccomandati** | 8-11, 16, 23, 24, 26 |
| **Valore aggiunto** | 13, 17, 20, 25 |
| **Solo se il resto funziona** | 21 |

---

## 19. Struttura del manoscritto

Formato tipico per IJSPP (abstract strutturato max 250 parole, testo ~3500 parole, max 5 fra tabelle e figure).

**Abstract** — Purpose / Methods / Results / Conclusions.

**Introduction** (~600 parole)
Talent identification nel ciclismo; cosa sappiamo (Gallo 2022, Mostaert 2022, Menaspà 2010, Svendsen 2018); il gap: nessuno ha studiato le categorie sotto i 15 anni, nessuno ha modellato il valore *incrementale* per età, nessuno ha affrontato la selezione nel predire la qualità da pro. Le tre domande.

**Methods** (~900 parole)
Disegno; fonte dati e periodo; definizioni operative (PRO, finestra, categorie); normalizzazione dei punteggi con giustificazione; gestione dei mancanti; analisi statistica in sotto-paragrafi che rispecchiano le tre domande; software e versioni; etica.

**Results** (~1000 parole)
Tabella 1: caratteristiche del campione e attrito.
Tabella 2: OR per categoria-anno (Step 12).
Figura 1: AUC cumulata per età di osservazione (Step 14) — **la figura chiave**.
Figura 2: probabilità predette per percentile, con IC.
Tabella 3: metriche di classificazione con PPV/NPV (Step 15).
Tabella 4: risultati della logistica ordinale (Step 19).
RAE nel testo.

**Discussion** (~1000 parole)
Interpretazione dei risultati principali; confronto con Gallo, Mostaert, Svendsen; il messaggio sul PPV e le implicazioni per la selezione precoce; limiti; applicazioni pratiche.

**Practical Applications** (sezione richiesta da IJSPP, ~200 parole)
Scrivila per gli allenatori, non per gli statistici. Frasi concrete, numeri interpretabili, nessun gergo.

### Limiti da dichiarare esplicitamente

Un elenco onesto rafforza il paper invece di indebolirlo:

1. **Solo Italia**: la struttura del ciclismo giovanile italiano non è generalizzabile ad altri paesi.
2. **Selezione sulla popolazione di partenza**: se il ranking include solo chi ha fatto punti, i risultati sono condizionati.
3. **Nessun dato fisiologico**: non puoi distinguere il talento dalla maturazione biologica, dal volume di allenamento, dal supporto societario.
4. **Selezione nella Domanda B**: dichiarata e parzialmente affrontata, non eliminata.
5. **Eventi rari**: precisione limitata, IC ampi, potenza bassa per gli effetti piccoli.
6. **Il PCS come misura di qualità** ha limiti noti (favorisce alcune tipologie di corridore, cambia sistema nel tempo).
7. **Sopravvivenza differenziale**: chi smette prima non è osservabile nelle categorie successive, e non smette a caso.
8. **Solo maschi** (se è così — dichiaralo, e se hai i dati femminili valuta uno studio parallelo, che sarebbe di grande interesse perché il tema è poco studiato).

---

## 20. Trappole da evitare

**1. Confondere significatività statistica e rilevanza pratica.**
Con n = 1300 quasi tutto diventa significativo. Riporta sempre effect size e IC.

**2. Interpretare "non significativo" come "nessun effetto".**
Con 43 eventi la potenza è bassa. Un IC [0,9–2,4] non dice "nessun effetto", dice "non lo sappiamo". Distinguere i due casi è cruciale proprio per la tua domanda C.

**3. Selezionare le variabili guardando i p-value (stepwise).**
La selezione stepwise produce modelli instabili, R² gonfiati, p-value invalidi. È sconsigliata da tutta la letteratura metodologica moderna. Scegli i predittori a priori sulla base della teoria, o usa la penalizzazione.

**4. Data leakage nella validazione.**
Qualunque operazione fatta sull'intero dataset prima della CV (selezione variabili, imputazione, standardizzazione) contamina i fold di test.

**5. Testare troppe ipotesi senza dichiararlo.**
Se stimi 8 modelli per categoria × 3 esiti × 4 specificazioni, alcuni risultati saranno significativi per caso. Dichiara quante analisi hai fatto e distingui chiaramente le pre-specificate dalle esplorative.

**6. Ignorare l'effetto coorte.**
Il ciclismo giovanile italiano del 2008 non è quello del 2022. Includi sempre la coorte di nascita come covariata o effetto fisso.

**7. Usare i punti grezzi.**
Ripetuto perché è l'errore più probabile e più dannoso.

**8. Presentare i risultati come strumento di selezione individuale.**
Statisticamente ingiustificabile con quel PPV, ed eticamente problematico su minori. Il framing corretto è: *comprendere il percorso di sviluppo*, non *identificare i predestinati*. Considera di dedicare un paragrafo esplicito della Discussion a questo punto — è il tipo di responsabilità che i revisori di riviste sportive apprezzano e che rende il paper citabile in ambito federale.

**9. Dimenticare che il risultato nullo va quantificato.**
Se gli Esordienti non predicono, non scrivere "nessuna associazione significativa". Scrivi: *"OR per +10 percentile = 1,03 (IC 95%: 0,97–1,09); ΔAUC rispetto al modello base = 0,004 (IC: −0,01–0,02)"*. Il primo è un non-risultato, il secondo è un risultato.

---

## 21. Glossario

**AUC / ROC** — Area sotto la curva ROC. Probabilità che il modello assegni un punteggio più alto a un caso rispetto a un non-caso presi a caso.

**Bootstrap** — Ricampionamento con reinserimento dal campione osservato, per stimare l'incertezza o correggere l'ottimismo.

**Calibrazione** — Corrispondenza fra probabilità predette e frequenze osservate.

**Censoring (a destra)** — Situazione in cui si sa che l'evento non è ancora accaduto al momento dell'osservazione, ma non se accadrà dopo.

**Cliff's delta** — Effect size non parametrico per il confronto fra due gruppi.

**Cloglog** — Complementary log-log, funzione di link che rende il modello a tempo discreto equivalente a un modello a rischi proporzionali.

**Collider bias** — Distorsione introdotta condizionando su una variabile causata da due o più fattori.

**Cross-validation** — Divisione ripetuta del campione in training e test per stimare la performance fuori campione.

**DCA** — Decision curve analysis: valutazione del beneficio netto di un modello a diverse soglie decisionali.

**Effect size** — Misura dell'entità di un effetto, indipendente dalla dimensione campionaria.

**Effetti fissi / casuali** — Nei modelli misti: parametri comuni a tutti i soggetti / deviazioni individuali.

**Elastic net** — Regressione penalizzata che combina ridge e lasso.

**EPV** — Events per variable: eventi disponibili per ogni predittore stimato. Minimo raccomandato: 10.

**Exclusion restriction** — Variabile che influenza la selezione ma non l'esito; necessaria per identificare il modello di Heckman.

**Firth** — Correzione penalizzata della verosimiglianza per eventi rari e separazione.

**Hazard** — Rischio istantaneo (o per intervallo) che l'evento accada, condizionato al non essere ancora accaduto.

**Heckman** — Modello a due equazioni per correggere la selezione su non osservabili.

**Hurdle model** — Modello a due parti: probabilità dell'evento × intensità condizionata.

**IDI** — Integrated Discrimination Improvement: guadagno nella separazione media fra casi e non casi.

**Imputazione multipla** — Generazione di più dataset completi per gestire i mancanti, con combinazione via regole di Rubin.

**Leakage** — Contaminazione dei dati di test con informazione dei dati di training.

**Logit** — Logaritmo degli odds; scala su cui la logistica è lineare.

**MAR** — Missing at random: la mancanza è spiegabile con le variabili osservate.

**Massima verosimiglianza** — Metodo di stima che sceglie i parametri che rendono più probabili i dati osservati.

**Multicollinearità** — Correlazione elevata fra predittori; instabilizza i coefficienti.

**NPV / PPV** — Valore predittivo negativo / positivo.

**NRI** — Net Reclassification Improvement.

**Odds** — Rapporto p/(1−p).

**Odds ratio** — Rapporto fra odds; `exp(β)` nella logistica.

**Ottimismo** — Sovrastima della performance dovuta alla valutazione sugli stessi dati usati per la stima.

**Overfitting** — Adattamento del modello al rumore del campione.

**Percentile** — Posizione relativa in una distribuzione, 0-100.

**Proportional odds** — Assunzione della logistica ordinale: effetto costante a tutti i punti di taglio.

**RAE** — Relative age effect: vantaggio dei nati nei primi mesi dell'anno di selezione.

**Ridge / Lasso** — Penalizzazioni L2 / L1 nella regressione.

**Sensibilità / Specificità** — Frazione di casi correttamente identificati / frazione di non-casi correttamente esclusi.

**Shrinkage** — Contrazione delle stime verso la media, per stabilizzarle.

**Spline** — Funzione flessibile a tratti per modellare relazioni non lineari.

**TRIPOD** — Checklist di reporting per studi di modelli predittivi.

**VIF** — Variance inflation factor, indice di multicollinearità.

---

## Riferimenti essenziali

**Studi di riferimento nel dominio**
- Gallo G, Mostaert M, Faelli E, Ruggeri P, Delbarba S, Codella R, Vansteenkiste P, Filipas L. Do race results in youth competitions predict future success as a road cyclist? A retrospective study in the Italian Cycling Federation. *Int J Sports Physiol Perform*. 2022;17(4):621-626.
- Mostaert M, Vansteenkiste P, Pion J, Deconinck FJA, Lenoir M. The importance of performance in youth competitions as an indicator of future success in cycling. *Eur J Sport Sci*. 2022;22(4):481-490.
- Menaspà P, Sassi A, Impellizzeri FM. Aerobic fitness variables do not predict the professional career of young cyclists. *Med Sci Sports Exerc*. 2010.
- Svendsen IS, Tønnessen E, Tjelta LI, Ørn S. Training, performance, and physiological predictors of a successful elite senior career in junior competitive road cyclists. *Int J Sports Physiol Perform*. 2018;13(10):1287-1292.

**Metodologia**
- Hosmer DW, Lemeshow S, Sturdivant RX. *Applied Logistic Regression*. 3rd ed. Wiley, 2013.
- Harrell FE. *Regression Modeling Strategies*. 2nd ed. Springer, 2015. — il riferimento su validazione, ottimismo, spline, penalizzazione.
- Steyerberg EW. *Clinical Prediction Models*. 2nd ed. Springer, 2019. — il più leggibile sui modelli predittivi.
- Heinze G, Schemper M. A solution to the problem of separation in logistic regression. *Stat Med*. 2002;21(16):2409-2419.
- Singer JD, Willett JB. *Applied Longitudinal Data Analysis*. Oxford, 2003. — capitoli 10-12 sulla sopravvivenza a tempo discreto, spiegati benissimo.
- Collins GS, Reitsma JB, Altman DG, Moons KGM. TRIPOD statement. *BMJ*. 2015;350:g7594.

**Pacchetti R**
`dplyr`, `tidyr` (manipolazione) · `logistf` (Firth) · `glmnet` (penalizzazione) · `pROC` (ROC, DeLong) · `rms` (validazione, calibrazione) · `MASS` (`polr`) · `brant` · `lme4` (modelli misti) · `survival`, `splines` (sopravvivenza) · `sampleSelection` (Heckman) · `mice` (imputazione) · `dcurves` (DCA) · `effsize` (Cliff's delta) · `sandwich`, `lmtest` (SE robusti)

