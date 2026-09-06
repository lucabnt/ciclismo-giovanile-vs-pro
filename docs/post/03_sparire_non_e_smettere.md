# 3. Sparire dalla classifica non è smettere

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio se
> i dati cambiano. Prima di pubblicare conviene eseguire
> `python scripts/11_verifica_documenti.py`. Sullo stile: [`STILE.md`](STILE.md).
>
> **Numero chiave del post:** 30,6%.
> **Moduli:** `attrito` (ricambio), `passaggi`, `posti`, `copertura` (i due imbuti).
> **Figure:** `attrito_uscite`, `passaggi_ritenzione`, `posti_quote`.

---

*Terza puntata. Nella seconda ho spiegato che la classifica nazionale raccoglie circa un
tesserato su sette e che fra i tredici e i ventidue anni ne perde quasi tutti. Qui provo a
capire dove finiscano, e ti anticipo che la risposta non è quella che sembra.*

Un ragazzo chiude la stagione da Allievo secondo anno al settantesimo posto della classifica
nazionale, l'anno dopo passa Juniores, e a fine stagione il suo nome in classifica non c'è
più. Se metti a confronto quei due elenchi la conclusione ti viene da sola: ha smesso.

È la conclusione più naturale del mondo ed è quasi sempre sbagliata. Nel resto del post provo
a spiegarti perché, e soprattutto a mostrarti come lo si dimostra senza dover telefonare a
nessuno.

## La prima crepa: i ritorni

Se sparire dalla classifica volesse dire smettere, non ci sarebbero ritorni: chi appende la
bici al chiodo non ricompare in una classifica nazionale due anni dopo.

Invece **il 30,6% degli atleti salta almeno una stagione e poi ricompare**, e il 6,7% torna
dopo un'assenza di due stagioni o più. Quasi un terzo, e non come caso limite ma come esito
normale per un ragazzo che a un certo punto smette di andare a punti. Ogni singolo rientro,
in fondo, è la prova che l'assenza dell'anno prima non era un abbandono.

## La seconda crepa: le liste si rinnovano da dentro

C'è un modo del tutto diverso di arrivare alla stessa conclusione, che non guarda le carriere
individuali ma la composizione delle liste: prendi due classifiche consecutive della stessa
categoria e conti quante facce nuove ci sono nella seconda.

| classifica | atleti | non c'erano l'anno prima |[^p3attrito]
|---|---|---|
| Under 15, secondo anno | 1 786 | 28,3% |
| Under 17, secondo anno | 1 602 | **50,8%** |
| Under 19, secondo anno | 901 | 38,8% |

Metà dei classificati al secondo anno di Allievi non c'era al primo. E non avevano cambiato
categoria, è la stessa fascia d'età dodici mesi dopo: sono ragazzi che l'anno prima correvano
senza andare a punti e quell'anno ci sono andati.

Le due misure, i rientri e il rinnovo delle liste, sono indipendenti l'una dall'altra e
portano allo stesso posto. Per questo te le do entrambe.

## Il crollo che in buona parte non c'è

Resta il fatto più vistoso, quello che sembra reggere la lettura drammatica: **il 77,2% di
chi esce dalla classifica esce nell'ultimo anno della propria categoria**. Non a metà
percorso, non dopo una brutta stagione, ma proprio quando si cambia fascia.

Sembra la prova provata che il salto di categoria sia un trauma, con distanze nuove,
avversari più grandi e squadra diversa, ed è una lettura del tutto plausibile. Proprio per
questo conviene metterla alla prova invece di darla per buona.

Il modo per farlo è confrontare due tipi di passaggio che durano entrambi una stagione:
quelli da un anno all'altro dentro la stessa categoria e quelli da un anno all'altro fra
categorie diverse. L'unica differenza è che ci sia o no il cambio di fascia.

| | resta in classifica | la lista di arrivo è fatta da chi c'era già |[^p3passaggi]
|---|---|---|
| dentro la categoria | **79,9%** | 60,7% |
| cambiando categoria | **32,4%** | **88,2%** |

