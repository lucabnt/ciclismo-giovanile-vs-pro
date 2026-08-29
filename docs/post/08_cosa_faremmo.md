# 8. Cosa faremmo con questi numeri

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio
> se i dati cambiano. Prima di pubblicare: `python scripts/11_verifica_documenti.py`.
> Le affermazioni qualitative restano da rileggere a mano.
>
> **Numero chiave del post:** da decidere (vedi le scelte aperte).
> **Moduli:** `validazione`, più i limiti dichiarati in tutte le sezioni.
> **Figure:** `validazione_sensibilita`.

---

Torniamo al ragazzo di tredici anni del primo post, quello che ha appena vinto la sua prima
gara.

Sette post fa la domanda era: cosa possiamo dire del suo futuro? Adesso c'è una risposta, e
si può dare per intero, senza sconti in nessuna delle due direzioni.

**Sì, si vede già qualcosa.** Il suo risultato non è rumore: a tredici anni la distanza fra
chi arriverà e chi no è già netta, e chi sostiene il contrario per prudenza dice una cosa
gentile e falsa.

**No, non basta per decidere.** Se quel ragazzo è fra i migliori d'Italia della sua età,
nove volte su dieci non diventerà professionista. E se non lo è, non vuol dire granché: due
futuri professionisti su tre, a tredici anni, in quella lista non ci sono.

**E la cosa più utile che i dati dicono non riguarda lui, ma chi lo guarda.**

## Prima però: quanto ci si può fidare

È la domanda che andrebbe fatta a ogni studio, e che quasi nessuno si fa. Un modello
misurato sugli stessi dati con cui è stato costruito si giudica da solo, e si giudica bene.
Serve verificare tre cose, e le riportiamo anche se sono noiose, perché è quello che
distingue un risultato da un'opinione con dei numeri attaccati.

**Il modello si sta illudendo?** Si ricostruisce **500 volte** su campioni estratti a
caso e si misura ogni volta di quanto si sopravvaluta. La risposta è **0,001** di
capacità predittiva, contro una soglia di allarme convenzionale cinquanta
volte più grande. Non è fortuna: è quello che succede quando si usano modelli con due o tre
parametri su centinaia di persone. La tentazione, con dati longitudinali su migliaia di
ragazzi, sarebbe stata costruire modelli ricchi. Il prezzo si sarebbe pagato qui.

**Funziona su ragazzi che il modello non ha mai visto?** Si addestra sulle annate più
vecchie e si verifica sulle più recenti, che è anche il modo in cui verrebbe usato davvero.
La capacità predittiva **non cala** — semmai sale, anche se le annate di verifica contengono
solo 27 casi e su quei numeri le stime ballano. Quello che si voleva escludere, un crollo,
non c'è.

**Le conclusioni dipendono dalle scelte che abbiamo fatto?** È la verifica più importante,
perché diverse decisioni di questo studio erano difendibili ma non obbligate. Cosa conta
come professionismo? Entro quale età? Dove si mette la soglia del «top»?

Le abbiamo cambiate tutte, una alla volta. Il numero di professionisti passa da **26 a 151**
a seconda della definizione — una differenza enorme — e la capacità di distinguerli oscilla
in tutto di **0,069**, sette centesimi. Spostare la finestra d'età da ventiquattro a ventisei anni
non cambia praticamente nulla, perché quasi tutti i passaggi avvengono prima.

Detto in modo diretto: **cambiando le definizioni cambia moltissimo chi conti come arrivato,
e quasi niente quanto il rendimento giovanile lo distingua.** Le conclusioni della serie non
poggiano sulle nostre scelte.

## Per chi allena

**Il risultato conta, e conta da subito.** Non è una licenza a selezionare — vedi sotto — ma
è una licenza a guardare. Quello che vedete in gara a tredici anni ha a che fare con il
futuro più di quanto abbia qualunque test di laboratorio, e su questo la letteratura
internazionale è quasi unanime.

