# STEP 16 — un modello per cella: quanto pesa il rendimento a una data eta'.
#
# LA DOMANDA
#     La descrittiva ha gia' detto che chi e' diventato professionista andava meglio.
#     Qui si chiede di quanto: dieci punti di percentile in piu' in una data cella
#     quanto moltiplicano l'odds di arrivare al professionismo?
#
# PERCHE' FIRTH E NON UNA LOGISTICA ORDINARIA
#     I professionisti sono il 2,7% del campione, e in alcune celle sono poche decine.
#     Con eventi rari la massima verosimiglianza produce coefficienti gonfiati, e nei
#     casi di separazione quasi completa diverge del tutto. La correzione di Firth
#     penalizza la verosimiglianza con il prior di Jeffreys: i coefficienti restano
#     finiti e la distorsione di piccolo campione si riduce. E' la scelta standard per
#     gli eventi rari, non una precauzione esotica.
#
#     Heinze e Schemper (2002), "A solution to the problem of separation in logistic
#     regression", Statistics in Medicine 21:2409-2419.
#
# UN MODELLO PER CELLA, NON UNO SOLO
#     Le celle non si mettono insieme qui. Chi e' presente in Under 23 e' gia' un
#     sopravvissuto a tre selezioni: il suo modello risponde a una domanda diversa
#     ("fra chi e' ancora in classifica a vent'anni, chi arriva?") da quello in Under 15
#     ("fra chi corre a quattordici anni, chi arriva?"). Sono popolazioni diverse e i
#     coefficienti non sono confrontabili come se misurassero la stessa cosa. Per questo
#     ogni riga porta con se' il proprio n e il proprio tasso di eventi.
#
# IL CONTROLLO CHE CONTA
#     L'AUC di un modello univariato deve coincidere con quella ricavata dal delta di
#     Cliff nella descrittiva: misurano la stessa cosa, cioe' la probabilita' che un
#     professionista preso a caso stia sopra un non professionista preso a caso. Se i
#     due numeri divergono lo script lo segnala, perche' vuol dire che uno dei due
#     percorsi ha un errore.
#
# USO
#     Rscript R/16_univariati.R          # dalla radice del progetto
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "logistf", "pROC"))

