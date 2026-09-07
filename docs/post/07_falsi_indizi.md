# 7. Il mese di nascita, la squadra, la regione

> ⚠️ **Bozza scritta a mano. Non si rigenera.** Ogni cifra è copiata dall'analisi al momento
> della stesura e diventerà falsa in silenzio se i dati cambiano. Prima di pubblicare
> conviene eseguire `python scripts/11_verifica_documenti.py`. Sullo stile:
> [`STILE.md`](STILE.md).
>
> **Numero chiave del post:** da 2,13 a 1,09.
> **Moduli:** `rae`, `contesto`.
> **Figure:** `rae_gradiente`, `contesto_confondente`.

---

*Settima puntata. Le precedenti hanno misurato quanto il risultato in gara predica il
professionismo; qui guardo le altre tre cose che tutti danno per scontate, cioè il mese di
nascita, la società e la regione.*

> 📷 **Immagine da procurare (copertina):** il foglio firma di partenza con la colonna dell'anno
>   di nascita accanto ai numeri di gara, fotografato in modo che i nomi non siano leggibili.
> *Didascalia proposta:* Tre cose che tutti danno per scontate: il mese di nascita, la squadra
>   e la regione. Due si vedono nei dati, e nessuna significa quello che sembra.
> *Testo alternativo:* Un foglio firma di gara con le date di nascita, ripreso da vicino.

Se frequenti il ciclismo giovanile sai benissimo che quelle tre cose contano. I ragazzi nati
a gennaio hanno quasi un anno di sviluppo in più di quelli nati a dicembre, e a quell'età si
vede. Chi entra in una squadra che sa lavorare arriva, chi resta nel club di paese si perde.
E nascere in Veneto o in Lombardia vuol dire gare tutte le domeniche, mentre altrove ne hai
una al mese.

Sono tre affermazioni ragionevoli. Due si vedono chiaramente nei dati. E nessuna delle tre
significa quello che sembra.

## Il mese di nascita, un vantaggio che non si converte

Cominciamo dal più documentato. Fra ragazzi della stessa annata, chi è nato a gennaio ha
fino a dodici mesi di sviluppo in più di chi è nato a dicembre, e alle età più basse quella
differenza è probabilmente il fattore che decide il risultato.

Prima però va tolta di mezzo una scorciatoia: l'atteso non è il 25% per trimestre. In Italia
si nasce di più fra maggio e settembre, e il primo trimestre è il più scarso di tutti, con
il 23,95% delle nascite delle annate che ho studiato. Confrontare con l'uniforme
sottostimerebbe l'effetto invece di gonfiarlo, quindi tanto vale fare il conto per bene.

Fatto per bene, l'effetto c'è ed è grosso.

| categoria | nati in gennaio-marzo, rispetto all'atteso |[^p7rae]
|---|---|
| Under 15 | +39% |
| Under 17 | +30% |
| Under 19 | +15% |
| Under 23 | −1% |

> 🖼️ **Figura: `rae_gradiente.png`**
> *Didascalia proposta:* L'atteso non è il 25% per trimestre: in Italia si nasce di più fra
>   maggio e settembre, e la figura tiene conto della stagionalità reale delle nascite.
> *Testo alternativo:* Linea discendente del rapporto fra nati nel primo e nell'ultimo
>   trimestre, da Under 15 a Under 23.

A tredici anni i ragazzi nati nel primo trimestre sono **2,13 volte** quelli nati
nell'ultimo, mentre in Under 23 il rapporto scende a **1,09**, cioè praticamente sparisce.

Qui i dati parlano da soli, e c'è un dettaglio metodologico che vale la pena notare: questo
confronto non ha bisogno di nessun dato esterno, perché riguarda le stesse annate ai due
estremi del percorso e la stagionalità delle nascite si cancella da sola. Anche se avessi
sbagliato la distribuzione attesa, il crollo da 2,13 a 1,09 resterebbe lì.

E fra chi arriva? Fra i 77 professionisti delle coorti in studio — chi ha corso in una
squadra di primo o secondo livello entro i venticinque anni — il rapporto fra primo e ultimo
trimestre è **1,5**, e non si distingue dal caso.

