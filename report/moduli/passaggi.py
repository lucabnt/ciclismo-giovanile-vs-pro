"""
Il passaggio di categoria e' davvero una rottura?

DA DOVE NASCE LA DOMANDA
    La sezione sull'attrito mostra che le uscite dalla classifica si concentrano
    nell'ultimo anno di ogni categoria. La lettura naturale e' che il passaggio di fascia
    sia un trauma: cambiano distanze, avversari, squadra, e chi non regge esce.

    E' una lettura plausibile, ed e' proprio per questo che va messa alla prova invece
    che assunta. Qui si confrontano due tipi di passaggio di stagione che distano un anno
    l'uno come l'altro: quelli **dentro** una categoria (dal primo al secondo anno) e
    quelli **fra** categorie. Se il cambio di fascia fosse una rottura, i secondi
    dovrebbero comportarsi peggio dei primi.

DUE COSE DIVERSE CHE VENGONO CONFUSE
    «Rottura» puo' voler dire due cose, e i dati le distinguono.

    Che **spariscano piu' persone**: si misura con la quota di chi e' ancora in classifica
    l'anno dopo.

    Che **si rimescoli l'ordine** fra chi resta: si misura con la correlazione fra i
    percentili delle due stagioni. Un rimescolamento vorrebbe dire che il risultato di
    una stagione dice poco su quello successiva.

    Le due cose hanno implicazioni opposte per una societa': la prima e' un problema di
    ritenzione, la seconda di valutazione.

LA TRAPPOLA DA DISINNESCARE
    Le classifiche non hanno tutte la stessa lunghezza, e le annate non ci compaiono in
    parti uguali. Salendo di categoria un atleta si ritrova in una lista condivisa con
    ragazzi piu' grandi, e al primo anno vince una minoranza dei piazzamenti a punti:
    poco piu' di un quarto in Allievi. La sua annata risulta quindi molto meno numerosa
    di quella sopra, e questo basta a produrre da solo un crollo apparente delle presenze
    al cambio di fascia, senza che sia successo nulla alle persone.

    La sezione «Quanti posti ci sono, e chi se li prende» misura il fenomeno e ne
    identifica la causa, che non e' la scarsita' dei posti ma la concorrenza fra annate.

    Il rimedio, qui, e' guardare anche **da dove viene la lista di arrivo**: quanta parte
    e' composta da chi c'era gia'. Quella quota non dipende da quanti siano i posti ne'
    da chi li vinca.
"""
import os
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, cfg          # noqa: E402
from lib_risultati import Archivio                 # noqa: E402
import lib_markdown as md                          # noqa: E402
import lib_grafici as gr                           # noqa: E402
from correlazioni import spearman                  # noqa: E402

W = "https://en.wikipedia.org/wiki/"

MIN_COPPIA = 30          # sotto questa numerosita' una correlazione non si riporta


def mediana(v):
    v = sorted(v)
    n = len(v)
    if not n:
        return None
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def calcola():
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    celle = cfg("modelli", "celle_correlazione")
    db = sqlite3.connect(DB_ANALISI)

    def presenti(cella):
        return db.execute(
            """SELECT COUNT(*) FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ?
               AND present_%s = 1""" % cella, (sesso, lo, hi)).fetchone()[0]

    def coppia(a, b):
        return db.execute(
            """SELECT pct_%s, pct_%s FROM tab_b WHERE sesso = ? AND
               birth_year BETWEEN ? AND ? AND present_%s = 1 AND present_%s = 1
               AND pct_%s IS NOT NULL AND pct_%s IS NOT NULL"""
            % (a, b, a, b, a, b), (sesso, lo, hi)).fetchall()

    with Archivio("passaggi") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))
        righe, dentro, fra = [], [], []
        for i in range(len(celle) - 1):
            a, b = celle[i], celle[i + 1]
            stessa = a.split("y")[0] == b.split("y")[0]
            na, nb = presenti(a), presenti(b)
            dati = coppia(a, b)
            n = len(dati)
            if not na or not nb or n < MIN_COPPIA:
                continue
            rho = spearman([d[0] for d in dati], [d[1] for d in dati])
            spostamento = mediana([abs(d[1] - d[0]) for d in dati])
            voce = {"da": a, "a": b, "stessa": stessa, "na": na, "nb": nb, "n": n,
                    "resta": 100 * n / na, "quota": 100 * n / nb,
                    "rho": rho, "spostamento": spostamento}
            righe.append(voce)
            (dentro if stessa else fra).append(voce)

        ar.tabella(
            "passaggi",
            [["%s → %s" % (r["da"], r["a"]),
              "dentro la categoria" if r["stessa"] else "cambio di categoria",
              r["na"], r["nb"], round(r["resta"], 1), round(r["quota"], 1),
              round(r["rho"], 3), round(r["spostamento"], 1)] for r in righe],
            colonne=["passaggio", "tipo", "in classifica prima", "in classifica dopo",
                     "% che resta", "% della lista di arrivo che c'era gia'",
                     "correlazione fra i due percentili",
                     "spostamento mediano (punti)"],
            titolo="Passaggi di stagione, dentro e fra le categorie",
            nota="tutti i passaggi distano una stagione: la sola differenza e' se "
                 "comportino o no un cambio di fascia")

        def media(gruppo, chiave):
            return round(sum(g[chiave] for g in gruppo) / len(gruppo), 1 if chiave !=
                         "rho" else 3) if gruppo else None

        for nome, gruppo in (("dentro", dentro), ("fra", fra)):
            ar.valore("resta_" + nome, media(gruppo, "resta"))
            ar.valore("quota_" + nome, media(gruppo, "quota"))
            ar.valore("rho_" + nome, media(gruppo, "rho"))
            ar.valore("spostamento_" + nome, media(gruppo, "spostamento"))

        if not os.environ.get("SENZA_FIGURE"):
            disegna(righe, ar)
    db.close()
    print("   passaggi: resta il %s%% dentro la categoria, il %s%% al cambio di fascia"
          % (media(dentro, "resta"), media(fra, "resta")))


