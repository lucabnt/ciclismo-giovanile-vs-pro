# 4. A tredici anni si vede già qualcosa

> ⚠️ **Bozza scritta a mano. Non si rigenera.** Ogni cifra è copiata dall'analisi al momento
> della stesura e diventerà falsa in silenzio se i dati cambiano. Prima di pubblicare
> conviene eseguire `python scripts/11_verifica_documenti.py`. Sullo stile:
> [`STILE.md`](STILE.md).
>
> **Numero chiave del post:** 74%.
> **Moduli:** `punteggi`, `univariati`, `annidati`, `validazione` (foresta ed elastic net),
>   `correlazioni` (di passaggio).
> **Figure:** `punteggi_delta`, `univariati_or`, `annidati_auc`.

---

*Quarta puntata. Le prime tre hanno chiarito di chi parliamo e cosa voglia dire uscire da una
classifica; da qui in avanti provo a rispondere alla domanda per cui è nato tutto lo studio,
cioè da che età il risultato in gara dica qualcosa sul futuro.*

> 📷 **Immagine da procurare (copertina):** una volata di Esordienti ripresa di lato o da
>   dietro, gruppo compatto su una strada stretta, senza volti riconoscibili.
> *Didascalia proposta:* A tredici anni mi aspettavo di non trovare niente, e invece qualcosa
>   si vede già.
> *Testo alternativo:* Un gruppo di giovanissimi ciclisti lanciati in volata su una strada di
>   paese.

Quando ho cominciato ero convinto che a tredici anni non ci fosse niente da vedere.

Lo dice la letteratura, perché a quell'età quello che misuri è soprattutto chi si è
sviluppato prima. Lo dice il buon senso: un ragazzino di prima media che vince una gara
Esordienti sta battendo dei coetanei con un anno di pubertà in meno, non sta dimostrando di
avere il motore di un professionista. E lo sa chiunque abbia allenato, visto che i
campioncini di quell'età spariscono con una regolarità che fa quasi impressione.

Mi aspettavo insomma di trovare zero, e di poterlo dire con precisione. Sarebbe stato un
risultato utile, perché avrebbe autorizzato a smettere di selezionare a tredici anni. È
andata diversamente.

## Guardare, prima di modellare

Il modo più semplice di rispondere non richiede statistica: prendi i ragazzi che poi sono
diventati professionisti, guardi dove stavano in classifica a tredici anni e lo confronti
con dove stavano tutti gli altri.

Il piazzamento è in percentile, cioè su una scala in cui 100 è il primo della classifica, 50
è a metà e 0 è l'ultimo. Serve a rendere confrontabili stagioni e categorie che hanno un
numero diverso di partecipanti.

| a tredici anni (Under 15, primo anno) | posizione tipica |
|---|---|
| chi **non** diventerà professionista | 49° percentile |
| chi diventerà professionista | **81° percentile** |

*professionista vuol dire aver corso in una squadra di primo o secondo livello entro i
venticinque anni*

A diciotto anni la distanza si allarga ancora: da 47 a 94.

C'è un modo elegante di riassumere quanto due gruppi si separino: prendi tutte le coppie
possibili formate da un futuro professionista e da un futuro non professionista, e conti
quante volte il professionista sta davanti. A tredici anni succede nel **74% dei casi**, a
diciotto nell'89%. Secondo le soglie convenzionali di questa misura la separazione a tredici
anni è già grande, e ti confesso che non era quello che mi aspettavo di
trovare.[^p4punteggi]

> 🖼️ **Figura: `punteggi_delta.png`**
> *Didascalia proposta:* Le due curve sono i percentili mediani dei due gruppi, e il gruppo
>   si conosce solo guardando indietro: a tredici anni nessuno sapeva chi fosse chi.
> *Testo alternativo:* Due profili di percentile a confronto, uno per i futuri professionisti
>   e uno per tutti gli altri, che si allontanano con l'età.

Su questo 74% conviene essere precisi, perché due equivoci sono in agguato. Il primo: il
confronto è **fra chi era in classifica quell'anno**, non fra tutti i ragazzi. Chi a tredici
anni non ha mai fatto un punto non entra né fra i professionisti né fra gli altri, quindi la
cifra dice quanto la classifica separa dentro di sé, e non quanto separi il mondo. Il
secondo: i «professionisti» del confronto sono i **futuri** professionisti, cioè ragazzi che
a tredici anni non erano niente di particolare e che sarebbero arrivati sei o sette anni
dopo. È un confronto costruito guardando indietro, ed è l'unico modo onesto di farlo.

