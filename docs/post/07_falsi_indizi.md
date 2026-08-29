# 7. I falsi indizi

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio
> se i dati cambiano. Prima di pubblicare: `python scripts/11_verifica_documenti.py`.
> Le affermazioni qualitative restano da rileggere a mano.
>
> **Numero chiave del post:** 96,3%.
> **Moduli:** `rae`, `contesto`.
> **Figure:** `rae_gradiente`, `contesto_confondente`.

---

Ci sono tre cose che chiunque frequenti il ciclismo giovanile vi dirà che contano.

Il mese di nascita: i ragazzi di gennaio hanno quasi un anno di sviluppo in più di quelli di
dicembre, e a quell'età si vede.

La società: chi entra in una squadra che sa lavorare arriva, chi resta in un club di paese
si perde.

La regione: nasci in Veneto o in Lombardia e hai gare tutte le domeniche, nasci altrove e ne
hai una al mese.

Tutte e tre sono ragionevoli. Due si vedono chiaramente nei dati. E nessuna delle tre
significa quello che sembra.

## La domanda

**Le cose che tutti credono contino, contano?**

## Il mese di nascita: un vantaggio che non si converte

Cominciamo dal più documentato. Fra ragazzi della stessa annata, chi è nato a gennaio ha
fino a dodici mesi di sviluppo in più di chi è nato a dicembre. Alle età più basse è
plausibilmente il fattore dominante del risultato in gara.

Prima però va tolta di mezzo una scorciatoia: **l'atteso non è il 25% per trimestre.** In
Italia si nasce di più fra maggio e settembre, e il primo trimestre è il più scarso di tutti
— il 23,95% delle nascite delle annate studiate. Confrontare con l'uniforme
sottostimerebbe l'effetto invece di gonfiarlo, e quindi è meglio farlo bene.

Fatto bene, l'effetto c'è ed è grosso:

| categoria | nati in gennaio-marzo, rispetto all'atteso |
|---|---|
| Under 15 | +39% |
| Under 17 | +30% |
| Under 19 | +15% |
| Under 23 | −1% |

A tredici anni i ragazzi nati nel primo trimestre sono **2,13 volte** quelli nati
nell'ultimo. In Under 23 il rapporto è **1,09**: praticamente sparito.

Questa è la parte del post in cui i dati parlano da soli, e c'è un dettaglio metodologico
che vale la pena notare: **questo confronto non ha bisogno di nessun dato esterno**. Sono le
stesse annate ai due estremi del percorso, quindi la stagionalità delle nascite si cancella
da sé. Anche se ci fossimo sbagliati su quale sia la distribuzione attesa, il crollo da 2,13
a 1,09 resterebbe.

E fra chi arriva? Fra i 77 professionisti il rapporto fra primo e ultimo trimestre è **1,5**,
e non si distingue dal caso.

La conclusione si scrive in una riga: **il vantaggio di essere nati a gennaio è un vantaggio
di accesso, non di talento.** Aiuta a entrare in classifica a tredici anni. Non aiuta ad
arrivare.

Che significa, girando la frase, che **chi seleziona a tredici anni sta in parte
selezionando la data di nascita** — e lo sta facendo a vuoto, perché quel vantaggio si
esaurisce da solo entro pochi anni. Non è un'accusa a nessuno: è il funzionamento normale di
una selezione fatta sul risultato, in un'età in cui il risultato dipende dallo sviluppo.

## Cambiare società: il caso da manuale

Qui il dato grezzo è spettacolare.

| cambi di società | professionisti |
|---|---|
| nessuno | **0,68%** |
| uno | 4,48% |
| due | 7,44% |
| tre | **7,32%** |

Un fattore dieci fra chi non ha mai cambiato e chi ha cambiato tre volte. Se questa tabella
finisse in un titolo di giornale, il titolo sarebbe «cambiare squadra aiuta».

C'è però una colonna che di solito non si guarda. Chi non ha mai cambiato società ha corso
**1,8 stagioni** in media. Chi ha cambiato tre volte ne ha corse **6,0**.

Non si cambia società stando fermi. Per cambiarla bisogna esserci ancora.

