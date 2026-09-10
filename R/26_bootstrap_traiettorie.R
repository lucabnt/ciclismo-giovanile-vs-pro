# STEP 26 — l'incertezza che lo STEP 24 non misura: il bootstrap a due stadi.
#
# IL PROBLEMA
#     Il modello con livello e pendenza si stima in due tempi. Prima un modello misto
#     legge le traiettorie individuali e assegna a ogni atleta un livello e una pendenza;
#     poi una logistica lega quei due numeri all'esito. Il punto e' che livello e
#     pendenza non sono osservati: sono stime, e per chi ha poche stagioni sono stime
#     incerte, tirate verso la media dallo shrinkage.
#
#     Lo STEP 24 ricampiona soltanto il secondo tempo. Il modello misto viene stimato
#     una volta sola, fuori dal ciclo, e le sue uscite entrano nel bootstrap come se
#     fossero colonne di dati osservati. L'ottimismo che ne esce (0,001) e' quindi
#     l'ottimismo del solo secondo stadio: l'incertezza del primo non c'e'.
#
#     Non e' un difetto grave — il primo stadio non vede mai l'esito, quindi non puo'
#     adattarsi ad esso — ma gli intervalli riportati sono piu' stretti del vero, e il
#     post 5 poggia interamente su quel modello. Questo script misura di quanto.
#
# COSA FA
#     Un bootstrap per grappoli sull'intera procedura. A ogni ripetizione:
#
#     1. si estraggono con reimmissione gli atleti (non le righe: le stagioni di uno
#        stesso atleta sono correlate, e vanno prese o lasciate insieme). Un atleta
#        estratto due volte diventa due atleti distinti, altrimenti il modello misto lo
#        tratterebbe come uno solo con il doppio delle stagioni;
#     2. si ristima il modello misto sul campione estratto — questo e' il pezzo che lo
#        STEP 24 non fa;
#     3. si ristima la logistica sulle stime del punto 2;
#     4. si applicano i parametri di quella ripetizione ai dati ORIGINALI, ricalcolando
#        i BLUP degli atleti veri con le componenti di varianza della ripetizione, e si
#        misura l'AUC anche li'.
#
#     La differenza fra l'AUC sul campione estratto e quella sugli originali e'
#     l'ottimismo di quella ripetizione, esattamente come nello STEP 24, ma con il primo
#     stadio dentro il ciclo. La distribuzione dei coefficienti fra le ripetizioni da'
#     inoltre intervalli percentili che comprendono l'incertezza delle traiettorie.
#
# PERCHE' I BLUP SI RICALCOLANO A MANO
#     Serve applicare il modello misto di una ripetizione agli atleti originali. Per un
#     modello con intercetta e pendenza casuali la formula chiusa e' breve:
#
#         b_i = D Z_i' (Z_i D Z_i' + sigma^2 I)^(-1) (y_i - X_i beta)
#
#     con D matrice 2x2 delle varianze degli effetti casuali, sigma^2 varianza residua,
#     Z_i = X_i = [1, eta_c]. Le matrici sono minuscole (al massimo 6 stagioni), quindi
#     costa poco, ed e' esattamente quello che `lme4` calcola internamente. Rifare
#     girare `lmer` sugli originali con i parametri bloccati sarebbe piu' fragile.
#
# USO
#     Rscript R/26_bootstrap_traiettorie.R            # 500 ripetizioni, circa 5 minuti
#     Rscript R/26_bootstrap_traiettorie.R 20         # una prova breve, una ventina di secondi
#
#     Il numero di ripetizioni e' l'unico argomento e vale 500 per difetto, come lo
#     STEP 24, cosi' i due ottimismi si confrontano a parita' di ricampionamenti.
#
#     Scrive nel modulo 'bootstrap_traiettorie' dell'archivio. Non tocca il modulo
#     'validazione': i due risultati convivono e il documento li mette a confronto.
#     Se il modulo non c'e', il documento si genera lo stesso e la sezione dice che
#     manca, con il comando per ottenerla.
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "logistf", "pROC", "lme4"))

