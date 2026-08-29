# 6. Predire non è selezionare

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio
> se i dati cambiano. Prima di pubblicare: `python scripts/11_verifica_documenti.py`.
> Le affermazioni qualitative restano da rileggere a mano.
>
> **Numeri chiave del post:** 59% e 52%.
> **Moduli:** `metriche`, `qualita`, `sopravvivenza`.
> **Figure:** `metriche_soglie`, `qualita_catena`, `sopravvivenza_hazard`.

---

Immaginate un esame del sangue per una malattia che colpisce tre persone su cento. È un
buon test: quando una persona è malata, lo trova quasi sempre.

Fate lo screening su mille persone. Trenta sono malate, novecentosettanta no. Il test ne
segnala un centinaio. Di quei cento segnalati, quanti sono davvero malati?

Molti meno della metà. Non perché il test sia scadente, ma perché i sani erano trentadue
volte più numerosi dei malati, e anche una piccola percentuale di errori su un gruppo enorme
produce più falsi allarmi di quanti siano i casi veri.

Questa è, quasi punto per punto, la situazione di chi seleziona giovani ciclisti. Con una
differenza: nel caso dello screening la persona segnalata fa un secondo esame e la storia
finisce lì. Nel caso del ciclismo, il ragazzo non segnalato smette di essere seguito.

## La domanda

**Se una società usasse davvero la classifica per scegliere, cosa otterrebbe?**

## Facciamolo

Prendiamo la categoria in cui la previsione funziona meglio — Juniores secondo anno,
diciotto anni — e applichiamo il criterio più naturale: **seguiamo il 10% migliore**.

Novecentouno ragazzi in classifica. Ne selezioniamo novantuno.

| | |
|---|---|
| futuri professionisti intercettati | **59%** |
| selezionati che non lo diventeranno | **52%** |

Entrambe le metà della frase sono vere, e sono quasi sempre citate una alla volta.

Chi vuole difendere la selezione dice la prima: *guardando il 10% migliore si prendono quasi
sei futuri professionisti su dieci*. Vero.

Chi vuole demolirla dice la seconda: *più della metà dei prescelti non ce la farà*. Vero
anche questo.

E il punto è che **non c'è una soglia che risolva**. Allargando al 25% migliore si sale
all'82% dei futuri professionisti intercettati, ma la quota di selezionati che arriva scende
al 27%: si prende quasi tutti quelli giusti insieme a tre volte tanti che non lo sono.
Stringendo, si perdono i professionisti veri. Le due colonne si muovono sempre in direzioni
opposte, perché descrivono lo stesso compromesso visto dai due lati.

## E a tredici anni?

Peggio, com'era prevedibile — ma vale la pena vedere quanto.

Selezionando il 10% migliore degli Esordienti primo anno si intercetta il **32%** dei futuri
professionisti, e di quei 169 ragazzi ne arriverà **l'11%**.

Tradotto: **nove ragazzi su dieci fra i migliori d'Italia a tredici anni non diventeranno
professionisti**, e due futuri professionisti su tre in quel momento non sono nel gruppo dei
migliori.

Il post 4 diceva che a tredici anni si vede già qualcosa, e resta vero. Questo post dice
cosa succede se si prova a usarlo per decidere, e le due cose stanno insieme senza
contraddirsi. Il segnale c'è; è il rapporto fra i numeri che rende inutilizzabile la
decisione.

## Perché non è colpa del criterio

Qui sta il punto che vale l'intero post, ed è aritmetica, non statistica.

Quando l'esito riguarda il 3% della popolazione, ogni criterio di selezione pesca in un mare
di persone che non arriveranno. Anche un ordinamento quasi perfetto — e il nostro, a
diciotto anni, mette davanti il ragazzo giusto in quasi nove coppie su dieci — produce
liste in cui i falsi positivi sono la maggioranza.

Non c'è modello, algoritmo o osservatore esperto che possa aggirarlo. Non è un difetto della
misura: è la forma del problema.

La conseguenza pratica è che **il numero da chiedere a chiunque proponga un criterio di
selezione non è "quanti ne intercetta", ma "quanti dei segnalati arrivano"**. Il primo
numero è sempre lusinghiero. Il secondo è quello che descrive la lista che vi ritrovate in
mano.

## Un'insidia nei numeri

C'è una riga della tabella completa che sembra ottima e non lo è. In Under 23, selezionando
il 10% migliore, arriva il **93%** dei selezionati.

