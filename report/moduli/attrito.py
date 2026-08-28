"""
Attrito: quanti restano, a quale eta' se ne vanno, quanti arrivano in fondo.

PERCHE' E' LA PRIMA SEZIONE
    Contestualizza tutto il resto. La maggior parte dell'abbandono avviene molto prima
    del punto in cui la prestazione diventa predittiva: senza questo numero davanti, i
    risultati sulla predittivita' vengono letti come piu' potenti di quanto siano.

TRE LETTURE, che dicono cose diverse

    L'imbuto        quanti atleti sono presenti in ciascuna categoria.
    La ritenzione   di chi era in Under 15, quanti si ritrovano dopo. Non e' la stessa
                    cosa: una quota consistente di ogni categoria non compare mai in
                    Under 15, quindi l'imbuto non e' una catena di sottoinsiemi e i due
                    numeri divergono.
    L'uscita        l'eta' dell'ultima presenza in classifica. E' la lettura piu'
                    informativa delle tre, perche' mostra *quando* si smette.

UN LIMITE CHE VALE PER TUTTO IL MODULO, e che qui viene misurato
    "Presente" significa "ha ottenuto almeno un punto". Chi ha corso una stagione intera
    senza mai andare a punti e' indistinguibile da chi non ha corso: l'attrito misurato
    qui e' quindi l'uscita dalla classifica, non l'abbandono dello sport.

    Non e' pero' una cautela generica da mettere in nota: passando di categoria si corre
    contro avversari piu' grandi, ed e' normale smettere di andare a punti pur
    continuando a correre. E' un RICAMBIO fra chi sta ai livelli alti, non un abbandono.
    Il modulo lo misura in due modi indipendenti — quanti spariscono e poi tornano, e
    quanto cambia la composizione di una cella rispetto a quella dell'anno prima nella
    stessa categoria — e i numeri sono grandi abbastanza da cambiare la lettura
    dell'imbuto, non solo da accompagnarla.
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

CATEGORIE = ("U15", "U17", "U19", "U23")

# Eta' del primo e dell'ultimo anno di ciascuna categoria: serve a distinguere chi esce
# a meta' percorso da chi esce dopo aver completato la categoria.
FASCE = {"U15": (13, 14), "U17": (15, 16), "U19": (17, 18), "U23": (19, 22)}

PRESENTE = {
    "U15": "(present_U15y1 = 1 OR present_U15y2 = 1)",
    "U17": "(present_U17y1 = 1 OR present_U17y2 = 1)",
    "U19": "(present_U19y1 = 1 OR present_U19y2 = 1)",
    "U23": "(present_U23y1 + present_U23y2 + present_U23y3 + present_U23y4) > 0",
}


def calcola():
    db = sqlite3.connect(DB_ANALISI)
    sesso = cfg("studio", "sesso")
    lo, hi = cfg("coorti", "domanda_a_c")
    base = "FROM tab_b WHERE sesso = ? AND birth_year BETWEEN ? AND ?"
    par = (sesso, lo, hi)

    def conta(dove=""):
        return db.execute("SELECT COUNT(*) " + base + dove, par).fetchone()[0]

    with Archivio("attrito") as ar:
        ar.valore("coorti", "%d-%d" % (lo, hi))
        totale = conta()
        ar.valore("atleti_totali", totale)

        # --- l'imbuto, nelle due letture -----------------------------------
        n_u15 = conta(" AND " + PRESENTE["U15"])
        righe, precedente, curva = [], None, []
        for cat in CATEGORIE:
            n = conta(" AND " + PRESENTE[cat])
            da_u15 = conta(" AND %s AND %s" % (PRESENTE["U15"], PRESENTE[cat]))
            if precedente:
                da_prec = conta(" AND %s AND %s" % (PRESENTE[precedente], PRESENTE[cat]))
                n_prec = conta(" AND " + PRESENTE[precedente])
                pct_prec = 100 * da_prec / n_prec if n_prec else None
            else:
                pct_prec = None
            tardivi = conta(" AND NOT %s AND %s" % (PRESENTE["U15"], PRESENTE[cat]))
            righe.append([cat, n, round(100 * da_u15 / n_u15, 1),
                          round(pct_prec, 1) if pct_prec is not None else None,
                          round(100 * tardivi / n, 1) if n else None])
            curva.append((cat, n, 100 * da_u15 / n_u15))
            precedente = cat

        ar.tabella("imbuto", righe,
                   colonne=["categoria", "atleti", "% di chi era in U15",
                            "% del livello precedente", "% mai visti in U15"],
                   titolo="Quanti restano, categoria per categoria")
        ar.valore("curva", [(c, n, round(p, 1)) for c, n, p in curva])
        ar.valore("ritenzione_u15_u23", round(curva[-1][2], 1))

        # --- gli esiti, in coda all'imbuto ---------------------------------
        righe_e = []
        for etichetta, filtro in (("professionisti", "PRO = 1"),
                                  ("top 500", "tier >= 2"),
                                  ("top 100", "tier = 3")):
            n = conta(" AND " + filtro)
            da_u15 = conta(" AND %s AND %s" % (PRESENTE["U15"], filtro))
            righe_e.append([etichetta, n, round(100 * n / n_u15, 2), da_u15])
        ar.tabella("esiti", righe_e,
                   colonne=["esito", "atleti", "% dei partenti U15", "veniva dall'U15"],
                   titolo="Chi arriva in fondo")
        pro = conta(" AND PRO = 1")
        ar.valore("pro_totali", pro)
        ar.valore("pro_su_mille_u15", round(1000 * pro / n_u15, 1))
        ar.valore("pro_dall_u15", conta(" AND %s AND PRO = 1" % PRESENTE["U15"]))

        # --- l'uscita: a che eta' si smette --------------------------------
        eta = dict(db.execute("SELECT last_racing_age, COUNT(*) " + base +
                              " AND last_racing_age IS NOT NULL GROUP BY 1", par))
        ar.valore("uscite_per_eta", sorted(eta.items()))

        righe_u = []
        for cat in CATEGORIE:
            primo, ultimo = FASCE[cat]
            dentro = sum(n for e, n in eta.items() if primo <= e <= ultimo)
            alla_fine = eta.get(ultimo, 0)
            if not dentro:
                continue
            righe_u.append([cat, "%d-%d" % (primo, ultimo), dentro, alla_fine,
                            round(100 * alla_fine / dentro, 1)])
        ar.tabella("uscite", righe_u,
                   colonne=["categoria", "eta'", "escono nella categoria",
                            "escono all'ultimo anno", "% all'ultimo anno"],
                   titolo="Quando si esce dalla classifica",
                   nota="l'ultimo anno di categoria e' quello in cui si e' costretti "
                        "a cambiare fascia")
        if righe_u:
            fine = [r for r in righe_u if r[0] != "U23"]
            ar.valore("quota_uscite_a_fine_categoria",
                      round(100 * sum(r[3] for r in fine) / sum(r[2] for r in fine), 1),
                      nota="fra chi esce nelle categorie U15, U17 e U19")

        # --- il ricambio: uscire dalla classifica non e' uscire dallo sport --
        # Due misure indipendenti, che dicono la stessa cosa da due lati:
        # chi sparisce e torna, e quanto cambia la composizione di una cella
        # rispetto a quella precedente della stessa categoria.
        per_atleta = {}
        for a, s in db.execute("""SELECT athlete_id, season FROM tab_a
                                  WHERE sesso = ? AND birth_year BETWEEN ? AND ?
                                    AND cat_year IS NOT NULL""", par):
            per_atleta.setdefault(a, set()).add(s)
        n_att = len(per_atleta)
        con_buco = sum(1 for s in per_atleta.values() if max(s) - min(s) + 1 > len(s))
        lunghi = sum(1 for s in per_atleta.values()
                     for o in [sorted(s)]
                     if any(o[i + 1] - o[i] > 2 for i in range(len(o) - 1)))
        ar.valore("rientri_dopo_assenza", round(100 * con_buco / n_att, 1),
                  nota="percentuale di atleti che salta almeno una stagione e poi torna")
        ar.valore("rientri_dopo_assenza_lunga", round(100 * lunghi / n_att, 1),
                  nota="assenza di due stagioni o piu'")

        righe_r = []
        for primo, secondo in (("U15y1", "U15y2"), ("U17y1", "U17y2"), ("U19y1", "U19y2")):
            n_sec = conta(" AND present_%s = 1" % secondo)
            nuovi = conta(" AND present_%s = 1 AND present_%s = 0" % (secondo, primo))
            if n_sec:
                righe_r.append([secondo, n_sec, nuovi, round(100 * nuovi / n_sec, 1)])
        ar.tabella("ricambio", righe_r,
                   colonne=["cella", "atleti", "non c'erano l'anno prima", "%"],
                   titolo="Quanto cambia la classifica da un anno all'altro",
                   nota="dentro la stessa categoria, fra primo e secondo anno")

        # --- continuita' oltre l'eta' giovanile ----------------------------
        ar.valore("a_punti_dopo_u23", conta(" AND punti_dopo_u23 = 1"),
                  nota="ancora a punti in una classifica dopo i 22 anni; e' un limite "
                       "inferiore, chi corre senza fare punti non compare")
        ar.valore("a_punti_dopo_u23_non_pro", conta(" AND punti_dopo_u23 = 1 AND PRO = 0"),
                  nota="continuano a correre a un livello che non e' il professionismo")

        # --- figure ---------------------------------------------------------
        if not os.environ.get("SENZA_FIGURE"):
            try:
                disegna(curva, righe_e, n_u15, eta, ar, lo, hi)
            except SystemExit as e:
                print("   figure saltate: %s" % e)

    print("Modulo 'attrito' eseguito.")
    for c, n, p in curva:
        print("   %-5s %5d atleti  (%.1f%% dei partenti U15)" % (c, n, p))


def disegna(curva, esiti, n_u15, eta, ar, lo, hi):
    # 1. l'imbuto
    with gr.figura("Su mille ragazzi classificati a tredici anni, "
                   "quanti si ritrovano dopo") as (fig, ax):
        etichette = [c for c, _, _ in curva] + [e[0] for e in esiti]
        valori = [p * 10 for _, _, p in curva] + [1000 * e[1] / n_u15 for e in esiti]
        colori = [gr.COLORI[0]] * len(curva) + [gr.COLORI[1]] * len(esiti)
        barre = ax.bar(range(len(valori)), valori, color=colori, zorder=3)
        for b, v in zip(barre, valori):
            ax.annotate("%d" % round(v) if v >= 1 else "%.1f" % v,
                        (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 4),
                        ha="center", fontsize=9)
        ax.set_xticks(range(len(etichette)))
        ax.set_xticklabels(etichette)
        ax.set_ylabel("su 1.000 partenti in Under 15")
        ax.set_yscale("log")
        fig.text(0.005, -0.03, "Coorti %d-%d. Scala logaritmica: senza, le ultime tre "
                 "barre sarebbero invisibili." % (lo, hi), fontsize=8, color=gr.GRIGIO)
    ar.figura("imbuto", gr.salva("attrito_imbuto"),
              didascalia="L'attrito non e' graduale: fra i mille classificati in Under 15 "
                         "e i %.0f che diventano professionisti ci sono tre ordini di "
                         "grandezza." % (1000 * esiti[0][1] / n_u15))

    # 2. l'eta' di uscita
    with gr.figura("Si smette alla fine di una categoria, non durante") as (fig, ax):
        x = sorted(e for e in eta if 13 <= e <= 26)
        y = [eta[e] for e in x]
        # l'ultimo anno di ogni categoria e' evidenziato: e' li' che si concentra l'uscita
        ultimi = {u for _, u in FASCE.values()}
        colori = [gr.COLORI[1] if e in ultimi else gr.COLORI[2] for e in x]
        ax.bar(x, y, color=colori, zorder=3)
        for cat, (primo, ultimo) in FASCE.items():
            if ultimo in x:
                ax.annotate(cat, (ultimo, eta[ultimo]), textcoords="offset points",
                            xytext=(0, 6), ha="center", fontsize=9, color=gr.COLORI[1])
        ax.set_xticks(x)
        ax.set_xlabel("eta' dell'ultima stagione a punti")
        ax.set_ylabel("atleti")
        fig.text(0.005, -0.03, "In rosso l'ultimo anno di ciascuna categoria, quando si e' "
                 "costretti a cambiare fascia.", fontsize=8, color=gr.GRIGIO)
    ar.figura("uscite", gr.salva("attrito_uscite"),
              didascalia="L'uscita si concentra nell'anno in cui la categoria finisce: "
                         "il passaggio di fascia e', piu' del rendimento, il momento in "
                         "cui si decide se continuare.")


def rendi(lt):
    v = lt.valori("attrito")
    imbuto = lt.tabella("attrito", "imbuto")
    esiti = lt.tabella("attrito", "esiti")
    uscite = lt.tabella("attrito", "uscite")

    p = [md.sezione("Quanti restano")]
    p.append(md.paragrafo(
        "Prima di chiedersi se il risultato a tredici anni predica qualcosa, conviene "
        "sapere quanti di quei ragazzi si ritrovano dopo. La risposta inquadra tutto il "
        "resto: **la maggior parte dell'abbandono avviene molto prima del punto in cui "
        "la prestazione diventa predittiva**.",
        "",
        "Su %s atleti delle coorti %s, %s sono arrivati al professionismo: **%s su mille** "
        "fra i classificati in Under 15."
        % (f"{v['atleti_totali']:,}".replace(",", "."), v["coorti"],
           v["pro_totali"], v["pro_su_mille_u15"])))

    p.append(md.metodo(
        "Come si legge l'imbuto",
        "«Presente in una categoria» significa aver ottenuto almeno un punto in almeno "
        "una delle sue stagioni. Le due colonne centrali rispondono a domande diverse: "
        "la prima conta chi era gia' in Under 15 ed e' arrivato fin li'; la seconda "
        "conta chi era nella categoria immediatamente precedente.\n\n"
        "Divergono perche' l'insieme non e' una catena di sottoinsiemi: si entra anche "
        "tardi. L'ultima colonna quantifica proprio questo.\n\n"
        "Nessuna delle tre e' un tasso di abbandono dello sport, per la ragione "
        "spiegata piu' avanti.",
        []))

    if imbuto:
        p.append(md.tabella(imbuto["colonne"], imbuto["righe"], colonne_conteggio={1}))
    p.append(md.paragrafo(
        "",
        "Le due colonne centrali dicono cose diverse, e la differenza conta. "
        "L'imbuto **non e' una catena di sottoinsiemi**: fra un quarto e un terzo degli "
        "atleti di ogni categoria non compare mai in Under 15. Sono ragazzi che entrano "
        "nel ranking piu' tardi, e che una lettura ingenua dell'imbuto conterebbe come "
        "\"sopravvissuti\" senza che siano mai partiti."))

    f = lt.figura("attrito", "imbuto")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.sezione("Quando si smette", 3))
    if uscite:
        p.append(md.tabella(uscite["colonne"], uscite["righe"],
                            colonne_conteggio={2, 3}, nota=uscite["nota"]))
    if v.get("quota_uscite_a_fine_categoria"):
        p.append(md.paragrafo(
            "",
            "Il **%s%%** di chi esce lo fa nell'ultimo anno della propria categoria. "
            "Non si smette perche' si va male a meta' percorso: si smette al passaggio "
            "di fascia, quando cambiano distanze, avversari e squadra. E' un fatto "
            "operativo, non statistico — indica *quando* un intervento di ritenzione "
            "avrebbe senso." % v["quota_uscite_a_fine_categoria"]))

    f = lt.figura("attrito", "uscite")
    if f:
        p.append(md.figura(f["percorso"], f["didascalia"]))

    p.append(md.sezione("Uscire dalla classifica non e' smettere", 3))
    ricambio = lt.tabella("attrito", "ricambio")
    p.append(md.paragrafo(
        "Le tabelle qui sopra vanno lette con una cautela che non e' una postilla: "
        "**sparire dalla classifica significa smettere di fare punti, non smettere di "
        "correre**. Un ragazzo che passa di categoria si trova contro avversari di un "
        "anno o due piu' grandi, e puo' benissimo continuare a correre senza piu' "
        "entrare a punti. Nella classifica quello e' indistinguibile da chi ha appeso "
        "la bici al chiodo.",
        "",
        "Non e' una possibilita' teorica: si misura. Il **%s%%** degli atleti salta "
        "almeno una stagione e poi **ricompare**, e il %s%% torna dopo un'assenza di due "
        "stagioni o piu'. Se l'assenza fosse abbandono, non ci sarebbero rientri."
        % (v.get("rientri_dopo_assenza"), v.get("rientri_dopo_assenza_lunga"))))

    p.append(md.metodo(
        "Le due misure del ricambio",
        "La prima conta gli atleti la cui sequenza di stagioni ha un buco: presenti, "
        "assenti per una o piu' stagioni, presenti di nuovo. Un rientro dimostra che "
        "l'assenza non era un abbandono.\n\n"
        "La seconda confronta due liste consecutive della stessa categoria e conta "
        "quanti nomi sono nuovi. Misura il rinnovo della composizione senza dipendere "
        "dalle carriere individuali.\n\n"
        "Sono indipendenti fra loro e portano alla stessa conclusione, che e' il motivo "
        "per cui vengono riportate entrambe.",
        []))

    if ricambio:
        p.append(md.tabella(ricambio["colonne"], ricambio["righe"],
                            colonne_conteggio={1, 2}, nota=ricambio["nota"]))
    p.append(md.paragrafo(
        "",
        "Il ricambio e' cosi' forte che **meta' dei classificati al secondo anno di "
        "Allievi non c'era al primo**, e non hanno cambiato categoria: e' la stessa "
        "fascia, un anno dopo. Quello che l'imbuto misura, quindi, non e' quanti "
        "ragazzi lasciano il ciclismo, ma **quanto e' mobile l'insieme di chi va a "
        "punti** — che e' una cosa diversa, e per certi versi piu' interessante: dice "
        "che essere fuori dalla classifica a sedici anni non e' una condanna."))

    p.append(md.sezione("Chi arriva in fondo", 3))
    if esiti:
        p.append(md.tabella(esiti["colonne"], esiti["righe"],
                            colonne_conteggio={1, 3}, decimali=2))
    p.append(md.paragrafo(
        "",
        "Dei %s professionisti, %s erano gia' nel ranking Under 15: gli altri sono entrati "
        "piu' tardi. E accanto a loro ci sono **%s atleti che risultavano ancora a punti "
        "dopo i ventidue anni senza essere diventati professionisti**: non tutto cio' che "
        "non e' professionismo e' abbandono."
        % (v["pro_totali"], v["pro_dall_u15"], v.get("a_punti_dopo_u23_non_pro", "—")),
        "",
        "> **Cosa misura questa sezione.** «Presente» significa «ha ottenuto almeno un "
        "punto». L'attrito che si vede qui e' l'uscita dalla classifica, non l'abbandono "
        "dello sport, e i due numeri non coincidono: ne' l'elenco dei tesserati ne' il "
        "numero di gare disputate sono pubblicati, quindi la differenza non e' "
        "quantificabile in modo diretto."))
    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
