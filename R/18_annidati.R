# STEP 18 — quanto aggiunge ogni categoria a quella precedente.
#
# LA DOMANDA (Domanda C)
#     Sapere come e' andato un ragazzo in Under 15 dice qualcosa sul suo arrivo al
#     professionismo. Sapere anche come e' andato in Under 17 dice **qualcosa in piu'**,
#     o e' informazione gia' contenuta nella precedente? E cosi' fino all'Under 23.
#
#     E' la domanda che distingue "la prestazione giovanile predice" da "la prestazione
#     giovanile predice, e sempre di piu' man mano che ci si avvicina".
#
# LA REGOLA CHE RENDE IL CONFRONTO LECITO
#     Tutti i modelli girano sullo **stesso identico sottocampione**: chi e' osservato in
#     tutte le celle della sequenza. Se M1 girasse su 1.700 atleti e M4 su 100, il salto
#     di AUC misurerebbe il cambio di popolazione e non l'aggiunta di informazione.
#     Lo script verifica di avere lo stesso n a ogni passo e si ferma se non e' cosi'.
#
#     Il prezzo e' che il sottocampione e' fortemente selezionato: sono gli atleti
#     arrivati fino all'Under 23 restando in classifica, e fra loro i professionisti
#     sono quasi la meta'. Le AUC di questa sezione **non sono confrontabili** con
#     quelle dello STEP 16, che girano su tutti. Qui interessa la differenza fra
#     modelli, non il livello.
#
# COME SI MISURA L'AGGIUNTA
#     Due strumenti, che rispondono a due domande diverse.
#
#     Il test del rapporto di verosimiglianza penalizzato chiede se il predittore in piu'
#     migliora l'adattamento del modello: e' una domanda sul modello.
#
#     Il test di DeLong chiede se l'area sotto la curva cresce in modo distinguibile dal
#     caso, tenendo conto che le due curve sono calcolate sugli stessi atleti e quindi
#     sono correlate: e' una domanda sulla capacita' di ordinare le persone. E' quella
#     che interessa a una societa' che deve decidere chi guardare.
#
#     DeLong, DeLong e Clarke-Pearson (1988), Biometrics 44:837-845.
#
# LE DUE VERSIONI DEL PREDITTORE U19
#     Il ranking nazionale Under 19 non include i risultati internazionali, e chi corre
#     all'estero risulta quindi piu' debole di quanto sia. La guida chiede di ripetere la
#     sequenza con un Under 19 armonizzato che li includa: se il salto U19 -> U23 si
#     riduce, parte del gradiente era un artefatto di misurazione.
#
#     Finche' quella colonna non esiste a monte, lo script gira la sola versione grezza e
#     lo dichiara, invece di far finta che la questione non esista.
#
# USO
#     Rscript R/18_annidati.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "logistf", "pROC"))

