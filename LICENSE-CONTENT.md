# Licenza dei contenuti — CC BY 4.0

> Questo file riguarda **i testi, le tabelle e le figure**. Il codice sta sotto una licenza
> diversa e più permissiva: [`LICENSE`](LICENSE), MIT.
>
> Se vuoi solo sapere cosa puoi fare: **puoi riusare tutto, anche commercialmente, anche
> modificandolo, purché tu dica da dove viene.** Il resto di questo file spiega i confini,
> che in un progetto costruito su dati di terzi non sono ovvi.

---

## Cosa copre questa licenza

I contenuti di questo repository — la prosa, le tabelle, le figure, l'analisi — sono di
**lucabnt**, che ne è autore e titolare dei diritti, e sono distribuiti sotto **Creative
Commons Attribuzione 4.0 Internazionale (CC BY 4.0)**.

- Sintesi leggibile: <https://creativecommons.org/licenses/by/4.0/deed.it>
- Testo legale completo: <https://creativecommons.org/licenses/by/4.0/legalcode.it>

Il testo legale a quell'indirizzo è parte integrante di questa licenza: qui non è ricopiato
per non rischiare di alterarlo trascrivendolo.

| percorso | cosa contiene |
|---|---|
| `docs/` | rassegna della letteratura, definizioni, checklist TRIPOD, verifiche della sorgente |
| `output/analisi.md` | il documento generato dall'analisi |
| `output/figure/` | tutte le figure, ciascuna con la data di generazione scritta dentro l'immagine |
| `README.md`, `guida_metodologica_v5.md` | descrizione del progetto e impianto metodologico |
| `riferimenti/*.csv` | la **trascrizione** dei dati pubblici FCI, comprese le intestazioni di provenienza |

Vale anche per **la prosa che il codice produce**. I moduli in `report/` sono codice e
stanno sotto MIT, ma le frasi che contengono — quelle che finiscono dentro `analisi.md` —
sono contenuti e stanno qui. Il confine è fra *ciò che fa qualcosa* e *ciò che dice
qualcosa*, non fra un'estensione di file e un'altra.

## Cosa NON copre, ed è la parte importante

**I dati di partenza non sono nostri e non possiamo concederli.**

Appartengono ai siti di riferimento da cui vengono, e nel repository non sono inclusi. Le
classifiche giovanili vengono da ciclismo.info, gli esiti di carriera da
ProCyclingStats, le nascite attese da Eurostat, i tesserati dalla Federazione Ciclistica
Italiana. Su ciascuna fonte valgono le condizioni della fonte, e nell'Unione Europea una
banca dati può essere protetta dal **diritto sui generis del costitutore** anche quando i
singoli fatti che contiene non sono proteggibili. Che un numero sia vero non lo rende
libero.

In pratica:

- **questo repository non distribuisce i dati di partenza.** `data/` è escluso da git per
  intero, e la ragione principale è un'altra — riguarda minorenni, vedi sotto — ma
  l'effetto sulla licenza è che qui non c'è nessuna banca dati da riusare;
- `riferimenti/*.csv` contiene **totali nazionali già pubblicati** dalla federazione. La
  nostra trascrizione, con la sua struttura e le sue note di provenienza, sta sotto CC BY;
  i numeri in sé sono fatti pubblici e nessuno può appropriarsene, noi compresi. Se li
  usi, cita la FCI come fonte e non noi;
- i **risultati aggregati** — percentuali, coefficienti, tabelle dell'analisi — sono
  elaborazione nostra e stanno sotto CC BY.

**Le opere altrui restano altrui.** La rassegna della letteratura descrive ventidue studi
pubblicati: le sintesi sono nostre e sono coperte da questa licenza, ma gli articoli
originali no. Citazioni e DOI sono nella rassegna proprio perché chi vuole risalga alla
fonte invece che alla nostra parafrasi.

## Dati personali

Lo studio riguarda **atleti minorenni** e nel repository non entra nulla che permetta di
risalire a una persona: gli identificativi sono cifrati con un segreto tenuto fuori dal
codice e nessuna tabella pubblicata contiene celle con meno di cinque atleti.

Questa non è una condizione della licenza, è un vincolo che viene prima della licenza. Se
riusi questi contenuti, **il divieto di re-identificare gli atleti resta**: nessuna licenza
può autorizzare quello che la normativa sulla protezione dei dati vieta, e CC BY non è
un'eccezione.

## Come attribuire

CC BY chiede di indicare l'autore, la fonte e la licenza, e di segnalare se hai fatto
modifiche. Una riga basta.

**Se citi o ripubblichi un testo così com'è:**

> Fonte: *Ranking giovanili italiani e transizione al professionismo*, lucabnt —
> https://github.com/lucabnt/ciclismo-giovanile-vs-pro — CC BY 4.0

**Se lo modifichi, tagli o rielabori**, aggiungi che l'hai fatto:

> Adattato da *Ranking giovanili italiani e transizione al professionismo*, lucabnt —
> https://github.com/lucabnt/ciclismo-giovanile-vs-pro — CC BY 4.0. Testo modificato.

**Se riusi una figura**, la stessa riga nella didascalia.

Due cortesie che la licenza non impone e che chiediamo lo stesso:

- **cita anche l'anno dei dati.** I numeri di questo studio riguardano le annate 1996-2000
  su classifiche 2007-2025. Un aggiornamento futuro darà numeri diversi, e una citazione
  senza data invecchia male;
- **non attribuire a noi conclusioni che non abbiamo tratto.** È lo scopo per cui ogni
  affermazione del documento generato dichiara il numero su cui si regge.

## Sul codice

Il codice — `scripts/`, `R/`, i moduli in `report/`, `config.toml`, `.githooks/` — sta
sotto **licenza MIT** ([`LICENSE`](LICENSE)), che è più permissiva: chiede solo di
conservare la nota di copyright, che porta lo stesso nome: lucabnt. La scelta è
deliberata. Il valore di questo progetto non sta nel codice, sta in come sono state prese le decisioni; il codice si riusi liberamente,
e se qualcuno rifà lo stesso lavoro su un'altra federazione, tanto meglio.

## Se questa licenza non ti basta

Chi vuole usare questi contenuti in un modo che CC BY non copre — o non vuole attribuire —
può scrivere: il repository non è il solo canale possibile e un accordo diverso si può
sempre fare.

---

## In English

The **content** of this repository — prose, tables, figures, the generated analysis — is
licensed under [Creative Commons Attribution 4.0 International (CC BY
4.0)](https://creativecommons.org/licenses/by/4.0/). You may reuse, adapt and redistribute
it, including commercially, provided you credit the source and indicate changes.

The **code** is under the MIT licence, see [`LICENSE`](LICENSE). Code and content are by
lucabnt, who holds the copyright.

The **underlying data is not included and is not ours to license**: it belongs to the source
sites. Youth rankings come from ciclismo.info,
career outcomes from ProCyclingStats, expected births from Eurostat, licence-holder counts
from the Italian Cycling Federation. Their terms apply, and in the EU a database may carry
a sui generis right of its own. This repository does not redistribute any of it.

The study concerns **underage athletes**. Nothing identifying is published here, and no
licence grants permission to re-identify anyone.
