# 6. Predire non è selezionare

> ⚠️ **Bozza scritta a mano. Non si rigenera.** Ogni cifra è copiata dall'analisi al momento
> della stesura e diventerà falsa in silenzio se i dati cambiano. Prima di pubblicare
> conviene eseguire `python scripts/11_verifica_documenti.py`. Sullo stile:
> [`STILE.md`](STILE.md).
>
> **Numeri chiave del post:** 59% e 52%.
> **Moduli:** `metriche`, `qualita`, `sopravvivenza`.
> **Figure:** `metriche_soglie`, `qualita_catena`, `sopravvivenza_hazard`.

---

*Sesta puntata, e quella a cui tutte le precedenti portavano. Fin qui ho misurato quanto il
rendimento giovanile predica il professionismo; qui provo a usare quella misura per
scegliere, che è una cosa molto diversa.*

Prendiamo la categoria in cui la previsione funziona meglio, cioè i Juniores di secondo
anno, diciotto anni, e applichiamo il criterio più naturale che una società possa adottare:
seguo il dieci per cento migliore. Su 901 ragazzi in classifica ne seleziono 91.

Una precisazione prima dei numeri, perché qui contano: *professionista* vuol dire aver corso
in una squadra di primo o secondo livello entro i venticinque anni, mentre *top 500* e *top
100* sono la migliore posizione raggiunta nella classifica mondiale annuale entro i
ventisei. Le finestre d'età servono a rendere confrontabili annate diverse, e chi arriva più
tardi in questi conti non c'è.

| | |
|---|---|
| futuri professionisti intercettati | **59%** |[^p6metriche]
| selezionati che non lo diventeranno | **52%** |

Sono vere tutte e due, e quasi sempre te ne citano una alla volta. Chi vuole difendere la
selezione ti dice la prima, cioè che guardando il dieci per cento migliore prendi quasi sei
futuri professionisti su dieci. Chi vuole demolirla ti dice la seconda, cioè che più della
metà dei prescelti non ce la farà.

Il punto è che non esiste una soglia che risolva il problema. Se allarghi al 25% migliore
sali all'82% dei futuri professionisti intercettati, ma la quota di selezionati che poi
arriva scende al 27%: prendi quasi tutti quelli giusti insieme a tre volte tanti che non lo
sono. Se stringi, perdi i professionisti veri. Le due colonne si muovono sempre in direzioni
opposte, perché descrivono lo stesso compromesso guardato dai due lati.

## A tredici anni va peggio, e conviene vedere quanto

Selezionando il dieci per cento migliore degli Esordienti di primo anno intercetti il
**32%** dei futuri professionisti, e di quei 169 ragazzi ne arriverà l'**11%**.

Tradotto: nove ragazzi su dieci fra i migliori d'Italia a tredici anni non diventeranno
professionisti, e due futuri professionisti su tre in quel momento non sono nel gruppo dei
migliori.

Il post precedente diceva che a tredici anni si vede già qualcosa, e resta vero; questo ti
dice cosa succede se provi a usarlo per decidere, e le due affermazioni stanno insieme senza
contraddirsi. Il segnale c'è, è il rapporto fra i numeri a rendere inutilizzabile la
decisione.

## Perché non è colpa del criterio

Il punto che vale l'intero post è di aritmetica e non di statistica, e te lo spiego con un
esempio che viene da tutt'altro campo.

Immagina un esame del sangue per una malattia che colpisce tre persone su cento, e che sia
un buon test, capace di trovare la malattia quasi sempre quando c'è. Fai lo screening su
mille persone: trenta saranno malate e novecentosettanta no. Se il test ne segnala un
centinaio, di quei cento segnalati i malati veri saranno molti meno della metà. Non perché
il test sia scadente, ma perché i sani erano trentadue volte più numerosi dei malati, e
anche una piccola percentuale di errori su un gruppo enorme produce più falsi allarmi di
quanti siano i casi veri.

