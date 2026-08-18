# D15 — MLOps / LLMOps e deployment local-first

## Meta-modulo D15

**Target**  
Me stesso oggi, e chiunque voglia mettere in produzione sistemi di ML/LLM in modo affidabile,
ripetibile e sicuro, con attenzione al deployment local-first (on-prem, edge, ambienti controllati)
e all’integrazione con pipeline OSINT/agenti.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D08 — Deep Learning e PyTorch
- D09 — Transformers, LLM e inference engineering
- D12 — Agentic systems, MCP e automazione affidabile

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - cos’è MLOps / LLMOps  
  - packaging di modelli e codice  
  - serving base (API locale)

- **Modalità standard (~8–10 ore)**  
  - versioning di modelli e dataset  
  - CI/CD per ML/LLM  
  - monitoring (performance, drift, errori)  
  - deployment local-first (Docker, on-prem, edge)

- **Modalità deep dive (più giornate)**  
  - pipeline end-to-end (training → validation → deployment → monitoring)  
  - ottimizzazione inferenza (quantizzazione, batching, caching)  
  - sicurezza e governance in produzione

**Quando considerare il modulo “completato”**

- so spiegare differenza tra ML engineering “artigianale” e MLOps/LLMOps
- so pacchettizzare un modello e servirlo via API
- so versionare modelli e dataset in modo sensato
- ho almeno una pipeline CI/CD base per un progetto ML/LLM
- so progettare deployment local-first (Docker, on-prem, edge) con monitoring

---

## Perché questo documento

Dopo D14 ho consapevolezza su etica, sicurezza e governance, ma mi manca il “come” operativo
per mettere in produzione sistemi ML/LLM:

- come gestisco versioni di modelli e dataset
- come automatizzo training, validation, deployment
- come servo modelli in produzione (API, batch, agenti)
- come monitoro performance, drift, errori
- come progetto deployment local-first (on-prem, edge, ambienti controllati)

Questo modulo mette insieme:

- MLOps classico (modelli tabellari, visione, ecc.)
- LLMOps (LLM, RAG, agenti)
- deployment local-first (Docker, on-prem, edge, ambienti isolati)

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere cos’è MLOps / LLMOps e perché serve
- pacchettizzare un modello e servirlo via API
- versionare modelli e dataset in modo sensato
- progettare pipeline CI/CD per ML/LLM
- monitorare performance, drift, errori in produzione
- progettare deployment local-first (Docker, on-prem, edge)

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Cos’è MLOps / LLMOps.
2. Packaging di modelli e codice.
3. Versioning di modelli e dataset.
4. CI/CD per ML/LLM.
5. Serving e deployment (API, batch, agenti).
6. Monitoring (performance, drift, errori).
7. Deployment local-first (Docker, on-prem, edge).
8. Sicurezza e governance in produzione.

---

## 2. Cos’è MLOps / LLMOps

### 2.1 MLOps

**MLOps** = insieme di pratiche per gestire il ciclo di vita dei sistemi di ML in produzione:

- sviluppo (training, validation)
- deployment (packaging, serving)
- monitoring (performance, drift, errori)
- manutenzione (aggiornamenti, rollback)

Obiettivi:

- riproducibilità (stessi risultati con stessi dati/codice)
- affidabilità (sistemi stabili, monitorati)
- scalabilità (gestire più modelli, più versioni)

### 2.2 LLMOps

**LLMOps** = MLOps applicato a LLM e sistemi basati su transformer:

- gestione di modelli grandi (centinaia di GB)
- RAG, agenti, tool calling
- monitoring di prompt, risposte, costi, latenza

Differenze rispetto a MLOps classico:

- modelli più grandi e costosi da addestrare/spostare
- più enfasi su inference che su training in-house
- più complessità nel monitoring (prompt, allucinazioni, costi token)

---

## 3. Packaging di modelli e codice

### 3.1 Perché pacchettizzare

Problemi senza packaging:

- “funziona sulla mia macchina”
- dipendenze non tracciate
- difficoltà a deployare su altri ambienti

Soluzione:

- pacchettizzare:
  - codice (script, moduli)
  - dipendenze (requirements, environment)
  - modelli (pesi, config)
  - dati (o riferimenti a dataset)

### 3.2 Strumenti

- **requirements.txt / pyproject.toml**  
  dipendenze Python

- **virtualenv / conda / uv**  
  ambienti isolati

- **Docker**  
  container con OS, dipendenze, codice, modelli

- **MLflow / DVC / WandB**  
  tracking esperimenti, versioning modelli

Riferimenti:

- [Docker docs](https://docs.docker.com/)
- [MLflow docs](https://mlflow.org/docs/latest/index.html)

---

## 4. Versioning di modelli e dataset

### 4.1 Versioning codice

- Git per codice (script, config, pipeline)
- branch per feature, esperimenti, release

### 4.2 Versioning dataset

- **DVC (Data Version Control)**  
  versioning di dataset grandi su storage esterno (S3, GCS, locale)

- **lakehouse / data lake**  
  storage strutturato per dataset (Delta Lake, Iceberg, ecc.)

- **metadata**  
  tracciare:
  - fonte
  - data di raccolta
  - pre-processing applicato
  - versione

### 4.3 Versioning modelli

- **MLflow Models**  
  registry di modelli con versioni, stage (staging, production)

- **Hugging Face Hub**  
  repository di modelli con versioning

- **naming convention**  
  es. `model-task-v1.2.3`, `model-date-metric`

Riferimenti:

- [DVC docs](https://dvc.org/doc)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)

---

## 5. CI/CD per ML/LLM

### 5.1 CI (Continuous Integration)

- automatizzare:
  - test (unitari, integrazione)
  - linting, formatting
  - training/validation su dataset piccoli

Strumenti:

- **GitHub Actions, GitLab CI, CircleCI**  
  pipeline CI

- **pytest, flake8, black**  
  test e qualità codice

### 5.2 CD (Continuous Deployment)

- automatizzare:
  - build di immagini Docker
  - deployment su ambienti (staging, production)
  - rollback in caso di problemi

Pattern:

- **blue/green deployment**  
  due ambienti, switch graduale

- **canary release**  
  deployment graduale su frazione di utenti

Riferimenti:

- [GitHub Actions docs](https://docs.github.com/en/actions)

---

## 6. Serving e deployment

### 6.1 Serving modelli

Pattern:

- **API REST**  
  endpoint `/predict` che riceve input e restituisce output

- **batch inference**  
  elaborazione periodica di dataset (es. nightly job)

- **streaming**  
  elaborazione in tempo reale (es. Kafka, Kinesis)

Strumenti:

- **FastAPI, Flask**  
  API Python

- **TorchServe, Triton Inference Server**  
  serving ottimizzato per modelli deep learning

- **vLLM, TGI (Text Generation Inference)**  
  serving ottimizzato per LLM

Riferimenti:

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Triton docs](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/)

### 6.2 Deployment local-first

**Local-first** = privilegiare deployment in ambienti controllati:

- on-prem (server locali, data center)
- edge (dispositivi periferici, IoT)
- ambienti isolati (VM, container, reti private)

Vantaggi:

- controllo totale su dati e modelli
- minore dipendenza da cloud
- migliore compliance (GDPR, policy interne)

Svantaggi:

- gestione infrastruttura a carico proprio
- scaling più complesso

Strumenti:

- **Docker, Docker Compose**  
  containerizzazione

- **Kubernetes (K8s)**  
  orchestrazione container (anche on-prem)

- **Ollama, llama.cpp**  
  inference locale per LLM

---

## 7. Monitoring

### 7.1 Cosa monitorare

- **performance**: latenza, throughput, errori
- **drift**: cambiamento distribuzione dati/input nel tempo
- **qualità**: accuratezza, allucinazioni, feedback utenti
- **costi**: token, GPU, storage

### 7.2 Strumenti

- **Prometheus + Grafana**  
  metriche e dashboard

- **ELK stack (Elasticsearch, Logstash, Kibana)**  
  log e analisi

- **Evidently AI, Arize, WhyLabs**  
  monitoring drift e qualità per ML/LLM

- **LLM-specific**:  
  tracking prompt, risposte, costi, feedback

Riferimenti:

- [Prometheus docs](https://prometheus.io/docs/)
- [Evidently AI docs](https://docs.evidentlyai.com/)

### 7.3 Alerting

- definire threshold (es. latenza > X, errore rate > Y)
- configurare alert (email, Slack, PagerDuty)
- avere procedure di risposta (chi fa cosa, come rollback)

---

## 8. Sicurezza e governance in produzione

### 8.1 Sicurezza

- **isolamento**: container, VM, reti private
- **autenticazione/autorizzazione**: API key, OAuth, ruoli
- **encryption**: dati in transito (TLS) e a riposo
- **audit log**: tracciare accessi e azioni

### 8.2 Governance

- **policy di deployment**: chi può deployare, come, con quali approvazioni
- **change management**: documentare cambiamenti (modelli, config, codice)
- **incident response**: procedure per incidenti (sicurezza, performance, errori)

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Packaging modello e API base

**Obiettivo:** pacchettizzare un modello e servirlo via API.

**Passi:**

1. Scegliere un modello (ML classico o LLM).
2. Creare script di inference (caricamento modello, predizione).
3. Creare `requirements.txt` con dipendenze.
4. Creare API con FastAPI:
   - endpoint `/predict` che riceve input e restituisce output
5. Testare API localmente (curl, Postman).
6. Annotare:
   - problemi di dipendenze
   - latenza e throughput

**Deliverable:**

- script modello + API FastAPI
- nota con osservazioni

---

### Laboratorio 2 — Dockerizzazione

**Obiettivo:** creare immagine Docker per il modello.

**Passi:**

1. Scrivere `Dockerfile`:
   - base image (es. `python:3.11-slim`)
   - installazione dipendenze
   - copia codice e modello
   - comando di avvio (API)
2. Build immagine: `docker build -t my-model:latest .`
3. Run container: `docker run -p 8000:8000 my-model:latest`
4. Testare API da host.
5. Annotare:
   - problemi di build/run
   - dimensioni immagine

**Deliverable:**

- Dockerfile + immagine
- nota con osservazioni

---

### Laboratorio 3 — CI/CD base con GitHub Actions

**Obiettivo:** automatizzare test e build.

**Passi:**

1. Creare workflow GitHub Actions:
   - trigger su push/PR
   - step: checkout, setup Python, install dipendenze, test
2. Aggiungere step di build Docker (opzionale).
3. Testare workflow su push.
4. Annotare:
   - tempi di esecuzione
   - errori comuni

**Deliverable:**

- file `.github/workflows/ci.yml`
- nota con osservazioni

---

### Laboratorio 4 — Monitoring base con Prometheus/Grafana

**Obiettivo:** monitorare latenza e errori.

**Passi:**

1. Aggiungere metriche all’API (es. con `prometheus_client`):
   - latenza per richiesta
   - conteggio errori
2. Deploy Prometheus + Grafana (Docker Compose).
3. Configurare dashboard per metriche.
4. Simulare carico (es. con `locust` o script semplice).
5. Annotare:
   - pattern di latenza/errori
   - utilità dashboard

**Deliverable:**

- config Prometheus/Grafana + dashboard
- nota con osservazioni

---

## 10. Rubriche e checklist

### Checklist — D15 completato

- [ ] So spiegare cos’è MLOps / LLMOps e perché serve.
- [ ] So pacchettizzare un modello e servirlo via API.
- [ ] So versionare modelli e dataset in modo sensato.
- [ ] Ho progettato una pipeline CI/CD base per un progetto ML/LLM.
- [ ] So monitorare performance, drift, errori in produzione.
- [ ] So progettare deployment local-first (Docker, on-prem, edge).

### Errori tipici da evitare

- non versionare modelli e dataset (impossibile riprodurre risultati).
- deployare senza test automatizzati (rischio errori in produzione).
- ignorare monitoring (nessuna visibilità su problemi).
- sottovalutare sicurezza (API esposte senza autenticazione).
- non avere procedure di rollback (incidenti più lunghi e dannosi).

### Segnali che “ho davvero capito” D15

- posso prendere un modello e metterlo in produzione in modo strutturato.
- so spiegare a un collega differenza tra ML engineering “artigianale” e MLOps.
- so progettare pipeline CI/CD e monitoring per sistemi reali.
- vedo deployment local-first come scelta strategica, non come ripiego.

---

## 11. Come ripartire dopo una pausa

Se torno su D15 dopo giorni o settimane:

1. Riapro un progetto ML/LLM già pacchettizzato.
2. Rieseguo build e test per ricordare il flusso.
3. Aggiungo una piccola modifica:
   - nuova metrica di monitoring
   - miglioramento CI/CD
   - ottimizzazione Docker
4. Aggiorno una nota con:
   - cosa ho cambiato
   - effetto su performance/manutenibilità

Scopo: mantenere fresco il legame tra teoria (MLOps/LLMOps) e pratica (pipeline, deployment).

---

## 12. Risorse consigliate

### 12.1 MLOps / LLMOps

- **Made With ML (corso online)**  
  Introduzione a MLOps end-to-end.  
  https://madewithml.com/  

- **Full Stack Deep Learning (corso)**  
  MLOps, deployment, monitoring.  
  https://fullstackdeeplearning.com/  

- **Hugging Face MLOps course**  
  LLMOps con Hugging Face.  
  https://huggingface.co/learn/  

### 12.2 Strumenti

- **Docker docs**  
  https://docs.docker.com/  

- **MLflow docs**  
  https://mlflow.org/docs/latest/index.html  

- **DVC docs**  
  https://dvc.org/doc  

- **FastAPI docs**  
  https://fastapi.tiangolo.com/  

- **Prometheus docs**  
  https://prometheus.io/docs/  

### 12.3 Sicurezza e governance

- **OWASP Top 10 for LLM**  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/  

- **NIST AI Risk Management Framework**  
  https://www.nist.gov/itl/ai-risk-management-framework  

Queste risorse non vanno studiate per intero: D15 serve a darti una mappa operativa
per mettere in produzione sistemi ML/LLM in modo affidabile, e a collegarti a tool quando serve approfondire.