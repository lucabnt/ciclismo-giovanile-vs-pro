"""
Accenti italiani nel testo generato.

PERCHE' UN MODULO E NON UNA CORREZIONE UNA TANTUM
    `analisi.md` si rigenera a ogni esecuzione, e si rigenerera' fra anni con dati
    nuovi. Correggere il documento a mano significherebbe rifarlo ogni volta: la
    correzione deve stare nel codice che lo produce.

    Qui c'e' la tabella delle parole italiane che portano l'accento, e la funzione che
    la applica. Il testo dei moduli puo' quindi essere scritto in ASCII puro — comodo
    per chi edita il codice da un terminale qualunque — e uscire accentato.

COSA NON VIENE TOCCATO
    Gli apostrofi di elisione (l', un', dell', nell') e il troncamento `po'` non sono
    nella tabella e restano intatti. La sostituzione richiede che la parola sia intera:
    non basta che la sequenza compaia dentro un'altra parola.
"""
import re

# Forma senza accento -> forma corretta. Solo parole intere.
ACCENTI = {
    "e": "è", "ne": "né", "se": "sé", "cioe": "cioè", "perche": "perché",
    "poiche": "poiché", "benche": "benché", "affinche": "affinché", "finche": "finché",
    "anziche": "anziché", "onesta": "onestà", "nonche": "nonché",
    "piu": "più", "gia": "già", "cosi": "così", "li": "lì", "cio": "ciò",
    "puo": "può", "pero": "però", "giu": "giù",
    "sara": "sarà", "saranno": "saranno", "potra": "potrà", "dovra": "dovrà",
    "andra": "andrà", "verra": "verrà", "restera": "resterà", "arrivera": "arriverà",
    "ridurra": "ridurrà", "crescera": "crescerà", "cambiera": "cambierà",
    "passera": "passerà", "restera": "resterà", "arrivera": "arriverà",
    "entrera": "entrerà", "uscira": "uscirà", "andra": "andrà",
    "portera": "porterà", "servira": "servirà", "dira": "dirà", "avra": "avrà",
    "vorra": "vorrà", "bastera": "basterà", "ci": "ci",
    "meta": "metà", "eta": "età", "citta": "città", "societa": "società",
    "qualita": "qualità", "quantita": "quantità", "numerosita": "numerosità",
    "molteplicita": "molteplicità",
    "eventualita": "eventualità",
    "entita": "entità", "parita": "parità", "mobilita": "mobilità",
    "stagionalita": "stagionalità", "variabilita": "variabilità", "unita": "unità",
    "possibilita": "possibilità", "probabilita": "probabilità", "capacita": "capacità",
    "densita": "densità", "continuita": "continuità", "normalita": "normalità",
    "facilita": "facilità", "rilevabilita": "rilevabilità", "bonta": "bontà",
    "predittivita": "predittività", "multicollinearita": "multicollinearità",
    "attivita": "attività", "specialita": "specialità", "identita": "identità",
    "verita": "verità", "liberta": "libertà", "difficolta": "difficoltà",
    "sensibilita": "sensibilità", "specificita": "specificità",
    "discontinuita": "discontinuità", "continuita": "continuità",
    "selettivita": "selettività", "affidabilita": "affidabilità",
    "stabilita": "stabilità", "specialita": "specialità",
    "proprieta": "proprietà", "novita": "novità",
    "confrontabilita": "confrontabilità", "comparabilita": "comparabilità",
    "distinguibilita": "distinguibilità", "generalizzabilita": "generalizzabilità",
    "impurita": "impurità", "percio": "perciò", "cio": "ciò",
    "disponibilita": "disponibilità", "scarsita": "scarsità", "si": "sì", "da": "dà",
    "puberta": "pubertà", "nazionalita": "nazionalità",
    "inutilita": "inutilità", "penalita": "penalità", "scarsita": "scarsità",
    "maturita": "maturità", "profondita": "profondità", "solidita": "solidità",
    "utilita": "utilità", "necessita": "necessità",
    "regolarita": "regolarità", "anzianita": "anzianità",
    "gravita": "gravità", "novita": "novità", "eterogeneita": "eterogeneità",
    "diventera": "diventerà", "restera": "resterà", "sapra": "saprà",
    "meta_campo": "metà campo",
}

# Confini: la parola non deve essere preceduta ne' seguita da una lettera. Cosi'
# l'apostrofo di elisione in "un'altra" o "l'eta'" non viene scambiato per un accento.
_LETTERA = r"[A-Za-zÀ-ÖØ-öø-ÿ]"


def _sostituisci(m):
    parola = m.group(1)
    accentata = ACCENTI[parola.lower()]
    return accentata.capitalize() if parola[0].isupper() else accentata


_RX = re.compile(r"(?<!%s)(%s)'(?!%s)"
                 % (_LETTERA, "|".join(sorted(ACCENTI, key=len, reverse=True)), _LETTERA),
                 re.IGNORECASE)


def _fuori_codice(testo, funzione):
    """Applica `funzione` solo al testo, mai dentro il codice.

    Riconosce sia i blocchi delimitati da tre apici inversi sia i tratti in linea. Una
    divisione ingenua sugli apici sbaglierebbe la parita' al primo blocco di codice che
    un modulo dovesse aggiungere.
    """
    pezzi = re.split(r"(```.*?```|`[^`]*`)", testo, flags=re.S)
    for i in range(0, len(pezzi), 2):          # gli indici dispari sono i tratti di codice
        pezzi[i] = funzione(pezzi[i])
    return "".join(pezzi)


def applica(testo):
    """Sostituisce le forme ASCII con quelle accentate, fuori dai tratti di codice."""
    return _fuori_codice(testo, lambda t: _RX.sub(_sostituisci, t))


_RX_APOSTROFO = re.compile(r"(?<!%s)(%s+)'(?!%s)" % (_LETTERA, _LETTERA, _LETTERA))

# Elisioni e troncamenti: finiscono in apostrofo ma non sono accenti mancanti.
_NON_ACCENTI = {"po", "un", "l", "d", "n", "c", "s", "t", "v", "m", "gl", "qual", "be"}


def residui(testo):
    """Parole con apostrofo che la tabella non conosce: possibili accenti mancanti.

    Rete di sicurezza per il testo nuovo. Un modulo scritto fra due anni potrebbe usare
    una parola accentata non prevista: l'assemblatore la segnala invece di lasciarla
    passare in un documento pubblicato.
    """
    fuori = []
    _fuori_codice(testo, lambda t: fuori.extend(
        m.group(1) for m in _RX_APOSTROFO.finditer(t)
        if m.group(1).lower() not in ACCENTI and m.group(1).lower() not in _NON_ACCENTI) or t)
    return sorted(set(fuori))