Chi seleziona giovani ciclisti sta nella stessa identica situazione, con una differenza:
nello screening la persona segnalata fa un secondo esame e la storia finisce lì, mentre nel
ciclismo il ragazzo non segnalato smette di essere seguito.

Quando l'esito riguarda il 3% della popolazione, quindi, qualunque criterio di selezione
pesca in un mare di gente che non arriverà, e anche un ordinamento quasi perfetto (il
nostro, a diciotto anni, mette davanti il ragazzo giusto in quasi nove coppie su dieci)
produce liste in cui i falsi positivi sono la maggioranza. Non c'è modello, algoritmo od
osservatore esperto che possa aggirare la cosa, perché non è un difetto della misura ma la
forma del problema.

Ne segue una conseguenza pratica che ti conviene tenere: il numero da chiedere a chiunque ti
proponga un criterio di selezione non è quanti ne intercetta, ma quanti dei segnalati
arrivano. Il primo numero è sempre lusinghiero, il secondo descrive la lista che ti ritrovi
davvero in mano.

## Un numero lusinghiero che non va creduto

C'è una riga della tabella completa che sembra ottima e non lo è: in Under 23, selezionando
il dieci per cento migliore, arriva il **93%** dei selezionati.

Sembrerebbe che a quell'età il criterio funzioni benissimo, e invece funziona esattamente
come prima. È cambiato il gruppo: in Under 23 chi è ancora in classifica ha già superato tre
selezioni, e i professionisti sono più di un terzo della lista. Applicare un criterio a un
gruppo già scremato lo fa sembrare più preciso senza che lo sia, ed è la stessa trappola del
denominatore del post 2 sotto un'altra veste. Ogni volta che una percentuale sembra
migliorare, chiediti se sia migliorata la misura o se sia cambiato il gruppo.

## Quanto vale, in probabilità

Rovesciamo la domanda: invece di scegliere una soglia, chiediamoci cosa si possa dire di un
singolo ragazzo.

| piazzamento a diciotto anni | professionista | almeno top 500 mondiale | top 100 |[^p6qualita]
|---|---|---|---|
| 50° percentile | 1,1% | 0,4% | 0,04% |
| 75° percentile | 10,0% | 4,6% | 0,73% |
| 90° percentile | **30,0%** | **15,8%** | 3,4% |

Un ragazzo nel dieci per cento migliore d'Italia a diciotto anni ha quindi circa il 30% di
probabilità di diventare professionista. Che è moltissimo rispetto alla media e pochissimo
rispetto a una certezza, perché sette volte su dieci non succederà. È il numero che rende
onesta tutta la conversazione, perché non dice né che ce la farà né che non ce la farà: dice
uno su tre.

## Quando succede, e quanto conta esserci

C'è una seconda domanda che una società si pone, e riguarda i tempi: fino a quando ha senso
aspettare?

Prima dei diciannove anni non passa professionista nessuno[^p6sopravvivenza], e non è un
dato ma un regolamento: non si può. Poi il rischio cresce e il massimo cade a **23 anni**,
dopo di che, salvo eccezioni, chi non è passato non passerà.

Nel modello che descrive questo percorso c'è un coefficiente che domina tutti gli altri, e
non è il rendimento ma l'esserci: un atleta che l'anno prima non era in classifica ha un
rischio di passare professionista venti volte più basso di uno che c'era. Va letto con la
cautela che merita, perché il post 3 ha già mostrato che sparire dalla classifica non
significa smettere di correre, per cui quel coefficiente misura in buona parte quanto sia
difficile rientrare una volta usciti dal gruppo osservato, e non quanto sia compromessa la
carriera di chi esce. E poi c'è un dato che ne ridimensiona la drammaticità: nell'**87,5%**
delle stagioni a rischio l'atleta non era in classifica l'anno prima. In Under 23 l'assenza
è la condizione normale, non l'eccezione.

