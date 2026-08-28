# STEP 21 — conta il livello o il miglioramento?
#
# LA DOMANDA, CHE E' QUELLA DEGLI ALLENATORI
#     Un ragazzo che passa dal 40esimo al 90esimo percentile in tre anni e' piu'
#     promettente di uno stabile al 75esimo? La domanda si sente in ogni societa', e i
#     dati longitudinali sono lo strumento per affrontarla.
#
# COME SI SEPARA IL LIVELLO DALLA PENDENZA
#     A ogni atleta si adatta una retta: il suo percentile in funzione dell'eta'. Due
#     numeri riassumono la traiettoria — dove passa la retta (il livello) e quanto sale
#     o scende (la pendenza).
#
#     Non si fa pero' una regressione separata per atleta. Chi ha due sole stagioni
#     avrebbe una pendenza stimata su due punti, cioe' rumore. Il modello misto stima le
#     rette di tutti insieme e applica lo **shrinkage**: le stime individuali vengono
#     tirate verso la media della popolazione tanto piu' quanto meno dati ha quell'atleta.
#     Chi ha sei stagioni tiene quasi la propria pendenza, chi ne ha due viene tirato
#     molto verso il centro. E' il comportamento corretto, e viene fuori da solo dalla
#     struttura del modello.
#
# LA FINESTRA SI FERMA A DICIOTTO ANNI
#     La traiettoria si misura sulle sole categorie giovanili fino agli Juniores. Oltre
#     comincia l'Under 23, dove alcuni atleti sono gia' professionisti: includere quelle
#     stagioni significherebbe usare per prevedere l'esito delle osservazioni raccolte
#     **dopo** che l'esito si e' verificato.
#
# L'ARTEFATTO DA NON IGNORARE
#     Pendenza e livello sono correlati negativamente per costruzione: il percentile e'
#     limitato a 100, quindi chi parte alto ha meno spazio per salire. Per questo le due
#     variabili entrano **sempre insieme** nel modello dell'esito, e la loro correlazione
#     viene riportata invece che nascosta.
#
# USO
#     Rscript R/21_traiettorie.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "lme4", "logistf", "pROC"))