### E le ragazze?

Se il vantaggio di gennaio è un vantaggio di maturazione, allora fra le atlete dovrebbe
essere più debole, perché le ragazze maturano prima: a tredici anni molte hanno già
attraversato la pubertà, mentre fra i coetanei maschi la differenza di sviluppo fra chi è
nato a gennaio e chi a dicembre è al suo massimo.

È una delle poche analisi che ho potuto rifare sul femminile, perché non ha bisogno di
sapere chi è arrivato: confronta la composizione della classifica con la demografia, e le
basta la data di nascita. Nella prossima puntata c'è il resto di quello che si può dire
sulle ragazze.

| categoria | maschi | femmine |[^p7rae]
|---|---|---|
| Esordienti | **1,98** | **1,51** |
| Allievi | 1,73 | 1,20 |
| Juniores | 1,29 | 1,42 |

*rapporto fra nati nel primo e nell'ultimo trimestre, sulle stesse annate e con lo stesso
atteso demografico*

L'ipotesi regge, almeno dove i numeri sono solidi. A tredici anni lo squilibrio femminile è
sensibilmente più basso di quello maschile, e in Allieve arriva a non distinguersi più dalla
distribuzione attesa. Due cautele però sono d'obbligo: le atlete in Esordienti sono 874
contro 5 544 atleti, quindi i valori femminili ballano molto di più; e il valore in Juniores
risale invece di scendere, il che con poche centinaia di atlete è esattamente quello che il
caso produce, e non va letto come un ritorno dell'effetto.

La conclusione sta in una riga: il vantaggio di essere nati a gennaio è un vantaggio di
accesso, non di talento. Ti aiuta a entrare in classifica a tredici anni, non ti aiuta ad
arrivare. Girando la frase, chi seleziona a tredici anni sta in parte selezionando la data
di nascita, e lo sta facendo a vuoto, perché quel vantaggio si esaurisce da solo nel giro di
pochi anni. Non è un'accusa a nessuno: è il funzionamento normale di una selezione fatta sul
risultato in un'età in cui il risultato dipende dallo sviluppo.

## Cambiare società, il caso da manuale

Qui il dato grezzo è spettacolare.

| cambi di società | professionisti |[^p7contesto]
|---|---|
| nessuno | **0,68%** |
| uno | 4,48% |
| due | 7,44% |
| tre | **7,32%** |

Fra chi non ha mai cambiato e chi ha cambiato tre volte c'è un fattore dieci. Se questa
tabella finisse in un titolo di giornale, il titolo sarebbe che cambiare squadra aiuta.

C'è però una colonna che di solito nessuno guarda, quella delle stagioni corse: chi non ha
mai cambiato società ha corso **1,8 stagioni** in media, chi ha cambiato tre volte ne ha
corse 6,0. Non si cambia società stando fermi, perché per cambiarla devi esserci ancora.

Il controllo consiste nel confrontare ragazzi che abbiano corso lo stesso numero di
stagioni, e con quello il gradiente quasi sparisce: dei **6,64 punti percentuali** di
divario grezzo ne resta al massimo **1,16**, e solo due durate di carriera hanno abbastanza
atleti in entrambi i gruppi per essere confrontate davvero. Non è una smentita netta, perché
con due strati non smentisci niente in modo netto, ma basta e avanza per non scrivere quel
titolo.

> 🖼️ **Figura: `contesto_confondente.png`**
> *Didascalia proposta:* Le due serie hanno la stessa forma. Il confronto a parità di stagioni
>   corse regge però solo su due durate di carriera: abbastanza per non scrivere quel titolo, non
>   abbastanza per una smentita.
> *Testo alternativo:* Due serie di barre sovrapponibili, una per il tasso di professionismo e
>   una per le stagioni corse, in funzione del numero di cambi di società.

Poi c'è la scoperta che chiude la questione, e che nessuno degli studi precedenti aveva
guardato. Non tutte le società sono attive in tutte le categorie, per cui quando un ragazzo
cambia fascia spesso deve cambiare squadra semplicemente perché la sua non lo segue più.

