---
aliases:
- D02
- Python Refresher
- Software Engineering Python
- Python per AI
- Ingegneria del Software Python
resources:
- title: 'Corey Schafer: Python OOP Tutorial'
  url: https://www.youtube.com/watch?v=ZDa-Z5JzLYM
  type: video
- title: Real Python Learning Paths
  url: https://realpython.com/learning-paths/
  type: ref
- title: Pytest Official Docs
  url: https://docs.pytest.org/
  type: ref
---
# Ingegneria del Software e Python Essentials per Pipeline AI

L'**ingegneria del software in Python per l'intelligenza artificiale** è la disciplina che applica pattern di progettazione modulari, isolamento degli ambienti, gestione robusta dell'I/O e testing automatizzato allo sviluppo di pipeline di machine learning e strumenti di analisi OSINT. Questa metodologia si adotta in contesti operativi e di ricerca per trasformare prototipi sperimentali in servizi software affidabili, manutenibili e facilmente integrabili in architetture agentiche. La disciplina esiste perché la resilienza di un sistema AI non dipende unicamente dalla complessità algoritmica dei modelli, ma dalla robustezza dell'infrastruttura di codice sottostante, dalla riproducibilità deterministica delle dipendenze e dalla protezione rigorosa delle chiavi crittografiche.

> [!TIP] Spiegato Semplice: Perché usare "Python" e i "Moduli"?
> Immagina Python come una gigantesca scatola di costruzioni LEGO. Invece di dover creare ogni singolo mattoncino da zero, puoi scaricare scatole piene di pezzi speciali già fatti da altri (i famosi "Pacchetti"). 

> [!NOTE] L'Analogia in Pratica
> "Ingegneria del Software" significa semplicemente costruire astronavi LEGO usando tanti moduli separati. Se si rompe l'ala (uno script), sostituisci solo quell'ala, senza dover buttare via l'intera astronave (il codice monolitico)! E i "Test" sono come un collaudo di sicurezza: prima di far volare la navicella, un mini-robot controlla in automatico che tutti i pezzi siano attaccati bene.

## Il Problema dello Script Monolitico e dei Notebook Sperimentali

