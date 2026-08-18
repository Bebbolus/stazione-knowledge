# D12 — Agentic systems, MCP e automazione affidabile

## Meta-modulo D12

**Target**  
Me stesso oggi, e chiunque voglia progettare e usare sistemi agentici basati su LLM:
agenti, tool calling, orchestrazione, MCP (Model Context Protocol), pattern (ReAct, planning, multi-agent),
e gestione di failure mode e rischi.

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D10 — RAG, knowledge base e grafi OSINT
- D11 — OSINT avanzato e discipline principali

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - differenza tra chat, workflow e agente  
  - concetto di tool/function calling  
  - pattern base: ReAct, planning

- **Modalità standard (~8–10 ore)**  
  - orchestrazione di agenti (single vs multi-agent)  
  - MCP (Model Context Protocol) e contesto strutturato  
  - gestione di errori, loop, allucinazioni  
  - integrazione con knowledge base (RAG, grafi)

- **Modalità deep dive (più giornate)**  
  - progettazione di sistemi multi-agente per OSINT/analisi  
  - automazione di flussi end-to-end (raccolta → analisi → report)  
  - valutazione e monitoring di sistemi agentici

**Quando considerare il modulo “completato”**

- so spiegare la differenza tra chat, workflow e agente
- so progettare un agente con tool calling e contesto strutturato
- so usare pattern come ReAct e planning in scenari reali
- ho almeno un sistema multi-agente funzionante per un caso d’uso (es. OSINT, analisi documenti)
- so identificare e mitigare failure mode tipici (loop, allucinazioni, drift)

---

## Perché questo documento

Dopo D11 ho metodologia OSINT e LLM/RAG, ma mi manca un **modello operativo per automazione avanzata**:

- come trasformare un LLM da “chat” a “agente” che agisce nel mondo (legge file, chiama API, scrive note)
- come orchestrare più agenti che collaborano
- come gestire errori, loop, allucinazioni in modo sistematico
- come usare MCP (Model Context Protocol) per dare contesto strutturato agli agenti

Questo modulo mette insieme:

- concetti di agentica (tool calling, planning, memoria)
- pattern architetturali (single vs multi-agent, orchestrator/worker)
- pratiche per affidabilità (guardrail, retry, fallback, audit)

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- distinguere chat, workflow e agenti
- progettare un agente con tool/function calling
- usare pattern ReAct e planning in task complessi
- progettare sistemi multi-agente (orchestrator + worker)
- usare MCP o approcci simili per contesto strutturato
- gestire failure mode (loop, allucinazioni, drift)
- integrare agenti con knowledge base (RAG, grafi) per OSINT/analisi

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Chat vs workflow vs agente.
2. Tool/function calling e azioni nel mondo.
3. Pattern agentici: ReAct, planning, reflection.
4. Single-agent vs multi-agent.
5. MCP (Model Context Protocol) e contesto strutturato.
6. Gestione di errori, loop, allucinazioni.
7. Integrazione con knowledge base (RAG, grafi).

---

## 2. Chat vs workflow vs agente

### 2.1 Chat

- interazione turno per turno (utente → modello → utente)
- stato limitato alla conversazione (context window)
- nessuna azione automatica nel mondo (non legge/scrive file, non chiama API da solo)

### 2.2 Workflow

- sequenza predefinita di passi (es. script, pipeline)
- logica fissa, poca adattabilità
- può usare LLM come “step” ma non decide autonomamente

### 2.3 Agente

- sistema che:
  - percepisce (legge input, contesto, memoria)
  - pianifica (sceglie azioni, tool, ordine)
  - agisce (chiama API, legge/scrive file, usa tool)
  - riflette (valuta risultati, corregge piano)
- può essere:
  - **single-agent**: un unico agente con più tool
  - **multi-agent**: più agenti che collaborano (orchestrator + worker, team specializzati)

---

## 3. Tool/function calling