| passaggio | ha cambiato società |[^p7contesto]
|---|---|
| dentro gli Esordienti | 15,8% |
| da Esordienti ad Allievi | 38,4% |
| dentro gli Allievi | 17,0% |
| da Allievi a Juniores | 77,1% |
| dentro gli Juniores | 29,0% |
| **da Juniores a Under 23** | **96,3%** |

Il passaggio da Juniores a Under 23 comporta un cambio di squadra nel **96,3% dei casi**: è
di fatto obbligatorio. Vuol dire che il numero di cambi di società non misura la mobilità, e
ancora meno le scelte di un ragazzo, ma quanti passaggi di categoria ha attraversato, cioè
quanto lontano è arrivato. È una variabile che descrive l'esito e sembra spiegarlo, ed è il
travestimento più comune nei dati sportivi.

## La società di partenza e la regione

Le altre due candidate si esauriscono in fretta.

La società da cui parti dice pochissimo: si va dal **2,90%** di professionisti fra chi
comincia in un club che non ne aveva mai prodotti al **3,79%** fra chi comincia nei
migliori, una differenza che con questi numeri non si distingue dal caso. E c'è anche una
ragione strutturale, cioè che il **67%** dei ragazzi parte da una società che nelle coorti
precedenti non aveva prodotto nemmeno un professionista, il che rende la variabile poco
informativa già per come è fatta.

La regione è la più frustrante, perché è l'unica domanda a cui non posso rispondere. La
concentrazione geografica esiste ed è forte, visto che Lombardia, Veneto e Toscana da sole
raccolgono circa il **52%** dei ragazzi in classifica, ma i tassi di professionismo per
regione restano illeggibili anche allargando a nove annate e **4 827 atleti**: si va dal
6,32% del Trentino Alto Adige allo 0% della Campania, e bastano due o tre ragazzi in più o
in meno per riordinare la classifica. Quella tabella si legge come una mappa della
partecipazione, non come una graduatoria dei vivai.

Per fare la domanda giusta, cioè se a parità di corridori e di gare disponibili la regione
aggiunga qualcosa, servirebbe sapere quanti tesserati ci sono in ogni regione. Quel dato non
è pubblicamente disponibile: esistono i tesserati per categoria e le società per regione,
non i due incrociati. Senza, la domanda resta aperta, e dichiararlo è più utile che riempire
il vuoto con una classifica che non significa niente.[^p7contesto]

## La lettura sbagliata, e come riconoscerla da solo

Il meccanismo è sempre lo stesso, e ti conviene imparare a riconoscerlo perché lo ritrovi
dappertutto. Una variabile misura quanto lontano sei arrivato; la osservi accanto all'esito;
vedi una correlazione forte; e la leggi come se spiegasse quanto lontano arriverai.

I cambi di società ne sono l'esempio perfetto, perché contano i passaggi di categoria e i
passaggi di categoria sono l'esito. Ma vale anche per il numero di stagioni corse, per il
numero di gare e per qualunque cosa che, per accumularsi, richieda di essere ancora in
gioco.

La regola pratica per difenderti è chiederti, prima di credere a un gradiente, cosa servisse
per finire nella casella più alta. Se serviva arrivare lontano, quel gradiente non sta
spiegando niente: sta raccontando l'esito due volte.

## Cosa te ne porti a casa

Il risultato negativo è utile quanto quello positivo, e lo dico con la stessa convinzione:
senza queste verifiche avrei pubblicato che cambiare squadra aiuta, con un fattore dieci a
sostegno, e sarebbe stato falso.

Se alleni, restano due cose concrete. La prima è che, selezionando a tredici anni, stai in
parte selezionando ragazzi nati a gennaio, e che quel vantaggio si scioglierà da solo: prova
a guardare la data di nascita accanto al piazzamento, non solo il piazzamento. La seconda è
che il cambio di squadra all'arrivo in Under 23 non è il segnale di niente, perché capita a
tutti.

