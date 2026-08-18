# D02 — Python refresher e software engineering essentials

## Meta-modulo D02

**Target**  
Me stesso oggi, e in futuro chiunque debba usare Python come lingua franca
per ML, LLM, agenti e pipeline OSINT, con attenzione alla qualità del codice
ma senza diventare “solo” sviluppatore backend.

**Prerequisiti consigliati**

- aver completato D01 (workspace, Git, Obsidian, LLM wiki) o almeno averlo impostato
- conoscenza di base di Python:
  - tipi principali (`int`, `float`, `str`, `list`, `dict`)
  - `if`, `for`, funzioni semplici
- familiarità minima con terminale e Git (clone, commit, push)

**Durata indicativa**

- **Modalità minima (~2–3 ore)**  
  - setup ambiente Python + virtualenv/uv  
  - script che legge/scrive JSONL  
  - logging ed error handling di base  
  - una chiamata API HTTP semplice

- **Modalità standard (~6–8 ore)**  
  - tutto quanto sopra  
  - struttura progetto (`src/`, `tests/`, `config/`)  
  - gestione config/segretI  
  - test con `pytest`  
  - CLI semplice per lanciare operazioni

- **Modalità deep dive (più giornate)**  
  - progetto consolidato “client API + logging + test + CLI + async”  
  - pattern riutilizzabili per moduli futuri (ML, LLM, agenti, OSINT)  
  - integrazione con tooling (pre-commit, formatter, linter)

**Quando considerare il modulo “completato”**

- ho almeno un progetto Python con:
  - `src/` + `tests/` + `logs/` + `config/`  
  - file di config + uso di variabili d’ambiente per i segreti  
  - logging funzionante su file + console  
  - almeno 1–2 test con `pytest` che girano senza errori
- so scrivere e capire uno script che:
  - legge un file JSON/JSONL  
  - chiama un’API HTTP  
  - gestisce errori in modo non triviale  
  - espone una CLI minima

---

## Perché questo documento

Questo documento è un **ripasso mirato di Python** e delle basi di *software engineering*
che mi servono per tutto il resto del percorso (ML, LLM, agenti, pipeline OSINT).

Non vuole insegnare Python da zero: definisce **standard e pattern** per:

- organizzare progetti in modo ripetibile (`src/`, `tests/`, `logs/`, `config/`)
- gestire dipendenze e ambienti
- scrivere codice leggibile e testabile
- lavorare con file, JSON, JSONL
- chiamare API HTTP e loggare in modo sensato

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- lavorare in un **ambiente Python riproducibile** (virtualenv/uv, requirements)
- scrivere script e moduli leggibili, con funzioni ben definite
- leggere/scrivere file (testo, JSON, JSONL) in modo robusto
- configurare logging ed error handling di base
- gestire configurazione e segreti senza hard-codarli nel codice
- usare HTTP/REST con una libreria (es. `requests` o `httpx`)
- scrivere test di base con `pytest`
- impacchettare un piccolo progetto “standard” da riutilizzare nei moduli successivi

---

## 1. Mappa degli argomenti

### 1.1 Blocchi principali

1. Setup ambiente Python (versione, virtualenv/uv, struttura progetto).
2. Refresher di sintassi e strutture dati.
3. File, JSON, JSONL.
4. Logging ed error handling.
5. Configurazione e segreti.
6. HTTP e client API.
7. Test con `pytest`.
8. CLI e piccolo tool da riga di comando.
9. Cenni di async (quando serve).
10. Progetto finale di consolidamento.

---

## 2. Setup ambiente Python

### 2.1 Versione e installazione

Per mantenere compatibilità con librerie moderne:

- preferisco Python **3.11+** se possibile
- su Mac e Windows mantengo un’installazione di base, ma isolo ogni progetto in un ambiente dedicato

Riferimenti:

- Documentazione ufficiale Python (home + tutorial):  
  https://www.python.org/  
  https://docs.python.org/3/tutorial/index.html  
- Guida “Python for beginners”:  
  https://www.python.org/about/gettingstarted/  

### 2.2 Ambienti virtuali / uv

Scopo: evitare conflitti di dipendenze tra progetti.

Approcci possibili:

- `venv` (standard library, sufficiente per molti casi)
- strumenti moderni come `uv` o `pipx` per gestione più veloce/ergonomica

Esempio con `venv`:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# oppure
.\.venv\Scripts\activate   # Windows