Se invece includi anche chi in classifica non c'era, trattando l'assenza come un rendimento
peggiore di qualunque presenza, la separazione **sale**, perché non esserci è a sua volta
un'informazione. Ne parlo nell'ultima puntata, dove metto alla prova proprio questa scelta.

## Di quanto conta, esattamente

Un modello ti permette di mettere un numero sul vantaggio, rispondendo alla domanda su
quanto conti salire di dieci posizioni percentuali.

| categoria | età | quanto moltiplica le probabilità |[^p4univariati]
|---|---|---|
| Under 15, primo anno | 13 | ×1,40 |
| Under 15, secondo anno | 14 | ×1,56 |
| Under 17, primo anno | 15 | ×1,70 |
| Under 17, secondo anno | 16 | ×1,98 |
| Under 19, primo anno | 17 | ×1,64 |
| **Under 19, secondo anno** | **18** | **×2,28** |
| Under 23, primo anno | 19 | ×1,32 |

> 🖼️ **Figura: `univariati_or.png`**
> *Didascalia proposta:* Ogni riga è un modello a sé, con l'intervallo al 95% e la scala
>   logaritmica, perché un odds ratio si legge in rapporti e non in differenze.
> *Testo alternativo:* Grafico a punti con barre di errore, un odds ratio per ogni categoria
>   e anno di categoria.

Si legge così: fra due Esordienti che differiscono di dieci posizioni percentuali, quello
davanti ha circa il 40% di probabilità in più di arrivare al professionismo; fra due
Juniores di secondo anno, quello davanti ne ha più del doppio.

Il peso del risultato cresce quindi con l'età, da 1,40 a tredici anni fino a 2,28 a
diciotto, però non in modo regolare, e le due righe che scendono meritano un'occhiata. Non
sono anomalie della prestazione ma cambi di popolazione, perché a ogni passaggio di
categoria cambia chi è rimasto nel gruppo che stai confrontando: in Under 23 i
professionisti sono già il 37% della lista. Confrontare quei numeri fra loro come se
misurassero la stessa cosa è il primo modo di sbagliare la lettura della tabella.

## Il primo anno sembra migliore del secondo, e non lo è

C'è un dettaglio che a prima vista sembra un risultato e non lo è. Te lo mostro perché è il
tipo di errore che si commette in perfetta buona fede.

Nella classifica del primo anno di ogni categoria la percentuale di futuri professionisti è
più alta che nel secondo: 6,7% contro 4,5% in Under 17, 9,7% contro 8,2% in Under 19.
Sembrerebbe che il primo anno selezioni meglio.

Le cose però stanno diversamente. Dagli Allievi in su la classifica è una sola e le due
annate ci convivono, correndo le stesse gare, e al primo anno se ne vince una minoranza:
poco più di un quarto dei posti a punti. Infatti i classificati al primo anno sono **181
contro 320** in Under 17. Comparirci è quindi molto più difficile, chi c'è è già più
selezionato, e un gruppo più selezionato contiene per forza una quota maggiore di futuri
professionisti: quel numero misura la selettività della cella, non la bontà della
previsione.

Alla domanda vera, cioè se il primo anno predica meglio del secondo, puoi rispondere
soltanto confrontando le due misure sulle stesse persone, cioè sui ragazzi presenti in
entrambe le classifiche della categoria.

| categoria | primo anno | secondo anno |[^p4univariati]
|---|---|---|
| Under 15 | 70% | **81%** |
| Under 17 | 81% | **85%** |
| Under 19 | 78% | **87%** |

*percentuale di coppie in cui il modello mette davanti quello giusto*

Il secondo anno discrimina meglio del primo in tutte le categorie, cioè esattamente il
contrario dell'impressione. Ha anche senso: al secondo anno il ragazzo corre contro i propri
pari da dodici mesi in più, e la classifica ne misura il rendimento con meno rumore.

## L'informazione non si accumula come ti aspetteresti

Qui arriva il risultato più utile del post, e per capirlo bisogna cambiare la domanda: non
quanto dica l'Under 17, ma quanto dica l'Under 17 che non fosse già nell'Under 15.

