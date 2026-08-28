# Ranking giovanili italiani e transizione al professionismo

Analisi predittiva sui ranking nazionali giovanili italiani (ciclismo.info, 2007-2025) e sull'esito professionistico (ProCyclingStats).

Impianto metodologico: [`guida_metodologica_v5.md`](guida_metodologica_v5.md).

## Da dove vengono i dati

| Fonte | Provenienza |
|---|---|
| Ranking giovanili italiani | `data/giovanile/ciclismo.db`, prodotto da **[lucabnt/risultati-ciclismo-giovanile](https://github.com/lucabnt/risultati-ciclismo-giovanile)** — repository separato con lo scraper di ciclismo.info e il database. Privato per ora, potenzialmente pubblico. Schema **2.1** in uso qui, **2.2** a monte (aggiunge `atleti.data_nascita` e `anno_nascita`); i numeri della verifica valgono per l'estrazione del **10 agosto 2026** |
| Date di nascita | schede personali di ciclismo.info, da `scripts/03_scarica_schede.py` → `data/giovanile/schede.db`. **Con lo schema 2.2 la nascita è già alla fonte**: rigenerando il database a monte la pipeline la usa da sola, senza modifiche (precedenza sorgente → scheda → inferenza). Vedi [`docs/da_fare.md`](docs/da_fare.md) §A5 |
| Esiti di carriera | ProCyclingStats, da `scripts/04_scarica_pcs.py` → `data/pcs/pcs.db` |
| Distribuzione attesa delle nascite | Eurostat `demo_fmonth`, per il test sull'effetto dell'età relativa |

Questo repository **non** contiene dati: `data/` è escluso da git per intero (vedi «Dati personali»).

## Documenti

| File | Contenuto |
|---|---|
| [`docs/definizioni.md`](docs/definizioni.md) | Definizioni operative congelate — coorti, esiti, predittori, esclusioni |
| [`docs/verifica_dati_giovanile.md`](docs/verifica_dati_giovanile.md) | Verifica della sorgente ciclismo.info (FASE 0, step 1 e 3) |
| [`docs/piano_pcs.md`](docs/piano_pcs.md) | Piano di acquisizione ProCyclingStats e procedura di matching |
| [`docs/da_fare.md`](docs/da_fare.md) | Lavoro aperto: configurazione esterna, correzioni note, analisi da impostare |
| [`docs/da_fare.md`](docs/da_fare.md) | Lavoro aperto: configurazione esterna, correzioni note, analisi da impostare |

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

## Dati personali

I dati riguardano **atleti minorenni**. Nel repository entra **solo cio' che e' anonimo**.

`.gitignore` nega tutto sotto `data/` per default e autorizza per eccezione: oggi la sola eccezione e' `data/private/manual/`, che contiene le decisioni di risoluzione manuale come id numerici e motivazioni impersonali. Restano quindi fuori la sorgente ciclismo.info (nomi e cognomi in chiaro), il crosswalk, le liste di verifica e il database di analisi.

Il **salt di anonimizzazione** vive in `data/private/salt.txt`, generato al primo avvio e mai committato. Tenerlo nel sorgente renderebbe l'anonimizzazione solo apparente: gli `id_atleta` sono interi fra 1 e 37.704, quindi con il salt pubblico la tabella `athlete_id → id_atleta` si ricostruisce per forza bruta in pochi secondi, e da li' bastano le classifiche pubbliche per risalire ai nomi. Va trattato come una chiave: perderlo significa che tutti gli `athlete_id` cambiano al ricalcolo successivo.

Prima di ogni commit:

```bash
python scripts/00_check_privacy.py
```

Verifica che i file sensibili siano esclusi da git e che nessun file destinato al repository contenga nomi di atleti. Per farlo eseguire in automatico:

```bash
git config core.hooksPath .githooks
```

## Stato

- [x] Verifica della sorgente giovanile
- [x] Definizioni congelate
- [x] Tabelle A e B (lato predittori)
- [x] Risoluzione manuale delle omonimie e trattamento delle stagioni anomale
- [x] Date di nascita dalle schede personali (sblocca il Relative Age Effect)
- [x] Variabili di contesto in `tab_b` (società, regione, mobilità)
- [ ] Acquisizione ProCyclingStats — script pronto, piano in [`docs/piano_pcs.md`](docs/piano_pcs.md)
- [ ] Matching e conteggio degli eventi (STEP 4: decide se la Domanda B è modellabile)
- [ ] Descrittiva, modelli, validazione
