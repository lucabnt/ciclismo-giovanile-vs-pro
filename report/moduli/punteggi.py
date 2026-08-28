"""
I punteggi giovanili di chi e' arrivato e di chi no.

LA DOMANDA
    Prima di qualunque modello: chi e' diventato professionista andava gia' meglio degli
    altri a tredici anni? E di quanto? E' la forma descrittiva della Domanda C, e
    conviene guardarla prima, perche' fissa l'ordine di grandezza di cio' che i modelli
    potranno trovare.

L'EFFECT SIZE, NON IL p
    Con 1.600 non professionisti contro 60 professionisti qualunque differenza risulta
    significativa: il p-value dice solo che il campione e' grande. Il numero che conta e'
    il **delta di Cliff**, che misura quanto le due distribuzioni si separano:

        delta = P(pro > non pro) - P(pro < non pro)

    Va da -1 a +1. Soglie convenzionali: sotto 0,15 trascurabile, 0,33 piccolo,
    0,47 medio, sopra 0,47 grande.

    E si traduce direttamente in AUC: **AUC = (delta + 1) / 2**. Un delta di 0,60
    corrisponde a un'area sotto la curva di 0,80, che e' esattamente cio' che i modelli
    univariati riporteranno. La descrittiva anticipa quindi il risultato modellistico,
    e se i due non tornano c'e' un errore da qualche parte.

LA TRAPPOLA DA NON PRENDERE
    I delta di celle diverse NON sono confrontabili come se fossero la stessa misura su
    popolazioni diverse. Chi e' presente in Under 23 e' gia' un sopravvissuto: in quella
    cella i professionisti sono piu' di un terzo, contro il 3,5% in Under 15. Un delta
    piu' basso in Under 23 non significa che il rendimento conti meno — significa che li'
    si stanno confrontando fra loro atleti gia' selezionati.

    Per questo la tabella riporta sempre il tasso di professionisti della cella accanto
    al delta: senza, il confronto fra righe induce in errore.

NIENTE DIPENDENZE
    Mediana, quartili, delta di Cliff e l'approssimazione normale di Mann-Whitney con
    correzione per i pari merito stanno tutte nella libreria standard.
"""
import math
import os
import sqlite3
import sys
from bisect import bisect_left, bisect_right

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, cfg          # noqa: E402
from lib_risultati import Archivio                 # noqa: E402
import lib_markdown as md                          # noqa: E402
import lib_grafici as gr                           # noqa: E402

# Radice dei rimandi enciclopedici usati nei riquadri metodologici.
W = "https://en.wikipedia.org/wiki/"

SOGLIE_DELTA = ((0.15, "trascurabile"), (0.33, "piccolo"), (0.47, "medio"))
MIN_GRUPPO = cfg("etica", "min_cella_pubblicabile")   # stessa soglia delle tabelle


def quantile(v, p):
    v = sorted(v)
    if not v:
        return None
    k = (len(v) - 1) * p
    f = int(k)
    return v[f] if f + 1 >= len(v) else v[f] + (k - f) * (v[f + 1] - v[f])


def cliff(a, b):
    """delta = P(a > b) - P(a < b). I pari merito contano zero, come da definizione."""
    if not a or not b:
        return None
    b = sorted(b)
    s = sum(bisect_left(b, x) - (len(b) - bisect_right(b, x)) for x in a)
    return s / (len(a) * len(b))


