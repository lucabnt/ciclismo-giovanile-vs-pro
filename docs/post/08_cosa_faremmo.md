# 8. Cosa faremmo con questi numeri

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio se
> i dati cambiano. Prima di pubblicare conviene eseguire
> `python scripts/11_verifica_documenti.py`. Sullo stile: [`STILE.md`](STILE.md).
>
> **Gancio del post:** «chi seguire, non chi lasciare andare».
> **Moduli:** `validazione`, più i limiti dichiarati in tutte le sezioni.
> **Figure:** `validazione_sensibilita`.

---

*Ultima puntata. Le sette precedenti hanno misurato quanto il risultato giovanile predica il
professionismo; qui provo a dirti cosa farne, e prima ancora quanto puoi fidarti di quello che
hai letto finora.*

Torniamo al ragazzo di tredici anni del primo post, quello che ha appena vinto la sua prima
gara. La domanda era cosa si potesse dire del suo futuro, e adesso una risposta c'è, che posso
darti per intero senza sconti in nessuna delle due direzioni.

Sì, qualcosa si vede già: il suo risultato non è rumore, perché a tredici anni la distanza fra
chi arriverà e chi no è già netta, e dirti il contrario per prudenza sarebbe gentile e falso.
No, non basta per decidere: se quel ragazzo è fra i migliori d'Italia della sua età, nove volte
su dieci non diventerà professionista, e se non lo è la cosa non vuol dire granché, visto che
due futuri professionisti su tre a tredici anni in quella lista non ci sono. E la cosa più
utile che i dati hanno da dire non riguarda lui, ma chi lo guarda.

## Prima però: quanto puoi fidarti

È la domanda che andrebbe fatta a ogni studio e che quasi nessuno si fa. Un modello misurato
sugli stessi dati con cui l'hai costruito si giudica da solo, e si giudica bene, per cui
servono tre verifiche. Te le riporto anche se sono noiose, perché sono quello che distingue un
risultato da un'opinione con dei numeri attaccati.

La prima chiede se il modello si stia illudendo. Lo ricostruisco **500 volte** su campioni
estratti a caso e misuro ogni volta di quanto si sopravvaluta: la risposta è **0,001** di
capacità predittiva, contro una soglia di allarme convenzionale cinquanta volte più grande.
Non è fortuna, è quello che succede quando usi modelli con due o tre parametri su centinaia di
persone. La tentazione, con dati longitudinali su migliaia di ragazzi, sarebbe stata costruire
modelli ricchi, e il prezzo l'avrei pagato qui.

La seconda chiede se funzioni su ragazzi che il modello non ha mai visto. Addestro sulle annate
più vecchie e verifico sulle più recenti, che poi è il modo in cui lo useresti davvero: la
capacità predittiva non cala, semmai sale, anche se le annate di verifica contengono soltanto
**27 casi** e su quei numeri le stime ballano parecchio. Quello che volevo escludere, cioè un
crollo, non si vede.

La terza è la più importante, perché diverse decisioni di questo studio erano difendibili ma
non obbligate: cosa conti come professionismo, entro quale età, dove mettere la soglia del
top. Le ho cambiate tutte, una alla volta, e il numero di professionisti passa **da 26 a 151**
a seconda della definizione, mentre la capacità di distinguerli oscilla in tutto di **0,069**,
cioè sette centesimi. Spostare la finestra d'età da ventiquattro a ventisei anni non cambia
praticamente nulla, perché quasi tutti i passaggi avvengono prima. Detto in modo diretto:
cambiando le definizioni cambia moltissimo chi conta come arrivato, e quasi niente quanto il
rendimento giovanile lo distingua. Le conclusioni della serie non poggiano sulle mie scelte.

## Se alleni

Il risultato conta, e conta da subito. Non è una licenza a selezionare, come vedrai fra poco,
ma è una licenza a guardare: quello che vedi in gara a tredici anni ha a che fare con il
futuro più di quanto ci abbia a che fare qualunque test di laboratorio, e su questo la
letteratura internazionale è quasi unanime.

