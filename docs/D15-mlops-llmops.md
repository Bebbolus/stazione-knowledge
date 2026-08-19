---
aliases: [D15, MLOps, LLMOps, Model Serving, Local Deployment, MLflow, Docker, Model Monitoring]
---

# MLOps, LLMOps e Ingegneria del Deployment Local-First

L'**MLOps** (Machine Learning Operations) e l'**LLMOps** (Large Language Model Operations) costituiscono l'insieme disciplinato di metodologie ingegneristiche, architetture software e strumenti di automazione per gestire l'intero ciclo di vita dei modelli predittivi e generativi in produzione, garantendo tracciabilità degli esperimenti, packaging immutabile, deployment ad alte prestazioni e monitoraggio continuo. Questa disciplina trova applicazione critica nell'erogazione di microservizi di inferenza ad alta affidabilità su workstation locali, server on-premise, edge device e cluster containerizzati operanti in ambienti controllati o isolati da Internet. L'ingegneria MLOps e LLMOps esiste per colmare la frattura strutturale tra il prototipo da laboratorio confinato nei notebook e il servizio software distribuito, prevenendo il debito tecnico nascosto, il decadimento silenzioso delle prestazioni dovuto al data drift e i colli di bottiglia computazionali e di memoria tipici dei moderni modelli di intelligenza artificiale.

## Il Problema dell'Operazionalizzazione del Machine Learning: Dal Prototipo da Laboratorio al Servizio di Produzione Affidabile