Il controllo consiste nel confrontare ragazzi che hanno corso lo stesso numero di stagioni,
e con quello **il gradiente quasi sparisce**: dei 6,64 punti percentuali di divario grezzo ne
resta al massimo 1,16, e solo due durate di carriera hanno abbastanza atleti in entrambi i
gruppi per essere confrontate davvero. Non è una smentita netta — con due strati non si
smentisce niente in modo netto — ma è più che sufficiente per non scrivere quel titolo.

Poi c'è la scoperta che chiude la questione, e che nessuno degli studi precedenti aveva
guardato. Non tutte le società sono attive in tutte le categorie: quando un ragazzo cambia
fascia, spesso deve cambiare squadra perché la sua non lo segue più.

| passaggio | ha cambiato società |
|---|---|
| dentro gli Esordienti | 15,8% |
| da Esordienti ad Allievi | 38,4% |
| dentro gli Allievi | 17,0% |
| da Allievi a Juniores | 77,1% |
| dentro gli Juniores | 29,0% |
| **da Juniores a Under 23** | **96,3%** |

Il passaggio da Juniores a Under 23 comporta un cambio di squadra nel **96,3% dei casi**: è
di fatto obbligatorio.

Quindi «numero di cambi di società» non misura la mobilità, e ancora meno le scelte di un
ragazzo. Misura **quanti passaggi di categoria ha attraversato**, cioè quanto lontano è
arrivato. È una variabile che descrive l'esito e sembra spiegarlo: il travestimento più
comune che esista nei dati sportivi.

## La società di partenza, e la regione

Le altre due candidate si esauriscono in fretta.

**La società da cui si parte** dice pochissimo: si va dal 2,90% di professionisti fra chi
comincia in un club che non ne aveva mai prodotti al 3,79% fra chi comincia nei migliori. Con
questi numeri la differenza non si distingue dal caso. E c'è un motivo strutturale: il 67%
dei ragazzi parte da una società che nelle coorti precedenti non aveva prodotto nessun
professionista, quindi la variabile è poco informativa già per come è fatta.

**La regione** è la più frustrante, perché è l'unica domanda a cui *non possiamo* rispondere.
La concentrazione geografica esiste ed è forte — Lombardia, Veneto e Toscana da sole
raccolgono circa il 52% dei ragazzi in classifica. Ma i tassi di professionismo per regione,
anche allargando a nove annate e 4 827 atleti, restano illeggibili: si va dal 6,32% del
Trentino Alto Adige allo 0% della Campania, e bastano due o tre ragazzi in più o in meno per
riordinare la classifica.

Quella tabella si legge come **una mappa della partecipazione, non come una graduatoria dei
vivai**.

Per fare la domanda giusta — *a parità di numero di corridori e di gare disponibili, la
regione aggiunge qualcosa?* — servirebbe sapere quanti tesserati ci sono in ogni regione.
La federazione pubblica i tesserati per categoria e le società per regione, mai i due
incrociati. Senza quel dato la domanda resta aperta, e dichiararlo è più utile che riempire
il vuoto con una classifica che non significa niente.

## La trappola

Il meccanismo è sempre lo stesso, e conviene saperlo riconoscere perché è ovunque.

Una variabile misura **quanto lontano sei arrivato**. La si osserva accanto all'esito, si
vede una correlazione forte, e la si legge come se spiegasse **quanto lontano arriverai**.

I cambi di società ne sono l'esempio perfetto: contano i passaggi di categoria, e i passaggi
di categoria sono l'esito. Ma la stessa cosa vale per il numero di stagioni corse, per il
numero di gare, per qualunque cosa richieda di essere ancora in gioco per accumularsi.

La regola pratica per difendersi: prima di credere a un gradiente, chiedersi **cosa serviva
per finire nella casella più alta**. Se serviva arrivare lontano, il gradiente non spiega
niente — lo sta solo raccontando due volte.

## Cosa se ne ricava

Il risultato negativo è utile quanto quello positivo, e va detto con la stessa convinzione:
senza queste verifiche, questo studio avrebbe pubblicato «cambiare squadra aiuta» con un
fattore dieci a sostegno, e sarebbe stato falso.

