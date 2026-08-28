# STEP 17 — la regressione penalizzata, come controllo e non come analisi principale.
#
# PERCHE' ARRIVA PER ULTIMO
#     La guida lo colloca subito dopo i modelli univariati, e per un buon motivo: se le
#     categorie giovanili misurassero tutte la stessa cosa, un modello che le usa insieme
#     non riuscirebbe a separarne i contributi e la penalizzazione sarebbe obbligatoria.
#
#     Il fattore di inflazione della varianza calcolato nella sezione sulle correlazioni
#     dice pero' che il massimo e' 2,89, ben sotto la soglia di 5. La penalizzazione non
#     e' quindi necessaria: e' un confronto. Farla per ultima, accanto alla foresta
#     casuale, la mette dove le appartiene — fra i controlli di robustezza.
#
# COSA FA L'ELASTIC NET
#     Aggiunge alla verosimiglianza una penalita' sui coefficienti, che li tira verso
#     zero. La forza della penalita' (lambda) si sceglie per validazione incrociata, e
#     conviene sceglierla **conservativa**: `lambda.1se` e' la penalita' piu' forte il cui
#     errore resta entro una deviazione standard dal minimo, e produce il modello piu'
#     parsimonioso fra quelli sostanzialmente equivalenti al migliore.
#
#     Il metodo mescola due penalita': quella di Ridge, che restringe tutti i
#     coefficienti, e quella del Lasso, che ne azzera alcuni. Con predittori correlati
#     come questi, una miscela e' piu' stabile del solo Lasso, che sceglierebbe a caso
#     una fra due variabili quasi identiche.
#
#     Zou e Hastie (2005), "Regularization and variable selection via the elastic net",
#     JRSS-B 67:301-320.
#
# NIENTE p-VALUE DA QUESTO MODELLO
#     I coefficienti penalizzati sono distorti verso zero per costruzione, e la
#     distribuzione campionaria che servirebbe per un test non e' quella che i programmi
#     riportano. Si guardano quali variabili sopravvivono e quanto vale la previsione,
#     non se un coefficiente sia «significativo».
#
# IL COSTO DA DICHIARARE
#     Il modello usa tutte le celle insieme, quindi gira solo su chi e' osservato in
#     tutte: il campione crolla, e insieme a lui il numero di eventi. E' lo stesso
#     problema dei modelli annidati, e la conclusione che se ne puo' trarre e' altrettanto
#     condizionata.
#
# USO
#     Rscript R/17_penalizzato.R
#
# DIPENDENZE
#     install.packages(c("RSQLite", "jsonlite", "glmnet", "pROC"))

suppressPackageStartupMessages({
  library(glmnet)
  library(pROC)
})

source("R/lib_risultati.R")

MODULO <- "penalizzato"
PASSO <- 10
ALPHA <- 0.5       # meta' Lasso e meta' Ridge: miscela stabile con predittori correlati
set.seed(20260828)


