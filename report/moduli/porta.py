"""
Da quale porta si entra nel professionismo.

DA DOVE NASCE
    Da un'obiezione. La sezione sulla qualita' della carriera trova che il rendimento
    Under 19 predice l'ingresso nel professionismo e quasi nulla di cio' che viene dopo, e
    la spiega dicendo che la classifica giovanile «non misura piu' niente» una volta
    varcata la soglia.

    C'e' pero' una spiegazione alternativa, e non e' campata in aria: le squadre
    professionistiche italiane hanno bisogno di corridori italiani, e i migliori juniores
    italiani sono il bacino naturale da cui pescarli. Se e' cosi', il ranking predice
    l'ingresso perche' ordina bene quel bacino, senza che questo dica granche' su quanto
    quei ragazzi valgano in assoluto.

    L'ipotesi si puo' mettere alla prova, ed e' quello che fa questa sezione.

COME SI DISTINGUE UNA SQUADRA ITALIANA
    ProCyclingStats non pubblica la nazionalita' della squadra in una forma che abbiamo
    raccolto, ma pubblica le rose. Una squadra la cui rosa e' per meta' o piu' italiana e'
    con ottima approssimazione una squadra italiana: il controllo a campione restituisce
    esattamente i nomi che ci si aspetta.

    E' un **proxy**, non il dato di registrazione UCI, e va detto. Circa un professionista
    su cinque non e' classificabile, perche' la rosa della sua squadra al debutto non e'
    fra quelle scaricate.

LE TRE DOMANDE, IN ORDINE DI FORZA
    **Quanto e' grande la porta italiana?** Se il bacino nazionale conta, i posti italiani
    nelle squadre a maggioranza italiana sono la misura di quanti ne entrano ogni anno.

    **Il ranking predice meglio l'ingresso in una squadra italiana che in una straniera?**
    E' il test discriminante: se il ranking misurasse soprattutto «il migliore fra gli
    italiani», dovrebbe predire molto meglio la prima.

    **Le due porte portano allo stesso posto?** Se la qualita' successiva dipende da quale
    porta si e' varcata, allora il fatto che il ranking non predica la qualita' si spiega
    in parte con l'eterogeneita' dell'ingresso, e non solo con i limiti della misura.
"""
import os
import re
import sqlite3
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(QUI, "..", "..", "scripts"))
from lib_giovanile import DB_ANALISI, cfg          # noqa: E402
from lib_risultati import Archivio                 # noqa: E402
import lib_markdown as md                          # noqa: E402
import lib_grafici as gr                           # noqa: E402

DB_PCS = os.path.join("data", "pcs", "pcs.db")
W = "https://en.wikipedia.org/wiki/"

SOGLIA_ITALIANA = 0.5      # quota della rosa oltre la quale la squadra e' italiana
MIN_ROSA = 5               # rose piu' piccole non sono rappresentative
# Livello della squadra, per scegliere quella giusta quando un corridore ne ha piu' d'una
# nella stagione del debutto: si tiene la piu' alta.
LIVELLO = {"WT": 5, "PRT": 4, "PCT": 4, "PT": 4, "CT": 2, "CLUB": 1}


def _chiave(nome):
    return re.sub(r"[^a-z0-9]+", "", (nome or "").lower())


def _quote_italiane(db):
    """Quota di italiani nella rosa, per squadra e stagione."""
    return {(slug, st): q for slug, st, q in db.execute(
        """SELECT team_slug, season,
                  AVG(CASE WHEN nazionalita = 'IT' THEN 1.0 ELSE 0 END)
           FROM p.pcs_roster GROUP BY 1, 2 HAVING COUNT(*) >= %d""" % MIN_ROSA)}


def _porta_al_debutto(db):
    """Per ogni professionista, se abbia debuttato in una squadra italiana o straniera."""
    quote = _quote_italiane(db)
    per_nome = {(_chiave(nome), st): slug for st, slug, nome in
                db.execute("SELECT season, team_slug, team_name FROM p.pcs_team")}
    migliore = {}
    for aid, st, nome, classe in db.execute(
            """SELECT b.athlete_id, b.year_turned_pro, rt.team_name, rt.team_class
               FROM tab_b b JOIN p.pcs_rider_team rt
                    ON rt.pcs_id = b.pcs_id AND rt.season = b.year_turned_pro
               WHERE b.PRO = 1"""):
        if aid not in migliore or LIVELLO.get(classe, 0) > LIVELLO.get(migliore[aid][2], 0):
            migliore[aid] = (st, nome, classe)

    porta, senza = {}, 0
    for aid, (st, nome, _) in migliore.items():
        slug = per_nome.get((_chiave(nome), st))
        q = quote.get((slug, st)) if slug else None
        if q is None:
            senza += 1
            continue
        porta[aid] = "italiana" if q >= SOGLIA_ITALIANA else "internazionale"
    return porta, len(migliore), senza


