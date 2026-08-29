# 4. A tredici anni si vede già qualcosa

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio
> se i dati cambiano. Prima di pubblicare: `python scripts/11_verifica_documenti.py`.
> Le affermazioni qualitative restano da rileggere a mano.
>
> **Numero chiave del post:** 2,28.
> **Moduli:** `punteggi`, `univariati`, `annidati`, `validazione` (foresta ed elastic net),
> `correlazioni` (di passaggio).
> **Figure:** `punteggi_delta`, `univariati_or`, `annidati_auc`.

---

Quando abbiamo cominciato, la previsione ragionevole era che a tredici anni non ci fosse
niente da vedere.

Lo dice la letteratura: a quell'età quello che si misura è soprattutto **chi si è sviluppato
prima**. Lo dice il buon senso: un ragazzo di prima media che vince una gara Esordienti sta
battendo dei coetanei con un anno di pubertà in meno, non sta dimostrando di avere un motore
da professionista. E lo dice l'esperienza di chiunque abbia allenato: i campioncini di
quell'età spariscono con una regolarità che fa quasi impressione.

Ci aspettavamo di trovare zero, e di poterlo dire con precisione. Un bello zero ben
misurato è un risultato utile: autorizza a smettere di selezionare a tredici anni.

Non è andata così.

## La domanda

**Da che età il risultato in gara comincia a dire qualcosa sul futuro?**

## Prima cosa: guardare, senza modelli

Il modo più semplice di rispondere non richiede statistica. Si prendono i ragazzi che poi
sono diventati professionisti, si guarda dove stavano in classifica a tredici anni, e si
confronta con dove stavano tutti gli altri.

Il piazzamento è espresso in **percentile**: 100 è il primo della classifica, 50 è a metà, 0
è ultimo. Serve a rendere confrontabili stagioni e categorie che hanno un numero diverso di
partecipanti.

| a tredici anni (Under 15, primo anno) | posizione tipica |
|---|---|
| chi **non** diventerà professionista | 49° percentile |
| chi diventerà professionista | **81° percentile** |

A diciotto anni, la distanza si allarga: 47 contro 94.

C'è un modo elegante di riassumere quanto due gruppi si separano. Si prendono tutte le
coppie possibili — un futuro professionista e un futuro non professionista — e si conta
quante volte il professionista sta davanti. A tredici anni succede in circa il **74% dei
casi**. A diciotto, nell'**89%**.

Le soglie convenzionali di questa misura dicono una cosa che non ci aspettavamo: la
separazione a tredici anni è già **grande**. Non trascurabile, non piccola. Grande.

## Poi: di quanto, esattamente

Un modello permette di mettere un numero sul vantaggio. La domanda è: quanto conta salire di
dieci posizioni percentuali?

| categoria | età | quanto moltiplica le probabilità |
|---|---|---|
| Under 15, primo anno | 13 | ×1,40 |
| Under 15, secondo anno | 14 | ×1,56 |
| Under 17, primo anno | 15 | ×1,70 |
| Under 17, secondo anno | 16 | ×1,98 |
| Under 19, primo anno | 17 | ×1,64 |
| **Under 19, secondo anno** | **18** | **×2,28** |
| Under 23, primo anno | 19 | ×1,32 |

Da leggere così: fra due Esordienti che differiscono di dieci posizioni percentuali, quello
davanti ha circa il 40% di probabilità in più di arrivare al professionismo; fra due
Juniores di secondo anno, quello davanti ne ha più del doppio.

Il peso del risultato cresce con l'età — 1,40 a tredici anni, 2,28 a diciotto — ma non in
modo regolare, e le due righe che scendono meritano attenzione. Non sono anomalie della
prestazione: sono cambi di popolazione. A ogni passaggio di categoria cambia chi è rimasto
nel gruppo che si sta confrontando, e in Under 23 i professionisti sono già il 37% della
lista. Confrontare quei numeri fra loro come se misurassero la stessa cosa è il primo modo
di sbagliare la lettura di questa tabella.

## Il primo anno o il secondo?

C'è un dettaglio che a prima vista sembra un risultato e non lo è, e vale la pena mostrarlo
perché è il tipo di errore che si commette in buona fede.