def disegna(righe, ar):
    gr.stile()
    etichette = ["%s→%s" % (r["da"], r["a"]) for r in righe]
    x = list(range(len(righe)))
    resta = [r["resta"] for r in righe]
    quota = [r["quota"] for r in righe]
    colori = [gr.COLORI[1] if not r["stessa"] else gr.COLORI[0] for r in righe]
    larghezza = 0.38
    with gr.figura("Chi resta, e chi compone la lista di arrivo") as (fig, ax):
        ax.bar([i - larghezza / 2 for i in x], resta, larghezza, color=colori,
               label="resta in classifica l'anno dopo")
        ax.bar([i + larghezza / 2 for i in x], quota, larghezza, color=colori,
               alpha=0.45, label="quota della lista di arrivo che c'era gia'")
        ax.set_xticks(x)
        ax.set_xticklabels(etichette, fontsize=8)
        ax.set_ylabel("percentuale")
        ax.set_ylim(0, 100)
        ax.legend(loc="lower left", fontsize=8)
        ax.grid(axis="x", visible=False)
        ax.annotate("in rosso i cambi di categoria", xy=(0.99, 0.97),
                    xycoords="axes fraction", ha="right", va="top", fontsize=8,
                    color=gr.GRIGIO)
    ar.figura("passaggi", gr.salva("passaggi_ritenzione"),
              didascalia="Le due misure vanno in direzioni opposte proprio dove ci si "
                         "aspetterebbe la rottura: al cambio di categoria resta meno "
                         "gente, ma la lista di arrivo e' fatta quasi solo di loro.")