La prima colonna conferma il crollo, e di brutto: si passa da quattro su cinque a uno su tre.
La seconda dice il contrario con la stessa forza, perché dopo un cambio di categoria la
classifica in cui arrivi è composta per l'**88,2%** da gente che c'era già, mentre dopo un
passaggio interno la quota è del 60,7%. Al cambio di fascia, cioè, non entra quasi nessuno di
nuovo.

I due numeri sembrano contraddirsi e non si contraddicono, e per capire perché ti serve
sapere una cosa su come sono fatte le classifiche. Negli Esordienti la fonte ne pubblica **due
separate**, una per annata: primo e secondo anno corrono gare loro e non si fanno concorrenza.
Dagli Allievi in su la classifica è **una sola**, e le due annate ci convivono correndo le
stesse identiche gare.

Il confronto fra le due situazioni è la cosa che mi ha divertito di più in tutto lo studio,
perché una fa da controllo all'altra. E i posti si possono contare, anche se il calendario non
è pubblicato: ogni gara assegna cinque piazzamenti a punti, dal primo al quinto, quindi
sommando tutti i piazzamenti nei primi cinque si ottiene quanti posti sono stati messi in
palio, e dividendo per cinque quante gare sono state. È una stima indiretta, che assume che
ogni gara assegni cinque posti e che tutti i piazzamenti finiscano in classifica; in Under 23
è un limite inferiore, perché in quella lista corrono anche gli Elite, che sono fuori dalla
finestra d'età di questo studio.

| categoria | quota dei posti presa dal primo anno |[^p3posti]
|---|---|
| Esordienti, classifiche separate | **49,7%** |
| Allievi, classifica unica | **26,7%** |
| Juniores, classifica unica | 33,3% |
| Under 23, classifica unica | 11,8% |

Dove nessuno fa concorrenza a nessuno le due annate si dividono i posti a metà, come è ovvio
che sia. Dove la lista è una sola, e le gare sono esattamente le stesse per tutti, il primo
anno ne prende poco più di un quarto.

Vuol dire che il crollo **non è una questione di posti che spariscono**: i posti sono gli
stessi, cambia chi li vince. Un Allievo al primo anno corre contro ragazzi che hanno un anno di
sviluppo in più, e i piazzamenti se li prendono loro. Quello che sembrava un trauma è in buona
parte questo: non sei peggiorato, sei diventato il più piccolo della gara.

## Fra chi il posto ce l'ha, l'ordine tiene

Una rottura potrebbe però prendere una seconda forma: non far sparire le persone ma
rimescolarne l'ordine. In quel caso il risultato di una stagione direbbe poco su quella dopo.

Un rimescolamento c'è, ma è modesto. La correlazione fra il piazzamento di due stagioni
consecutive vale **0,591** dentro la categoria e **0,471** al cambio di fascia, quindi la
differenza esiste e va nella direzione che ti aspetti, senza però essere grande. Detta in modo
più concreto: chi resta in classifica si sposta in mediana di 14,4 posizioni percentuali
dentro la categoria e di 19,7 al cambio di fascia, che su una scala da 0 a 100 sono
spostamenti dello stesso ordine. Il cambio di categoria, insomma, toglie persone dalla
classifica molto più di quanto rimescoli quelle che restano.

Una precisazione, per non esagerare nella direzione opposta: le gare, salendo di categoria,
calano davvero. Da circa 640 classificazioni di gara per stagione in Esordienti si scende a
146 in Under 23. Il calendario si accorcia, quindi una parte della lettura corrente è giusta;
quello che non regge è attribuire a quel restringimento il crollo del primo anno, visto che
succede anche dove le gare sono le stesse.

E già che siamo in argomento, contando le gare è venuta fuori la cosa più inattesa di tutto
lo studio, che con l'abbandono non c'entra ma merita una riga: **il calendario giovanile si è
quasi dimezzato in sedici anni**. Fra il 2009 e il 2025 le classificazioni di gara calano del
40% in Esordienti e del 58% in Under 23, e non è colpa del covid, perché il calo era
cominciato molto prima e dopo il 2020 non si è tornati ai valori di prima. Nella finestra in
cui possiamo confrontare, i tesserati Esordienti calano di circa un decimo e le gare di quasi
un quinto: il movimento si restringe, e il calendario si restringe più in fretta.

