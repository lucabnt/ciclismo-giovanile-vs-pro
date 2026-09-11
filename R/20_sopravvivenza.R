# STEP 20 — quando si diventa professionisti, e cosa lo rende piu' probabile.
#
# COSA AGGIUNGE RISPETTO AI MODELLI PRECEDENTI
#     Tre cose che gli altri non possono dare.
#
#     **Il tempo.** Fin qui la domanda era "diventera' professionista si' o no". Qui e'
#     "con quale probabilita' lo diventa **in questa stagione**, dato che non lo e'
#     ancora". La risposta e' una curva sull'eta', non un numero.
#
#     **Le coorti recenti.** Chi e' nato nel 2004 non ha finito la finestra dei
#     venticinque anni, e per questo era escluso da tutto il resto. Qui contribuisce le
#     stagioni gia' osservate ed esce dal rischio quando l'osservazione finisce: e'
#     la censura, ed e' cio' che quasi raddoppia il numero di eventi disponibili.
#
#     **Il rendimento che cambia.** Il predittore non e' piu' il percentile di una cella
#     fissa, ma quello della stagione precedente, che cambia di anno in anno insieme
#     all'atleta.
#
# PERCHE' cloglog E NON logit
#     Il legame complementare log-log deriva da un processo in tempo continuo osservato a
#     intervalli discreti — che e' esattamente la situazione: la decisione di ingaggiare
#     un corridore matura in un momento qualunque dell'anno, noi la vediamo per stagione.
#     Il suo coefficiente si legge come rapporto fra rischi (hazard ratio) e non dipende
#     dalla lunghezza dell'intervallo, cosa che per il logit non e' vera.
#
#     Il modello a tempo discreto con legame cloglog e' l'equivalente in tempo discreto
#     del modello a rischi proporzionali. Riferimento: Allison (1982), "Discrete-time
#     methods for the analysis of event histories", Sociological Methodology 13:61-98.
#
# GLI ERRORI STANDARD VANNO AGGIUSTATI
#     Ogni atleta compare in piu' righe, una per stagione, e quelle righe non sono
#     osservazioni indipendenti. Ignorarlo restringerebbe gli intervalli di confidenza di
#     una quantita' arbitraria. Si usa lo stimatore sandwich raggruppato per atleta,
#     calcolato qui a mano per non aggiungere una dipendenza per venti righe di codice.
#
# TRE STATI, NON DUE
#     Chi non era in classifica l'anno prima non ha un percentile. Metterlo a zero
#     equivarrebbe a dire che era l'ultimo, che e' una cosa diversa dal non esserci. Si
#     tiene quindi una variabile indicatrice separata, e il percentile degli assenti si
#     fissa alla media: cosi' il coefficiente del percentile parla dei soli presenti e
#     quello dell'indicatrice dice quanto pesa l'assenza in se'.
#
#     Ma gli stati sono tre, non due, ed e' un errore facile da fare: «assente dalla
#     classifica» e «classifica inesistente» non sono la stessa cosa. Il ranking
#     giovanile finisce con l'Under 23, cioe' a ventidue anni: per le stagioni successive
#     non esiste alcuna classifica da cui essere assenti. Confonderle metterebbe nel
#     gruppo degli assenti tutte le stagioni oltre i ventitre' anni, dove il predittore
#     e' semplicemente non osservato, e il modello attribuirebbe all'assenza cio' che e'
#     mancanza di dati.
#
#     La finestra del modello finisce quindi dove finisce il predittore. Gli eventi che
#     cadono oltre vengono contati e dichiarati, non silenziosamente inclusi.
#
# USO
#     Rscript R/20_sopravvivenza.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite"))    # splines e' di base

suppressPackageStartupMessages({
  library(splines)
})

source("R/lib_risultati.R")

MODULO <- "sopravvivenza"
PASSO <- 10        # i coefficienti si leggono per dieci punti di percentile