def mann_whitney(a, b):
    """p a due code, approssimazione normale con correzione per i pari merito.

    L'approssimazione e' adeguata: i gruppi qui sono sempre sopra la decina, e il p
    e' comunque la parte meno interessante del confronto.
    """
    n1, n2 = len(a), len(b)
    if n1 < 3 or n2 < 3:
        return None
    tutti = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranghi, i, pareggi = [0.0] * len(tutti), 0, []
    while i < len(tutti):
        j = i
        while j + 1 < len(tutti) and tutti[j + 1][0] == tutti[i][0]:
            j += 1
        medio = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranghi[k] = medio
        if j > i:
            pareggi.append(j - i + 1)
        i = j + 1
    r1 = sum(r for r, (_, g) in zip(ranghi, tutti) if g == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    n = n1 + n2
    corr = sum(t ** 3 - t for t in pareggi)
    var = n1 * n2 / 12 * ((n + 1) - corr / (n * (n - 1))) if n > 1 else 0
    if var <= 0:
        return None
    z = (u1 - mu) / math.sqrt(var)
    return math.erfc(abs(z) / math.sqrt(2))


def etichetta_delta(d):
    a = abs(d)
    for soglia, nome in SOGLIE_DELTA:
        if a < soglia:
            return nome
    return "grande"


def calcola():
    db = sqlite3.connect(DB_ANALISI)
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    celle = cfg("modelli", "celle_correlazione")

    with Archivio("punteggi") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))

        righe, curva = [], []
        for cella in celle:
            d = db.execute("""SELECT pct_%s, PRO FROM tab_b WHERE sesso = ?
                              AND birth_year BETWEEN ? AND ? AND present_%s = 1
                              AND pct_%s IS NOT NULL""" % (cella, cella, cella),
                           (sesso, lo, hi)).fetchall()
            no = [r[0] for r in d if not r[1]]
            si = [r[0] for r in d if r[1]]
            if len(si) < MIN_GRUPPO or len(no) < MIN_GRUPPO:
                continue
            dl = cliff(si, no)
            righe.append([
                cella, len(d), round(100 * len(si) / len(d), 1),
                "%.0f [%.0f-%.0f]" % (quantile(no, .5), quantile(no, .25), quantile(no, .75)),
                "%.0f [%.0f-%.0f]" % (quantile(si, .5), quantile(si, .25), quantile(si, .75)),
                round(dl, 2), etichetta_delta(dl), round((dl + 1) / 2, 2)])
            curva.append((cella, dl, len(si), len(d)))
            ar.valore("delta_%s" % cella,
                      {"delta": round(dl, 3), "auc": round((dl + 1) / 2, 3),
                       "n_pro": len(si), "n_totale": len(d),
                       "p_mann_whitney": mann_whitney(si, no)})

        ar.tabella("per_cella", righe,
                   colonne=["cella", "atleti", "% pro", "non pro: mediana [IQR]",
                            "pro: mediana [IQR]", "delta di Cliff", "entita'", "AUC"],
                   titolo="Il percentile di chi e' arrivato e di chi no",
                   nota="il percentile va da 0 a 100; la colonna «% pro» e' il tasso di "
                        "professionisti della cella, e serve a non confrontare fra loro "
                        "delta calcolati su popolazioni diverse")
        if curva:
            giovanili = [c for c in curva if not c[0].startswith("U23")]
            ar.valore("delta_primo", [giovanili[0][0], round(giovanili[0][1], 2)])
            mx = max(giovanili, key=lambda c: c[1])
            ar.valore("delta_massimo", [mx[0], round(mx[1], 2), round((mx[1] + 1) / 2, 2)])
            u23 = [c for c in curva if c[0].startswith("U23")]
            if u23:
                ar.valore("delta_u23", [u23[0][0], round(u23[0][1], 2),
                                        round(100 * u23[0][2] / u23[0][3], 1)])

        # --- il gradiente per livello dell'esito ---------------------------
        righe_t = []
        for cella in celle:
            riga = [cella]
            for t in range(4):
                v = [r[0] for r in db.execute(
                    """SELECT pct_%s FROM tab_b WHERE sesso = ? AND
                       birth_year BETWEEN ? AND ? AND present_%s = 1 AND tier = ?
                       AND pct_%s IS NOT NULL""" % (cella, cella, cella),
                    (sesso, lo, hi, t))]
                riga.append("%.0f (n=%d)" % (quantile(v, .5), len(v)) if len(v) >= MIN_GRUPPO
                            else ("n=%d" % len(v) if v else "—"))
            righe_t.append(riga)
        ar.tabella("per_tier", righe_t,
                   colonne=["cella", "non pro", "pro senza top 500", "top 500", "top 100"],
                   titolo="Percentile mediano per livello raggiunto",
                   nota="fra parentesi la numerosita'; dove e' sotto la soglia si riporta "
                        "solo quella, non la mediana")

        if not os.environ.get("SENZA_FIGURE"):
            try:
                disegna(curva, ar, lo, hi)
            except SystemExit as e:
                print("   figura saltata: %s" % e)

    print("Modulo 'punteggi' eseguito.")
    for c, dl, npro, ntot in curva:
        print("   %-7s delta %.2f  (AUC %.2f)  %d pro su %d" % (c, dl, (dl + 1) / 2, npro, ntot))