Per chi allena, restano due cose concrete. La prima: se selezionate a tredici anni, sappiate
che state in parte selezionando ragazzi nati a gennaio, e che quel vantaggio si scioglierà
da solo — provate a guardare la data di nascita accanto al piazzamento, non solo il
piazzamento. La seconda: il cambio di squadra all'arrivo in Under 23 non è un segnale di
niente. Succede a tutti.

## Il gancio

A questo punto abbiamo un quadro: cosa predice, quanto, da che età, e cosa invece è solo
apparenza.

Resta la domanda che conta davvero, che non è sui ragazzi ma su chi li guarda. **Cosa
faremmo, con questi numeri?**

---

> **Come lo sappiamo**
>
> L'atteso per trimestre viene dalle nascite mensili registrate in Italia nelle annate
> studiate (fonte Eurostat), non da una distribuzione uniforme. L'effetto è riassunto anche
> dalla V di Cramer, che scende da 0,28 in Under 15 a 0,06 in Under 23 — cioè da uno
> squilibrio evidente a uno trascurabile.
>
> Il confronto sulla mobilità a parità di stagioni corse è la cosa più delicata del post:
> stratificando, molte caselle restano con pochi atleti e solo due durate di carriera hanno
> abbastanza persone in entrambi i gruppi. È il motivo per cui la conclusione è «il
> gradiente quasi sparisce» e non «non esiste».
>
> Società e regione non entrano come variabili di controllo in nessun modello dello studio, e
> per una ragione precisa: cambiano *in risposta* ai risultati — un buon piazzamento fa
> arrivare l'offerta di una società migliore — quindi stanno sul percorso fra rendimento ed
> esito. Inserirle fra i controlli sottrarrebbe parte dell'effetto che si vuole misurare.
> Sono oggetto di studio, mai correttivi.
>
> Le percentuali regionali usano nove annate (1992-2000) invece delle cinque del resto della
> serie, perché la regione di partenza non ha bisogno della finestra stretta che serve agli
> esiti. Le celle con meno di cinque atleti non sono pubblicate.

---

## Scelte aperte per questo post

**A. Tre temi o due.** Il post ne tiene insieme tre: età relativa, mobilità, geografia. La
geografia è la più debole — è quasi solo un «non possiamo rispondere» — e si può spostare
nel post 8 fra le cose che servirebbero. **Consiglio di spostarla**: il post 7 diventa più
netto (due falsi indizi, due meccanismi diversi) e il post 8 guadagna un esempio concreto di
cosa manca.

**B. L'effetto dell'età relativa merita un post suo?** È il tema con più letteratura alle
spalle, ha una figura efficace, e la conclusione — *chi seleziona presto premia
sistematicamente chi è nato prima, e lo fa a vuoto* — è forse la più utile della serie per
chi lavora con i ragazzini. Contro: da solo è un post corto e senza tensione, perché la
risposta arriva subito. A favore: qui rischia di essere schiacciato dal caso dei cambi di
società, che è più spettacolare.

**C. Il tono sulla selezione precoce.** Il testo dice «non è un'accusa a nessuno». Si può:
(a) tenerlo così, prudente; (b) essere più diretti — la selezione a tredici anni è
misurabilmente distorta, e questo è un problema di sistema, non di singoli. La seconda è
sostenibile con i dati e più utile; costa qualche antipatia.

**D. Il numero chiave.** Il piano indica 96,3%. È il numero più memorabile del post, ma è il
numero del *falso* indizio: chi lo ricorda senza contesto potrebbe ricordarsi che «cambiare
squadra conta». Alternativa: usare come numero chiave **2,13 → 1,09**, il crollo del
vantaggio di chi nasce a gennaio, che è la conclusione vera del post.

**E. La regola pratica per riconoscere il travestimento** («chiedersi cosa serviva per
finire nella casella più alta») è la cosa più trasferibile della serie e ora sta in fondo,
nella trappola. Si può portarla in apertura e costruirci sopra tutto il post — struttura più
didattica, meno narrativa.