suppressPackageStartupMessages({
  library(logistf)
  library(pROC)
  library(lme4)
})

source("R/lib_risultati.R")

MODULO <- "bootstrap_traiettorie"
PASSO <- 10
ETA_MAX <- 18
MIN_STAGIONI <- 2
set.seed(20260910)   # come per la validazione: lo stesso comando da' lo stesso numero

args <- commandArgs(trailingOnly = TRUE)
B <- if (length(args) >= 1) as.integer(args[1]) else 500


auc_di <- function(y, punteggio) {
  as.numeric(pROC::auc(pROC::roc(y, punteggio, quiet = TRUE, direction = "<")))
}


# Il pannello: una riga per atleta e stagione, fino ai diciotto anni.
leggi_pannello <- function(dd) {
  d <- dbGetQuery(dd, sprintf(
    "SELECT p.athlete_id, p.eta, p.pct FROM panello p
       JOIN campione c ON c.athlete_id = p.athlete_id
      WHERE p.eta <= %d AND p.presente = 1 AND p.pct IS NOT NULL", ETA_MAX))
  d$athlete_id <- as.character(d$athlete_id)
  d
}


# Stima il modello misto e restituisce, oltre alle traiettorie, i parametri che
# servono per applicarlo ad altri atleti.
stadio_uno <- function(pannello, centro) {
  d <- pannello
  d$eta_c <- d$eta - centro
  m <- lmer(pct ~ eta_c + (eta_c | athlete_id), data = d,
            control = lmerControl(calc.derivs = FALSE))
  vc <- VarCorr(m)$athlete_id
  list(beta = fixef(m),
       D = matrix(as.numeric(vc), 2, 2),
       sigma2 = sigma(m) ^ 2,
       re = coef(m)$athlete_id)
}


# I BLUP di atleti qualsiasi sotto i parametri di un modello gia' stimato.
# Restituisce livello e pendenza, cioe' effetto fisso piu' effetto casuale.
blup <- function(par, pannello, centro) {
  d <- pannello
  d$eta_c <- d$eta - centro
  ordine <- order(d$athlete_id)
  d <- d[ordine, ]
  taglio <- rle(d$athlete_id)
  fine <- cumsum(taglio$lengths)
  inizio <- fine - taglio$lengths + 1L

  livello <- numeric(length(taglio$values))
  pendenza <- numeric(length(taglio$values))
  for (k in seq_along(taglio$values)) {
    righe <- inizio[k]:fine[k]
    Z <- cbind(1, d$eta_c[righe])
    r <- d$pct[righe] - as.vector(Z %*% par$beta)
    V <- Z %*% par$D %*% t(Z)
    diag(V) <- diag(V) + par$sigma2
    b <- par$D %*% t(Z) %*% solve(V, r)
    livello[k] <- par$beta[[1]] + b[1]
    pendenza[k] <- par$beta[[2]] + b[2]
  }
  data.frame(athlete_id = taglio$values, livello = livello, pendenza = pendenza,
             stagioni = taglio$lengths, stringsAsFactors = FALSE)
}


# Il secondo stadio, con la standardizzazione che usa il resto del progetto.
stadio_due <- function(tr, camp, riferimento = NULL) {
  d <- merge(tr[tr$stagioni >= MIN_STAGIONI, ], camp, by = "athlete_id")
  if (nrow(d) == 0 || length(unique(d$PRO)) < 2) return(NULL)
  rif <- if (is.null(riferimento))
    list(m_liv = mean(d$livello), sd_pend = sd(d$pendenza),
         m_coorte = mean(d$birth_year)) else riferimento
  d$livello10 <- (d$livello - rif$m_liv) / PASSO
  d$pendenza_sd <- d$pendenza / rif$sd_pend
  d$coorte <- d$birth_year - rif$m_coorte
  fit <- try(logistf(PRO ~ livello10 + pendenza_sd + coorte, data = d), silent = TRUE)
  if (inherits(fit, "try-error")) return(NULL)
  list(fit = fit, dati = d, riferimento = rif)
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)

  camp <- dbGetQuery(dd, "SELECT athlete_id, PRO, birth_year FROM campione
                          WHERE PRO IS NOT NULL AND birth_year IS NOT NULL")
  camp$athlete_id <- as.character(camp$athlete_id)

  pannello <- leggi_pannello(dd)
  centro <- mean(pannello$eta)
  atleti <- unique(pannello$athlete_id)
  # Diviso una volta sola: rifiltrare il pannello atleta per atleta a ogni
  # ripetizione costerebbe piu' del modello misto.
  per_atleta <- split(pannello, pannello$athlete_id)

  cat(sprintf("STEP 26 — bootstrap a due stadi, %d ripetizioni su %d atleti\n",
              B, length(atleti)))
  cat("   ogni ripetizione ristima anche il modello misto: e' il passo lento.\n")

  # --- il modello sui dati veri, che e' il termine di paragone ---------------
  p0 <- stadio_uno(pannello, centro)
  tr0 <- blup(p0, pannello, centro)
  s0 <- stadio_due(tr0, camp)
  if (is.null(s0)) stop("Il modello di riferimento non si stima: controllare i dati.")
  auc0 <- auc_di(s0$dati$PRO, s0$fit$predict)
  or0 <- exp(coef(s0$fit))
  cat(sprintf("   riferimento: n=%d, eventi=%d, AUC %.3f, OR livello %.2f, OR pendenza %.2f\n",
              nrow(s0$dati), sum(s0$dati$PRO), auc0,
              or0[["livello10"]], or0[["pendenza_sd"]]))

  # Controllo: i BLUP ricalcolati a mano devono coincidere con quelli di lme4.
  # coef() restituisce gia' effetto fisso piu' casuale: si confronta con quello.
  scarto <- max(abs(tr0$pendenza -
                    p0$re[match(tr0$athlete_id, rownames(p0$re)), "eta_c"]))
  cat(sprintf("   controllo BLUP ricalcolati contro lme4: scarto massimo %.2e\n", scarto))
  if (scarto > 1e-6) {
    cat("   ATTENZIONE: i BLUP ricalcolati non coincidono con quelli del modello.\n")
    cat("   Il resto dei numeri non e' affidabile finche' questo non torna.\n")
  }

  # --- il ciclo ---------------------------------------------------------------
  or_liv <- numeric(0); or_pen <- numeric(0)
  auc_boot <- numeric(0); auc_orig <- numeric(0)
  falliti <- 0
  inizio <- Sys.time()

  for (i in seq_len(B)) {
    estratti <- sample(atleti, length(atleti), replace = TRUE)
    # Un atleta estratto due volte deve diventare due grappoli distinti.
    pezzi <- per_atleta[estratti]
    for (j in seq_along(pezzi)) {
      pezzi[[j]]$athlete_id <- sprintf("%s#%d", estratti[j], j)
    }
    pb <- do.call(rbind, pezzi)
    mappa <- data.frame(athlete_id = sprintf("%s#%d", estratti, seq_along(estratti)),
                        vero = estratti, stringsAsFactors = FALSE)
    campb <- merge(mappa, camp, by.x = "vero", by.y = "athlete_id")
    campb <- campb[, c("athlete_id", "PRO", "birth_year")]

    par <- try(stadio_uno(pb, centro), silent = TRUE)
    if (inherits(par, "try-error")) {
      falliti <- falliti + 1
      if (falliti == 1) cat("   primo fallimento, primo stadio:", par, "\n")
      next
    }
    trb <- blup(par, pb, centro)
    sb <- stadio_due(trb, campb)
    if (is.null(sb)) {
      falliti <- falliti + 1
      if (falliti == 1) cat("   primo fallimento: il secondo stadio non si stima\n")
      next
    }

    # Gli stessi parametri applicati agli atleti veri: primo stadio compreso.
    tro <- blup(par, pannello, centro)
    so <- stadio_due(tro, camp, riferimento = sb$riferimento)
    if (is.null(so)) {
      falliti <- falliti + 1
      if (falliti == 1) cat("   primo fallimento: il modello della ripetizione non si applica agli originali
")
      next
    }
    p_orig <- as.vector(predict(sb$fit, newdata = so$dati, type = "response"))

    ors <- exp(coef(sb$fit))
    or_liv <- c(or_liv, ors[["livello10"]])
    or_pen <- c(or_pen, ors[["pendenza_sd"]])
    auc_boot <- c(auc_boot, auc_di(sb$dati$PRO, sb$fit$predict))
    auc_orig <- c(auc_orig, auc_di(so$dati$PRO, p_orig))

    if (i %% 10 == 0 || i == B) {
      trascorso <- as.numeric(difftime(Sys.time(), inizio, units = "mins"))
      cat(sprintf("   %4d/%d  %.1f min trascorsi, ~%.1f alla fine\n",
                  i, B, trascorso, trascorso / i * (B - i)))
    }
  }

  riuscite <- length(auc_boot)
  # La soglia si adatta alla prova breve: con B piccolo si sta solo controllando che
  # lo script giri, con B grande un tasso di fallimenti alto e' un problema vero.
  if (riuscite < max(1L, as.integer(B * 0.5)))
    stop(sprintf("Solo %d ripetizioni su %d sono riuscite: il risultato non e' utilizzabile.",
                 riuscite, B))

  ott <- mean(auc_boot - auc_orig)
  q <- function(x) unname(quantile(x, c(0.025, 0.975)))
  ic_liv <- q(or_liv); ic_pen <- q(or_pen)

  cat(sprintf("\n   riuscite %d su %d (%d fallite)\n", riuscite, B, falliti))
  cat(sprintf("   ottimismo a due stadi %.4f  ->  AUC corretta %.3f\n", ott, auc0 - ott))
  cat(sprintf("   OR livello  %.2f  IC 95%% %.2f-%.2f\n", or0[["livello10"]],
              ic_liv[1], ic_liv[2]))
  cat(sprintf("   OR pendenza %.2f  IC 95%% %.2f-%.2f\n", or0[["pendenza_sd"]],
              ic_pen[1], ic_pen[2]))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)
  scrivi_valore(ar, "ripetizioni", riuscite)
  scrivi_valore(ar, "ripetizioni_chieste", B)
  scrivi_valore(ar, "auc_apparente", round(auc0, 3))
  scrivi_valore(ar, "ottimismo", round(ott, 4),
                "ottimismo con il modello misto dentro il ciclo di ricampionamento")
  scrivi_valore(ar, "auc_corretta", round(auc0 - ott, 3))
  scrivi_tabella(
    ar, "coefficienti",
    list(list("livello: dieci punti di percentile in piu'", round(or0[["livello10"]], 2),
              round(ic_liv[1], 2), round(ic_liv[2], 2)),
         list("pendenza: una deviazione standard di miglioramento annuo",
              round(or0[["pendenza_sd"]], 2), round(ic_pen[1], 2), round(ic_pen[2], 2))),
    c("variabile", "odds ratio", "ic_basso", "ic_alto"),
    titolo = "Odds ratio con intervalli che comprendono l'incertezza delle traiettorie",
    nota = paste("intervalli percentili del bootstrap per grappoli: a ogni ripetizione",
                 "si ristima anche il modello misto, quindi l'incertezza delle pendenze",
                 "stimate e' dentro l'intervallo e non fuori"))
  scrivi_valore(ar, "eta_riferimento", round(centro, 1))
  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