suppressPackageStartupMessages({
  library(logistf)
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "univariati"

# I coefficienti si leggono per dieci punti di percentile, non per uno: un punto e' una
# differenza che nessuno percepisce, dieci punti sono il salto fra un piazzamento e
# quello successivo in una classifica di duecento.
PASSO <- 10


# Il modello di una singola cella. Restituisce una riga di risultati, oppure NULL se la
# cella e' troppo sottile per dire qualcosa.
modello_cella <- function(dati, cella, min_eventi) {
  col_pct <- paste0("pct_", cella)
  col_pre <- paste0("present_", cella)

  d <- dati[dati[[col_pre]] == 1 & !is.na(dati[[col_pct]]), ]
  d <- data.frame(pro = as.integer(d$PRO), pct = as.numeric(d[[col_pct]]),
                  anno = as.numeric(d$birth_year))
  d <- d[!is.na(d$pro) & !is.na(d$anno), ]
  d$anno_c <- d$anno - mean(d$anno)      # centrato: l'intercetta resta interpretabile

  n <- nrow(d)
  eventi <- sum(d$pro)
  if (eventi < min_eventi || n - eventi < min_eventi) {
    return(list(cella = cella, n = n, eventi = eventi, sottile = TRUE))
  }

  # Due modelli, per due scopi diversi.
  #
  # Il grezzo serve al controllo: con un solo predittore monotono la sua AUC deve
  # coincidere con quella ricavata dal delta di Cliff nella descrittiva, e se non lo fa
  # c'e' un errore in uno dei due percorsi.
  #
  # L'aggiustato per anno di nascita e' quello che si riporta. Le coorti non sono
  # equivalenti fra loro: le piu' recenti hanno avuto meno tempo per arrivare al
  # professionismo, e senza il termine di coorte quella differenza di osservazione
  # finirebbe attribuita al rendimento.
  fit0 <- logistf(pro ~ pct, data = d)
  auc0 <- as.numeric(pROC::auc(pROC::roc(d$pro, fit0$predict, quiet = TRUE)))

  fit <- logistf(pro ~ pct + anno_c, data = d)
  beta <- unname(coef(fit)["pct"])
  ic <- c(fit$ci.lower[["pct"]], fit$ci.upper[["pct"]])
  auc <- as.numeric(pROC::auc(pROC::roc(d$pro, fit$predict, quiet = TRUE)))

  list(cella = cella, n = n, eventi = eventi, sottile = FALSE,
       or = exp(beta * PASSO),
       or_lo = exp(ic[1] * PASSO), or_hi = exp(ic[2] * PASSO),
       p = unname(fit$prob["pct"]),
       auc = auc,
       or_grezzo = exp(unname(coef(fit0)["pct"]) * PASSO),
       auc_grezza = auc0)
}


# L'AUC che la descrittiva ha gia' ricavato dal delta di Cliff, se c'e'. Serve solo come
# termine di paragone: se manca, il modello gira lo stesso.
auc_descrittiva <- function(cella) {
  if (!file.exists(DB_RISULTATI)) return(NA_real_)
  db <- dbConnect(SQLite(), DB_RISULTATI)
  on.exit(dbDisconnect(db))
  r <- dbGetQuery(db, "SELECT valore FROM valore WHERE modulo='punteggi' AND chiave=?",
                  list(paste0("delta_", cella)))
  if (nrow(r) == 0) return(NA_real_)
  as.numeric(fromJSON(r$valore[1])$auc)
}


# Primo anno contro secondo anno della stessa categoria, sugli atleti presenti in
# entrambi. E' l'unico modo di rispondere alla domanda "il primo anno predice meglio?":
# confrontare i tassi di professionismo delle due celle non risponde, perche' le due
# classifiche hanno ampiezze diverse e quindi popolazioni diverse.
confronto_anni <- function(dati, celle, min_eventi) {
  categorie <- unique(sub("y.*", "", celle))
  out <- list()
  for (cat in categorie) {
    c1 <- paste0(cat, "y1")
    c2 <- paste0(cat, "y2")
    if (!(c1 %in% celle) || !(c2 %in% celle)) next

    ok <- dati[[paste0("present_", c1)]] == 1 & dati[[paste0("present_", c2)]] == 1 &
      !is.na(dati[[paste0("pct_", c1)]]) & !is.na(dati[[paste0("pct_", c2)]]) &
      !is.na(dati$PRO)
    d <- dati[ok, ]
    if (nrow(d) == 0 || sum(d$PRO) < min_eventi) next

    r1 <- pROC::roc(d$PRO, as.numeric(d[[paste0("pct_", c1)]]), quiet = TRUE)
    r2 <- pROC::roc(d$PRO, as.numeric(d[[paste0("pct_", c2)]]), quiet = TRUE)
    p <- tryCatch(pROC::roc.test(r1, r2, method = "delong", paired = TRUE)$p.value,
                  error = function(e) NA_real_)
    a1 <- as.numeric(pROC::auc(r1))
    a2 <- as.numeric(pROC::auc(r2))
    out[[length(out) + 1]] <- list(cat, nrow(d), sum(d$PRO), a1, a2, a2 - a1, p)
    cat(sprintf("  %-4s n=%4d eventi=%3d  AUC y1=%.3f  y2=%.3f  differenza=%+.3f  p=%.3g
",
                cat, nrow(d), sum(d$PRO), a1, a2, a2 - a1, p))
  }
  out
}


# LA DOMANDA CHE UN LETTORE FA SUBITO
#     A tredici anni il percentile misura il rendimento o misura la data di nascita?
#     Fra ragazzi della stessa annata chi e' nato a gennaio ha fino a dodici mesi di
#     sviluppo in piu' di chi e' nato a dicembre, e la sezione sull'effetto dell'eta'
#     relativa mostra che nel ranking Under 15 i nati nel primo trimestre sono il doppio
#     di quelli dell'ultimo. Se il vantaggio in classifica fosse in buona parte
#     maturazione anagrafica, l'AUC di 0,736 direbbe soprattutto quello.
#
#     Il modo diretto di rispondere e' rifare ogni modello aggiungendo l'eta' relativa
#     come covariata e guardare cosa succede al coefficiente del percentile. Se resta
#     dov'era, la maturazione non e' cio' che il percentile sta misurando.
#
#     L'eta' relativa e' continua — giorni fra la nascita e il 31 dicembre — e non
#     ridotta a trimestri: il trimestre e' una discretizzazione arbitraria che butta via
#     informazione, e con eventi rari conviene non buttarne. Il coefficiente si legge
#     per cento giorni, cioe' circa un trimestre.
modello_eta_relativa <- function(dati, cella, min_eventi) {
  col_pct <- paste0("pct_", cella)
  col_pre <- paste0("present_", cella)

  d <- dati[dati[[col_pre]] == 1 & !is.na(dati[[col_pct]]), ]
  d <- data.frame(pro = as.integer(d$PRO), pct = as.numeric(d[[col_pct]]),
                  anno = as.numeric(d$birth_year), rel = as.numeric(d$rel_age))
  d <- d[stats::complete.cases(d), ]
  if (nrow(d) == 0) return(NULL)

  eventi <- sum(d$pro)
  if (eventi < min_eventi || nrow(d) - eventi < min_eventi) return(NULL)

  d$anno_c <- d$anno - mean(d$anno)
  d$rel_c <- (d$rel - mean(d$rel)) / 100        # per cento giorni, circa un trimestre

  fit_s <- logistf(pro ~ pct + anno_c, data = d)
  fit_c <- logistf(pro ~ pct + anno_c + rel_c, data = d)
  fit_r <- logistf(pro ~ rel_c + anno_c, data = d)

  auc <- function(f) as.numeric(pROC::auc(pROC::roc(d$pro, f$predict, quiet = TRUE)))

  list(cella = cella, n = nrow(d), eventi = eventi,
       or_senza = exp(unname(coef(fit_s)["pct"]) * PASSO),
       or_con = exp(unname(coef(fit_c)["pct"]) * PASSO),
       auc_senza = auc(fit_s), auc_con = auc(fit_c), auc_rel = auc(fit_r),
       or_rel = exp(unname(coef(fit_c)["rel_c"])),
       p_rel = unname(fit_c$prob["rel_c"]))
}


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  dati <- leggi_campione(dd)
  celle <- conf$celle_modello
  min_eventi <- conf$min_cella_pubblicabile

  cat(sprintf("STEP 16 — logistica di Firth, %d celle, %d atleti (%d professionisti)\n",
              length(celle), nrow(dati), sum(dati$PRO, na.rm = TRUE)))

  righe <- list()
  scarti <- c()
  sottili <- c()
  for (cella in celle) {
    r <- modello_cella(dati, cella, min_eventi)
    if (isTRUE(r$sottile)) {
      sottili <- c(sottili, cella)
      cat(sprintf("  %-7s n=%4d eventi=%3d  cella troppo sottile, saltata\n",
                  r$cella, r$n, r$eventi))
      next
    }
    # Il controllo si fa sul modello GREZZO: e' quello che deve coincidere con il
    # delta di Cliff. L'aggiustato non ha ragione di coincidere, perche' usa un
    # predittore in piu'.
    atteso <- auc_descrittiva(cella)
    scarto <- if (is.na(atteso)) NA_real_ else abs(r$auc_grezza - atteso)
    scarti <- c(scarti, scarto)

    cat(sprintf("  %-7s n=%4d eventi=%3d  OR/10pt=%.2f [%.2f-%.2f]  AUC=%.3f%s\n",
                r$cella, r$n, r$eventi, r$or, r$or_lo, r$or_hi, r$auc,
                if (is.na(scarto)) "" else
                  sprintf("  (grezza %.3f = descrittiva %.3f)", r$auc_grezza, atteso)))

    righe[[length(righe) + 1]] <- list(
      cella = r$cella, n = r$n, eventi = r$eventi,
      tasso = 100 * r$eventi / r$n,
      or = r$or, or_lo = r$or_lo, or_hi = r$or_hi, auc = r$auc,
      or_grezzo = r$or_grezzo)
  }

  if (length(righe) == 0) stop("Nessuna cella ha abbastanza eventi per un modello.")

  peggiore <- if (all(is.na(scarti))) NA_real_ else max(scarti, na.rm = TRUE)
  if (!is.na(peggiore) && peggiore > 0.01) {
    cat(sprintf("\nATTENZIONE: scarto massimo fra AUC del modello e AUC descrittiva %.3f.\n",
                peggiore))
    cat("Le due strade devono dare lo stesso numero: c'e' un errore da cercare.\n")
  } else if (!is.na(peggiore)) {
    cat(sprintf("\nControllo superato: AUC del modello e AUC da delta di Cliff coincidono
entro %.4f su tutte le celle.\n", peggiore))
  }

  cat("
Primo contro secondo anno, sugli stessi atleti:
")
  anni <- confronto_anni(dati, celle, min_eventi)

  cat("
Il percentile, aggiustato anche per l'eta' relativa:
")
  rel <- list()
  for (cella in celle) {
    r <- modello_eta_relativa(dati, cella, min_eventi)
    if (is.null(r)) next
    cat(sprintf("  %-7s OR %.2f -> %.2f   AUC %.3f -> %.3f   (sola eta' relativa %.3f)
",
                r$cella, r$or_senza, r$or_con, r$auc_senza, r$auc_con, r$auc_rel))
    rel[[length(rel) + 1]] <- r
  }

  # Chi diventa professionista senza mai comparire nelle classifiche Under 23: se fosse
  # una quota rilevante, i modelli sull'Under 23 sarebbero stimati su un gruppo da cui
  # i piu' forti sono usciti, e andrebbero letti di conseguenza.
  colonne_u23 <- grep("^present_U23", names(dati), value = TRUE)
  mai_u23 <- rowSums(sapply(colonne_u23, function(c) ifelse(is.na(dati[[c]]), 0,
                                                            dati[[c]]))) == 0
  pro_mai_u23 <- sum(dati$PRO == 1 & mai_u23, na.rm = TRUE)
  pro_tot <- sum(dati$PRO, na.rm = TRUE)
  precoci <- sum(dati$PRO == 1 & dati$age_turned_pro <= 20, na.rm = TRUE)
  cat(sprintf("
Professionisti mai presenti in Under 23: %d su %d. Passati al pro entro
i 20 anni: %d.
", pro_mai_u23, pro_tot, precoci))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  if (length(anni)) {
    scrivi_tabella(ar, "primo_contro_secondo", anni,
                   c("categoria", "atleti", "professionisti", "auc_y1", "auc_y2",
                     "differenza", "p_delong"),
                   titolo = "Primo e secondo anno a confronto, sugli stessi atleti",
                   nota = paste("Solo gli atleti presenti in entrambe le classifiche",
                                "della categoria: e' l'unico confronto in cui le due",
                                "misure riguardano le stesse persone."))
  }
  if (length(rel)) {
    scrivi_tabella(
      ar, "eta_relativa",
      lapply(rel, function(r) list(r$cella, r$n, r$eventi, r$or_senza, r$or_con,
                                   r$auc_senza, r$auc_con, r$or_rel, r$p_rel,
                                   r$auc_rel)),
      c("cella", "atleti", "professionisti", "or_senza", "or_con", "auc_senza",
        "auc_con", "or_rel", "p_rel", "auc_rel"),
      titolo = "Il percentile, prima e dopo l'aggiustamento per eta' relativa",
      nota = paste("L'eta' relativa e' in giorni dal 31 dicembre e il suo odds ratio",
                   "si legge per cento giorni, cioe' circa un trimestre. Le due AUC",
                   "sono dello stesso modello con e senza quel termine, sugli stessi",
                   "atleti."))
    peggio <- rel[[which.max(sapply(rel, function(r) abs(r$auc_con - r$auc_senza)))]]
    scrivi_valore(ar, "rel_age_scarto_auc", round(peggio$auc_con - peggio$auc_senza, 4),
                  "massimo spostamento di AUC dovuto all'aggiustamento per eta' relativa")
    primo <- rel[[1]]
    scrivi_valore(ar, "rel_age_prima_cella",
                  list(cella = primo$cella,
                       or_senza = round(primo$or_senza, 2),
                       or_con = round(primo$or_con, 2),
                       auc_senza = round(primo$auc_senza, 3),
                       auc_con = round(primo$auc_con, 3),
                       auc_rel = round(primo$auc_rel, 3),
                       or_rel = round(primo$or_rel, 2),
                       p_rel = signif(primo$p_rel, 3)),
                  "la cella piu' precoce, quella in cui l'eta' relativa dovrebbe pesare di piu'")
  }
  scrivi_valore(ar, "pro_mai_in_u23", pro_mai_u23)
  scrivi_valore(ar, "pro_totali", pro_tot)
  scrivi_valore(ar, "pro_precoci", precoci,
                "professionisti alla prima stagione entro i vent'anni")

  # R scrive numeri, non testo gia' formattato: gli intervalli restano due colonne
  # numeriche e sara' il modulo Python a comporli, con la virgola decimale italiana e
  # gli arrotondamenti che decide la presentazione.
  scrivi_tabella(
    ar, "per_cella",
    lapply(righe, function(r) list(r$cella, r$n, r$eventi, r$tasso,
                                   r$or, r$or_lo, r$or_hi, r$auc, r$or_grezzo)),
    c("cella", "atleti", "professionisti", "tasso", "or", "or_lo", "or_hi", "auc",
      "or_grezzo"),
    titolo = "Logistica di Firth, un modello per cella, aggiustato per anno di nascita",
    nota = paste("Ogni riga e' un modello a se', stimato sui soli atleti presenti in",
                 "quella cella. Gli odds ratio di celle diverse non sono confrontabili",
                 "fra loro: cambiano le popolazioni, non solo i coefficienti."))

  ors <- sapply(righe, function(r) r$or)
  aucs <- sapply(righe, function(r) r$auc)
  celle_ok <- sapply(righe, function(r) r$cella)
  i_max <- which.max(aucs)

  scrivi_valore(ar, "passo", PASSO, "punti di percentile a cui si riferisce l'odds ratio")
  scrivi_valore(ar, "celle_stimate", length(righe))
  scrivi_valore(ar, "celle_saltate", if (length(sottili)) sottili else list())
  scrivi_valore(ar, "auc_massima", list(cella = celle_ok[i_max],
                                        auc = round(aucs[i_max], 3),
                                        or = round(ors[i_max], 2)),
                "la cella in cui il rendimento discrimina di piu'")
  scrivi_valore(ar, "auc_prima", list(cella = celle_ok[1],
                                      auc = round(aucs[1], 3),
                                      or = round(ors[1], 2)),
                "la prima cella disponibile, cioe' la piu' precoce")
  scrivi_valore(ar, "scarto_controllo",
                if (is.na(peggiore)) NA else round(peggiore, 4),
                "scarto massimo fra AUC del modello e AUC ricavata dal delta di Cliff")
  info <- leggi_celle(dd)
  scrivi_tabella(ar, "ampiezza_liste",
                 lapply(seq_len(nrow(info)), function(i)
                   list(info$cella[i], info$ampiezza_lista[i])),
                 c("cella", "ampiezza_media"),
                 titolo = "Quanto e' larga la classifica di ogni cella")
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  # Quanto sposta l'aggiustamento per coorte: se sposta poco, il gradiente osservato
  # non e' un effetto di quanto tempo ciascuna coorte ha avuto a disposizione.
  spostamento <- max(abs(sapply(righe, function(r) r$or - r$or_grezzo)))
  scrivi_valore(ar, "spostamento_coorte", round(spostamento, 3),
                "massima differenza fra odds ratio grezzo e aggiustato per anno di nascita")

  cat(sprintf("\nScritti %d risultati in %s (modulo '%s').\n",
              length(righe), DB_RISULTATI, MODULO))
}

main()