Prendo i ragazzi osservati in tutte le categorie, che sono 102, un gruppo piccolo e molto
selezionato ma l'unico su cui il confronto sia legittimo, e aggiungo una categoria alla
volta guardando quanto migliori la previsione.

| il modello conosce… | quanto ci prende |[^p4annidati]
|---|---|
| solo l'anno di nascita | 51% (cioè: nulla) |
| più l'Under 15 | 58% |
| più l'Under 17 | 66% |
| **più l'Under 19** | **81%** |
| più l'Under 23 | 82% |

> 🖼️ **Figura: `annidati_auc.png`**
> *Didascalia proposta:* Il confronto regge solo perché i 102 atleti sono sempre gli stessi:
>   cambiando gruppo a ogni passo si misurerebbe chi è rimasto, e non l'informazione aggiunta.
> *Testo alternativo:* Linea crescente della capacità predittiva a mano a mano che si
>   aggiungono categorie, con un gradino marcato in corrispondenza dell'Under 19.

Il salto è tutto in un punto solo: l'Under 19 da solo aggiunge più di tutte le categorie
precedenti messe insieme, mentre l'Under 23, che pure è la categoria più vicina al
traguardo, non aggiunge quasi nulla a chi già conosce l'Under 19.

Poteva essere una stranezza di questo sottocampione, quindi ho fatto la stessa domanda in
altri due modi completamente diversi. Una foresta casuale, cioè un algoritmo che si arrangia
da solo a trovare le combinazioni utili, ha ricevuto diciassette variabili invece di una e
ha guadagnato **1,3 punti percentuali** di capacità predittiva, con in cima alla sua
classifica di importanza proprio il piazzamento in Under 19. Una regressione penalizzata,
cioè un metodo che mette tutte le categorie in un modello solo e poi butta via quelle che
non si guadagnano il posto, ne ha tenute **2 su 8** contando anche l'anno di nascita:
l'Under 19 secondo anno e l'Under 23.[^p4confronti]

Tre strade diverse, la stessa conclusione: quasi tutta l'informazione utile sta nell'ultima
misura che hai. Le stagioni precedenti non si sommano a quella, sono in gran parte la stessa
cosa vista da più lontano.

## La lettura sbagliata

La conclusione che questo post ti invita a trarre, e che non segue, è che a tredici anni si
possa già selezionare.

Il motivo per cui non segue non ha niente a che vedere con la qualità del dato, perché il
modello a tredici anni è buono e mette davanti quello giusto in tre casi su quattro. È
l'aritmetica del gruppo su cui lo applichi a rovinare tutto: quando i professionisti sono
meno del 3%, anche un ordinamento accurato produce in maggioranza segnalazioni sbagliate. È
il tema della prossima puntata e non te lo anticipo oltre, però tieniti già adesso la
distinzione fra il predire e il bastare per decidere.

## Cosa te ne porti a casa

Il risultato a tredici anni non è rumore, e chi lo dice per prudenza ti sta dicendo una cosa
gentile e falsa: se guardi i piazzamenti dei tuoi Esordienti stai guardando qualcosa che in
media ha a che fare con il futuro.

La parte operativa, però, è l'altra. Se quasi tutta l'informazione utile sta nella misura
più recente, allora tenersi l'archivio di quello che un ragazzo faceva tre anni fa serve
molto meno di quanto si creda, perché la stagione in corso ti dice quasi tutto quello che ti
direbbe quella cartella. E se il salto vero è fra i sedici e i diciotto anni, è lì che vale
la pena guardare con attenzione: non perché prima non ci sia segnale, ma perché prima il
segnale è già dentro quello che vedrai dopo.

Fin qui però abbiamo parlato solo di livello, cioè di dove un ragazzo sta in classifica,
mentre la domanda che in società ci si fa più spesso riguarda la direzione. Meglio uno
stabile al settantacinquesimo percentile o uno che in tre anni è passato dal quarantesimo al
novantesimo? È il tema della prossima puntata.

---