Nelle fasi esplorative di analisi dati e prototipazione di modelli AI, è comune concentrare l'intera logica computazionale all'interno di singoli script monolitici o di notebook interattivi come [Jupyter](https://jupyter.org/). Sebbene questo approccio consenta una validazione immediata delle ipotesi, si rivela fragile e inadeguato quando il codice deve essere eseguito in modo non presidiato, integrato in pipeline di Continuous Integration o scalato su grandi volumi di dati.

> [!TIP]
> **💡 L'Importanza Pratica di Jupyter**
> Anche se la messa in produzione richiede script modulari, **Jupyter Notebook** (o il suo equivalente cloud Google Colab) resta lo standard industriale per la sperimentazione esplorativa (*Exploratory Data Analysis*), la prototipazione rapida e la visualizzazione interattiva dei dati. È uno strumento formidabile ed essenziale da conoscere per testare velocemente nuove idee e visualizzare grafici prima di cristallizzare il codice in moduli Python definitivi.

I notebook interattivi memorizzano lo stato globale delle variabili in memoria volatile in modo dipendente dall'ordine cronologico con cui l'utente esegue le celle. L'esecuzione non sequenziale genera inconsistenze silenti e comportamenti non riproducibili, mentre il loro formato JSON interno rende complessa la revisione del codice e la risoluzione dei conflitti su sistemi di controllo versione come [Git](https://git-scm.com/) (il sistema di controllo versione distribuito open-source). Parallelamente, gli script monolitici che incorporano credenziali API cablate nel sorgente (*hardcoding*) o percorsi assoluti violano le buone pratiche di sicurezza e collassano sistematicamente in presenza di latenze di rete anomale o errori temporanei del server.

La soluzione ingegneristica consiste nell'adottare un'architettura modulare a pacchetti, isolare le librerie mediante ambienti virtuali dedicati, esternalizzare le configurazioni parametriche in variabili d'ambiente protette e strutturare suite di test automatici con [pytest](https://docs.pytest.org/) (il framework di testing per il linguaggio Python) per garantire la non-regressione a ogni ciclo di rilascio.

## Architettura del Progetto e Layout Standard

Una struttura di directory standardizzata garantisce la netta separazione delle responsabilità tra logica di business, configurazioni, test ed emissione dei log operativi.

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
│   └── app.log
├── .env.example
├── requirements.txt
└── README.md
```

La directory `src/` racchiude esclusivamente i moduli sorgente del pacchetto applicativo, isolandoli dalla suite di collaudo collocata in `tests/`. Le configurazioni parametriche e i file di template per le variabili d'ambiente risiedono in `config/` e `.env.example`, mentre la cartella `logs/` raccoglie le tracce diagnostiche generate a runtime. L'entry point applicativo è definito in `main.py`, orchestrando i moduli specializzati senza generare dipendenze circolari.

## Isolamento delle Dipendenze e Ambienti Virtuali

L'installazione globale di pacchetti [Python](https://www.python.org/) (il linguaggio di programmazione di riferimento per l'AI) sul sistema operativo genera conflitti di versione insanabili (*dependency hell*) tra librerie condivise da progetti differenti. L'isolamento mediante ambienti virtuali assicura l'indipendenza e la perfetta riproducibilità di ciascun ambiente di esecuzione.

### Creazione e Attivazione dell'Ambiente Virtuale

Il modulo standard `venv` consente di creare una sandbox isolata contenente una copia dedicata dell'interprete Python e dell'albero dei pacchetti `site-packages`.

```bash
# Creazione dell'ambiente virtuale dedicato
python -m venv .venv

# Attivazione dell'ambiente su sistemi macOS e Linux
source .venv/bin/activate

# Attivazione dell'ambiente su sistemi Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Aggiornamento del package manager e installazione delle dipendenze essenziali
pip install -U pip
pip install requests pytest httpx pyyaml
```

### Congelamento e Dichiarazione delle Dipendenze

Le dipendenze del progetto vengono tracciate in modo deterministico all'interno di `requirements.txt`. Questo file garantisce che altri sviluppatori, runner di Continuous Integration o agenti automatici possano riprodurre fedelmente l'esatto ambiente software con un unico comando di ripristino (`pip install -r requirements.txt`).

## Manipolazione del File System e Flussi Dati (JSON vs JSONL)

L'elaborazione di dati non strutturati, log di rete e dataset di training richiede costrutti solidi e portabili per l'accesso ai file su disco.

### Navigazione Portabile dei Percorsi con Pathlib

L'impiego del modulo nativo `pathlib` sostituisce la fragile concatenazione manuale di stringhe con oggetti `Path` polimorfi, garantendo la compatibilità cross-platform tra separatori di percorso Windows (`\`) e POSIX (`/`).

```python
from pathlib import Path

# Navigazione e scansione iterativa di file JSON in una directory
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

for json_file in data_dir.glob("*.json"):
    print(f"Rilevato file: {json_file.name}")

# Lettura e scrittura atomica di file di testo
notes_path = Path("notes") / "example.md"
notes_path.parent.mkdir(exist_ok=True)

text_content = notes_path.read_text(encoding="utf-8") if notes_path.exists() else "Intestazione iniziale.\n"
notes_path.write_text(text_content + "Nuovo paragrafo di aggiornamento.\n", encoding="utf-8")
```

### Streaming ad Alta Efficienza con Formato JSONL

I file JSON convenzionali richiedono il parsing dell'intero albero gerarchico in memoria RAM prima di consentire l'accesso al primo elemento, provocando saturazione di memoria (*Out-Of-Memory*) in presenza di dataset massivi. Il formato **JSON Lines (JSONL)** risolve questo collo di bottiglia strutturando il file come sequenza di oggetti JSON indipendenti, ciascuno delimitato da un carattere di nuova riga (`\n`). Ciò consente l'elaborazione in streaming riga per riga con consumo costante di memoria ($O(1)$ rispetto alla dimensione del file).

```python
import json
from pathlib import Path

log_path = Path("logs") / "events.jsonl"
log_path.parent.mkdir(exist_ok=True)

# Scrittura append-only di eventi strutturati
event = {"type": "inference_request", "model": "llama-3", "status": "completed", "latency_ms": 142}
with log_path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")

# Lettura in streaming riga per riga
events = []
with log_path.open("r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            events.append(json.loads(line))
```

## Logging Strutturato e Gestione Robusta delle Eccezioni

L'utilizzo di istruzioni `print()` per il debug è un anti-pattern critico nei sistemi software: non fornisce timestamp, non supporta livelli di severità e non consente l'indirizzamento parallelo verso file di log e stream di console.

### Configurazione del Logging Multi-Destinazione

Il modulo nativo `logging` consente di configurare formati uniformi e handler multipli per registrare simultaneamente gli eventi operativi sia su file persistente che su console standard.

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
logger.info("Sistema inizializzato con successo.")
```

### Tracciamento e Rilancio Controllato delle Eccezioni

Il soffocamento cieco degli errori tramite blocchi `except: pass` nasconde anomalie critiche e corrompe lo stato applicativo. Le eccezioni devono essere intercettate in modo granulare e registrate con traccia di stack completa mediante `logger.exception()`.

```python
def execute_pipeline(payload: dict) -> dict:
    try:
        # Simulazione chiamata operativa
        if not payload.get("target"):
            raise ValueError("Il campo 'target' è obbligatorio nel payload.")
        return {"status": "success", "result": payload["target"].upper()}
    except Exception as e:
        logger.exception("Fallimento critico durante l'esecuzione della pipeline: %s", e)
        raise
```

## Gestione delle Configurazioni e Protezione dei Segreti

I parametri operativi variabili e i segreti crittografici non devono mai essere cablati (*hardcoded*) nel codice sorgente.

### Separazione dei Parametri in File YAML

I parametri non sensibili, come URL base, valori di timeout e livelli di logging, vengono formalizzati in file di configurazione strutturati in formato YAML.

```yaml
# config/settings.example.yaml
api:
  base_url: "https://api.example.com"
  timeout_seconds: 10
  max_retries: 3
logging:
  level: "INFO"
  format: "json"
```

### Acquisizione Sicura di Chiavi API da Variabili d'Ambiente

I token di autenticazione e le credenziali di accesso vengono iniettati a runtime tramite variabili d'ambiente di sistema o file `.env` locali esclusi dal versionamento Git.

```python
import os

API_KEY = os.environ.get("SERVICE_API_KEY")
if not API_KEY:
    raise RuntimeError("La variabile SERVICE_API_KEY non è impostata. Verificare il file .env o l'ambiente locale.")
```


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D02-python-refresher. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Client HTTP Resilienti e Pattern di Rete

Le interazioni con endpoint esterni, API di modelli linguistici e servizi OSINT richiedono client HTTP robusti in grado di gestire latenze variabili, disconnessioni temporanee ed errori di stato.

### Wrapper Modulare per Chiamate Sincrone con Requests

L'utilizzo della libreria [Requests](https://requests.readthedocs.io/) (il client HTTP sincrono per Python) richiede l'impostazione tassativa del parametro di timeout e la verifica esplicita dei codici di stato di risposta tramite `raise_for_status()`.

```python
import logging
import os
import requests

logger = logging.getLogger("my_project.api_client")
BASE_URL = os.environ.get("API_BASE_URL", "https://httpbin.org")

def fetch_resource(endpoint: str, timeout: int = 10, **kwargs) -> dict:
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    logger.info("Inoltro richiesta GET verso: %s", url)
    try:
        response = requests.get(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Errore di rete durante la richiesta a %s: %s", url, e)
        raise
```

## Collaudo Automatizzato con pytest e Interfacce CLI

La verifica automatica del codice e l'esposizione di parametri da riga di comando costituiscono i pilastri dell'automazione ingegneristica.

### Scrittura ed Esecuzione di Test Unitari

Il framework [pytest](https://docs.pytest.org/) individua ed esegue automaticamente i test definiti nella cartella `tests/`, verificando funzioni pure e moduli isolati mediante asserzioni native.

```python
# src/my_project/math_utils.py
def calculate_batch_offset(batch_index: int, batch_size: int) -> int:
    if batch_index < 0 or batch_size <= 0:
        raise ValueError("Parametri di batch non validi.")
    return batch_index * batch_size
```

```python
# tests/test_math_utils.py
import pytest
from my_project.math_utils import calculate_batch_offset

def test_calculate_batch_offset_standard():
    assert calculate_batch_offset(2, 50) == 100

def test_calculate_batch_offset_invalid():
    with pytest.raises(ValueError):
        calculate_batch_offset(-1, 50)
```

L'esecuzione dell'intera suite di collaudo dal terminale restituisce il resoconto analitico dello stato di conformità:

```bash
# Esecuzione della suite di test in modalità sintetica
pytest -q
```

### Costruzione di Interfacce da Linea di Comando con Argparse

L'esposizione di comandi CLI tramite il modulo nativo `argparse` consente a utenti umani, pipeline di orchestrazione e agenti software di parametrizzare l'esecuzione dello script.

```python
# src/my_project/main.py
import argparse
import sys

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Strumento CLI per pipeline AI Stazione")
    parser.add_argument("--input", required=True, help="Percorso del file dati di input")
    parser.add_argument("--mode", choices=["inspect", "process"], default="inspect", help="Modalità operativa")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    print(f"Esecuzione avviata in modalità '{args.mode}' sul target: {args.input}")

if __name__ == "__main__":
    main()
```

```bash
# Esecuzione del modulo principale tramite CLI
python -m my_project.main --input data/source.json --mode process
```

## Concorrenza Asincrona con Asyncio e HTTPX

Nelle pipeline OSINT ad alta intensità di I/O o nell'interrogazione parallela di molteplici modelli linguistici, il modello sincrono genera inefficienze e blocchi nell'attesa delle risposte di rete. La libreria [HTTPX](https://www.python-httpx.org/) (il client HTTP avanzato per Python con supporto asincrono e HTTP/2) integrata con `asyncio` abilita l'elaborazione concorrente non bloccante.

```python
import asyncio
import httpx

async def fetch_async(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url, timeout=10.0)
    response.raise_for_status()
    return response.json()

async def main_async():
    endpoints = [
        "https://httpbin.org/get?id=1",
        "https://httpbin.org/get?id=2",
        "https://httpbin.org/get?id=3",
    ]
    async with httpx.AsyncClient() as client:
        tasks = [fetch_async(client, url) for url in endpoints]
        results = await asyncio.gather(*tasks)
        print(f"Completate con successo {len(results)} richieste concorrenti.")

if __name__ == "__main__":
    asyncio.run(main_async())
```

## Compromessi Operativi e Analisi dei Limiti

L'adozione delle pratiche ingegneristiche in Python impone scelte ponderate in termini di complessità e risorse computazionali.

### Complessità del Paradigma Asincrono vs Semplicità Sincrona

Il codice asincrono basato su `asyncio` aumenta la densità logica e rende più complessa la diagnosi degli errori rispetto al codice sincrono sequenziale. L'asincronismo offre vantaggi tangibili unicamente per operazioni limitate dalla velocità di rete o disco (I/O-bound), mentre per carichi di lavoro ad alta intensità di calcolo (CPU-bound, come trasformazioni matematiche massive su matrici) non introduce benefici velocistici a causa del Global Interpreter Lock (GIL) di Python, richiedendo invece librerie C-backed come [NumPy](https://numpy.org/) (la libreria per il calcolo scientifico vettorializzato) o l'uso di multiprocessing.

### Overhead di Archiviazione dei Log e Gestione della Memoria

La registrazione prolungata di log strutturati su file JSONL produce file di grandi dimensioni che possono saturare lo spazio disco se non accompagnati da policy di rotazione (*log rotation*). Inoltre, l'elaborazione di flussi JSONL ad altissima frequenza richiede buffer di scrittura dedicati per evitare frammentazione delle operazioni di I/O sul disco.

## Riferimenti Bibliografici e Risorse Tecniche

### Standard di Linguaggio e Guide Ufficiali

La specifica della sintassi di base e dei tipi di dato nativi è documentata nel tutorial ufficiale [The Python Tutorial](https://docs.python.org/3/tutorial/index.html) (la guida autorevole curata dalla [Python Software Foundation](https://www.python.org/psf-landing/)). Le convenzioni di stile e architettura di progetto sono approfondite nel testo open-source [The Hitchhiker's Guide to Python](https://docs.python-guide.org/) (il manuale di riferimento sulle best practice di packaging e organizzazione del codice).

### Testing Avanzato e Percorsi di Formazione Specialistica

Per approfondire l'architettura dei test con fixture e mocking, la documentazione ufficiale di [pytest](https://docs.pytest.org/) fornisce linee guida complete per suite di collaudo industriali. La piattaforma indipendente [Real Python](https://realpython.com/) (il portale di formazione tecnica per programmatori Python) offre percorsi tematici dedicati all'ingegneria del software, alla concorrenza asincrona e alla costruzione di strumenti CLI nei suoi [Learning Paths](https://realpython.com/learning-paths/).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



- [ ] Configurazione dell'ambiente e logging strutturato: Creare la cartella di lavoro `stazione-python-lab/`, inizializzare l'ambiente virtuale con `python -m venv .venv`, attivarlo e configurare `main.py` per registrare messaggi informativi e di errore sia su standard output sia su file persistente `logs/app.log`.
- [ ] Elaborazione di dataset in formato JSONL: Scrivere uno script che genera dieci dizionari di test e li scrive in modalità append all'interno di `logs/events.jsonl`. Realizzare una seconda funzione che esegue lo streaming del file riga per riga, deserializza gli oggetti con `json.loads()` e calcola il conteggio aggregato degli eventi per tipologia.
- [ ] Client API resiliente con variabili d'ambiente: Implementare il modulo `src/my_project/api_client.py` con una funzione che acquisisce l'endpoint da configurazione YAML e la chiave di autorizzazione dalla variabile d'ambiente `SERVICE_API_KEY`, eseguendo una richiesta GET con timeout e gestione delle eccezioni di rete.
- [ ] Costruzione di interfaccia CLI e suite di test: Esporre i comandi di ispezione ed elaborazione tramite `argparse` all'interno di `main.py`. Creare la cartella `tests/`, implementare il test unitario per una funzione di utilità matematica e validare l'intera suite eseguendo `pytest -q`.