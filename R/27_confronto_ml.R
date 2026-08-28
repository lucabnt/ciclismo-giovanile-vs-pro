# STEP 27 — un modello piu' complicato farebbe meglio?
#
# A COSA SERVE QUESTO CONFRONTO
#     Non a scegliere il modello finale, che resta quello parametrico e interpretabile.
#     Serve a rispondere a un'obiezione legittima: «con tutti questi dati, una foresta
#     casuale non troverebbe di piu'?».
#
#     Se la risposta e' no — l'esito piu' probabile con poche decine di eventi — allora
#     la semplicita' dei modelli usati non e' una scorciatoia ma la scelta giusta, e
#     averlo verificato vale piu' che averlo affermato.
#
# COME SI CONFRONTA ONESTAMENTE
#     Sulle stesse partizioni. Si divide il campione in cinque parti, si addestra su
#     quattro e si misura sulla quinta, si ripete per ogni parte e poi si ripete tutto
#     cinque volte con partizioni diverse. Entrambi i modelli vedono esattamente gli
#     stessi dati di addestramento e vengono misurati esattamente sugli stessi dati di
#     verifica: la differenza fra le loro AUC e' allora attribuibile al modello e non
#     alla fortuna della divisione.
#
#     La foresta riceve **piu' informazione** del modello parametrico, non meno: tutte le
#     celle invece di una sola. Se anche cosi' non guadagna, la conclusione e' solida.
#
# PERCHE' NON C'E' UNA RICERCA DI IPERPARAMETRI
#     Con settantaquattro eventi, ottimizzare gli iperparametri dentro la validazione
#     incrociata aggiungerebbe rumore piu' che prestazione, e farlo fuori sarebbe barare.
#     Si usano i valori predefiniti, che per una foresta casuale sono ragionevoli, e lo
#     si dichiara.
#
# USO
#     Rscript R/27_confronto_ml.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "randomForest", "logistf", "pROC"))

