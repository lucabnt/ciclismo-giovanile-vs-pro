# Ranking giovanili italiani e transizione al professionismo

Analisi predittiva sui ranking nazionali giovanili italiani (ciclismo.info, 2007-2025) e sull'esito professionistico (ProCyclingStats).

Impianto metodologico: [`guida_metodologica_v5.md`](guida_metodologica_v5.md).

> **In English.** A statistical study of Italian youth cycling rankings (ciclismo.info, seasons 2007-2025) and of who later races professionally (ProCyclingStats). It asks from what age race results say something about a rider's future. They already do at thirteen, more than the literature expected; the study then measures why that is still a poor basis for selection, since most of the riders any threshold would flag never turn professional. Published here are the code, the generated report (`output/analisi.md`) and the results archive (`output/risultati.db`) that every number in it is drawn from. The underlying data are not published, because they concern minors. Code is MIT, text and figures CC BY 4.0. Everything else, this file included, is in Italian.

## Da dove vengono i dati

| Fonte | Provenienza |
|---|---|
| Ranking giovanili italiani | `data/giovanile/ciclismo.db`, prodotto da **[lucabnt/risultati-ciclismo-giovanile](https://github.com/lucabnt/risultati-ciclismo-giovanile)** — repository separato con lo scraper di ciclismo.info e il database. Privato per ora, potenzialmente pubblico. Schema **2.1** in uso qui, **2.2** a monte (aggiunge `atleti.data_nascita` e `anno_nascita`); i numeri della verifica valgono per l'estrazione del **10 agosto 2026** |
| Date di nascita | schede personali di ciclismo.info, da `scripts/03_scarica_schede.py` → `data/giovanile/schede.db`. **Con lo schema 2.2 la nascita è già alla fonte**: rigenerando il database a monte la pipeline la usa da sola, senza modifiche (precedenza sorgente → scheda → inferenza). Vedi [`docs/da_fare.md`](docs/da_fare.md) §A5 |
| Esiti di carriera | ProCyclingStats, da `scripts/04_scarica_pcs.py` → `data/pcs/pcs.db` |
| Distribuzione attesa delle nascite | Eurostat `demo_fmonth`, per il test sull'effetto dell'età relativa |

Questo repository **non** contiene dati: `data/` è escluso da git per intero (vedi «Dati personali»).

## Riferimenti esterni

`riferimenti/` contiene i dati pubblici che servono come denominatore o come atteso, trascritti a mano da fonti che non hanno un'API. Ogni file porta in testa la propria provenienza e i propri limiti, perché un dato trascritto senza provenienza non è utilizzabile.

| file | cosa contiene | fonte |
|---|---|---|
| `tesserati_fci.csv` | tesserati per categoria e sesso, 2020-2025 | FCI, «I numeri della Federazione Ciclistica Italiana» |
| `societa_fci.csv` | società affiliate per regione, 2021-2025 | idem, Parte I |

Stanno qui e non sotto `data/` di proposito: `data/` è negato senza eccezioni perché contiene riferimenti a persone, e quella regola non va indebolita per dei totali nazionali.

Servono a rispondere alla domanda che dà scala a tutto il resto: **in classifica compare circa un tesserato su sette**. Ogni percentuale dello studio ha quel settimo come denominatore.

## Documenti

| File | Contenuto |
|---|---|
| [`docs/definizioni.md`](docs/definizioni.md) | Definizioni operative congelate — coorti, esiti, predittori, esclusioni |
| [`docs/verifica_dati_giovanile.md`](docs/verifica_dati_giovanile.md) | Verifica della sorgente ciclismo.info (FASE 0, step 1 e 3) |
| [`docs/piano_pcs.md`](docs/piano_pcs.md) | Piano di acquisizione ProCyclingStats e procedura di matching |
| [`docs/da_fare.md`](docs/da_fare.md) | Lavoro aperto: configurazione esterna, correzioni note, analisi da impostare |
| [`docs/literature_review.md`](docs/literature_review.md) | Rassegna della letteratura, 22 studi, con appendice di revisione |
| [`docs/tripod.md`](docs/tripod.md) | Checklist TRIPOD compilata: cosa è coperto, cosa resta un limite |
| `docs/post/`, `docs/piano_post.md` | Le bozze dei nove post, il piano editoriale, le regole di scrittura e i titoli. **Non stanno nel repository**: sono il prodotto, non la prova, e i post finiti si leggono sul blog. Ogni loro cifra è controllata contro `output/risultati.db` da [`scripts/11_verifica_documenti.py`](scripts/11_verifica_documenti.py), che salta i file se non li trova |
| `archive/` | Le quattro versioni precedenti della guida metodologica. **Non stanno nel repository**: sono superate dalla `v5`, e la storia di git le conserva comunque per chi voglia vedere come il disegno dello studio è cambiato |

## Rieseguire tutto da zero

La sequenza completa, dall'archivio vuoto al documento finito. Le sezioni successive
spiegano ogni passo nel dettaglio; questa serve a non doverle leggere tutte per sapere in
che ordine vanno e quanto costano.

**Cosa serve prima di cominciare.** Python 3.9 o successivo (`tomllib` è nella libreria
standard dal 3.11; sotto, `requirements.txt` installa `tomli`), R 4.6 per i
soli modelli, e il database di partenza `data/giovanile/ciclismo.db`, che **non è in questo
repository**: viene da [risultati-ciclismo-giovanile](https://github.com/lucabnt/risultati-ciclismo-giovanile).
Senza quello non si parte, e non c'è modo di ricostruirlo da qui.

**La versione di R conta.** La catena è collaudata con R 4.6.1. I pacchetti compilati per
una versione di R non si caricano con una precedente: con `logistf` installato sotto la
4.6, un R 4.2 rimasto sulla stessa macchina si ferma al primo modello. Se ne convivono due,
`Rscript --version` dice quale risponde.

| # | comando | quanto dura | serve a |
|---|---|---|---|
| 1 | `pip install -r requirements.txt` | un minuto | dipendenze Python |
| 2 | `python scripts/03_scarica_schede.py` | ~4 ore e mezza | date di nascita complete, senza le quali l'effetto dell'età relativa non è misurabile |
| 3 | `python scripts/01_build_tabelle.py` | qualche minuto | costruisce `analisi.db`: `tab_a`, `tab_b`, anagrafica |
| 4 | `python scripts/02_casi_da_verificare.py` | qualche minuto | genera le liste di verifica manuale; le decisioni già prese sono in `data/private/manual/` e vengono riapplicate da sole |
| 5 | `python scripts/04_scarica_pcs.py` | ~2 ore | esiti di carriera da ProCyclingStats |
| 6 | `python scripts/05_match_pcs.py` | qualche minuto | collega i giovanili ai profili PCS |
| 7 | `python scripts/06_esiti.py` | qualche minuto | porta `PRO` e `tier` in `tab_b` |
| 8 | `python scripts/07_riferimenti.py` | un minuto | nascite attese da Eurostat |
| 9 | `python scripts/08_prepara_modelli.py` | qualche minuto | costruisce `modelli.db`, il rettangolo che legge R |
| 10 | `Rscript R/16_univariati.R` … `R/30_misura.R` | qualche minuto in tutto | i modelli, nell'ordine elencato più avanti |
| 11 | `python scripts/10_sensibilita.py` | qualche minuto | analisi di sensibilità |
| 12 | `python report/assembla.py` | un minuto | genera `output/analisi.md` e le figure |
| 13 | `Rscript R/26_bootstrap_traiettorie.R` | cinque minuti | facoltativo: l'incertezza delle traiettorie stimate; poi si rilancia il 12 |

**Due trappole, entrambe già costate tempo.** La prima: `01` ricostruisce `analisi.db` da
zero e svuota `match_pcs`, quindi dopo ogni `01` vanno rifatti `05` e `06`, in
quest'ordine. La seconda: i passi 2 e 5 scaricano da siti esterni e sono ripartibili, ma
se si interrompono lasciano l'archivio incompleto senza dirlo — si controlla con
`python scripts/04_scarica_pcs.py --stato`.

**Prima di ogni commit**, due controlli che escono con codice diverso da zero se qualcosa
non va:

```bash
python scripts/00_check_privacy.py        # nessun dato personale nei file destinati a git
python scripts/11_verifica_documenti.py   # le cifre scritte a mano coincidono con l'analisi
```

**La catena femminile** gira sugli stessi script, cambiando un parametro. `SESSO=F`
sovrascrive `studio.sesso` senza toccare la configurazione, così il maschile resta in
piedi mentre si lavora sull'altro:

```bash
SESSO=F python scripts/04_scarica_pcs.py --strati AB   # ~22 min, archivio separato pcs_F.db
SESSO=F python scripts/05_match_pcs.py
SESSO=F python scripts/06_esiti.py
```

Il femminile ha però un limite che nessun comando risolve: le divisioni professionistiche
femminili nascono nel 2020 (la seconda solo nel 2025), quindi l'esito «professionista» non
è confrontabile con quello maschile sulle coorti più vecchie. Vedi
[`docs/definizioni.md`](docs/definizioni.md).

## Pipeline

```bash
python scripts/01_build_tabelle.py
```

Legge `data/giovanile/ciclismo.db` e ricostruisce da zero `data/analisi/analisi.db`:

| Tabella | Contenuto |
|---|---|
| `tab_a` | formato lungo: atleta × stagione × categoria × anno di categoria, con percentili entro cella |
| `tab_b` | formato largo: una riga per atleta, predittori pivotati; colonne di esito da popolare dopo PCS |
| `anagrafica` | anno di nascita ricostruito, con livello di affidabilità |
| `attrito` | conteggi per coorte e categoria |
| `match_pcs` | ponte verso ProCyclingStats, da popolare |
| `qualita_dati` | diagnostica dell'ultima esecuzione |

Script di supporto:

| Script | A cosa serve |
|---|---|
| `00_check_privacy.py` | controllo da eseguire prima di ogni commit |
| `02_casi_da_verificare.py` | genera le liste di verifica manuale; le decisioni si scrivono in `data/private/manual/` e sono applicate al giro successivo |
| `03_scarica_schede.py` | scarica le schede personali da ciclismo.info per la data di nascita completa — vedi sotto |
| `04_scarica_pcs.py` | scarica gli esiti di carriera da ProCyclingStats in quattro strati; `--stato` produce il conteggio degli eventi dello STEP 4 |
| `05_match_pcs.py` | collega gli atleti giovanili ai profili PCS su nome più data di nascita; popola `match_pcs` |
| `06_esiti.py` | porta gli esiti di carriera in `tab_b`: `PRO`, `tier`, `team_quality_first` |

**L'ordine conta**: `01` ricostruisce `analisi.db` da zero e svuota `match_pcs`, quindi la sequenza è `01` → `05` → `06`.

L'anno di nascita viene preso dalla prima fonte disponibile: colonna della sorgente → scheda personale → inferenza dall'anno di corso.

## Scaricare le date di nascita

Le classifiche non riportano l'età, ma ciclismo.info pubblica una scheda per atleta con la data di nascita completa. Serve per tre cose: sostituire l'anno di nascita inferito, ricavare l'anno di corso Under 23, e rendere analizzabile il Relative Age Effect.

È un processo lungo ma senza sorprese, e conviene lanciarlo in un terminale a parte.

```bash
python scripts/03_scarica_schede.py --stato
```

Dice a che punto siamo, quanto manca, la copertura della data completa per coorte di nascita e il confronto fra l'anno letto dalla scheda e quello inferito. Non fa richieste di rete.

```bash
python scripts/03_scarica_schede.py --solo-incerti
```

Scarica le schede dei soli atleti il cui anno di nascita non è certo, circa 3.000: **poco più di un'ora**. È il minimo per chiudere le incertezze anagrafiche.

```bash
python scripts/03_scarica_schede.py
```

Scarica tutti i circa 13.000 atleti: **circa quattro ore e mezza**. Serve se si vuole la data completa per tutta la popolazione, cioè per il Relative Age Effect.

Utile sapere:

- **Si può interrompere con Ctrl+C in qualunque momento.** Il lavoro fatto è salvato e rilanciando lo stesso comando riprende da dove era arrivato. Vale anche se il portatile si spegne o cade la rete.
- L'avanzamento viene stampato ogni 25 schede con il tempo che manca.
- La pausa fra le richieste è di 1,2 secondi ed è regolabile con `--pausa`, ma non conviene scendere sotto il secondo: è un sito piccolo e non c'è fretta.
- `--limite 200` fa un lotto di prova e si ferma.
- L'HTML viene conservato compresso, quindi se il parsing va migliorato basta `--riparsa`, che riestrae i campi senza rifare una sola richiesta.

Finito il download:

```bash
python scripts/01_build_tabelle.py
```

che usa le nascite osservate al posto di quelle inferite. Poi conviene rilanciare anche `02_casi_da_verificare.py`: con le date complete il controllo sulle omonimie diventa molto più netto, perché due frammenti della stessa persona hanno la stessa data mentre due omonimi no.

Scrive inoltre `data/private/crosswalk_atleti.csv`, che collega `athlete_id` a nome e cognome. Serve solo per il matching e la verifica manuale.

## Scaricare gli esiti da ProCyclingStats

```bash
pip install procyclingstats cloudscraper
```

Il secondo pacchetto serve perché PCS sta dietro Cloudflare; senza, le richieste possono tornare 403. Lo script avvisa se manca.

```bash
python scripts/04_scarica_pcs.py --strati AB
```

Rose WorldTeam e ProTeam 2011-2026 più la top 500 globale per stagione: circa 700 richieste, **mezz'ora**. È il minimo per il conteggio degli eventi.

```bash
python scripts/04_scarica_pcs.py --stato
```

Produce la tabella dello STEP 4 — professionisti, top 500 e top 100 per coorte — che decide se la Domanda B è modellabile o va ridimensionata a descrittiva. Non fa richieste di rete.

```bash
python scripts/04_scarica_pcs.py --strati CD
```

Italiani a punti 2007-2025 e profili dei candidati: qualche ora. Serve per il predittore internazionale U19/U23 e per le date di nascita PCS.

```bash
python scripts/04_scarica_pcs.py --strati A --continental
```

Facoltativo. Aggiunge le squadre Continental all'enumerazione, circa 200 per stagione, un paio d'ore. Serve solo a chiudere il caso di chi ha corso Continental senza mai fare punti PCS e senza mai passare da WorldTeam o ProTeam: per tutti gli altri candidati la classe Continental si sa già dallo strato D, perché `teams_history()` restituisce tutte le stagioni con la classe della squadra.

Come il 03, è ripartibile e interrompibile con Ctrl+C, con pausa di 2,5 secondi fra le richieste.

**Chi ha continuato a correre senza diventare professionista** si legge invece da ciclismo.info, senza alcuna richiesta: `tab_b.elite_seasons` conta le stagioni nella classifica Elite italiana dopo i 23 anni e `tab_b.racing_after_u23` dice se l'atleta compare in una qualunque classifica dopo i 22. È la classifica «promiscua» che era stata esclusa dalle celle U23 perché come denominatore non andava bene, ma come segnale di continuità è esatta.

## Dal dato al testo

L'obiettivo del progetto è una serie di blog post. Il livello di produzione genera un
documento Markdown unico, con tabelle e figure, da cui i post si ritagliano.

```bash
pip install -r requirements.txt
python scripts/07_riferimenti.py     # una volta: scarica gli attesi demografici Eurostat
python report/assembla.py
```

**Il documento e le figure sono versionati**, a differenza di tutto il resto di ciò che si
rigenera. La ragione è che chi clona il repository non può rigenerarli: il database di
partenza contiene dati personali e resta fuori da git, quindi senza i file di output i
risultati non sarebbero verificabili da nessuno. Sono aggregati e mascherati, e il controllo
privacy li attraversa come ogni altro file destinato al repository.

Produce `output/analisi.md` — con indice, tabelle, figure e un riquadro «Come si misura» per ogni metodo usato — e le figure in due versioni: `output/figure/` per il documento, che sta nel repository, e `output/figure_web/` per i post, con testi più grandi e maggiore risoluzione, che resta in locale perché sarebbe la stessa cosa due volte.

**Ogni output dice di quando è.** Il documento porta la data di generazione in testa, le
figure di `output/figure/` la portano scritta dentro l'immagine in basso a destra, e
l'archivio la registra modulo per modulo nella tabella `esecuzione`. Le figure sono l'unico
caso in cui la data va dentro il file invece che accanto: un PNG ritagliato dal documento
viaggia da solo, e senza quella riga nessuno saprebbe più di quando siano i numeri. Le
versioni per il web ne fanno a meno, per come stanno in pagina: lì la figura sta dentro un
post che porta già la propria data. Le bozze dei post,
che sono scritte a mano, portano in intestazione la data dell'analisi contro cui sono state
verificate, e la scrive `scripts/11_verifica_documenti.py` quando il controllo passa: se le
cifre non corrispondono più, la data non avanza.

Il testo dei moduli si scrive in ASCII e **gli accenti si applicano alla generazione** (`report/accenti.py`): il documento si rigenera ogni anno con dati nuovi, quindi una correzione fatta a mano sul file andrebbe rifatta ogni volta. Se compare una parola accentata non prevista, l'assemblatore la segnala invece di lasciarla passare.

**Calcolo e presentazione sono separati.** Ogni modulo in `report/moduli/` ha due funzioni:

| | |
|---|---|
| `calcola()` | interroga i database e scrive in `output/risultati.db` |
| `rendi(lettura)` | legge **solo** dall'archivio e restituisce il testo della sezione |

È la regola che tiene onesto il documento: se un numero non è nell'archivio non può finire nel testo, quindi non può essere scritto a mano. E i modelli, che sono la parte lenta, non si rilanciano ogni volta che si riscrive un paragrafo:

```bash
python report/assembla.py --solo-testo   # riusa i risultati già calcolati
python report/assembla.py --moduli rae   # un modulo solo
```

**L'ordine delle sezioni sta in `config.toml`**, non nei nomi dei file: riorganizzare il documento, o dividerlo in più post, non comporta rinominare moduli.

**I commenti dichiarano la propria premessa.** I numeri vengono tutti da una query, ma le frasi che li interpretano — «il gradiente quasi sparisce», «il secondo anno discrimina meglio» — sono scritte a mano guardando i dati di oggi. `md.afferma(condizione, premessa, testo)` chiede di dichiarare accanto alla frase la condizione numerica che la sostiene: quando la condizione cade, la frase esce con un avviso nel testo e l'assemblatore lo segnala. È il modo in cui il documento può essere rigenerato fra anni senza pubblicare in silenzio un commento che i dati non sostengono più.

Due regole sono imposte dal codice invece che ricordate: ogni tabella dichiara la propria numerosità, e **nessuna cella con meno di 5 atleti viene pubblicata** — diventa `<5`. I dati riguardano minorenni, e una cella con due o tre persone li rende identificabili anche in forma aggregata.

### I modelli in R

I modelli statistici stanno in R e scrivono nello stesso `output/risultati.db`: SQLite è il confine fra i due linguaggi. Python non stima nulla e R non formatta nulla.

```bash
python scripts/08_prepara_modelli.py     # costruisce data/analisi/modelli.db
Rscript R/16_univariati.R                # un modello per categoria
Rscript R/18_annidati.R                  # quanto aggiunge ogni categoria alla precedente
Rscript R/19_metriche.R                  # cosa succede se si seleziona davvero
Rscript R/20_sopravvivenza.R             # a che età si passa professionisti
Rscript R/21_traiettorie.R               # conta il livello o il miglioramento?
Rscript R/22_qualita_carriera.R          # non solo se si arriva, ma fino a dove
Rscript R/24_validazione.R               # ottimismo e validazione temporale
python scripts/10_sensibilita.py         # le scelte di disegno cambiano le conclusioni?
Rscript R/27_confronto_ml.R              # un modello piu' complicato farebbe meglio?
Rscript R/17_penalizzato.R               # e se si usassero tutte le categorie insieme?
Rscript R/30_misura.R                    # lo stesso punteggio e' lo stesso risultato?
python report/assembla.py                # rigenera il documento
```

Fuori da questa sequenza c'è un passo solo, e sta fuori perché è l'unico lento:

```bash
Rscript R/26_bootstrap_traiettorie.R     # circa 5 minuti, 500 ricampionamenti
```

Ristima il modello misto delle traiettorie a ogni ricampionamento, cosa che
`24_validazione.R` non fa, e misura quanta incertezza aggiunga il fatto che livello e
pendenza siano stimati e non osservati. Va rieseguito solo quando cambiano i dati.
Se non lo si esegue il documento si genera lo stesso: la sezione dice che manca e
riporta il comando.

`08_prepara_modelli.py` esiste perché le regole dello studio — coorti, sesso, celle, quali classi contano come professionismo — stanno in `config.toml`, che R non legge senza dipendenze aggiuntive. Le regole si applicano una volta sola in Python e R trova un rettangolo già filtrato: cambiare le coorti significa modificare `config.toml` e rilanciare lo script, senza toccare i file R.

Pacchetti richiesti:

```r
install.packages(c("RSQLite", "jsonlite", "logistf", "pROC", "MASS", "lme4", "randomForest", "glmnet"))
```

Se R non è installato, il documento si genera lo stesso: le sezioni modellistiche dichiarano cosa manca e con quale comando ottenerlo, invece di sparire in silenzio.

**Ogni modello porta con sé un controllo.** Lo STEP 16 rilegge dall'archivio l'AUC che la descrittiva ha ricavato dal delta di Cliff e verifica di ritrovare lo stesso numero: due strade indipendenti per la stessa quantità. Se divergono, lo script lo dice.

## Dati personali

I dati riguardano **atleti minorenni**. Nel repository entra **solo cio' che e' anonimo**.

`.gitignore` nega tutto sotto `data/` per default e autorizza per eccezione: oggi la sola eccezione e' `data/private/manual/`, che contiene le decisioni di risoluzione manuale come id numerici e motivazioni impersonali. Restano quindi fuori la sorgente ciclismo.info (nomi e cognomi in chiaro), il crosswalk, le liste di verifica e il database di analisi.

Il **salt di anonimizzazione** vive in `data/private/salt.txt`, generato al primo avvio e mai committato. Tenerlo nel sorgente renderebbe l'anonimizzazione solo apparente: gli `id_atleta` sono interi fra 1 e 37.704, quindi con il salt pubblico la tabella `athlete_id → id_atleta` si ricostruisce per forza bruta in pochi secondi, e da li' bastano le classifiche pubbliche per risalire ai nomi. Va trattato come una chiave: perderlo significa che tutti gli `athlete_id` cambiano al ricalcolo successivo.

Undici documenti del progetto contengono cifre scritte a mano, perché sono prosa e non file generati: la checklist TRIPOD, il piano editoriale e le nove bozze dei post. Tutti portano in testa l'avviso che non si rigenerano. Che le loro cifre non siano diventate false lo verifica:

```bash
python scripts/11_verifica_documenti.py
```

Prima di ogni commit:

```bash
python scripts/00_check_privacy.py
```

Verifica che i file sensibili siano esclusi da git e che nessun file destinato al repository contenga nomi di atleti. Per farlo eseguire in automatico:

```bash
git config core.hooksPath .githooks
```

## Licenza

Due licenze, perché in questo repository ci sono due cose diverse.

| cosa | licenza | in una riga |
|---|---|---|
| **Codice** — `scripts/`, `R/`, `report/`, `config.toml`, `.githooks/` | MIT, [`LICENSE`](LICENSE) | fanne quello che vuoi, tieni la nota di copyright |
| **Contenuti** — `docs/`, `output/analisi.md`, le figure, questo README, la guida metodologica, le trascrizioni in `riferimenti/` | CC BY 4.0, [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md) | riusali come vuoi, anche commercialmente, **purché tu dica da dove vengono** |

Il confine passa fra *ciò che fa qualcosa* e *ciò che dice qualcosa*, non fra estensioni di
file: la prosa che i moduli di `report/` producono è contenuto, anche se il file che la
genera è codice.

**Il titolare dei diritti è lucabnt**, autore del codice e dei contenuti: è il nome che
portano i due file di licenza.

**I dati di partenza non sono inclusi e non sono nostri.** Appartengono ai siti da cui
vengono, ciascuno con le proprie condizioni: le classifiche a ciclismo.info, gli esiti di
carriera a ProCyclingStats, le nascite attese a Eurostat, i tesserati alla Federazione
Ciclistica Italiana. Nell'Unione Europea una banca dati può essere protetta anche quando i
fatti che contiene non lo sono. Questo repository non ne distribuisce nessuna: `data/` è
escluso da git per intero, e `riferimenti/` contiene soltanto totali nazionali già
pubblicati dalla federazione, trascritti con la loro fonte.

**E resta il vincolo che viene prima di ogni licenza**: i dati riguardano minorenni, qui non
entra nulla che permetta di risalire a una persona, e nessuna licenza autorizza a provarci.

## Stato

- [x] Verifica della sorgente giovanile
- [x] Definizioni congelate
- [x] Tabelle A e B (lato predittori)
- [x] Risoluzione manuale delle omonimie e trattamento delle stagioni anomale
- [x] Date di nascita dalle schede personali (sblocca il Relative Age Effect)
- [x] Variabili di contesto in `tab_b` (società, regione, mobilità)
- [x] Acquisizione ProCyclingStats e conteggio degli eventi (STEP 4)
- [x] Modelli e validazione — tutti gli STEP della guida — i restanti in [`docs/da_fare.md`](docs/da_fare.md) §FASE 3
- [x] Matching giovanili ↔ PCS (STEP 6) — resta la verifica manuale, [`docs/da_fare.md`](docs/da_fare.md) §C5
- [x] Esiti di carriera in `tab_b` (`PRO`, `tier`, qualità della società)
- [x] Livello di produzione: `report/` con archivio dei risultati e generatore Markdown
- [x] Descrittiva: attrito (9), punteggi per gruppo (10), correlazioni e VIF (11), età relativa (15)
- [x] Descrittiva: contesto e mobilità (STEP 13-14)
- [x] Modelli in R (FASE 3 e 4) e validazione (FASE 5) — STEP 16-28 chiusi
- [x] Bozze dei nove blog post — fuori dal repository, come il resto della lavorazione editoriale
- [ ] Stesura definitiva dei post e revisione delle figure post per post
