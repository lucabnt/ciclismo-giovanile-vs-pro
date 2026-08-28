# STEP 19 — cosa succede se si usa davvero il ranking per selezionare.
#
# LA DOMANDA
#     Le sezioni precedenti dicono che il rendimento giovanile predice, e quanto. Questa
#     traduce il "quanto" in cio' che una societa' o una famiglia si trova davanti:
#     se si guardassero solo gli atleti sopra una certa soglia, quanti futuri
#     professionisti si intercetterebbero, e quanti dei selezionati non lo diventeranno.
#
# PERCHE' NON BASTA L'AUC
#     Un'AUC di 0,89 sembra ottima. Ma con un esito raro — meno del 3% della coorte
#     diventa professionista — anche un ordinamento quasi perfetto produce moltissimi
#     falsi positivi, perche' i non professionisti sono trenta volte piu' numerosi. Il
#     valore predittivo positivo e' l'unico numero che lo rende visibile, ed e' quello
#     che nessuno riporta mai.
#
# LE SOGLIE
#     Due tipi, per due usi.
#
#     La soglia di Youden e' quella che massimizza sensibilita' + specificita' - 1: e' la
#     scelta "statisticamente ottima" e serve da riferimento.
#
#     Le soglie fisse — il 10% e il 25% migliore della cella — sono quelle che una
#     societa' userebbe davvero, perche' corrispondono a una capienza: "quanti ne posso
#     seguire". Sono le piu' utili da citare.
#
# USO
#     Rscript R/19_metriche.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "pROC"))

suppressPackageStartupMessages({
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "metriche"

# Percentili di taglio da riportare oltre alla soglia di Youden.
SOGLIE_FISSE <- c(90, 75)


# La tabella 2x2 a una data soglia, con le quattro metriche che ne discendono.
metriche <- function(pro, pct, soglia) {
  sel <- pct >= soglia
  vp <- sum(sel & pro == 1)
  fp <- sum(sel & pro == 0)
  fn <- sum(!sel & pro == 1)
  vn <- sum(!sel & pro == 0)
  list(soglia = soglia, selezionati = vp + fp,
       vp = vp, fp = fp, fn = fn, vn = vn,
       sensibilita = if (vp + fn > 0) vp / (vp + fn) else NA_real_,
       specificita = if (vn + fp > 0) vn / (vn + fp) else NA_real_,
       vpp = if (vp + fp > 0) vp / (vp + fp) else NA_real_,
       vpn = if (vn + fn > 0) vn / (vn + fn) else NA_real_)
}


riga <- function(cella, nome_soglia, m, n) {
  list(cella, nome_soglia, round(m$soglia, 1), m$selezionati, m$vp, m$fp,
       100 * m$sensibilita, 100 * m$specificita, 100 * m$vpp, 100 * m$vpn)
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  dati <- leggi_campione(dd)
  celle <- conf$celle_modello

  cat(sprintf("STEP 19 — metriche pratiche su %d celle\n", length(celle)))

  righe <- list()
  chiave <- NULL
  for (cella in celle) {
    d <- dati[dati[[paste0("present_", cella)]] == 1 &
                !is.na(dati[[paste0("pct_", cella)]]) & !is.na(dati$PRO), ]
    pro <- as.integer(d$PRO)
    pct <- as.numeric(d[[paste0("pct_", cella)]])
    n <- length(pro)
    if (sum(pro) < conf$min_cella_pubblicabile) next

    # Youden: la soglia che massimizza sensibilita' + specificita' - 1.
    r <- pROC::roc(pro, pct, quiet = TRUE)
    j <- pROC::coords(r, "best", best.method = "youden", transpose = FALSE)
    s_youden <- as.numeric(j$threshold[1])

    m <- metriche(pro, pct, s_youden)
    righe[[length(righe) + 1]] <- riga(cella, "Youden", m, n)
    cat(sprintf("  %-7s Youden  soglia=%5.1f  sens=%4.0f%%  VPP=%4.0f%%  (%d selezionati)\n",
                cella, m$soglia, 100 * m$sensibilita, 100 * m$vpp, m$selezionati))

    for (q in SOGLIE_FISSE) {
      s <- as.numeric(quantile(pct, q / 100, na.rm = TRUE))
      m <- metriche(pro, pct, s)
      righe[[length(righe) + 1]] <- riga(cella, sprintf("migliore %d%%", 100 - q), m, n)
      cat(sprintf("  %-7s top%-3d  soglia=%5.1f  sens=%4.0f%%  VPP=%4.0f%%  (%d selezionati)\n",
                  cella, 100 - q, m$soglia, 100 * m$sensibilita, 100 * m$vpp,
                  m$selezionati))
      # La frase da citare si costruisce sulla cella piu' discriminante al 10%.
      if (q == 90) {
        cand <- list(cella = cella, sensibilita = 100 * m$sensibilita,
                     vpp = 100 * m$vpp, selezionati = m$selezionati,
                     eventi = sum(pro), n = n)
        if (is.null(chiave) || cand$sensibilita > chiave$sensibilita) chiave <- cand
      }
    }
  }

  if (length(righe) == 0) stop("Nessuna cella con abbastanza eventi.")

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(
    ar, "soglie", righe,
    c("cella", "criterio", "soglia", "selezionati", "veri positivi", "falsi positivi",
      "sensibilita", "specificita", "vpp", "vpn"),
    titolo = "Cosa si intercetta, e a che prezzo",
    nota = paste("La soglia e' un percentile della cella. Sensibilita': quota di futuri",
                 "professionisti dentro la selezione. Valore predittivo positivo: quota",
                 "di selezionati che diventera' professionista."))

  scrivi_valore(ar, "soglie_fisse", 100 - SOGLIE_FISSE)
  scrivi_valore(ar, "frase_chiave", chiave,
                "la cella in cui il migliore 10% intercetta piu' futuri professionisti")
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