Nella classifica del **primo** anno di ogni categoria, la percentuale di futuri
professionisti è più alta che nel secondo: 6,7% contro 4,5% in Under 17, 9,7% contro 8,2% in
Under 19. Sembra che il primo anno selezioni meglio.

Non è così. Le classifiche del primo anno sono **molto più corte** — in Under 17, 181
classificati contro 320 — e in una lista più corta entrare è più difficile. Chi c'è è già
più selezionato, e un gruppo più selezionato contiene per forza una quota maggiore di futuri
professionisti. Quel numero misura la selettività della lista, non la bontà della previsione.

La domanda giusta si risponde solo confrontando le due misure **sulle stesse persone**: i
ragazzi presenti in entrambe le classifiche della categoria.

| categoria | primo anno | secondo anno |
|---|---|---|
| Under 15 | 70% | **81%** |
| Under 17 | 81% | **85%** |
| Under 19 | 78% | **87%** |

*percentuale di coppie in cui il modello mette davanti quello giusto*

**Il secondo anno discrimina meglio in tutte le categorie**, ed è il contrario
dell'impressione. Ha anche senso: al secondo anno il ragazzo corre contro i propri pari da
dodici mesi in più, e la classifica ne misura il rendimento con meno rumore.

## La cosa che non ci aspettavamo: non si accumula

Qui arriva il risultato più utile del post, e per capirlo bisogna cambiare domanda. Non
«quanto dice l'Under 17?», ma **«quanto dice l'Under 17 che non fosse già nell'Under 15?»**.

Si prendono i ragazzi osservati in tutte le categorie — sono 102, un gruppo piccolo e molto
selezionato, ma è l'unico modo per confrontare mele con mele — e si aggiunge una categoria
alla volta, guardando quanto migliora la previsione.

| il modello conosce… | quanto ci prende |
|---|---|
| solo l'anno di nascita | 51% (cioè: nulla) |
| + Under 15 | 58% |
| + Under 17 | 66% |
| **+ Under 19** | **81%** |
| + Under 23 | 82% |

Il salto è tutto in un punto solo: **l'Under 19 aggiunge da solo più di tutte le categorie
precedenti messe insieme**. E l'Under 23, che pure è la categoria più vicina al traguardo,
non aggiunge quasi nulla a chi già conosce l'Under 19.

Poteva essere un caso di questo particolare sottocampione, quindi abbiamo chiesto la stessa
cosa in altri due modi completamente diversi.

Una **foresta casuale** — un algoritmo di apprendimento automatico che si arrangia da solo a
trovare le combinazioni utili — ha ricevuto diciassette variabili invece di una, e ha
guadagnato **1,3 punti percentuali** di capacità predittiva. Con quindici predittori in più.
E in cima alla sua classifica di importanza ha messo esattamente il piazzamento in Under 19.

Una **regressione penalizzata** — un metodo che mette tutte le categorie in un modello solo e
poi butta via quelle che non si guadagnano il posto — ne ha tenute **2 su 8** — le sette categorie
più l'anno di nascita — e sono Under 19 secondo anno e Under 23. Tutte le altre
azzerate.

Tre strade diverse, la stessa conclusione: **quasi tutta l'informazione utile sta
nell'ultima misura disponibile**. Le stagioni precedenti non si sommano a quella; sono in
gran parte la stessa cosa vista da più lontano.

## La trappola

La lettura sbagliata di questo post è: *«allora a tredici anni si può già selezionare»*.

Non segue, e il motivo non ha niente a che vedere con la qualità del dato. Il modello a
tredici anni è buono: mette davanti quello giusto in tre casi su quattro. È l'aritmetica
del gruppo su cui lo si applica che rovina tutto — quando i professionisti sono meno del 3%,
anche un ordinamento accurato produce in maggioranza segnalazioni sbagliate.

È il tema del prossimo post e non lo anticipo oltre, ma vale la pena tenere già adesso la
distinzione: **«predice» e «basta per decidere» sono due frasi diverse.**

## Cosa se ne ricava

Il risultato agonistico a tredici anni **non è rumore**. Chi lo dice per prudenza dice una
cosa gentile e falsa. Chi guarda i piazzamenti dei propri Esordienti sta guardando qualcosa
che, in media, ha a che fare con il futuro.