**Il miglioramento conta quanto il livello, ma solo sopra una certa quota.** Un ragazzo di
metà classifica che sale ha probabilità circa tre volte più alte di un ragazzo forte che
sta calando. Un ragazzo del terzo più basso che sale, invece, resta dov'è: il livello è una
condizione, il miglioramento un moltiplicatore.

**L'uscita dalla classifica non è un giudizio.** Quasi un terzo di chi sparisce ricompare, e
al cambio di categoria la lista si dimezza per ragioni che non riguardano i ragazzi. Se
usate la presenza in classifica come segnale, tenete presente che al primo anno di ogni
categoria quel segnale è molto più severo del solito.

**Il momento in cui intervenire sulla ritenzione è il passaggio di fascia.** È lì che si
concentra il 77% delle uscite, ed è lì che un ragazzo che sta facendo esattamente quello che
deve smette di ricevere riscontri.

## Per chi seleziona

**Qualunque soglia scegliate, la maggioranza dei selezionati non arriverà.** Al meglio delle
nostre possibilità — diciotto anni, 10% migliore — poco più della metà dei prescelti non
diventerà professionista. A tredici anni sono nove su dieci. Non è un difetto del criterio:
è quello che succede a qualunque criterio applicato a un esito che riguarda il 3% delle
persone.

**Quindi il criterio serve a decidere chi guardare, non chi escludere.** È la conclusione
pratica di tutta la serie e vale la pena scriverla per esteso: la classifica giovanile è uno
strumento ragionevole per decidere **chi seguire**, e uno strumento pessimo per decidere chi
lasciare andare. Le due decisioni non sono simmetriche. Seguire un ragazzo in più costa
poco. Lasciarne andare uno costa quanto valeva quel ragazzo, e vi sbagliereste spesso.

**Diffidate dei gradienti spettacolari.** Prima di credere che una variabile spieghi
qualcosa, chiedetevi cosa serviva per finire nella casella più alta. Se serviva arrivare
lontano, quella variabile non sta spiegando l'esito: lo sta raccontando due volte.

## Per chi ha un figlio in bici

**Non c'è fretta.** Nessuno diventa professionista prima dei diciannove anni — è un
regolamento — e il passaggio avviene in genere fra i ventuno e i ventitré. Tutto quello che
succede prima è preparazione, non verdetto.

**Sparire dalla classifica a sedici anni non è una condanna.** Metà dei classificati al
secondo anno di Allievi non c'era al primo.

**E se vostro figlio è nel 10% migliore d'Italia a diciotto anni**, ha circa una probabilità
su tre. È moltissimo rispetto alla media, ed è meno di una promessa.

## Cosa non possiamo sapere

Questa è la parte che dà la misura di tutto il resto.

**Nessuna fonte pubblica altezza, peso, specialità, allenamento o numero di gare corse.** Di
ogni ragazzo sappiamo dove è arrivato, non come ci è arrivato, e nemmeno quante volte ci ha
provato. Ogni conclusione di questa serie vale **a parità di ciò che la classifica
registra**, che è molto meno di quello che un allenatore vede da bordo strada.

**Non sappiamo quasi nulla di chi va oltre.** Il rendimento giovanile predice l'ingresso nel
professionismo e poi si ferma: sui gradini successivi possiamo dire che *non si vede* un
effetto, non che non ci sia. I ragazzi arrivati fra i primi cento al mondo sono otto.

**Non sappiamo niente delle ragazze.** Tutto questo studio riguarda i maschi. La stessa
analisi sul femminile richiede di cambiare un parametro, ma non è stata fatta — e non
sarebbe la stessa analisi: la categoria Under 23 femminile non esiste, e le atlete in
classifica sono un decimo degli atleti. Sarebbe uno studio descrittivo, e per l'effetto
dell'età relativa sarebbe il primo al mondo.

**E non sappiamo se la regione conti.** La federazione ha il dato che servirebbe — i
tesserati per anno, regione e categoria — e non lo pubblica. Con quello si potrebbe
finalmente chiedere se, a parità di corridori, un territorio aggiunga qualcosa. È la
richiesta più concreta che questa serie può fare a chi ha i dati.

## E allora?

Il ragazzo di tredici anni ha vinto la sua prima gara. Cosa possiamo dirgli?