## Sono più continui, quelli che arrivano?

Una domanda che mi hanno fatto e che merita una risposta secca: i futuri professionisti sono
più costanti degli altri? Dipende da cosa intendi per costanti, e le due risposte sono
opposte.

Se intendi **quanto durano**, sì, e in modo clamoroso: nelle coorti che ho studiato i futuri
professionisti compaiono in classifica per 7,9 stagioni in media, contro le 2,8 di tutti gli
altri. Il guaio è che il numero non ti serve per decidere, perché è in gran parte una
conseguenza e non una causa: si resta in classifica se si va bene, quindi la durata racconta
l'esito invece di prevederlo. È lo stesso travestimento dei cambi di società, di cui parlo
nella settima puntata.

Se invece intendi **quanto sono stabili nel livello**, la risposta è no. Fra chi ha almeno tre
stagioni, lo scarto tipico del proprio percentile vale 16,7 posizioni per i futuri
professionisti e 17,3 per tutti gli altri: praticamente identico. Chi arriverà oscilla quanto
chiunque altro, solo che oscilla più in alto.[^p3continuita]

Se poi la domanda è cosa dica il *movimento* di un ragazzo, cioè se stia salendo o scendendo
negli anni, quella è un'altra cosa ancora e ha una risposta molto più interessante: è il tema
della quinta puntata.

## La conferma che arriva da fuori

Tutto quello che ti ho detto finora è misurato dentro la classifica, e una verifica interna
lascia sempre il dubbio di essere circolare. Per fortuna c'è un controllo esterno, cioè i
tesserati della federazione: se la classifica si restringesse più in fretta della popolazione
che la genera vorrebbe dire che sta perdendo gente per ragioni sue, mentre se le due cose
calano allo stesso ritmo si sta solo limitando a seguire il ciclismo giovanile italiano.

Dall'ingresso in Esordienti all'Under 23 resta il **16,6% dei tesserati** e il 17,2% dei
classificati, calcolati per anno di età in modo da poterli confrontare. Praticamente lo stesso
numero.

Il confronto diventa interessante per via di un terzo numero, che invece non combacia:
seguendo le singole persone anziché i conteggi, solo il 59,6% di chi era in Esordienti si
ritrova in Allievi. La distanza fra il 73% delle teste contate per stagione e il 59,6% delle
persone seguite una per una è il ricambio, e dice che la classifica tiene la propria
dimensione sostituendo gli individui invece di trattenerli. Due fonti indipendenti, la stessa
conclusione: l'imbuto individuale che vedi nella classifica è molto più ripido dell'abbandono
vero.

## La lettura sbagliata

La trappola sta nel titolo di quasi tutti gli articoli che si scrivono su questo tema, cioè
che il ciclismo giovanile perda tre ragazzi su quattro.

Quel numero esiste, ma misura il ricambio di una lista di merito e non l'abbandono di uno
sport. Sono grandezze diverse, e confonderle ha una conseguenza pratica sgradevole: fa
sembrare un fallimento del movimento quello che è in buona parte il funzionamento normale di
una classifica a posti limitati.

Tienti anche questo dettaglio: accanto ai 77 professionisti delle coorti che ho studiato —
professionista vuol dire aver corso in una squadra di primo o secondo livello entro i
venticinque anni — ci sono **108 atleti che risultavano ancora a punti dopo i ventidue anni** senza essere diventati
professionisti. Sono più numerosi dei professionisti stessi. Non tutto ciò che non è
professionismo è abbandono.

## Cosa te ne porti a casa

Un ragazzo che sparisce dalla classifica al primo anno di una categoria nuova sta molto
probabilmente ancora correndo, contro avversari di uno o due anni più grandi che gli portano
via tre posti su quattro, e nella maggioranza dei casi tornerà a farsi vedere.