La transizione di un modello di intelligenza artificiale dall'ambiente di sviluppo esplorativo all'infrastruttura di produzione evidenzia una profonda asimmetria tra codice algoritmico e complessità infrastrutturale. Nello studio fondamentale condotto da D. Sculley e dai ricercatori di [Google](https://about.google/) intitolato *[Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/pub43146/)*, viene dimostrato come il codice di machine learning vero e proprio rappresenti solo una frazione minuscola (spesso inferiore al 10%) di un sistema operativo reale. L'architettura circostante è dominata da componenti critici deputati all'ingestion e alla pulizia dei dati, all'estrazione e validazione delle feature, alla gestione delle configurazioni, all'allocazione delle risorse hardware e al monitoraggio continuo delle prestazioni.

A differenza del software deterministico tradizionale, in cui il comportamento del sistema è interamente specificato dalla logica del codice sorgente, i sistemi di machine learning dipendono intrinsecamente dalla distribuzione statistica dei dati operativi. Un programma classico non cambia comportamento a parità di input a meno che non intervengano modifiche al codice; un modello di machine learning, al contrario, subisce un degrado prestazionale silenzioso quando la realtà esterna muta, generando fenomeni di *data drift* (spostamento della distribuzione delle variabili di ingresso $P(X)$) e *concept drift* (mutazione della relazione probabilistica tra input e target $P(Y \mid X)$).

I Jupyter Notebook, strumenti eccellenti per la prototipazione rapida e l'esplorazione visiva, manifestano gravi limiti architetturali se impiegati come unità di produzione. Lo stato mutabile e non lineare delle celle, l'assenza di type checking statico, l'impossibilità di eseguire test automatizzati e l'accoppiamento opaco con l'ambiente locale dell'utente impediscono la riproducibilità deterministica degli artefatti. L'ingegneria MLOps trasforma l'approccio artigianale in una pipeline software modulare, separando nettamente i carichi di elaborazione dati, l'addestramento distribuito e i microservizi di inferenza stateless.

Nell'ambito dei moderni modelli linguistici di grandi dimensioni, la disciplina si specializza in **LLMOps**. Mentre l'MLOps classico si concentra sull'addestramento periodico o incrementale di modelli tabellari, di regressione o di classificazione su larga scala con metriche di loss deterministiche, l'LLMOps affronta la gestione operativa di modelli fondazionali composti da miliardi di parametri già pre-addestrati. Le sfide dominanti dell'LLMOps riguardano l'ottimizzazione del recupero contestuale ([D10](D10-rag-knowledge-osint.md)), l'ingegneria dei prompt ([D12c](D12c-prompt-context-engineering.md)), la gestione della memoria della GPU (KV-cache) e la valutazione qualitativa delle risposte generate per mitigare allucinazioni e vulnerabilità di sicurezza ([D14](D14-responsible-ai-cyber.md)).

```text
+-----------------------------------------------------------------------------------------+
|                  IL DEBITO TECNICO NASCOSTO NEL MACHINE LEARNING (SCULLEY ET AL.)         |
+-----------------------------------------------------------------------------------------+

  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │ Raccolta e       │  │ Estrazione e     │  │ Validazione e    │  │ Gestione della   │
  │ Ingestion Dati   │  │ Feature Store    │  │ Pulizia Dati     │  │ Configurazione   │
  └─────────┬────────┘  └─────────┬────────┘  └─────────┬────────┘  └─────────┬────────┘
            │                     │                     │                     │
            ▼                     ▼                     ▼                     ▼
  ┌────────────────────────────────────────────────────────────────────────────────────┐
  │                     INFRASTRUTTURA DI ORCHESTRAZIONE E PIPELINE                    │
  │                                                                                    │
  │                              ┌──────────────────┐                                  │
  │                              │    CODICE ML     │                                  │
  │                              │ (Training/Infor) │                                  │
  │                              │     (~ 5-10%)    │                                  │
  │                              └────────┬─────────┘                                  │
  │                                       │                                            │
  └───────────────────────────────────────┼────────────────────────────────────────────┘
                                          │
            ┌─────────────────────────────┴────────────────────────────┐
            ▼                                                          ▼
  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │ Serving &        │  │ Gestione Risorse │  │ Telemetria &     │  │ Analisi Drift &  │
  │ Latenza Minima   │  │ GPU / CPU / RAM  │  │ Log Prometheus   │  │ Retraining Loop  │
  └──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```

## Tracciamento degli Esperimenti e Versionamento di Modelli e Dati: MLflow Tracking e DVC

La riproducibilità scientifica costituisce il requisito fondamentale per qualsiasi pipeline di machine learning. Durante la fase di sviluppo, gli sviluppatori esplorano decine di combinazioni di iperparametri, architetture neurali e sottoinsiemi di dati. Se i metadati e i pesi risultanti non vengono archiviati in modo sistematico, diventa impossibile risalire alla configurazione esatta che ha originato il modello in produzione, impedendo diagnosi di regressione o verifiche di conformità normativa.

La soluzione a questa frammentazione risiede nell'adozione combinata di [MLflow](https://mlflow.org/) (la piattaforma open-source per la gestione del ciclo di vita del machine learning, tracciamento esperimenti e model registry) e [DVC](https://dvc.org/) (lo strumento open-source di versionamento per dati e pipeline di machine learning integrato con [Git](https://git-scm.com/)). L'architettura di MLflow si articola in due componenti primari: il **Backend Store**, un database relazionale ([SQLite](https://www.sqlite.org/) per installazioni locali o [PostgreSQL](https://www.postgresql.org/) per ambienti enterprise) che memorizza i parametri scalari, le metriche temporali per epoca, i tag e l'ID del commit Git di origine; e l'**Artifact Store**, uno storage basato su file system locale o object storage che conserva i modelli serializzati, le matrici di confusione e i grafici diagnostici.

Il **Model Registry** di MLflow centralizza la governance dei modelli, consentendo transizioni controllate di stato attraverso ambienti di staging, produzione e archiviazione. Ogni modello registrato incapsula il formato standard `MLmodel`, che specifica in modo dichiarativo il flavor del runtime ([Scikit-learn](https://scikit-learn.org/), [PyTorch](https://pytorch.org/), [Transformers](https://huggingface.co/docs/transformers)) e le dipendenze Python necessarie, garantendo che l'artefatto possa essere caricato e servito in qualsiasi ambiente senza discrepanze di versione.

Parallelamente, il versionamento dei dati e dei pesi voluminosi viene gestito tramite [DVC](https://dvc.org/). Poiché [Git](https://git-scm.com/) (il sistema di controllo versione distribuito) non è strutturato per gestire in modo efficiente file binari di grandi dimensioni, DVC introduce puntatori leggeri in formato testuale (`.dvc`) memorizzati nel repository [GitHub](https://github.com/), contenenti gli hash crittografici dei file reali archiviati in un archivio *Content-Addressable Storage* (CAS). Tramite il file dichiarativo `dvc.yaml`, DVC traccia inoltre i grafi aciclici diretti (DAG) delle pipeline di elaborazione, ricalcolando unicamente gli step i cui dati di input o codici sorgente sono stati modificati (`dvc repro`).

```text
+-----------------------------------------------------------------------------------------+
|                  LINEAGE DETERMINISTICO: GIT + DVC + MLFLOW                              |
+-----------------------------------------------------------------------------------------+

   REPOSITORY GIT (Codice & Puntatori)            STORAGE DATI DVC (Content-Addressable)
   ┌──────────────────────────────────┐            ┌──────────────────────────────────┐
   │ src/train.py                     │            │ .dvc/cache/                      │
   │ params.yaml                      │            │ ├── a1/b4c890ef... (Dataset v1)  │
   │ data/corpus.parquet.dvc ─────────┼───────────►│ └── d4/e7f123ab... (Dataset v2)  │
   │ dvc.yaml                         │            └──────────────────────────────────┘
   └────────────────┬─────────────────┘
                    │
                    ▼ (Esecuzione Pipeline Deterministica: dvc repro)
   ┌──────────────────────────────────────────────────────────────────────────────────┐
   │ MLFLOW TRACKING SERVER & MODEL REGISTRY                                          │
   │                                                                                  │
   │  Run ID: run_20260819_01                                                         │
   │  ├── Parametri: lr=0.001, batch_size=32, model_type="random_forest"              │
   │  ├── Metriche:  val_loss=0.184, val_f1=0.942, latency_p95_ms=12.4                │
   │  ├── Tag:       git_commit="7f8a9b", dvc_hash="d4e7f123ab"                       │
   │  └── Artifacts: model/ (MLmodel, model.pkl, requirements.txt, confusion_mat.png) │
   │                                                                                  │
   │  Model Registry Status: "Production" (v2.1.0)                                    │
   └──────────────────────────────────────────────────────────────────────────────────┘
```

## Containerizzazione e Isolamento dell'Ambiente: Docker, Docker Compose e Configurazione Riproducibile

L'incoerenza tra gli ambienti di sviluppo e di produzione rappresenta una delle principali fonti di fallimento nei sistemi di intelligenza artificiale. Differenze minime nelle versioni delle librerie C/C++ sottostanti, nei driver CUDA di [NVIDIA](https://www.nvidia.com/) o nelle configurazioni del sistema operativo possono alterare i risultati numerici o causare crash imprevisti del runtime.

La containerizzazione tramite [Docker](https://www.docker.com/) (la piattaforma open-source per isolare ed eseguire applicazioni in container leggeri) risolve questa criticità incapsulando il modello, il runtime dell'interprete [Python](https://www.python.org/), i driver compilati e le dipendenze software all'interno di un'immagine immutabile. L'adozione del pattern **Multi-Stage Build** nei file `Dockerfile` consente di separare lo stadio di compilazione pesante (in cui sono presenti compilatori C++, header di sviluppo e pacchetti di build) dallo stadio finale di produzione minimale (basato su distribuzioni leggere come `python:3.11-slim`), riducendo la dimensione dell'immagine finale da decine di gigabyte a poche centinaia di megabyte e minimizzando drasticamente la superficie di attacco esposta.

Per coordinare microservizi complessi in ambiente locale o su server dedicati, si impiega [Docker Compose](https://docs.docker.com/compose/) (lo strumento per definire ed eseguire ambienti multi-container tramite file di configurazione YAML). Uno stack tipico local-first integra dichiarativamente il microservizio di inferenza basato su [FastAPI](https://fastapi.tiangolo.com/), il server di telemetria [Prometheus](https://prometheus.io/), il server di tracciamento [MLflow](https://mlflow.org/) e il database relazionale di supporto [PostgreSQL](https://www.postgresql.org/), gestendo l'allocazione delle porte, i volumi persistenti e le reti bridge isolate.

Quando i requisiti operativi scalano verso cluster enterprise ad alta disponibilità con replica automatica dei pod e gestione distribuita dei carichi GPU, la configurazione viene estesa a [Kubernetes](https://kubernetes.io/) (il sistema open-source di orchestrazione di container per automatizzare deployment, scalabilità e gestione di applicazioni containerizzate), sfruttando il plugin per dispositivi NVIDIA per mappare l'accelerazione hardware direttamente all'interno dei pod di calcolo.

## Architetture di Inferenza e Serving ad Alte Prestazioni: FastAPI, vLLM, Ollama e llama.cpp per Deployment Local-First

L'erogazione dei modelli in produzione richiede architetture di serving ottimizzate per rispondere a diversi schemi di carico: elaborazione batch asincrona su grandi volumi di dati, predizioni sincrone real-time via API REST a bassa latenza e streaming token-by-token per modelli linguistici generativi.

Per i modelli di machine learning classico e deep learning a bassa latenza, lo standard industriale di riferimento è [FastAPI](https://fastapi.tiangolo.com/) (il framework web moderno ad alte prestazioni in Python per la creazione di API REST con validazione Pydantic). Sfruttando la natura asincrona di `asyncio` e del server Uvicorn, FastAPI gestisce elevati volumi di richieste concorrenti senza bloccare l'event loop, convalidando rigidamente i payload in ingresso e in uscita mediante schemi [Pydantic](https://docs.pydantic.dev/). La gestione del ciclo di vita tramite il costrutto `lifespan` garantisce che i pesi del modello vengano caricati in memoria RAM o VRAM una sola volta durante l'inizializzazione dell'applicazione, azzerando l'overhead computazionale sulle singole chiamate HTTP.

Nel dominio dei Large Language Model, l'inferenza tradizionale incontra un severo collo di bottiglia nella gestione della memoria video: durante la generazione autoregressiva, la memorizzazione dei tensori Key e Value (KV-cache) per ogni token della sequenza richiede allocazioni contigue di memoria, causando frammentazione interna ed esterna fino all'80% della VRAM disponibile. Il motore [vLLM](https://github.com/vllm-project/vllm) (l'engine open-source di inferenza LLM ad alto throughput basato sull'algoritmo di gestione della memoria PagedAttention) risolve questo limite ispirandosi alla paginazione della memoria virtuale dei sistemi operativi. **PagedAttention** suddivide la KV-cache in blocchi non contigui di dimensione fissa, azzerando la frammentazione della memoria e consentendo il **Continuous Batching** iterativo, che accoglie nuove richieste a ogni singolo token generato moltiplicando il throughput globale di 5-10 volte rispetto al batching statico.

Per il deployment local-first su computer portatili, workstation o edge server privi di cluster GPU dedicati, l'ecosistema si affida a runtime ottimizzati in C/C++ come [llama.cpp](https://github.com/ggerganov/llama.cpp) (l'engine di inferenza in C/C++ ottimizzato per modelli quantizzati in formato GGUF su CPU e GPU consumer) e [Ollama](https://ollama.com/) (lo strumento open-source multipiattaforma per scaricare ed eseguire Large Language Model in locale). Attraverso il formato binario compatto GGUF e la quantizzazione a 4-bit (come i formati k-quant `Q4_K_M`), questi motori consentono di eseguire modelli avanzati da 7B o 14B parametri direttamente sulla CPU e sulla memoria RAM di sistema, garantendo piena sovranità sui dati ed eliminando qualsiasi dipendenza da API cloud di terze parti.

Infrastrutture enterprise su larga scala impiegano server dedicati quali [TGI](https://github.com/huggingface/text-generation-inference) (il framework di [Hugging Face](https://huggingface.co/) per l'erogazione di API di inferenza ad alte prestazioni per LLM in produzione), [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) (la libreria open-source di [NVIDIA](https://www.nvidia.com/) per l'ottimizzazione e inferenza ultra-rapida di modelli LLM su GPU Tensor Core) e [Triton Inference Server](https://github.com/triton-inference-server/server) (il server open-source di NVIDIA per l'orchestrazione e il deployment scalabile di microservizi di inferenza AI multi-modello).

```text
+-----------------------------------------------------------------------------------------+
|                  ARCHITETTURA PAGEDATTENTION & CONTINUOUS BATCHING IN VLLM               |
+-----------------------------------------------------------------------------------------+

  BATCHING STATICO CLASSICO (Inefficiente - Bloccato dalla sequenza più lunga)
  Richiesta 1: [Tok 1][Tok 2][Tok 3][Tok 4][Tok 5] ──► Finito
  Richiesta 2: [Tok 1][Tok 2] ──────────────────────────► (Idle / VRAM sprecata per padding)
  Richiesta 3: [Tok 1][Tok 2][Tok 3][Tok 4][Tok 5][Tok 6][Tok 7][Tok 8] ──► Finito

  CONTINUOUS BATCHING ITERATIVO (vLLM - Throughput Ottimale)
  Iterazione t:   [Req 1: Tok 1] [Req 2: Tok 1] [Req 3: Tok 1]
  Iterazione t+1: [Req 1: Tok 2] [Req 2: Tok 2 (FINE)] [Req 3: Tok 2] ──► Req 4 Entra Subito!
  Iterazione t+2: [Req 1: Tok 3] [Req 4: Tok 1] [Req 3: Tok 3]
  Iterazione t+3: [Req 1: Tok 4] [Req 4: Tok 2] [Req 3: Tok 4]

  GESTIONE MEMORIA: PAGEDATTENTION (KV-Cache a Blocchi Virtuali Non Contigui)
  Memoria Logica Sequenza:   [ Bloc 0 ] ──► [ Bloc 1 ] ──► [ Bloc 2 ]
                                 │              │              │
  Tabella delle Pagine:          ▼              ▼              ▼
  Memoria Fisica VRAM (Spazio): [ VRAM Slot 14 ][ VRAM Slot 3 ][ VRAM Slot 82 ] (Zero frammentazione!)
```

## Continuous Integration, Continuous Delivery (CI/CD) e Testing Automatizzato per Modelli AI

L'integrazione continua e il deployment continuo nei sistemi di intelligenza artificiale richiedono un paradigma di testing multidimensionale che va oltre la semplice verifica del codice sorgente tradizionale.

La piramide di collaudo per l'intelligenza artificiale comprende quattro livelli complementari. Al primo livello si collocano i test del codice tradizionale (unitari e di integrazione con `pytest`), volti a verificare la correttezza deterministica di funzioni di trasformazione dati, pipeline di tokenizzazione e routing API. Al secondo livello intervengono i test di validazione dei dati e degli schemi, che verificano l'assenza di valori nulli imprevisti, la coerenza tipologica e il rispetto dei range ammissibili per ogni variabile numerica o categorica.

Al terzo livello si eseguono i test di qualità del modello su *golden test set* congelati, verificando che le metriche prestazionali (accuratezza, F1-score, latenza P95) soddisfino i requisiti minimi di rilascio rispetto al modello attualmente in produzione. Al quarto livello si implementano i test comportamentali (basati sulla metodologia *CheckList* di Ribeiro et al.), articolati in test di invarianza (la predizione non deve mutare a fronte di perturbazioni irrilevanti dell'input, come la modifica di nomi propri o spaziature), test di aspettativa direzionale (l'inserimento di termini semanticamente negativi deve ridurre prevedibilmente il punteggio di gradimento) e verifiche di funzionalità minima sui casi limite operativi.

Le pipeline di automazione implementate su [GitHub](https://github.com/) Actions orchestrano l'esecuzione sequenziale dei test, l'estrazione automatica dei dataset da [DVC](https://dvc.org/), la validazione del modello e la generazione dell'immagine [Docker](https://www.docker.com/). Il rilascio in produzione adotta strategie a rischio controllato quali il **Blue/Green Deployment** (in cui il nuovo ambiente Green viene validato prima della commutazione istantanea del traffico di rete), i **Canary Releases** (rilascio incrementale a una frazione del 5-10% degli utenti per monitorare le metriche reali di errore) o lo **Shadow Deployment** (duplicazione asincrona del traffico reale verso il modello candidato per valutarne la stabilità senza impattare gli utenti).

## Osservabilità e Monitoraggio in Produzione: Metriche Prometheus, Rilevamento Data Drift con Evidently AI e Logging

Una volta distribuito in produzione, un sistema di intelligenza artificiale deve essere continuamente monitorato per rilevare anomalie operative e degradazioni qualitative della capacità predittiva.

I quattro pilastri dell'osservabilità AI comprendono: le metriche di sistema (saturazione CPU, consumo di RAM, utilizzo dei Tensor Core GPU e VRAM allocata); le metriche di servizio (latenza P50/P95/P99, throughput delle richieste, tasso di errori HTTP, oltre a *Time To First Token* e *Time Per Output Token* per gli LLM); le metriche di dati (variazione della distribuzione delle feature di ingresso); e le metriche di modello (scostamento delle predizioni e calo della performance rispetto ai dati reali raccolti).

La raccolta telemetrica si basa sullo standard di [Prometheus](https://prometheus.io/) (il sistema open-source di monitoraggio e database di serie temporali della Cloud Native Computing Foundation). Attraverso la libreria Python `prometheus_client`, il microservizio espone l'endpoint `/metrics`, fornendo contatori cumulativi (`Counter` per il volume totale di richieste e codici di stato), indicatori istantanei (`Gauge` per la memoria occupata e le connessioni attive) e distribuzioni a bucket (`Histogram` per la latenza dell'inferenza).

Il rilevamento formale del **Data Drift** viene automatizzato mediante la libreria [Evidently AI](https://www.evidentlyai.com/) (la libreria open-source per il monitoraggio e rilevamento di data drift e qualità dei modelli ML in produzione) applicando test statistici rigorosi:

Il **Test di Kolmogorov-Smirnov a Due Campioni (KS-Test)** per feature numeriche continue confronta le funzioni di distribuzione cumulativa empirica (ECDF) del campione di riferimento e del campione di produzione:

$$D = \sup_{x} |F_{ref}(x) - F_{prod}(x)|$$

Se il p-value associato alla statistica $D$ risulta inferiore alla soglia di significatività (tipicamente $\alpha = 0.05$), l'ipotesi nulla di identità distributiva viene rigettata, segnalando la presenza di data drift statisticamente rilevante.

La **Distanza di Wasserstein** ($W_1$, o Earth Mover's Distance) quantifica il lavoro minimo necessario per trasformare una distribuzione empirica nell'altra:

$$W_1(u, v) = \int_{-\infty}^{\infty} |U(x) - V(x)| \, dx$$

Il **Population Stability Index (PSI)** valuta invece la stabilità di variabili categoriche o discretizzate in $K$ intervalli:

$$PSI = \sum_{k=1}^{K} \left( P_{prod}(k) - P_{ref}(k) \right) \times \ln\left( \frac{P_{prod}(k)}{P_{ref}(k)} \right)$$

Un valore di $PSI < 0.1$ indica una distribuzione pienamente stabile; un valore compreso tra $0.1$ e $0.2$ segnala un drift moderato che richiede attenzione diagnostica; un valore di $PSI \ge 0.2$ indica uno scostamento critico che attiva automaticamente alert MLOps per avviare una nuova pipeline di retraining.

## Trade-off Ingegneristici e Scelte Operative: Local-First vs Cloud Managed, Throughput vs Latenza, Frequenza di Retraining vs Costo

La progettazione di architetture di deployment per l'intelligenza artificiale richiede un bilanciamento continuo tra vincoli economici, tecnici e normativi:

### Deployment Local-First On-Premise vs Cloud Managed Hyperscaler

Il paradigma Local-First garantisce la sovranità assoluta sui dati confidenziali, elimina i costi variabili legati al consumo di token API commerciali e soddisfa i requisiti più stringenti di conformità a [GDPR](https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016R0679) e [EU AI Act](https://artificialintelligenceact.eu/). L'infrastruttura locale offre latenze di rete minime all'interno del perimetro aziendale e assicura la piena continuità operativa anche in assenza di connettività Internet. Di contro, richiede investimenti iniziali in hardware GPU e oneri di manutenzione infrastrutturale a carico del team interno. I servizi cloud gestiti offrono provisioning immediato e scalabilità orizzontale illimitata, ma espongono a costi esponenziali su grandi volumi e a potenziali rischi di data privacy.

### Ottimizzazione dell'Inferenza: Throughput vs Latenza

La dimensione del batch di inferenza impone un compromesso diretto: batch ampi massimizzano l'efficienza computazionale della GPU aumentando il numero totale di transazioni processate al secondo (*throughput* globale), ma incrementano la latenza percepita dal singolo utente ($P99$). Batch ridotti o elaborazioni a singolo campione minimizzano il tempo di risposta immediato (*time-to-first-token*), lasciando tuttavia i core di calcolo parzialmente sottoutilizzati (*compute starvation*).

### Precisione dei Pesi e Quantizzazione

La precisione numerica dei parametri determina il consumo di memoria e la qualità predittiva del modello. I formati `FP16` e `BF16` (2 byte per parametro) preservano la massima fedeltà matematica ma richiedono GPU di fascia datacenter (es. 16 GB di VRAM per un modello da 7B). I formati quantizzati a 8-bit (`INT8`) dimezzano l'ingombro di memoria con un impatto trascurabile sulla perplessità, mentre i formati quantizzati a 4-bit (`GGUF Q4_K_M`, circa 0.55 byte per parametro inclusi metadati) riducono il footprint di memoria di oltre il 70%, consentendo l'esecuzione fluida su workstation standard e laptop dotati di memoria RAM condivisa.

| Criterio Ingegneristico | Deployment Local-First (On-Premise / Edge) | Deployment Cloud Managed (SaaS / Hyperscaler) |
| :--- | :--- | :--- |
| **Privacy e Sovranità del Dato** | Massima (dati mai trasmessi fuori dal perimetro di rete) | Soggetta a contratti cloud, policy del provider e data transfer |
| **Struttura dei Costi** | CAPEX iniziale hardware, OPEX fisso e prevedibile | Zero CAPEX, OPEX variabile ed esponenziale con l'aumento dei token |
| **Latenza di Rete** | Sub-millisecondo su LAN locale / IPC di processo | Variabile (20–150 ms per roundtrip Internet + coda serverless) |
| **Manutenzione Infrastrutturale** | A carico del team interno (aggiornamenti, hardware, raffreddamento) | Interamente gestita dal fornitore di servizi cloud |
| **Scalabilità Oris. Picchi Improvvisi** | Limitata alla capacità fisica dell'hardware installato | Praticamente illimitata tramite autoscaling on-demand |
| **Resilienza alle Disconnessioni** | Funzionamento garantito al 100% anche in totale black-out di rete | Interruzione immediata del servizio in caso di disconnessione Internet |

## Riferimenti Bibliografici e Risorse Tecniche

La formalizzazione del debito tecnico e delle sfide ingegneristiche nel machine learning trova il suo punto di riferimento nello studio *[Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/pub43146/)* di D. Sculley et al. (Google Research, 2015). L'architettura di PagedAttention e del continuous batching per l'inferenza ad alto throughput di Large Language Model è documentata in *[PagedAttention and vLLM: Efficient Memory Management for Large Language Model Serving](https://arxiv.org/abs/2309.06180)* condotto dai ricercatori della UC Berkeley.

I principi cardine per la progettazione di sistemi a dati intensivi affidabili, scalabili e manutenibili sono illustrati nel testo *[Designing Data-Intensive Applications](https://martin.kleppmann.com/)* redatto da [Martin Kleppmann](https://martin.kleppmann.com/) (il ricercatore di sistemi distribuiti presso l'Università di Cambridge e autore di Designing Data-Intensive Applications). Per la metodologia di collaudo comportamentale dei modelli linguistici si rimanda a *[Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://arxiv.org/abs/2005.04118)* di Marco Tulio Ribeiro et al. (2020).

I percorsi formativi di riferimento per l'ingegneria del deployment comprendono [Made With ML](https://madewithml.com/) di Goku Mohandas, il programma [Full Stack Deep Learning](https://fullstackdeeplearning.com/) e le guide operative [Hugging Face Learn: MLOps and LLMOps](https://huggingface.co/learn/) curate da [Hugging Face](https://huggingface.co/). La documentazione tecnica ufficiale include i portali di [MLflow](https://mlflow.org/), [DVC](https://dvc.org/), [Docker](https://docs.docker.com/), [Docker Compose](https://docs.docker.com/compose/), [FastAPI](https://fastapi.tiangolo.com/), [Prometheus](https://prometheus.io/), [Evidently AI](https://www.evidentlyai.com/), [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) di [OWASP](https://owasp.org/) e il [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) dell'agenzia [NIST](https://www.nist.gov/).

## Appendice Operativa: Laboratori Pratici

### Laboratorio 1: Setup di Tracciamento Esperimenti e Model Registry con MLflow

Questo laboratorio configura un ambiente di tracciamento locale con [MLflow](https://mlflow.org/) basato su backend [SQLite](https://www.sqlite.org/). Il codice addestra modelli con [Scikit-learn](https://scikit-learn.org/), registra iperparametri, metriche scalari di performance, artifact diagnostici (matrice di confusione JSON) e registra il modello formale all'interno del Model Registry di MLflow.

```python
import os
import json
import tempfile
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import mlflow
import mlflow.sklearn

def run_mlflow_experiment_lab():
    # 1. Configurazione del tracking URI locale basato su SQLite
    db_path = os.path.abspath("mlflow_tracking.db")
    artifact_dir = os.path.abspath("mlruns_artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    
    tracking_uri = f"sqlite:///{db_path}"
    mlflow.set_tracking_uri(tracking_uri)
    
    experiment_name = "osint_threat_classification"
    mlflow.set_experiment(experiment_name)
    
    print(f"[MLflow] Tracking URI impostato su: {tracking_uri}")
    print(f"[MLflow] Esperimento attivo: {experiment_name}")

    # 2. Generazione di un dataset sintetico controllato per classificazione
    X, y = make_classification(
        n_samples=1200,
        n_features=12,
        n_informative=8,
        n_redundant=2,
        n_classes=2,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # 3. Definizione di griglia di iperparametri per due run comparative
    hyperparameter_sets = [
        {"n_estimators": 50, "max_depth": 5, "min_samples_split": 4, "run_tag": "baseline_fast"},
        {"n_estimators": 150, "max_depth": 12, "min_samples_split": 2, "run_tag": "deep_ensemble"}
    ]

    for idx, params in enumerate(hyperparameter_sets, start=1):
        run_name = f"run_{params['run_tag']}_v{idx}"
        with mlflow.start_run(run_name=run_name) as run:
            print(f"\n---> Avvio esecuzione: {run_name} (Run ID: {run.info.run_id})")

            # Log dei parametri di configurazione
            mlflow.log_param("n_estimators", params["n_estimators"])
            mlflow.log_param("max_depth", params["max_depth"])
            mlflow.log_param("min_samples_split", params["min_samples_split"])
            mlflow.log_param("model_type", "RandomForestClassifier")
            mlflow.log_param("dataset_samples", len(X))
            mlflow.set_tag("pipeline_environment", "local_development")

            # Addestramento modello
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                min_samples_split=params["min_samples_split"],
                random_state=42
            )
            model.fit(X_train, y_train)

            # Valutazione predittiva
            y_pred = model.predict(X_test)
            acc = float(accuracy_score(y_test, y_pred))
            prec = float(precision_score(y_test, y_pred, zero_division=0))
            rec = float(recall_score(y_test, y_pred, zero_division=0))
            f1 = float(f1_score(y_test, y_pred, zero_division=0))

            # Log delle metriche di performance
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)

            print(f"     Metriche registrate: Acc={acc:.4f} | Prec={prec:.4f} | Rec={rec:.4f} | F1={f1:.4f}")

            # Generazione e salvataggio artifact diagnostico: Matrice di Confusione in formato JSON
            cm = confusion_matrix(y_test, y_pred).tolist()
            cm_dict = {
                "run_id": run.info.run_id,
                "confusion_matrix": cm,
                "classes": [0, 1],
                "test_samples": len(y_test)
            }
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
                json.dump(cm_dict, tmp_file, indent=2)
                tmp_json_path = tmp_file.name

            mlflow.log_artifact(tmp_json_path, artifact_path="evaluation_metrics")
            os.remove(tmp_json_path)

            # Registrazione del modello in formato MLmodel standard
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="threat_classifier_model",
                registered_model_name="ThreatClassifierLocal"
            )
            print(f"     Artifact del modello e metadati registrati con successo in MLflow.")

    print("\n[Completato] Laboratorio 1 terminato. I dati sono persistiti in SQLite.")

if __name__ == "__main__":
    run_mlflow_experiment_lab()
```

### Laboratorio 2: Microservizio di Inferenza REST e Streaming SSE con FastAPI e Pydantic

Questo laboratorio realizza un microservizio asincrono di inferenza in [FastAPI](https://fastapi.tiangolo.com/) con validazione tipizzata tramite [Pydantic](https://docs.pydantic.dev/). Il server gestisce il ciclo di vita dell'applicazione con il lifespan context manager per caricare i pesi una sola volta in memoria, espone un endpoint di predizione real-time `/predict` e un endpoint `/stream` basato su Server-Sent Events (SSE) per la generazione in streaming.

```python
import asyncio
import time
import json
from contextlib import asynccontextmanager
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
import uvicorn

# 1. Definizione degli Schemi Pydantic di Richiesta e Risposta
class InferenceRequest(BaseModel):
    features: List[float] = Field(..., description="Vettore numerico di feature di input")
    model_version: Optional[str] = Field(default="latest", description="Versione del modello richiesta")

class InferenceResponse(BaseModel):
    prediction: int = Field(..., description="Classe predetta (0 o 1)")
    probability: float = Field(..., description="Probabilità associata alla predizione")
    model_version: str = Field(..., description="Versione del modello che ha servito l'inferenza")
    latency_ms: float = Field(..., description="Tempo di elaborazione in millisecondi")

class StreamRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Prompt di testo per la generazione in streaming")
    max_tokens: int = Field(default=20, ge=1, le=100, description="Numero massimo di token da emettere")
    stream_delay_seconds: float = Field(default=0.05, ge=0.01, le=0.5, description="Latenza artificiale per token")

# 2. Simulatore di Modello Machine Learning Caricato in Memoria
class InProcessModelRuntime:
    def __init__(self):
        self.weights = None
        self.version = "1.0.0"
        self.is_loaded = False

    def load_weights(self):
        # Simulazione caricamento pesi in memoria VRAM/RAM
        time.sleep(0.1)
        self.weights = [0.25, -0.42, 0.15, 0.88, -0.12]
        self.is_loaded = True
        print("[Runtime] Pesi del modello caricati con successo in memoria.")

    def predict(self, features: List[float]) -> tuple[int, float]:
        if not self.is_loaded:
            raise RuntimeError("Il modello non è stato inizializzato in memoria.")
        # Calcolo deterministico rapido: combinazione lineare + sigmoide
        score = sum(f * w for f, w in zip(features[:len(self.weights)], self.weights))
        prob = 1.0 / (1.0 + (2.718281828 ** (-score)))
        pred_class = 1 if prob >= 0.5 else 0
        return pred_class, float(prob)

    def release(self):
        self.weights = None
        self.is_loaded = False
        print("[Runtime] Risorse del modello liberate correttamente.")

# Istanza globale dello stato dell'applicazione
runtime_engine = InProcessModelRuntime()

# 3. Lifespan Context Manager per Caricamento Unico al Boot
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inizializzazione del modello
    runtime_engine.load_weights()
    yield
    # Shutdown: pulizia delle risorse
    runtime_engine.release()

app = FastAPI(
    title="High-Performance Local Inference Gateway",
    description="Microservizio FastAPI per inferenza locale batch, real-time e streaming SSE",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware per misurazione del tempo di risposta totale
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# 4. Endpoint di Healthcheck
@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if runtime_engine.is_loaded else "unhealthy",
        "model_version": runtime_engine.version,
        "runtime": "FastAPI ASGI"
    }

# 5. Endpoint di Inferenza Sincrona / Real-Time
@app.post("/predict", response_model=InferenceResponse)
async def predict_endpoint(payload: InferenceRequest):
    start_op = time.perf_counter()
    if len(payload.features) == 0:
        raise HTTPException(status_code=400, detail="Il vettore di feature non può essere vuoto.")
    
    # Esecuzione dell'inferenza in thread pool asincrono per non bloccare l'event loop
    pred_class, prob = await asyncio.to_thread(runtime_engine.predict, payload.features)
    latency = (time.perf_counter() - start_op) * 1000
    
    return InferenceResponse(
        prediction=pred_class,
        probability=round(prob, 4),
        model_version=runtime_engine.version,
        latency_ms=round(latency, 3)
    )

# 6. Endpoint di Inferenza Generativa con Streaming Server-Sent Events (SSE)
@app.post("/stream")
async def stream_endpoint(payload: StreamRequest):
    async def token_generator():
        prompt_words = payload.prompt.strip().split()
        yield f"data: {json.dumps({'event': 'start', 'prompt_length': len(prompt_words)})}\n\n"
        
        simulated_tokens = [
            f"token_{i}[" + str(hash(f"{payload.prompt}_{i}") % 1000) + "]"
            for i in range(payload.max_tokens)
        ]
        
        for idx, tok in enumerate(simulated_tokens):
            await asyncio.sleep(payload.stream_delay_seconds)
            chunk = {
                "index": idx,
                "token": tok,
                "finished": idx == len(simulated_tokens) - 1
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            
        yield f"data: {json.dumps({'event': 'done'})}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    print("[Server] Configurazione del microservizio FastAPI pronta.")
```

### Laboratorio 3: Rilevamento Matematico del Data Drift e Degradazione di Modello con Statistica KS e PSI

Questo laboratorio implementa un motore di analisi di data drift e stabilità distributiva in [Python](https://www.python.org/) e [SciPy](https://scipy.org/). Il codice simula dataset di baseline e di produzione, calcola il test a due campioni di Kolmogorov-Smirnov, la distanza di Wasserstein ($W_1$) e il Population Stability Index (PSI), esportando un report diagnostico per l'attivazione di pipeline di retraining.

```python
import json
import numpy as np
from scipy import stats

def calculate_psi(reference_data: np.ndarray, current_data: np.ndarray, num_bins: int = 10) -> float:
    """Calcola il Population Stability Index (PSI) tra due distribuzioni continue."""
    quantiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(reference_data, quantiles)
    bin_edges[0] -= 1e-5
    bin_edges[-1] += 1e-5

    ref_counts, _ = np.histogram(reference_data, bins=bin_edges)
    curr_counts, _ = np.histogram(current_data, bins=bin_edges)

    ref_props = (ref_counts + 1e-4) / (len(reference_data) + (1e-4 * num_bins))
    curr_props = (curr_counts + 1e-4) / (len(current_data) + (1e-4 * num_bins))

    psi_value = np.sum((curr_props - ref_props) * np.log(curr_props / ref_props))
    return float(psi_value)

def run_data_drift_analysis_lab():
    np.random.seed(42)
    sample_size = 1000

    # 1. Creazione del Baseline Reference Dataset (Distribuzioni di Addestramento)
    ref_feature_1 = np.random.normal(loc=0.0, scale=1.0, size=sample_size)
    ref_feature_2 = np.random.gamma(shape=2.0, scale=1.0, size=sample_size)
    ref_feature_3 = np.random.uniform(low=0.0, high=10.0, size=sample_size)

    reference_dataset = {
        "feature_signal_amplitude": ref_feature_1,
        "feature_response_delay": ref_feature_2,
        "feature_packet_size": ref_feature_3
    }

    # 2. Creazione del Current Production Dataset con Drift Simulato
    curr_feature_1 = np.random.normal(loc=1.2, scale=1.1, size=sample_size)
    curr_feature_2 = np.random.gamma(shape=2.5, scale=1.2, size=sample_size)
    curr_feature_3 = np.random.uniform(low=0.0, high=10.0, size=sample_size)

    current_dataset = {
        "feature_signal_amplitude": curr_feature_1,
        "feature_response_delay": curr_feature_2,
        "feature_packet_size": curr_feature_3
    }

    print("==========================================================================================")
    print("                    ANALISI METRICA DI DATA DRIFT E STABILITÀ DISTRIBUTIVA                ")
    print("==========================================================================================")
    print(f"{'Nome Feature':<28} | {'KS Stat':<8} | {'p-value':<9} | {'Wasserstein':<11} | {'PSI':<7} | {'Stato Drift'}")
    print("------------------------------------------------------------------------------------------")

    drift_detected_count = 0
    drift_report = {}

    for feat_name in reference_dataset.keys():
        ref_arr = reference_dataset[feat_name]
        curr_arr = current_dataset[feat_name]

        # 1. Test di Kolmogorov-Smirnov a due campioni
        ks_stat, p_val = stats.ks_2samp(ref_arr, curr_arr)

        # 2. Distanza di Wasserstein (Earth Mover's Distance)
        wasserstein_dist = stats.wasserstein_distance(ref_arr, curr_arr)

        # 3. Population Stability Index (PSI)
        psi = calculate_psi(ref_arr, curr_arr, num_bins=10)

        # Criterio di Decisione: Rigetto dell'ipotesi nulla con alpha=0.05 o PSI >= 0.1
        is_drift = bool(p_val < 0.05 or psi >= 0.1)
        if is_drift:
            drift_detected_count += 1
            status_str = "DRIFT RILEVATO"
        else:
            status_str = "STABILE"

        drift_report[feat_name] = {
            "ks_statistic": round(float(ks_stat), 4),
            "p_value": float(p_val),
            "wasserstein_distance": round(float(wasserstein_dist), 4),
            "psi": round(float(psi), 4),
            "drift_detected": is_drift
        }

        print(f"{feat_name:<28} | {ks_stat:<8.4f} | {p_val:<9.2e} | {wasserstein_dist:<11.4f} | {psi:<7.4f} | {status_str}")

    print("------------------------------------------------------------------------------------------")
    drift_share = drift_detected_count / len(reference_dataset)
    print(f"Riepilogo: Feature in Drift: {drift_detected_count}/{len(reference_dataset)} ({drift_share * 100:.1f}%)")

    alert_triggered = drift_share >= 0.33
    if alert_triggered:
        print("\n[ALERT MLOPS]: La quota di feature in drift supera la soglia critica (>33%).")
        print("                Azione raccomandata: Attivare pipeline automatica di retraining.")
    else:
        print("\n[STATO OK]: Distribuzioni entro le soglie di tolleranza consentite.")

    # Esportazione del report diagnostico JSON
    output_json = "drift_diagnostic_report.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": "2026-08-19T06:00:00Z",
            "drift_share": drift_share,
            "alert_triggered": alert_triggered,
            "features": drift_report
        }, f, indent=2)
    print(f"[File] Report diagnostico esportato in: {output_json}")

if __name__ == "__main__":
    run_data_drift_analysis_lab()
```

### Laboratorio 4: Servizio di Inferenza con Esportazione Telemetrica Prometheus e Containerizzazione Multi-Stage

Questo laboratorio illustra la strumentazione telemetrica di un microservizio di inferenza con la libreria `prometheus_client` in [Python](https://www.python.org/) per esporre contatori di richieste, istogrammi di latenza e gauge di allocazione memoria sull'endpoint `/metrics`, corredato dai file dichiarativi `Dockerfile` multi-stage e `docker-compose.yml` per l'orchestrazione con [Prometheus](https://prometheus.io/).

```python
import time
import random
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import uvicorn

# 1. Definizione delle Metriche Prometheus Native per MLOps/LLMOps
REQUEST_COUNTER = Counter(
    "model_inference_requests_total",
    "Numero totale di richieste di inferenza ricevute dal microservizio",
    ["model_name", "status_code"]
)

INFERENCE_LATENCY = Histogram(
    "model_inference_latency_seconds",
    "Distribuzione della latenza di elaborazione dell'inferenza in secondi",
    ["model_name"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)

ACTIVE_REQUESTS = Gauge(
    "model_active_inference_requests",
    "Numero di richieste di inferenza attualmente in fase di elaborazione attiva"
)

MODEL_MEMORY_USAGE = Gauge(
    "model_memory_footprint_megabytes",
    "Stima della memoria RAM/VRAM occupata dai pesi del modello caricato in MB",
    ["model_name"]
)

app = FastAPI(title="Prometheus Instrumented Inference Server")

# Inizializzazione della metrica di memoria
MODEL_MEMORY_USAGE.labels(model_name="ThreatDetector_v1").set(482.5)

@app.get("/metrics")
async def metrics_endpoint():
    """Endpoint standard per lo scraping periodico da parte di Prometheus."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
async def predict_with_telemetry():
    """Endpoint di inferenza con tracciamento della latenza e dei contatori."""
    ACTIVE_REQUESTS.inc()
    start_time = time.perf_counter()
    model_name = "ThreatDetector_v1"
    
    try:
        # Simulazione elaborazione inferenziale con latenza casuale calibrata
        simulated_delay = random.uniform(0.012, 0.085)
        time.sleep(simulated_delay)
        
        # Registrazione metrica di successo
        REQUEST_COUNTER.labels(model_name=model_name, status_code="200").inc()
        return {
            "prediction": "benign",
            "score": 0.942,
            "inference_time_s": simulated_delay
        }
    except Exception as e:
        REQUEST_COUNTER.labels(model_name=model_name, status_code="500").inc()
        raise e
    finally:
        latency = time.perf_counter() - start_time
        INFERENCE_LATENCY.labels(model_name=model_name).observe(latency)
        ACTIVE_REQUESTS.dec()

# ---------------------------------------------------------------------------------
# ARTIFACT DI CONFIGURAZIONE DOCKER E PROMETHEUS (Generati come stringhe di riferimento)
# ---------------------------------------------------------------------------------

DOCKERFILE_CONTENT = """# Multi-Stage Dockerfile Ottimizzato per Inferenza AI
# Stage 1: Build delle dipendenze
FROM python:3.11-slim as builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime minimale finale
FROM python:3.11-slim as runtime

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

RUN useradd -m -u 10001 appuser
USER appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser src/ /app/src/

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/metrics')" || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

DOCKER_COMPOSE_CONTENT = """version: '3.8'

services:
  inference-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: local_inference_service
    ports:
      - "8000:8000"
    restart: unless-stopped
    networks:
      - ai-ops-network

  prometheus:
    image: prom/prometheus:v2.49.1
    container_name: local_prometheus_server
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped
    networks:
      - ai-ops-network

volumes:
  prometheus-data:

networks:
  ai-ops-network:
    driver: bridge
"""

PROMETHEUS_YML_CONTENT = """global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'inference_service_metrics'
    static_configs:
      - targets: ['inference-api:8000']
"""

if __name__ == "__main__":
    print("[Docker Compose Spec]:\n", DOCKER_COMPOSE_CONTENT)
    print("\n[Prometheus Config]:\n", PROMETHEUS_YML_CONTENT)
```