Ma la parte operativa è l'altra. Se quasi tutta l'informazione utile sta nella misura più
recente, allora **tenere un archivio di quello che un ragazzo faceva tre anni fa serve
molto meno di quanto si creda**. La cartella con i risultati dai tredici anni in poi non è
una miniera: la stagione in corso dice quasi tutto quello che quella cartella direbbe.

E se il salto vero è fra i sedici e i diciotto anni, è lì che vale la pena guardare con
attenzione — non perché prima non ci sia segnale, ma perché prima il segnale è già dentro
quello che si vedrà dopo.

## Il gancio

Fin qui abbiamo parlato di livello: dove sta un ragazzo in classifica. Ma la domanda che in
società si fa più spesso è un'altra, e riguarda la direzione.

Meglio uno stabile al settantacinquesimo percentile, o uno che in tre anni è passato dal
quarantesimo al novantesimo?

---

> **Come lo sappiamo**
>
> Il predittore è il percentile dentro la cella `stagione × categoria × anno di categoria`,
> che rende confrontabili classifiche di lunghezza diversa. L'esito è essere arrivati a
> correre in una squadra professionistica di primo o secondo livello entro i venticinque
> anni.
>
> I modelli sono regressioni logistiche con la correzione di Firth, che serve perché l'esito
> è raro — meno del 3% — e senza di essa le stime sarebbero distorte verso l'alto. Sono
> aggiustati per anno di nascita: le coorti recenti hanno avuto meno tempo per arrivare.
> L'aggiustamento sposta i coefficienti di meno di 0,01, quindi il gradiente non è un effetto
> di coorte.
>
> «Quanto ci prende» è l'area sotto la curva ROC, cioè la probabilità che il modello metta
> davanti il futuro professionista quando gli si dà una coppia a caso. Il confronto fra due
> modelli sulle stesse persone usa il test di DeLong, che tiene conto della correlazione fra
> le due misure.
>
> Il limite più serio: il confronto fra categorie gira su **102 atleti**, quelli osservati
> ovunque. Sono pochi e sono sopravvissuti — fra loro i professionisti sono il 43% — quindi
> di quella tabella conta la *differenza fra righe*, non il livello.

---

## Scelte aperte per questo post

**A. Aprire con l'aspettativa smentita?** Il testo attuale apre dicendo «ci aspettavamo
zero, non è andata così». È il modo più onesto e più coinvolgente, ma **funziona solo se il
post 1 ha impostato quell'attesa** (vedi la scelta B del post 1). Le due decisioni vanno
prese insieme. Se il post 1 non anticipa nulla, questo può aprire con una scena: un
direttore sportivo che guarda una gara Esordienti.

**B. Quanto mostrare del «non si accumula».** È il risultato metodologicamente più
interessante della serie e il più difficile da raccontare. Tre livelli possibili:

1. **solo la tabella dei modelli annidati** (come ora), con le altre due conferme in una
   riga ciascuna;
2. **tutte e tre le conferme distese**, con la foresta casuale spiegata: più solido, ma
   introduce l'apprendimento automatico in un post che non ne ha bisogno;
3. **spostare tutto il tema in un post a sé**, insieme alla validazione del post 8.
   Sconsigliato: da solo non regge un post e in fondo alla serie nessuno lo leggerebbe.

**C. Il numero chiave.** Il piano indica 2,28 (l'odds ratio a diciotto anni). Ma il numero
più memorabile del post è probabilmente **«grande a tredici anni»**, che non è una cifra.
Alternativa: usare come numero chiave il **74%** — quante volte su cento, a tredici anni, il
futuro professionista sta davanti — che è concreto e comprensibile senza spiegazioni.
**Consiglio questa.**

**D. Come chiamare l'AUC.** Il testo la traduce in «quante volte su cento il modello mette
davanti quello giusto» e non usa mai la sigla. Alternative: introdurre la sigla una volta
fra parentesi, per i lettori che vorranno cercarla; oppure usare la percentuale nel corpo e
mettere le AUC vere solo nelle tabelle. La seconda è più pulita ma rende il post non
confrontabile con il documento tecnico.

**E. La conseguenza pratica sull'archivio storico** («tenere i risultati di tre anni fa
serve meno di quanto si creda») è una mia deduzione, corretta ma non testata direttamente.
Da tenere, ammorbidire o togliere: è il tipo di frase che un direttore sportivo citerà, e
va decisa consapevolmente.
