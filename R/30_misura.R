# Lo stesso punteggio non e' lo stesso risultato.
#
# NON E' UNO STEP DELLA GUIDA
#     I file numerati da 30 in su sono analisi nate dopo, da domande che il lavoro ha
#     fatto emergere. Questa nasce da Hasselaar e Elferink-Gemser (2025), che mostrano
#     due ciclisti con **lo stesso identico punteggio** in un ranking federale — 414 —
#     e livelli reali completamente diversi, 76 contro 21 in una metrica costruita
#     apposta. La loro critica colpisce la fonte di questo studio, e va verificata sui
#     nostri dati invece che accettata o respinta a parole.
#
# LE DUE DOMANDE
#     **Quanto sono frequenti i pari merito?** In una classifica dove la vittoria vale
#     cinque punti e il quinto posto uno, moltissimi atleti finiscono con lo stesso
#     totale. Se il totale e' l'unica cosa che si guarda, sono indistinguibili.
#
#     **Il modo in cui si arriva a un punteggio porta informazione?** Cinque punti si
#     ottengono con una vittoria oppure con cinque quinti posti. Il progetto ha scelto
#     fin dall'inizio di sciogliere i pari merito guardando prima le vittorie, poi i
#     secondi posti e cosi' via. Quella scelta si puo' mettere alla prova: le due
#     versioni del percentile si confrontano sugli stessi atleti, e la differenza di AUC
#     dice quanto valeva la pena distinguere.
#
# LA TERZA DOMANDA, CHE E' QUELLA DI HASSELAAR
#     La fonte pesa le gare per livello, ma **solo nelle categorie internazionali**: in
#     Juniores e Under 23 una gara nazionale vale il doppio di una regionale e una
#     internazionale il triplo, mentre in Esordienti e Allievi una gara all'estero vale
#     quanto una regionale. Non abbiamo il dettaglio delle singole gare, ma il rapporto
#     fra punti e piazzamenti nei primi cinque e' un indicatore indiretto: dove le gare
#     pesano, quel rapporto deve salire.
#
# USO
#     Rscript R/30_misura.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "pROC"))

suppressPackageStartupMessages({
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "misura"
MIN_EVENTI <- 5


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)

  d <- dbGetQuery(dd, "SELECT * FROM misure")
  if (nrow(d) == 0) stop("Tabella misure vuota: eseguire 08_prepara_modelli.py")
  celle <- conf$celle_modello

  cat(sprintf("Lo stesso punteggio non e' lo stesso risultato — coorti %d-%d\n",
              conf$coorti_a_c[1], conf$coorti_a_c[2]))

  # --- 1. quanto sono frequenti i pari merito ---------------------------------
  # Un atleta e' a pari merito se qualcun altro ha il suo stesso punteggio nella
  # classifica completa della sua stagione e cella: il flag viene da
  # 08_prepara_modelli.py, perche' qui ci sono solo gli atleti delle coorti. La quota e'
  # la parte di atleti a pari merito. Prima era uno meno il rapporto fra punteggi
  # distinti e atleti, calcolato sommando stagioni diverse: un'altra grandezza, che in
  # Under 23 gonfiava il dato fino a diciassette punti.
  pari <- dbGetQuery(dd, "SELECT cella, COUNT(*) n, SUM(pari) condivisi
                          FROM misure GROUP BY cella")
  pari$quota <- 100 * pari$condivisi / pari$n

  # --- 2. le due misure a confronto, cella per cella --------------------------
  righe <- list()
  for (c in celle) {
    x <- d[d$cella == c, ]
    if (nrow(x) == 0 || sum(x$PRO) < MIN_EVENTI) next
    r1 <- pROC::roc(x$PRO, x$pct_punti, quiet = TRUE, direction = "<")
    r2 <- pROC::roc(x$PRO, x$pct_esteso, quiet = TRUE, direction = "<")
    a1 <- as.numeric(pROC::auc(r1))
    a2 <- as.numeric(pROC::auc(r2))
    p <- tryCatch(pROC::roc.test(r1, r2, method = "delong", paired = TRUE)$p.value,
                  error = function(e) NA_real_)
    q <- pari$quota[pari$cella == c]
    righe[[length(righe) + 1]] <- list(c, nrow(x), sum(x$PRO),
                                       if (length(q)) q else NA_real_, a1, a2, a2 - a1, p)
    cat(sprintf("  %-7s n=%4d eventi=%3d  pari merito %4.1f%%  AUC punti %.3f -> esteso %.3f (%+.3f, p=%.3g)\n",
                c, nrow(x), sum(x$PRO), if (length(q)) q else NA, a1, a2, a2 - a1, p))
  }
  if (length(righe) == 0) stop("Nessuna cella con abbastanza eventi.")

  guadagni <- sapply(righe, function(r) r[[7]])
  positivi <- sum(guadagni > 0)

  # --- 3. quanto vale un piazzamento, categoria per categoria -----------------
  # Il rapporto fra punti e piazzamenti nei primi cinque: dove la fonte pesa le gare per
  # livello, un piazzamento vale in media di piu'.
  rap <- dbGetQuery(dd, "SELECT categoria, COUNT(*) n, AVG(punti) punti,
                                AVG(top5) top5, AVG(punti / NULLIF(top5, 0)) rapporto
                         FROM misure WHERE top5 > 0 GROUP BY categoria ORDER BY categoria")
  cat("\n  quanto vale in media un piazzamento nei primi cinque:\n")
  for (i in seq_len(nrow(rap))) {
    cat(sprintf("    %-4s %.2f punti per piazzamento (%d osservazioni)\n",
                rap$categoria[i], rap$rapporto[i], rap$n[i]))
  }

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(
    ar, "confronto", righe,
    c("cella", "atleti", "professionisti", "pari_merito", "auc_punti", "auc_esteso",
      "differenza", "p"),
    titolo = "Le due versioni dello stesso piazzamento",
    nota = paste("le due misure sono calcolate sugli stessi atleti: il confronto e'",
                 "appaiato, e il test di DeLong ne tiene conto"))

  scrivi_tabella(
    ar, "rapporto",
    lapply(seq_len(nrow(rap)), function(i)
      list(rap$categoria[i], rap$n[i], round(rap$punti[i], 1),
           round(rap$top5[i], 2), round(rap$rapporto[i], 2))),
    c("categoria", "osservazioni", "punti medi", "piazzamenti medi",
      "punti per piazzamento"),
    titolo = "Quanto vale un piazzamento, categoria per categoria",
    nota = paste("la scala della tabella precedente si applica a ogni piazzamento: in",
                 "Esordienti e Allievi e' piatta salvo i due campionati italiani,",
                 "dagli Juniores in su cresce con il livello della gara"))

  scrivi_valore(ar, "celle_migliorate", positivi)
  scrivi_valore(ar, "celle_confrontate", length(righe))
  scrivi_valore(ar, "guadagno_massimo", round(max(guadagni), 3))
  scrivi_valore(ar, "guadagno_medio", round(mean(guadagni), 3))
  scrivi_valore(ar, "pari_merito_massimo", round(max(pari$quota), 1))
  scrivi_valore(ar, "rapporto_estremi",
                list(bassa = rap$categoria[which.min(rap$rapporto)],
                     valore_basso = round(min(rap$rapporto), 2),
                     alta = rap$categoria[which.max(rap$rapporto)],
                     valore_alto = round(max(rap$rapporto), 2)))
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