Se alleni, questo ti sposta il problema. Il momento in cui presidiare la ritenzione non è dopo
una brutta stagione ma al passaggio di fascia, dove si concentra il 77% delle uscite ed è lì
che un ragazzo che sta facendo esattamente quello che deve smette di ricevere riscontri. E se
leggi una classifica, la regola pratica è una sola: l'assenza di un nome non è un giudizio su
quel nome.

Se il ricambio è così forte, però, ti viene un dubbio ragionevole: con tutta questa gente che
entra ed esce, il risultato di una stagione dirà ancora qualcosa sul futuro di un ragazzo? A
tredici anni, in particolare: si vede già qualcosa, o stiamo solo misurando chi si è
sviluppato prima? È il tema della prossima puntata.

---

> **Come lo sappiamo**
>
> I rientri si contano cercando i buchi nelle sequenze di stagioni di ogni atleta, cioè
> presente, assente, presente di nuovo. Il rinnovo delle liste confronta due classifiche
> consecutive e conta i nomi nuovi. Sono misure indipendenti fra loro.
>
> Il confronto fra passaggi interni e cambi di categoria usa soltanto transizioni che durano
> una stagione, così che l'unica differenza fra i due gruppi sia il cambio di fascia. La
> correlazione riportata è quella di Spearman, che guarda l'ordine e non i valori.
>
> Il limite principale è che tutte queste misure riguardano chi era in classifica: su chi non
> c'è mai stato, e su chi corre senza andare a punti, questi dati non dicono nulla, e
> servirebbe
> l'elenco dei tesserati per anno e per atleta, che non è pubblicamente disponibile.

[^p3attrito]: Calcolo in `report/moduli/attrito.py`.

[^p3passaggi]: Calcolo in `report/moduli/passaggi.py`.

[^p3posti]: Calcolo in `report/moduli/posti.py`, che stima i posti a punti dai piazzamenti
    nei primi cinque e li divide per annata.

[^p3continuita]: Conteggi su `tab_b` per le stagioni corse e su `tab_a` per lo scarto tipo
    del percentile, coorti in studio.

---

## Scelte aperte per questo post

**A. Quante prove riportare.** Il post ne mette quattro in fila, cioè i rientri, il rinnovo
delle liste, la lunghezza delle classifiche e il confronto con i tesserati. È la struttura a
evidenze convergenti prevista dal piano, ma quattro è al limite, e si potrebbe togliere il
confronto con i tesserati, che è il più tecnico, recuperandolo nel post 8 fra i limiti.
Consiglierei di tenerle tutte e quattro, perché è il post in cui la convergenza è
l'argomento, accorciando piuttosto la terza.

**B. Dove mettere il 77,2%.** Ora arriva a metà, come apparente prova a favore del trauma, e
viene smontato subito dopo. In alternativa potrebbe aprire il post, con una struttura più
teatrale del tipo «sembra che, invece», con il rischio però che il lettore che si ferma al
primo paragrafo si porti a casa esattamente il numero sbagliato.

**C. Quanto insistere sulla lunghezza delle liste.** È la spiegazione vera del crollo, ma è
anche il punto in cui il post diventa un discorso su come è fatta una classifica invece che
sui ragazzi. Le due varianti sono la spiegazione esplicita con i numeri delle liste, come
adesso, oppure una versione più breve con l'immagine della porta che si stringe e i numeri
relegati al riquadro finale.

**D. La chiusura.** L'attuale rimanda al post 4 sulla predittività. L'alternativa è chiudere
sui 108 atleti ancora a punti dopo i ventidue anni, che è emotivamente più forte, perché
mostra come esistano carriere che non finiscono in professionismo e non sono fallimenti, ma
sposta il tema e sottrae materiale al post 8.

**E. Il titolo.** «Sparire dalla classifica non è smettere» dice già tutto, forse troppo.
Alternative: «Un terzo di quelli che spariscono torna»; «La porta si stringe, non è il salto».