main <- function() {
  dd <- dati_apri()
  on.exit(dbDisconnect(dd))
  conf <- leggi_config(dd)
  celle <- conf$celle_modello

  colonne <- c("PRO", "birth_year", paste0("pct_", celle), paste0("present_", celle))
  d <- dbGetQuery(dd, sprintf("SELECT %s FROM campione WHERE PRO IS NOT NULL
                               AND birth_year IS NOT NULL",
                              paste(colonne, collapse = ", ")))

  # Il modello richiede tutte le celle su ogni riga: restano solo gli atleti osservati
  # ovunque. E' la stessa restrizione dei modelli annidati e va detta, non subita.
  completi <- rep(TRUE, nrow(d))
  for (c in celle) {
    completi <- completi & !is.na(d[[paste0("pct_", c)]]) &
      !is.na(d[[paste0("present_", c)]]) & d[[paste0("present_", c)]] == 1
  }
  x <- d[completi, ]
  cat(sprintf("STEP 17 — elastic net, coorti %d-%d\n",
              conf$coorti_a_c[1], conf$coorti_a_c[2]))
  cat(sprintf("  %d atleti su %d hanno tutte le %d celle osservate: %d professionisti\n",
              nrow(x), nrow(d), length(celle), sum(x$PRO)))
  if (sum(x$PRO) < 10) stop("Troppo pochi eventi nel sottocampione completo.")

  X <- as.matrix(x[, paste0("pct_", celle)]) / PASSO
  colnames(X) <- celle
  X <- cbind(X, coorte = x$birth_year - mean(x$birth_year))
  y <- x$PRO

  cv <- cv.glmnet(X, y, family = "binomial", alpha = ALPHA,
                  nfolds = 10, type.measure = "deviance")
  coefficienti <- as.matrix(coef(cv, s = "lambda.1se"))
  nomi <- rownames(coefficienti)[-1]
  valori <- coefficienti[-1, 1]

  sopravvissuti <- nomi[valori != 0]
  cat(sprintf("\n  lambda scelto (1se): %.4f — %d coefficienti su %d restano diversi da zero\n",
              cv$lambda.1se, length(sopravvissuti), length(nomi)))
  for (i in seq_along(nomi)) {
    cat(sprintf("    %-9s %s\n", nomi[i],
                if (valori[i] == 0) "azzerato"
                else sprintf("OR = %.2f", exp(valori[i]))))
  }

  # Il confronto che interessa: la penalizzazione fa previsioni migliori del modello a
  # una cella sola? Sullo stesso sottocampione, altrimenti non si confronta niente.
  p_pen <- as.vector(predict(cv, newx = X, s = "lambda.1se", type = "response"))
  auc_pen <- as.numeric(pROC::auc(pROC::roc(y, p_pen, quiet = TRUE)))

  cella_sola <- conf$celle_annidate[length(conf$celle_annidate) - 1]
  if (!(cella_sola %in% celle)) cella_sola <- celle[length(celle) - 1]
  semplice <- glm(y ~ X[, cella_sola] + X[, "coorte"], family = binomial())
  auc_sem <- as.numeric(pROC::auc(pROC::roc(y, fitted(semplice), quiet = TRUE)))
  cat(sprintf("\n  AUC sullo stesso sottocampione: elastic net %.3f, solo %s %.3f (%+.3f)\n",
              auc_pen, cella_sola, auc_sem, auc_pen - auc_sem))

  ar <- archivio_apri(MODULO)
  on.exit(archivio_chiudi(ar), add = TRUE)

  scrivi_tabella(
    ar, "coefficienti",
    lapply(seq_along(nomi), function(i)
      list(nomi[i], if (valori[i] == 0) NULL else exp(valori[i]),
           if (valori[i] == 0) "azzerato" else "trattenuto")),
    c("variabile", "odds ratio penalizzato", "esito"),
    titolo = "Cosa sopravvive alla penalizzazione",
    nota = paste("elastic net a meta' fra le due penalita', con lambda scelto per",
                 "validazione incrociata nella versione conservativa; gli odds ratio sono",
                 "distorti verso zero per costruzione e non vanno letti come stime"))

  scrivi_valore(ar, "alpha", ALPHA)
  scrivi_valore(ar, "lambda", round(cv$lambda.1se, 4))
  scrivi_valore(ar, "n", nrow(x))
  scrivi_valore(ar, "n_coorte", nrow(d))
  scrivi_valore(ar, "eventi", sum(y))
  scrivi_valore(ar, "trattenuti", length(sopravvissuti))
  scrivi_valore(ar, "totali", length(nomi))
  scrivi_valore(ar, "auc", list(penalizzato = round(auc_pen, 3),
                                semplice = round(auc_sem, 3),
                                cella = cella_sola,
                                differenza = round(auc_pen - auc_sem, 3)))
  scrivi_valore(ar, "coorti", sprintf("%d-%d", conf$coorti_a_c[1], conf$coorti_a_c[2]))

  cat(sprintf("\nScritti i risultati in %s (modulo '%s').\n", DB_RISULTATI, MODULO))
}

main()