pip install -U pip
pip install requests pytest
```

Buone pratiche:

- non installare pacchetti globalmente se non necessario
- avere un file `requirements.txt` o equivalente per ogni progetto

---

### 2.3 Struttura di progetto standard

Struttura consigliata per i progetti che userò in tutto il percorso:

```text
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── config.py
│       ├── api_client.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_api_client.py
├── config/
│   └── settings.example.yaml
├── logs/
├── .env.example
├── requirements.txt
└── README.md
```

Questa struttura:

- separa chiaramente **codice applicativo**, **test**, **config**, **log**
- è facile da spostare, archiviare, trasformare in libreria o servizio più avanti

---

## 3. Refresher sintassi e strutture dati

### 3.1 Tipi base e controllo di flusso

Mi assicuro di sentirmi solido su:

- tipi: `int`, `float`, `str`, `bool`, `list`, `dict`, `set`, `tuple`
- controllo di flusso: `if/elif/else`, `for`, `while`
- comprensioni di lista e dizionario
- funzioni con parametri di default, keyword arguments

Se qualcosa scricchiola:

- riprendo le sezioni pertinenti del *Python Tutorial*:  
  https://docs.python.org/3/tutorial/introduction.html  
  https://docs.python.org/3/tutorial/controlflow.html  

### 3.2 Strutture dati che uso davvero

Nel contesto ML/LLM/OSINT userò soprattutto:

- liste di dizionari (es. righe di dataset, log strutturati)
- dizionari annidati (config, risposte API)
- `Path` (modulo `pathlib`) per gestire file in modo portabile

Esempio:

```python
from pathlib import Path

data_dir = Path("data")
for json_file in data_dir.glob("*.json"):
    print(json_file.name)
```

---

## 4. File, JSON e JSONL

### 4.1 File di testo (Markdown, log, appunti)

Pattern base:

```python
from pathlib import Path

file_path = Path("notes") / "example.md"
file_path.parent.mkdir(exist_ok=True)

text = file_path.read_text(encoding="utf-8")
file_path.write_text(text + "\n\nNuova nota.", encoding="utf-8")
```

Uso:

- note di lavoro
- log “narrativi”
- output di agenti/LLM da salvare in locale

### 4.2 JSON e JSONL

Per dati strutturati:

- **JSON**: un oggetto per file
- **JSONL**: un oggetto JSON per riga → ideale per log, dataset, eventi

Esempio di scrittura JSONL:

```python
import json
from pathlib import Path

log_path = Path("logs") / "events.jsonl"
log_path.parent.mkdir(exist_ok=True)

event = {"type": "api_call", "status": "ok"}

with log_path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

Esempio di lettura:

```python
events = []
with log_path.open(encoding="utf-8") as f:
    for line in f:
        events.append(json.loads(line))
```

---

## 5. Logging ed error handling

### 5.1 Logging strutturato

Uso il modulo `logging` per:

- avere log su file + console
- distinguere livelli (INFO, WARNING, ERROR)
- in futuro, loggare in formato JSON (utile per analisi/OSINT)

Esempio base:

```python
import logging
from pathlib import Path

log_file = Path("logs") / "app.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("my_project")

logger.info("Applicazione avviata")
```

### 5.2 Gestione degli errori

Regole pratiche:

- non soffocare le eccezioni con `except Exception: pass`
- usare `logging.exception` per tracciare stack trace

Esempio:

```python
def call_api(...):
    # implementazione
    ...

try:
    response = call_api(...)
except Exception as e:
    logger.exception("Errore nella chiamata API: %s", e)
    # eventuale rilancio o gestione specifica
```

---

## 6. Configurazione e segreti

### 6.1 Config file

Non hard-codare nel codice:

- URL di servizi
- path di cartelle
- timeouts, parametri di retrial
- nomi di indici, ID di collezioni

Uso file in `config/` (`.yaml`, `.ini`, `.json`) caricati all’avvio.

Esempio minimal in YAML:

```yaml
api:
  base_url: "https://api.example.com"
  timeout: 10
log:
  level: "INFO"
```

### 6.2 Segreti e variabili d’ambiente

Qualunque chiave API/token va:

- in variabile d’ambiente
- o in `.env` *non* versionato (e `.env.example` nel repo come template)

Esempio:

```python
import os

API_KEY = os.environ.get("MY_API_KEY")
if not API_KEY:
    raise RuntimeError("MY_API_KEY non impostata; verifica il file .env o le variabili d'ambiente.")
```

---

## 7. HTTP e client API

### 7.1 Chiamate HTTP di base

Uso una libreria come `requests` o `httpx` (sincrono o async).

Esempio con `requests`:

```python
import requests

def get_status():
    resp = requests.get("https://httpbin.org/get", timeout=10)
    resp.raise_for_status()
    return resp.json()
```

Linee guida:

- sempre `timeout`
- `raise_for_status()` per non ignorare errori HTTP
- logging di URL, status code, latenza se necessario

### 7.2 Pattern per client riutilizzabile

