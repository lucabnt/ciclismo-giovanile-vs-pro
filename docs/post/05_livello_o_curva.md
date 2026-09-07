# 5. Il livello o la curva?

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio se
> i dati cambiano. Prima di pubblicare conviene eseguire
> `python scripts/11_verifica_documenti.py`. Sullo stile: [`STILE.md`](STILE.md).
>
> **Numeri chiave del post:** 20,7% contro 2,1%.
> **Moduli:** `traiettorie`.
> **Figure:** `traiettorie_incrocio`.

---

*Quinta puntata. Nella precedente ho mostrato che il piazzamento in classifica dice qualcosa
già a tredici anni; qui provo a rispondere alla domanda che in società ci si fa più spesso,
cioè se conti di più dove sei o dove stai andando.*

Due ragazzi, sedici anni tutti e due. Il primo è sempre stato lì, da tre stagioni attorno al
settantacinquesimo percentile della sua categoria: regolare, nessuna sorpresa, nessun crollo.
Il secondo tre anni fa era al quarantesimo, poi cinquantacinquesimo, poi settantesimo, e
adesso è al novantesimo. Se dovessi puntare su uno solo, quale sceglieresti?

Per una volta i dati possono risponderti davvero, perché le classifiche giovanili sono una
serie storica, e da una serie storica leggi non solo dove uno sta ma anche dove sta andando. I
due ragazzi dell'esempio non esistono, questo va detto; i numeri che seguono sì.

## Come si separa il livello dalla direzione

A ogni ragazzo si può adattare una retta che descrive il suo percentile in funzione dell'età,
e due numeri la riassumono: il livello, cioè dove passa la retta a metà del percorso
giovanile, e la pendenza, cioè quanto sale o scende ogni anno.

C'è però una precauzione da prendere, ed è il motivo per cui l'analisi non è banale. Un
ragazzo con due sole stagioni osservate avrebbe una pendenza calcolata su due punti, cioè
rumore travestito da tendenza. Il modello che ho usato stima tutte le rette insieme e tira
quelle basate su pochi dati verso la media della popolazione, così che chi ha poche stagioni
riceva una pendenza prudente. È il comportamento giusto, ma va saputo, perché vuol dire che le
traiettorie più marcate appartengono per costruzione a chi ha corso di più. Ci torno fra poco,
perché è esattamente il tipo di trappola in cui questa serie è già inciampata una volta.

## La risposta, in due coefficienti

| | quanto moltiplica le probabilità |[^p5traiettorie]
|---|---|
| dieci posizioni percentuali di livello in più | **×3,02** |
| una deviazione standard di miglioramento annuo | **×3,35** |

Contano tutti e due, quindi, e il miglioramento non è affatto il parente povero: un modello
che conosce solo il livello mette davanti il futuro professionista in circa 85 casi su 100,
mentre aggiungendo la pendenza si sale a 92. Non è informazione ridondante, perché sapere dove
sta andando un ragazzo ti dice qualcosa che il suo livello attuale non ti dice.

## La stessa risposta senza coefficienti

I coefficienti hanno il difetto di essere astratti, e la stessa cosa si vede molto meglio
dividendo i ragazzi in tre gruppi per livello e tre per miglioramento, e contando quanti sono
arrivati in ciascuna delle nove caselle.

| | miglioramento basso | medio | alto |[^p5traiettorie]
|---|---|---|---|
| **livello alto** | 2,1% | 13,2% | **20,7%** |
| **livello medio** | 0,0% | 0,9% | 5,9% |
| **livello basso** | 1,1% | 0,0% | 0,7% |

La tabella si legge in due direzioni, e le due letture insieme sono la risposta del post.

In orizzontale, lungo la riga alta: fra i ragazzi di livello alto, chi stava anche migliorando
è diventato professionista nel **20,7%** dei casi — professionista vuol dire aver corso in una
squadra di primo o secondo livello entro i venticinque anni — mentre chi stava calando si è fermato al
**2,1%**. Dieci volte meno, a parità di livello. La direzione conta, e conta moltissimo.

In verticale invece si vede che fra i ragazzi in forte crescita si passa dallo 0,7% del
livello basso al 20,7% del livello alto, e che la riga bassa è praticamente piatta: nel terzo
con il livello più basso il miglioramento non salva quasi nessuno.

Poi c'è una casella che da sola vale tutto il post, cioè quella dei ragazzi di livello medio
in forte crescita, che sta al **5,9%** ed è più alta di quella dei ragazzi di livello alto con
la pendenza in calo, ferma al 2,1%. Detto altrimenti: il ragazzo mediocre che sta salendo
batte il ragazzo forte che sta scendendo. Con la precisazione che quella casella poggia su 187
atleti e 11 professionisti, quindi prendila come indicazione e non come stima precisa.

La frase da portarsi via è che il livello è una condizione e il miglioramento un
moltiplicatore: senza il primo il secondo non basta, con il primo il secondo cambia tutto.

## Non sarà di nuovo la durata della carriera?

Nel post successivo vedrai un caso da manuale di variabile che sembra spiegare e invece
descrive, cioè i cambi di società. Qui il sospetto è lo stesso ed è tecnicamente fondato,
perché il modello assegna pendenze prudenti a chi ha poche stagioni: una pendenza marcata è
quindi anche un indizio di carriera lunga, e una carriera lunga ovviamente correla con
l'arrivare. Non è che sto misurando chi è rimasto di più e lo sto chiamando chi migliorava?

