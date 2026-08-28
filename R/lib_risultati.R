# L'archivio dei risultati, lato R.
#
# PERCHE'
#     I modelli girano in R, il report si assembla in Python. Il punto di incontro e'
#     `output/risultati.db`: questo file scrive esattamente nello stesso schema che usa
#     `report/lib_risultati.py`, con la stessa serializzazione JSON. Un valore scritto
#     qui si rilegge da Python senza conversioni e senza sapere chi lo ha prodotto.
#
#     Il vincolo utile e' che un numero non presente nell'archivio non puo' finire nel
#     testo: non c'e' modo di scrivere a mano un risultato nel report.
#
# COME SI USA
#
#     source("R/lib_risultati.R")
#
#     ar <- archivio_apri("univariati")
#     scrivi_valore(ar, "auc_u15y1", 0.74, "area sotto la curva, cella U15y1")
#     scrivi_tabella(ar, "per_cella", righe, c("cella", "n", "OR", "AUC"))
#     archivio_chiudi(ar)
#
#     Aprire l'archivio cancella i risultati precedenti di quel modulo: una nuova
#     esecuzione non lascia in giro numeri di quella vecchia.
#
# DIPENDENZE
#     RSQLite e jsonlite. Si installano con:
#         install.packages(c("RSQLite", "jsonlite"))

suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
  library(jsonlite)
})

DB_RISULTATI <- "output/risultati.db"
DB_MODELLI   <- "data/analisi/modelli.db"

DDL <- c(
  "CREATE TABLE IF NOT EXISTS valore (
     modulo TEXT NOT NULL, chiave TEXT NOT NULL, valore TEXT, nota TEXT,
     PRIMARY KEY (modulo, chiave))",
  "CREATE TABLE IF NOT EXISTS tabella (
     modulo TEXT NOT NULL, chiave TEXT NOT NULL, colonne TEXT NOT NULL,
     righe TEXT NOT NULL, titolo TEXT, nota TEXT,
     PRIMARY KEY (modulo, chiave))",
  "CREATE TABLE IF NOT EXISTS figura (
     modulo TEXT NOT NULL, chiave TEXT NOT NULL, percorso TEXT NOT NULL,
     didascalia TEXT, PRIMARY KEY (modulo, chiave))",
  "CREATE TABLE IF NOT EXISTS esecuzione (
     modulo TEXT PRIMARY KEY, eseguito_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     note TEXT)"
)


archivio_apri <- function(modulo, percorso = DB_RISULTATI) {
  dir.create(dirname(percorso), showWarnings = FALSE, recursive = TRUE)
  db <- dbConnect(SQLite(), percorso)
  for (q in DDL) dbExecute(db, q)
  for (t in c("valore", "tabella", "figura")) {
    dbExecute(db, sprintf("DELETE FROM %s WHERE modulo = ?", t), list(modulo))
  }
  list(db = db, modulo = modulo)
}


archivio_chiudi <- function(ar, note = NULL) {
  dbExecute(ar$db,
            "INSERT OR REPLACE INTO esecuzione (modulo, eseguito_il, note)
             VALUES (?, CURRENT_TIMESTAMP, ?)",
            list(ar$modulo, if (is.null(note)) NA_character_ else note))
  dbDisconnect(ar$db)
}


# La serializzazione deve combaciare con quella di Python: `json.dumps(0.74)` produce
# `0.74`, non `[0.74]`. In R uno scalare e' un vettore di lunghezza uno, quindi va
# chiesto esplicitamente a jsonlite di non incapsularlo.
come_json <- function(x) {
  if (length(x) == 1 && is.null(names(x))) {
    if (is.na(x)) return("null")
    return(toJSON(x, auto_unbox = TRUE, digits = NA))
  }
  toJSON(x, auto_unbox = TRUE, digits = NA, null = "null")
}


scrivi_valore <- function(ar, chiave, valore, nota = NULL) {
  dbExecute(ar$db, "INSERT OR REPLACE INTO valore VALUES (?,?,?,?)",
            list(ar$modulo, chiave, come_json(valore),
                 if (is.null(nota)) NA_character_ else nota))
}


# Le righe arrivano come data.frame o come lista di liste. In entrambi i casi escono
# come lista di liste, che e' cio' che Python si aspetta di rileggere.
scrivi_tabella <- function(ar, chiave, righe, colonne, titolo = NULL, nota = NULL) {
  if (is.data.frame(righe)) {
    righe <- lapply(seq_len(nrow(righe)), function(i) unname(as.list(righe[i, ])))
  }
  righe <- lapply(righe, function(r) {
    lapply(r, function(v) if (length(v) == 1 && is.na(v)) NULL else v)
  })
  dbExecute(ar$db, "INSERT OR REPLACE INTO tabella VALUES (?,?,?,?,?,?)",
            list(ar$modulo, chiave,
                 toJSON(colonne, auto_unbox = FALSE),
                 toJSON(righe, auto_unbox = TRUE, digits = NA, null = "null"),
                 if (is.null(titolo)) NA_character_ else titolo,
                 if (is.null(nota)) NA_character_ else nota))
}


scrivi_figura <- function(ar, chiave, percorso, didascalia = NULL) {
  dbExecute(ar$db, "INSERT OR REPLACE INTO figura VALUES (?,?,?,?)",
            list(ar$modulo, chiave, percorso,
                 if (is.null(didascalia)) NA_character_ else didascalia))
}


# ---------------------------------------------------------------------------
# Lettura dei dati preparati da Python
# ---------------------------------------------------------------------------

# I modelli non aprono mai `analisi.db`: leggono il rettangolo gia' filtrato che
# `scripts/08_prepara_modelli.py` ha costruito applicando le regole di config.toml.
# Cosi' le scelte dello studio restano in un posto solo.
dati_apri <- function(percorso = DB_MODELLI) {
  if (!file.exists(percorso)) {
    stop(sprintf("Manca %s. Eseguire prima: python scripts/08_prepara_modelli.py",
                 percorso), call. = FALSE)
  }
  dbConnect(SQLite(), percorso)
}


leggi_config <- function(db) {
  r <- dbGetQuery(db, "SELECT chiave, valore FROM config")
  out <- lapply(r$valore, function(v) fromJSON(v))
  names(out) <- r$chiave
  out
}


leggi_campione <- function(db, tabella = "campione") {
  dbGetQuery(db, sprintf("SELECT * FROM %s", tabella))
}


leggi_celle <- function(db) {
  dbGetQuery(db, "SELECT * FROM celle ORDER BY ordine")
}
