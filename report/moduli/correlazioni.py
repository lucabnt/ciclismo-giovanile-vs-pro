"""
Quanto si somigliano i percentili di categorie diverse, e cosa comporta per i modelli.

LA DOMANDA OPERATIVA
    Se il rendimento a tredici anni e quello a diciassette sono molto correlati, un
    modello che li usa entrambi non riesce a separarne i contributi: i coefficienti
    diventano instabili e cambiano segno al minimo cambio di campione. E' la
    multicollinearita', e il modo standard di misurarla e' il VIF.

    La regola pratica: VIF sopra 5 su piu' variabili rende **obbligatoria** la
    regressione penalizzata invece di quella ordinaria. Questa sezione decide quindi
    quale strada prendere nella parte modellistica, e va letta prima di stimare.

DUE COSE CHE NON VANNO CONFUSE
    La matrice di correlazione e' calcolata **a coppie**, usando per ogni coppia tutti
    gli atleti presenti in entrambe le celle. E' la lettura descrittiva.

    Il VIF invece richiede un unico campione con tutte le variabili osservate, e li' il
    campione crolla: su tutte e dieci le celle restano poche decine di atleti. Il
    sottoinsieme su cui si calcola sta in config.toml ed e' dichiarato accanto al
    risultato, perche' un VIF senza il proprio n non significa niente.

PERCHE' SPEARMAN E NON PEARSON
    I percentili sono distribuzioni con ammassi (molti atleti a pari merito in coda), e
    la relazione fra categorie non ha ragione di essere lineare. Spearman misura la
    concordanza dell'ordinamento, che e' cio' che interessa qui.

NIENTE DIPENDENZE
    Correlazione di rango e inversione di matrice sono aritmetica elementare e stanno
    qui in cinquanta righe. Sono verificabili a mano, a differenza dei modelli, che
    stanno in R e usano pacchetti maturi.
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

# Radice dei rimandi enciclopedici usati nei riquadri metodologici.
W = "https://en.wikipedia.org/wiki/"

SOGLIA_VIF = 5.0


def ranghi(v):
    """Ranghi medi, cosi' i pari merito non spostano la correlazione."""
    ordine = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(ordine):
        j = i
        while j + 1 < len(ordine) and v[ordine[j + 1]] == v[ordine[i]]:
            j += 1
        medio = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[ordine[k]] = medio
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5 if sxx > 0 and syy > 0 else None


def spearman(x, y):
    return pearson(ranghi(x), ranghi(y))