def auc(valori, esiti):
    """Probabilita' che un caso positivo stia sopra un negativo, presi a caso."""
    su = [v for v, e in zip(valori, esiti) if e]
    giu = [v for v, e in zip(valori, esiti) if not e]
    if not su or not giu:
        return None
    vinte = sum(1 for a in su for b in giu if a > b)
    pari = sum(1 for a in su for b in giu if a == b)
    return (vinte + 0.5 * pari) / (len(su) * len(giu))


def calcola():
    if not os.path.exists(DB_PCS):
        print("   porta: manca %s, salto il modulo" % DB_PCS)
        return
    db = sqlite3.connect(DB_ANALISI)
    db.execute("ATTACH DATABASE ? AS p", (DB_PCS,))

    porta, totali, senza = _porta_al_debutto(db)
    if len(porta) < 50:
        print("   porta: troppo pochi professionisti classificabili, salto il modulo")
        return

    with Archivio("porta") as ar:
        ar.valore("professionisti_con_squadra", totali)
        ar.valore("non_classificabili", senza)
        ar.valore("soglia_italiana", int(SOGLIA_ITALIANA * 100))

        # --- 1. quanto e' grande la porta italiana ---------------------------
        stagioni = [r[0] for r in db.execute(
            """SELECT DISTINCT season FROM p.pcs_roster WHERE season >= 2015 ORDER BY 1""")]
        posti = []
        for st in stagioni:
            n = db.execute(
                """SELECT COUNT(*) FROM p.pcs_roster r
                   WHERE r.season = ? AND r.nazionalita = 'IT' AND r.team_slug IN (
                       SELECT team_slug FROM p.pcs_roster WHERE season = ?
                       GROUP BY team_slug
                       HAVING AVG(CASE WHEN nazionalita = 'IT' THEN 1.0 ELSE 0 END) >= ?
                          AND COUNT(*) >= ?)""",
                (st, st, SOGLIA_ITALIANA, MIN_ROSA)).fetchone()[0]
            if n:
                posti.append([st, n])
        if len(posti) >= 5:
            ar.tabella("posti_italiani", posti,
                       colonne=["stagione", "corridori italiani"],
                       titolo="Quanti italiani corrono nelle squadre a maggioranza italiana",
                       nota="conteggio delle rose, non dei posti che si liberano ogni anno")
            ar.valore("posti_estremi", {"prima": posti[0][0], "n_prima": posti[0][1],
                                        "ultima": posti[-1][0], "n_ultima": posti[-1][1]})

        # --- 2. il ranking predice meglio una porta o l'altra? ---------------
        righe = list(db.execute(
            """SELECT athlete_id, pct_U19y2, PRO, tier FROM tab_b
               WHERE present_U19y2 = 1 AND pct_U19y2 IS NOT NULL"""))
        valori = [r[1] for r in righe]
        confronto = []
        for etichetta, quale in (("in una squadra a maggioranza italiana", "italiana"),
                                 ("in una squadra internazionale", "internazionale")):
            esiti = [1 if (r[2] == 1 and porta.get(r[0]) == quale) else 0 for r in righe]
            a = auc(valori, esiti)
            if a is None:
                continue
            confronto.append([etichetta, sum(esiti), round(a, 3)])
        if len(confronto) == 2:
            ar.tabella("previsione", confronto,
                       colonne=["diventare professionista…", "casi",
                                "quanto il percentile Under 19 li distingue"],
                       titolo="Il ranking predice meglio una porta o l'altra?",
                       nota="stessa popolazione, %s atleti in classifica al secondo anno "
                            "da Juniores; il valore e' la probabilita' che il modello "
                            "metta davanti quello giusto" % len(righe))
            ar.valore("auc_porte", {"italiana": confronto[0][2],
                                    "internazionale": confronto[1][2],
                                    "n": len(righe)})

        # --- 3. le due porte portano allo stesso posto? ----------------------
        esiti_q = []
        for quale in ("italiana", "internazionale"):
            sub = [r for r in righe if r[2] == 1 and porta.get(r[0]) == quale]
            if len(sub) < 20:
                continue
            top = [r for r in sub if (r[3] or 0) >= 2]
            a = auc([r[1] for r in sub], [1 if (r[3] or 0) >= 2 else 0 for r in sub])
            esiti_q.append([quale, len(sub), len(top), round(100 * len(top) / len(sub), 1),
                            round(a, 3) if a is not None else None])
        if len(esiti_q) == 2:
            ar.tabella("qualita_per_porta", esiti_q,
                       colonne=["porta d'ingresso", "professionisti", "arrivati nel top 500",
                                "quota", "il percentile Under 19 li distingue"],
                       titolo="Dove si arriva, a seconda della porta",
                       nota="l'ultima colonna e' calcolata fra i soli professionisti di "
                            "quel gruppo: dice se il rendimento giovanile aiuti a capire "
                            "chi andra' lontano una volta entrato")
            ar.valore("qualita_porte", {r[0]: {"n": r[1], "top500": r[2], "quota": r[3],
                                               "auc": r[4]} for r in esiti_q})

        disegna(posti, esiti_q, ar)

    print("   porta: %d professionisti classificati, il %.0f%% entra da una squadra "
          "a maggioranza italiana"
          % (len(porta),
             100 * sum(1 for x in porta.values() if x == "italiana") / len(porta)))


