# D02 — Python refresher e software engineering essentials

## Perché questo documento

Questo documento è un **ripasso mirato di Python** e delle basi di *software engineering* che mi servono
per tutto il resto del percorso (ML, LLM, agenti, pipeline OSINT).

Non vuole insegnare Python da zero: dà una struttura essenziale e rende espliciti
gli standard che userò per:

- script, notebook e piccoli tool
- chiamate API
- gestione di configurazione e segreti
- logging, error handling e test

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- lavorare in un **ambiente Python riproducibile** (virtualenv/uv, requirements)
- scrivere script e moduli leggibili, con funzioni ben definite
- leggere/scrivere file (JSON, JSONL), loggare e gestire errori in modo sensato
- chiamare API HTTP in modo robusto
- scrivere test base con `pytest`
- impacchettare un piccolo progetto di esempio (client API + logging + test)

---

## 1. Mappa degli argomenti

### 1.1 Blocchi principali

1. Setup ambiente Python (versione, virtualenv, gestione dipendenze).
2. Sintassi base e strutture dati (refresher).
3. File, JSON/JSONL, path.
4. Logging ed error handling.
5. Configurazione e segreti.
6. HTTP e API.
7. Test con `pytest`.
8. Piccola CLI / script eseguibile.
9. Progetto finale di consolidamento.

---

## 2. Setup ambiente Python

### 2.1 Versione e installazione

Per coerenza con librerie ML/LLM moderne:

- uso Python 3.11 o superiore, se possibile;
- su macOS e Windows mantengo **un’installazione “di sistema”** e creo ambienti isolati per i progetti.

Riferimenti:

- Documentazione ufficiale Python (installazione e tutorial):  
  https://www.python.org/doc/  
  https://docs.python.org/3/tutorial/index.html

### 2.2 Ambienti virtuali e gestione dipendenze

Approccio consigliato:

- uso `venv` o uno strumento moderno (es. `uv`, `pipx`) per isolare le dipendenze di ciascun progetto;
- ogni progetto ha il suo file di requisiti (`requirements.txt` o equivalente).

Esempio con `venv`:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# oppure
.\.venv\Scripts\activate   # Windows

pip install -U pip
pip install requests pytest
```

---

## 3. Refresher sintassi e strutture dati

### 3.1 Tipi base e controllo di flusso

Verifico di sentirmi solido su:

- tipi base: `int`, `float`, `str`, `bool`
- strutture: `list`, `dict`, `set`, `tuple`
- `if/elif/else`, `for`, `while`, comprensioni di lista
- funzioni con parametri di default e keyword arguments

Se qualcosa scricchiola:

- riprendo sezioni mirate dal *Python Tutorial*:  
  https://docs.python.org/3/tutorial/introduction.html

### 3.2 Strutture dati “che uso davvero”

Per questo percorso, le più usate sono:

- `list` di dict (es. righe di un JSONL)
- `dict` annidati per configurazioni e risposte API
- `Path` (da `pathlib`) per gestire file e directory in modo cross-platform

Esempio:

```python
from pathlib import Path

data_dir = Path("data")
for json_file in data_dir.glob("*.json"):
    print(json_file.name)
```

---

## 4. File, JSON e JSONL

### 4.1 Lettura/scrittura file di testo

Uso costantemente file di testo (`.txt`, `.md`, `.log`):

```python
from pathlib import Path

file_path = Path("notes") / "example.md"

text = file_path.read_text(encoding="utf-8")
file_path.write_text(text + "\n\nNuova nota.", encoding="utf-8")
```

### 4.2 JSON e JSONL

Per lavorare con dati strutturati:

- **JSON**: un oggetto completo per file.
- **JSONL**: un oggetto JSON per riga, formato comodo per dataset e log.

Esempio JSONL:

```python
import json
from pathlib import Path

log_path = Path("logs") / "events.jsonl"

event = {"type": "api_call", "status": "ok"}
with log_path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

---

## 5. Logging ed error handling

### 5.1 Logging

Uso il modulo `logging` invece di `print` per:

- separare livelli (info, warning, error)
- scrivere log su file
- filtrare output a seconda dell’ambiente (dev/prod)

Esempio:

```python
import logging
from pathlib import Path

log_file = Path("logs") / "app.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logging.info("Applicazione avviata")
```

### 5.2 Error handling

Regola pratica:

- non catturare tutto (“`except Exception`” ovunque) senza loggare;
- usare `try`/`except` dove ha senso e loggare errori con contesto.

Esempio:

```python
try:
    response = call_api(...)
except Exception as e:
    logging.exception("Errore nella chiamata API: %s", e)
    # eventualmente rilancio o gestisco in modo chiaro
```

---

## 6. Configurazione e segreti

### 6.1 File di configurazione

Non hard-codare nel codice:

- URL di API
- path di cartelle
- timeouts
- nomi di indici

Uso file `.env`, `.ini` o `.yaml` letti all’avvio dell’app.

### 6.2 Segreti e variabili d’ambiente

Qualunque chiave API o token deve stare:

- in variabile d’ambiente
- in `.env` *non* versionato (es. ignorato in `.gitignore`)

Esempio con `os.environ`:

```python
import os

api_key = os.environ.get("MY_API_KEY")
if not api_key:
    raise RuntimeError("MY_API_KEY non impostata")
```

---

## 7. HTTP e API

### 7.1 Chiamate HTTP di base

Per lavorare con API (LLM, servizi esterni) userò una libreria come `requests` o `httpx`.

Esempio con `requests`:

```python
import requests

resp = requests.get("https://httpbin.org/get", timeout=10)
resp.raise_for_status()
data = resp.json()
```

Buone pratiche:

- impostare `timeout`
- gestire errori (`raise_for_status`, try/except)
- loggare endpoint e status code

---

## 8. Test con pytest

### 8.1 Perché test

Anche per script “personali”, un minimo di test:

- evita regressioni quando modifico funzioni usate in più progetti
- dà più sicurezza quando integro strumenti diversi (OSINT, LLM, agenti)

### 8.2 Struttura minima

- cartella `tests/`
- file `test_xxx.py`
- funzioni che iniziano con `test_`

Esempio:

```python
# src/math_utils.py
def add(a, b):
    return a + b

# tests/test_math_utils.py
from src.math_utils import add

def test_add():
    assert add(2, 3) == 5
```

Esecuzione:

```bash
pytest -q
```

---

## 9. Script e CLI di base

### 9.1 Script eseguibili

Per creare un entrypoint:

```python
# src/main.py
def main():
    print("Ciao dalla Stazione!")

if __name__ == "__main__":
    main()
```

Esecuzione:

```bash
python -m src.main
```

### 9.2 Argomenti da riga di comando

Con `argparse` posso creare una CLI semplice:

```python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path al file di input")
    args = parser.parse_args()
    print(f"Uso il file: {args.input}")

if __name__ == "__main__":
    main()
```

---

## 10. Progetto finale di consolidamento (idea)

Un piccolo progetto che userò come “scheletro standard” nei moduli successivi:

- directory `src/` con:
  - `config.py` (lettura config/variabili d’ambiente)
  - `api_client.py` (chiamate HTTP con logging ed error handling)
  - `main.py` (entrypoint CLI)
- directory `tests/` con test minimi per `api_client.py`
- directory `logs/` per log applicativi
- file `requirements.txt` e istruzioni nel `README.md`

Questo mini-progetto verrà riutilizzato e ampliato quando parlerò di:

- integrazione con modelli LLM via API
- pipeline OSINT
- agenti che orchestrano chiamate API e scrivono log/note

---

## 11. Risorse consigliate

### 11.1 Documentazione ufficiale Python

- **Python Tutorial** (ufficiale):  
  https://docs.python.org/3/tutorial/index.html

- **Python per principianti** (entrypoint e risorse di base):  
  https://www.python.org/about/gettingstarted/  
  https://www.python.org/doc/

### 11.2 Guide e best practice

- **The Hitchhiker’s Guide to Python** (best practice per uso quotidiano di Python):  
  https://docs.python-guide.org/

- **Python.org — home e documentazione**  
  https://www.python.org/

### 11.3 Tutorial e percorsi strutturati

- **Real Python** — articoli e percorsi di apprendimento:  
  https://realpython.com/  
  Panoramica dei learning path (beginner → advanced):  
  https://realpython.com/learning-paths/

Queste risorse non vanno studiate per intero: le tengo come “toolbox” da cui pescare
articoli e sezioni in base ai punti che emergono come deboli durante il lavoro sui moduli successivi.

---

## 12. Prossimi passi per me

- Verificare la mia confidenza scrivendo uno script che:
  - legge config e segreti
  - chiama una piccola API pubblica
  - logga risultati e errori
  - ha almeno 1–2 test con `pytest`
- Aggiornare questo documento con snippet di codice reali
  che uso nei progetti OSINT/LLM.
- Riutilizzare la struttura del progetto finale come base comuni
  per i moduli su ML, LLM e agenti.