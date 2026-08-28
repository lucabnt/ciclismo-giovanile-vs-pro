# STEP 24 e 25 — quanto di questi risultati sopravvive fuori dai dati che li hanno
# prodotti.
#
# IL PROBLEMA
#     Un modello stimato su un campione e misurato sullo stesso campione si giudica da
#     solo, e si giudica bene. Una parte della sua bravura e' vera, un'altra e'
#     adattamento al rumore di quelle particolari duemila righe. Le due parti non si
#     distinguono guardando il numero: servono procedure apposta.
#
# STEP 24 — LA CORREZIONE DELL'OTTIMISMO
#     Si ricampiona con reimmissione, si ristima il modello sul campione estratto e si
#     misura la sua AUC due volte: sul campione che lo ha addestrato e sui dati
#     originali. La differenza fra le due e' l'**ottimismo** di quella ripetizione. La
#     media degli ottimismi si sottrae all'AUC apparente.
#
#     Harrell, Lee e Mark (1996), "Multivariable prognostic models", Statistics in
#     Medicine 15:361-387. La procedura e' quella di `rms::validate`, riscritta qui in
#     una trentina di righe per non aggiungere una dipendenza pesante e perche' scritta
#     in chiaro si capisce cosa fa.
#
#     Si riporta anche la **pendenza di calibrazione**: si ristima il modello sui dati
#     originali usando come unico predittore il punteggio previsto. Se vale 1 le
#     probabilita' previste sono nella scala giusta; se vale meno di 1 il modello e'
#     troppo sicuro di se', ed e' il sintomo tipico del sovradattamento.
#
# STEP 25 — LA VALIDAZIONE TEMPORALE
#     Il ricampionamento verifica la stabilita' interna, non la generalizzabilita'. Per
#     quella si addestra sulle coorti piu' vecchie e si misura su quelle piu' recenti,
#     che e' anche il modo in cui il modello verrebbe usato davvero: si stima su chi ha
#     gia' finito il percorso e si applica a chi lo sta facendo.
#
#     Se la prestazione crolla non e' un fallimento da nascondere: significa che i
#     pattern cambiano nel tempo, ed e' un risultato.
#
# COSA SI VALIDA
#     I due modelli su cui il documento appoggia le sue affermazioni pratiche: quello
#     con il solo percentile Under 19, da cui escono le probabilita' composte, e quello
#     con livello e pendenza della traiettoria, che e' il piu' accurato.
#
# USO
#     Rscript R/24_validazione.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "logistf", "pROC", "lme4"))

suppressPackageStartupMessages({
  library(logistf)
  library(pROC)
  library(lme4)
})

source("R/lib_risultati.R")

MODULO <- "validazione"
PASSO <- 10
B <- 500           # ripetizioni bootstrap
ETA_MAX_TRAIETTORIA <- 18
set.seed(20260828) # la validazione deve dare lo stesso numero a ogni rigenerazione


auc_di <- function(y, punteggio) {
  as.numeric(pROC::auc(pROC::roc(y, punteggio, quiet = TRUE, direction = "<")))
}


# L'ottimismo, secondo Harrell: quanto il modello si giudica meglio di quanto sia.
ottimismo <- function(dati, formula, b = B) {
  fit <- logistf(formula, data = dati)
  apparente <- auc_di(dati$PRO, fit$predict)

  # Pendenza di calibrazione: si rigetta il punteggio previsto dentro una logistica.
  # Meno di 1 significa previsioni troppo estreme.
  lp <- log(pmax(fit$predict, 1e-9) / pmax(1 - fit$predict, 1e-9))
  pend <- coef(glm(dati$PRO ~ lp, family = binomial()))[[2]]

  scarti <- numeric(0)
  scarti_pend <- numeric(0)
  for (i in seq_len(b)) {
    idx <- sample(nrow(dati), replace = TRUE)
    d2 <- dati[idx, ]
    if (length(unique(d2$PRO)) < 2) next
    f2 <- try(logistf(formula, data = d2), silent = TRUE)
    if (inherits(f2, "try-error")) next
    # AUC sul campione che ha addestrato, e sugli originali.
    p_orig <- as.vector(predict(f2, newdata = dati, type = "response"))
    a_boot <- auc_di(d2$PRO, f2$predict)
    a_orig <- auc_di(dati$PRO, p_orig)
    scarti <- c(scarti, a_boot - a_orig)

    lp2 <- log(pmax(p_orig, 1e-9) / pmax(1 - p_orig, 1e-9))
    s2 <- try(coef(glm(dati$PRO ~ lp2, family = binomial()))[[2]], silent = TRUE)
    if (!inherits(s2, "try-error")) scarti_pend <- c(scarti_pend, 1 - s2)
  }
  list(apparente = apparente,
       ottimismo = mean(scarti),
       corretta = apparente - mean(scarti),
       pendenza = pend,
       pendenza_corretta = pend - mean(scarti_pend),
       ripetizioni = length(scarti))
}


