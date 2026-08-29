# 5. Il livello o la curva?

> ⚠️ **Bozza scritta a mano. Non si rigenera.**
> Ogni cifra è copiata dall'analisi al momento della stesura e diventerà falsa in silenzio
> se i dati cambiano. Prima di pubblicare: `python scripts/11_verifica_documenti.py`.
> Le affermazioni qualitative restano da rileggere a mano.
>
> **Numero chiave del post:** 20,7%.
> **Moduli:** `traiettorie`.
> **Figure:** `traiettorie_incrocio`.

---

Due ragazzi, stessa età, sedici anni.

Il primo è sempre stato lì: da tre stagioni gira attorno al settantacinquesimo percentile
della sua categoria. Regolare, mai una sorpresa, mai un crollo.

Il secondo tre anni fa era al quarantesimo. Poi cinquantacinquesimo, poi settantesimo,
adesso novantesimo. Sale.

Se doveste puntare su uno solo, quale?

È la domanda che in società ci si fa più spesso, e per una volta i dati possono rispondere
davvero: le classifiche giovanili sono una serie storica, e da una serie storica si legge
non solo dove uno sta ma dove sta andando.

## La domanda

**Conta di più dove sei, o dove stai andando?**

## Come si separa il livello dalla direzione

A ogni ragazzo si può adattare una retta: il suo piazzamento in funzione dell'età. Due
numeri la riassumono — il **livello**, cioè dove passa la retta a metà del percorso
giovanile, e la **pendenza**, cioè quanto sale o scende ogni anno.

C'è una precauzione da prendere, ed è il motivo per cui questa analisi non è banale. Un
ragazzo con due sole stagioni osservate avrebbe una pendenza calcolata su due punti, cioè
rumore travestito da tendenza. Il modello usato qui stima tutte le rette insieme e tira
quelle basate su pochi dati verso la media della popolazione: chi ha poche stagioni riceve
una pendenza prudente. È il comportamento corretto, ma va saputo, perché significa che le
traiettorie più marcate appartengono per costruzione a chi ha corso di più.

Ci torniamo, perché è esattamente il tipo di trappola in cui questa serie è già inciampata
una volta.

## La risposta, in due coefficienti

| | quanto moltiplica le probabilità |
|---|---|
| dieci posizioni percentuali di livello in più | **×3,02** |
| una deviazione standard di miglioramento annuo | **×3,35** |

**Contano tutti e due, e il miglioramento non è il parente povero.** Un modello che conosce
solo il livello mette davanti il futuro professionista in circa 85 casi su 100; aggiungendo
la pendenza sale a 92. Non è informazione ridondante: sapere dove sta andando un ragazzo
dice qualcosa che il suo livello attuale non dice.

## La stessa risposta senza coefficienti

I coefficienti hanno il difetto di essere astratti. La stessa cosa si vede meglio dividendo
i ragazzi in tre gruppi per livello e tre per miglioramento, e contando quanti sono arrivati
in ciascuna delle nove caselle.

| | miglioramento basso | medio | alto |
|---|---|---|---|
| **livello alto** | 2,1% | 13,2% | **20,7%** |
| **livello medio** | 0,0% | 0,9% | 5,9% |
| **livello basso** | 1,1% | 0,0% | 0,7% |

Si legge in due direzioni, e le due letture insieme sono la risposta al post.

**In orizzontale**, nella riga alta: fra i ragazzi di livello alto, chi stava anche
migliorando è diventato professionista nel **20,7%** dei casi; chi stava calando, nel
**2,1%**. Dieci volte tanto, a parità di livello. La direzione conta, e conta moltissimo.

**In verticale**: fra i ragazzi che stavano migliorando molto, si passa dallo 0,7% nel
livello basso al 20,7% nel livello alto. E la riga bassa è quasi piatta: **nel terzo con il
livello più basso, il miglioramento non salva praticamente nessuno.**

C'è una casella che vale da sola tutto il post. Livello medio ma in forte crescita: **5,9%**.
È più di livello alto con la pendenza in calo, che sta al 2,1%. Il ragazzo mediocre che sta
salendo batte il ragazzo forte che sta scendendo.

La frase da portare via è questa: **il livello è una condizione, il miglioramento è un
moltiplicatore.** Senza il primo, il secondo non basta; con il primo, il secondo cambia
tutto.

## La trappola

Nel post 7 si vedrà un caso da manuale di variabile che sembra spiegare e invece descrive:
i cambi di società. Qui il sospetto è lo stesso, ed è tecnicamente fondato.

Il modello dà pendenze prudenti a chi ha poche stagioni. Quindi una pendenza marcata è
anche un indizio di carriera lunga — e una carriera lunga, ovviamente, correla con
l'arrivare. Non è che stiamo misurando «chi è rimasto di più» e chiamandolo «chi
migliorava»?

Il controllo si fa aggiungendo al modello il numero di stagioni osservate. Se il
miglioramento fosse un travestimento della durata, il suo coefficiente crollerebbe.

Passa da **3,35 a 3,09**.

Si riduce, ma resta grande. **Questa volta il gradiente non è un travestimento della durata
della carriera** — e il fatto che sappiamo distinguere i due casi, avendo trovato l'altro,
è la ragione per cui questo controllo era da fare.