suppressPackageStartupMessages({
  library(lme4)
  library(logistf)
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "traiettorie"
ETA_MAX <- 18      # ultima stagione giovanile prima dell'Under 23
MIN_STAGIONI <- 2  # sotto due osservazioni non esiste una pendenza individuale


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)

  d <- dbGetQuery(dd, sprintf(
    "SELECT athlete_id, eta, pct, PRO FROM panello
     WHERE eta <= %d AND presente = 1 AND pct IS NOT NULL", ETA_MAX))
  if (nrow(d) == 0) stop("Nessuna osservazione: eseguire 08_prepara_modelli.py")

  quante <- table(table(d$athlete_id))
  cat(sprintf("STEP 21 — traiettorie individuali, coorti %d-%d\n",
              conf$coorti_a_c[1], conf$coorti_a_c[2]))
  cat(sprintf("  %d osservazioni su %d atleti, eta' fino a %d\n",
              nrow(d), length(unique(d$athlete_id)), ETA_MAX))
  cat("  stagioni osservate per atleta: ")
  cat(paste(sprintf("%s->%d", names(quante), as.integer(quante)), collapse = "  "))
  cat("\n")

  # Eta' centrata sulla media: l'intercetta diventa «il livello a meta' del percorso
  # giovanile» invece che «il livello a zero anni», che non vuol dire niente.
  eta_rif <- mean(d$eta)
  d$eta_c <- d$eta - eta_rif

  m <- lmer(pct ~ eta_c + (eta_c | athlete_id), data = d,
            control = lmerControl(calc.derivs = FALSE))
  fissi <- fixef(m)
  vc <- VarCorr(m)$athlete_id
  cat(sprintf("\n  effetti fissi: livello medio %.1f, pendenza media %+.2f punti l'anno\n",
              fissi[["(Intercept)"]], fissi[["eta_c"]]))
  cat(sprintf("  variabilita' fra atleti: livello %.1f, pendenza %.2f, correlazione %+.2f\n",
              sqrt(vc[1, 1]), sqrt(vc[2, 2]), attr(vc, "correlation")[1, 2]))

  re <- coef(m)$athlete_id
  # Gli identificativi sono stringhe anonimizzate, non numeri: convertirli produrrebbe
  # solo NA silenziosi.
  traj <- data.frame(athlete_id = rownames(re),
                     livello = re[, "(Intercept)"],
                     pendenza = re[, "eta_c"],
                     stringsAsFactors = FALSE)
  n_oss <- as.data.frame(table(d$athlete_id), stringsAsFactors = FALSE)
  names(n_oss) <- c("athlete_id", "stagioni")
  traj <- merge(traj, n_oss, by = "athlete_id")

  # L'esito. Solo chi ha almeno due stagioni: con una sola la pendenza individuale non
  # esiste, lo shrinkage la riporta esattamente alla media della popolazione e la riga
  # non porterebbe informazione sulla domanda che si sta facendo.
  camp <- dbGetQuery(dd, "SELECT athlete_id, PRO, birth_year FROM campione")
  dati <- merge(traj[traj$stagioni >= MIN_STAGIONI, ], camp, by = "athlete_id")
  dati <- dati[!is.na(dati$PRO) & !is.na(dati$birth_year), ]
  dati$coorte <- dati$birth_year - mean(dati$birth_year)
  # In unita' da dieci punti, come nel resto del documento.
  dati$livello10 <- (dati$livello - mean(dati$livello)) / 10
  # La pendenza si riporta in deviazioni standard, non in decine di punti: dieci punti
  # di percentile guadagnati ogni anno sono quasi quattro deviazioni standard, cioe' un
  # atleta che non esiste. Una deviazione standard e' un confronto che si puo' fare.
  sd_pend <- sd(dati$pendenza)
  dati$pendenza_sd <- dati$pendenza / sd_pend

  cat(sprintf("\n  modello dell'esito su %d atleti (%d professionisti)\n",
              nrow(dati), sum(dati$PRO)))

  solo_livello <- logistf(PRO ~ livello10 + coorte, data = dati)
  completo <- logistf(PRO ~ livello10 + pendenza_sd + coorte, data = dati)

  # Controllo: la pendenza potrebbe essere un travestimento della durata della carriera.
  # Chi ha piu' stagioni osservate ha una pendenza meno tirata verso la media, quindi
  # piu' estrema, e altrove in questo studio la durata della carriera si e' gia' rivelata
  # il vero motore di un gradiente apparente. Il controllo si fa e si riporta — anche se
  # il numero di stagioni e' a sua volta un mediatore, e infatti non entra nel modello
  # principale.
  con_durata <- logistf(PRO ~ livello10 + pendenza_sd + coorte + stagioni, data = dati)
  or_senza <- exp(unname(coef(completo)["pendenza_sd"]))
  or_con <- exp(unname(coef(con_durata)["pendenza_sd"]))
  estremita <- tapply(abs(dati$pendenza), dati$stagioni, mean)

  r1 <- pROC::roc(dati$PRO, solo_livello$predict, quiet = TRUE)
  r2 <- pROC::roc(dati$PRO, completo$predict, quiet = TRUE)
  auc1 <- as.numeric(pROC::auc(r1))
  auc2 <- as.numeric(pROC::auc(r2))
  p_delong <- tryCatch(
    pROC::roc.test(r1, r2, method = "delong", paired = TRUE)$p.value,
    error = function(e) NA_real_)

  righe <- list()
  for (nome in c("livello10", "pendenza_sd")) {
    b <- unname(coef(completo)[nome])
    lo <- completo$ci.lower[[nome]]
    hi <- completo$ci.upper[[nome]]
    righe[[length(righe) + 1]] <- list(
      switch(nome,
             livello10 = "livello: dieci punti di percentile in piu'",
             pendenza_sd = "pendenza: una deviazione standard di miglioramento annuo"),
      exp(b), exp(lo), exp(hi), unname(completo$prob[nome]))
    cat(sprintf("    %-11s OR=%.2f [%.2f-%.2f]  p=%.3g\n", nome, exp(b), exp(lo),
                exp(hi), unname(completo$prob[nome])))
  }
  cat(sprintf("\n  AUC solo livello %.3f, livello + pendenza %.3f, differenza %+.3f (DeLong p=%.3g)\n",
              auc1, auc2, auc2 - auc1, p_delong))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(ar, "coefficienti", righe,
                 c("variabile", "odds ratio", "ic_lo", "ic_hi", "p"),
                 titolo = "Livello e pendenza insieme nello stesso modello",
                 nota = paste("le due variabili entrano sempre insieme: sono correlate",
                              "per costruzione, perche' il percentile ha un soffitto a",
                              "100 e chi parte alto ha meno spazio per salire"))

  scrivi_tabella(ar, "stagioni",
                 lapply(seq_along(quante), function(i)
                   list(as.integer(names(quante)[i]), as.integer(quante[i]))),
                 c("stagioni osservate", "atleti"),
                 titolo = "Quante stagioni si osservano per atleta",
                 nota = paste("lo shrinkage del modello misto tira verso la media le",
                              "traiettorie stimate su poche stagioni: e' corretto, ma",
                              "va saputo che molte pendenze sono poco individuali"))

  scrivi_valore(ar, "eta_riferimento", round(eta_rif, 1))
  scrivi_valore(ar, "eta_massima", ETA_MAX)
  scrivi_valore(ar, "min_stagioni", MIN_STAGIONI)
  scrivi_valore(ar, "n_atleti", nrow(dati))
  scrivi_valore(ar, "n_eventi", sum(dati$PRO))
  scrivi_valore(ar, "n_osservazioni", nrow(d))
  scrivi_valore(ar, "pendenza_media", round(fissi[["eta_c"]], 2))
  scrivi_valore(ar, "sd_livello", round(sqrt(vc[1, 1]), 1))
  scrivi_valore(ar, "sd_pendenza", round(sqrt(vc[2, 2]), 2))
  scrivi_valore(ar, "correlazione_livello_pendenza",
                round(attr(vc, "correlation")[1, 2], 2),
                "negativa per costruzione: il percentile ha un soffitto")
  scrivi_valore(ar, "auc", list(livello = round(auc1, 3), completo = round(auc2, 3),
                                differenza = round(auc2 - auc1, 3),
                                p = p_delong))
  # La domanda «livello o miglioramento?» merita anche una risposta che si legga senza
  # sapere cosa sia un odds ratio: il tasso di professionismo incrociando i terzili delle
  # due dimensioni.
  terzili <- function(x) cut(x, breaks = quantile(x, c(0, 1/3, 2/3, 1)),
                             include.lowest = TRUE, labels = c("basso", "medio", "alto"))
  dati$t_liv <- terzili(dati$livello)
  dati$t_pen <- terzili(dati$pendenza)
  incrocio <- list()
  for (l in levels(dati$t_liv)) {
    for (pnd in levels(dati$t_pen)) {
      sel <- dati$t_liv == l & dati$t_pen == pnd
      n <- sum(sel)
      k <- sum(dati$PRO[sel])
      incrocio[[length(incrocio) + 1]] <- list(
        l, pnd, n, k, if (n > 0) 100 * k / n else NA_real_)
    }
  }
  scrivi_tabella(ar, "incrocio", incrocio,
                 c("livello", "pendenza", "atleti", "professionisti", "% pro"),
                 titolo = "Livello e miglioramento insieme",
                 nota = paste("terzili delle due dimensioni; il gradiente corre in",
                              "entrambe le direzioni, che e' il modo piu' diretto di",
                              "dire che contano tutte e due"))

  scrivi_valore(ar, "sd_pendenza_stimata", round(sd_pend, 2),
                "deviazione standard delle pendenze individuali stimate, in punti l'anno")
  scrivi_valore(ar, "controllo_durata",
                list(senza = round(or_senza, 2), con = round(or_con, 2)),
                "odds ratio della pendenza, senza e con il numero di stagioni osservate")
  scrivi_tabella(ar, "shrinkage",
                 lapply(seq_along(estremita), function(i)
                   list(as.integer(names(estremita)[i]), round(estremita[[i]], 2))),
                 c("stagioni osservate", "pendenza media in valore assoluto"),
                 titolo = "Lo shrinkage, visto sui dati",
                 nota = paste("chi ha poche stagioni riceve una pendenza vicina alla",
                              "media della popolazione: e' il comportamento corretto del",
                              "modello misto, non un difetto, ma va saputo"))
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