suppressPackageStartupMessages({
  library(logistf)
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "annidati"
PASSO <- 10


# Il sottocampione: chi e' osservato in tutte le celle della sequenza. Da qui in poi non
# cambia piu', ed e' questa la condizione che rende confrontabili i modelli.
sottocampione <- function(dati, celle, colonne_pct) {
  ok <- rep(TRUE, nrow(dati))
  for (i in seq_along(celle)) {
    ok <- ok & dati[[paste0("present_", celle[i])]] == 1 &
      !is.na(dati[[colonne_pct[i]]])
  }
  ok <- ok & !is.na(dati$PRO) & !is.na(dati$birth_year)
  d <- dati[ok, ]
  out <- data.frame(pro = as.integer(d$PRO),
                    anno_c = as.numeric(d$birth_year) - mean(as.numeric(d$birth_year)))
  for (i in seq_along(celle)) {
    out[[paste0("x", i)]] <- as.numeric(d[[colonne_pct[i]]]) / PASSO
  }
  out
}


# La sequenza M0 -> M1 -> ... -> Mk. Ogni modello aggiunge una cella al precedente.
sequenza <- function(d, celle) {
  modelli <- list()
  termini <- "anno_c"
  etichette <- c("M0 (solo coorte)")
  for (i in seq_along(celle)) {
    termini <- c(termini, paste0("x", i))
    etichette <- c(etichette, sprintf("M%d (+%s)", i, celle[i]))
  }
  for (k in 0:length(celle)) {
    f <- as.formula(paste("pro ~", paste(termini[1:(k + 1)], collapse = " + ")))
    fit <- logistf(f, data = d)
    modelli[[k + 1]] <- list(
      etichetta = etichette[k + 1],
      fit = fit,
      roc = pROC::roc(d$pro, fit$predict, quiet = TRUE),
      loglik = fit$loglik[1],
      gradi = length(termini[1:(k + 1)]))
  }
  modelli
}


# Il confronto fra un modello e il precedente: quanto e' cresciuta l'AUC, e se la
# crescita e' distinguibile dal caso.
confronta <- function(prima, dopo) {
  auc0 <- as.numeric(pROC::auc(prima$roc))
  auc1 <- as.numeric(pROC::auc(dopo$roc))
  # Il test di DeLong per curve appaiate: gli atleti sono gli stessi, e ignorarlo
  # gonfierebbe l'incertezza della differenza.
  p_delong <- tryCatch(
    pROC::roc.test(prima$roc, dopo$roc, method = "delong", paired = TRUE)$p.value,
    error = function(e) NA_real_)
  # Rapporto di verosimiglianza penalizzato: la statistica e' 2 volte la differenza
  # delle log-verosimiglianze penalizzate, con un grado di liberta' per il termine
  # aggiunto.
  chi <- 2 * (dopo$loglik - prima$loglik)
  gl <- dopo$gradi - prima$gradi
  p_lr <- if (chi > 0 && gl > 0) pchisq(chi, gl, lower.tail = FALSE) else NA_real_
  list(auc = auc1, delta = auc1 - auc0, p_delong = p_delong, p_lr = p_lr)
}


ic_auc <- function(r) {
  ci <- as.numeric(pROC::ci.auc(r, method = "delong"))
  c(ci[1], ci[3])
}


# Una passata completa della sequenza, per una versione del predittore U19.
passata <- function(dati, celle, colonne_pct, nome) {
  d <- sottocampione(dati, celle, colonne_pct)
  n <- nrow(d)
  eventi <- sum(d$pro)
  cat(sprintf("\n[%s] sottocampione: %d atleti, %d professionisti (%.0f%%)\n",
              nome, n, eventi, 100 * eventi / n))

  modelli <- sequenza(d, celle)

  # La verifica che la guida chiede esplicitamente: stesso n in tutti i modelli.
  enne <- sapply(modelli, function(m) length(m$fit$predict))
  if (length(unique(enne)) != 1) {
    stop(sprintf("I modelli non girano sullo stesso campione: %s",
                 paste(enne, collapse = ", ")), call. = FALSE)
  }

  righe <- list()
  for (k in seq_along(modelli)) {
    m <- modelli[[k]]
    auc <- as.numeric(pROC::auc(m$roc))
    ic <- ic_auc(m$roc)
    if (k == 1) {
      cat(sprintf("  %-18s AUC=%.3f [%.3f-%.3f]\n", m$etichetta, auc, ic[1], ic[2]))
      righe[[k]] <- list(m$etichetta, n, eventi, auc, ic[1], ic[2], NA, NA, NA)
    } else {
      cf <- confronta(modelli[[k - 1]], m)
      cat(sprintf("  %-18s AUC=%.3f [%.3f-%.3f]  dAUC=%+.3f  DeLong p=%.3g  LR p=%.3g\n",
                  m$etichetta, auc, ic[1], ic[2], cf$delta, cf$p_delong, cf$p_lr))
      righe[[k]] <- list(m$etichetta, n, eventi, auc, ic[1], ic[2],
                         cf$delta, cf$p_delong, cf$p_lr)
    }
  }
  list(n = n, eventi = eventi, righe = righe, modelli = modelli)
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  dati <- leggi_campione(dd)
  celle <- conf$celle_annidate

  cat(sprintf("STEP 18 — sequenza annidata su %s\n", paste(celle, collapse = " -> ")))

  grezza <- passata(dati, celle, paste0("pct_", celle), "grezza")

  # Versione armonizzata: stessa sequenza, ma con l'U19 misurato includendo i risultati
  # internazionali. Gira solo se la colonna esiste.
  col_arm <- paste0("pct_", conf$cella_u19_armonizzata)
  ha_arm <- col_arm %in% names(dati)
  armonizzata <- NULL
  if (ha_arm) {
    colonne <- paste0("pct_", celle)
    colonne[grepl("^U19", celle)] <- col_arm
    armonizzata <- passata(dati, celle, colonne, "armonizzata")
  } else {
    cat(sprintf("\n[armonizzata] la colonna %s non esiste ancora: la sequenza gira
solo nella versione grezza. Vedi docs/da_fare.md §C3.\n", col_arm))
  }

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  colonne_out <- c("modello", "atleti", "professionisti", "auc", "auc_lo", "auc_hi",
                   "delta_auc", "p_delong", "p_lr")
  scrivi_tabella(ar, "sequenza", grezza$righe, colonne_out,
                 titolo = "Modelli annidati, versione grezza",
                 nota = paste("Tutti i modelli girano sugli stessi", grezza$n,
                              "atleti. Le AUC non sono confrontabili con quelle dei",
                              "modelli univariati: qui il sottocampione e' composto da",
                              "chi e' arrivato fino all'Under 23 restando in classifica."))
  if (!is.null(armonizzata)) {
    scrivi_tabella(ar, "sequenza_armonizzata", armonizzata$righe, colonne_out,
                   titolo = "Modelli annidati, Under 19 armonizzato")
  }

  aucs <- sapply(grezza$righe, function(r) r[[4]])
  delta <- sapply(grezza$righe[-1], function(r) r[[7]])
  etichette <- sapply(grezza$righe[-1], function(r) r[[1]])
  i_max <- which.max(delta)

  # L'eta' di osservazione di ciascuna cella serve al grafico centrale, dove l'asse x
  # e' l'eta' e non il numero del modello: e' quello che rende leggibile "quanto si sa,
  # e a che eta' lo si sa".
  info_celle <- leggi_celle(dd)
  scrivi_valore(ar, "celle", celle)
  scrivi_valore(ar, "eta_celle",
                info_celle$eta[match(celle, info_celle$cella)])
  scrivi_valore(ar, "n", grezza$n, "atleti osservati in tutte le celle della sequenza")
  scrivi_valore(ar, "n_coorte", nrow(dati),
                "atleti della coorte, da cui il sottocampione e' estratto")
  scrivi_valore(ar, "eventi", grezza$eventi)
  scrivi_valore(ar, "tasso_pro", round(100 * grezza$eventi / grezza$n, 1))
  scrivi_valore(ar, "auc_base", round(aucs[1], 3), "modello con la sola coorte")
  scrivi_valore(ar, "auc_finale", round(aucs[length(aucs)], 3))
  scrivi_valore(ar, "guadagno_totale", round(aucs[length(aucs)] - aucs[2], 3),
                "quanto aggiunge tutto il resto rispetto al solo Under 15")
  scrivi_valore(ar, "salto_maggiore",
                list(modello = etichette[i_max], delta = round(delta[i_max], 3)),
                "il passo che aggiunge di piu'")
  scrivi_valore(ar, "armonizzata_disponibile", ha_arm)
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