def disegna(curva, ar, lo, hi):
    with gr.figura("Quanto il percentile separa chi arrivera' da chi no") as (fig, ax):
        x = list(range(len(curva)))
        y = [c[1] for c in curva]
        colori = [gr.COLORI[1] if c[0].startswith("U23") else gr.COLORI[0] for c in curva]
        ax.bar(x, y, color=colori, zorder=3)
        for soglia, nome in SOGLIE_DELTA:
            gr.linea_riferimento(ax, soglia, nome)
        gr.linea_riferimento(ax, 0.47, "grande")
        for i, (c, dl, npro, ntot) in enumerate(curva):
            ax.annotate("%.2f" % dl, (i, dl), textcoords="offset points",
                        xytext=(0, 4), ha="center", fontsize=9)
        ax.set_xticks(x)
        ax.set_xticklabels(["%s\n%.0f%% pro" % (c[0], 100 * c[2] / c[3]) for c in curva],
                           fontsize=8)
        ax.set_ylabel("delta di Cliff")
        ax.set_ylim(0, 1)
        fig.text(0.005, -0.05, "Coorti %d-%d. In rosso l'Under 23, dove il confronto avviene "
                 "fra atleti gia' selezionati e il valore non e' confrontabile con gli "
                 "altri." % (lo, hi), fontsize=8, color=gr.GRIGIO)
    ar.figura("delta", gr.salva("punteggi_delta"),
              didascalia="La separazione fra chi arrivera' e chi no e' gia' «grande» a "
                         "tredici anni, e cresce fino all'ultimo anno da Juniores.")