Una nota su come si usa il numero delle stagioni: serve come verifica, non entra nel modello
principale. Il motivo è che chi va bene resta di più, quindi la durata sta *in mezzo* fra il
rendimento e l'esito. Metterla fra i controlli sottrarrebbe una parte dell'effetto che si
vuole misurare, facendolo sembrare più debole di quanto sia.

## Un limite che va detto

Le pendenze di questo post sono stimate su chi ha almeno due stagioni in classifica: **1 903
ragazzi, fra cui 74 professionisti**. Sotto le due stagioni una direzione non esiste, e non
è una scelta metodologica ma una constatazione.

Il che vuol dire che di un ragazzo alla sua prima stagione a punti questo post **non dice
nulla**. Per lui c'è solo il livello, ed è la situazione di quasi metà dei classificati:
844 dei 2 747 atleti con una traiettoria stimabile hanno una sola stagione osservata.

La domanda «sta migliorando?» richiede tempo per essere posta. Non è un limite dei dati: è
un limite della domanda.

## Cosa se ne ricava

Se doveste puntare su uno dei due ragazzi dell'apertura, i dati dicono: **il secondo, ma
solo se il novantesimo percentile è vero**. Non è la crescita in sé a valere — è la crescita
che porta in alto. Un ragazzo che passa dal ventesimo al quarantesimo percentile sta
migliorando esattamente quanto uno che passa dal settantesimo al novantesimo, e le loro
probabilità non si somigliano affatto.

Il che, tradotto in pratica, dà una regola semplice per chi guarda una scheda: **prima il
livello, poi la direzione**. Il livello dice se il ragazzo è nella zona in cui la domanda ha
senso; la direzione dice, dentro quella zona, quanto vale la pena crederci.

E dà anche una ragione concreta per non liquidare un ragazzo di metà classifica che sta
salendo: 5,9% non è tanto in assoluto, ma è tre volte il tasso di un suo coetaneo più forte
che sta calando.

## Il gancio

A questo punto sembra ci sia tutto per costruire un criterio di selezione: prendiamo i più
forti, fra questi i più in crescita, e abbiamo la nostra lista.

Proviamo a farlo davvero, e a contare quanti ne prendiamo a vuoto.

---

> **Come lo sappiamo**
>
> Le traiettorie vengono da un modello a effetti misti stimato su 7 599 osservazioni di
> 2 747 atleti, che assegna a ciascuno un livello e una pendenza individuali applicando lo
> *shrinkage*: le stime basate su poche stagioni vengono tirate verso la media.
>
> La finestra si ferma a diciotto anni. Oltre comincia l'Under 23, dove alcuni atleti sono
> già professionisti: includere quelle stagioni significherebbe prevedere l'esito con
> osservazioni raccolte dopo che l'esito si è verificato.
>
> Livello e pendenza entrano sempre insieme nel modello, perché sono correlati per
> costruzione — il percentile ha un tetto a 100, quindi chi parte alto ha meno spazio per
> salire. Nei dati quella correlazione vale −0,15.
>
> La tabella a nove caselle usa i terzili delle due dimensioni; tre caselle contengono meno
> di cinque atleti e sono riportate solo come percentuale arrotondata, senza il conteggio.

---

## Scelte aperte per questo post

**A. Coefficienti prima o tabella prima.** Ora il post dà i due odds ratio e poi la tabella
a nove caselle. Si può invertire: partire dalla tabella, che è comprensibile a chiunque, e
usare i coefficienti solo come conferma nel riquadro finale. **Consiglio l'inversione**: la
tabella è la cosa migliore che questo post ha, e ora arriva seconda.

**B. Il caso «livello medio, forte crescita».** Il 5,9% è il dato più utile per chi allena —
è l'unica casella che autorizza a scommettere su un ragazzo non ancora forte — ma poggia su
187 atleti e 11 professionisti. Si può: (a) tenerlo con l'enfasi attuale; (b) tenerlo
citando la numerosità nel corpo, non solo nel riquadro; (c) ridimensionarlo a osservazione
di passaggio. **Consiglio (b)**: la frase è troppo utile per toglierla e troppo sottile per
darla senza il suo denominatore.

**C. Quanto spazio dare allo shrinkage.** È il concetto tecnicamente più ostico della serie
e occupa due paragrafi. Alternative: spiegarlo come ora; ridurlo a una riga rimandando al
riquadro; oppure toglierlo del tutto dal corpo — con il rischio che il controllo sulla
durata della carriera, subito dopo, diventi incomprensibile.

**D. La coppia di ragazzi dell'apertura.** Sono inventati, ed è una scelta: nessun dato
personale di minori entra in questa serie. Si può dirlo esplicitamente («i due ragazzi non
esistono, i numeri sì») oppure lasciarlo implicito. Dirlo costa una riga e previene la
domanda.

**E. Il numero chiave.** Il piano indica 20,7%. Funziona, ma da solo non dice niente: va
sempre accoppiato al 2,1%. La coppia **«20,7% contro 2,1%»** è più forte del singolo numero
e andrebbe usata come formula ricorrente nel titolo e nella chiusura.