Creo un modulo `api_client.py` con una classe o funzioni che incapsulano logica ripetuta:

```python
import logging
import os
import requests

logger = logging.getLogger("my_project.api_client")

BASE_URL = os.environ.get("MY_API_BASE_URL", "https://httpbin.org")

def get(path: str, **kwargs):
    url = f"{BASE_URL}/{path.lstrip('/')}"
    logger.info("GET %s", url)
    resp = requests.get(url, timeout=kwargs.pop("timeout", 10), **kwargs)
    resp.raise_for_status()
    return resp.json()
```

Questo pattern sarà riusato per:

- chiamare API di modelli LLM
- integrare servizi OSINT
- orchestrare pipeline agentiche

---

## 8. Test con pytest

### 8.1 Perché test

Test anche minimi:

- riducono regressioni quando modifico funzioni condivise
- danno sicurezza quando integro più servizi (API LLM + database + file system)

### 8.2 Struttura minima

- cartella `tests/`
- file `test_xxx.py`
- funzioni `test_...`

Esempio:

```python
# src/my_project/math_utils.py
def add(a, b):
    return a + b

# tests/test_math_utils.py
from my_project.math_utils import add

def test_add():
    assert add(2, 3) == 5
```

Esecuzione:

```bash
pytest -q
```

---

## 9. Script e CLI (Command Line Interface)

### 9.1 Entry point `main.py`

Pattern standard:

```python
# src/my_project/main.py
def main():
    print("Ciao dalla Stazione!")

if __name__ == "__main__":
    main()
```

Esecuzione:

```bash
python -m my_project.main
```

### 9.2 Argomenti da riga di comando

Uso `argparse` per creare una CLI semplice:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Tool di esempio della Stazione")
    parser.add_argument("--input", required=True, help="Path al file di input")
    args = parser.parse_args()
    print(f"Uso il file: {args.input}")

if __name__ == "__main__":
    main()
```

Questo permette:

- invocazione da terminale
- integrazione con script e automazioni

---

## 10. Cenni di async (opzionale)

In molti casi ML/LLM/OSINT inizierò a voler fare chiamate API in parallelo:

- per ora è sufficiente **sapere che esiste** l’approccio async
- in moduli successivi posso introdurre `asyncio` e `httpx.AsyncClient`

Esempio minimale (solo a livello concettuale):

```python
import asyncio
import httpx

async def fetch(client, url):
    resp = await client.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

async def main():
    async with httpx.AsyncClient() as client:
        data = await fetch(client, "https://httpbin.org/get")
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

Non è necessario padroneggiare subito l’async: basta sapere che questa strada esiste
e che diventa utile quando ho **molte** chiamate IO-bound.

---

## 11. Progetto finale di consolidamento (schema)

### 11.1 Obiettivo

Creare un mini-progetto standard che userò come **scheletro riutilizzabile**:

- client API  
- logging  
- config/segretI  
- test con `pytest`  
- CLI per lanciare operazioni

### 11.2 Specifica di massima

Il progetto deve:

- leggere una config da `config/settings.yaml` (es. `base_url`, `timeout`)
- leggere una chiave API da variabile d’ambiente
- esporre una funzione `run()` in `main.py` che:
  - chiama un endpoint di test (es. `GET /status`)  
  - logga richiesta e risposta  
  - scrive un evento JSONL in `logs/events.jsonl`  
- avere almeno 1–2 test che:
  - mockano l’API o testano funzioni pure  
  - girano con `pytest`

Questo modulo non richiede che il progetto sia perfetto:
basta che sia **coerente** e riutilizzabile.

---

## 12. Laboratori ed esercizi

### Laboratorio 1 — Setup ambiente e “Hello, logs”

**Obiettivo:** configurare ambiente Python + logging base.

**Passi:**

1. Creare una nuova cartella di progetto (es. `stazione-python-demo/`).
2. Inizializzare ambiente virtuale (o `uv`/`pipx`) e installare `requests` e `pytest`.
3. Creare `src/my_project/main.py` con un semplice `print`.
4. Aggiungere logging come nell’esempio della sezione 5.1.

**Deliverable:**

- progetto minimale con logging funzionante su console + file.

---

### Laboratorio 2 — File JSONL e log strutturati

**Obiettivo:** leggere/scrivere JSONL per log/analisi in stile OSINT/LLM.

**Passi:**

1. Creare una funzione che scrive eventi in `logs/events.jsonl`.
2. Creare uno script che legge il file e stampa il numero di eventi per tipo.
3. Aggiungere un test che verifica il corretto parsing di una riga JSONL.

**Deliverable:**

- file `logs/events.jsonl` con alcuni eventi
- test che passa su una funzione di parsing

