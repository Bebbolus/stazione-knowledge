---
aliases: [Architettura SOTA, SOTA 2026, Architettura Definitiva, Ecosistema Integrato, Stazione Knowledge Base, Stack Architetturale]
---
# Architettura SOTA Definitiva: Sintesi del Sistema

L'**Architettura SOTA Definitiva (State Of The Art 2026)** è il progetto ingegneristico che unifica tutte le tecnologie, i protocolli e le metodologie discusse nelle venti monografie precedenti in un singolo sistema operativo locale, coeso e resistente al logoramento tecnologico (future-proof). Si tratta dell'infrastruttura pratica che l'analista implementa sulla propria macchina (la "Stazione") per eseguire investigazioni OSINT, analisi dei dati e flussi agentici autonomi, mantenendo il controllo totale su costi, privacy e determinismo dell'esecuzione. Questo modello architetturale definitivo esiste per dimostrare che i concetti isolati — come i container Docker, il routing LLM, i guardrails locali, i 12-Factor Agents e il Model Context Protocol — acquisiscono valore esponenziale unicamente quando interconnessi in una gerarchia rigorosa, separando la logica di business dall'implementazione temporanea dei singoli tool.

## Il Problema: Il Crollo dei Sistemi Assemblati a Caso

Quando un professionista assembla una pipeline AI seguendo tutorial sconnessi trovati in rete, costruisce un sistema fragile. Configura un database vettoriale, installa un agent framework complesso (che magari forza un'architettura multi-agente parallela instabile) e connette direttamente le API del modello cloud. Il risultato è un sistema che soffre di quattro patologie critiche. 

Il **Vendor Lock-in**: il codice dipende in modo assoluto dal fornitore del modello, richiedendo riscritture massive a ogni evoluzione commerciale. Il **Context Bloat**: senza filtri e compressione, il modello consuma migliaia di token a ogni iterazione, saturando il budget. La **Violazione della Privacy**: ogni frammento di dato sensibile italiano (Codici Fiscali, Partite IVA) viene iniettato nei server esteri, esponendo l'operatore a sanzioni GDPR. Il **Caos dello Stato (State Chaos)**: l'agente "vive" nella memoria volatile dell'applicazione e, in caso di crash o timeout, l'intero lavoro investigativo va perso.

L'Architettura SOTA 2026 risolve alla radice il caos sistemico imponendo una rigida stratificazione (layering). Nessun componente comunica casualmente con un altro. Ogni interazione è mediata da un protocollo standardizzato o da una cartella su disco, garantendo che qualsiasi pezzo del sistema possa essere sostituito domani senza impattare il lavoro dell'operatore (zero code change).

## Anatomia del Sistema a Tre Livelli

L'architettura definitiva è fisicamente e logicamente divisa in tre livelli concentrici: il Nucleo di Memoria Fredda, il Motore Infrastrutturale (Backend) e l'Ecosistema Esecutivo (Frontend/Agenzia).

### 1. Il Nucleo di Memoria Fredda (File System e Obsidian)
Il livello zero, la fondazione di cemento armato del sistema, è il file system locale strutturato secondo i princìpi della [Interpretable Context Methodology (ICM)](https://github.com/RinDig/icm-architect) teorizzata da [Jake Van Clief](https://github.com/RinDig). Non esistono database proprietari che sequestrano la conoscenza dell'utente. Il sapere dell'analista (la Knowledge Base) e lo stato dei progetti operativi (i flussi ICM) risiedono in file Markdown puri (puro testo). 

[Obsidian](https://obsidian.md/) viene utilizzato come "Motore Semantico Headless": l'umano lo usa per editare manualmente o leggere le note grafiche, ma il sistema agentico lo interroga programmaticamente (via MCP) per estrarre la mappa dei collegamenti (backlink) tra i concetti. I file `IDENTITY.md` e `CONTEXT.md` agiscono come contratti contratti comportamentali persistenti (secondo il pattern 12-Factor). Se la macchina esplode o i server cloud chiudono, l'operatore possiede ancora l'intera logica di business e tutti i risultati in formato portatile.

### 2. Il Motore Infrastrutturale (Backend Dockerizzato)
Il livello intermedio è la sala macchine. Interamente isolato in container Docker tramite un singolo file `docker-compose.yml`, questo livello processa i dati ma non esegue mai le istruzioni dell'utente in via diretta. Comprende:

- **Il Motore di Information Retrieval:** [Qdrant](https://qdrant.tech/), il database vettoriale in Rust che indicizza automaticamente i file Markdown del livello uno. Esegue ricerche ibride (BM25 lessicale + vettori semantici) utilizzando embedding locali (es. `nomic-embed-text`) e modelli di Reranking (es. `bge-reranker`). Garantisce un recupero del contesto chirurgico, respingendo le costose e spesso inutili complessità delle architetture GraphRAG (come HippoRAG) per i vault già strutturati.
- **La Pipeline di Sicurezza (Guardrails):** Il binomio [Rizzo-PII](https://huggingface.co/rizzoaiacademy/rizzo-pii-0.3B) e [LLM Guard](https://github.com/protectai/llm-guard) agisce come firewall. Prima che qualsiasi prompt lasci la macchina, Rizzo-PII anonimizza i dati sensibili italiani (sostituendoli con segnaposto come `[CF_1]`) e LLM Guard blocca le prompt injection indirette. 
- **Il Gateway di Rete:** [LiteLLM](https://github.com/BerriAI/litellm) funge da router e traduttore universale. Riceve le richieste nel formato aperto OpenAI e le smista (con regole di fallback automatico) verso i veri fornitori cloud (Anthropic, DeepSeek) o verso istanze locali (Ollama, vLLM).

### 3. L'Ecosistema Esecutivo (Il Single Pane of Glass)
Il livello superiore è l'unico con cui l'analista interagisce. L'**Agent Harness** — incarnato da [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) grazie alla sua architettura flessibile a plugin (Cordis) — agisce come *Single Pane of Glass* (SPoG). L'utente non naviga più tra il terminale e cinquanta schede del browser. 

Il client si collega ai server [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) per recuperare le capacità: si collega all'MCP del file system per leggere la Knowledge Base, all'MCP di Qdrant per le ricerche semantiche e all'MCP di [Agent-Reach](https://github.com/Panniantong/Agent-Reach) o a istanze isolate di OSINT Sandbox (Virtual Machines) per l'estrazione dati dal web. Quando l'analista fornisce un obiettivo, il client delega l'azione al modello cloud (attraverso il firewall locale) e orchestra le risposte, applicando i vincoli di interruzione automatica e di approvazione umana (Human-in-the-Loop) imposti dai 12-Factor Agents.

## Dinamica di Esecuzione: Un Caso Pratico OSINT

Il funzionamento sinergico del sistema è meglio compreso tracciando il flusso (lifecycle) di una singola operazione investigativa complessa. L'operatore avvia un'indagine su un individuo creando una nuova cartella ICM (es. `01_Ricerca_Profilo`) contenente un `CONTEXT.md` che specifica l'obiettivo, e un `IDENTITY.md` che ordina all'agente di cercare l'individuo limitandosi ai registri pubblici.

Dall'interfaccia dell'Harness (DSH), l'utente attiva l'agente assegnandolo a quella cartella. L'agente legge i file (livello 1) tramite il server MCP del file system. Per espandere il contesto, l'agente interroga l'MCP di Qdrant, chiedendo "Quali aziende sono state citate nei report OSINT degli ultimi tre mesi riguardanti la città di Roma?". Il container Qdrant (livello 2) elabora i vettori, calcola i punteggi ibridi, ordina i risultati tramite il Reranker locale e restituisce i frammenti Markdown esatti. 

Equipaggiato col contesto e l'obiettivo, l'agente formula la chiamata (tool call) per interrogare un registro pubblico web esterno (tramite un plugin MCP in Sandbox). La richiesta di rete viene intercettata dal Gateway locale (LiteLLM). Prima di essere inoltrata al modello Anthropic, Rizzo-PII (livello 2) verifica il payload e anonimizza un eventuale Codice Fiscale, mentre LLM Guard verifica l'assenza di payload malevoli. 

Il modello cloud processa la logica e restituisce il JSON della chiamata. Rizzo-PII lo de-anonimizza, restituendolo intatto all'Harness (livello 3). L'Harness esegue fisicamente lo scraping all'interno della macchina virtuale usa-e-getta, ottiene il testo della pagina web, e lo fornisce all'agente. L'agente (modello cloud) ne deduce una sintesi investigativa e istruisce l'Harness a scrivere il file `output/report_investigativo.md` nella cartella di origine. L'operazione termina, il report è salvo, nessun dato personale ha violato il GDPR, e l'analista ha pilotato il tutto da una singola finestra.

## Compromessi dell'Architettura Definitiva

Implementare l'Architettura SOTA 2026 richiede un significativo **investimento infrastrutturale inziale**. Configurare i file YAML di Docker, scrivere i contratti `IDENTITY.md` per ogni stadio, scaricare i modelli di embedding e avviare il router locale comporta ore di setup tecnico che non producono alcun risultato investigativo immediato. Per un utente che necessita di analizzare un singolo file PDF una tantum, questo ecosistema rappresenta un enorme ostacolo (overkill); in quei casi, usare un'interfaccia web commerciale rimane la scelta pragmaticamente superiore.

Il secondo compromesso riguarda le **risorse hardware locali**. Sebbene i modelli generativi massivi (LLM) risiedano nel cloud (bypassando la necessità di schede grafiche VRAM da decine di migliaia di euro sulla scrivania), i componenti di infrastruttura richiedono memoria. Docker Desktop con Qdrant, LiteLLM, LLM Guard e i modelli di Reranking necessitano di almeno 8-16 GB di RAM di sistema dedicati stabilmente per funzionare in modo fluido, in aggiunta alle risorse necessarie per il sistema operativo host.

## Laboratorio 1 — Il "Bootstrap" dell'Ecosistema SOTA

Questo laboratorio condensa l'implementazione pratica dell'architettura in un singolo file di orchestrazione infrastrutturale (Infrastructure as Code) pronto per il deployment.

```yaml
# docker-compose-sota.yml
# L'infrastruttura backend dell'Architettura Definitiva 2026
version: '3.8'

services:
  # 1. Il Gateway di Rete e Routing (LiteLLM)
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: sota_gateway
    ports:
      - "4000:4000"
    volumes:
      - ./infra_config/litellm_config.yaml:/app/config.yaml
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    command: [ "--config", "/app/config.yaml" ]
    restart: always

  # 2. La Pipeline di Guardrails (LLM Guard)
  llm_guard:
    image: protectai/llm-guard-api:latest
    container_name: sota_firewall
    ports:
      - "8000:8000"
    volumes:
      - ./infra_config/llm_guard_scanners.yml:/app/config/scanners.yml
    restart: unless-stopped

  # 3. Il Motore di Ricerca Ibrida (Qdrant)
  qdrant:
    image: qdrant/qdrant:latest
    container_name: sota_hybrid_db
    ports:
      - "6333:6333"
    volumes:
      - ./infra_data/qdrant_storage:/qdrant/storage
    restart: unless-stopped

  # 4. Il Generatore di Embedding Locale
  # (Espone un'API OpenAI-compatibile dedicata solo al calcolo dei vettori)
  embedding_server:
    image: ghcr.io/huggingface/text-embeddings-inference:cpu-latest
    container_name: sota_embedder
    ports:
      - "8080:80"
    volumes:
      - ./infra_data/models:/data
    command: [ "--model-id", "nomic-ai/nomic-embed-text-v1.5" ]
    restart: unless-stopped
```

Avviando questo singolo file, la base infrastrutturale (Il Motore di Backend) è pronta e in ascolto. Da questo momento in poi, l'analista avvierà il suo Client (DeepSeek Harness) che punterà alla porta 4000 di questa infrastruttura. Le configurazioni dei server MCP e i contratti ICM faranno il resto. Questo file YAML è l'eredità tangibile di tutto il percorso di apprendimento della Stazione: la trasformazione di venti moduli teorici in un sistema operativo scalabile, inviolabile e governabile dall'operatore umano.