def rendi(lt):
    v = lt.valori("punteggi")
    per_cella = lt.tabella("punteggi", "per_cella")
    per_tier = lt.tabella("punteggi", "per_tier")

    p = [md.sezione("Chi e' arrivato andava gia' meglio?")]
    p.append(md.paragrafo(
        "Prima di qualunque modello vale la pena guardare la cosa piu' semplice: il "
        "percentile di chi e' diventato professionista, confrontato con quello di tutti "
        "gli altri, stagione per stagione.",
        "",
        "Il numero da guardare **non e' il p-value**. Con milleseicento non professionisti "
        "contro sessanta professionisti qualunque differenza risulta significativa: il p "
        "direbbe solo che il campione e' grande. Il numero che conta e' il **delta di "
        "Cliff**, che misura quanto le due distribuzioni si separano, e che si traduce "
        "direttamente in area sotto la curva: `AUC = (delta + 1) / 2`."))

    p.append(md.metodo(
        "Delta di Cliff",
        "Si prendono tutte le coppie possibili fra un professionista e un non "
        "professionista e si conta quante volte il primo ha un percentile piu' alto. "
        "Il delta e' la differenza fra la quota di coppie in cui vince il "
        "professionista e quella in cui vince l'altro: vale 1 se i professionisti "
        "stanno tutti sopra, 0 se le due distribuzioni sono sovrapposte, -1 nel caso "
        "opposto. I pari merito non contano.\n\n"
        "Non assume ne' normalita' ne' varianze uguali, e non risente dei valori "
        "estremi: guarda solo l'ordinamento. Soglie convenzionali: sotto 0,15 "
        "trascurabile, 0,33 piccolo, 0,47 medio, sopra 0,47 grande.\n\n"
        "Si converte in area sotto la curva ROC con AUC = (delta + 1) / 2, che e' il "
        "ponte fra questa descrittiva e i modelli.",
        [("Effect size", W + "Effect_size"),
         ("Curva ROC e AUC", W + "Receiver_operating_characteristic")]))

    p.append(md.metodo(
        "Mediana e scarto interquartile",
        "La mediana e' il valore che lascia meta' degli atleti sopra e meta' sotto. "
        "Fra parentesi quadre c'e' l'intervallo fra il primo e il terzo quartile, "
        "cioe' la fascia in cui sta la meta' centrale del gruppo.\n\n"
        "Si usano al posto di media e deviazione standard perche' i percentili qui non "
        "sono distribuiti simmetricamente e hanno grossi ammassi in coda: la media "
        "verrebbe tirata dai valori estremi, la mediana no.",
        [("Scarto interquartile", W + "Interquartile_range"),
         ("Percentile", W + "Percentile_rank")]))

    if per_cella:
        p.append(md.tabella(per_cella["colonne"], per_cella["righe"],
                            colonne_conteggio={1}, decimali=2, nota=per_cella["nota"]))

    dp, dm = v.get("delta_primo"), v.get("delta_massimo")
    if dp and dm:
        p.append(md.paragrafo(
            "",
            "**Gia' a tredici anni la separazione e' netta.** Il delta in %s vale "
            "**%.2f**, esattamente sul confine convenzionale fra «medio» e «grande», e "
            "sale fino a **%.2f** in %s — un'AUC di %.2f, che e' l'ordine di grandezza "
            "di cio' che un modello univariato potra' ottenere."
            % (dp[0], dp[1], dm[1], dm[0], dm[2])))

    du = v.get("delta_u23")
    if du:
        p.append(md.paragrafo(
            "",
            "**Attenzione pero' all'ultima riga.** In %s il delta scende a %.2f, e "
            "sarebbe facile leggerlo come «il rendimento da Under 23 conta meno». Non e' "
            "cosi': in quella cella i professionisti sono il **%.0f%%**, contro poche "
            "unita' percentuali nelle categorie giovanili. Chi arriva li' e' gia' un "
            "sopravvissuto, e il confronto avviene fra atleti gia' selezionati. "
            "I delta di righe diverse **non sono confrontabili** fra loro, ed e' il "
            "motivo per cui la tabella riporta il tasso di professionisti accanto a "
            "ciascuno." % (du[0], du[1], du[2])))

    f = lt.figura("punteggi", "delta")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.metodo(
        "Perche' il p-value non compare in tabella",
        "Il test di Mann-Whitney e' calcolato e conservato nell'archivio dei risultati, "
        "ma non e' riportato qui. Con gruppi cosi' sbilanciati — millesettecento contro "
        "sessanta — il p diventa minuscolo per differenze di qualunque entita', e "
        "risponde alla domanda sbagliata: dice se la differenza esiste, non quanto e' "
        "grande. In tutte le celle risulta comunque sotto un millesimo.",
        [("Test di Mann-Whitney", W + "Mann%E2%80%93Whitney_U_test")]))

    p.append(md.sezione("Il gradiente per livello raggiunto", 3))
    if per_tier:
        p.append(md.tabella(per_tier["colonne"], per_tier["righe"], nota=per_tier["nota"]))
    p.append(md.paragrafo(
        "",
        "La mediana cresce monotonicamente con il livello raggiunto, in tutte le celle: "
        "non c'e' una soglia oltre la quale il percentile smette di dire qualcosa. "
        "Le colonne di destra sono pero' sottili — otto atleti in tutto arrivano in "
        "top 100 — e vanno lette come indicazione, non come stima."))
    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