### 3.1 Cos’è

**Tool calling** (o function calling) = capacità del LLM di invocare funzioni esterne:

- il modello non esegue codice, ma **propone** chiamate a tool
- un orchestratore (script, framework) esegue la chiamata e restituisce risultato al modello

Esempi di tool:

- ricerca web
- lettura/scrittura file
- query a DB (SQL, Neo4j)
- chiamate API (LLM, servizi esterni)
- esecuzione di script Python

### 3.2 Contratto di tool

Ogni tool ha:

- **nome**
- **descrizione** (cosa fa, quando usarlo)
- **schema input** (parametri, tipi)
- **schema output** (cosa restituisce)

Il LLM impara a:

- scegliere il tool giusto in base al task
- costruire argomenti corretti
- interpretare risultati

Riferimenti:

- [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic tool use](https://docs.anthropic.com/claude/docs/tool-use)

---

## 4. Pattern agentici

### 4.1 ReAct (Reason + Act)

Idea:

- il modello alterna:
  - **ragionamento** (pensiero, ipotesi, piano)
  - **azione** (chiamata tool)
  - **osservazione** (risultato del tool)
- ciclo: Thought → Action → Observation → Thought → … → Risposta finale

Vantaggi:

- rende esplicito il ragionamento
- permette di correggere piano in base ai risultati

Riferimenti:

- [ReAct paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)

### 4.2 Planning

Il modello:

- costruisce un piano ad alto livello (lista di step)
- esegue step uno per uno (con tool)
- adatta piano se incontra errori o nuove informazioni

Pattern:

- **plan-and-solve**: piano completo, poi esecuzione
- **iterative planning**: piano parziale, esecuzione, revisione

### 4.3 Reflection / self-critique

Il modello:

- genera una risposta/azione
- la critica (cerca errori, allucinazioni, lacune)
- la corregge o espande

Utile per:

- ridurre allucinazioni
- migliorare qualità di analisi e report

---

## 5. Single-agent vs multi-agent

### 5.1 Single-agent

Un unico agente con:

- accesso a più tool (search, file, DB, API, LLM)
- capacità di pianificare e agire

Vantaggi:

- più semplice da progettare e debuggare
- meno overhead di coordinamento

Svantaggi:

- può diventare “troppo carico” (troppi task, troppi tool)
- più difficile specializzare competenze

### 5.2 Multi-agent

Più agenti specializzati:

- **orchestrator**: coordina, assegna task, consolida risultati
- **worker**: esegue task specifici (ricerca, analisi, scrittura, verifica)

Pattern comuni:

- **orchestrator/worker**: un agente coordina, altri eseguono
- **team specializzati**: agente ricerca, agente analisi, agente redazione, agente verifica
- **ad-hoc**: agenti creati dinamicamente per sotto-task

Vantaggi:

- specializzazione (ogni agente fa “bene” una cosa)
- scalabilità (più task in parallelo)

Svantaggi:

- complessità di coordinamento
- rischio di “allucinazioni di gruppo” se non ben progettato

Riferimenti:

- [CAMEL-AI](https://www.camel-ai.org/)
- [AutoGen](https://microsoft.github.io/autogen/)

---

## 6. MCP (Model Context Protocol) e contesto strutturato

### 6.1 Cos’è MCP

**MCP** (Model Context Protocol) = approccio per dare contesto strutturato agli agenti:

- invece di prompt lunghi e disordinati, uso file/directory come “contesto leggibile”
- il filesystem diventa parte del “cervello” dell’agente

Idea:

- cartelle = aree di contesto (es. `context/osint/`, `context/progetti/`)
- file Markdown = memoria, istruzioni, stato
- l’agente legge/scrive file per:
  - capire task
  - tracciare stato
  - lasciare traccia di decisioni

### 6.2 Vantaggi

- contesto persistente oltre la context window
- tracciabilità (cosa ha letto/scritto l’agente)
- separazione istruzioni/dati (meno confusione)

### 6.3 Pattern di uso

- `AGENTS.md`: istruzioni generali per agenti
- `CONTEXT.md`: contesto specifico per un task/progetto
- `STATE.md`: stato corrente (cosa fatto, cosa da fare)
- `LOG.md`: log delle azioni dell’agente

Riferimenti:

- [ICM: Interpretable Context Methodology](https://github.com/interpretable-context-methodology/Interpreted-Context-Methdology) (o repo simili)

---

## 7. Gestione di errori, loop, allucinazioni

### 7.1 Failure mode tipici

- **loop infiniti**: agente ripete stesse azioni senza progresso
- **allucinazioni**: agente inventa fatti, fonti, risultati
- **drift**: agente si allontana dal task originale
- **tool misuse**: agente usa tool sbagliati o con parametri errati
- **overconfidence**: agente non ammette incertezze o limiti

### 7.2 Mitigazioni

- **guardrail**:
  - limiti di step (max iterazioni)
  - whitelist di tool e azioni permesse
- **retry con fallback**:
  - se un tool fallisce, riprova con parametri diversi o usa fallback
- **validation step**:
  - un agente “verificatore” controlla risultati prima di consolidare
- **log e audit**:
  - tracciare tutte le azioni (tool, input, output)
  - permettere review umana su task critici

---

## 8. Integrazione con knowledge base (RAG, grafi)

### 8.1 Agenti + RAG

Pattern:

- agente usa RAG per:
  - recuperare documenti rilevanti
  - basare risposte su fonti
  - tracciare citazioni

Flusso:

1. agente riceve task
2. usa tool di retrieval (RAG) per cercare contesto
3. usa contesto per pianificare e agire
4. cita fonti nei report

### 8.2 Agenti + grafi

Pattern:

- agente usa grafo (Neo4j) per:
  - query su entità e relazioni
  - scoprire connessioni nascoste
  - validare ipotesi

Flusso:

1. agente formula query Cypher (o usa tool dedicato)
2. esegue query su grafo
3. usa risultati per analisi e report

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Primo agente con tool calling

**Obiettivo:** costruire un agente semplice con tool.

**Passi:**

1. Scegliere un framework (es. LangChain, LlamaIndex, Goose, OpenWork, o script proprio).
2. Definire 2–3 tool:
   - ricerca web (o simulata)
   - lettura file
   - scrittura file
3. Implementare un ciclo ReAct:
   - Thought → Action → Observation → …
4. Testare su task semplici:
   - “trova informazioni su X e scrivile in un file”
5. Annotare:
   - come l’agente sceglie tool
   - errori o loop

**Deliverable:**

- script/notebook con agente
- nota con osservazioni su comportamento

---

### Laboratorio 2 — Agente con planning

**Obiettivo:** aggiungere planning esplicito.

**Passi:**

1. Partire dall’agente del laboratorio 1.
2. Aggiungere step di planning:
   - prima di agire, l’agente scrive un piano (lista di step)
3. Eseguire piano step-by-step:
   - ogni step = azione con tool
4. Permettere revisione del piano se emergono problemi.
5. Testare su task più complessi:
   - “analizza un tema OSINT e produci un report”
6. Annotare:
   - qualità del piano
   - capacità di adattamento

**Deliverable:**

- script con agente + planning
- nota con piani e risultati

---

### Laboratorio 3 — Multi-agent base

**Obiettivo:** sperimentare un sistema multi-agente.

**Passi:**

1. Definire 2 agenti:
   - **ricercatore**: cerca informazioni (web, RAG)
   - **analista**: analizza informazioni e produce sintesi
2. Aggiungere un **orchestrator** (può essere un altro agente o script):
   - assegna task
   - consolida risultati
3. Testare su un caso OSINT:
   - ricerca su un tema
   - analisi