A questo punto il quadro c'è: cosa predice, quanto, da che età, e cosa invece è solo
apparenza. Prima di tirare le somme resta però una domanda che mi hanno fatto ogni volta che
ho raccontato questo lavoro, e a cui la prossima puntata è dedicata per intero: e le
ragazze?

---

> **Come lo sappiamo**
>
> L'atteso per trimestre viene dalle nascite mensili registrate in Italia nelle annate
> studiate, fonte Eurostat, e non da una distribuzione uniforme. L'effetto è riassunto anche
> dalla V di Cramer, che scende da 0,28 in Under 15 a 0,06 in Under 23, cioè da uno
> squilibrio evidente a uno trascurabile.
>
> Il confronto sulla mobilità a parità di stagioni corse è la cosa più delicata del post,
> perché stratificando molte caselle restano con pochi atleti e soltanto due durate di
> carriera hanno abbastanza persone in entrambi i gruppi: è il motivo per cui la conclusione
> è che il gradiente quasi sparisca e non che non esista.
>
> Società e regione non entrano come variabili di controllo in nessun modello dello studio,
> e per una ragione precisa: cambiano in risposta ai risultati, visto che un buon
> piazzamento fa arrivare l'offerta di una società migliore, e stanno quindi sul percorso
> fra rendimento ed esito. Inserirle fra i controlli sottrarrebbe parte dell'effetto che si
> vuole misurare, per cui sono oggetto di studio e mai correttivi.
>
> Le percentuali regionali usano nove annate, dal 1992 al 2000, invece delle cinque del
> resto della serie, perché la regione di partenza non ha bisogno della finestra stretta che
> serve agli esiti. Le celle con meno di cinque atleti non sono pubblicate.

[^p7rae]: Calcolo in [report/moduli/rae.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/rae.py).
    Le nascite attese vengono da Eurostat, tavola `demo_fmonth` (*Live births by month*),
    scaricata da [scripts/07_riferimenti.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/scripts/07_riferimenti.py):
    <https://ec.europa.eu/eurostat/databrowser/view/demo_fmonth/default/table>.

[^p7contesto]: Calcolo in [report/moduli/contesto.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/contesto.py).

---

## Scelte aperte per questo post

**A. Tre temi o due.** Il post ne tiene insieme tre, cioè età relativa, mobilità e geografia,
e la geografia è il più debole, perché si riduce quasi a un «non possiamo rispondere». Si
può spostarlo nel post 8, fra le cose che servirebbero, e lo consiglierei: il post 7
diventerebbe più netto, con due falsi indizi e due meccanismi diversi, e il post 8
guadagnerebbe un esempio concreto di cosa manchi.

**B. L'effetto dell'età relativa merita un post suo?** È il tema con più letteratura alle
spalle, ha una figura efficace, e la conclusione, cioè che chi seleziona presto premi
sistematicamente chi è nato prima e lo faccia a vuoto, è forse la più utile della serie per
chi lavora con i ragazzini. Contro questa scelta gioca il fatto che da solo sarebbe un post
corto e senza tensione, perché la risposta arriva subito; a favore, il fatto che qui rischi
di essere schiacciato dal caso dei cambi di società, che è più spettacolare.

**C. Il tono sulla selezione precoce.** Il testo dice che non è un'accusa a nessuno. Si può
tenere questa prudenza oppure essere più diretti, perché la selezione a tredici anni è
misurabilmente distorta e questo è un problema di sistema più che di singoli: la seconda
strada è sostenibile con i dati, più utile, e costa qualche antipatia.

**D. Il numero chiave.** Il piano indicava 96,3%, che è il numero più memorabile del post ma
appartiene al falso indizio, per cui chi lo ricordasse senza contesto si porterebbe a casa
l'idea che cambiare squadra conti. Ho messo come numero chiave il crollo da 2,13 a 1,09, che
è la conclusione vera del post; la scelta si può ribaltare.

**E. La regola pratica per riconoscere il travestimento**, cioè chiedersi cosa servisse per
finire nella casella più alta, è la cosa più trasferibile della serie e ora sta in fondo. La
si può portare in apertura e costruirci sopra tutto il post, ottenendo una struttura più
didattica e meno narrativa.
