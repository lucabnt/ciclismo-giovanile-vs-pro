# 2. Di chi stiamo parlando

> ⚠️ **Bozza scritta a mano. Non si rigenera.** Ogni cifra è copiata dall'analisi al momento
> della stesura, quindi se i dati vengono aggiornati questo testo non se ne accorge. Prima
> di pubblicare conviene eseguire `python scripts/11_verifica_documenti.py`, che confronta
> le cifre del post con l'archivio dei risultati. Sullo stile: [`STILE.md`](STILE.md).
>
> **Numero chiave del post:** 1 su 7.
> **Moduli:** `provenienza`, `copertura`, `attrito` (l'imbuto), `misura`, `posti`.
> **Figure:** `copertura_tesserati`, `attrito_imbuto`, `misura_rapporto`,
>   `posti_concentrazione`.

---

*Seconda puntata. Nella prima ho raccontato cosa dice la letteratura; qui comincio a
guardare i miei dati, partendo dalla domanda più noiosa e più importante di tutte, cioè di
chi stiamo parlando esattamente.*

> 📷 **Immagine da procurare (copertina):** il tavolo della giuria a fine gara, con i fogli
>   dell'ordine di arrivo, fotografati in modo che i nomi non siano leggibili.
> *Didascalia proposta:* Tutto lo studio parte da qui: una classifica costruita sui primi
>   cinque di ogni gara, che non è l'elenco dei giovani ciclisti italiani.
> *Testo alternativo:* Fogli dell'ordine di arrivo appoggiati sul tavolo della giuria.

C'è una frase che salta fuori ogni volta che si discute di questi numeri, e che è quasi
sempre sbagliata: su mille giovani ciclisti italiani, trentacinque diventano professionisti.
Il numero è giusto. È «giovani ciclisti italiani» a non esserlo per niente.

Lo studio parte da una classifica, quella che ciclismo.info pubblica ogni anno per ogni
categoria giovanile, e che nel periodo considerato raccoglie 28 041 piazzamenti stagionali
di 11 098 ragazzi, dal 2007 al 2025. È l'archivio più completo che esista sul ciclismo
giovanile italiano, ma non è l'elenco dei giovani ciclisti italiani, perché per entrarci
devi aver fatto almeno un punto, e i punti li prendono solo i primi cinque di ogni gara:
cinque alla vittoria e a scendere fino a uno al quinto posto. Comparire lì dentro anche con
un punto solo vuol dire quindi essere arrivato almeno una volta nei primi cinque. Non è un
tesseramento, è un risultato.

E non è nemmeno una deduzione, perché si può controllare, e l'ho fatto: tutte le 28 041
righe della classifica hanno almeno un piazzamento nei primi cinque, senza una sola
eccezione.

## Uno su sette

La Federazione pubblica ogni anno quanti sono i tesserati per categoria, e mettendo i due
conteggi uno accanto all'altro, per le stagioni in cui esistono entrambi, viene fuori la
risposta.

| categoria | tesserati per stagione | in classifica | quota |[^p2copertura]
|---|---|---|---|
| Esordienti | 3 214 | 497 | 15,5% |
| Allievi | 2 673 | 371 | 13,9% |
| Juniores | 1 687 | 262 | 15,5% |
| Under 23 | 1 060 | 162 | 15,3% |

> 🖼️ **Figura: `copertura_tesserati.png`**
> *Didascalia proposta:* La barra è la media delle stagioni, la linea va dalla più bassa alla
>   più alta. Nel conteggio dei tesserati c'è anche chi corre altre specialità, quindi uno su
>   sette semmai sovrastima la copertura.
> *Testo alternativo:* Barre per categoria con la quota di tesserati presenti in classifica,
>   tutte attorno al quindici per cento.

In classifica ci finisce **circa un tesserato su sette**, e la cosa che colpisce non è il
valore in sé ma quanto stia fermo: quattro categorie e otto stagioni, sempre lo stesso
ordine di grandezza, in una forbice fra il 12,2% e il 17,2%. Non è l'effetto di un anno
strano o di una categoria particolare, è proprio come funziona il sistema.

Gli altri sei su sette corrono senza mai andare a punti, oppure corrono in una specialità
diversa dalla strada: la tessera è per categoria e non per disciplina, quindi un Esordiente
che fa solo mountain bike è dentro quel conteggio pur non potendo comparire in nessuna
classifica su strada. Il che vuol dire che uno su sette, semmai, sovrastima la copertura
vera. Insomma, la classifica non è un censimento del ciclismo giovanile ma la punta che
emerge, ed è di quella punta che ti sto parlando.

## Due classifiche, o una sola

Un'ultima cosa sulla struttura, che serve più avanti e che quasi nessuno sa. Negli
Esordienti la fonte pubblica **due classifiche separate**, una per annata: primo e secondo
anno corrono gare loro e non si fanno concorrenza. Dagli Allievi in su la classifica è **una
sola** e le due annate ci convivono, correndo le stesse gare.

Sembra un dettaglio da archivio e invece cambia la lettura di parecchie cose, perché nelle
categorie a lista unica un ragazzo al primo anno gareggia contro chi ha un anno di sviluppo
in più. I posti a punti se li prendono i più grandi: in Allievi il primo anno ne vince il
**26,7%**, contro il 49,7% degli Esordienti dove le liste sono separate.[^p2posti] Ci torno
nella prossima puntata, perché è la chiave di un equivoco piuttosto diffuso.

E già che siamo sui numeri della classifica, una risposta alla domanda che si fanno tutti
guardandola: sì, si piazzano sempre gli stessi. Il dieci per cento migliore si prende fra il
37% e il 43% dei punti della categoria. La cosa curiosa è che questa quota **non cambia
salendo di categoria**: è la stessa a tredici anni e a ventidue, per cui la selezione non si
stringe con l'età, ha già quella forma fin dall'inizio.

> 🖼️ **Figura: `posti_concentrazione.png`**
> *Didascalia proposta:* Il dieci per cento migliore prende quattro punti su dieci in ogni
>   categoria. È la stessa forma anche fra le ragazze, come racconta l'ottava puntata.
> *Testo alternativo:* Andamento quasi piatto della quota di punti presa dal decile migliore,
>   categoria per categoria.

## L'imbuto, e come non leggerlo

Adesso che sai di chi si parla, possiamo guardare l'attrito. Le coorti principali sono i
nati fra il 1996 e il 2000, che hanno avuto tutti il tempo di arrivare o di non arrivare, e
sono
**2 817 ragazzi, 77 professionisti**. Professionista, in tutta questa serie, vuol dire aver
corso in una squadra di primo o secondo livello entro i venticinque anni: la finestra d'età
serve a rendere confrontabili annate diverse, e chi arriva più tardi qui non risulta.

| categoria | atleti | quota di chi era in Under 15 |[^p2attrito]
|---|---|---|
| Under 15 | 2 187 | 100% |
| Under 17 | 1 741 | 59,6% |
| Under 19 | 1 051 | 34,1% |
| Under 23 | 342 | 10,2% |
| professionisti | 77 | 3,5% |

> 🖼️ **Figura: `attrito_imbuto.png`**
> *Didascalia proposta:* Il primo scalino non è «tutti i giovani ciclisti italiani»: è chi a
>   tredici anni era già arrivato almeno una volta nei primi cinque. Tre ordini di grandezza
>   separano quello scalino dall'ultimo.
> *Testo alternativo:* Imbuto a scalini che si restringe dagli Under 15 ai professionisti.

Da poco più di duemila ragazzi si arriva a settantasette, cioè trentacinque su mille, con
tre ordini di grandezza fra l'inizio e la fine.

Sembra un imbuto, e in parte lo è, però ha una proprietà che rovina le letture semplici,
perché non è una catena di sottoinsiemi. Fra un quarto e un terzo degli atleti di ogni
categoria non è mai comparso in Under 15, e in Under 23 sono più di uno su tre: sono ragazzi
entrati nel ranking più tardi. Se leggi l'imbuto come «di quei duemila ne sono rimasti
trecento», stai contando fra i sopravvissuti gente che non era mai partita.

## Il denominatore, che è la trappola vera

Mettendo insieme le due cose si arriva al punto in cui quasi tutti sbagliano.

Quel 3,5% non è la probabilità che un ragazzo che comincia a correre diventi professionista.
È la probabilità che ci arrivi uno che a tredici anni era già andato almeno una volta nei
primi cinque in una gara. Il denominatore, cioè, è già stato scremato una volta.

Rispetto a tutti i tesserati la quota sarebbe molto più bassa, grosso modo sette volte, se
la copertura di oggi valesse anche allora. Quella moltiplicazione però non l'ho fatta, e te
lo racconto perché è una decisione e non una dimenticanza. I dati sui tesserati esistono
solo dal 2018, mentre le coorti che ho studiato correvano prima, e trasferire il rapporto da
un periodo all'altro sarebbe una stima travestita da misura.

Non è una preoccupazione teorica, per giunta. Ho provato a stimare all'indietro gli anni che
mancano e poi a controllare il risultato sugli anni che invece conosco, e il metodo
**sbaglia del 27% a due anni di distanza**. C'è di peggio: stimando la tendenza in due modi
entrambi difendibili, cioè includendo o escludendo le stagioni della pandemia, i tesserati
Esordienti del 2012 vengono 5 554 oppure 3 576. Una differenza di 1,6 volte che non viene
dai dati ma da una scelta di chi fa il conto.

Il numero quindi resta quello che è, con la sua etichetta attaccata: trentacinque su mille
fra chi era già in classifica. Se lo trovi citato senza l'etichetta, sta dicendo un'altra
cosa.

## Cosa misura, di preciso, quella classifica

Vale un momento in più fermarsi sullo strumento, perché nel 2025 due ricercatori olandesi
hanno pubblicato la critica più efficace che si potesse muovere a uno studio come il
mio.[^p2hasselaar]

Hanno preso due ciclisti, uno che correva gare internazionali e uno che correva soprattutto
gare locali, che nel ranking della federazione olandese avevano lo stesso identico
punteggio: 414 punti. In una metrica costruita per tenere conto del livello delle gare
quegli stessi due valevano 76 e 21, cioè un fattore quasi quattro nascosto dentro un
pareggio. Il motivo è che il ranking olandese non conta i risultati internazionali, e quindi
dà zero punti proprio alle gare più difficili. La critica colpisce in pieno chiunque usi un
ranking federale come misura, me compreso, e meritava una verifica invece di una risposta a
parole.

La prima metà non ci riguarda, perché la classifica italiana pesa le gare per livello: nelle
categorie con calendario internazionale, cioè Juniores e Under 23, una gara nazionale vale
il doppio di una regionale e una internazionale il triplo. Il dettaglio delle singole gare
non ce l'ho, ma la conseguenza si vede lo stesso, e basta dividere i punti per il numero di
piazzamenti nei primi cinque.

| categoria | punti per piazzamento |[^p2misura]
|---|---|
| Under 15 | 2,67 |
| Under 17 | 2,73 |
| **Under 19** | **3,02** |
| **Under 23** | **4,17** |

> 🖼️ **Figura: `misura_rapporto.png`**
> *Didascalia proposta:* I moltiplicatori delle gare non sono nei dati, e si vedono solo
>   dividendo i punti per il numero di piazzamenti: è un modo indiretto di controllare che la
>   scala faccia quello che dichiara.
> *Testo alternativo:* Barre dei punti per piazzamento, in crescita dalle categorie piccole
>   all'Under 23.

Il salto cade esattamente fra Allievi e Juniores, cioè dove i moltiplicatori entrano in
funzione. È una conferma indiretta ma pulita: la scala fa quello che dichiara di fare.

La seconda metà della critica, invece, resta in piedi. Un ranking premia comunque chi va
forte nelle tipologie di gara più frequenti in calendario, per cui uno scalatore, in un
calendario fatto soprattutto di percorsi veloci, ha meno occasioni di andare a punti. Per
correggerlo servirebbe il dettaglio gara per gara, che non è pubblico: è un limite che mi
porto dietro dalla fonte, e conviene che tu lo tenga presente ogni volta che leggi un
piazzamento come se fosse una misura del valore di un atleta.

Nel verificare tutto questo è saltato fuori un terzo problema, che gli olandesi non
sollevano. Con una scala che va da cinque a un punto i totali possibili sono pochi e i
ragazzi tanti, al punto che **fino al 95% dei classificati condivide il proprio punteggio
con qualcun altro**. Il problema me lo aspettavo, e avevo deciso di sciogliere i pari merito
guardando prima le vittorie, poi i secondi posti e così via, decisione presa prima di
guardare qualunque esito. Messa alla prova, però, quella raffinatezza non migliora la
previsione in nessuna categoria: a parità di punti, il modo in cui li hai presi non aggiunge
niente, e cinque punti fatti con una vittoria valgono quanto cinque punti fatti con cinque
quinti posti.[^p2misura]

Questo apre una domanda che mi hanno fatto più volte, e che vale la pena chiudere qui. Nelle
categorie piccole le gare sono corte e quasi sempre pianeggianti, quindi a vincere tendono a
essere i ragazzi esplosivi, quelli con lo spunto veloce. Se fosse un fenotipo che non porta
lontano, dovremmo vedere che **a parità di punti** chi vince di più arriva di meno. Ho
guardato: prendendo atleti con esattamente lo stesso punteggio nella stessa stagione e
confrontando chi ha una quota di vittorie sopra e sotto la mediana, in Esordienti il tasso
di professionismo è identico (1,7% contro 1,8%), in Allievi va peggio chi vince di più (1,0%
contro 2,2%) e in Juniores meglio (4,7% contro 2,8%, ma su 43 casi). Nessun andamento
coerente: né conferma né smentita, e i numeri sono troppo piccoli per pretendere di
più.[^p2vittorie]

Va detto anche perché la domanda resta aperta sul serio: il profilo delle gare, cioè
lunghezza e altimetria, non è nei dati. Per rispondere davvero servirebbe sapere che gara
era quella in cui hai vinto, e quell'informazione non è pubblicamente disponibile.

## Cosa te ne porti a casa

Tre cose, e valgono per tutto il resto della serie.

Ogni percentuale che leggerai ha come denominatore un settimo dei ragazzi tesserati e non la
loro totalità, per cui le quote vere sono più basse di quelle che trovi scritte. Di quanto
esattamente non lo so, e chi ti dice di saperlo sta estrapolando.

L'imbuto non è una catena: una parte consistente di chi si trova in una categoria non c'era
in quella prima. Entrare tardi è normalissimo.

E la classifica misura quanto sei andato a punti in Italia, con le gare pesate per livello
dai Juniores in su. È una misura onesta e grossolana: buona per ordinare, insufficiente per
giudicare.

Restano poi quei 1 845 ragazzi che si perdono per strada fra l'Under 15 e l'Under 23, e la
domanda ovvia è se abbiano smesso di correre. La risposta è no, e il modo in cui si dimostra
è la parte più sorprendente di tutta questa ricerca. È il tema della prossima puntata.

---

> **Come lo sappiamo**
>
> Le classifiche vengono da ciclismo.info, stagioni 2007-2025, raccolte da un progetto
> separato che ne mantiene lo scaricamento
> ([risultati-ciclismo-giovanile](https://github.com/lucabnt/risultati-ciclismo-giovanile)).
> I tesserati vengono dai dati statistici pubblicati dalla Federazione Ciclistica Italiana e
> coprono le stagioni 2018-2025, perché prima di allora non sono pubblici.
>
> Le due serie non sono perfettamente allineate, in quanto il tesseramento è per categoria e
> non per specialità: la copertura calcolata è quindi un limite inferiore, perché confronta
> i classificati su strada con tutti i tesserati di quella categoria, compreso chi corre
> solo fuoristrada.
>
> Il confronto fra le due versioni del percentile e il test sui pari merito stanno in
> [R/30_misura.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/30_misura.R); l'esperimento di estrapolazione all'indietro è nella sezione «Si possono
> stimare gli anni che mancano?» del documento completo.

[^p2copertura]: Calcolo in [report/moduli/copertura.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/copertura.py), dai tesserati raccolti in
    [riferimenti/tesserati_fci.csv](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/riferimenti/tesserati_fci.csv).

[^p2attrito]: Calcolo in [report/moduli/attrito.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/attrito.py).

[^p2misura]: Calcolo in [R/30_misura.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/30_misura.R), reso da [report/moduli/misura.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/misura.py).

[^p2posti]: Calcolo in [report/moduli/posti.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/posti.py).

[^p2hasselaar]: Hasselaar M., Elferink-Gemser M.T. (2025), *How to quantify youth cycling
    performance? Development of a method based on competition results*, Current Issues in
    Sport Science 10(1), articolo 012. DOI
    [10.36950/2025.10ciss012](https://doi.org/10.36950/2025.10ciss012). Ad accesso aperto.

[^p2vittorie]: Confronto a parità esatta di punteggio dentro la stessa stagione, sui
    classificati al secondo anno di categoria delle coorti in studio. Non entra nel
    documento generato: è una verifica fatta apposta per questa domanda.

---

## Scelte aperte per questo post

**A. Il post è lungo e contiene due temi.** «Chi c'è dentro la classifica» e «cosa misura la
classifica» sono argomenti imparentati ma distinti, e ci sono tre strade. Lasciarli insieme
come ora, con il vantaggio che il lettore incontra lo strumento una volta sola e non ci
torna più. Spostare la parte sulla misura nel post 4, dove il percentile comincia a essere
usato per predire, il che la avvicina all'uso ma appesantisce un post già denso. Oppure
farne un post a sé, portando la serie a nove: ha materiale sufficiente, fra i due ciclisti
olandesi, i moltiplicatori e i pari merito, e un risultato controintuitivo tutto suo. Se la
serie può permettersi nove puntate consiglierei quest'ultima, perché la storia dei 414 punti
identici è troppo buona per stare in mezzo a un altro discorso.

**B. Il tono sulla moltiplicazione non fatta.** Ora è raccontata come una scelta metodologica
di cui andare orgogliosi. Si può anche tagliarla, limitandosi a dire che il dato non c'è,
oppure tenerla spostandola nel riquadro finale per non spezzare il ritmo. Tenerla nel corpo
costa circa centocinquanta parole e in cambio dà al lettore un esempio concreto di cosa
significhi non barare con i numeri, che è metà del messaggio della serie.

**C. Quale figura mettere in apertura.** Le candidate sono `copertura_tesserati`, che porta il
numero chiave, e `attrito_imbuto`, che è più spettacolare per via dei tre ordini di
grandezza. Se il post apre con l'imbuto, però, il lettore incontra la conclusione prima del
denominatore, che è esattamente l'errore che il post vuole correggere: meglio la copertura
in apertura e l'imbuto a metà. I segnaposto nel testo seguono già questa scelta, e
spostarli vuol dire spostare due blocchi.

**D. La frase iniziale.** Il post apre smentendo una frase molto diffusa, il che è efficace e
un filo polemico. L'alternativa più fredda è aprire con la regola dei primi cinque e
arrivare alla smentita soltanto alla fine.