Sembra che il criterio funzioni benissimo, a quell'età. In realtà funziona esattamente come
prima: quello che è cambiato è il gruppo. In Under 23 chi è ancora in classifica ha già
superato tre selezioni, e i professionisti sono più di un terzo della lista. Applicare un
criterio a un gruppo già scremato lo fa sembrare più preciso senza che lo sia.

È la stessa trappola del denominatore del post 2, in un'altra veste. Ogni volta che una
percentuale sembra migliorare, conviene chiedersi se sia migliorata la misura o se sia
cambiato il gruppo.

## Quanto vale, in probabilità

Rovesciamo la domanda: invece di scegliere una soglia, chiediamo cosa possiamo dire di un
singolo ragazzo.

| piazzamento a diciotto anni | professionista | almeno top 500 mondiale | top 100 |
|---|---|---|---|
| 50° percentile | 1,1% | 0,4% | 0,04% |
| 75° percentile | 10,0% | 4,6% | 0,73% |
| 90° percentile | **30,0%** | **15,8%** | 3,4% |

Un ragazzo nel 10% migliore d'Italia a diciotto anni ha **circa il 30% di probabilità di
diventare professionista**. È tantissimo rispetto alla media e pochissimo rispetto a una
certezza: sette volte su dieci, non succederà.

Ed è il numero che rende onesta tutta la conversazione. Non «ce la farà», non «non ce la
farà»: uno su tre.

## Quando succede, e quanto conta esserci

C'è una seconda domanda che una società si pone, e riguarda i tempi: **fino a quando ha
senso aspettare?**

Prima dei diciannove anni non passa professionista nessuno, e non è un dato ma un
regolamento: non si può. Poi il rischio cresce e il massimo cade a **23 anni**. Chi non
è passato entro quell'età, salvo eccezioni, non passerà.

Nel modello che descrive questo percorso c'è un coefficiente che domina tutti gli altri, e
non è il rendimento. È **l'esserci**. Un atleta che l'anno prima non era in classifica ha un
rischio di passare professionista **venti volte più basso** di uno che c'era.

Va letto con la cautela che merita, perché il post 3 ha già mostrato che sparire dalla
classifica non è smettere di correre. Quel coefficiente misura in buona parte **quanto è
difficile rientrare** una volta usciti dal gruppo osservato, non quanto sia compromessa la
carriera di chi esce. E c'è un dato che ridimensiona la drammaticità: nell'**87,5%** delle
stagioni a rischio l'atleta non era in classifica l'anno prima. L'assenza è la
condizione normale, non l'eccezione.

Per chi invece c'è tutti gli anni, i numeri sono questi: **11,1%** di probabilità di
arrivare al professionismo con un rendimento nella media della classifica, **30,9%** con
venti posizioni percentuali in più, **3,7%** con venti in meno.

## Il rendimento predice l'ingresso, e poi si ferma

Ultima domanda, e la risposta è la più netta di tutta la serie.

Fin qui il professionismo è stato trattato come una porta: dentro o fuori. Ma fra i
professionisti c'è chi corre tre stagioni in una squadra di seconda divisione e chi entra
fra i primi cento al mondo. Il piazzamento a diciotto anni dice qualcosa anche su questo?

| | quanto moltiplica le probabilità |
|---|---|
| diventare professionista | **×2,47** |
| entrare nel top 500, **fra i professionisti** | ×1,20 *(non distinguibile dal caso)* |
| entrare nel top 100, **fra i top 500** | ×1,28 *(non distinguibile dal caso)* |

**La classifica giovanile italiana predice chi entrerà, e quasi nulla di ciò che succede
dopo.**

Attenzione a come si legge, perché la formulazione sbagliata è a un passo. Non significa che
fra i professionisti il talento non conti. Significa che **quella classifica non lo misura
più**. A diciotto anni distingue bene chi diventerà professionista da chi no; una volta
varcata la soglia, quello che decide se si arriva fra i primi cento al mondo è qualcosa che
il ranking giovanile italiano non ha registrato.

Con un limite da dire: il gradino più alto poggia su quindici atleti. Su quel numero si può
concludere che **non si vede** un effetto, non che non ci sia.

## Cosa se ne ricava

Il numero da tenere non è quanti ne intercetti. È quanti ne scarti per sbaglio, e quanti ne
tieni che non arriveranno.