def inverti(m):
    """Gauss-Jordan con pivot parziale. Restituisce None se la matrice e' singolare."""
    k = len(m)
    a = [list(r) + [1.0 if i == j else 0.0 for j in range(k)] for i, r in enumerate(m)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-12:
            return None
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [x / piv for x in a[c]]
        for r in range(k):
            if r != c and a[r][c]:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [r[k:] for r in a]


def calcola():
    db = sqlite3.connect(DB_ANALISI)
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    celle = cfg("modelli", "celle_vif")
    campo = cfg("predittore", "principale").replace("pct_rank_ext", "pct")

    def valori(colonne):
        """Righe con TUTTE le colonne richieste osservate."""
        sel = ", ".join("pct_%s" % c for c in colonne)
        w = " AND ".join("present_%s = 1" % c for c in colonne)
        return db.execute("""SELECT %s FROM tab_b WHERE sesso = ? AND
                             birth_year BETWEEN ? AND ? AND %s""" % (sel, w),
                          (sesso, lo, hi)).fetchall()

    with Archivio("correlazioni") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))
        ar.valore("celle_vif", celle)

        # --- matrice a coppie ----------------------------------------------
        tutte = cfg("modelli", "celle_correlazione")
        righe = []
        for i, a in enumerate(tutte):
            riga = [a]
            for j, b in enumerate(tutte):
                if j < i:
                    riga.append(None)
                elif j == i:
                    riga.append(1.0)
                else:
                    d = valori([a, b])
                    r = spearman([x[0] for x in d], [x[1] for x in d]) if len(d) >= 10 else None
                    riga.append(round(r, 2) if r is not None else None)
                    ar.valore("n_%s_%s" % (a, b), len(d))
            righe.append(riga)
        ar.tabella("matrice", righe, colonne=["cella"] + list(tutte),
                   titolo="Correlazione di Spearman fra i percentili",
                   nota="calcolata a coppie: ogni cella usa gli atleti presenti in "
                        "entrambe le celle, quindi le numerosita' non sono uguali")

        # la coppia piu' e meno correlata, per il testo
        coppie = []
        for i, a in enumerate(tutte):
            for j, b in enumerate(tutte):
                if j > i and righe[i][j + 1] is not None:
                    coppie.append((righe[i][j + 1], a, b))
        if coppie:
            coppie.sort()
            ar.valore("meno_correlate", list(coppie[0]))
            ar.valore("piu_correlate", list(coppie[-1]))

        # --- VIF, su un campione dichiarato ---------------------------------
        d = valori(celle)
        ar.valore("n_vif", len(d))
        if len(d) >= 3 * len(celle):
            colonne = [[r[i] for r in d] for i in range(len(celle))]
            rk = [ranghi(c) for c in colonne]
            R = [[1.0 if i == j else pearson(rk[i], rk[j]) or 0.0
                  for j in range(len(celle))] for i in range(len(celle))]
            inv = inverti(R)
            if inv:
                righe_v = []
                for i, c in enumerate(celle):
                    vif = inv[i][i]
                    righe_v.append([c, round(vif, 2), round(1 - 1 / vif, 3) if vif else None])
                ar.tabella("vif", righe_v,
                           colonne=["cella", "VIF", "R² sulle altre"],
                           titolo="Fattore di inflazione della varianza",
                           nota="calcolato sui %d atleti presenti in tutte le celle "
                                "elencate" % len(d))
                sopra = [r[0] for r in righe_v if r[1] > SOGLIA_VIF]
                ar.valore("vif_massimo", max(r[1] for r in righe_v))
                ar.valore("celle_sopra_soglia", sopra)
                ar.valore("penalizzazione_necessaria", len(sopra) >= 2,
                          nota="due o piu' variabili sopra VIF %g" % SOGLIA_VIF)
            else:
                ar.valore("vif_errore", "matrice di correlazione singolare")
        else:
            ar.valore("vif_errore",
                      "campione insufficiente: %d atleti per %d variabili"
                      % (len(d), len(celle)))

        if not os.environ.get("SENZA_FIGURE"):
            try:
                disegna(tutte, righe, ar)
            except SystemExit as e:
                print("   figura saltata: %s" % e)

    print("Modulo 'correlazioni' eseguito.")
    print("   VIF su %d atleti, %s" % (len(d), ", ".join(celle)))


def disegna(tutte, righe, ar):
    plt = gr.stile()
    n = len(tutte)
    m = [[righe[i][j + 1] if righe[i][j + 1] is not None else
          (righe[j][i + 1] if righe[j][i + 1] is not None else float("nan"))
          for j in range(n)] for i in range(n)]
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    im = ax.imshow(m, cmap="BuPu", vmin=0, vmax=1)
    ax.set_xticks(range(n))
    ax.set_xticklabels(tutte, rotation=45, ha="right")
    ax.set_yticks(range(n))
    ax.set_yticklabels(tutte)
    for i in range(n):
        for j in range(n):
            if m[i][j] == m[i][j]:
                ax.text(j, i, "%.2f" % m[i][j], ha="center", va="center", fontsize=8,
                        color="white" if m[i][j] > 0.6 else "#333333")
    ax.set_title("Quanto si somigliano i percentili di due categorie", loc="left", pad=12)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Spearman")
    ar.figura("matrice", gr.salva("correlazioni_matrice", fig),
              didascalia="Piu' le due celle sono vicine nel tempo, piu' l'ordinamento "
                         "degli atleti si somiglia. Nessuna coppia arriva a livelli tali "
                         "da rendere una delle due ridondante.")


