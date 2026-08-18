# D10 — RAG, knowledge base e grafi OSINT

## Meta-modulo D10

**Target**  
Me stesso oggi, e chiunque voglia progettare e usare sistemi di Retrieval Augmented Generation (RAG)
e knowledge base strutturate per OSINT: embedding, vector DB, grafi (Neo4j), pipeline di retrieval
e integrazione con LLM per analisi e generazione di report.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D05 — Fondamenti di Machine Learning
- D08 — Deep Learning e PyTorch (tensori, modelli, training loop)
- D09 — Transformers, LLM e inference engineering

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - concetto di RAG e perché serve  
  - embedding e vector DB (idea base)  
  - pipeline semplice: documenti → embedding → retrieval → LLM

- **Modalità standard (~8–10 ore)**  
  - embedding models (sentence transformers, ecc.)  
  - vector DB (es. Chroma, FAISS, Qdrant)  
  - integrazione con LLM (cloud/locale) per Q&A e analisi  
  - introduzione a grafi della conoscenza (Neo4j) per OSINT

- **Modalità deep dive (più giornate)**  
  - pipeline RAG complete con chunking, metadata, filtering  
  - grafi OSINT (entità, relazioni, eventi) queryati da LLM  
  - valutazione di retrieval e generazione (RAGAS, ecc.)

**Quando considerare il modulo “completato”**

- so spiegare a parole mie cos’è RAG e perché è utile con i LLM
- so costruire una pipeline RAG base su documenti testuali
- so usare un vector DB e un modello di embedding
- ho almeno un prototipo di knowledge base (testo + grafo) per un caso OSINT
- so valutare qualitativamente (e in parte quantitativamente) un sistema RAG

---

## Perché questo documento

Dopo D09 ho capito come funzionano i LLM, ma so anche che:

- i modelli hanno conoscenza “congelata” al pretraining
- allucinano e inventano fatti quando non hanno contesto
- non hanno accesso automatico ai miei documenti, note, fonti OSINT

Il **RAG** (Retrieval Augmented Generation) è il pattern principale per:

- dare ai LLM contesto rilevante estratto da una knowledge base
- ridurre allucinazioni e migliorare factual accuracy
- costruire sistemi di analisi e Q&A su documenti propri (report, note, fonti OSINT)

In più, i **grafi della conoscenza** (es. Neo4j) permettono di:

- modellare entità, relazioni, eventi in modo strutturato
- fare query complesse (pattern, percorsi, connessioni nascoste)
- integrare grafi + RAG per OSINT avanzato

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere il pattern RAG e i suoi componenti (embedding, retrieval, generazione)
- scegliere e usare modelli di embedding e vector DB
- progettare una pipeline RAG per documenti testuali
- modellare una knowledge base a grafo per un caso OSINT
- integrare LLM + RAG + grafi in un flusso di analisi e report

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Cos’è il RAG e perché serve.
2. Embedding: modelli, dimensioni, similarità.
3. Vector DB: FAISS, Chroma, Qdrant, ecc.
4. Pipeline RAG: chunking, retrieval, generazione.
5. Knowledge base a grafo: entità, relazioni, query.
6. RAG + grafi per OSINT: casi d’uso e pattern.
7. Valutazione di retrieval e generazione.

---

## 2. Cos’è il RAG

### 2.1 Idea base

**RAG** = Retrieval Augmented Generation:

- invece di chiedere al LLM “a memoria”, gli fornisco contesto rilevante estratto da una base di conoscenza
- flusso tipico:
  1. utente fa una domanda
  2. sistema cerca documenti/paragrafi rilevanti (retrieval)
  3. costruisce un prompt con contesto + domanda
  4. LLM genera risposta basata sul contesto

Vantaggi:

- riduce allucinazioni (il modello “legge” il contesto)
- permette di usare conoscenza aggiornata e privata
- separa storage della conoscenza (documenti, grafi) dal modello

Riferimenti:

- [RAG paper (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)

### 2.2 Quando serve RAG

RAG è utile quando:

- ho documenti/report/fonti che il modello non conosce
- voglio risposte basate su fonti specifiche (OSINT, intelligence, compliance)
- devo tracciare fonti e citazioni delle risposte

Non serve (o serve meno) quando:

- il task è puramente creativo o generico
- la conoscenza richiesta è già ben coperta dal modello
- ho vincoli di latenza molto stretti e retrieval costoso

---

## 3. Embedding

### 3.1 Cos’è un embedding

Un **embedding** è un vettore numerico che rappresenta un testo (o immagine, audio, ecc.):

- testi simili → vettori vicini nello spazio
- posso misurare similarità con cosine similarity, dot product, ecc.

### 3.2 Modelli di embedding

Modelli comuni:

- **Sentence Transformers** (es. `all-MiniLM-L6-v2`, `multi-qa`)  
  leggeri, buoni per frasi/paragrafi
- **OpenAI embeddings** (`text-embedding-3-small/large`)  
  API cloud, buone performance
- **Altri open** (E5, BGE, GTE, ecc.)

Scelta del modello:

- dimensione vettore (da 384 a 1024+ dimensioni)
- lingua (monolingua vs multilingua)
- task (search, QA, clustering, ecc.)

Riferimenti:

- [Sentence Transformers docs](https://sbert.net/)
- [OpenAI embeddings docs](https://platform.openai.com/docs/guides/embeddings)

### 3.3 Similarità e retrieval

Metriche comuni:

- **cosine similarity**: misura l’angolo tra vettori
- **dot product**: prodotto scalare (usato in alcuni DB)
- **euclidean distance**: distanza euclidea (meno usata per testo)

In pratica:

- calcolo embedding di query e documenti
- cerco i k documenti con similarità più alta

---

## 4. Vector DB

### 4.1 Perché serve un vector DB

Un **vector database** è ottimizzato per:

- memorizzare milioni di vettori
- fare nearest neighbor search veloce (ANN: Approximate Nearest Neighbors)
- filtrare per metadata (fonte, data, tipo, ecc.)

Alternative:

- **FAISS** (Facebook AI Similarity Search)  
  libreria efficiente, più “low-level”
- **Chroma**  
  semplice, buono per prototipi
- **Qdrant, Weaviate, Pinecone, Milvus**  
  più orientati a produzione, con API, filtering, scaling

Riferimenti:

- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Chroma docs](https://docs.trychroma.com/)
- [Qdrant docs](https://qdrant.tech/docs/)

### 4.2 Schema concettuale

Tipicamente:

- collezione / index = insieme di documenti vettorializzati
- ogni documento ha:
  - `id`
  - `embedding` (vettore)
  - `metadata` (testo originale, fonte, data, tag, ecc.)

Operazioni base:

- `add` documenti (testo → embedding → insert)
- `query` con vettore o testo (quest’ultimo viene embeddingato al volo)
- `filter` per metadata

---

## 5. Pipeline RAG

### 5.1 Componenti

Una pipeline RAG tipica:

1. **Ingestione**  
   - carico documenti (PDF, Markdown, HTML, ecc.)
   - pulisco testo (rimozione boilerplate, normalizzazione)

2. **Chunking**  
   - divido testi in chunk (paragrafi, finestre di token)
   - gestisco overlap tra chunk per non perdere contesto

3. **Embedding**  
   - calcolo embedding per ogni chunk
   - salvo in vector DB con metadata

4. **Retrieval**  
   - ricevo query utente
   - calcolo embedding della query
   - cerco k chunk più simili (con/senza filter)

5. **Generazione**  
   - costruisco prompt: istruzioni + contesto + domanda
   - chiamo LLM (cloud/locale)
   - restituisco risposta + fonti

### 5.2 Prompting per RAG

Struttura tipica:

```text
Sei un assistente che risponde basandosi sul contesto fornito.
Usa solo le informazioni nel contesto. Se il contesto non è sufficiente, dillo esplicitamente.

Contesto:
- [chunk 1]
- [chunk 2]
...

Domanda: {query}
```

Buone pratiche:

- chiedere di citare fonti (es. “Secondo il documento X…”)
- specificare cosa fare se il contesto è insufficiente
- limitare lunghezza del contesto per non superare la context window

---

## 6. Knowledge base a grafo

### 6.1 Perché un grafo

Un grafo della conoscenza permette di:

- modellare **entità** (persone, organizzazioni, luoghi, eventi, documenti)
- modellare **relazioni** (lavora_per, situato_in, coinvolto_in, cita, ecc.)
- fare query su connessioni e percorsi (es. “trova tutti i percorsi tra A e B”)

Per OSINT:

- utile per tracciare reti, influenze, flussi di informazioni
- complementare al RAG testuale (documenti + relazioni)

### 6.2 Neo4j e Cypher

**Neo4j** è un DB a grafo molto usato:

- nodi = entità
- relazioni = archi etichettati
- query in **Cypher** (linguaggio dichiarativo simile a SQL per grafi)

Esempio:

```cypher
MATCH (p:Person)-[:WORKS_FOR]->(o:Organization)
WHERE p.name = "Mario Rossi"
RETURN o
```

Riferimenti:

- [Neo4j docs](https://neo4j.com/docs/)
- [Cypher cheat sheet](https://neo4j.com/docs/cypher-cheat-sheet/current/)

### 6.3 Costruire un grafo OSINT

Passi tipici:

1. estrarre entità e relazioni da testi (NER, relation extraction, LLM)
2. normalizzare entità (stessa persona/organizzazione in nodi unici)
3. creare nodi e relazioni in Neo4j
4. arricchire con metadata (fonte, data, confidence)

---

## 7. RAG + grafi per OSINT

### 7.1 Pattern di integrazione

Combinare RAG testuale e grafi:

- **RAG su documenti** → risposta basata su testi
- **Query su grafo** → risposta basata su relazioni
- **LLM come orchestratore** → decide quando usare RAG, quando il grafo, o entrambi

Esempi:

- domanda su un evento → RAG su report + query su grafo per partecipanti
- domanda su un’organizzazione → RAG su documenti + query su grafo per relazioni

### 7.2 Casi d’uso OSINT

- analisi di reti di influenza (politica, economica, criminale)
- tracciamento di campagne di disinformazione (fonti, condivisioni, bot)
- correlazione di eventi (proteste, attacchi, dichiarazioni)
- supporto ad analisti: Q&A su grandi volumi di documenti e relazioni

---

## 8. Valutazione di retrieval e generazione

### 8.1 Metriche di retrieval

- **Recall@k**: frazione di documenti rilevanti tra i primi k recuperati
- **Precision@k**: frazione di documenti recuperati che sono rilevanti
- **MRR (Mean Reciprocal Rank)**: media dell’inverso del rango del primo documento rilevante

In pratica:

- creo un set di query con “ground truth” (documenti rilevanti)
- valuto il retrieval su queste query

### 8.2 Metriche di generazione (RAG)

Strumenti come **RAGAS** propongono metriche:

- **faithfulness**: quanto la risposta è fedele al contesto
- **answer relevance**: quanto la risposta è pertinente alla domanda
- **context relevance**: quanto il contesto recuperato è pertinente

Riferimenti:

- [RAGAS GitHub](https://github.com/explodinggradients/ragas)

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Primi embedding e similarità

**Obiettivo:** capire come funzionano embedding e similarità.

**Passi:**

1. Installare `sentence-transformers`.
2. Calcolare embedding di alcune frasi in italiano/inglese.
3. Calcolare similarità cosine tra coppie di frasi.
4. Annotare:
   - quali frasi risultano simili
   - limiti (es. sinonimi, negazioni, contesto)

**Deliverable:**

- script/notebook con embedding e similarità
- nota con osservazioni

---

### Laboratorio 2 — Vector DB base con Chroma/FAISS

**Obiettivo:** costruire un piccolo index di documenti.

**Passi:**

1. Scegliere una collezione di documenti (es. 10–20 articoli, note, report).
2. Fare chunking semplice (per paragrafo o finestra di token).
3. Calcolare embedding e caricare in Chroma o FAISS.
4. Fare query testuali e inspectare i chunk recuperati.
5. Annotare:
   - qualità del retrieval
   - effetti di chunk size e overlap

**Deliverable:**

- script/notebook con pipeline ingest + query
- nota con osservazioni su chunking e retrieval

---

### Laboratorio 3 — RAG base con LLM

**Obiettivo:** integrare retrieval e generazione.

**Passi:**

1. Usare il vector DB del laboratorio 2.
2. Per ogni query:
   - recuperare k chunk
   - costruire prompt con contesto + domanda
   - chiamare un LLM (cloud o locale)
3. Valutare risposte:
   - correttezza rispetto al contesto
   - allucinazioni
4. Annotare:
   - casi in cui RAG aiuta
   - casi in cui il contesto è insufficiente o fuorviante

**Deliverable:**

- script/pipeline RAG completa
- nota con esempi di domande/risposte e valutazione

---

### Laboratorio 4 — Grafo OSINT minimale con Neo4j

**Obiettivo:** modellare un piccolo grafo OSINT.

**Passi:**

1. Installare Neo4j (Desktop o Docker).
2. Scegliere un piccolo caso (es. 5–10 entità: persone, organizzazioni, eventi).
3. Definire schema (tipi di nodi e relazioni).
4. Inserire dati (manualmente o via script/LLM).
5. Scrivere query Cypher per:
   - trovare connessioni tra entità
   - elencare relazioni di un’organizzazione
6. Annotare:
   - cosa è facile esprimere a grafo
   - limiti e difficoltà

**Deliverable:**

- script Cypher o notebook con query
- nota con schema e osservazioni

---

## 10. Rubriche e checklist

### Checklist — D10 completato

- [ ] So spiegare cos’è RAG e perché è utile con i LLM.
- [ ] So usare un modello di embedding e calcolare similarità.
- [ ] Ho usato un vector DB (Chroma, FAISS, Qdrant, ecc.) per documenti testuali.
- [ ] Ho costruito una pipeline RAG base con retrieval + generazione.
- [ ] Ho modellato un piccolo grafo OSINT in Neo4j.
- [ ] So discutere vantaggi e limiti di RAG e grafi per OSINT.

### Errori tipici da evitare

- usare chunk troppo grandi o troppo piccoli (retrieval rumoroso o incompleto).
- non filtrare per metadata (fonti vecchie, irrilevanti, non affidabili).
- fidarsi ciecamente delle risposte RAG senza verificare il contesto.
- modellare grafi senza schema (nodi e relazioni inconsistenti).
- esporre vector DB o Neo4j senza autenticazione in ambienti non sicuri.

### Segnali che “ho davvero capito” D10

- posso prendere un nuovo corpus documentale e costruire una pipeline RAG funzionante in poche ore.
- so spiegare a un collega perché RAG riduce le allucinazioni rispetto a un LLM “nudo”.
- so usare un grafo per rispondere a domande su connessioni che il testo da solo non rende evidenti.
- so valutare criticamente un sistema RAG (retrieval + generazione) e proporre miglioramenti.

---

## 11. Come ripartire dopo una pausa

Se torno su D10 dopo giorni o settimane:

1. Riapro la pipeline RAG o il grafo OSINT già costruiti.
2. Eseguo qualche query per ricordare il flusso.
3. Aggiungo una piccola modifica:
   - nuovo modello di embedding
   - diverso chunk size
   - nuova query Cypher
4. Aggiorno una nota con:
   - cosa ho cambiato
   - effetto su retrieval/risposte

Scopo: mantenere fresco il legame tra teoria (embedding, grafi) e pratica (pipeline, query).

---

## 12. Risorse consigliate

### 12.1 RAG e retrieval

- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)**  
  Paper originale sul RAG.  
  https://arxiv.org/abs/2005.11401  

- **RAGAS: Automated Evaluation of Retrieval Augmented Generation**  
  Framework per valutare faithfulness, relevance, context quality.  
  https://github.com/explodinggradients/ragas  

### 12.2 Embedding e vector DB

- **Sentence Transformers documentation**  
  Modelli di embedding per frasi e paragrafi.  
  https://sbert.net/  

- **FAISS GitHub**  
  Libreria per similarity search efficiente.  
  https://github.com/facebookresearch/faiss  

- **Chroma documentation**  
  Vector DB semplice per prototipi.  
  https://docs.trychroma.com/  

- **Qdrant documentation**  
  Vector DB orientato a produzione.  
  https://qdrant.tech/docs/  

### 12.3 Grafi e Neo4j

- **Neo4j documentation**  
  Guide, tutorial, reference per Neo4j e Cypher.  
  https://neo4j.com/docs/  

- **Cypher cheat sheet**  
  Riferimento rapido per query Cypher.  
  https://neo4j.com/docs/cypher-cheat-sheet/current/  

### 12.4 OSINT e knowledge graph

- **Graph-based OSINT (articoli e talk)**  
  Cercare “knowledge graph OSINT”, “Neo4j OSINT” per casi d’uso e pattern.  

Queste risorse non vanno studiate per intero: D10 serve a darti una mappa operativa
per costruire sistemi RAG e knowledge base a grafo, e a collegarti a paper/tool quando serve approfondire.