def rendi(lt):
    v = lt.valori("passaggi")
    t = lt.tabella("passaggi", "passaggi")

    p = [md.sezione("Il passaggio di categoria e' una rottura?")]

    if not t:
        p.append(md.paragrafo("*Sezione non disponibile: i risultati non sono stati "
                              "calcolati.*"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "Le uscite dalla classifica si concentrano nell'ultimo anno di ogni categoria, e "
        "la lettura naturale e' che il cambio di fascia sia un trauma: distanze nuove, "
        "avversari piu' grandi, squadra diversa. E' plausibile, ed e' proprio per questo "
        "che conviene metterla alla prova invece di darla per buona."))

    p.append(md.metodo(
        "Come si mette alla prova l'idea di rottura",
        "Si confrontano passaggi di stagione che distano tutti un anno, divisi in due "
        "tipi: quelli **dentro** una categoria, dal primo al secondo anno, e quelli "
        "**fra** categorie. La distanza temporale e' la stessa, cambia solo se ci sia o "
        "no un cambio di fascia.\n\n"
        "«Rottura» puo' voler dire due cose diverse, con implicazioni opposte. Che "
        "**spariscano piu' persone** — un problema di ritenzione. O che **si rimescoli "
        "l'ordine** fra chi resta — un problema di valutazione, perche' vorrebbe dire "
        "che il risultato di una stagione dice poco su quella successiva. Le due si "
        "misurano separatamente.\n\n"
        "C'e' una trappola da disinnescare: al primo anno di una categoria gli atleti "
        "sono molto meno numerosi che al secondo, perche' corrono nella stessa lista dei "
        "piu' grandi e vincono una minoranza dei piazzamenti a punti. Se un'annata occupa "
        "un quarto dei posti invece della meta', gran parte delle persone esce dalla "
        "classifica anche senza che sia successo nulla. Per questo si guarda anche **da "
        "dove viene la lista di arrivo**: quanta parte e' composta da chi c'era gia'. "
        "Quella quota non dipende da quanti siano i posti ne' da chi li vinca.",
        [("Correlazione di Spearman", W + "Spearman%27s_rank_correlation_coefficient")]))

    righe = [r[:6] + [md.num(r[6], 3), md.num(r[7], 1)] for r in t["righe"]]
    p.append(md.tabella(t["colonne"], righe, nota=t["nota"],
                        colonne_conteggio=(2, 3), decimali=1))

    rd, rf = v.get("resta_dentro"), v.get("resta_fra")
    qd, qf = v.get("quota_dentro"), v.get("quota_fra")
    if rd and rf:
        p.append(md.paragrafo(
            "",
            md.afferma(
                rf < rd,
                "al cambio di categoria resta in classifica una quota molto minore che "
                "dentro la categoria",
                "**Il crollo c'e', ed e' grande.** Dentro una categoria resta in "
                "classifica il %s%% degli atleti; al cambio di fascia il %s%%. Presa "
                "cosi', la lettura del trauma sembra confermata."
                % (md.num(rd, 1), md.num(rf, 1)))))

    if qd and qf:
        p.append(md.paragrafo(
            "",
            md.afferma(
                qf > qd,
                "la lista di arrivo di un cambio di categoria e' composta in quota "
                "maggiore da chi c'era gia', rispetto a un passaggio interno",
                "**Ma la colonna successiva dice il contrario, e con la stessa forza.** "
                "La lista che si trova dopo un cambio di categoria e' composta per il "
                "%s%% da persone che c'erano gia'; dopo un passaggio interno, solo per "
                "il %s%%. Al cambio di fascia non entra quasi nessuno di nuovo."
                % (md.num(qf, 1), md.num(qd, 1))),
            "",
            "I due numeri sembrano contraddirsi e non si contraddicono: al cambio di "
            "categoria **l'annata che arriva occupa molti meno posti**. Passa da essere "
            "la piu' anziana della propria lista a essere la piu' giovane, contro ragazzi "
            "con un anno di sviluppo in piu', e nelle stesse gare vince molto meno. Resta "
            "quindi meno gente, ma i posti che restano se li tengono quasi tutti quelli "
            "che c'erano. Il ricambio vero, l'ingresso di facce nuove, avviene **dentro** "
            "la categoria, dove l'annata cresce di peso.",
            "",
            "Quello che sembrava un trauma del passaggio di fascia e' in buona parte "
            "**una conseguenza di come sono fatte le classifiche**: dagli Allievi in su "
            "la lista e' una sola e le annate convivono, quindi al primo anno si compare "
            "poco per definizione. Chi esce al cambio di fascia in molti casi non ha "
            "smesso e non e' peggiorato: ha smesso di battere ragazzi piu' grandi."))

    rhod, rhof = v.get("rho_dentro"), v.get("rho_fra")
    if rhod and rhof:
        p.append(md.paragrafo(
            "",
            "Resta la seconda domanda: fra chi il posto ce l'ha, l'ordine si rimescola? "
            "Un po' di piu', ma poco. La correlazione fra i percentili di due stagioni "
            "consecutive e' %s dentro la categoria e %s al cambio di fascia. La "
            "differenza esiste e va nella direzione attesa, ma e' modesta: **il cambio "
            "di categoria toglie persone dalla classifica molto piu' di quanto "
            "rimescoli quelle che restano**."
            % (md.num(rhod, 3), md.num(rhof, 3))))

    sd, sf = v.get("spostamento_dentro"), v.get("spostamento_fra")
    if sd and sf:
        p.append(md.paragrafo(
            "",
            "Lo stesso in una forma piu' concreta: chi resta in classifica si sposta di "
            "%s punti di percentile in mediana dentro la categoria, e di %s al cambio di "
            "fascia. Su una scala da 0 a 100, e con il proprio piazzamento che dipende "
            "anche da quante gare si sono corse, sono spostamenti dello stesso ordine."
            % (md.num(sd, 1), md.num(sf, 1))))

    f = lt.figura("passaggi", "passaggi")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.paragrafo(
        "",
        "> **Cosa se ne ricava, per chi allena.** L'idea che al cambio di categoria si "
        "perdano i ragazzi perche' il salto e' troppo duro non trova conferma in questi "
        "dati — o meglio, non nella forma in cui la si racconta di solito. Chi era in "
        "classifica ci resta, se un posto c'e'. Quello che cambia bruscamente e' quanto "
        "e' larga la porta. Un ragazzo che sparisce dalla classifica al primo anno di "
        "una categoria nuova sta molto probabilmente ancora correndo, contro avversari "
        "di un anno piu' grandi, in una lista che ha meta' dei posti di prima."))

    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