Il miglioramento conta quanto il livello, ma solo sopra una certa quota. Un ragazzo di metà
classifica che sale ha probabilità circa tre volte più alte di un ragazzo forte che sta
calando, mentre un ragazzo del terzo più basso che sale resta dov'è: il livello è una
condizione, il miglioramento un moltiplicatore.

L'uscita dalla classifica non è un giudizio, perché quasi un terzo di chi sparisce ricompare e
perché al cambio di categoria la lista si dimezza per ragioni che non riguardano i ragazzi. Se
usi la presenza in classifica come segnale, tieni presente che al primo anno di ogni categoria
quel segnale è molto più severo del solito.

Il momento in cui intervenire sulla ritenzione, infine, è il passaggio di fascia, perché lì si
concentra il **77%** delle uscite ed è lì che un ragazzo che sta facendo esattamente quello che
deve smette di ricevere riscontri.

## Se selezioni

Qualunque soglia scegli, la maggioranza dei selezionati non arriverà. Nel caso migliore, cioè
a diciotto anni prendendo il dieci per cento più forte, poco più della metà dei prescelti non
diventerà professionista, e a tredici anni sono nove su dieci. Non è un difetto del criterio,
è quello che succede a qualunque criterio applicato a un esito che riguarda il 3% delle
persone.

Ne segue che il criterio serve a decidere chi guardare e non chi escludere, ed è la conclusione
pratica di tutta la serie: la classifica giovanile è uno strumento ragionevole per decidere chi
seguire e uno strumento pessimo per decidere chi lasciare andare. Le due decisioni non sono
simmetriche, perché seguire un ragazzo in più ti costa poco, mentre lasciarne andare uno ti
costa quanto valeva quel ragazzo, e sbaglieresti spesso.

E diffida dei gradienti spettacolari: prima di credere che una variabile spieghi qualcosa,
chiediti cosa servisse per finire nella casella più alta, perché se serviva arrivare lontano
quella variabile non ti sta spiegando l'esito, te lo sta raccontando due volte.

## Se hai un figlio in bici

Non c'è fretta. Nessuno diventa professionista prima dei diciannove anni, è un regolamento, e
il passaggio avviene in genere fra i ventuno e i ventitré: tutto quello che succede prima è
preparazione, non verdetto.

Sparire dalla classifica a sedici anni non è una condanna, visto che metà dei classificati al
secondo anno di Allievi non c'era al primo.

E se tuo figlio è nel dieci per cento migliore d'Italia a diciotto anni, ha circa una
probabilità su tre: moltissimo rispetto alla media, e meno di una promessa.

## Cosa non possiamo sapere

Questa è la parte che ti dà la misura di tutto il resto.

Nessuna fonte pubblica altezza, peso, specialità, allenamento o numero di gare corse, per cui
di ogni ragazzo so dove è arrivato e non come ci è arrivato, e nemmeno quante volte ci ha
provato. Ogni conclusione di questa serie vale quindi a parità di ciò che la classifica
registra, che è molto meno di quello che un allenatore vede da bordo strada.

Di chi va oltre il professionismo non so quasi niente, perché il rendimento giovanile predice
l'ingresso e poi si ferma: sui gradini successivi posso dire che non si vede un effetto, non
che non ce ne sia uno, e i ragazzi arrivati fra i primi cento al mondo sono otto.

Delle ragazze non so niente, perché tutto questo studio riguarda i maschi. La stessa analisi
sul femminile richiederebbe di cambiare un parametro, ma non l'ho fatta, e comunque non sarebbe
la stessa analisi: la categoria Under 23 femminile non esiste e le atlete in classifica sono un
decimo degli atleti, per cui verrebbe fuori uno studio descrittivo. Che però, sull'effetto
dell'età relativa, sarebbe il primo al mondo.

E non so se la regione conti. La federazione ha il dato che servirebbe, cioè i tesserati per
anno, regione e categoria, e non lo pubblica: con quello si potrebbe finalmente chiedere se a
parità di corridori un territorio aggiunga qualcosa. È la richiesta più concreta che questa
serie possa fare a chi i dati li ha.

## E allora?

