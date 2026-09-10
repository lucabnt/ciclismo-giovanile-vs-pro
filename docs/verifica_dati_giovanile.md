# Verifica dei dati ciclismo.info

**Data della verifica:** 27 agosto 2026 · aggiornato dopo le risoluzioni manuali
**Sorgente:** `data/giovanile/ciclismo.db` (schema v2.1), estratta il **10 agosto 2026**
**Copre:** FASE 0 / STEP 1 e STEP 3 del piano operativo (Sezione 18 della guida)

---

## 0. Sintesi

| | |
|---|---|
| Record totali | 140.308 |
| Atleti | 13.000 |
| Società | 1.883 |
| Righe atleta–anno–regione | 33.175 (12.782 atleti, 98,3%) |
| Record usabili per l'analisi | **30.979** (individuali, annuali, stagioni 2007-2025) |
| Atleti nel dataset di analisi | **12.357** |

**Verdetto: i dati sono utilizzabili.** Non ci sono lacune di scraping sulle categorie maschili, l'identità degli atleti regge tutti i controlli di coerenza, e l'anno di nascita è ricostruibile per il 95,3% degli atleti — anzi, **osservabile** per tutti, perché la fonte pubblica una scheda per atleta con la data di nascita completa (§9). Ci sono però **quattro vincoli strutturali** che cambiano il disegno dello studio rispetto a quanto ipotizzato nella guida, e vanno recepiti prima di procedere.

---

## 1. Le quattro conseguenze da recepire

### ① Le classifiche Esordienti partono dal 2009, non dal 2007 — le coorti diventano cinque

Questa era la verifica obbligatoria dello STEP 1, ed è andata nel senso sfavorevole.

| Categoria | Prima stagione | Ultima |
|---|---|---|
| Esordienti (U15) M | **2009** | 2026 |
| Allievi (U17) M | 2007 | 2026 |
| Juniores (U19) M | 2007 | 2026 |
| Elite-Under23 M | 2007 | 2026 |
| Tutte le categorie femminili | 2011 | 2026 |

Il primo nato che ha l'U15 primo anno coperto è quello del **1996** (13 anni nel 2009). Con il limite superiore fissato dai 25 anni compiuti entro una stagione chiusa (2025), la finestra è:

