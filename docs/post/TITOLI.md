# Titoli della serie, e come si categorizza sul sito

> Questo file non si rigenera. Serve a tenere in un posto solo i titoli pubblici, che sono
> diversi dai titoli di lavoro usati nei file delle bozze, e la scelta della categoria sul
> sito. Se cambia un titolo, cambia qui.

## Il titolo comune

**Ciclismo giovanile e professionismo**

È il nome della serie, e apre ogni titolo seguito dai due punti. La ripetizione è
voluta: in una lista di post è il segnale che dice «questi nove vanno letti insieme».

Il prezzo è che trentotto caratteri identici precedono la parte distintiva di ogni titolo,
e in un elenco l'occhio deve saltarli nove volte. La contromisura non è accorciare il
prefisso, che perderebbe la metà del suo significato, ma **caricare l'informazione
all'inizio della seconda metà**: ogni titolo deve reggere anche letto da solo, troncato
dopo poche parole, come succede nei risultati di ricerca e nelle condivisioni.

## I nove titoli

| # | titolo pubblico | file |
|---|---|---|
| 1 | Ciclismo giovanile e professionismo: cosa sappiamo già, e cosa no | `01_cosa_sappiamo.md` |
| 2 | Ciclismo giovanile e professionismo: di chi stiamo parlando | `02_di_chi_parliamo.md` |
| 3 | Ciclismo giovanile e professionismo: sparire dalla classifica non è smettere | `03_sparire_non_e_smettere.md` |
| 4 | Ciclismo giovanile e professionismo: a tredici anni si vede già qualcosa | `04_a_tredici_anni.md` |
| 5 | Ciclismo giovanile e professionismo: il livello o la curva? | `05_livello_o_curva.md` |
| 6 | Ciclismo giovanile e professionismo: predire non è selezionare | `06_predire_non_e_selezionare.md` |
| 7 | Ciclismo giovanile e professionismo: i falsi indizi | `07_falsi_indizi.md` |
| 8 | Ciclismo giovanile e professionismo: e le ragazze? | `08_le_ragazze.md` |
| 9 | Ciclismo giovanile e professionismo: cosa faremmo con questi numeri | `09_cosa_faremmo.md` |

**Due titoli sono più deboli degli altri e vale la pena deciderli a parte.**

Il secondo, «di chi stiamo parlando», non dice nulla a chi lo incontra fuori dalla serie.
Alternative che portano il numero chiave nel titolo: «in classifica ci finisce un tesserato
su sette»; «chi c'è dentro la classifica».

Il settimo, «i falsi indizi», è evocativo ma vago. Alternative: «il mese di nascita, la
squadra, la regione»; «tre indizi che non lo sono».

## Il tag sul sito

**`ciclismo-giovanile`**

Segue la convenzione già in uso su [lucabontempi.com](https://lucabontempi.com/tags/), dove
i tag sono minuscoli, in inglese o in italiano secondo il contenuto, e uniti dal trattino:
`app-store`, `mobile-app`, `photography`, `thesis`.

Accanto va **`ita`**, il tag di lingua che il sito usa già per i contenuti in italiano, dato
che i post di questa serie sono gli unici insieme alla tesi triennale a non essere in
inglese.

Un terzo tag ha senso solo se serve a collegare questi post ad altri che verranno: `dati`
oppure `analisi` raccoglierebbero la serie insieme a lavori futuri di tipo simile, mentre
`ciclismo-giovanile` resta specifico dell'argomento.

**Se il tema lo permette**, la strada migliore resta una tassonomia `series` di Hugo
separata dai tag: il nome della serie comparirebbe sopra il titolo e la navigazione fra le
puntate verrebbe da sola, permettendo di accorciare i titoli. PaperMod non la offre
predefinita ma Hugo la supporta con poche righe in `hugo.toml`. È l'unica soluzione che
elimina la ripetizione senza perdere il segnale della serie.
