"""
Controlla che i numeri citati nei documenti scritti a mano siano ancora quelli
dell'analisi.

PERCHE' ESISTE
    Tutto il resto del progetto ha una regola: nessun numero si scrive a mano, perche' i
    numeri cambiano quando i dati cambiano e un testo fisso diventa falso in silenzio.

    Alcuni documenti violano quella regola, e non per distrazione. `docs/tripod.md` e'
    prosa di controllo, `docs/piano_post.md` e' un piano editoriale, e le bozze in
    `docs/post/` sono testo che deve suonare come italiano e non come una query:
    rigenerarli a ogni esecuzione non avrebbe senso. Contengono pero' decine di cifre
    copiate dall'analisi — quanti professionisti, quanti eventi, quale percentuale
    intercettata — che l'anno prossimo saranno altre.

    I post sono il caso piu' serio, perche' sono gli unici destinati a uscire di casa.

    Questo script e' il compromesso: i documenti restano scritti a mano, ma le loro cifre
    vengono confrontate con l'archivio dei risultati. Se divergono lo dice, invece di
    lasciare in giro testi che descrivono un'analisi che non esiste piu'.

COSA NON FA
    Non verifica le affermazioni qualitative, che sono la parte importante di quei
    documenti e vanno riviste da una persona. Verifica solo le cifre, che sono la parte
    che si guasta da sola.

    Non controlla `docs/literature_review.md`: quella non cita cifre dell'analisi, quindi
    non si guasta quando i dati cambiano. Invecchia con la letteratura, che e' un altro
    tipo di manutenzione e ha il suo avviso in testa al file.

USO
    python scripts/11_verifica_documenti.py
"""
import json
import os
import re
import sqlite3
import sys

TRIPOD = os.path.join("docs", "tripod.md")
PIANO = os.path.join("docs", "piano_post.md")
POST = os.path.join("docs", "post")
RISULTATI = os.path.join("output", "risultati.db")
ANALISI = os.path.join("output", "analisi.md")

# Il documento generato usa lo spazio stretto insecabile per le migliaia.
SPAZI = (" ", " ", " ")