Che quel risultato dice davvero qualcosa, e che sarebbe disonesto fingere di no. Che nove
volte su dieci non basterà, e che questo non è un giudizio su di lui ma la forma del
problema. Che il tempo per capirlo è lungo — sei o sette anni — e che nel frattempo
sparire da una classifica non vuol dire niente.

E che la cosa più importante che questi dati hanno da dire non riguarda lui.

Riguarda chi, guardando la stessa classifica, decide di smettere di guardarlo.

---

> **Come lo sappiamo**
>
> La correzione dell'ottimismo usa 500 ricampionamenti bootstrap con la procedura di
> Harrell: si ristima il modello su ogni campione estratto e si misura quanto si giudica
> meglio di quanto sia. La pendenza di calibrazione, che dice se le probabilità previste
> sono nella scala giusta, vale fra 1,01 e 1,02 — cioè è corretta.
>
> La verifica temporale addestra sulle annate 1996-1998 e misura su quelle 1999-2000. La
> verifica di sensibilità rifà l'analisi principale con tre definizioni di professionismo,
> tre finestre d'età e cinque soglie di «top».
>
> Tutti i numeri di questa serie si rigenerano da un comando, e il documento tecnico
> completo — con i metodi, gli intervalli di confidenza e i limiti sezione per sezione — è
> pubblico. I post no: sono scritti a mano, e per questo ogni loro cifra viene confrontata
> con l'archivio dei risultati prima della pubblicazione.

---

## Scelte aperte per questo post

**A. Il numero chiave manca.** Il piano ne assegna uno a ogni post e per l'ultimo non c'è.
Tre candidati:

- **0,069** — quanto oscilla la capacità predittiva cambiando tutte le definizioni. È il
  numero che sostiene la fiducia nel resto, ma è astratto;
- **26 → 151** — quanto cambia il numero di professionisti a seconda di come li si conta. Più
  concreto, dice la stessa cosa dal lato opposto;
- nessun numero, e come gancio mnemonico la frase **«chi seguire, non chi lasciare andare»**.
  **È quella che consiglierei**: l'ultimo post chiude una narrazione, e una frase regge
  meglio di una cifra.

**B. Quanto spazio dare alla validazione.** Ora apre il post e occupa un quarto dello
spazio. È la parte meno leggibile ma è ciò che autorizza tutto il resto. Alternative: (a)
come ora, in apertura, con l'argomento «ve lo dobbiamo»; (b) spostarla in fondo, subito
prima del riquadro, come appendice per chi vuole controllare; (c) ridurla a tre frasi e
rimandare al documento tecnico. **Consiglio (a) o (b) ma non (c)**: è l'unica serie di post
sul ciclismo giovanile in cui qualcuno abbia verificato che le proprie conclusioni non
dipendono dalle proprie definizioni, e vale la pena dirlo.

**C. Il femminile.** Il post lo cita fra i limiti in tre righe. Si può: (a) lasciarlo così;
(b) trasformarlo in un annuncio esplicito («la prossima serie»), se c'è l'intenzione di
farlo; (c) espanderlo in un box, spiegando che sull'effetto dell'età relativa sarebbe il
primo studio al mondo. La (c) è la più interessante ma sposta il finale.

**D. La richiesta alla federazione.** Ora è una riga fra i limiti. Se la serie ambisce ad
avere un effetto pratico, quella richiesta può diventare la chiusura del post — «serve una
tabella sola: tesserati per anno, regione e categoria» — al posto del ritorno al ragazzo di
tredici anni. Le due chiusure sono incompatibili: una è civile, l'altra narrativa. **Il
piano prevede la narrativa**, e concordo, ma la scelta va fatta consapevolmente.

**E. La struttura per destinatari** (chi allena / chi seleziona / chi ha un figlio) è chiara
ma somiglia a un elenco di raccomandazioni. Alternativa: un'unica narrazione che segue una
decisione concreta — una società che deve scegliere dieci ragazzi su cento — e fa emergere
le stesse conclusioni dal caso. Più coinvolgente, più lunga, più difficile da scrivere bene.