suppressPackageStartupMessages({
  library(randomForest)
  library(logistf)
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "confronto_ml"
PASSO <- 10
PARTI <- 5         # partizioni della validazione incrociata
RIPETIZIONI <- 5   # quante volte si ripete con partizioni diverse
set.seed(20260828)


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  celle <- conf$celle_modello

  colonne <- c("PRO", "birth_year", "rel_age", "n_seasons_youth",
               paste0("pct_", celle), paste0("present_", celle))
  d <- dbGetQuery(dd, sprintf("SELECT %s FROM campione WHERE PRO IS NOT NULL
                               AND birth_year IS NOT NULL", paste(colonne, collapse = ", ")))

  # L'assenza dalla classifica non e' un valore mancante: e' un rendimento che non c'e'
  # stato. Si codifica con un valore fuori scala, cosi' la foresta puo' separarlo, e con
  # l'indicatrice di presenza gia' presente fra le colonne.
  for (c in celle) {
    v <- d[[paste0("pct_", c)]]
    pres <- d[[paste0("present_", c)]]
    d[[paste0("pct_", c)]] <- ifelse(is.na(pres) | pres == 0 | is.na(v), -10, v)
    d[[paste0("present_", c)]] <- ifelse(is.na(pres), 0, pres)
  }
  d$rel_age[is.na(d$rel_age)] <- median(d$rel_age, na.rm = TRUE)
  d$n_seasons_youth[is.na(d$n_seasons_youth)] <- 0
  d$coorte <- d$birth_year - mean(d$birth_year)

  # Il modello parametrico e' quello del documento: una cella sola, piu' la coorte.
  cella_principale <- paste0("pct_", conf$celle_annidate[length(conf$celle_annidate) - 1])
  if (!(cella_principale %in% names(d))) cella_principale <- paste0("pct_", celle[1])
  d$pct10 <- (d[[cella_principale]] - mean(d[[cella_principale]])) / PASSO

  cat(sprintf("STEP 27 — confronto con il machine learning, %d atleti, %d eventi\n",
              nrow(d), sum(d$PRO)))
  cat(sprintf("  parametrico: %s + coorte\n", cella_principale))
  cat(sprintf("  foresta casuale: %d predittori (tutte le celle, eta' relativa, "
              , length(celle) * 2 + 2))
  cat("stagioni corse)\n")

  predittori <- c(paste0("pct_", celle), paste0("present_", celle),
                  "rel_age", "n_seasons_youth", "coorte")
  formula_rf <- as.formula(paste("y ~", paste(predittori, collapse = " + ")))

  auc_par <- numeric(0)
  auc_rf <- numeric(0)
  for (rip in seq_len(RIPETIZIONI)) {
    piega <- sample(rep(seq_len(PARTI), length.out = nrow(d)))
    p_par <- numeric(nrow(d))
    p_rf <- numeric(nrow(d))
    for (k in seq_len(PARTI)) {
      tr <- d[piega != k, ]
      te <- d[piega == k, ]
      if (sum(tr$PRO) < 5) next

      f <- logistf(PRO ~ pct10 + coorte, data = tr)
      p_par[piega == k] <- as.vector(predict(f, newdata = te, type = "response"))

      tr$y <- factor(tr$PRO, levels = c(0, 1))
      rf <- randomForest(formula_rf, data = tr, ntree = 500)
      p_rf[piega == k] <- predict(rf, newdata = te, type = "prob")[, "1"]
    }
    auc_par <- c(auc_par, as.numeric(pROC::auc(pROC::roc(d$PRO, p_par, quiet = TRUE))))
    auc_rf <- c(auc_rf, as.numeric(pROC::auc(pROC::roc(d$PRO, p_rf, quiet = TRUE))))
    cat(sprintf("    ripetizione %d: parametrico %.3f, foresta %.3f\n",
                rip, auc_par[rip], auc_rf[rip]))
  }

  differenze <- auc_rf - auc_par
  cat(sprintf("\n  media su %d ripetizioni: parametrico %.3f, foresta %.3f, "
              , RIPETIZIONI, mean(auc_par), mean(auc_rf)))
  cat(sprintf("differenza %+.3f\n", mean(differenze)))

  # Quali variabili la foresta ritiene utili. Non e' una spiegazione causale, e' una
  # diagnostica: se mettesse in cima una cella che il modello parametrico ignora,
  # varrebbe la pena aggiungerla.
  d$y <- factor(d$PRO, levels = c(0, 1))
  rf_tutto <- randomForest(formula_rf, data = d, ntree = 500, importance = TRUE)
  imp <- importance(rf_tutto, type = 2)
  ordine <- order(imp[, 1], decreasing = TRUE)[1:6]
  importanza <- lapply(ordine, function(i) list(rownames(imp)[i], round(imp[i, 1], 2)))
  cat("\n  variabili piu' usate dalla foresta:\n")
  for (r in importanza) cat(sprintf("    %-22s %s\n", r[[1]], r[[2]]))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(
    ar, "confronto",
    list(list(sprintf("parametrico (%s + coorte)", cella_principale),
              2, round(mean(auc_par), 3), round(sd(auc_par), 3)),
         list(sprintf("foresta casuale (%d predittori)", length(predittori)),
              length(predittori), round(mean(auc_rf), 3), round(sd(auc_rf), 3))),
    c("modello", "predittori", "auc media", "deviazione standard"),
    titolo = "Modello parametrico contro foresta casuale",
    nota = sprintf(paste("validazione incrociata a %d parti, ripetuta %d volte sulle",
                         "stesse partizioni per entrambi i modelli"), PARTI, RIPETIZIONI))

  scrivi_tabella(ar, "importanza", importanza,
                 c("variabile", "importanza (riduzione di impurita')"),
                 titolo = "Su cosa si appoggia la foresta",
                 nota = paste("diagnostica, non spiegazione causale: serve a vedere se",
                              "la foresta usi informazione che il modello parametrico",
                              "sta ignorando"))

  scrivi_valore(ar, "parti", PARTI)
  scrivi_valore(ar, "ripetizioni", RIPETIZIONI)
  scrivi_valore(ar, "n", nrow(d))
  scrivi_valore(ar, "eventi", sum(d$PRO))
  scrivi_valore(ar, "differenza", round(mean(differenze), 3),
                "AUC della foresta meno quella del modello parametrico")
  scrivi_valore(ar, "cella_principale", cella_principale)
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
