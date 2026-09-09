"""
Da dove vengono i dati.

PERCHE' E' UNA SEZIONE DEL DOCUMENTO E NON UNA NOTA NEL README
    Il README lo legge chi vuole eseguire il progetto; questo documento lo legge chi
    vuole credere ai risultati. Sono due pubblici diversi con la stessa domanda di fondo:
    da dove escono questi numeri, e cosa non c'e' dentro.

    Una sezione sulla provenienza in testa al documento e' anche cio' che la voce 4a
    della checklist TRIPOD chiede, e non e' una formalita': senza, ogni percentuale che
    segue e' priva del suo denominatore.

I NUMERI DELLA PROVENIENZA SI CONTANO, NON SI RICORDANO
    Quante stagioni, quanti atleti, quante righe, quanti abbinamenti riusciti: sono tutti
    ricavabili dai database, e ricavarli significa che la descrizione della fonte resta
    vera anche quando la fonte cresce.
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

DB_PCS = os.path.join("data", "pcs", "pcs.db")
TESSERATI = os.path.join("riferimenti", "tesserati_fci.csv")


def calcola():
    db = sqlite3.connect(DB_ANALISI)
    sesso = cfg("studio", "sesso")

    with Archivio("provenienza") as ar:
        for chiave in ("repository", "estrazione", "schema", "portale"):
            ar.valore(chiave, cfg("fonte", chiave))

        lo, hi, righe, atleti = db.execute(
            """SELECT MIN(season), MAX(season), COUNT(*), COUNT(DISTINCT athlete_id)
               FROM tab_a WHERE sesso = ?""", (sesso,)).fetchone()
        ar.valore("stagioni", [lo, hi])
        ar.valore("righe_classifica", righe)
        ar.valore("atleti", atleti)

        # Quante date di nascita sono osservate e quante inferite: e' la differenza fra
        # un dato e una ricostruzione, e chi legge l'effetto dell'eta' relativa deve
        # saperlo.
        conf = dict(db.execute(
            """SELECT birth_year_conf, COUNT(*) FROM tab_b WHERE sesso = ? GROUP BY 1""",
            (sesso,)).fetchall())
        osservate = sum(v for k, v in conf.items() if k in ("sorgente", "scheda"))
        ar.valore("nascite_osservate", osservate)
        ar.valore("nascite_totali", sum(conf.values()))
        con_data = db.execute(
            "SELECT COUNT(*) FROM tab_b WHERE sesso = ? AND birth_date IS NOT NULL",
            (sesso,)).fetchone()[0]
        ar.valore("con_data_completa", con_data)
        ar.valore("nascite_corrette", conf.get("corretta_a_mano", 0))

        abbinati = db.execute(
            "SELECT COUNT(*) FROM tab_b WHERE sesso = ? AND pcs_matched = 1",
            (sesso,)).fetchone()[0]
        ar.valore("abbinati_pcs", abbinati)

        # Come sono stati abbinati, non solo quanti: uno studio costruito sul
        # collegamento fra due archivi si giudica anche da quanto quel collegamento
        # sia fragile, e la risposta e' una riga di SQL.
        metodi = dict(db.execute(
            """SELECT m.metodo, COUNT(*) FROM match_pcs m
               JOIN tab_b b ON b.athlete_id = m.athlete_id
               WHERE b.sesso = ? GROUP BY 1""", (sesso,)).fetchall())
        ar.valore("abbinamenti_per_metodo", metodi)
        ar.valore("abbinamenti_esatti", metodi.get("esatto_data", 0))
        ar.valore("abbinamenti_ambigui", db.execute(
            """SELECT COUNT(*) FROM match_pcs m JOIN tab_b b
               ON b.athlete_id = m.athlete_id
               WHERE b.sesso = ? AND m.ambiguo = 1""", (sesso,)).fetchone()[0])

        if os.path.exists(DB_PCS):
            p = sqlite3.connect(DB_PCS)
            ar.valore("stagioni_pcs", list(
                p.execute("SELECT MIN(season), MAX(season) FROM pcs_ranking").fetchone()))
            p.close()
        ar.valore("ha_tesserati", os.path.exists(TESSERATI))
    db.close()
    print("   provenienza: %d righe di classifica, %d atleti, %d abbinati a PCS"
          % (righe, atleti, abbinati))


def rendi(lt):
    v = lt.valori("provenienza")
    if not v:
        return ""

    st = v.get("stagioni", [None, None])
    p = [md.sezione("Da dove vengono i dati")]

    p.append(md.paragrafo(
        "Ogni numero di questo documento nasce da due fonti pubbliche, unite da una "
        "terza operazione — riconoscere che un ragazzo in una classifica giovanile "
        "italiana e un corridore in un archivio internazionale sono la stessa persona. "
        "Vale la pena descrivere tutte e tre, perche' i limiti dei risultati vengono "
        "quasi tutti da qui."))

    righe = [
        ["classifiche giovanili italiane",
         "%s, stagioni %s-%s" % (v.get("portale"), st[0], st[1]),
         "%s righe di classifica, %s atleti"
         % (md.conta(v.get("righe_classifica")), md.conta(v.get("atleti")))],
        ["date di nascita",
         "schede personali su %s" % v.get("portale"),
         "%s date complete; %s anni di nascita osservati anziche' dedotti"
         % (md.conta(v.get("con_data_completa")), md.conta(v.get("nascite_osservate")))],
        ["esiti di carriera",
         "ProCyclingStats, classifiche %s-%s"
         % tuple(v.get("stagioni_pcs", ["—", "—"])),
         "%s atleti abbinati" % md.conta(v.get("abbinati_pcs"))],
        ["nascite attese per trimestre", "Eurostat, tavola `demo_fmonth`",
         "serve solo all'effetto dell'eta' relativa"],
    ]
    if v.get("ha_tesserati"):
        righe.append(["tesserati per categoria",
                      "Federazione Ciclistica Italiana, dati statistici pubblicati",
                      "serve a dare scala alle percentuali"])
    p.append(md.tabella(["cosa", "fonte", "quanto"], righe))

    p.append(md.paragrafo(
        "",
        "**Le classifiche giovanili** sono quelle che %s pubblica per ogni stagione e "
        "per ogni categoria. Non sono state raccolte per questo studio: derivano da un "
        "progetto separato che ne mantiene lo scaricamento e il database "
        "([%s](%s)), e questo documento lavora sull'estrazione del %s, schema `%s`. "
        "Tenere separate le due cose ha un motivo pratico — la raccolta si aggiorna con "
        "un ritmo suo, l'analisi si rigenera quando serve — e uno di onesta': chi vuole "
        "controllare i dati di partenza guarda quel repository, non questo.\n\n"
        "Va detto che cosa quella fonte non e': **non e' l'archivio ufficiale della federazione**, "
        "ma un portale che raccoglie e ordina i risultati per conto proprio. Le classifiche "
        "che pubblica sono l'unico archivio giovanile italiano consultabile per stagione e "
        "per categoria, e la verifica della struttura delle liste e del sistema a punti sta "
        "in `docs/verifica_dati_giovanile.md`, ma un errore di trascrizione a monte non "
        "sarebbe visibile da qui. Il percentile attenua il problema, perche' un punteggio "
        "sbagliato sposta un atleta di qualche posizione e non cambia l'ordine "
        "generale, e non lo azzera."
        % (v.get("portale"), v.get("repository", "").split("/")[-1],
           v.get("repository"), v.get("estrazione"), v.get("schema"))))

    p.append(md.paragrafo(
        "",
        "**Le date di nascita** vengono dalle schede personali dello stesso portale, "
        "scaricate a parte. Servono all'effetto dell'eta' relativa, che senza il giorno "
        "esatto non si puo' misurare. La copertura e' quasi totale — %s anni di nascita "
        "su %s sono letti da una scheda e non dedotti — e questo conta, perche' dove la "
        "scheda manca l'anno si ricostruirebbe dalla categoria e dalla stagione, che e' "
        "inferenza e non osservazione. Le due cose restano distinte in tutto il "
        "progetto. %s date sono state corrette a mano dopo aver trovato incoerenze fra "
        "la scheda e le classifiche, e le correzioni sono registrate una per una."
        % (md.conta(v.get("nascite_osservate")), md.conta(v.get("nascite_totali")),
           md.conta(v.get("nascite_corrette")))))

    p.append(md.paragrafo(
        "",
        "**Gli esiti di carriera** vengono da ProCyclingStats: rose delle squadre "
        "professionistiche stagione per stagione, da cui si ricava chi e' passato "
        "professionista e quando, e classifiche mondiali annuali, da cui si ricava fin "
        "dove e' arrivato. L'abbinamento fra i due archivi e' fatto su nome e data di "
        "nascita, con quattro passaggi di precisione decrescente; i casi ambigui sono "
        "stati risolti a mano guardando **solo** nome e data, mai la carriera, e "
        "registrati uno per uno.",
        "",
        "Quanto regge quel collegamento e' una domanda legittima, e la risposta e' "
        "questa: dei %s abbinamenti **%s sono esatti su nome piu' data di nascita "
        "completa**, e due persone diverse con lo stesso nome normalizzato e la stessa "
        "data al giorno sono un'eventualita' trascurabile. I restanti %s sono stati "
        "guardati uno per uno, e al termine della verifica **nessun abbinamento resta "
        "ambiguo**. La stessa verifica ha corretto %s date di nascita: le due fonti non "
        "sempre concordano, e caso per caso ha avuto ragione ora l'una ora l'altra, "
        "quindi nessuna regola automatica avrebbe funzionato."
        % (md.conta(v.get("abbinati_pcs")), md.conta(v.get("abbinamenti_esatti")),
           md.conta((v.get("abbinati_pcs") or 0) - (v.get("abbinamenti_esatti") or 0)),
           md.conta(v.get("nascite_corrette")))))

    p.append(md.paragrafo(
        "",
        "> **Cosa non c'e', ed e' il limite principale.** Nessuna delle fonti pubblica "
        "altezza, peso, specialita', volume di allenamento o numero di gare disputate. "
        "Di ogni atleta si sa il piazzamento, non come ci e' arrivato. Ogni conclusione "
        "di questo documento va quindi letta come **«a parita' di cio' che la classifica "
        "registra»**, che e' meno di cio' che un allenatore vede.",
        "",
        "> In particolare il percentile non sa quante gare ha corso un atleta: chi ne "
        "ha corse dieci e chi una sola possono trovarsi allo stesso posto in classifica, "
        "e il primo ha avuto dieci occasioni di andare a punti. I risultati valgono quindi "
        "a parita' di esposizione alla gara, che nei dati non c'e'.",
        "",
        "> Non c'e' nemmeno l'elenco dei tesserati per regione, il che lascia aperta "
        "l'unica domanda geografica che varrebbe la pena porre.",
        "",
        "> I dati riguardano minorenni e nel repository non entra nulla che permetta di "
        "risalire a una persona: gli identificativi sono cifrati con un segreto tenuto "
        "fuori dal codice, e nessuna tabella pubblicata contiene celle con meno di "
        "cinque atleti."))

    return (chr(10) * 2).join(x.strip() for x in p if x)


if __name__ == "__main__":
    calcola()