def valore(db, modulo, chiave):
    r = db.execute("SELECT valore FROM valore WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def tabella(db, modulo, chiave):
    r = db.execute("SELECT righe FROM tabella WHERE modulo=? AND chiave=?",
                   (modulo, chiave)).fetchone()
    return json.loads(r[0]) if r else None


def _numero(testo):
    """Da «2 817» o «30,6» al numero. Restituisce None se non e' un numero."""
    if testo is None:
        return None
    ripulito = testo
    for s in SPAZI:
        ripulito = ripulito.replace(s, "")
    try:
        return float(ripulito.replace(",", "."))
    except ValueError:
        return None


def attesi_tripod(db):
    """Le cifre che la checklist cita, ricavate dall'archivio.

    Ogni voce e' (descrizione, valore atteso, espressione che lo cerca nel testo). Il
    primo gruppo non vuoto dell'espressione deve catturare il numero.
    """
    livelli = tabella(db, "qualita", "livelli") or []
    top100 = next((r[1] for r in livelli if "top 100" in str(r[0])), None)
    temporale = tabella(db, "validazione", "temporale") or []
    chiave = valore(db, "metriche", "frase_chiave") or {}

    sezioni = None
    if os.path.exists(ANALISI):
        with open(ANALISI, encoding="utf-8") as f:
            # L'indice e' una sezione del documento ma non una sezione di analisi.
            sezioni = len(re.findall(r"^## ", f.read(), re.M)) - 1

    return [
        ("professionisti nelle coorti principali",
         valore(db, "attrito", "pro_totali"),
         r"(\d+) professionisti sulle coorti principali"),
        ("eventi nel modello di sopravvivenza",
         valore(db, "sopravvivenza", "n_eventi"),
         r"(\d+) nel modello di sopravvivenza"),
        ("atleti nel livello top 100", top100,
         r"(\d+) nel livello top 100"),
        ("ripetizioni del bootstrap",
         valore(db, "validazione", "ripetizioni"),
         r"\((\d+) ricampionamenti\)"),
        ("eventi nelle coorti di verifica",
         temporale[0][4] if temporale else None,
         r"riserva dei (\d+) eventi"),
        ("futuri professionisti intercettati",
         round(chiave["sensibilita"]) if chiave.get("sensibilita") else None,
         r"il (\d+)% dei futuri professionisti"),
        ("selezionati che non arrivano",
         round(100 - chiave["vpp"]) if chiave.get("vpp") else None,
         r"il (\d+)% dei selezionati che non ce la far"),
        ("sezioni del documento", sezioni,
         r"documento a (\d+) sezioni"),
    ]


def attesi_piano(db):
    """Le cifre che il piano editoriale cita, ricavate dall'archivio."""
    curva = valore(db, "attrito", "curva") or []
    chiave = valore(db, "metriche", "frase_chiave") or {}
    tra = valore(db, "traiettorie", "auc") or {}
    uni_max = valore(db, "univariati", "auc_massima") or {}
    ann = valore(db, "annidati", "salto_maggiore") or {}
    return [
        ("classificati in Under 15", curva[0][1] if curva else None,
         r"da ([\d  ]+) classificati in Under 15"),
        ("professionisti venuti dall'Under 15",
         valore(db, "attrito", "pro_dall_u15"),
         r"classificati in Under 15 a (\d+)\s"),
        ("professionisti nelle coorti", valore(db, "attrito", "pro_totali"),
         r"i (\d+) professionisti sui 2 817"),
        ("rientri dopo un'assenza",
         valore(db, "attrito", "rientri_dopo_assenza"),
         r"(\d+,\d)% degli atleti salta almeno una stagione"),
        ("resta in classifica al cambio di categoria",
         valore(db, "passaggi", "resta_fra"),
         r"resta in classifica il (\d+)% contro"),
        ("quota della lista di arrivo che c'era gia'",
         valore(db, "passaggi", "quota_fra"),
         r"composta per l'(\d+)% da persone"),
        ("cambio di societa' fra Juniores e Under 23",
         valore(db, "contesto", "cambio_juniores_u23"),
         r"il (\d+,\d)% cambia societ"),
        ("futuri professionisti intercettati",
         round(chiave["sensibilita"]) if chiave.get("sensibilita") else None,
         r"si intercetta il (\d+)% dei futuri"),
        ("selezionati che non arrivano",
         round(100 - chiave["vpp"]) if chiave.get("vpp") else None,
         r"il (\d+)% dei selezionati non lo diventer"),
        ("odds ratio piu' alto", uni_max.get("or"),
         r"per (\d,\d\d) in Under 19"),
        ("AUC con livello e pendenza", tra.get("completo"),
         r"da 0,848 a (\d,\d+)"),
        ("salto maggiore nei modelli annidati", ann.get("delta"),
         r"\(ΔAUC \+(\d,\d+)\)"),
    ]


def attesi_post(db):
    """Le cifre che le bozze dei blog post citano, ricavate dall'archivio.

    I post sono la parte piu' esposta del progetto: sono scritti a mano, sono destinati a
    uscire di casa, e contengono piu' cifre copiate di tripod.md e piano_post.md messi
    insieme. Se l'analisi viene rigenerata su dati nuovi, un post pubblicato resta com'e' —
    quindi le sue cifre vanno controllate qui prima, non scoperte sbagliate dopo.

    Non si controlla ogni numero citato: si controllano quelli su cui poggia
    un'affermazione. Se cambia uno di questi, non basta correggere la cifra — va riletto
    il paragrafo che ci sta intorno, perche' probabilmente cambia anche cosa se ne puo'
    dire.

    Le percentuali derivate da un'AUC (per esempio «mette davanti quello giusto nel 74%
    dei casi») sono confrontate con l'AUC moltiplicata per cento: e' la stessa quantita'
    detta in italiano.
    """
    def v(modulo, chiave, *strada):
        x = valore(db, modulo, chiave)
        for passo in strada:
            if x is None:
                return None
            x = x[passo]
        return x

    def riga(modulo, chiave, testo, colonna):
        """Il valore in una colonna della riga la cui prima cella contiene `testo`."""
        for r in tabella(db, modulo, chiave) or []:
            if testo in str(r[0]):
                return r[colonna]
        return None

    def pct(x):
        return None if x is None else x * 100

    hazard = tabella(db, "sopravvivenza", "hazard_grezzo") or []
    eta_max = max(hazard, key=lambda r: r[3])[0] if hazard else None
    mob = v("contesto", "mobilita_grezza_da_a") or [None, None]
    grezzo = None if None in mob[:2] else mob[1] - mob[0]
    chiave = v("metriche", "frase_chiave") or {}

    return {
        "02_di_chi_parliamo.md": [
            ("professionisti venuti dall'Under 15",
             v("attrito", "pro_dall_u15"), r"ma solo (\d+) erano in classifica"),
            ("professionisti mai visti in Under 15",
             v("attrito", "pro_mai_in_u15"), r"gli altri (\d+) sono entrati"),
            ("persi fra Under 15 e Under 23",
             v("attrito", "persi_fra_u15_e_u23"), r"e sono circa (\d \d+)"),

            ("righe di classifica", v("provenienza", "righe_classifica"),
             r"le (\d[\d ]*\d) righe della"),
            ("copertura minima", v("copertura", "copertura_min"),
             r"fra il (\d+,\d)% e il 17,2%"),
            ("copertura massima", v("copertura", "copertura_max"),
             r"fra il 12,2% e il (\d+,\d)%"),
            ("classificati in Under 15", v("attrito", "curva", 0, 1),
             r"\| Under 15 \| (\d[\d ]*\d) \| 100%"),
            ("atleti nelle coorti", v("attrito", "atleti_totali"),
             r"(\d[\d ]*\d) ragazzi, 77 professionisti"),
            ("professionisti", v("attrito", "pro_totali"),
             r"2 817 ragazzi, (\d+) professionisti"),
            ("punti per piazzamento, U15",
             v("misura", "rapporto_estremi", "valore_basso"),
             r"\| Under 15 \| (\d,\d\d) \|"),
            ("punti per piazzamento, U23",
             v("misura", "rapporto_estremi", "valore_alto"),
             r"\| Under 23 \| (\d,\d\d) \|"),
            ("pari merito massimi", v("misura", "pari_merito_massimo"),
             r"fino al (\d+)% dei classificati"),
            ("errore dell'estrapolazione", v("copertura", "backtest_errore"),
             r"sbaglia fino al (\d+)%"),
            ("quota dei posti al primo anno di Allievi",
             v("posti", "quota_primo_anno_U17"),
             r"il primo anno ne vince il (\d+,\d)%"),
            ("quota dei posti al primo anno di Esordienti",
             v("posti", "quota_primo_anno_U15"),
             r"contro il (\d+,\d)% degli Esordienti"),
            ("concentrazione minima", v("posti", "decile_minimo"),
             r"fra il (\d+,\d)% e il 43,2% dei punti"),
            ("concentrazione massima", v("posti", "decile_massimo"),
             r"fra il 36,7% e il (\d+,\d)% dei punti"),
        ],
        "03_sparire_non_e_smettere.md": [
            ("stagioni medie dei professionisti",
             v("attrito", "stagioni_medie_pro"),
             r"in classifica per (\d,\d) stagioni in media"),
            ("stagioni medie degli altri",
             v("attrito", "stagioni_medie_altri"),
             r"contro le (\d,\d) di tutti gli altri"),
            ("scarto tipo del percentile, professionisti",
             v("attrito", "sd_percentile_pro"),
             r"vale (\d+,\d) posizioni"),
            ("scarto tipo del percentile, gli altri",
             v("attrito", "sd_percentile_altri"), r"e (\d+,\d) per tutti gli altri"),

            ("rientri dopo un'assenza", v("attrito", "rientri_dopo_assenza"),
             r"Il (\d+,\d)% degli atleti salta almeno una stagione"),
            ("rientri dopo due stagioni", v("attrito", "rientri_dopo_assenza_lunga"),
             r"Il (\d,\d)% torna dopo"),
            ("facce nuove in U17y2", riga("attrito", "ricambio", "U17y2", 3),
             r"\| Under 17, secondo anno \| 1 602 \| (\d+,\d)% \|"),
            ("resta, dentro la categoria", v("passaggi", "resta_dentro"),
             r"\| dentro la categoria \| (\d+,\d)% \|"),
            ("resta, cambiando categoria", v("passaggi", "resta_fra"),
             r"\| cambiando categoria \| (\d+,\d)% \|"),
            ("la lista di arrivo che c'era gia'", v("passaggi", "quota_fra"),
             r"composta per l'(\d+,\d)% da"),
            ("correlazione dentro la categoria", v("passaggi", "rho_dentro"),
             r"vale (\d,\d+) dentro la categoria"),
            ("correlazione al cambio di fascia", v("passaggi", "rho_fra"),
             r"e (\d,\d+) al cambio di fascia"),
            ("uscite nell'ultimo anno di categoria",
             v("attrito", "quota_uscite_a_fine_categoria"),
             r"il (\d+,\d)% di chi esce"),
            ("tesserati residui in Under 23", v("copertura", "residuo_tesserati"),
             r"il (\d+,\d)% dei tesserati"),
            ("ancora a punti dopo i 22 senza professionismo",
             v("attrito", "a_punti_dopo_u23_non_pro"),
             r"(\d+) atleti che risultavano ancora a punti"),
            ("quota dei posti, Esordienti primo anno",
             v("posti", "quota_primo_anno_U15"),
             r"Esordienti, classifiche separate \| (\d+,\d)%"),
            ("quota dei posti, Allievi primo anno",
             v("posti", "quota_primo_anno_U17"),
             r"Allievi, classifica unica \| (\d+,\d)%"),
            ("gare per stagione in Esordienti",
             v("posti", "gare_per_stagione", "U15"),
             r"circa (\d+) classificazioni di gara"),
            ("gare per stagione in Under 23",
             v("posti", "gare_per_stagione", "U23"),
             r"si scende a (\d+) in Under 23"),
            # nell'archivio il calo e' negativo, nel testo e' detto come una perdita
            ("calo del calendario in Under 23", abs(v("posti", "calo_massimo") or 0),
             r"e del (\d+)% in Under 23"),
        ],
        "04_a_tredici_anni.md": [
            ("quanto separa a tredici anni", pct(v("univariati", "auc_prima", "auc")),
             r"nel (\d+)% dei casi"),
            ("quanto separa a diciotto anni", pct(v("univariati", "auc_massima", "auc")),
             r"a diciotto nell'(\d+)%"),
            ("odds ratio a tredici anni", v("univariati", "auc_prima", "or"),
             r"\| Under 15, primo anno \| 13 \| ×(\d,\d\d) \|"),
            ("odds ratio a diciotto anni", v("univariati", "auc_massima", "or"),
             r"Under 19, secondo anno \| 18 \| ×(\d,\d\d)"),
            ("secondo anno di Under 15",
             pct(riga("univariati", "primo_contro_secondo", "U15", 4)),
             r"\| Under 15 \| 70% \| (\d+)% \|"),
            ("modello con la sola coorte", pct(v("annidati", "auc_base")),
             r"\| solo l'anno di nascita \| (\d+)%"),
            ("modello con tutte le categorie", pct(v("annidati", "auc_finale")),
             r"più l'Under 23 \| (\d+)%"),
            ("atleti nella sequenza annidata", v("annidati", "n"),
             r"sono (\d+), un gruppo piccolo"),
            ("guadagno della foresta casuale", pct(v("confronto_ml", "differenza")),
             r"guadagnato (\d,\d) punti percentuali"),
            ("coefficienti trattenuti dall'elastic net",
             v("penalizzato", "trattenuti"), r"ne ha tenute (\d) su 8"),
            ("lunghezza della lista U17y1",
             riga("univariati", "ampiezza_liste", "U17y1", 1),
             r"sono (\d+) contro 320 in Under 17"),
            ("separazione a tredici anni con gli assenti",
             pct(riga("sensibilita", "mancanti", "Under 15 primo anno, tutta", 4)),
             r"dal 74% al (\d+)%"),
            ("separazione a diciotto anni con gli assenti",
             pct(riga("sensibilita", "mancanti", "Under 19 secondo anno, tutta", 4)),
             r"dall'89% al (\d+)%"),
            ("professionisti in classifica a tredici anni",
             riga("sensibilita", "mancanti", "Under 15 primo anno, solo", 1),
             r"(\d+) dei 77 futuri professionisti"),
        ],
        "05_livello_o_curva.md": [
            ("odds ratio del livello",
             riga("traiettorie", "coefficienti", "livello", 1),
             r"di livello in più \| ×(\d,\d\d)"),
            ("odds ratio della pendenza",
             riga("traiettorie", "coefficienti", "pendenza", 1),
             r"di miglioramento annuo \| ×(\d,\d\d)"),
            ("previsione con il solo livello", pct(v("traiettorie", "auc", "livello")),
             r"in circa (\d+) casi su 100"),
            ("previsione con anche la pendenza",
             pct(v("traiettorie", "auc", "completo")),
             r"si sale a (\d+)"),
            ("livello alto e in crescita", incrocio(db, "alto", "alto"),
             r"nel (\d+,\d)% dei casi"),
            ("livello alto e in calo", incrocio(db, "alto", "basso"),
             r"fermato al (\d,\d)%"),
            ("livello medio e in crescita", incrocio(db, "medio", "alto"),
             r"che sta al (\d,\d)%"),
            ("pendenza, controllata per la durata",
             v("traiettorie", "controllo_durata", "con"),
             r"da 3,35 a (\d,\d\d)"),
            ("atleti con almeno due stagioni", v("traiettorie", "n_atleti"),
             r"(\d[\d ]*\d) ragazzi, fra cui 74 professionisti"),
            ("atleti con una sola stagione",
             riga("traiettorie", "stagioni", "1", 1),
             r"(\d+) dei 2 747 atleti"),
        ],
        "06_predire_non_e_selezionare.md": [
            ("futuri professionisti intercettati",
             chiave.get("sensibilita"), r"intercettati \| (\d+)%"),
            ("selezionati che non arrivano",
             None if not chiave else 100 - chiave["vpp"],
             r"non lo diventeranno \| (\d+)%"),
            ("intercettati a tredici anni",
             riga_soglia(db, "U15y1", "migliore 10%", 6),
             r"intercetti il (\d+)% dei futuri"),
            ("selezionati a tredici anni che arrivano",
             riga_soglia(db, "U15y1", "migliore 10%", 8),
             r"ne arriverà l'(\d+)%"),
            ("selezionati in Under 23 che arrivano",
             riga_soglia(db, "U23y1", "migliore 10%", 8),
             r"arriva il (\d+)% dei selezionati"),
            ("probabilita' al 90° percentile",
             riga("qualita", "composte", "90", 1),
             r"\| 90° percentile \| (\d+,\d)%"),
            ("probabilita' di top 500 al 90° percentile",
             riga("qualita", "composte", "90", 2),
             r"30,0% \| (\d+,\d)%"),
            ("odds ratio per diventare professionista",
             riga("qualita", "stadi", "diventare professionista", 3),
             r"diventare professionista \| ×(\d,\d\d)"),
            ("odds ratio per il top 500 fra i professionisti",
             riga("qualita", "stadi", "top 500, fra i professionisti", 3),
             r"fra i professionisti \| ×(\d,\d\d)"),
            ("probabilita' cumulata, rendimento medio",
             v("sopravvivenza", "cumulate", "medio"),
             r"(\d+,\d)% di probabilità di arrivare"),
            ("stagioni a rischio senza classifica",
             v("sopravvivenza", "quota_assenti"),
             r"nell'(\d+,\d)% delle"),
            ("eta' di rischio massimo", eta_max,
             r"il massimo cade a (\d+) anni"),
        ],
        "07_falsi_indizi.md": [
            ("rapporto Q1/Q4 in Under 15", v("rae", "q1_su_q4_max"),
             r"(\d,\d\d) volte quelli nati"),
            ("rapporto Q1/Q4 in Under 23", v("rae", "q1_su_q4_min"),
             r"il rapporto scende a (\d,\d\d)"),
            ("rapporto Q1/Q4 fra i professionisti",
             riga("rae", "successo", "professionisti", 6),
             r"primo e ultimo trimestre è (\d,\d)"),
            ("professionisti senza cambi di società", mob[0],
             r"\| nessuno \| (\d,\d\d)% \|"),
            ("professionisti con tre cambi", mob[1],
             r"\| tre \| (\d,\d\d)% \|"),
            ("stagioni di chi non ha mai cambiato",
             v("contesto", "stagioni_da_a", 0), r"(\d,\d) stagioni"),
            ("divario grezzo della mobilità", grezzo,
             r"dei (\d,\d\d) punti percentuali di divario grezzo"),
            ("divario residuo a parità di carriera",
             v("contesto", "gradiente_residuo"), r"resta al massimo (\d,\d\d)"),
            ("cambio di società fra Juniores e Under 23",
             v("contesto", "cambio_juniores_u23"),
             r"nel (\d+,\d)% dei casi"),
            ("società di partenza, tasso minimo",
             v("contesto", "qualita_da_a", 0), r"dal (\d,\d\d)% di professionisti"),
            ("società di partenza, tasso massimo",
             v("contesto", "qualita_da_a", 1), r"al (\d,\d\d)% fra chi comincia"),
            ("quota che parte da società senza professionisti",
             v("contesto", "quota_societa_senza_pro"),
             r"il (\d+)% dei ragazzi part"),
            ("quota delle prime tre regioni", v("contesto", "quota_prime_tre"),
             r"circa il (\d+)% dei ragazzi in classifica"),
            ("atleti nelle coorti allargate", v("contesto", "atleti_regioni"),
             r"annate e (\d[\d ]*\d) atleti"),
            ("effetto dell'eta' relativa, maschi in Esordienti",
             v("rae", "sessi_prima_categoria", "maschi"),
             r"\| Esordienti \| (\d,\d\d) \|"),
            ("effetto dell'eta' relativa, femmine in Esordienti",
             v("rae", "sessi_prima_categoria", "femmine"),
             r"\| Esordienti \| 1,98 \| (\d,\d\d) \|"),
            ("atlete in Esordienti",
             v("rae", "sessi_prima_categoria", "n_femmine"),
             r"anni, sono (\d+) contro"),
        ],
        "08_le_ragazze.md": [
            ("quota dei posti prima della separazione",
             v("ragazze", "separazione_quote", "prima"),
             r"le annate convivono \| 2011-2021 \| (\d+,\d)%"),
            ("quota dei posti dopo la separazione",
             v("ragazze", "separazione_quote", "dopo"),
             r"ognuna la sua \| 2022-2025 \| (\d+,\d)%"),
            ("atlete in Esordienti", riga("ragazze", "dimensione", "Esordienti", 1),
             r"\| Esordienti \| (\d[\d ]*\d) \| 6 360"),
            ("quante volte meno gare in Esordienti",
             riga("ragazze", "dimensione", "Esordienti", 6),
             r"640 \| (\d,\d)×"),
            ("effetto dell'eta' relativa, maschi in Esordienti",
             v("rae", "sessi_prima_categoria", "maschi"),
             r"\| Esordienti \| (\d,\d\d) \|"),
            ("effetto dell'eta' relativa, femmine in Esordienti",
             v("rae", "sessi_prima_categoria", "femmine"),
             r"\| Esordienti \| 1,98 \| (\d,\d\d) \|"),
        ],
        "09_cosa_faremmo.md": [
            ("separazione a diciotto anni con gli assenti, nel post 9",
             pct(riga("sensibilita", "mancanti", "Under 19 secondo anno, tutta", 4)),
             r"dall'89% al (\d+)%"),
            ("separazione a tredici anni con gli assenti, nel post 9",
             pct(riga("sensibilita", "mancanti", "Under 15 primo anno, tutta", 4)),
             r"dal 74% al (\d+)%"),
            ("professionisti in classifica a tredici anni, nel post 9",
             riga("sensibilita", "mancanti", "Under 15 primo anno, solo", 1),
             r"ci sono (\d+) dei 77 futuri professionisti"),
            ("abbinamenti con ProCyclingStats",
             v("provenienza", "abbinati_pcs"), r"ne ho (\d+)"),
            ("abbinamenti esatti su nome e data",
             v("provenienza", "abbinamenti_esatti"),
             r"e (\d+) sono esatti su nome"),
            ("date di nascita corrette a mano",
             v("provenienza", "nascite_corrette"),
             r"corretto (\d+) date di nascita"),

            ("ripetizioni del bootstrap", v("validazione", "ripetizioni"),
             r"(\d+) volte su campioni"),
            ("ottimismo massimo", v("validazione", "ottimismo_massimo"),
             r"La risposta è (\d,\d+)"),
            ("eventi nelle coorti di verifica",
             riga("validazione", "temporale", "percentile Under 19", 4),
             r"contengono soltanto (\d+) casi"),
            ("professionisti con la definizione piu' stretta",
             riga("sensibilita", "definizione", "solo prima divisione", 1),
             r"passa da (\d+) a 151"),
            ("professionisti con la definizione piu' larga",
             riga("sensibilita", "definizione", "anche le Continental", 1),
             r"passa da 26 a (\d+)"),
            ("oscillazione dell'AUC", v("sensibilita", "oscillazione_auc"),
             r"in tutto di (\d,\d+)"),
            ("pendenza di calibrazione",
             riga("validazione", "ottimismo", "livello e pendenza", 6),
             r"vale fra (\d,\d\d) e 1,02"),
            ("uscite nell'ultimo anno di categoria",
             v("attrito", "quota_uscite_a_fine_categoria"),
             r"concentra il (\d+)% delle uscite"),
        ],
    }


def incrocio(db, livello, pendenza):
    """La percentuale di professionisti nella casella (livello, pendenza)."""
    for r in tabella(db, "traiettorie", "incrocio") or []:
        if r[0] == livello and r[1] == pendenza:
            return r[4]
    return None


def riga_soglia(db, cella, criterio, colonna):
    """Una colonna della riga di `metriche.soglie` per quella cella e quel criterio."""
    for r in tabella(db, "metriche", "soglie") or []:
        if r[0] == cella and r[1] == criterio:
            return r[colonna]
    return None


def _normalizza(testo):
    """Toglie il grassetto e manda a capo tutto su una riga sola.

    La prima versione cercava le cifre nel testo com'era, con gli asterischi del grassetto e
    gli a capo dentro le frasi. Bastava spostare un grassetto o riscrivere una riga per far
    fallire trenta controlli su ottanta, il che rendeva questo script un ostacolo alla
    riscrittura invece che una rete di sicurezza. Qui il markup sparisce e gli spazi
    diventano uno solo: le espressioni descrivono la frase, non la sua impaginazione.
    """
    return re.sub(r"\s+", " ", testo.replace("*", ""))


def controlla(testo, voci, problemi):
    testo = _normalizza(testo)
    for descrizione, atteso, pattern in voci:
        m = re.search(pattern, testo, re.I)
        citato = next((g for g in m.groups() if g), None) if m else None
        if atteso is None:
            stato = "NON CALCOLATO: eseguire l'analisi"
        elif m is None:
            stato = "NON CITATO nel documento"
        elif _numero(citato) is None:
            stato = "non interpretabile: %r" % citato
        elif abs(_numero(citato) - float(atteso)) > _tolleranza(citato):
            stato = "il documento dice %s" % citato
        else:
            stato = "ok"
        if stato != "ok":
            problemi.append(descrizione)
        print("  %-44s analisi %-9s %s"
              % (descrizione, "—" if atteso is None else _mostra(atteso), stato))


def _tolleranza(citato):
    """Quanto puo' discostarsi il valore citato da quello dell'archivio.

    Dipende da come e' scritto: chi arrotonda a numero intero non sta sbagliando, sta
    arrotondando, e la tolleranza deve essere mezza unita' dell'ultima cifra scritta.
    Confrontare «32» con 32,4 pretendendo l'uguaglianza segnalerebbe un errore che non
    c'e' — e un controllo che grida al lupo smette di essere letto.
    """
    decimali = len(citato.split(",")[1]) if "," in citato else 0
    return 0.5 * 10 ** (-decimali) + 1e-9


def _mostra(v):
    return ("%g" % v).replace(".", ",") if isinstance(v, float) else str(v)


def data_analisi(db):
    """La data dell'ultima esecuzione registrata nell'archivio."""
    r = db.execute("SELECT MAX(eseguito_il) FROM esecuzione").fetchone()
    return r[0][:10] if r and r[0] else None


def timbra(db):
    """Scrive nell'intestazione di ogni post la data dell'analisi contro cui e' stato
    verificato.

    I post sono l'unico documento del progetto scritto a mano, e finiscono fuori di casa:
    chi li legge deve poter sapere di quando siano i numeri. La riga non si scrive a mano,
    pero', altrimenti resterebbe indietro proprio quando conta. La mette questo script, e
    solo dopo che il controllo e' passato: se le cifre non corrispondono piu', la data non
    viene aggiornata e resta quella dell'ultima volta in cui corrispondevano.
    """
    quando = data_analisi(db)
    if not quando or not os.path.isdir(POST):
        return
    riga = "> **Cifre verificate contro l'analisi del %s.**" % quando
    for nome in sorted(os.listdir(POST)):
        if not re.match(r"^\d\d_.*\.md$", nome):
            continue
        percorso = os.path.join(POST, nome)
        with open(percorso, encoding="utf-8") as f:
            righe = f.read().split("\n")
        righe = [r for r in righe if not r.startswith("> **Cifre verificate")]
        for i, r in enumerate(righe):
            if r.startswith("> **Figure:**"):
                righe.insert(i + 1, riga)
                break
        else:
            continue
        with open(percorso, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(righe))
    print("Intestazioni dei post timbrate con la data dell'analisi: %s." % quando)


def main():
    if not os.path.exists(RISULTATI):
        sys.exit("Manca %s: eseguire prima l'analisi." % RISULTATI)
    db = sqlite3.connect(RISULTATI)
    problemi = []

    documenti = [(TRIPOD, attesi_tripod(db)), (PIANO, attesi_piano(db))]
    per_post = attesi_post(db)
    documenti += [(os.path.join(POST, nome), per_post[nome])
                  for nome in sorted(per_post)]

    for percorso, voci in documenti:
        if not os.path.exists(percorso):
            print("%s: manca, salto\n" % percorso.replace(os.sep, "/"))
            continue
        print(percorso.replace(os.sep, "/"))
        with open(percorso, encoding="utf-8") as f:
            controlla(f.read(), voci, problemi)
        print()

    if problemi:
        print("%d cifra/e non corrispondono piu' all'analisi." % len(problemi))
        print("Aggiornare il documento, e rileggere le affermazioni che vi si "
              "appoggiano: quando i numeri cambiano, di solito cambia anche cosa se ne "
              "puo' dire.")
        return 1
    timbra(db)
    db.close()
    print("Le cifre dei documenti scritti a mano corrispondono all'analisi corrente.")
    print("Le affermazioni qualitative restano da rivedere a mano: sono la parte che "
          "questo controllo non puo' fare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
