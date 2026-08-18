# D12b — AI Harness e Plugin per agenti OSINT portatili

## Meta-modulo D12b

**Target**  
Me stesso oggi, e chiunque voglia progettare e usare "harness" (ambienti controllati) per agenti AI
e creare plugin/tool pack portatili per OSINT: agenti mobili, air-gapped, deployment su edge.

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D12 — Agentic systems, MCP e automazione affidabile

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - cos'è un AI harness e perché serve  
  - concetto di plugin/tool pack per agenti  
  - casi d'uso base (agenti mobili, edge)

- **Modalità standard (~8–10 ore)**  
  - pattern architetturali di harness (esempi da LangChain, AutoGen, Goose)  
  - creazione di plugin portatili (ricerca web, RAG, grafi)  
  - deployment di agenti su edge/air-gapped

- **Modalità deep dive (più giornate)**  
  - progettazione di harness personalizzati per OSINT  
  - pack di plugin avanzati (tool multipli, orchestrazione)  
  - casi d'uso reali (agenti mobili, deployment in ambienti controllati)

**Quando considerare il modulo "completato"**

- so spiegare cos'è un AI harness e perché è diverso da un agente "nudo"
- so creare plugin/tool pack portatili per agenti OSINT
- ho almeno un harness minimale funzionante per un agente OSINT
- so deployare agenti su edge o in ambienti air-gapped

---

## Perché questo documento

Dopo D12 ho agenti basati su LLM, ma mi manca capire come:

- progettare **harness** (ambienti controllati) per agenti (sicurezza, isolamento, audit)
- creare **plugin portatili** (tool, connector, MCP server) per agenti OSINT
- deployare agenti in scenari reali (mobili, edge, air-gapped)

Questo modulo è **operativo e architetturale**: non è teoria astratta, ma pattern per costruire agenti robusti e portatili.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere cos'è un AI harness e pattern architetturali comuni
- creare plugin/tool pack portatili per agenti OSINT
- deployare agenti su edge o in ambienti air-gapped
- integrare harness con knowledge base (RAG, grafi)

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Cos'è un AI harness e perché serve.
2. Pattern architetturali di harness (LangChain, AutoGen, Goose).
3. Plugin/tool pack per agenti OSINT.
4. Deployment su edge e air-gapped.

---

## 2. Cos'è un AI harness

### 2.1 Definizione

**AI harness** = ambiente controllato in cui un agente opera:

- isola l'agente da sistemi critici (sicurezza)
- fornisce tool e risorse controllate
- traccia azioni (log, audit)
- gestisce errori, retry, fallback

Differenza tra agente "nudo" e agente in harness:

- **agente nudo**: accesso diretto a tool, rischi di azioni pericolose
- **agente in harness**: tool limitati, log auditabili, guardrail

Riferimenti:

- [The Anatomy of an Agent Harness (LangChain)](https://blog.langchain.dev/anatomy-of-an-agent-harness/)
- [HarnessX Paper](https://arxiv.org/abs/2401.xxxxx) (o documentazione specifica)

### 2.2 Pattern architetturali

Pattern comuni:

- **sandbox**: agente esegue in container/VM isolata
- **tool gateway**: tutti i tool passano per un gateway che valida input/output
- **log auditabile**: tutte le azioni sono tracciate in file leggibili
- **guardrail**: limiti di azioni permesse (whitelist di tool, limiti di step)

Esempi:

- **LangChain**: agent executor con tool filtering
- **AutoGen**: group chat con orchestrator che coordina agenti
- **Goose**: harness per agenti con MCP e file system come contesto

---

## 3. Plugin/tool pack per agenti OSINT

### 3.1 Cos'è un plugin

**Plugin** = tool o connector che un agente può usare:

- ricerca web (API, scraping)
- RAG (query su vector DB)
- grafi (query su Neo4j)
- file system (lettura/scrittura)
- API esterne (LLM, servizi OSINT)

### 3.2 Creare plugin portatili

Pattern:

- **interfaccia standard**: ogni plugin espone schema input/output chiaro
- **configurazione esterna**: plugin configurabili via file (es. `config.yaml`)
- **log integrato**: ogni plugin logga azioni per audit

Esempio di plugin pack per OSINT:

- `web_search`: ricerca su motori, social, forum
- `rag_query`: query su vector DB (documenti, report)
- `graph_query`: query su grafo (entità, relazioni)
- `file_read_write`: lettura/scrittura file (note, report)
- `llm_call`: chiamata a LLM (cloud o locale)

### 3.3 Portabilità

Plugin portatili = funzionano su diversi harness/ambienti:

- **containerizzati**: Docker con dipendenze incluse
- **configurabili**: stessi plugin, config diverse per ambiente
- **documentati**: schema chiaro, esempi di uso

---

## 4. Deployment su edge e air-gapped

### 4.1 Edge deployment

**Edge** = dispositivi periferici (laptop, Raspberry Pi, server locali):

- vantaggi: bassa latenza, controllo locale, privacy
- svantaggi: risorse limitate, gestione più complessa

Pattern:

- **modelli leggeri**: LLM piccoli (Phi, Mistral 7B quantizzati)
- **inference locale**: Ollama, llama.cpp, vLLM
- **plugin minimali**: solo tool essenziali per edge

### 4.2 Air-gapped deployment

**Air-gapped** = ambienti isolati da Internet (sicurezza massima):

- vantaggi: nessun rischio di leakage via rete, controllo totale
- svantaggi: aggiornamenti difficili, nessun accesso a cloud

Pattern:

- **modelli locali**: LLM open-weight deployati in locale
- **plugin offline**: tool che non richiedono rete (file, grafi locali)
- **aggiornamenti manuali**: aggiornamenti via USB o rete interna

---

## 5. Laboratori ed esercizi

### Laboratorio 1 — Costruire un harness minimale

**Obiettivo:** progettare un harness per un agente OSINT.

**Passi:**

1. Scegliere un framework (LangChain, AutoGen, Goose, o script proprio).
2. Definire:
   - tool permessi (whitelist)
   - log auditabile (file `LOG.md`)
   - guardrail (limiti di step, azioni vietate)
3. Implementare harness:
   - agente esegue solo tool permessi
   - tutte le azioni sono loggate
4. Testare su task semplice (es. ricerca web + report).
5. Annotare:
   - vantaggi dell'harness
   - limiti o complessità aggiunte

**Deliverable:**

- script/harness implementato
- nota con osservazioni

---

### Laboratorio 2 — Creare un plugin pack per OSINT

**Obiettivo:** creare un pack di plugin portatili.

**Passi:**

1. Scegliere 3–5 plugin (es. `web_search`, `rag_query`, `graph_query`, `file_read_write`).
2. Implementare ogni plugin con:
   - interfaccia standard (input/output)
   - configurazione esterna (`config.yaml`)
   - log integrato
3. Testare plugin in harness del laboratorio 1.
4. Annotare:
   - facilità di integrazione
   - problemi di portabilità

**Deliverable:**

- plugin pack implementato
- nota con osservazioni

---

### Laboratorio 3 — Deployment su edge o air-gapped

**Obiettivo:** deployare un agente su edge o in ambiente air-gapped.

**Passi:**

1. Scegliere scenario:
   - edge: laptop con Ollama + plugin minimali
   - air-gapped: VM isolata con LLM locale + plugin offline
2. Configurare:
   - modello (es. Phi 3, Mistral 7B quantizzato)
   - plugin (solo tool essenziali)
3. Testare agente su task OSINT semplice.
4. Annotare:
   - performance (latenza, accuratezza)
   - limiti (risorse, aggiornamenti)

**Deliverable:**

- configurazione deployment (Dockerfile, config, ecc.)
- nota con osservazioni

---

## 6. Rubriche e checklist

### Checklist — D12b completato

- [ ] So spiegare cos'è un AI harness e perché è diverso da un agente "nudo".
- [ ] Ho creato plugin/tool pack portatili per agenti OSINT.
- [ ] So deployare agenti su edge o in ambienti air-gapped.
- [ ] Ho almeno un harness minimale funzionante per un agente OSINT.
- [ ] So integrare harness con knowledge base (RAG, grafi).

### Errori tipici da evitare

- non isolare l'agente (rischio di azioni pericolose).
- non loggare azioni (impossibile audit o debug).
- creare plugin non portatili (dipendenze hardcoded, config fisse).
- sottovalutare limiti di risorse su edge (modelli troppo grandi).
- ignorare aggiornamenti in ambienti air-gapped (obsolescenza).

### Segnali che "ho davvero capito" D12b

- posso spiegare a un collega cos'è un harness e perché serve.
- so creare plugin portatili e integrarli in harness diversi.
- so deployare agenti su edge o air-gapped con consapevolezza di limiti.
- vedo harness come pattern architetturale, non come vincolo.

---

## 7. Come ripartire dopo una pausa

Se torno su D12b dopo giorni o settimane:

1. Riapro un harness o plugin pack già costruito.
2. Rieseguo un task per ricordare il flusso.
3. Aggiungo una piccola modifica:
   - nuovo plugin
   - miglioramento harness (log, guardrail)
   - deployment su nuovo scenario (edge/air-gapped)
4. Aggiorno una nota con:
   - cosa ho aggiunto
   - effetto su performance/manutenibilità

Scopo: mantenere fresco il legame tra teoria (harness, plugin) e pratica (agenti, deployment).

---

## 8. Risorse consigliate

### 8.1 AI Harness e pattern

- **The Anatomy of an Agent Harness (LangChain)**  
  https://blog.langchain.dev/anatomy-of-an-agent-harness/  

- **AutoGen - Group Chat and Orchestrator**  
  https://microsoft.github.io/autogen/docs/groupchat  

- **Goose - Agent Harness con MCP**  
  https://github.com/block/goose  

### 8.2 Plugin e tool

- **LangChain Tools**  
  https://python.langchain.com/docs/integrations/tools/  

- **LlamaIndex Tools**  
  https://docs.llamaindex.ai/en/stable/module_guides/deploying/tools.html  

### 8.3 Edge e air-gapped

- **Ollama - Local LLM**  
  https://ollama.com/  

- **llama.cpp - Inference locale**  
  https://github.com/ggerganov/llama.cpp  

- **vLLM - Serving ottimizzato**  
  https://github.com/vllm-project/vllm  

Queste risorse non vanno studiate per intero: D12b serve a darti una mappa operativa
per costruire harness e plugin per agenti OSINT, e a collegarti a framework/tool quando serve approfondire.