Il ragazzo di tredici anni ha vinto la sua prima gara, e la domanda era cosa potessimo dirgli.

Che quel risultato dice davvero qualcosa, e fingere di no sarebbe disonesto. Che nove volte su
dieci non basterà, e che questo non è un giudizio su di lui ma la forma del problema. Che il
tempo per capirlo è lungo, sei o sette anni, e che nel frattempo sparire da una classifica non
vuol dire niente.

E che la cosa più importante che questi dati hanno da dire non riguarda lui, ma chi, guardando
la stessa classifica, decide di smettere di guardarlo.

---

> **Come lo sappiamo**
>
> La correzione dell'ottimismo usa 500 ricampionamenti bootstrap con la procedura di Harrell,
> cioè si ristima il modello su ogni campione estratto e si misura quanto si giudichi meglio di
> quanto sia. La pendenza di calibrazione, che dice se le probabilità previste siano nella
> scala giusta, vale fra **1,01** e 1,02, cioè è corretta.
>
> La verifica temporale addestra sulle annate 1996-1998 e misura su quelle 1999-2000, mentre
> la verifica di sensibilità rifà l'analisi principale con tre definizioni di professionismo,
> tre finestre d'età e cinque soglie di top.
>
> Tutti i numeri di questa serie si rigenerano con un comando, e il documento tecnico completo,
> con i metodi, gli intervalli di confidenza e i limiti sezione per sezione, è pubblico. I post
> no, perché sono scritti a mano, ed è la ragione per cui ogni loro cifra viene confrontata con
> l'archivio dei risultati prima della pubblicazione.

---

## Scelte aperte per questo post

**A. Il gancio finale.** Il piano assegna a ogni post un numero chiave e per l'ultimo non ne
prevedeva nessuno. I candidati numerici erano 0,069, cioè quanto oscilli la capacità
predittiva cambiando tutte le definizioni, che sostiene la fiducia nel resto ma è astratto,
oppure il passaggio da 26 a 151 professionisti a seconda di come li si conti, che dice la
stessa cosa dal lato opposto ed è più concreto. Ho scelto invece una frase, «chi seguire, non
chi lasciare andare», perché l'ultimo post chiude una narrazione e una frase regge meglio di
una cifra; la scelta si può ribaltare.

**B. Quanto spazio dare alla validazione.** Ora apre il post e occupa un quarto dello spazio,
ed è la parte meno leggibile ma quella che autorizza tutto il resto. Le alternative sono
lasciarla in apertura come adesso, con l'argomento che al lettore sia dovuta, oppure spostarla
in fondo, subito prima del riquadro, come appendice per chi voglia controllare. Ridurla a tre
frasi rimandando al documento tecnico la sconsiglierei, perché questa è probabilmente l'unica
serie di post sul ciclismo giovanile in cui qualcuno abbia verificato che le proprie
conclusioni non dipendano dalle proprie definizioni, e vale la pena dirlo.

**C. Il femminile.** Il post lo cita fra i limiti in poche righe. Si può lasciarlo così,
trasformarlo in un annuncio esplicito della prossima serie, se c'è l'intenzione di farla,
oppure espanderlo in un riquadro spiegando che sull'effetto dell'età relativa sarebbe il primo
studio al mondo: quest'ultima è la più interessante ma sposta il finale.

**D. La richiesta alla federazione.** Ora è una riga fra i limiti, ma se la serie ambisce ad
avere un effetto pratico quella richiesta può diventare la chiusura del post, al posto del
ritorno al ragazzo di tredici anni. Le due chiuse sono incompatibili, perché una è civile e
l'altra narrativa: il piano prevede la narrativa e concordo, ma la scelta va fatta
consapevolmente.

**E. La struttura per destinatari**, cioè se alleni, se selezioni, se hai un figlio, è chiara
ma somiglia a un elenco di raccomandazioni. L'alternativa è un'unica narrazione che segua una
decisione concreta, per esempio una società che debba scegliere dieci ragazzi su cento,
facendo emergere le stesse conclusioni dal caso: più coinvolgente, più lunga e più difficile da
scrivere bene.