def rendi(lt):
    v = lt.valori("correlazioni")
    matrice = lt.tabella("correlazioni", "matrice")
    vif = lt.tabella("correlazioni", "vif")

    p = [md.sezione("Quanto si somigliano le categorie")]
    p.append(md.paragrafo(
        "Se il rendimento a tredici anni e quello a diciassette dicono la stessa cosa, "
        "un modello che li usa entrambi non riesce a separarne i contributi. La domanda "
        "non e' accademica: decide se la parte modellistica potra' usare una regressione "
        "ordinaria o dovra' essere penalizzata."))

    p.append(md.metodo(
        "Correlazione di Spearman",
        "Si sostituisce a ogni percentile la sua posizione in graduatoria e si misura "
        "quanto le due graduatorie concordano. Vale 1 se l'ordine degli atleti e' "
        "identico nelle due categorie, 0 se non c'e' relazione.\n\n"
        "Si usa al posto della correlazione di Pearson perche' non richiede che la "
        "relazione sia lineare: interessa sapere se chi sta davanti a tredici anni sta "
        "davanti anche a diciassette, non se lo fa in proporzione fissa. Il quadrato "
        "del coefficiente si legge come quota di variabilita' dell'ordinamento "
        "condivisa fra le due categorie.",
        [("Correlazione di Spearman", W + "Spearman%27s_rank_correlation_coefficient")]))

    if matrice:
        p.append(md.tabella(matrice["colonne"], matrice["righe"],
                            decimali=2, nota=matrice["nota"]))
    if v.get("piu_correlate") and v.get("meno_correlate"):
        pc, mc = v["piu_correlate"], v["meno_correlate"]
        p.append(md.paragrafo(
            "",
            "La coppia piu' concorde e' **%s con %s** (%.2f), la meno concorde "
            "**%s con %s** (%.2f). L'ordine di grandezza e' quello che ci si aspetta: "
            "due stagioni consecutive si somigliano, due stagioni lontane molto meno."
            % (pc[1], pc[2], pc[0], mc[1], mc[2], mc[0])))

    f = lt.figura("correlazioni", "matrice")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.sezione("Serve la penalizzazione?", 3))
    p.append(md.metodo(
        "Fattore di inflazione della varianza (VIF)",
        "Per ogni cella si prova a prevederne il percentile a partire da tutte le "
        "altre. Se ci si riesce bene, quella cella non porta informazione propria e in "
        "un modello che le usa tutte il suo contributo non e' separabile dagli altri: "
        "i coefficienti diventano instabili e possono cambiare segno cambiando poche "
        "osservazioni.\n\n"
        "Il VIF vale 1 / (1 - R quadro) di quella previsione: 1 significa nessuna "
        "sovrapposizione, 5 significa che l'80% della variabilita' e' gia' spiegata "
        "dalle altre. Sopra 5 su piu' variabili la regressione penalizzata diventa "
        "necessaria.\n\n"
        "Richiede che tutte le variabili siano osservate sullo stesso atleta, ed e' il "
        "motivo per cui il campione qui e' molto piu' piccolo del totale.",
        [("Fattore di inflazione della varianza", W + "Variance_inflation_factor"),
         ("Multicollinearita'", W + "Multicollinearity")]))

    if vif:
        p.append(md.tabella(vif["colonne"], vif["righe"], decimali=2, nota=vif["nota"]))
        sopra = v.get("celle_sopra_soglia") or []
        if v.get("penalizzazione_necessaria"):
            p.append(md.paragrafo(
                "",
                "**Si': %d variabili superano la soglia di %g** (%s). Con questi valori i "
                "coefficienti di una regressione ordinaria sarebbero instabili, e la "
                "regressione penalizzata non e' un raffinamento ma un requisito."
                % (len(sopra), SOGLIA_VIF, ", ".join(sopra))))
        else:
            p.append(md.paragrafo(
                "",
                "**No.** Il VIF piu' alto e' %.2f, sotto la soglia di %g: le celle "
                "portano informazione abbastanza distinta da poter essere usate insieme "
                "in una regressione ordinaria. La versione penalizzata resta comunque "
                "utile come confronto, ma non e' obbligata."
                % (v.get("vif_massimo", 0), SOGLIA_VIF)))
    elif v.get("vif_errore"):
        p.append(md.paragrafo(
            "",
            "Il VIF non e' calcolabile sull'insieme richiesto: %s. E' esso stesso un "
            "risultato — vuol dire che quelle celle non sono osservate insieme abbastanza "
            "spesso perche' un modello possa usarle tutte." % v["vif_errore"]))

    p.append(md.paragrafo(
        "",
        "> Il VIF richiede che tutte le variabili siano osservate sullo stesso atleta, e "
        "il campione crolla: dei %s atleti delle coorti, solo **%s** compaiono in tutte le "
        "celle considerate. E' la stessa selezione che limita i modelli annidati, e va "
        "ricordata ogni volta che si cita un numero di questa sezione."
        % (lt.valore("attrito", "atleti_totali", "—"), v.get("n_vif", "—"))))
    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