# Le traiettorie: si ricalcolano qui perche' la validazione temporale deve poterle
# stimare sulle sole coorti di addestramento.
traiettorie <- function(dd, coorti = NULL) {
  filtro <- if (is.null(coorti)) "" else
    sprintf(" AND c.birth_year BETWEEN %d AND %d", coorti[1], coorti[2])
  d <- dbGetQuery(dd, sprintf(
    "SELECT p.athlete_id, p.eta, p.pct FROM panello p
       JOIN campione c ON c.athlete_id = p.athlete_id
      WHERE p.eta <= %d AND p.presente = 1 AND p.pct IS NOT NULL%s",
    ETA_MAX_TRAIETTORIA, filtro))
  if (nrow(d) == 0) return(NULL)
  d$eta_c <- d$eta - mean(d$eta)
  m <- lmer(pct ~ eta_c + (eta_c | athlete_id), data = d,
            control = lmerControl(calc.derivs = FALSE))
  re <- coef(m)$athlete_id
  n_oss <- as.data.frame(table(d$athlete_id), stringsAsFactors = FALSE)
  names(n_oss) <- c("athlete_id", "stagioni")
  merge(data.frame(athlete_id = rownames(re), livello = re[, "(Intercept)"],
                   pendenza = re[, "eta_c"], stringsAsFactors = FALSE),
        n_oss, by = "athlete_id")
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)

  camp <- dbGetQuery(dd, "SELECT athlete_id, PRO, birth_year, pct_U19y2, present_U19y2
                          FROM campione WHERE PRO IS NOT NULL AND birth_year IS NOT NULL")

  cat(sprintf("STEP 24-25 — validazione, coorti %d-%d, %d ripetizioni bootstrap\n",
              conf$coorti_a_c[1], conf$coorti_a_c[2], B))

  # --- modello 1: il percentile Under 19 -------------------------------------
  d1 <- camp[camp$present_U19y2 == 1 & !is.na(camp$pct_U19y2), ]
  d1$pct10 <- (d1$pct_U19y2 - mean(d1$pct_U19y2)) / PASSO
  d1$coorte <- d1$birth_year - mean(d1$birth_year)
  o1 <- ottimismo(d1, PRO ~ pct10 + coorte)
  cat(sprintf("\n  Under 19: n=%d, eventi=%d\n", nrow(d1), sum(d1$PRO)))
  cat(sprintf("    AUC apparente %.3f, ottimismo %.3f, corretta %.3f\n",
              o1$apparente, o1$ottimismo, o1$corretta))
  cat(sprintf("    pendenza di calibrazione %.2f (corretta %.2f)\n",
              o1$pendenza, o1$pendenza_corretta))

  # --- modello 2: livello e pendenza della traiettoria ------------------------
  tr <- traiettorie(dd)
  d2 <- merge(tr[tr$stagioni >= 2, ], camp, by = "athlete_id")
  d2$livello10 <- (d2$livello - mean(d2$livello)) / PASSO
  d2$pendenza_sd <- d2$pendenza / sd(d2$pendenza)
  d2$coorte <- d2$birth_year - mean(d2$birth_year)
  o2 <- ottimismo(d2, PRO ~ livello10 + pendenza_sd + coorte)
  cat(sprintf("\n  traiettorie: n=%d, eventi=%d\n", nrow(d2), sum(d2$PRO)))
  cat(sprintf("    AUC apparente %.3f, ottimismo %.3f, corretta %.3f\n",
              o2$apparente, o2$ottimismo, o2$corretta))
  cat(sprintf("    pendenza di calibrazione %.2f (corretta %.2f)\n",
              o2$pendenza, o2$pendenza_corretta))

  # --- STEP 25: validazione temporale ----------------------------------------
  anni <- sort(unique(camp$birth_year))
  taglio <- anni[ceiling(length(anni) / 2)]
  cat(sprintf("\n  validazione temporale: addestramento su %d-%d, verifica su %d-%d\n",
              min(anni), taglio, taglio + 1, max(anni)))

  temporale <- list()
  # Il percentile Under 19 non richiede di ristimare nulla di preliminare.
  tr_a <- d1[d1$birth_year <= taglio, ]
  te_a <- d1[d1$birth_year > taglio, ]
  f_a <- logistf(PRO ~ pct10, data = tr_a)
  p_a <- as.vector(predict(f_a, newdata = te_a, type = "response"))
  temporale[[1]] <- list("percentile Under 19", nrow(tr_a), sum(tr_a$PRO),
                         nrow(te_a), sum(te_a$PRO),
                         auc_di(tr_a$PRO, f_a$predict), auc_di(te_a$PRO, p_a))

  # Le traiettorie invece vanno ristimate sulle sole coorti di addestramento: usare i
  # valori stimati su tutti significherebbe far vedere al modello anche le coorti di
  # verifica, che e' precisamente cio' che questa prova deve escludere.
  tr_train <- traiettorie(dd, c(min(anni), taglio))
  if (!is.null(tr_train)) {
    a <- merge(tr_train[tr_train$stagioni >= 2, ], camp, by = "athlete_id")
    a <- a[a$birth_year <= taglio, ]
    a$livello10 <- (a$livello - mean(a$livello)) / PASSO
    sd_p <- sd(a$pendenza)
    a$pendenza_sd <- a$pendenza / sd_p
    f_b <- logistf(PRO ~ livello10 + pendenza_sd, data = a)

    b_ <- d2[d2$birth_year > taglio, ]
    b_$livello10 <- (b_$livello - mean(a$livello)) / PASSO
    b_$pendenza_sd <- b_$pendenza / sd_p
    p_b <- as.vector(predict(f_b, newdata = b_, type = "response"))
    temporale[[2]] <- list("livello e pendenza", nrow(a), sum(a$PRO),
                           nrow(b_), sum(b_$PRO),
                           auc_di(a$PRO, f_b$predict), auc_di(b_$PRO, p_b))
  }
  for (t in temporale) {
    cat(sprintf("    %-22s addestramento %d/%d AUC %.3f -> verifica %d/%d AUC %.3f\n",
                t[[1]], t[[3]], t[[2]], t[[6]], t[[5]], t[[4]], t[[7]]))
  }

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(
    ar, "ottimismo",
    list(list("solo percentile Under 19", nrow(d1), sum(d1$PRO), o1$apparente,
              o1$ottimismo, o1$corretta, o1$pendenza),
         list("livello e pendenza della traiettoria", nrow(d2), sum(d2$PRO),
              o2$apparente, o2$ottimismo, o2$corretta, o2$pendenza)),
    c("modello", "atleti", "eventi", "auc_apparente", "ottimismo", "auc_corretta",
      "pendenza_calibrazione"),
    titolo = "Correzione dell'ottimismo con bootstrap",
    nota = sprintf(paste("%d ricampionamenti; l'ottimismo e' quanto il modello si",
                         "giudica meglio di quanto sia, e va sottratto"), B))

  scrivi_tabella(
    ar, "temporale", temporale,
    c("modello", "atleti addestramento", "eventi addestramento", "atleti verifica",
      "eventi verifica", "auc_addestramento", "auc_verifica"),
    titolo = "Validazione temporale",
    nota = sprintf(paste("addestramento sulle coorti %d-%d, verifica sulle %d-%d:",
                         "e' il modo in cui il modello verrebbe usato davvero"),
                   min(anni), taglio, taglio + 1, max(anni)))

  scrivi_valore(ar, "ripetizioni", B)
  scrivi_valore(ar, "taglio_temporale", c(min(anni), taglio, max(anni)))
  scrivi_valore(ar, "ottimismo_massimo",
                round(max(o1$ottimismo, o2$ottimismo), 3))
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