Da cui una distinzione che vale più di tutte le tabelle: **la classifica giovanile è uno
strumento ragionevole per decidere chi seguire, e uno strumento pessimo per decidere chi
lasciare andare.** Le due decisioni sembrano simmetriche e non lo sono. Seguire un ragazzo
in più costa poco e il costo dell'errore è basso. Lasciarne andare uno costa quanto vale
quel ragazzo, e a tredici anni sbagliereste due volte su tre.

E per chi ha un figlio in bici: se a diciotto anni è nel 10% migliore d'Italia, ha circa una
probabilità su tre. Se non c'è, non è finita — ma il tempo utile si chiude attorno ai
ventitré anni, e questo è un dato, non un'opinione.

## Il gancio

Restano da guardare le cose che tutti pensano contino. Il mese di nascita, la squadra
giusta, la regione giusta.

Sono tre indizi, e nessuno dei tre è quello che sembra.

---

> **Come lo sappiamo**
>
> Le due colonne che il post mette una accanto all'altra si chiamano **sensibilità** (quota
> di futuri professionisti dentro la selezione) e **valore predittivo positivo** (quota di
> selezionati che arriverà). Nessuno studio sul ciclismo giovanile basato sui risultati di
> gara aveva mai riportato il secondo.
>
> Le probabilità per percentile sono previsioni di un modello, non frequenze osservate:
> vanno lette come ordini di grandezza. Quelle della sezione sui tempi valgono per chi resta
> in classifica **ogni** stagione, che è una minoranza molto selezionata — non sono la
> probabilità di un ragazzo qualunque che comincia a correre.
>
> Il modello sui tempi è di sopravvivenza a tempo discreto, con una riga per ogni stagione
> in cui un atleta poteva diventare professionista e non lo era ancora; chi non ha ancora
> completato la finestra contribuisce le stagioni osservate senza essere contato come un
> no. Gli errori standard sono raggruppati per atleta.
>
> La finestra si ferma a ventitré anni perché lì finisce il predittore: oltre l'Under 23 non
> esiste più una classifica giovanile nazionale. Dieci passaggi al professionismo avvenuti
> dopo restano fuori dal modello, ed è dichiarato invece che nascosto.

---

## Scelte aperte per questo post

**A. L'esempio dello screening.** Il piano lo indica come il modo migliore per far capire il
valore predittivo positivo, e il post lo usa in apertura. Due riserve da valutare:

- il pubblico di un blog di ciclismo potrebbe trovare l'apertura medica fredda o
  fuori tema;
- l'analogia va spiegata bene o si ritorce: un lettore può concludere «quindi i test medici
  non servono», che non è il punto.

Alternative: (a) tenerla in apertura come ora; (b) spostarla a metà, dopo aver dato i numeri
del ciclismo, come spiegazione del perché; (c) sostituirla con un esempio più vicino — i
provini di calcio, le audizioni. **Consiglio (b)**: i numeri del ciclismo aprono meglio, e
l'analogia arriva quando serve a spiegare, non a introdurre.

**B. Il post contiene tre analisi diverse** — soglie di selezione, tempi del passaggio,
profondità della carriera — ed è il più denso della serie. Si può scorporare la parte sui
tempi («quando si diventa professionisti», con il coefficiente dell'esserci) in un post a
sé, portando la serie a nove. Contro: da sola quella parte è più tecnica che utile. A
favore: alleggerisce il post più importante della serie.

**C. Quanto insistere su «chi seguire / chi lasciare andare».** È la conclusione operativa
di tutta la ricerca e per ora sta in tre righe nel «cosa se ne ricava». Si può portarla in
apertura come tesi dichiarata, oppure lasciarla dov'è e riprenderla nel post 8. **Il piano
prevede che sia la chiusura del post 8**: se la si anticipa qui con troppa forza, l'ultimo
post perde il suo finale.

**D. Il 93% dell'Under 23.** È l'unico numero lusinghiero della tabella e viene smontato
subito. Si può anche ometterlo del tutto: costa un paragrafo e rischia di essere citato
fuori contesto da chi legge in fretta. Consiglio di tenerlo — è il miglior esempio di come
un gruppo scremato faccia sembrare bravo un criterio qualsiasi — ma di non metterlo in un
riquadro evidenziato.

**E. La frase sul figlio in bici.** «Se a diciotto anni è nel 10% migliore, ha una
probabilità su tre» è vera e verificabile, ma è anche la frase che verrà estratta e
condivisa da sola. Valutare se accompagnarla sempre con il suo complemento («e nove su dieci
dei migliori a tredici anni non arriveranno»).