---

### Laboratorio 3 — Mini client HTTP con config e segreti

**Obiettivo:** esercitarsi con API, config e variabili d’ambiente.

**Passi:**

1. Creare `config/settings.example.yaml` con `base_url` e `timeout`.
2. Scrivere un modulo `api_client.py` che legge la config e chiama `GET /get` su `https://httpbin.org`.
3. Usare una variabile d’ambiente fittizia (es. `MY_DEMO_TOKEN`) e loggare se è presente o meno.
4. Aggiungere un test che verifica il comportamento di una funzione pura (es. generazione header).

**Deliverable:**

- file di config + client API funzionante
- almeno un test che gira con `pytest`

---

### Laboratorio 4 — CLI “stazione-cli”

**Obiettivo:** creare una CLI che usa le funzioni precedenti.

**Passi:**

1. In `main.py`, creare una CLI con `argparse` che:
   - accetta un parametro `--mode` (es. `status`, `dump-logs`)
2. In modalità `status`, chiama il client API e stampa/ logga il risultato.
3. In modalità `dump-logs`, legge `logs/events.jsonl` e stampa un riepilogo.

**Deliverable:**

- CLI utilizzabile da riga di comando
- screenshot o log di esempio che mostra le due modalità

---

## 13. Rubriche e checklist

### Checklist — D02 completato

- [ ] Ho un ambiente Python configurato (3.11+, virtualenv/uv).
- [ ] Ho almeno un progetto con struttura `src/`, `tests/`, `logs/`, `config/`.
- [ ] So leggere/scrivere file di testo, JSON e JSONL.
- [ ] Ho configurato logging su file + console.
- [ ] Gestisco almeno una chiave API via variabili d’ambiente (niente token hard-coded).
- [ ] Ho scritto almeno un test con `pytest` che gira con successo.
- [ ] Ho una CLI minimale per eseguire funzioni del progetto.

### Errori tipici da evitare

- mescolare codice, config e dati nella stessa cartella senza criterio.
- non usare ambienti virtuali e installare tutto globalmente.
- hard-codare URL, token o path direttamente nel codice.
- affidarsi solo a `print` invece che a logging strutturato.
- non scrivere **nessun** test, rendendo ogni modifica rischiosa.

### Segnali che “ho davvero capito” D02

- posso creare un nuovo progetto Python “pulito” in meno di 10–15 minuti.
- so spiegare perché uso JSONL per log/dataset invece di un unico JSON.
- so aggiungere una nuova opzione alla CLI senza rompere nulla.
- so aggiungere un test per una funzione nuova o modificata prima di usarla altrove.

---

## 14. Come ripartire dopo una pausa

Se torno su D02 dopo giorni o settimane:

1. Apro il progetto Python di riferimento (quello del laboratorio 3/4).
2. Eseguo i test con `pytest -q` per vedere se tutto è ancora verde.
3. Lancio la CLI (es. `python -m my_project.main --mode status`) e verifico che funziona.
4. Scelgo un micro-task:
   - aggiungere un nuovo comando alla CLI
   - scrivere un test in più
   - migliorare la gestione dei log o della config
5. Aggiorno una nota in `private/notes/` con:
   - cosa ho fatto in questa sessione
   - quale miglioramento vorrei fare la prossima volta

L’obiettivo è **non ripartire da zero**: uso il progetto consolidato come ancora,
faccio un piccolo passo e lascio tracce per il “me futuro”.

---

## 15. Risorse consigliate

### 15.1 Documentazione ufficiale Python

- **The Python Tutorial (Python 3)**  
  Tutorial ufficiale con introduzione, strutture dati, moduli, IO, errori, classi.  
  https://docs.python.org/3/tutorial/index.html

- **Python Documentation & Getting Started**  
  Hub della documentazione ufficiale + sezione “Python for beginners”.  
  https://www.python.org/doc/  
  https://www.python.org/about/gettingstarted/

### 15.2 Guide e best practice

- **The Hitchhiker’s Guide to Python**  
  Guida “opinionated” all’uso quotidiano di Python, con best practice su installazione, ambienti, tool.  
  https://docs.python-guide.org/

### 15.3 Tutorial e percorsi strutturati

- **Real Python** — articoli e corsi  
  Tutorial di qualità su quasi ogni aspetto di Python (HTTP, logging, test, CLI, ecc.).  
  https://realpython.com/  
  Panoramica dei learning path (beginner → advanced):  
  https://realpython.com/learning-paths/  

Queste risorse non vanno consumate tutte in una volta: le tengo come “toolbox”,
da cui pescare articoli e sezioni quando, durante i moduli successivi,
emerge un punto debole (es. logging avanzato, async, testing più strutturato).