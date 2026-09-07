"""
Controllo di sicurezza da eseguire PRIMA di ogni commit.

Verifica due cose:
  1. che i file con dati personali siano effettivamente esclusi da git;
  2. che nessun file destinato al repository contenga nomi di atleti.

Esce con codice 1 se trova un problema, cosi' e' usabile come hook pre-commit:

    git config core.hooksPath .githooks
"""
import csv
import os
import re
import subprocess
import sys

CROSSWALK = "data/private/crosswalk_atleti.csv"

# Percorsi che non devono MAI finire in git.
DEVONO_ESSERE_IGNORATI = [
    "data/giovanile/ciclismo.db",
    "data/private/crosswalk_atleti.csv",
    "data/private/casi_omonimia.csv",
    "data/private/casi_eta_incoerente.csv",
    "data/private/salt.txt",
    "data/analisi/analisi.db",
]

# File dove cercare nomi: testo, non binari.
ESTENSIONI = {".md", ".csv", ".py", ".r", ".R", ".txt", ".json", ".sql", ".yml", ".yaml",
              ".db"}   # l'archivio dei risultati e' binario ma contiene testo: va letto

# Nomi generici usati come esempio nella prosa ("ci saranno diversi Marco Rossi
# del 1997"). Coincidono per caso con atleti reali del dataset, ma non rivelano
# nessuno: il senso della frase e' proprio che il nome e' comunissimo.
# Aggiungere qui solo nomi che compaiono come esempio inventato, mai un nome che
# si riferisca davvero a un atleta del dataset.
ESEMPI_AMMESSI = {"marco rossi", "mario rossi"}


def file_in_git():
    """File tracciati piu' quelli che un 'git add .' aggiungerebbe."""
    tracciati = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    nuovi = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                           capture_output=True, text=True).stdout.split()
    return sorted(set(tracciati) | set(nuovi))


def nomi_atleti():
    """Nomi completi, nei due ordini in cui possono comparire."""
    if not os.path.exists(CROSSWALK):
        return None
    nomi = set()
    with open(CROSSWALK, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nome, cognome = (r.get("nome") or "").strip(), (r.get("cognome") or "").strip()
            if len(nome) >= 3 and len(cognome) >= 3:
                nomi.add(("%s %s" % (cognome, nome)).lower())
                nomi.add(("%s %s" % (nome, cognome)).lower())
    return nomi - ESEMPI_AMMESSI


def main():
    problemi = []

    for p in DEVONO_ESSERE_IGNORATI:
        if not os.path.exists(p):
            continue
        ignorato = subprocess.run(["git", "check-ignore", "-q", p]).returncode == 0
        if not ignorato:
            problemi.append("NON IGNORATO da git: %s" % p)

    nomi = nomi_atleti()
    if nomi is None:
        print("Nota: %s assente, salto la ricerca di nomi." % CROSSWALK)
    else:
        for p in file_in_git():
            if os.path.splitext(p)[1] not in ESTENSIONI:
                continue
            try:
                testo = open(p, encoding="utf-8", errors="ignore").read().lower()
            except OSError:
                continue
            # Si estraggono le coppie di parole adiacenti del testo e si intersecano
            # con l'insieme dei nomi: costa quanto leggere il file, invece di una
            # regex per ciascuno dei 24.000 nomi. Lavorando su parole intere evita
            # anche i falsi positivi per sottostringa, cioe' il cognome di un atleta
            # che e' prefisso del cognome di un altro.
            parole = re.findall(r"[a-zàèéìòù']+", testo)
            coppie = {"%s %s" % (parole[i], parole[i + 1]) for i in range(len(parole) - 1)}
            trovati = sorted(coppie & nomi)
            if trovati:
                problemi.append("%s contiene %d nome/i di atleti (primo: '%s')"
                                % (p, len(trovati), trovati[0]))

    if problemi:
        print("CONTROLLO PRIVACY FALLITO\n")
        for x in problemi:
            print("  - %s" % x)
        print("\nNel repository entra solo cio' che e' anonimo. Correggi prima di committare.")
        return 1

    print("Controllo privacy superato: %d file destinati al repository, nessun dato personale."
          % len(file_in_git()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
