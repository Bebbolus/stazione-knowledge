# D12c — Prompt engineering e context engineering avanzati

## Meta-modulo D12c

**Target**  
Me stesso oggi, e chiunque voglia padroneggiare tecniche avanzate di prompting e context engineering
per LLM e agenti: da zero-shot/few-shot a ReAct, CoT, ToT, auto-reflection, e pattern di contesto
strutturato (MCP, file system, knowledge base).

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D12 — Agentic systems, MCP e automazione affidabile

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - prompt engineering base (zero-shot, few-shot)  
  - concetto di context engineering  
  - pattern semplici (CoT, ReAct)

- **Modalità standard (~8–10 ore)**  
  - tecniche avanzate (ToT, auto-reflection, self-critique)  
  - context engineering con MCP e file system  
  - integrazione con knowledge base (RAG, grafi)

- **Modalità deep dive (più giornate)**  
  - sperimentazione di pattern complessi su task reali  
  - progettazione di contesto strutturato per agenti OSINT  
  - valutazione di efficacia di prompt e contesto

**Quando considerare il modulo "completato"**

- so usare tecniche di prompting (zero-shot, few-shot, CoT, ReAct, ToT)
- so progettare contesto strutturato per agenti (MCP, file, knowledge base)
- ho sperimentato pattern avanzati su task OSINT reali
- so valutare efficacia di prompt e contesto

---

## Perché questo documento

Dopo D12 ho agenti basati su LLM, ma mi manca padroneggiare:

- **prompt engineering avanzato**: tecniche oltre il prompting base
- **context engineering**: come strutturare contesto per agenti (MCP, file, knowledge base)
- **integrazione con knowledge base**: RAG, grafi come contesto

Questo modulo è **operativo e sperimentale**: non è teoria astratta, ma tecniche da applicare subito.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- usare tecniche di prompting (zero-shot, few-shot, CoT, ReAct, ToT, auto-reflection)
- progettare contesto strutturato per agenti (MCP, file system, knowledge base)
- integrare RAG e grafi come contesto per agenti
- valutare efficacia di prompt e contesto su task reali

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Prompt engineering: tecniche base e avanzate.
2. Context engineering: MCP, file system, knowledge base.
3. Integrazione con RAG e grafi.
4. Valutazione di efficacia.

---

## 2. Prompt engineering: tecniche base e avanzate

### 2.1 Tecniche base

**Zero-shot**:

- prompt senza esempi: "Rispondi alla domanda: X"
- utile per task semplici, ma limitato per task complessi

**Few-shot**:

- prompt con esempi: "Ecco alcuni esempi: [esempi]. Ora rispondi: X"
- migliora performance su task specifici

Riferimenti:

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### 2.2 Tecniche avanzate

**Chain of Thought (CoT)**:

- prompt che incoraggia ragionamento passo-passo: "Pensa passo passo..."
- migliora performance su task di ragionamento

Riferimenti:

- [Chain of Thought Paper (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)

**ReAct (Reason + Act)**:

- prompt che alterna ragionamento e azione: "Thought: ... Action: ... Observation: ..."
- usato in agenti per tool calling

Riferimenti:

- [ReAct Paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)

**Tree of Thoughts (ToT)**:

- prompt che esplora più percorsi di ragionamento (albero di pensieri)
- utile per task complessi con multiple soluzioni

Riferimenti:

- [Tree of Thoughts Paper (Yao et al., 2023)](https://arxiv.org/abs/2305.10601)

**Auto-reflection / Self-critique**:

- prompt che chiede al modello di criticare/correggere la propria risposta
- riduce allucinazioni, migliora qualità

Riferimenti:

- [Self-Refine Paper (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651)

---

## 3. Context engineering: MCP, file system, knowledge base

### 3.1 Cos'è context engineering

**Context engineering** = progettare come il contesto (istruzioni, dati, memoria) è strutturato per un agente.

Obiettivi:

- massimizzare rilevanza del contesto
- minimizzare rumore e confusione
- permettere tracciabilità (cosa ha letto l'agente)

### 3.2 MCP (Model Context Protocol)

**MCP** = approccio per dare contesto strutturato agli agenti:

- cartelle = aree di contesto (es. `context/osint/`, `context/progetti/`)
- file Markdown = memoria, istruzioni, stato
- agente legge/scrive file per:
  - capire task
  - tracciare stato
  - lasciare traccia di decisioni

Pattern:

- `AGENTS.md`: istruzioni generali
- `CONTEXT.md`: contesto specifico per task
- `STATE.md`: stato corrente
- `LOG.md`: log delle azioni

Riferimenti:

- [ICM: Interpretable Context Methodology](https://github.com/modelcontextprotocol)

### 3.3 File system come contesto

Oltre a MCP, il file system può essere usato come contesto:

- **documenti**: report, note, fonti
- **configurazioni**: istruzioni, parametri
- **log**: traccia delle azioni

Vantaggi:

- contesto persistente oltre la context window
- tracciabilità completa
- facilità di debug

---

## 4. Integrazione con RAG e grafi

### 4.1 RAG come contesto

**RAG** = retrieval di documenti rilevanti come contesto per agente.

Pattern:

- agente riceve task
- usa RAG per recuperare documenti rilevanti
- usa documenti come contesto per rispondere/agire

Vantaggi:

- contesto basato su fonti reali
- riduzione allucinazioni

### 4.2 Grafi come contesto

**Grafi** = relazioni ed eventi come contesto per agente.

Pattern:

- agente riceve task
- interroga grafo (Neo4j) per relazioni ed eventi
- usa risultati come contesto per analisi/report

Vantaggi:

- contesto strutturato (entità, relazioni)
- scoperta di connessioni nascoste

---

## 5. Valutazione di efficacia

### 5.1 Metriche per prompt

- **accuratezza**: quanto la risposta è corretta
- **completezza**: quanto la risposta copre il task
- **coerenza**: quanto la risposta è logica e strutturata
- **efficienza**: quanti token/costi per ottenere la risposta

### 5.2 Metriche per contesto

- **rilevanza**: quanto il contesto è pertinente al task
- **completezza**: quanto il contesto copre informazioni necessarie
- **rumore**: quanto il contesto include informazioni irrilevanti

### 5.3 Sperimentazione

Pattern:

- testare varianti di prompt (zero-shot vs few-shot vs CoT)
- testare varianti di contesto (MCP vs RAG vs grafi)
- valutare metriche e scegliere migliore

---

## 6. Laboratori ed esercizi

### Laboratorio 1 — Sperimentare tecniche di prompting

**Obiettivo:** confrontare tecniche di prompting su task OSINT.

**Passi:**

1. Scegliere un task OSINT (es. analisi di disinformazione, correlazione eventi).
2. Sperimentare:
   - zero-shot
   - few-shot (con esempi)
   - CoT ("pensa passo passo")
   - ReAct (thought/action/observation)
3. Valutare:
   - accuratezza
   - completezza
   - coerenza
4. Annotare:
   - quale tecnica funziona meglio per quale task
   - limiti di ciascuna tecnica

**Deliverable:**

- raccolta di prompt e risposte
- nota con confronto e osservazioni

---

### Laboratorio 2 — Progettare contesto strutturato per agente

**Obiettivo:** progettare contesto strutturato (MCP, file) per un agente.

**Passi:**

1. Scegliere un task OSINT complesso.
2. Progettare struttura di contesto:
   - `AGENTS.md` (istruzioni)
   - `CONTEXT.md` (task, fonti)
   - `STATE.md` (stato)
   - `LOG.md` (log)
3. Implementare contesto (file Markdown).
4. Testare agente con contesto progettato.
5. Annotare:
   - vantaggi del contesto strutturato
   - limiti o complessità aggiunte

**Deliverable:**

- file di contesto (`AGENTS.md`, `CONTEXT.md`, ecc.)
- nota con osservazioni

---

### Laboratorio 3 — Integrare RAG e grafi come contesto

**Obiettivo:** usare RAG e grafi come contesto per agente.

**Passi:**

1. Configurare RAG (vector DB + documenti).
2. Configurare grafo (Neo4j + entità/relazioni).
3. Progettare agente che:
   - usa RAG per recuperare documenti
   - usa grafo per query su relazioni
   - integra entrambi come contesto
4. Testare su task OSINT reale.
5. Annotare:
   - vantaggi di RAG + grafi
   - limiti o problemi di integrazione

**Deliverable:**

- script/agente con RAG + grafi
- nota con osservazioni

---

## 7. Rubriche e checklist

### Checklist — D12c completato

- [ ] So usare tecniche di prompting (zero-shot, few-shot, CoT, ReAct, ToT).
- [ ] So progettare contesto strutturato per agenti (MCP, file system).
- [ ] So integrare RAG e grafi come contesto per agenti.
- [ ] Ho sperimentato pattern avanzati su task OSINT reali.
- [ ] So valutare efficacia di prompt e contesto.

### Errori tipici da evitare

- usare prompt troppo lunghi o confusi (rumore nel contesto).
- non strutturare contesto (agente "perso" in informazioni disordinate).
- fidarsi ciecamente di una tecnica di prompting (nessuna tecnica è universale).
- ignorare valutazione di efficacia (nessun miglioramento iterativo).
- non tracciare contesto usato (impossibile audit o debug).

### Segnali che "ho davvero capito" D12c

- posso spiegare a un colleghi differenze tra tecniche di prompting.
- so progettare contesto strutturato per agenti OSINT.
- so integrare RAG e grafi come contesto in modo efficace.
- so valutare e migliorare prompt e contesto in modo iterativo.
- vedo prompt e contesto come strumenti da progettare, non come dettagli.

---

## 8. Come ripartire dopo una pausa

Se torno su D12c dopo giorni o settimane:

1. Riapro un esperimento di prompting o contesto già fatto.
2. Rieseguo un task per ricordare il flusso.
3. Aggiungo una piccola modifica:
   - nuova tecnica di prompting
   - miglioramento contesto (MCP, file)
   - integrazione RAG/grafi
4. Aggiorno una nota con:
   - cosa ho aggiunto
   - effetto su performance

Scopo: mantenere fresco il legame tra teoria (prompt, contesto) e pratica (task OSINT).

---

## 9. Risorse consigliate

### 9.1 Prompt engineering

- **OpenAI Prompt Engineering Guide**  
  https://platform.openai.com/docs/guides/prompt-engineering  

- **Chain of Thought Paper (Wei et al., 2022)**  
  https://arxiv.org/abs/2201.11903  

- **ReAct Paper (Yao et al., 2022)**  
  https://arxiv.org/abs/2210.03629  

- **Tree of Thoughts Paper (Yao et al., 2023)**  
  https://arxiv.org/abs/2305.10601  

### 9.2 Context engineering e MCP

- **ICM: Interpretable Context Methodology**  
  https://github.com/modelcontextprotocol  

- **MCP (Model Context Protocol)**  
  https://modelcontextprotocol.io/  

### 9.3 RAG e grafi

- **Hugging Face RAG Documentation**  
  https://huggingface.co/docs/transformers/model_doc/rag  

- **Neo4j Documentation**  
  https://neo4j.com/docs/  

Queste risorse non vanno studiate per intero: D12c serve a darti una mappa operativa
per padroneggiare prompt e context engineering, e a collegarti a paper/tool quando serve approfondire.