def disegna(posti, esiti_q, ar):
    if os.environ.get("SENZA_FIGURE") or len(posti) < 5:
        return
    gr.stile()
    with gr.figura("Quanti posti ci sono nelle squadre italiane", altezza=3.4) as (f, ax):
        ax.plot([p[0] for p in posti], [p[1] for p in posti], marker="o", markersize=4,
                linewidth=2, color=gr.COLORI[0])
        ax.set_ylabel("corridori italiani in rosa")
        ax.set_ylim(bottom=0)
        ax.grid(axis="x", visible=False)
    ar.figura("posti_italiani", gr.salva("porta_posti"),
              didascalia="La porta principale del professionismo italiano si e' ristretta "
                         "di circa un terzo in dieci anni. E' un conteggio delle rose, non "
                         "dei posti che si liberano: quelli sono molti di meno.")


def rendi(lt):
    v = lt.valori("porta")
    prev = lt.tabella("porta", "previsione")
    qual = lt.tabella("porta", "qualita_per_porta")
    posti = lt.tabella("porta", "posti_italiani")

    p = [md.sezione("Da quale porta si entra")]
    if not prev:
        p.append(md.paragrafo("*Sezione non disponibile: mancano le rose di "
                              "ProCyclingStats.*"))
        return (chr(10) * 2).join(x.strip() for x in p if x)

    p.append(md.paragrafo(
        "La sezione precedente ha trovato che il rendimento Under 19 predice l'ingresso nel "
        "professionismo e quasi nulla di cio' che viene dopo, e lo ha spiegato dicendo che "
        "la classifica giovanile smette di misurare qualcosa oltre quella soglia. C'e' pero' "
        "una spiegazione alternativa che merita di essere messa alla prova: le squadre "
        "professionistiche italiane hanno bisogno di corridori italiani, e i migliori "
        "juniores nazionali sono il bacino da cui pescano. Se fosse cosi', il ranking "
        "predirebbe l'ingresso perche' ordina bene quel bacino, non perche' misuri il valore "
        "assoluto di un atleta."))

    p.append(md.metodo(
        "Come si riconosce una squadra italiana, e con quale approssimazione",
        "La nazionalita' di registrazione delle squadre non e' fra i dati raccolti, ma le "
        "rose si': una squadra la cui rosa e' per meta' o piu' italiana e' con ottima "
        "approssimazione una squadra italiana, e il controllo a campione restituisce "
        "esattamente i nomi che ci si aspetta.\n\n"
        "E' un **proxy**: nessuna delle conclusioni che seguono dipende da un singolo caso "
        "limite, ma la classificazione non e' un dato ufficiale. Dei %s professionisti di "
        "cui si conosce la squadra al debutto, %s non sono classificabili perche' la rosa "
        "di quella squadra non e' fra quelle scaricate.\n\n"
        "Quando un corridore compare in piu' squadre nella stagione del debutto si tiene "
        "quella di livello piu' alto."
        % (md.conta(v.get("professionisti_con_squadra")),
           md.conta(v.get("non_classificabili")))))

    if posti:
        est = v.get("posti_estremi") or {}
        p.append(md.paragrafo(
            "La prima cosa da guardare e' quanto sia grande quella porta. Nelle squadre a "
            "maggioranza italiana i corridori italiani in rosa sono passati da %s nel %s a "
            "%s nel %s."
            % (md.conta(est.get("n_prima")), est.get("prima"),
               md.conta(est.get("n_ultima")), est.get("ultima"))))
        f = lt.figura("porta", "posti_italiani")
        if f:
            p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.sezione("Il test discriminante", 3))
    p.append(md.paragrafo(
        "Se il ranking misurasse soprattutto «il migliore fra gli italiani», dovrebbe "
        "predire l'ingresso in una squadra italiana molto meglio dell'ingresso in una "
        "squadra straniera, dove la concorrenza non e' nazionale. Le due previsioni si "
        "calcolano sulla stessa popolazione e con lo stesso predittore."))
    p.append(md.tabella(prev["colonne"],
                        [[r[0], md.conta(r[1]), md.num(r[2], 3)] for r in prev["righe"]],
                        nota=prev["nota"], colonne_conteggio=(1,)))

    ap = v.get("auc_porte") or {}
    if ap:
        p.append(md.paragrafo(
            "",
            md.afferma(
                abs(ap.get("italiana", 0) - ap.get("internazionale", 0)) < 0.05,
                "il percentile Under 19 distingue in modo quasi identico chi entrera' in "
                "una squadra italiana e chi in una straniera",
                "**La versione forte dell'ipotesi non regge.** Il percentile Under 19 "
                "distingue chi entrera' in una squadra italiana con %s e chi entrera' in "
                "una squadra straniera con %s: praticamente lo stesso valore. Se il "
                "ranking fosse soltanto una graduatoria del bacino nazionale, la seconda "
                "cifra dovrebbe essere molto piu' bassa. Quello che misura, qualunque cosa "
                "sia, interessa anche a chi non ha bisogno di italiani."
                % (md.num(ap.get("italiana"), 3), md.num(ap.get("internazionale"), 3)))))

    if qual:
        p.append(md.sezione("Ma le due porte non portano allo stesso posto", 3))
        p.append(md.tabella(
            qual["colonne"],
            [[r[0], md.conta(r[1]), md.conta(r[2]), md.num(r[3], 1) + "%",
              md.num(r[4], 3) if r[4] is not None else "—"] for r in qual["righe"]],
            nota=qual["nota"], colonne_conteggio=(1, 2)))

        qp = v.get("qualita_porte") or {}
        ita, inter = qp.get("italiana", {}), qp.get("internazionale", {})
        if ita and inter:
            p.append(md.paragrafo(
                "",
                md.afferma(
                    inter.get("quota", 0) > ita.get("quota", 100),
                    "chi debutta in una squadra internazionale arriva nel top 500 piu' "
                    "spesso di chi debutta in una squadra a maggioranza italiana",
                    "**Qui invece l'ipotesi trova il suo sostegno.** Di chi debutta in una "
                    "squadra a maggioranza italiana arriva nel top 500 mondiale il %s%%; "
                    "di chi debutta in una squadra straniera, il %s%%. La stessa soglia, "
                    "due destini molto diversi."
                    % (md.num(ita.get("quota"), 1), md.num(inter.get("quota"), 1)))))

            p.append(md.paragrafo(
                "",
                "Ne segue una lettura piu' precisa del risultato della sezione precedente. "
                "Non e' che il rendimento giovanile smetta di contare oltre la soglia del "
                "professionismo: e' che **la soglia non e' una sola**. Passare dalla porta "
                "italiana e passare da quella internazionale sono due eventi diversi, con "
                "esiti diversi, e il ranking li predice entrambi allo stesso modo. "
                "Mettendoli insieme in un unico esito «professionista», una parte della "
                "capacita' predittiva si perde per costruzione."))

            if ita.get("auc") is not None and inter.get("auc") is not None:
                p.append(md.paragrafo(
                    "",
                    "Dentro ciascun gruppo, poi, il rendimento giovanile aiuta poco a "
                    "capire chi andra' lontano: %s fra chi e' entrato da una squadra "
                    "italiana e %s fra chi e' entrato da una straniera, dove 0,5 "
                    "significa tirare a indovinare. Su questi numeri sono indicazioni, non "
                    "stime: i due gruppi contano %s e %s professionisti."
                    % (md.num(ita.get("auc"), 3), md.num(inter.get("auc"), 3),
                       md.conta(ita.get("n")), md.conta(inter.get("n")))))

    p.append(md.paragrafo(
        "",
        "> **Cosa resta non verificato.** Questa sezione dice che la nazionalita' conta, "
        "ma non misura *quanto* pesi rispetto al valore dell'atleta: per farlo servirebbe "
        "confrontare corridori italiani e stranieri a parita' di rendimento giovanile, e i "
        "ranking giovanili degli altri paesi non sono nei dati. Resta anche possibile che "
        "la differenza fra le due porte non dipenda dalla porta ma da chi la sceglie: chi "
        "e' piu' forte va all'estero, e sarebbe arrivato lontano comunque."))

    return (chr(10) * 2).join(x.strip() for x in p if x)