# Errori standard robusti al raggruppamento per atleta.
#
# Il sandwich: (X'WX)^-1 [ sum_g (X_g' u_g)(X_g' u_g)' ] (X'WX)^-1, dove u sono i
# contributi allo score. Per un modello lineare generalizzato lo score della riga i e'
# x_i (y_i - mu_i) (dmu/deta_i) / [mu_i (1 - mu_i)].
sandwich_cluster <- function(fit, gruppo) {
  X <- model.matrix(fit)
  mu <- fitted(fit)
  eta <- fit$linear.predictors
  y <- fit$y
  peso <- fit$family$mu.eta(eta) / (mu * (1 - mu))
  score <- X * as.vector((y - mu) * peso)
  per_gruppo <- rowsum(score, gruppo)
  pane <- summary(fit)$cov.unscaled
  carne <- crossprod(per_gruppo)
  v <- pane %*% carne %*% pane
  # Correzione per il numero di gruppi, come fa la convenzione CR1.
  g <- nrow(per_gruppo)
  n <- nrow(X)
  k <- ncol(X)
  v * (g / (g - 1)) * ((n - 1) / (n - k))
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  eta_min <- conf$eta_minima_pro
  eta_max <- conf$eta_massima_pro

  tutto <- dbGetQuery(dd, sprintf(
    "SELECT * FROM persona_anno WHERE eta BETWEEN %d AND %d", eta_min, eta_max))
  if (nrow(tutto) == 0) stop("Tabella persona_anno vuota: eseguire 08_prepara_modelli.py")

  # La finestra si chiude dove finisce il predittore, non dove finisce la finestra
  # dell'esito: oltre l'ultima eta' coperta dal ranking non c'e' nulla da osservare.
  eta_ultima <- max(tutto$eta[!is.na(tutto$cella_prec)])
  fuori <- sum(tutto$evento[tutto$eta > eta_ultima])
  d <- tutto[tutto$eta <= eta_ultima, ]

  cat(sprintf("STEP 20 — sopravvivenza a tempo discreto, coorti %d-%d\n",
              conf$coorti_sopravvivenza[1], conf$coorti_sopravvivenza[2]))
  cat(sprintf("  %d stagioni-atleta, %d atleti, %d eventi\n",
              nrow(d), length(unique(d$athlete_id)), sum(d$evento)))
  cat(sprintf(paste("  finestra %d-%d anni: oltre i %d il ranking giovanile non esiste",
                    "piu', quindi %d passaggi restano fuori dal modello\n"),
              eta_min, eta_ultima, eta_ultima, fuori))

  # L'assenza dalla classifica e' una categoria a se': il percentile degli assenti si
  # fissa alla media dei presenti, e a distinguerli ci pensa l'indicatrice.
  d$assente <- ifelse(d$presente_prec == 0, 1, 0)
  media_pct <- mean(d$pct_prec[d$assente == 0], na.rm = TRUE)
  d$pct <- ifelse(d$assente == 1, media_pct, d$pct_prec)
  d$pct[is.na(d$pct)] <- media_pct
  d$pct10 <- (d$pct - media_pct) / PASSO
  d$coorte <- d$birth_year - mean(d$birth_year)

  # Il rischio grezzo per eta', prima di qualunque modello: e' il dato, e va guardato.
  grezzo <- aggregate(cbind(rischio = rep(1, nrow(d)), eventi = d$evento),
                      by = list(eta = d$eta), FUN = sum)
  grezzo$hazard <- 1000 * grezzo$eventi / grezzo$rischio
  for (i in seq_len(nrow(grezzo))) {
    cat(sprintf("    %2d anni: a rischio %5d, eventi %3d, rischio %.1f per mille\n",
                grezzo$eta[i], grezzo$rischio[i], grezzo$eventi[i], grezzo$hazard[i]))
  }

  fit <- glm(evento ~ ns(eta, df = 3) + pct10 + assente + coorte,
             family = binomial(link = "cloglog"), data = d)
  v <- sandwich_cluster(fit, d$athlete_id)
  se <- sqrt(diag(v))
  coef_ <- coef(fit)

  righe <- list()
  for (nome in c("pct10", "assente", "coorte")) {
    b <- coef_[[nome]]
    s <- se[[which(names(coef_) == nome)]]
    z <- b / s
    righe[[length(righe) + 1]] <- list(
      nome, exp(b), exp(b - 1.96 * s), exp(b + 1.96 * s),
      2 * pnorm(-abs(z)))
  }
  cat("\n  rapporti fra rischi (hazard ratio), errori standard raggruppati per atleta:\n")
  for (r in righe) {
    cat(sprintf("    %-8s HR=%.3f [%.3f-%.3f]  p=%.3g\n", r[[1]], r[[2]], r[[3]],
                r[[4]], r[[5]]))
  }

  # La curva del rischio per eta', a parita' di tutto il resto: e' il risultato
  # principale, e si legge senza sapere cosa sia un cloglog.
  nuovo <- data.frame(eta = eta_min:eta_ultima, pct10 = 0, assente = 0, coorte = 0)
  X <- model.matrix(~ ns(eta, df = 3) + pct10 + assente + coorte, data = nuovo)
  lp <- as.vector(X %*% coef_)
  ee <- sqrt(rowSums((X %*% v) * X))
  curva <- data.frame(eta = nuovo$eta,
                      h = 1000 * (1 - exp(-exp(lp))),
                      lo = 1000 * (1 - exp(-exp(lp - 1.96 * ee))),
                      hi = 1000 * (1 - exp(-exp(lp + 1.96 * ee))))

  # Cosa vuol dire, in pratica: probabilita' cumulata di arrivare al professionismo
  # entro i 25 anni per due profili di rendimento, tenendo il resto fermo.
  cumulata <- function(delta_pct10) {
    n2 <- data.frame(eta = eta_min:eta_ultima, pct10 = delta_pct10, assente = 0,
                     coorte = 0)
    X2 <- model.matrix(~ ns(eta, df = 3) + pct10 + assente + coorte, data = n2)
    h <- 1 - exp(-exp(as.vector(X2 %*% coef_)))
    1 - prod(1 - h)
  }
  # +2 e -2 in unita' da dieci punti: venti punti di percentile sopra e sotto la media.
  p_alto <- cumulata(2)
  p_medio <- cumulata(0)
  p_basso <- cumulata(-2)
  cat(sprintf(paste("\n  probabilita' cumulata entro i %d anni, per chi resta in",
                    "classifica ogni stagione:\n    %.1f%% venti punti sopra la media,",
                    "%.1f%% alla media, %.1f%% venti punti sotto\n"),
              eta_ultima, 100 * p_alto, 100 * p_medio, 100 * p_basso))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(ar, "hazard_grezzo",
                 lapply(seq_len(nrow(grezzo)), function(i)
                   list(grezzo$eta[i], grezzo$rischio[i], grezzo$eventi[i],
                        grezzo$hazard[i])),
                 c("eta", "a rischio", "passaggi al professionismo",
                   "rischio per mille"),
                 titolo = "Quando si diventa professionisti",
                 nota = paste("una riga per stagione a rischio; chi diventa",
                              "professionista esce dal rischio, chi non ha ancora finito",
                              "la finestra dei venticinque anni e' censurato"))

  scrivi_tabella(ar, "coefficienti",
                 lapply(righe, function(r) list(
                   switch(r[[1]],
                          pct10 = "dieci punti di percentile in piu'",
                          assente = "assente dalla classifica l'anno prima",
                          coorte = "un anno di nascita piu' recente"),
                   r[[2]], r[[3]], r[[4]], r[[5]])),
                 c("variabile", "hazard ratio", "ic_lo", "ic_hi", "p"),
                 titolo = "Cosa cambia il rischio di passare professionista",
                 nota = paste("errori standard raggruppati per atleta: le stagioni dello",
                              "stesso corridore non sono osservazioni indipendenti"))

  scrivi_tabella(ar, "curva",
                 lapply(seq_len(nrow(curva)), function(i)
                   list(curva$eta[i], curva$h[i], curva$lo[i], curva$hi[i])),
                 c("eta", "rischio per mille", "lo", "hi"),
                 titolo = "Rischio stimato per eta', a parita' di rendimento")

  scrivi_valore(ar, "n_righe", nrow(d))
  scrivi_valore(ar, "n_atleti", length(unique(d$athlete_id)))
  scrivi_valore(ar, "n_eventi", sum(d$evento))
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_sopravvivenza[1],
                                      conf$coorti_sopravvivenza[2]))
  scrivi_valore(ar, "eta_finestra", c(eta_min, eta_ultima))
  scrivi_valore(ar, "eventi_fuori_finestra", fuori,
                "passaggi al professionismo oltre l'ultima eta' coperta dal ranking")
  scrivi_valore(ar, "quota_assenti",
                round(100 * mean(d$assente), 1),
                paste("quota delle stagioni a rischio in cui l'atleta non era",
                      "in classifica l'anno prima"))
  # L'eta' del rischio piu' alto si legge sulla tabella osservata, che e' quella che il
  # documento mostra; il massimo della curva stimata, piu' liscia, puo' cadere altrove e
  # ha un nome suo.
  scrivi_valore(ar, "eta_rischio_massimo", grezzo$eta[which.max(grezzo$hazard)],
                "eta' con il rischio osservato piu' alto, dalla tabella hazard_grezzo")
  scrivi_valore(ar, "eta_rischio_massimo_modello", curva$eta[which.max(curva$h)],
                "eta' con il rischio piu' alto sulla curva stimata, a parita' del resto")
  scrivi_valore(ar, "cumulate", list(alto = round(100 * p_alto, 1),
                                     medio = round(100 * p_medio, 1),
                                     basso = round(100 * p_basso, 1),
                                     scarto = PASSO * 2))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