> **Come lo sappiamo**
>
> Il predittore è il percentile dentro la cella `stagione × categoria × anno di categoria`,
> che rende confrontabili classifiche di lunghezza diversa. L'esito è essere arrivati a
> correre in una squadra professionistica di primo o secondo livello entro i venticinque
> anni.
>
> I modelli sono regressioni logistiche con la correzione di Firth[^p4firth], necessaria
> perché l'esito è raro, meno del 3%, e senza di essa le stime sarebbero distorte verso
> l'alto. Sono aggiustati per anno di nascita, dato che le coorti recenti hanno avuto meno
> tempo per arrivare; l'aggiustamento sposta i coefficienti di meno di 0,01, quindi il
> gradiente non è un effetto di coorte.
>
> Quello che chiamo «quanto ci prende» è l'area sotto la curva ROC, cioè la probabilità che
> il modello metta davanti il futuro professionista quando gli si dà una coppia a caso. Il
> confronto fra due modelli sulle stesse persone usa il test di DeLong[^p4delong], che tiene
> conto della correlazione fra le due misure.
>
> Il limite più serio riguarda il confronto fra categorie, che gira su 102 atleti, cioè
> quelli osservati ovunque. Sono pochi e sono sopravvissuti, visto che fra loro i
> professionisti sono il 43%, quindi di quella tabella conta la differenza fra le righe e
> non il livello.

[^p4firth]: Firth D. (1993), *Bias reduction of maximum likelihood estimates*, Biometrika
    80(1), 27-38. DOI [10.1093/biomet/80.1.27](https://doi.org/10.1093/biomet/80.1.27).
    Implementata dal pacchetto R `logistf`.

[^p4delong]: DeLong E.R., DeLong D.M., Clarke-Pearson D.L. (1988), *Comparing the areas
    under two or more correlated receiver operating characteristic curves: a nonparametric
    approach*, Biometrics 44(3), 837-845. DOI
    [10.2307/2531595](https://doi.org/10.2307/2531595). Implementato dal pacchetto R
    `pROC`.

[^p4punteggi]: Calcolo in [report/moduli/punteggi.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/punteggi.py), delta di Cliff convertito in area
    sotto la curva.

[^p4univariati]: Modelli in [R/16_univariati.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/16_univariati.R), resi da [report/moduli/univariati.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/univariati.py).

[^p4annidati]: Modelli in [R/18_annidati.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/18_annidati.R), resi da [report/moduli/annidati.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/annidati.py).

[^p4confronti]: Foresta casuale in [R/27_confronto_ml.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/27_confronto_ml.R), regressione penalizzata in
    [R/17_penalizzato.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/17_penalizzato.R).

---

## Scelte aperte per questo post

**A. Aprire con l'aspettativa smentita.** Il testo attuale apre dicendo che mi aspettavo zero
e che non è andata così, che è il modo più onesto e più coinvolgente, ma funziona soltanto
se il post 1 ha impostato quell'attesa (si veda la scelta B del post 1). Le due decisioni
vanno prese insieme, e se il post 1 non anticipa nulla questo può aprire con una scena, per
esempio un direttore sportivo che guarda una gara Esordienti.

**B. Quanto mostrare del fatto che l'informazione non si accumula.** È il risultato
metodologicamente più interessante della serie e il più difficile da raccontare, e ci sono
tre livelli possibili. Soltanto la tabella dei modelli annidati, come adesso, con le altre
due conferme in una riga ciascuna. Tutte e tre le conferme distese, con la foresta casuale
spiegata per esteso, il che è più solido ma introduce l'apprendimento automatico in un post
che non ne ha bisogno. Oppure spostare l'intero tema in un post a sé, insieme alla
validazione del post 8, cosa che sconsiglierei, perché da solo non regge un post e in fondo
alla serie nessuno lo leggerebbe.

**C. Il numero chiave.** Il piano indicava 2,28, cioè l'odds ratio a diciotto anni, ma il
numero più memorabile del post è il 74%, cioè quante volte su cento a tredici anni il futuro
professionista sta davanti, che è concreto e comprensibile senza spiegazioni. L'ho messo
come numero chiave, e la scelta si può ancora ribaltare.

**D. Come chiamare l'AUC.** Il testo la traduce in «quante volte su cento il modello mette
davanti quello giusto» e non usa mai la sigla. Le alternative sono introdurre la sigla una
volta fra parentesi, per i lettori che vorranno cercarla, oppure usare la percentuale nel
corpo e mettere le AUC vere soltanto nelle tabelle, che è più pulito ma rende il post non
confrontabile con il documento tecnico.

**E. La conseguenza pratica sull'archivio storico**, cioè che tenere i risultati di tre anni
fa serva meno di quanto si creda, è una mia deduzione, corretta ma non testata direttamente.
Si può tenere, ammorbidire o togliere: è il tipo di frase che un direttore sportivo citerà,
e conviene deciderla consapevolmente.
