# 2. Di chi stiamo parlando

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra qui dentro è copiata dall'analisi al momento della stesura. Se i dati vengono
> aggiornati, questo testo **non se ne accorge**. Prima di pubblicare:
> `python scripts/11_verifica_documenti.py`, che confronta le cifre di questo post con
> l'archivio dei risultati. Le affermazioni qualitative restano da rileggere a mano.
>
> **Numero chiave del post:** 1 su 7.
> **Moduli:** `provenienza`, `copertura`, `attrito` (l'imbuto), `misura`.
> **Figure:** `copertura_tesserati`, `attrito_imbuto`, `misura_rapporto`.

---

C'è una frase che ricorre ogni volta che si parla di questi numeri, ed è quasi sempre
sbagliata: *«su mille giovani ciclisti italiani, trentacinque diventano professionisti»*.

Il numero è giusto. È la parola «giovani ciclisti italiani» a non esserlo.

Questo studio parte da una classifica: quella che il portale ciclismo.info pubblica ogni
anno per ogni categoria giovanile. 28 041 piazzamenti stagionali, 11 098 ragazzi,
dal 2007 al 2025. È l'archivio più completo che esista sul
ciclismo giovanile italiano, e non è l'elenco dei giovani ciclisti italiani.

Per entrarci bisogna aver fatto **almeno un punto**. E i punti li assegnano solo i primi
cinque di ogni gara: cinque alla vittoria, quattro al secondo, giù fino a uno al quinto.
Comparire in quella classifica anche con un solo punto, quindi, significa **essere arrivati
almeno una volta nei primi cinque**. Non è un tesseramento, è un risultato.

Lo si può verificare invece che dedurlo, e lo abbiamo fatto: **tutte** le 28 041 righe della
classifica hanno almeno un piazzamento nei primi cinque. Nessuna eccezione.

## La domanda

**Quando diciamo «i giovani ciclisti italiani», chi stiamo contando?**

## Uno su sette

La Federazione Ciclistica Italiana pubblica ogni anno quanti sono i tesserati per categoria.
Mettendo i due numeri uno accanto all'altro, per le stagioni in cui esistono entrambi, si
ottiene la risposta.

| categoria | tesserati per stagione | in classifica | quota |
|---|---|---|---|
| Esordienti | 3 214 | 497 | 15,5% |
| Allievi | 2 673 | 371 | 13,9% |
| Juniores | 1 687 | 262 | 15,5% |
| Under 23 | 1 060 | 162 | 15,3% |

**In classifica compare circa un tesserato su sette**, e la cosa notevole non è il valore
ma la sua stabilità: quattro categorie, otto stagioni, sempre lo stesso ordine di
grandezza, in una forbice fra il 12,2% e il 17,2%. Non è l'effetto di un anno strano o di
una categoria particolare. È come funziona il sistema.

Gli altri sei su sette corrono senza mai entrare a punti, oppure corrono in una specialità
diversa dalla strada — la tessera è per categoria, non per disciplina, quindi un Esordiente
che fa solo mountain bike è dentro quel conto e non comparirà mai in una classifica su
strada. Il che vuol dire che uno su sette è, se mai, una sovrastima della copertura reale.

La classifica non è un censimento del ciclismo giovanile: **è la punta che emerge.** Questo
studio parla della punta.

## L'imbuto, e come non leggerlo

Ora si può guardare l'attrito, sapendo di chi si parla. Le coorti principali sono i nati
fra il 1996 e il 2000, che hanno avuto tutti il tempo di arrivare o di non arrivare:
**2 817 ragazzi, 77 professionisti**.

| categoria | atleti | quota di chi era in Under 15 |
|---|---|---|
| Under 15 | 2 187 | 100% |
| Under 17 | 1 741 | 59,6% |
| Under 19 | 1 051 | 34,1% |
| Under 23 | 342 | 10,2% |
| professionisti | 77 | 3,5% |

Da duemila e passa ragazzi a settantasette. **Trentacinque su mille**, tre ordini di
grandezza fra l'inizio e la fine.

Sembra un imbuto e in parte lo è, ma ha una proprietà che rovina le letture semplici:
**non è una catena di sottoinsiemi**. Fra un quarto e un terzo degli atleti di ogni
categoria non è mai comparso in Under 15 — sono ragazzi entrati più tardi. In Under 23 sono
più di uno su tre. Chi legge l'imbuto come «di quei duemila, ne sono rimasti trecento» sta
contando fra i sopravvissuti persone che non erano mai partite.

## La trappola: il denominatore

Adesso mettiamo insieme le due cose, perché è qui che quasi tutti sbagliano.

Quel 3,5% non è la probabilità che un ragazzo che comincia a correre diventi
professionista. È la probabilità che ci arrivi **uno che a tredici anni era già andato
almeno una volta nei primi cinque in una gara**. Il denominatore è già selezionato una
volta.

Rispetto a tutti i tesserati la quota sarebbe molto più bassa — grosso modo sette volte, se
la copertura di oggi valesse anche allora. E qui c'è la parte che vale la pena raccontare,
perché è una decisione presa e non un'omissione: **quella moltiplicazione non l'abbiamo
fatta**.

Il motivo è che i dati sui tesserati esistono solo dal 2018, mentre le coorti studiate
correvano prima. Trasferire il rapporto da un periodo all'altro sarebbe una stima travestita
da misura. E non è una preoccupazione teorica: abbiamo provato a stimare all'indietro gli
anni mancanti e poi a controllare il risultato sugli anni che invece conosciamo. **Sbaglia
del 27% a due anni di distanza.** Peggio ancora, stimando la tendenza in due modi entrambi
difendibili — includendo o escludendo le stagioni della pandemia — i tesserati Esordienti
del 2012 risultano 5 554 oppure 3 576. Una differenza di 1,6 volte che non viene dai dati:
viene da una scelta di chi fa il conto.

Quindi il numero resta quello che è, con la sua etichetta attaccata: **trentacinque su mille
fra chi era già in classifica.** Se qualcuno lo cita senza l'etichetta, sta dicendo un'altra
cosa.

## E quella classifica, cosa misura esattamente?

Vale la pena fermarsi ancora un momento sullo strumento, perché nel 2025 due ricercatori
olandesi hanno pubblicato la critica più efficace che si potesse fare a studi come questo.

Hanno preso due ciclisti. Uno correva gare internazionali, l'altro soprattutto gare locali.
Nel ranking della federazione olandese avevano **lo stesso identico punteggio: 414 punti**.
In una metrica costruita per tenere conto del livello delle gare, gli stessi due valevano
76 e 21. Un fattore quasi quattro, nascosto dentro un pareggio.

La ragione è che il ranking olandese non conta i risultati internazionali, e quindi assegna
zero punti proprio alle gare più difficili. La critica colpisce in pieno chiunque usi un
ranking federale come misura — noi compresi. Meritava una verifica, non una risposta a
parole.

**La prima metà non ci riguarda.** La classifica italiana pesa le gare per livello: nelle
categorie con calendario internazionale — Juniores e Under 23 — una gara nazionale vale il
doppio di una regionale e una internazionale il triplo. Non abbiamo il dettaglio delle
singole gare, ma la conseguenza si vede lo stesso, e basta dividere i punti per il numero di
piazzamenti nei primi cinque:

| categoria | punti per piazzamento |
|---|---|
| Under 15 | 2,67 |
| Under 17 | 2,73 |
| **Under 19** | **3,02** |
| **Under 23** | **4,17** |

Il salto è esattamente fra Allievi e Juniores, cioè dove i moltiplicatori entrano in
funzione. La scala fa quello che dichiara di fare.

**La seconda metà, invece, resta in piedi.** Un ranking premia comunque chi eccelle nelle
tipologie di gara più frequenti in calendario: chi va forte in salita, in un calendario
fatto soprattutto di percorsi veloci, ha meno occasioni di andare a punti. Servirebbe il
dettaglio gara per gara, che non è pubblico. È un limite che ereditiamo e che va tenuto in
mente ogni volta che si legge un piazzamento come se fosse una misura del valore di un
atleta.

E poi ne abbiamo trovata una terza, che nessuno aveva sollevato. Con una scala da cinque a
un punto, i totali possibili sono pochi e i ragazzi tanti: **fino al 95% dei classificati
condivide il proprio punteggio con qualcun altro**. Avevamo previsto il problema e deciso —
prima di guardare qualunque risultato — di sciogliere i pari merito guardando prima le
vittorie, poi i secondi posti, e così via. Messa alla prova, quella raffinatezza **non
migliora la previsione in nessuna categoria**. A parità di punti, il modo in cui sono stati
ottenuti non aggiunge nulla: cinque punti presi con una vittoria e cinque punti presi con
cinque quinti posti danno le stesse probabilità di arrivare.

## Cosa se ne ricava

Tre cose, e valgono per tutto il resto della serie.

Ogni percentuale che leggerete ha come denominatore **un settimo dei ragazzi tesserati**,
non tutti. Le quote reali sono più basse di quelle riportate, quanto esattamente non lo
sappiamo, e chi vi dice di saperlo sta estrapolando.

L'imbuto non è una catena: una parte consistente di chi c'è in una categoria non c'era in
quella prima. Entrare tardi è normale.

E la classifica misura quanto si è andati a punti in Italia, con gare pesate per livello
dagli Juniores in su. È una misura onesta e grossolana: buona per ordinare, insufficiente
per giudicare.

## Il gancio

Restano quei 1 845 ragazzi che si perdono per strada fra l'Under 15 e l'Under 23. Hanno
smesso di correre?

No. E il modo in cui si dimostra è la parte più sorprendente di tutta questa ricerca.

---

> **Come lo sappiamo**
>
> Le classifiche vengono da ciclismo.info, stagioni 2007-2025, raccolte da un progetto
> separato che ne mantiene lo scaricamento
> ([risultati-ciclismo-giovanile](https://github.com/lucabnt/risultati-ciclismo-giovanile)).
> I tesserati vengono dai dati statistici pubblicati dalla Federazione Ciclistica Italiana e
> coprono le stagioni 2018-2025: prima di allora non sono pubblici.
>
> Le due serie non sono perfettamente allineate — il tesseramento è per categoria e non per
> specialità — quindi la copertura calcolata è un **limite inferiore**: i classificati su
> strada sono confrontati con tutti i tesserati di quella categoria, anche chi corre solo
> fuoristrada.
>
> Il confronto fra le due misure del percentile e il test sui pari merito sono in
> `R/30_misura.R`; l'esperimento di estrapolazione all'indietro è nella sezione «Si possono
> stimare gli anni che mancano?» del documento completo.

---

## Scelte aperte per questo post

**A. Il post è lungo, e contiene due temi.** «Chi c'è dentro la classifica» e «cosa misura
la classifica» sono parenti ma non identici. Tre strade:

1. **lasciarli insieme** come ora (~1 800 parole, il post più lungo della serie): il
   vantaggio è che il lettore incontra lo strumento una volta sola e non ci torna più;
2. **spostare la parte sulla misura nel post 4**, dove si comincia a usare il percentile per
   predire: più vicino all'uso, ma il post 4 è già denso;
3. **farne un post a sé** — «Lo stesso punteggio è lo stesso risultato?» — portando la serie
   a nove. Ha materiale sufficiente (i due ciclisti olandesi, i moltiplicatori, i pari
   merito) e un risultato controintuitivo tutto suo. **È l'opzione che consiglierei se la
   serie può permettersi nove post**: la storia dei 414 punti identici è troppo buona per
   stare in mezzo a un altro discorso.

**B. Il tono sul «non abbiamo fatto la moltiplicazione».** Ora è raccontato come una scelta
metodologica orgogliosa. Si può anche: (a) tagliarlo e limitarsi a dire che il dato non
c'è; (b) tenerlo ma spostarlo nel riquadro finale, per non spezzare il ritmo. Tenerlo nel
corpo costa circa 150 parole e in cambio dà al lettore un esempio concreto di cosa
significhi non barare con i numeri — che è metà del messaggio della serie.

**C. Quale figura mettere in apertura.** `copertura_tesserati` (uno su sette, il numero
chiave) oppure `attrito_imbuto` (più spettacolare, tre ordini di grandezza). Se il post
apre con l'imbuto, però, il lettore incontra la conclusione prima del denominatore, che è
esattamente l'errore che il post vuole correggere. Consiglio: copertura in apertura, imbuto
a metà.

**D. La frase iniziale.** Ora il post apre smentendo una frase («su mille giovani ciclisti
italiani…»). È efficace ma leggermente polemica. Alternativa più fredda: aprire con la
regola dei primi cinque, e arrivare alla smentita in fondo.
