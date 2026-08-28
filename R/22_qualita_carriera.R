# STEP 22 e 23 — non solo se si arriva, ma fino a dove.
#
# LA DOMANDA B
#     Tutto il resto dello studio tratta il professionismo come una porta: dentro o
#     fuori. Ma fra i professionisti c'e' chi corre tre anni in una squadra di seconda
#     divisione e chi vince tappe al Giro. La Domanda B chiede se il rendimento giovanile
#     dica qualcosa anche su **quanto lontano** si arriva, non solo sull'arrivarci.
#
# DUE MODI DI GUARDARE LA STESSA COSA
#     **Il modello ordinale (STEP 22)** tratta i quattro livelli — non professionista,
#     professionista, top 500, top 100 — come gradini di un'unica scala, e stima un solo
#     coefficiente. E' l'analisi principale: usa tutta l'informazione, non spezza il
#     campione e non soffre del problema di selezione.
#
#     **Il modello a stadi (STEP 23)** scompone il percorso in tre passaggi successivi:
#     diventare professionista, poi entrare nel top 500 fra i professionisti, poi nel top
#     100 fra i top 500. Ogni coefficiente e' condizionato a «fra chi e' arrivato a quel
#     livello», il che lo rende piu' difficile da leggere ma piu' informativo su dove il
#     rendimento giovanile smette di contare.
#
#     Da qui esce anche la probabilita' composta, che e' il numero piu' comunicabile
#     dell'intero studio.
#
# PERCHE' IL PREDITTORE E' L'UNDER 19 E NON L'UNDER 23
#     La guida propone di usarli entrambi. Ma nelle coorti della Domanda B sono presenti
#     in Under 23 appena 236 atleti, di cui 94 professionisti: chiedere entrambe le celle
#     riduce il campione a poche centinaia di sopravvissuti, dove i professionisti sono
#     quasi la meta'. E' esattamente il problema di selezione che il modello ordinale
#     dovrebbe evitare.
#
#     L'Under 19 secondo anno e' invece presente per 1.730 atleti e cattura 140 dei 145
#     professionisti, compresi tutti e quindici quelli arrivati nel top 100. E' quindi il
#     predittore dell'analisi principale, e l'Under 23 entra solo in un modello
#     secondario, dichiarato come condizionato.
#
# L'ASSUNZIONE DA CONTROLLARE
#     Il modello ordinale assume che l'effetto del predittore sia lo stesso su tutti i
#     gradini: gli **odds proporzionali**. Si controlla stimando separatamente le tre
#     soglie cumulate e confrontando i coefficienti. Se sono simili l'assunzione regge;
#     se divergono, il coefficiente unico e' una media che nasconde andamenti diversi.
#
# USO
#     Rscript R/22_qualita_carriera.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "MASS", "logistf"))

suppressPackageStartupMessages({
  library(MASS)
  library(logistf)
})

source("R/lib_risultati.R")

MODULO <- "qualita"
PASSO <- 10
ETICHETTE <- c("non professionista", "professionista", "top 500", "top 100")


