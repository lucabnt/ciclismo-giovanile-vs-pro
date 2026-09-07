# Come sono scritti questi post

> Questo file non descrive un gusto personale: descrive le regole che le bozze in questa
> cartella seguono, così che una riscrittura futura non le contraddica senza accorgersene.
> Se una regola smette di convincere, si cambia qui e poi nei post, non il contrario.

La prima stesura di queste bozze era scritta in un italiano che sembrava tradotto
dall'inglese. Il problema non erano i contenuti ma il ritmo: centoventidue trattini lunghi
in quindicimila parole, decine di paragrafi di una riga sola messi lì per fare effetto, e
la formula «non è X, è Y» ripetuta quarantasei volte. Sono tutti tratti tipici delle
newsletter americane, e in italiano suonano finti.

Le regole che seguono nascono da due riferimenti: la prosa italiana di
[`Il mercato informatico`](https://lucabontempi.com/il_mercato_informatico/), che è
distesa, legata da connettivi e priva di artifici tipografici, e i post di
[lucabontempi.com](https://lucabontempi.com/blog/), che usano la prima persona, aprono
con una nota di contesto e restano concreti.

## Le regole

**Il trattino lungo si usa quasi mai.** Al suo posto vanno la virgola, i due punti, le
parentesi, oppure un punto e una frase nuova. Un inciso per post è tollerabile, dieci no.

**I periodi sono lunghi e collegati.** L'italiano scritto tiene insieme due o tre
proposizioni con un connettivo: *dato che, infatti, tuttavia, in particolare, d'altra
parte, del resto, in ogni caso, per contro, nello specifico*. Spezzare tutto in frasi corte
non rende il testo più chiaro, lo rende telegrafico.

**Niente paragrafi di una riga usati come colpo di scena.** Se una frase è importante lo si
capisce da cosa dice, non da quanto spazio bianco ha intorno.

**Si scrive in prima persona, e non solo per i metodi.** *Mi aspettavo, ho provato, non
l'ho fatto, confesso che, la trovo la cosa più utile di tutta la serie.* L'impersonale
resta dove il soggetto è davvero irrilevante, ma se una scelta l'ho fatta io lo dico io.

**Si dà del tu al lettore**, sempre singolare e sempre lo stesso per tutta la serie: *se
alleni, tuo figlio, prova a guardare, te lo dico subito*. È il registro dei blog italiani
che si leggono volentieri, e non toglie niente alla solidità: i numeri restano quelli, con
i loro intervalli e i loro limiti. Il «voi» e l'impersonale a distanza, che erano nella
prima stesura, facevano suonare i post come una relazione.

**La lingua è quella parlata, non quella scritta bene.** *Però, insomma, il punto è che, in
fondo, certo, non è che.* Vanno bene le domande buttate lì nel mezzo del discorso e gli
incisi fra parentesi (quelli sì, al posto dei trattini). Non vanno bene le frasi da
comunicato: *si evince, risulta pertanto, in ottemperanza*.

**Il grassetto è raro.** Una o due occorrenze per sezione, sul numero che conta o sulla
conclusione. Il grassetto sparso a metà frase è un tic da newsletter e smette di
funzionare esattamente quando serve.

**I titoli di sezione sono dichiarativi.** Le domande stanno nel testo, dove hanno una
risposta accanto.

**Ogni fonte si cita per intero, e il rimando è un link vero.** Gli studi con autori, anno,
titolo, rivista e DOI: chi legge deve poter arrivare all'originale senza cercarlo. I file
del progetto con l'indirizzo completo su GitHub, perché un percorso nudo come
`report/moduli/rae.py` non è cliccabile per chi legge il blog e non gli dice dove andare. Il
blocco di avviso in testa fa eccezione: parla a chi mantiene il repository, non a chi legge,
e lì i comandi restano comandi.

**Ogni cifra viaggia con il suo denominatore**, ed è la sola regola che vale anche per il
codice.

**Niente frasi senza verbo**, e niente chiuse aforistiche costruite per essere citate.

## Le definizioni e le fonti

**Ogni post si regge da solo.** I termini che tornano ovunque vanno definiti una volta per
post — cosa vuol dire professionista, cosa vogliono dire top 500 e top 100, cosa vuol dire
essere in classifica — perché chi arriva dal motore di ricerca al post 6 non deve leggere il 2
per capirlo.

**La definizione va dentro il testo, alla prima volta che il termine compare**, non in un
riquadro all'inizio. Un riquadro di definizioni prima ancora di aver detto di cosa si parla è
un glossario, e i glossari non si leggono: un inciso fra trattini o una riga in corsivo sotto
la tabella arrivano invece nel momento in cui servono. Dove ripetere per esteso sarebbe
pesante, si mette la versione corta e si rimanda al post che approfondisce.

**Ogni numero ha una fonte, e la fonte sta a piè di pagina.** Due tipi:

- i risultati di questo studio rimandano al file del repository che li produce, cioè al
  modulo di `report/moduli/` o allo script in `R/`. Chi vuole controllare apre quel file e
  ci trova la query;
- le citazioni della letteratura rimandano allo studio, con autore, anno e DOI.

Il marcatore si mette **una volta per tabella, per figura o per blocco di numeri**, non a
ogni cifra: una nota ogni tre parole rende il testo illeggibile e non aggiunge niente, dato
che i numeri di un paragrafo vengono quasi sempre dallo stesso posto.

**Sui dati che mancano non si accusa nessuno.** Non «la federazione non li pubblica», ma
«non sono pubblicamente disponibili». È più corto, è quello che sappiamo davvero, e non
attribuisce un'intenzione a nessuno.

## La struttura di ogni post

Resta quella del piano editoriale, con una differenza: la nota di contesto in testa, come
nei post del blog, che dice al lettore da dove arrivano i numeri prima che li incontri.

Apertura concreta, la domanda, le evidenze che convergono, la lettura sbagliata da
disinnescare, cosa se ne ricava, il rimando al post successivo, e in fondo un riquadro sul
metodo per chi vuole controllare.

Il riquadro finale è l'unico posto in cui il registro si alza: lì si parla di modelli e di
intervalli di confidenza, e chi ci arriva vuole quello.