Il controllo si fa aggiungendo al modello il numero di stagioni osservate: se il miglioramento
fosse un travestimento della durata, il suo coefficiente crollerebbe. Passa invece da 3,35 a
**3,09**, cioè si riduce e resta grande. Questa volta il gradiente non è un travestimento
della durata della carriera, e il fatto che io sappia distinguere i due casi, avendo trovato
anche l'altro, è la ragione per cui il controllo andava fatto.

Sul modo in cui uso il numero di stagioni, una precisazione: serve come verifica e non entra
nel modello principale, perché chi va bene resta di più e la durata sta quindi in mezzo fra il
rendimento e l'esito. Metterla fra i controlli sottrarrebbe una parte dell'effetto che voglio
misurare, e lo farebbe sembrare più debole di quanto sia.

## Un limite che va detto

Le pendenze di questo post sono stimate su chi ha almeno due stagioni in classifica, cioè
**1 903 ragazzi, fra cui 74 professionisti**, perché sotto le due stagioni una direzione non
esiste, e non è una scelta metodologica ma una constatazione.

Vuol dire che di un ragazzo alla sua prima stagione a punti questo post non ti dice niente:
per lui c'è solo il livello. Ed è la situazione di quasi metà dei classificati, visto che 844
dei 2 747 atleti con una traiettoria stimabile hanno una sola stagione osservata. La domanda
«sta migliorando?» ha bisogno di tempo prima di poter essere posta, e non è un limite dei dati
ma della domanda.

## Cosa te ne porti a casa

Tornando ai due ragazzi dell'inizio: i dati dicono di puntare sul secondo, ma soltanto perché
il novantesimo percentile è vero. Non è la crescita in sé a valere, è la crescita che porta in
alto. Un ragazzo che passa dal ventesimo al quarantesimo percentile sta migliorando
esattamente quanto uno che passa dal settantesimo al novantesimo, e le loro probabilità non si
somigliano per niente.

Tradotto in pratica, ne esce una regola semplice per quando guardi una scheda: prima il
livello, poi la direzione. Il livello ti dice se il ragazzo è nella zona in cui la domanda ha
senso, la direzione ti dice, dentro quella zona, quanto convenga crederci. E ne esce anche una
ragione concreta per non liquidare un ragazzo di metà classifica che sta salendo, perché 5,9%
non è tanto in assoluto ma è tre volte il tasso di un suo coetaneo più forte che sta calando.

A questo punto sembrerebbe esserci tutto per costruire un criterio di selezione: prendi i più
forti, e fra questi i più in crescita. Nella prossima puntata provo a farlo davvero, e a
contare quanti ne prenderesti a vuoto.

---

> **Come lo sappiamo**
>
> Le traiettorie vengono da un modello a effetti misti stimato su 7 599 osservazioni di 2 747
> atleti, che assegna a ciascuno un livello e una pendenza individuali applicando lo
> *shrinkage*, cioè tirando verso la media le stime basate su poche stagioni.
>
> La finestra si ferma a diciotto anni, perché oltre comincia l'Under 23, dove alcuni atleti
> sono già professionisti: includere quelle stagioni significherebbe prevedere l'esito con
> osservazioni raccolte dopo che l'esito si è verificato.
>
> Livello e pendenza entrano sempre insieme nel modello, essendo correlati per costruzione: il
> percentile ha un tetto a 100, quindi chi parte alto ha meno spazio per salire, e nei dati
> quella correlazione vale −0,15.
>
> La tabella a nove caselle usa i terzili delle due dimensioni, e tre caselle contengono meno
> di cinque atleti, per cui sono riportate come sola percentuale arrotondata senza il
> conteggio.

[^p5traiettorie]: Modello misto in [R/21_traiettorie.R](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/R/21_traiettorie.R), reso da
    [report/moduli/traiettorie.py](https://github.com/lucabnt/ciclismo-giovanile-vs-pro/blob/main/report/moduli/traiettorie.py).

---

## Scelte aperte per questo post

**A. Coefficienti prima o tabella prima.** Ora il post dà i due odds ratio e poi la tabella a
nove caselle, ma si può invertire, partendo dalla tabella, che è comprensibile a chiunque, e
usando i coefficienti soltanto come conferma nel riquadro finale. Consiglierei l'inversione,
perché la tabella è la cosa migliore che questo post abbia e adesso arriva seconda.

**B. Il caso del livello medio in forte crescita.** Il 5,9% è il dato più utile per chi
allena, essendo l'unica casella che autorizzi a scommettere su un ragazzo non ancora forte, ma
poggia su 187 atleti e 11 professionisti. Nella stesura attuale la numerosità è citata nel
corpo, che è la soluzione che preferisco; le alternative sono lasciarla soltanto nel riquadro,
con più enfasi e meno prudenza, oppure ridimensionare il passaggio a osservazione di passaggio.

**C. Quanto spazio dare allo shrinkage.** È il concetto tecnicamente più ostico della serie e
occupa un paragrafo pieno. Si può ridurlo a una riga rimandando al riquadro, oppure toglierlo
del tutto dal corpo, con il rischio però che il controllo sulla durata della carriera, che
arriva poco dopo, diventi incomprensibile.

**D. I due ragazzi dell'apertura.** Sono inventati, ed è una scelta, perché in questa serie
non entrano dati personali di minori. Ora il testo lo dice esplicitamente in una riga; si può
anche lasciarlo implicito, risparmiando la riga e lasciando aperta la domanda.

**E. I numeri chiave.** Il piano indicava 20,7%, che però da solo non dice niente e va sempre
accoppiato al 2,1%. Ho messo la coppia, che funziona meglio come formula ricorrente nel titolo
e nella chiusura.