# Un singolo stadio del percorso: chi passa al livello successivo fra chi ha raggiunto
# quello attuale. Firth perche' gli ultimi stadi hanno pochissimi eventi.
stadio <- function(d, soglia, etichetta) {
  sel <- d$livello >= soglia - 1
  x <- d[sel, ]
  y <- as.integer(x$livello >= soglia)
  if (sum(y) < 5 || length(y) - sum(y) < 5) {
    return(list(etichetta = etichetta, n = length(y), eventi = sum(y), sottile = TRUE))
  }
  f <- logistf(y ~ pct10, data = data.frame(y = y, pct10 = x$pct10))
  list(etichetta = etichetta, n = length(y), eventi = sum(y), sottile = FALSE,
       or = exp(unname(coef(f)["pct10"])),
       lo = exp(f$ci.lower[["pct10"]]), hi = exp(f$ci.upper[["pct10"]]),
       p = unname(f$prob["pct10"]),
       fit = f)
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  d <- dbGetQuery(dd, "SELECT athlete_id, tier, pct_U19y2, pct_U23y1, present_U19y2,
                              present_U23y1, birth_year FROM campione_b
                       WHERE present_U19y2 = 1 AND pct_U19y2 IS NOT NULL
                         AND tier IS NOT NULL AND birth_year IS NOT NULL")
  d$livello <- as.integer(d$tier)
  d$pct10 <- (as.numeric(d$pct_U19y2) - mean(as.numeric(d$pct_U19y2))) / PASSO
  d$coorte <- d$birth_year - mean(d$birth_year)

  conteggi <- table(factor(d$livello, levels = 0:3))
  cat(sprintf("STEP 22-23 — qualita' della carriera, coorti %d-%d\n",
              conf$coorti_b[1], conf$coorti_b[2]))
  cat(sprintf("  %d atleti presenti in Under 19 secondo anno\n", nrow(d)))
  for (i in 0:3) {
    cat(sprintf("    %-20s %5d\n", ETICHETTE[i + 1], conteggi[[as.character(i)]]))
  }

  # --- STEP 22: il modello ordinale ------------------------------------------
  d$livello_f <- factor(d$livello, levels = 0:3, labels = ETICHETTE, ordered = TRUE)
  ord <- MASS::polr(livello_f ~ pct10 + coorte, data = d, Hess = TRUE)
  b <- coef(ord)[["pct10"]]
  se <- sqrt(diag(vcov(ord)))[["pct10"]]
  or_ord <- exp(b)
  ic_ord <- exp(c(b - 1.96 * se, b + 1.96 * se))
  p_ord <- 2 * pnorm(-abs(b / se))
  cat(sprintf("\n  modello ordinale: OR=%.2f [%.2f-%.2f] per %d punti di percentile, p=%.3g\n",
              or_ord, ic_ord[1], ic_ord[2], PASSO, p_ord))

  # --- il controllo degli odds proporzionali ---------------------------------
  # Si stimano le tre soglie cumulate separatamente: se il coefficiente e' lo stesso,
  # l'assunzione del modello ordinale regge.
  soglie <- list()
  for (k in 1:3) {
    y <- as.integer(d$livello >= k)
    f <- logistf(y ~ pct10 + coorte, data = data.frame(y = y, pct10 = d$pct10,
                                                       coorte = d$coorte))
    soglie[[length(soglie) + 1]] <- list(
      sprintf("almeno %s", ETICHETTE[k + 1]), sum(y),
      exp(unname(coef(f)["pct10"])),
      exp(f$ci.lower[["pct10"]]), exp(f$ci.upper[["pct10"]]))
    cat(sprintf("    soglia «almeno %s» (%d casi): OR=%.2f [%.2f-%.2f]\n",
                ETICHETTE[k + 1], sum(y), soglie[[k]][[3]], soglie[[k]][[4]],
                soglie[[k]][[5]]))
  }
  or_soglie <- sapply(soglie, function(s) s[[3]])
  divario <- max(or_soglie) / min(or_soglie)

  # --- STEP 23: gli stadi successivi -----------------------------------------
  stadi <- list(stadio(d, 1, "diventare professionista"),
                stadio(d, 2, "entrare nel top 500, fra i professionisti"),
                stadio(d, 3, "entrare nel top 100, fra i top 500"))
  cat("\n  stadi successivi:\n")
  for (s in stadi) {
    if (isTRUE(s$sottile)) {
      cat(sprintf("    %-42s n=%4d eventi=%3d  troppo sottile\n", s$etichetta, s$n,
                  s$eventi))
    } else {
      cat(sprintf("    %-42s n=%4d eventi=%3d  OR=%.2f [%.2f-%.2f]\n", s$etichetta,
                  s$n, s$eventi, s$or, s$lo, s$hi))
    }
  }

  # --- la probabilita' composta ----------------------------------------------
  # E' il numero da citare: cosa succede a un atleta a un dato percentile, seguendo il
  # percorso stadio per stadio.
  percentili <- c(50, 75, 90)
  medio <- mean(as.numeric(d$pct_U19y2))
  composte <- list()
  for (q in percentili) {
    x <- (q - medio) / PASSO
    prob <- c()
    for (s in stadi) {
      if (isTRUE(s$sottile)) {
        prob <- c(prob, NA_real_)
      } else {
        cf <- coef(s$fit)
        prob <- c(prob, plogis(cf[["(Intercept)"]] + cf[["pct10"]] * x))
      }
    }
    composte[[length(composte) + 1]] <- list(
      q, 100 * prob[1], 100 * prob[1] * prob[2],
      100 * prob[1] * prob[2] * prob[3])
    cat(sprintf("    al %d° percentile U19: pro %.1f%%, almeno top 500 %.1f%%, top 100 %.2f%%\n",
                q, composte[[length(composte)]][[2]],
                composte[[length(composte)]][[3]],
                composte[[length(composte)]][[4]]))
  }

  # --- modello secondario, condizionato all'Under 23 --------------------------
  d2 <- dbGetQuery(dd, "SELECT tier, pct_U19y2, pct_U23y1, birth_year FROM campione_b
                        WHERE present_U19y2 = 1 AND present_U23y1 = 1
                          AND pct_U19y2 IS NOT NULL AND pct_U23y1 IS NOT NULL
                          AND tier IS NOT NULL AND birth_year IS NOT NULL")
  or_u23 <- NULL
  if (nrow(d2) >= 100) {
    d2$livello_f <- factor(as.integer(d2$tier), levels = 0:3, labels = ETICHETTE,
                           ordered = TRUE)
    d2$a <- (as.numeric(d2$pct_U19y2) - mean(as.numeric(d2$pct_U19y2))) / PASSO
    d2$b <- (as.numeric(d2$pct_U23y1) - mean(as.numeric(d2$pct_U23y1))) / PASSO
    d2$coorte <- d2$birth_year - mean(d2$birth_year)
    o2 <- MASS::polr(livello_f ~ a + b + coorte, data = d2, Hess = TRUE)
    se2 <- sqrt(diag(vcov(o2)))
    or_u23 <- list(n = nrow(d2),
                   u19 = exp(coef(o2)[["a"]]), u23 = exp(coef(o2)[["b"]]),
                   p_u19 = 2 * pnorm(-abs(coef(o2)[["a"]] / se2[["a"]])),
                   p_u23 = 2 * pnorm(-abs(coef(o2)[["b"]] / se2[["b"]])))
    cat(sprintf("\n  modello condizionato (n=%d, presenti in Under 23): U19 OR=%.2f, U23 OR=%.2f\n",
                or_u23$n, or_u23$u19, or_u23$u23))
  }

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(ar, "livelli",
                 lapply(0:3, function(i) list(ETICHETTE[i + 1],
                                              conteggi[[as.character(i)]])),
                 c("livello raggiunto", "atleti"),
                 titolo = "Fin dove si arriva",
                 nota = paste("solo gli atleti presenti nella classifica Under 19",
                              "secondo anno, che comprendono 140 dei 145 professionisti",
                              "delle coorti"))

  scrivi_tabella(ar, "soglie", soglie,
                 c("soglia", "casi", "odds ratio", "ic_lo", "ic_hi"),
                 titolo = "Le tre soglie stimate separatamente",
                 nota = paste("se il modello ordinale e' appropriato questi tre",
                              "coefficienti devono somigliarsi: e' il controllo",
                              "dell'assunzione di odds proporzionali"))

  scrivi_tabella(ar, "stadi",
                 lapply(stadi, function(s) if (isTRUE(s$sottile))
                   list(s$etichetta, s$n, s$eventi, NULL, NULL, NULL)
                   else list(s$etichetta, s$n, s$eventi, s$or, s$lo, s$hi)),
                 c("passaggio", "chi ci prova", "chi ci riesce", "odds ratio",
                   "ic_lo", "ic_hi"),
                 titolo = "Il percorso, stadio per stadio",
                 nota = paste("ogni riga e' condizionata alla precedente: il secondo",
                              "coefficiente vale fra i professionisti, il terzo fra i",
                              "top 500"))

  scrivi_tabella(ar, "composte", composte,
                 c("percentile in Under 19", "professionista", "almeno top 500",
                   "top 100"),
                 titolo = "Dove si arriva, partendo da un dato percentile",
                 nota = paste("probabilita' composta lungo i tre stadi; sono previsioni",
                              "del modello, non frequenze osservate"))

  # Griglia fine per la figura: la stessa catena di probabilita', su tutta la scala.
  griglia <- list()
  for (q in seq(10, 99, by = 1)) {
    x <- (q - medio) / PASSO
    prob <- sapply(stadi, function(s) {
      if (isTRUE(s$sottile)) return(NA_real_)
      cf <- coef(s$fit)
      plogis(cf[["(Intercept)"]] + cf[["pct10"]] * x)
    })
    griglia[[length(griglia) + 1]] <- list(
      q, 100 * prob[1], 100 * prob[1] * prob[2],
      100 * prob[1] * prob[2] * prob[3])
  }
  scrivi_tabella(ar, "curve", griglia,
                 c("percentile", "professionista", "almeno top 500", "top 100"),
                 titolo = "La catena delle probabilita', su tutta la scala")

  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_b[1], conf$coorti_b[2]))
  scrivi_valore(ar, "n", nrow(d))
  scrivi_valore(ar, "passo", PASSO)
  scrivi_valore(ar, "ordinale", list(or = round(or_ord, 2),
                                     lo = round(ic_ord[1], 2),
                                     hi = round(ic_ord[2], 2), p = p_ord))
  scrivi_valore(ar, "divario_soglie", round(divario, 2),
                "rapporto fra il maggiore e il minore dei tre odds ratio di soglia")
  if (!is.null(or_u23)) {
    scrivi_valore(ar, "condizionato",
                  list(n = or_u23$n, u19 = round(or_u23$u19, 2),
                       u23 = round(or_u23$u23, 2),
                       p_u19 = or_u23$p_u19, p_u23 = or_u23$p_u23))
  }

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