| Analisi | Coorti | N |
|---|---|---|
| **Principale (parte dall'U15y1)** | **1996-2000** | **5** |
| Dall'U15y2 | 1995-2000 | 6 |
| Dall'U17y1 | 1992-2000 | 9 |
| Dall'U19y1 | 1990-2000 | 11 |
| Sopravvivenza a tempo discreto (con censura) | tutte | — |

La guida prevedeva sette coorti; ne restano cinque. Conta soprattutto per la Domanda B (qualità della carriera): la stima di 15-25 eventi top-100 va rivista al ribasso di circa un terzo, e va **ricontata sul serio allo STEP 4**, prima di progettare qualunque modello. Se scendesse sotto i 15, la Domanda B va ridimensionata a descrittiva, come già previsto.

Contropartita: i modelli che partono dall'U17 hanno **nove** coorti invece di otto. Vale la pena costruirli sul serio, non solo come estensione.

### ② Il denominatore è "chi ha fatto almeno un punto"

Il punteggio minimo osservato è **1, mai 0**, in tutte le categorie e tutte le stagioni. Non esiste in classifica un solo atleta con zero punti.

Ogni conclusione va quindi formulata come: *«fra gli atleti che hanno ottenuto almeno un punto nel ranking nazionale della loro categoria…»*. Non "fra i giovani ciclisti italiani", e nemmeno "fra i classificati", che è ambiguo. Un ragazzo che ha corso tutta la stagione senza mai entrare a punti è indistinguibile da uno che non ha corso affatto.

### ③ La stagione 2020 è un cratere e la 2026 è incompleta

| | 2019 | 2020 | 2021 |
|---|---|---|---|
| U15 M | 531 | **280** (−47%) | 477 |
| U17 M | 566 | **246** (−54%) | 461 |
| U19 M | 400 | **195** (−51%) | 355 |
| U23 M | 161 | **84** (−48%) | 164 |

Il 2020 è l'unico salto brusco di `n_ranked` in tutta la serie: il resto della copertura decresce in modo regolare (calo reale del tesseramento giovanile, circa −40% dal 2007 al 2025), senza gradini da cambio di criterio della fonte. Il percentile assorbe il calo di numerosità, ma **non** il fatto che nel 2020 si sia corso molto meno: chi ha ottenuto punti quell'anno lo ha fatto su molte meno occasioni. Le celle 2020 vanno marcate e trattate in analisi di sensibilità.

La stagione **2026 è in corso** al momento dell'estrazione (10 agosto). Va esclusa da qualunque analisi, non solo troncata.

### ④ L'Under 23 non è usabile senza l'anno di nascita — ma la fonte ce l'ha

Per l'U23 la fonte pubblica una classifica unica sui quattro anni di corso, senza indicare l'età. L'anno di corso è ricostruibile solo dall'anno di nascita, che dalle sole classifiche **manca per i 586 atleti che compaiono solo da U23** (non hanno mai fatto punti da giovanili, o sono stranieri). Sono il 34% della popolazione U23.

Sembrava un problema risolvibile solo con ProCyclingStats. Non è così: ciclismo.info pubblica una **scheda personale per atleta** con la data di nascita completa. Vedi §8.

---

## 2. Struttura delle classifiche: come è fatta davvero la fonte

Questo è il punto in cui il DB si presta a essere letto male, e da cui dipende tutta la costruzione della Tabella A.

Il sito pubblica, per ogni categoria e stagione, **due liste**: una generale e una "primo anno". Il rapporto fra le due **cambia da categoria a categoria**, e in un caso cambia anche nel tempo:

| Categoria | Struttura | Sovrapposizione fra le due liste | Anni |
|---|---|---|---|
| Esordienti M | **disgiunte** — la generale è la classifica di 2° anno | 0 su 18 stagioni | 2009-2026 |
| Donne Esordienti | **annidate** fino al 2021, poi **disgiunte** | 100% → 0% dal 2022 | 2011-2026 |
| Allievi M, Juniores M, Donne Allieve, Donne Juniores | **annidate** — la generale contiene tutti, la primo anno è il sottoinsieme | 100% in tutte le stagioni | 2007/2011-2026 |
| Elite-Under23 M | tre liste: `elite-under23` (Elite+U23), `under23` (solo U23), `elite-under23_primo_anno` | `under23` ⊂ `elite-under23` | 2007-2026 |

Due conseguenze operative, entrambe recepite in `scripts/01_build_tabelle.py`:

**Per l'U23 va usata la lista `under23`, non la `promiscua`.** Sulle 1.481 presenze che stanno nella promiscua ma non nella under23, solo **4** hanno un'età da U23: sono Elite over-22. La lista `under23` è quindi completa e la promiscua aggiunge solo rumore.

**Il campo `anno_corso` del DB non va usato così com'è.** Per le Donne Esordienti 2011-2021 la lista generale è etichettata `anno_corso = 2` pur contenendo anche le prime anno, che compaiono quindi due volte con due etichette diverse. È l'unico errore di etichettatura trovato, riguarda solo la categoria femminile, e produce 321 doppioni se lo si prende alla lettera.

> La vista `v_stagionale` del DB sorgente eredita entrambi i problemi: contiene **971 righe duplicate** (650 Elite-Under23, 321 Donne Esordienti) per lo stesso atleta/anno/categoria. Non usarla come base dell'analisi; `tab_a` la sostituisce.

---

## 2-bis. Cosa dicono i regolamenti federali

*Aggiunto il 10 settembre 2026, leggendo le Norme Attuative 2027 della FCI — due documenti, uno
per Esordienti e Allievi, uno per Juniores, Under 23 ed Elite.* Fino a qui la struttura delle
classifiche era stata ricostruita dai dati; questi articoli la confermano dalla parte del
regolamento, e chiudono un'assunzione che i post dichiaravano come tale.

| Cosa | Dove | Cosa dice |
|---|---|---|
| **Le due annate degli Esordienti hanno classifiche separate** | Esordienti/Allievi, art. 4.2.1 e 4.2.5 | Primo e secondo anno «possono correre separatamente in manifestazioni organizzate nella stessa località»; e quando il comitato regionale approva una **gara unica**, si adotta il chilometraggio del primo anno «**con classifica separata per fascia d'età**». Vale anche per le Donne Esordienti |
| **L'eccezione, ed è stretta** | Esordienti/Allievi, art. 4.2.4 | Se in una delle due categorie i partenti sono meno di dieci, «può essere stilata un'unica classifica». Sotto i cinque partenti, la categoria può essere accorpata (Elite/U23/Juniores, art. 1.7) |
| **I punti vanno ai primi cinque, da 5 a 1** | Esordienti/Allievi, art. 4.4.21 | «5 pnt al 1°, 4 pnt al 2°, 3 pnt al 3°, 2 pnt al 4°, 1 pnt al 5°». La stessa scala compare per le gare femminili: «punteggio di valorizzazione FCI per le prime 5 classificate» (Juniores/U23, art. 11.4.1 e 11.6) |
| **Le classifiche restano separate anche quando la gara è una sola** | Juniores/U23, art. 11.6 | Nelle gare femminili «Open», che mettono insieme Junior ed Elite/Under 23, «sono previste due classifiche separate» |
| **Le categorie e le età** | Esordienti/Allievi, art. 1.1-1.5; Juniores/U23, art. 11 | Esordienti 13 e 14 anni distinti per annata, Allievi 15-16 in una categoria sola, Juniores 17-18, Under 23 dai 19 |
| **La lista Under 23 contiene anche gli Elite** | Juniores/U23, art. 11.2.2 | Nelle gare nazionali e regionali Elite/Under 23 corrono italiani fino a 27 anni. È la ragione per cui il conteggio delle gare in Under 23 è un limite inferiore |

**Cosa non c'è in questi documenti.** I moltiplicatori per livello di gara — nazionale che vale
il doppio di una regionale, internazionale il triplo — non compaiono nelle Norme Attuative: la
scala federale di valorizzazione è piatta, cinque punti al vincitore di qualunque gara. Il peso
per livello è quindi un'elaborazione della fonte, oppure sta nel RTAA, che è un altro documento
e non l'ho letto. **Il punto si è chiuso il giorno dopo**: il regolamento della fonte, letto in
§2-ter, pubblica i moltiplicatori per esteso, quindi sono suoi. Il documento tecnico attribuisce correttamente quel peso «alla classifica
italiana» e non alla federazione, e l'effetto è comunque verificato dai dati, dividendo i punti
per il numero di piazzamenti.

**Cosa cambia nei testi.** Il post 3 dichiarava come assunzione che negli Esordienti le due
annate non si facciano concorrenza: ora è un articolo di regolamento, con la sua nota. Il post 2
afferma che i punti vanno ai primi cinque: è la scala federale, non una convenzione della fonte.

---

## 2-ter. Cosa dice il regolamento della fonte

*Aggiunto il 10 settembre 2026, leggendo i «Regolamenti speciali della classifica nazionale by
ciclismo.info»: Esordienti (ver. 1.00 del 16 febbraio 2009), Allievi e Juniores (ver. 1.00 del
16 agosto 2008). Sono tre documenti di una pagina, datati ma coerenti con i dati fino al 2026, e
sono conservati fuori dal repository insieme al resto del materiale di lavorazione. Il
regolamento Under 23 non è stato reperito.*

Fino a qui la scala dei punti era stata dichiarata sulla base della documentazione del sito e
verificata indirettamente sui dati. Questi documenti la danno per esteso, e con essa quattro
regole di raccolta che non erano note e che lasciano un segno nei numeri.

### La scala dei punti

| tipo di gara | Esordienti e Allievi | Juniores |
|---|---|---|
| regionale | 5-4-3-2-1 | 5-4-3-2-1 |
| nazionale | 5-4-3-2-1 | 10-8-6-4-2 |
| internazionale | non in calendario | 15-12-9-6-3 |
| campionato italiano in linea | 15-12-9-6-3 | 15-12-9-6-3 |
| campionato italiano a cronometro | 15-12-9-6-3, ma **solo Allievi** | 15-12-9-6-3 |
| campionato europeo | non in calendario | 20-16-12-8-4 |
| campionato del mondo | non in calendario | 30-24-18-12-6 |

**Una delle righe è lettera morta.** Il fascicolo Esordienti della fonte ricalca quello
Allievi parola per parola, campionato a cronometro compreso, ma quel campionato **per gli
Esordienti non si disputa**: le Norme Attuative 2027, art. 6.2.2, lo prevedono in due gare
distinte «per le categorie Allievi e Donne Allieve», e basta. In Esordienti la gara a punteggio
triplo è quindi una sola all'anno, il campionato italiano in linea, che l'art. 6.1 prevede in
prove distinte per il primo e per il secondo anno — un'altra conferma della separazione fra le
due annate.

*Un dettaglio che vale la pena notare, perché lega la classifica alla selezione.* In Esordienti
l'unica gara che vale il triplo è anche l'unica a cui non ci si iscrive: al campionato italiano
in linea si va selezionati dal proprio comitato regionale, tre atleti per comitato più le quote
proporzionali ai tesserati (art. 6.1). I punti pesanti di quella categoria sono quindi
accessibili solo a chi è già stato scelto da qualcuno. Sono cinque piazzamenti all'anno su
migliaia, quindi l'effetto sui totali è trascurabile, ma è un caso in cui la misura e la
selezione non sono del tutto indipendenti.

Per l'Under 23 si assume la scala Juniores, essendo anch'essa una categoria con calendario
internazionale. **È un'assunzione, e va tenuta presente**: se l'Under 23 avesse moltiplicatori
diversi, la riga U23 della tabella «quanto vale un piazzamento» andrebbe letta di conseguenza.
Il resto dell'analisi non ne dipende, perché il predittore è il percentile dentro la cella e non
il punteggio.

### Le quattro regole di raccolta

| Regola | Cosa dice il regolamento | Effetto sui dati |
|---|---|---|
| **Solo strada** | Contano le gare su strada, in circuito e a cronometro, di qualunque lunghezza, «escluse le gare tipo pista» | La classifica non è un censimento del ciclismo giovanile ma della sola strada: la copertura sui tesserati è un limite inferiore |
| **Solo società italiane** | «Non partecipano i corridori appartenenti a Società affiliate all'estero anche se ottengono risultati in gare svolte in Italia» | Chi passa a una squadra straniera esce dalla classifica senza aver smesso di correre: un meccanismo in più fra quelli del post 3 |
| **I risultati esteri li segnala l'atleta** | Chi corre all'estero «dovrà far pervenire a ciclismo.info copia dell'ordine di arrivo» perché il risultato valga | Le gare internazionali sono previste ma non raccolte d'ufficio: la copertura dipende da un'iniziativa individuale |
| **Anche in Italia la raccolta è a impegno di mezzi** | Il comitato «farà il possibile» per conoscere tutti i risultati e segnalerà le gare mancanti al momento della pubblicazione | Non è un archivio ufficiale: un'assenza può essere una mancanza della fonte |

### Lo spareggio è quello della fonte

A parità di punti il regolamento ordina «per prima cosa [per] le vittorie, a seguire i secondi
posti e così via fino al quinto posto»; poi, se ancora pari, vince chi ha raggiunto per primo il
punteggio; in ultimo il più giovane.

**I primi due livelli sono esattamente il criterio esteso di questo studio**, scelto all'inizio
del progetto come scelta metodologica propria e prima di guardare qualunque esito. Non era una
nostra invenzione: è la regola pubblicata. Ricostruendo il percentile con essa non si impone un
ordinamento nostro, si riproduce quello della fonte — e la verifica sui pari merito mostra
comunque che la scelta non cambia i risultati. Gli ultimi due livelli non si applicano qui: il
primo chiederebbe la data di ogni gara, che non abbiamo; il secondo introdurrebbe l'età dentro
la misura, che è ciò che l'analisi si preoccupa di tenerne fuori.

### Altre due cose minori

**I pari merito in gara.** Se due atleti arrivano a pari merito, entrambi prendono i punti della
posizione e il corridore successivo è considerato terzo. È la ragione per cui i punti totali di
una stagione possono superare la somma teorica dei posti a punti.

**La stagione.** Va da fine marzo all'ultima gara di ottobre, secondo il calendario federale, e
i risultati arretrati entrano fino a quindici giorni dopo la fine.

### Cosa cambia rispetto a quanto era scritto

1. **Il punto lasciato aperto in §2-bis si chiude.** I moltiplicatori per livello non sono
   nelle Norme Attuative della FCI perché **sono della fonte**, e il suo regolamento li
   pubblica. Non serve più ipotizzare che stiano nel RTAA.
2. **Erano due i moltiplicatori, sono cinque.** Il documento tecnico diceva «nazionale il
   doppio, internazionale il triplo»: mancavano il campionato italiano (×3 anche in Esordienti e
   Allievi), l'europeo (×4) e il mondiale (×6).
3. **La scala in Esordienti e Allievi non è piatta**, come si era scritto: i campionati
   italiani valgono il triplo. Sono due gare per stagione in Allievi e **una sola in
   Esordienti**, dove il campionato a cronometro non si disputa: l'effetto sui totali è
   trascurabile, ma la frase era sbagliata due volte.
4. **Una cifra era sbagliata.** «15 punti per la vittoria internazionale contro 5 per quella
   nazionale» confondeva la gara nazionale con quella regionale: la nazionale ne vale 10.
5. **Il regolamento non descrive due classifiche per gli Esordienti**, e parla della categoria
   come di una sola. La struttura ricostruita in §2 mostra però che dal 2009 la fonte pubblica
   per gli Esordienti maschili **due liste disgiunte**, e per le Donne Esordienti lo fa dal
   2022: su questo il regolamento è più vecchio dei dati, e valgono i dati.

---

## 3. Anno di corso: la regola è esatta

L'anno di corso in U17 e U19 si deduce dall'appartenenza alla lista "primo anno". È una deduzione, quindi andava validata. Il test: prendere i 6.656 atleti il cui anno di nascita è **certo** perché ricavato dalle liste disgiunte degli Esordienti, e verificare se la loro presenza nella lista primo anno Allievi corrisponde davvero all'avere 15 anni.

| | in lista primo anno | non in lista |
|---|---|---|
| **15 anni** (1° anno) | 2.213 | **0** |
| **16 anni** (2° anno) | **0** | 3.107 |

**Concordanza 100% su 5.320 verifiche, in entrambe le direzioni.** La regola è esatta, non approssimata.

Il test chiarisce anche un dato che a prima vista sembra un artefatto: i primi anno classificati sono sistematicamente **meno** dei secondi anno (rapporto 0,71 in U17, stabile in tutte le stagioni dal 2007 al 2026). Non è un difetto della fonte — è il fenomeno reale che i primi anno, correndo contro ragazzi più grandi, entrano a punti meno spesso. Va detto nel blog post: è già di per sé un risultato.

---

## 4. Anno di nascita

Non è un campo della fonte: va ricostruito. La ricostruzione è a due livelli di affidabilità, e il livello va portato dentro l'analisi, non nascosto.

| Livello | Come | Atleti | % |
|---|---|---|---|
| **certo** | liste disgiunte (Esordienti) o presenza in una lista "primo anno" | 9.207 | 74,5% |
| **presunto** | solo lista generale → si assume 2° anno | 2.525 | 20,4% |
| conflitto | stime incompatibili (probabile problema di identità) | 39 | 0,3% |
| ignoto | compare solo da U23 | 586 | 4,7% |

L'errore possibile nel livello "presunto" è unidirezionale: se l'atleta era in realtà un primo anno che non compare nella lista primo anno, l'anno di nascita risulta **anticipato di uno**. Per questo, a parità di evidenza, si prende il massimo delle stime e non il minimo.

> **Nota su `v_atleta_nascita`.** La vista del DB sorgente usa `MIN()` sulle stime, che va nella direzione sbagliata proprio rispetto a questo errore. Sui 426 atleti con stime discordanti, `MIN` coincide con la stima affidabile in 63 casi su 385; `MAX` in 305. La stima ricostruita in `anagrafica` corregge il problema e riduce i casi irrisolti da 426 a 39.

**Quanto è affidabile il livello "certo".** I 5.068 atleti che hanno **almeno due segnali di livello 1 indipendenti** — presenza in una lista "primo anno", oppure Esordienti a liste disgiunte — concordano in **5.067 casi su 5.068 (99,98%)**. Nessuna lista sorgente è contaminata, in nessuna stagione. Ne segue la regola usata per gli omonimi (§5): due stime di livello 1 diverse indicano due persone, non un errore di misura.

Coerenza età/categoria dopo la ricostruzione: **99,85%** delle righe. Le 47 righe residue (39 atleti, 0,3%) sono marcate `eta_coerente = 0` in `tab_a` — vedi §5.

---

## 5. Identità degli atleti

Il rischio principale in un dataset di questo tipo è l'omonimia: due persone diverse fuse in un solo `id_atleta`, o una persona spezzata in due.

**Fusioni: nessuna.** La durata massima di una carriera nel dataset è **9 stagioni**, che è esattamente il massimo teorico (Esordienti 1° anno a 13 anni → U23 4° anno a 22). Se due omonimi fossero stati fusi, comparirebbero carriere di 12-18 anni. Non ce ne sono.

> Le carriere apparentemente lunghissime (fino a 18 anni) che si vedono nella vista `v_carriera` vengono tutte dalla lista `elite-under23` promiscua, che include gli Elite di qualunque età: un professionista che corre una gara italiana a 30 anni compare lì. Usando la lista `under23` il problema sparisce.

**Frammentazioni: risolte.** Ci sono 142 gruppi di `id_atleta` distinti con lo stesso nome completo, che generano **33 coppie** con anni di nascita compatibili. Di queste:

| Esito | N | Base della decisione |
|---|---|---|
| Persone diverse | 18 | presenti nella **stessa stagione** |
| Persone diverse | 7 | **regioni diverse** |
| Persone diverse | 5 | due stime di nascita di **livello 1 discordanti** (§4: concordano nel 99,98% dei casi) |
| Persone diverse | 1 | deciso a mano: due atleti della stessa regione, nati 1996 e 1995 |
| **Stessa persona → fuse** | **3** | nascita concorde, stessa regione, carriere che si incastrano senza sovrapporsi |

Le tre fusioni sono registrate in `data/private/manual/fusioni_atleti.csv`, che contiene solo id numerici e motivazioni impersonali ed è quindi la traccia verificabile della decisione senza essere un dato personale. Dopo la fusione le tre carriere risultano continue e coerenti in ogni stagione — una copre senza salti da U17 secondo anno a U23 quarto anno, il che conferma la scelta a posteriori.

Nessuno dei trenta atleti coinvolti è un candidato professionista: uno solo sta sopra il 95° percentile (femminile, quindi fuori dall'analisi principale) e la mediana del gruppo è 46.

**Presenze fuori categoria: 82 righe, legittime.** Un Under 23 al primo anno può correre alcune gare Juniores, e comparire quindi nel ranking Juniores a 19 anni. Non è un errore della fonte:

| Categoria | Età | Righe |
|---|---|---|
| U19 | 19 | 65 |
| U17 | 17-18 | 12 |
| U23 | 17-18 | 5 |

Quella stagione però **non appartiene alla popolazione in studio** per quella categoria. Le righe restano in `tab_a` con `cat_year_conf = 'fuori_categoria'` e `cat_year` nullo: sono documentate ma non entrano in nessuna cella, né come numeratore né come denominatore. Questa regola risolve da sola anche i dodici casi di atleti presenti in due categorie nella stessa stagione: dopo l'esclusione non ne resta **nessuno**.

**Contraddizioni residue: 39 atleti (0,3%), tutte marcate.** La colonna `eta_coerente` di `tab_a` vale 0 quando l'età implicata dall'anno di nascita non è compatibile con l'anno di corso assegnato. Sono 47 righe su 30.979, e hanno tutte la stessa forma: età da primo anno ma anno di corso letto come secondo, su atleti il cui anno di nascita è `presunto` o in conflitto. È l'incertezza di livello 2 descritta in §4, non un problema nuovo.

Vanno **escluse o controllate a mano, non corrette d'ufficio**: qualunque correzione automatica sceglierebbe arbitrariamente quale delle due evidenze contraddittorie tenere.

---

## 6. Completezza dello scraping

| Esito | N |
|---|---|
| ok | 6.062 |
| vuota | 2.134 |
| errore di rete | 792 |
| 404 | 15 |

Tutti i fallimenti su URL **nazionali** riguardano le categorie femminili nelle stagioni **2007-2010**, cioè prima che quelle classifiche esistessero. Le pagine `vuota` sono classifiche regionali di regioni con pochissimi tesserati (Valle d'Aosta, Basilicata, Calabria, Molise).

**Nessuna classifica nazionale maschile risulta mancante o fallita.** La copertura per cella (stagione × categoria × anno di corso) non presenta buchi né gradini oltre al 2020 già discusso.

---

## 7. Il punto più delicato: i pari punti

I punteggi sono piccoli e molto discreti — mediana 7-8 punti, primo quartile 3. Il risultato è che l'ordinamento per soli punti, come prescritto dalla guida, lascia **la quasi totalità degli atleti a pari merito**:

| | % atleti a pari punti | valori distinti di percentile per cella | atleti per cella |
|---|---|---|---|
| U15 | 92,2% | 58,6 | 280,8 |
| U17 | 93,1% | 43,4 | 228,7 |
| U19 | 87,9% | 43,4 | 161,6 |
| U23 | 59,6% | 21,0 | 34,5 |

Una cella U17 con 229 atleti produce 43 valori distinti di percentile. Il predittore principale dello studio è, di fatto, una variabile a 43 livelli con enormi ammassi.

**C'è però più informazione nei dati.** La fonte pubblica, oltre ai punti, il numero di vittorie e di piazzamenti dal 2° al 5° posto, e li usa per sciogliere i pari punti: la posizione pubblicata è un ordinamento **totale** 1..n, senza ex aequo. Ricostruendo lo stesso criterio (punti → vittorie → 2i → 3i → 4i → 5i) con `ties.method = "min"`:

| | % a pari merito | valori distinti per cella |
|---|---|---|
| U15 | 92,2% → **52,7%** | 58,6 → **160,4** |
| U17 | 93,1% → **59,4%** | 43,4 → **118,5** |
| U19 | 87,9% → **51,0%** | 43,4 → **95,6** |
| U23 | 59,6% → **28,9%** | 21,0 → **28,0** |

La granularità quasi triplica e la correlazione con la versione a soli punti resta **r = 0,996-0,998**: non è una variabile diversa, è la stessa variabile misurata meglio.

> **Non usare invece la posizione pubblicata dalla fonte.** In coda alla classifica ordina in modo arbitrario atleti con record identico: nella cella U15 2015 primo anno, le ultime venti posizioni sono tutte «1 punto, un quinto posto». Prendere quelle posizioni per buone significa inventare un ordinamento dove non ce n'è uno.

**Raccomandazione:** usare `pct_rank_ext` come predittore principale e `pct_rank` (soli punti, versione della guida) come analisi di sensibilità. Entrambi sono in `tab_a`, e in `tab_b` come `pct_*` e `pctpt_*`. Costa zero riportarli tutti e due.

---

## 8. Cosa c'è di più di quanto previsto dalla guida

Tre covariate che la guida dava per "da verificare" e che ci sono:

- **Regione** — 12.782 atleti su 13.000 (98,3%), per stagione. Concentrazione forte: Lombardia 23%, Veneto 19%, Toscana 13%. Utilizzabile come effetto di raggruppamento o come covariata.
- **Società** — 1.883 società, con storico dei nomi e alias. Utilizzabile come effetto casuale nei modelli misti.
- **Vittorie e piazzamenti (1°-5°) per stagione** — oltre ai punti. Alimentano il percentile esteso della sezione 7 e permettono predittori alternativi (numero di vittorie da U15, presenza sul podio).

C'è inoltre una serie di **classifiche mensili** (57.000 record) non usata dalla pipeline. Permetterebbe di misurare la progressione *dentro* la stagione. Fuori perimetro per ora, ma è lì.

---

## 9. Le schede personali: la fonte ha la data di nascita

Le classifiche non riportano l'età, ma ciclismo.info pubblica una **scheda per atleta** che contiene la data di nascita completa:

```
http://<sottodominio>.ciclismo.info/scheda_corridore_risultati_gare_<id>_<x>_<y>_<anno>.htm
```

Tre cose verificate direttamente:

- **Il segmento con il nome è ignorato dal server**: conta solo l'id. Un URL con `_x_y_` al posto di cognome e nome restituisce la stessa pagina. Sparisce così ogni rischio legato alla normalizzazione di nomi, accenti e cognomi doppi — che sarebbe stato il punto fragile di questa raccolta.
- **Sottodominio e anno invece contano**: vanno presi da una stagione in cui l'atleta compare davvero, altrimenti la risposta è 200 ma senza dati anagrafici. Si usa la stagione più recente di ciascun atleta.
- **Ci sono due campi, non uno**: l'intestazione riporta sempre `COGNOME NOME (AAAA)`, e in più compare `Nato il GG Mese AAAA`. Sui casi provati l'anno c'era nel **100%** dei casi, la data completa nell'**82%**.

### La ricostruzione per inferenza, messa alla prova

Confronto fra l'anno ricostruito (§4) e quello letto dalla scheda, su un campione stratificato:

| Livello inferito | Esito |
|---|---|
| `certo` | **27/27 concordano** |
| `presunto` | 26/27 concordano; 1 diverge di −1 |
| `presunto_conflitto` | **9/9 divergono, sempre di −1** |
| `ignoto` | risolti dalla scheda |

La ricostruzione regge dove dichiarava di reggere, e questa è la sua validazione esterna. Ma emergono due difetti che senza questa fonte non si sarebbero visti: sul livello `presunto` c'è circa un **4% di errore**, che su 2.505 atleti sono un centinaio di anni di nascita sbagliati; e sui casi `presunto_conflitto` la regola del massimo sbaglia **sistematicamente di un anno** — lì il minimo era la scelta corretta.

Non serve sceglierla meglio: dove la nascita è osservata, l'inferenza non viene usata.

### Cosa si sblocca

**Il Relative Age Effect torna fra le domande di ricerca.** La guida lo esclude perché «la data di nascita completa c'è solo per i professionisti». Con le schede c'è per la grande maggioranza di tutti i classificati, quindi il confronto di Voet — RAE presente fra chi non arriva, assente fra chi arriva — diventa replicabile sulla coorte italiana.

Si sbloccano inoltre l'anno di corso U23 senza dipendere da PCS, e una chiave di matching con PCS molto più forte: data esatta invece di anno presunto.

### Cosa non si sblocca

- **La nazionalità c'è ma è quasi sempre vuota** (circa il 5% delle schede). Troppo rara per identificare gli stranieri: quell'esclusione resta affidata a PCS.
- **Il numero di gare disputate resta non disponibile.** La scheda elenca i piazzamenti dal 1° al 5° posto con data, regione e nome della gara, non le partenze. Il limite ② della Sezione 3 della guida regge.

### Come è organizzata la raccolta

`scripts/03_scarica_schede.py` scarica una scheda per atleta, con pausa di 1,2 s, ripartibile, e conserva l'HTML compresso in `data/giovanile/schede.db` così da poter cambiare il parsing senza rifare le richieste. Il sito non espone un `robots.txt`.

La pipeline usa le nascite in questo ordine: **colonna della sorgente** se un giorno ci sarà → **scheda** → **inferenza**. Il primo livello oggi è vuoto ma il codice lo cerca già: quando il database di partenza esporrà la nascita, le schede diventeranno superflue senza toccare nient'altro.

---

## 10. Le date di nascita, validate contro ProCyclingStats

Il matching con PCS produce, gratis, la validazione incrociata delle date di nascita: 727 atleti hanno la data completa su entrambi i lati, raccolta da due fonti indipendenti con due parser diversi.

| | |
|---|---|
| Date identiche | **709 (97,52%)** |
| Date diverse | 18 (2,48%) |

Le 18 divergenze, per tipo:

| Tipo | N |
|---|---|
| Giorno e mese scambiati | **7** |
| Stesso mese, giorno diverso | 5 |
| Anno diverso | 3 |
| Altro | 2 |
| Stesso giorno, mese diverso | 1 |

**Solo 6 divergenze su 727 (0,83%) cambiano il trimestre di nascita**, che è la quota che tocca il Relative Age Effect. L'impatto sull'analisi è quindi trascurabile, ma il fatto che sia misurato conta più del suo essere piccolo.

### Nessuna delle due fonti è sistematicamente giusta

Sette casi sono stati verificati a mano uno per uno. Il risultato:

| Chi aveva ragione | N |
|---|---|
| ProCyclingStats | 5 |
| ciclismo.info | 2 |

Non esiste quindi una regola automatica del tipo «in caso di conflitto vince PCS». I casi vanno decisi singolarmente, e le decisioni si registrano in `data/private/manual/date_corrette.csv`, che ha la precedenza su ogni fonte automatica.

Il pattern dominante — sette casi di giorno e mese scambiati — riguarda tutti date con giorno ≤ 12, quindi ambigue fra i due ordinamenti. Non può essere un errore del nostro parser, che legge il mese per esteso dal testo italiano della scheda («Nato il 06 Febbraio 2010»): l'inversione è già nel dato di una delle due fonti.

### Un'insidia pratica del file di verifica

Il file `match_da_verificare.csv` viene scritto con date in formato `AAAA-MM-GG`, ma **aprendolo in Excel le date vengono riformattate** nel formato locale e salvate così. Dopo un giro in Excel il file non è più attendibile come dato.

Per questo `05_match_pcs.py` rilegge dal file **solo le colonne `verdetto` e `nota`**, e riscrive tutte le altre dai database. Le annotazioni scritte a mano sopravvivono a ogni riesecuzione; i dati non vengono mai riletti da lì.

---

## 11. Cosa resta da fare prima di modellare

1. ~~Risolvere a mano i candidati frammento~~ — fatto (§5): 3 fusioni applicate, il resto sono omonimi genuini.
2. **Contare gli eventi** (STEP 4) dopo il matching con PCS: professionisti totali, top-200, top-100 sulle coorti 1996-2000. È il numero che decide se la Domanda B è modellabile.
3. **Completare le schede personali** (§9) e ricalcolare l'anno di corso U23, e con esso `pct_rank` per le celle U23. Non serve più aspettare PCS.
4. ~~Decidere il trattamento del 2020~~ — fatto: resta nel dataset con `flag_stagione = 'covid'`, escluso dall'analisi principale e riportato in sensibilità. La stagione 2026 è esclusa alla fonte (`STAGIONE_MAX = 2025`) e si recupera cambiando una costante quando sarà chiusa.