Per chi invece c'è tutti gli anni, i numeri sono questi: **11,1%** di probabilità di
arrivare al professionismo con un rendimento nella media della classifica, 30,9% con venti
posizioni percentuali in più, 3,7% con venti in meno.

## Il rendimento predice l'ingresso, e poi si ferma

Resta un'ultima domanda, e la risposta è la più netta di tutta la serie.

Fin qui il professionismo è stato trattato come una porta, dentro o fuori, mentre fra i
professionisti c'è chi corre tre stagioni in una squadra di seconda divisione e chi entra
fra i primi cento al mondo. Il piazzamento a diciotto anni dice qualcosa anche su questo?

| | quanto moltiplica le probabilità |[^p6qualita]
|---|---|
| diventare professionista | **×2,47** |
| entrare nel top 500, **fra i professionisti** | ×1,20 *(non distinguibile dal caso)* |
| entrare nel top 100, **fra i top 500** | ×1,28 *(non distinguibile dal caso)* |

La classifica giovanile italiana predice chi entrerà, e quasi nulla di quello che succede
dopo. La formulazione però va scelta con attenzione, perché quella sbagliata è a un passo:
non significa che fra i professionisti il talento non conti, ma che quella classifica non lo
misura più. A diciotto anni distingue bene chi diventerà professionista da chi no; una volta
varcata la soglia, quello che decide se arrivi fra i primi cento al mondo è qualcosa che il
ranking giovanile italiano non ha registrato. Con un limite da aggiungere: il gradino più
alto poggia su quindici atleti, quindi su quei numeri si può dire che non si veda un
effetto, non che non ce ne sia uno.

C'è però una spiegazione alternativa che vale la pena raccontare, perché mi è stata proposta
e i dati la sostengono a metà. Le squadre professionistiche italiane hanno bisogno di
corridori italiani, quindi i migliori juniores nazionali sono il bacino da cui pescano: il
ranking potrebbe predire l'ingresso semplicemente perché ordina bene quel bacino. Ho provato
a verificarlo separando chi debutta in una squadra a maggioranza italiana da chi debutta in
una straniera. La versione forte non regge, perché il percentile Under 19 predice le due
cose praticamente allo stesso modo (0,863 contro 0,867). Ma le due porte non portano allo
stesso posto: di chi entra da una squadra italiana arriva nel top 500 il **33%**, di chi
entra da una straniera il **59%**. Quindi «diventare professionista» non è un evento solo, e
metterne insieme due così diversi spiega una parte di quello che il ranking non riesce a
predire.[^p6porta]

## Cosa te ne porti a casa

Il numero da tenere non è quanti ne intercetti, ma quanti ne scarti per sbaglio e quanti ne
tieni che non arriveranno.

Ne segue una distinzione che vale più di tutte le tabelle: la classifica giovanile è uno
strumento ragionevole per decidere chi seguire e uno strumento pessimo per decidere chi
lasciare andare. Le due decisioni sembrano simmetriche e non lo sono, perché seguire un
ragazzo in più ti costa poco, mentre lasciarne andare uno ti costa quanto valeva quel
ragazzo, e a tredici anni sbaglieresti due volte su tre.

Se hai un figlio che corre, la traduzione è semplice: se a diciotto anni è nel dieci per
cento migliore d'Italia ha circa una probabilità su tre, e se non c'è non è finita, anche se
il tempo utile si chiude attorno ai ventitré anni. Quello è un dato, non un'opinione.

Restano da guardare le cose che tutti pensano contino, cioè il mese di nascita, la squadra
giusta e la regione giusta. Sono tre indizi, e nessuno dei tre è quello che sembra: è il
tema della prossima puntata.

---

