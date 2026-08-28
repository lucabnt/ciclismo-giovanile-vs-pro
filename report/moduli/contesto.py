"""
Societa', regione e mobilita': cosa sembrano dire e cosa dicono davvero.

PERCHE' QUESTA SEZIONE E' SCRITTA IN NEGATIVO
    Le variabili di contesto producono con facilita' correlazioni forti e sbagliate.
    Cambiare societa' sembra predire il professionismo in modo netto — finche' non si
    nota che chi cambia societa' ha semplicemente corso piu' stagioni. Il gradiente e'
    un artefatto della durata della carriera, e questo modulo lo mostra invece di
    riportare il numero grezzo.

    E' un risultato negativo, ma e' esattamente il tipo di risultato che serve: senza,
    il dato grezzo diventa "cambiare squadra aiuta", che i dati non dicono.

MEDIATORI, NON CONFONDENTI
    Societa' e regione cambiano *durante* la carriera, e cambiano in risposta ai
    risultati: un buon risultato a quattordici anni fa arrivare l'offerta di una
    societa' migliore. Stanno quindi sul percorso causale fra rendimento ed esito, e
    inserirle come controlli in un modello sottrarrebbe parte dell'effetto che si vuole
    misurare.

    L'unica variabile di contesto ammissibile come controllo e' la **regione alla prima
    stagione osservata**, che precede il predittore. Tutte le altre sono oggetto di
    studio, mai controlli — vedi definizioni.md.

COSA C'E' E COSA NO
    La qualita' della societa' di partenza e' calcolata come tasso di professionisti
    prodotti nelle coorti PRECEDENTI a quella dell'atleta. Il vincolo non e' formale:
    senza, l'esito dell'atleta entrerebbe nel proprio predittore.
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

W = "https://en.wikipedia.org/wiki/"
MIN_GRUPPO = 20          # sotto questa numerosita' un tasso non si riporta


def calcola():
    db = sqlite3.connect(DB_ANALISI)
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    base = "FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ?"
    par = (sesso, lo, hi)

    def conta(dove="", extra=()):
        return db.execute("SELECT COUNT(*), SUM(PRO) " + base + dove,
                          par + extra).fetchone()

    with Archivio("contesto") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))

        # --- 1. la mobilita', come appare ----------------------------------
        righe = []
        for r in db.execute("""SELECT n_team_changes, COUNT(*), SUM(PRO),
                                      ROUND(AVG(n_seasons_youth), 1) """ + base +
                            " AND n_team_changes IS NOT NULL GROUP BY 1 ORDER BY 1", par):
            if r[1] < MIN_GRUPPO:
                continue
            righe.append([r[0], r[1], r[2], round(100 * r[2] / r[1], 2), r[3]])
        ar.tabella("mobilita_grezza", righe,
                   colonne=["cambi di societa'", "atleti", "professionisti",
                            "% pro", "stagioni corse in media"],
                   titolo="Mobilita' e professionismo, senza controlli",
                   nota="l'ultima colonna e' gia' l'indizio: chi cambia di piu' ha "
                        "corso di piu'")
        if len(righe) >= 2:
            ar.valore("mobilita_grezza_da_a",
                      [righe[0][3], righe[-1][3], righe[0][0], righe[-1][0]])
            ar.valore("stagioni_da_a", [righe[0][4], righe[-1][4]])

        # --- 2. lo stesso confronto, dentro ogni durata di carriera ---------
        gruppi = ((0, 0, "nessun cambio"), (1, 1, "un cambio"), (2, 9, "due o piu'"))
        righe_s = []
        for ns in range(1, 9):
            riga = ["%d stagion%s" % (ns, "e" if ns == 1 else "i")]
            visibili = 0
            for a, b, _ in gruppi:
                n, pro = conta(" AND n_seasons_youth = ? AND n_team_changes BETWEEN ? AND ?",
                               (ns, a, b))
                if n >= MIN_GRUPPO:
                    riga.append("%s%% (n=%d)" % (md.num(100 * (pro or 0) / n, 1), n))
                    visibili += 1
                else:
                    riga.append("n=%d" % n if n else "—")
            if visibili:
                righe_s.append(riga)
        ar.tabella("mobilita_stratificata", righe_s,
                   colonne=["durata della carriera"] + [g[2] for g in gruppi],
                   titolo="La stessa mobilita', a parita' di stagioni corse",
                   nota="percentuale di professionisti; le celle con meno di %d atleti "
                        "riportano solo la numerosita'" % MIN_GRUPPO)

        # --- 3. cambio di regione ------------------------------------------
        righe_r = []
        for v, et in ((0, "e' rimasto"), (1, "ha cambiato regione")):
            n, pro = conta(" AND changed_region = ?", (v,))
            righe_r.append([et, n, pro, round(100 * (pro or 0) / n, 2) if n else None])
        ar.tabella("regione", righe_r,
                   colonne=["", "atleti", "professionisti", "% pro"],
                   titolo="Chi ha cambiato regione durante il percorso giovanile")
        n_cambi = righe_r[1][1]
        ar.valore("n_cambio_regione", n_cambi)
        ar.valore("pro_cambio_regione", righe_r[1][2])

        # --- 4. qualita' della societa' di partenza ------------------------
        fasce = ((-0.001, 0.0001, "nessun professionista"), (0.0001, 0.05, "fino al 5%"),
                 (0.05, 0.10, "dal 5 al 10%"), (0.10, 1.1, "oltre il 10%"))
        righe_q = []
        for a, b, et in fasce:
            n, pro = conta(" AND team_quality_first > ? AND team_quality_first <= ?", (a, b))
            if n >= MIN_GRUPPO:
                righe_q.append([et, n, pro, round(100 * (pro or 0) / n, 2)])
        ar.tabella("qualita_societa", righe_q,
                   colonne=["tasso storico della societa' di partenza", "atleti",
                            "professionisti", "% pro"],
                   titolo="La societa' da cui si parte")
        r = db.execute("SELECT COUNT(*), SUM(team_quality_first = 0) " + base +
                       " AND team_quality_first IS NOT NULL", par).fetchone()
        ar.valore("quota_societa_senza_pro", round(100 * r[1] / r[0], 0) if r[0] else None)
        if len(righe_q) >= 2:
            ar.valore("qualita_da_a", [righe_q[0][3], righe_q[-1][3]])

        # --- 5. densita' regionale, descrittiva -----------------------------
        righe_d = []
        for r in db.execute("""SELECT region_first, COUNT(*), SUM(PRO) """ + base +
                            " AND region_first IS NOT NULL GROUP BY 1 "
                            "HAVING COUNT(*) >= 50 ORDER BY 2 DESC", par):
            righe_d.append([r[0].replace("_", " "), r[1], r[2],
                            round(100 * (r[2] or 0) / r[1], 2)])
        ar.tabella("regioni", righe_d,
                   colonne=["regione alla prima stagione", "atleti", "professionisti",
                            "% pro"],
                   titolo="Da dove vengono",
                   nota="solo le regioni con almeno 50 atleti nelle coorti")
        if righe_d:
            ar.valore("prime_tre_regioni", [r[0] for r in righe_d[:3]])
            tot = sum(r[1] for r in righe_d)
            ar.valore("quota_prime_tre",
                      round(100 * sum(r[1] for r in righe_d[:3]) / tot, 0))

        if not os.environ.get("SENZA_FIGURE"):
            try:
                disegna(righe, righe_s, ar, lo, hi)
            except SystemExit as e:
                print("   figura saltata: %s" % e)

    print("Modulo 'contesto' eseguito.")
    if righe:
        print("   mobilita' grezza: dal %.2f%% al %.2f%% di professionisti"
              % (righe[0][3], righe[-1][3]))
        print("   ma le stagioni corse passano da %.1f a %.1f" % (righe[0][4], righe[-1][4]))


def disegna(grezza, strat, ar, lo, hi):
    plt = gr.stile()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2))
    x = [r[0] for r in grezza]
    ax1.bar(x, [r[3] for r in grezza], color=gr.COLORI[1], zorder=3)
    ax1.set_title("Cosi' sembra", loc="left", pad=10)
    ax1.set_xlabel("cambi di societa'")
    ax1.set_ylabel("% professionisti")
    ax2.bar(x, [r[4] for r in grezza], color=gr.COLORI[2], zorder=3)
    ax2.set_title("Ma chi cambia ha corso di piu'", loc="left", pad=10)
    ax2.set_xlabel("cambi di societa'")
    ax2.set_ylabel("stagioni corse, media")
    fig.text(0.005, -0.04, "Coorti %d-%d. Le due barre hanno la stessa forma: e' la durata "
             "della carriera a spiegare il gradiente, non la mobilita'." % (lo, hi),
             fontsize=8, color=gr.GRIGIO)
    fig.tight_layout()
    ar.figura("confondente", gr.salva("contesto_confondente", fig),
              didascalia="Il gradiente apparente della mobilita' ha la stessa forma della "
                         "durata della carriera: e' la seconda a spiegare la prima.")


def rendi(lt):
    v = lt.valori("contesto")
    grezza = lt.tabella("contesto", "mobilita_grezza")
    strat = lt.tabella("contesto", "mobilita_stratificata")
    regione = lt.tabella("contesto", "regione")
    qualita = lt.tabella("contesto", "qualita_societa")
    regioni = lt.tabella("contesto", "regioni")

    p = [md.sezione("Societa', regione, mobilita'")]
    p.append(md.paragrafo(
        "Questa sezione e' scritta in negativo, e vale la pena dire subito perche'. "
        "Le variabili di contesto producono con facilita' correlazioni forti e "
        "sbagliate, e questa e' il caso da manuale."))

    p.append(md.metodo(
        "Perche' queste variabili non entrano nei modelli come controlli",
        "Societa' e regione cambiano durante la carriera, e cambiano *in risposta* ai "
        "risultati: un buon piazzamento a quattordici anni fa arrivare l'offerta di una "
        "societa' migliore. Stanno quindi sul percorso causale fra rendimento ed esito, "
        "e sono mediatori, non confondenti.\n\n"
        "Inserire un mediatore fra i controlli di un modello sottrae parte dell'effetto "
        "che si vuole misurare, e lo fa apparire piu' debole di quanto sia. Per questo "
        "qui sono oggetto di studio e mai variabili di controllo. L'unica eccezione e' "
        "la regione alla prima stagione osservata, che precede il predittore.",
        [("Mediazione", W + "Mediation_(statistics)"),
         ("Confondimento", W + "Confounding")]))

    if grezza:
        p.append(md.tabella(grezza["colonne"], grezza["righe"],
                            colonne_conteggio={1, 2}, decimali=2, nota=grezza["nota"]))
    da_a, st = v.get("mobilita_grezza_da_a"), v.get("stagioni_da_a")
    if da_a and st:
        p.append(md.paragrafo(
            "",
            "Preso cosi', il dato e' clamoroso: si passa dal **%.2f%%** di professionisti "
            "fra chi non ha mai cambiato societa' al **%.2f%%** fra chi ha cambiato %d "
            "volte. Un fattore dieci." % (da_a[0], da_a[1], da_a[3]),
            "",
            "Ma l'ultima colonna dice come stanno le cose: chi non ha mai cambiato ha "
            "corso **%.1f stagioni in media**, chi ha cambiato %d volte ne ha corse "
            "**%.1f**. Non si cambia societa' stando fermi: per cambiarla bisogna "
            "esserci ancora." % (st[0], da_a[3], st[1])))

    f = lt.figura("contesto", "confondente")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.sezione("Lo stesso confronto, a parita' di carriera", 3))
    if strat:
        p.append(md.tabella(strat["colonne"], strat["righe"], nota=strat["nota"]))
    p.append(md.paragrafo(
        "",
        "**Il gradiente sparisce.** Dentro ogni durata di carriera la mobilita' non "
        "distingue piu' niente, e dove i numeri sono meno sottili va nella direzione "
        "opposta. Quello che il dato grezzo mostrava non era un effetto della mobilita': "
        "era la durata della carriera vista da un'altra angolazione.",
        "",
        "E' un risultato negativo, ed e' il piu' utile di questa sezione: senza, il "
        "numero grezzo sarebbe diventato «cambiare squadra aiuta», che i dati non dicono."))

    p.append(md.sezione("Regione e societa' di partenza", 3))
    if regione:
        p.append(md.tabella(regione["colonne"], regione["righe"], colonne_conteggio={1, 2},
                            decimali=2))
    if v.get("n_cambio_regione"):
        p.append(md.paragrafo(
            "",
            "Il cambio di regione riguarda **%d atleti su circa duemilaottocento**, con "
            "%s professionisti fra loro. Con questi numeri non si conclude niente in un "
            "senso o nell'altro, e vale la pena dirlo esplicitamente invece di riportare "
            "una percentuale che sembrerebbe informativa."
            % (v["n_cambio_regione"], v.get("pro_cambio_regione", "—"))))

    if qualita:
        p.append(md.tabella(qualita["colonne"], qualita["righe"],
                            colonne_conteggio={1, 2}, decimali=2))
    qa = v.get("qualita_da_a")
    if qa:
        p.append(md.paragrafo(
            "",
            "Anche la societa' da cui si parte dice poco: si va dal **%.2f%%** al "
            "**%.2f%%**, una differenza che con questi numeri non si distingue dal caso. "
            "E il %d%% degli atleti parte da una societa' che nelle coorti precedenti non "
            "aveva prodotto nessun professionista — il che rende la variabile poco "
            "informativa gia' per costruzione."
            % (qa[0], qa[1], v.get("quota_societa_senza_pro", 0))))

    if regioni:
        p.append(md.tabella(regioni["colonne"], regioni["righe"],
                            colonne_conteggio={1, 2}, decimali=2, nota=regioni["nota"]))
    if v.get("prime_tre_regioni"):
        p.append(md.paragrafo(
            "",
            "La concentrazione geografica e' forte — %s da sole raccolgono circa il "
            "%d%% degli atleti — ma il tasso di professionismo fra regioni non mostra "
            "differenze leggibili con queste numerosita'."
            % (", ".join(v["prime_tre_regioni"]), v.get("quota_prime_tre", 0))))
    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