> **Come lo sappiamo**
>
> Le due colonne che il post mette una accanto all'altra si chiamano sensibilità, cioè la
> quota di futuri professionisti che finisce dentro la selezione, e valore predittivo
> positivo, cioè la quota di selezionati che arriverà. Nessuno studio sul ciclismo giovanile
> basato sui risultati di gara aveva mai riportato il secondo.
>
> Le probabilità per percentile sono previsioni di un modello e non frequenze osservate, per
> cui vanno lette come ordini di grandezza. Quelle della sezione sui tempi valgono per chi
> resta in classifica ogni stagione, che è una minoranza molto selezionata, e non sono
> quindi la probabilità di un ragazzo qualunque che comincia a correre.
>
> Il modello sui tempi è di sopravvivenza a tempo discreto, con una riga per ogni stagione
> in cui un atleta poteva diventare professionista e non lo era ancora; chi non ha ancora
> completato la finestra contribuisce le stagioni osservate senza essere contato come un no,
> e gli errori standard sono raggruppati per atleta.
>
> La finestra si ferma a ventitré anni perché lì finisce il predittore, visto che oltre
> l'Under 23 non esiste più una classifica giovanile nazionale. I dieci passaggi al
> professionismo avvenuti dopo restano fuori dal modello, ed è dichiarato invece che
> nascosto.

[^p6metriche]: Calcolo in [R/19_metriche.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/19_metriche.R), reso da [report/moduli/metriche.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/metriche.py).

[^p6qualita]: Modello ordinale e catena degli stadi in [R/22_qualita_carriera.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/22_qualita_carriera.R), resi da
    [report/moduli/qualita.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/qualita.py).

[^p6sopravvivenza]: Modello di sopravvivenza in [R/20_sopravvivenza.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/20_sopravvivenza.R), reso da
    [report/moduli/sopravvivenza.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/sopravvivenza.py).

[^p6porta]: Calcolo in [report/moduli/porta.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/porta.py), che classifica le squadre dalla
    composizione delle rose di ProCyclingStats.

---

## Scelte aperte per questo post

**A. Dove mettere l'esempio dello screening.** Il piano lo indicava come il modo migliore per
far capire il valore predittivo positivo. Nella prima stesura apriva il post, mentre adesso
arriva a metà, dopo i numeri del ciclismo, come spiegazione del perché: è la soluzione che
preferisco, perché i numeri del ciclismo aprono meglio e l'analogia serve a spiegare, non a
introdurre. Le alternative restano riportarlo in apertura, con il rischio che un pubblico di
ciclismo lo trovi freddo, oppure sostituirlo con un esempio più vicino, come i provini di
calcio o le audizioni.

**B. Il post contiene tre analisi diverse**, cioè le soglie di selezione, i tempi del passaggio
e la profondità della carriera, ed è il più denso della serie. Si può scorporare la parte
sui tempi, con il coefficiente dell'esserci, in un post a sé, portando la serie a nove:
contro questa scelta gioca il fatto che da sola quella parte sia più tecnica che utile, a
favore il fatto che alleggerirebbe il post più importante della serie.

**C. Quanto insistere sulla distinzione fra chi seguire e chi lasciare andare.** È la
conclusione operativa di tutta la ricerca e per ora sta in poche righe. La si può portare in
apertura come tesi dichiarata, oppure lasciarla dov'è e riprenderla nel post 8, che secondo
il piano dovrebbe chiudersi proprio lì: anticipandola qui con troppa forza, l'ultimo post
perde il suo finale.

**D. Il 93% dell'Under 23.** È l'unico numero lusinghiero della tabella e viene smontato
subito, ma si può anche omettere del tutto, perché costa un paragrafo e rischia di essere
citato fuori contesto da chi legge in fretta. Consiglierei di tenerlo, essendo il miglior
esempio di come un gruppo già scremato faccia sembrare bravo un criterio qualsiasi, evitando
però di metterlo in evidenza tipografica.

**E. La frase sul figlio in bici.** Dire che nel dieci per cento migliore a diciotto anni hai
una probabilità su tre è vero e verificabile, ed è anche la frase che verrà estratta e
condivisa da sola. Conviene decidere se accompagnarla sempre con il suo complemento, cioè
che nove su dieci dei migliori a tredici anni non arriveranno.
