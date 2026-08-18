# D09 — Transformers, LLM e inference engineering

## Meta-modulo D09

**Target**  
Me stesso oggi, e chiunque voglia capire come funzionano i transformer e i large language model (LLM)
e come usarli in modo consapevole: architettura, tokenizzazione, pretraining/finetuning,
inferenza locale/cloud, ottimizzazione e integrazione in pipeline.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D04 — Matematica e statistica just-in-time (algebra lineare, probabilità, derivate)
- D05 — Fondamenti di Machine Learning
- D08 — Deep Learning e PyTorch (tensori, autograd, MLP, CNN, RNN, training loop)

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - idea di transformer (attention, encoder/decoder)  
  - cos’è un LLM e come viene addestrato (pretraining, finetuning)  
  - uso di API cloud e modelli locali (concetti base)

- **Modalità standard (~8–10 ore)**  
  - tokenizzazione (BPE, WordPiece, SentencePiece)  
  - architettura transformer (attention, positional encoding, layer norm)  
  - pretraining vs instruction tuning vs alignment  
  - inferenza locale (Ollama, llama.cpp, vLLM) e cloud (API provider)

- **Modalità deep dive (più giornate)**  
  - studio di paper e note su transformer (Attention Is All You Need, ecc.)  
  - esperimenti con modelli open (Llama, Mistral, Qwen, ecc.)  
  - ottimizzazione inferenza (quantizzazione, batching, caching, speculative decoding)

**Quando considerare il modulo “completato”**

- so spiegare a parole mie cos’è l’attention e perché i transformer hanno scalato meglio delle RNN
- so descrivere il ciclo di vita di un LLM: pretraining, finetuning, instruction tuning, alignment
- so usare almeno un’API cloud e un modello locale per inferenza
- so leggere documentazione di modelli (Hugging Face, repo GitHub) e capire architettura e limiti
- ho almeno un progetto che integra un LLM in una pipeline (chat, analisi testo, OSINT, ecc.)

---

## Perché questo documento

Dopo D08 ho le basi di deep learning con PyTorch.  
D09 si concentra sui **transformer e LLM**, che sono:

- l’architettura dominante per NLP moderno (e non solo)
- la base di ChatGPT, Claude, Gemini, Llama, Mistral, ecc.
- il “motore” dietro molti sistemi agentici e di RAG

Questo modulo non vuole:

- trasformarmi in ricercatore di architetture transformer
- farmi implementare da zero un modello frontier

Vuole invece:

- darmi una mappa chiara di come funzionano
- permettermi di scegliere e usare modelli in modo consapevole
- collegarmi a risorse serie per approfondire quando serve

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere l’architettura transformer (attention, encoder/decoder, positional encoding)
- spiegare cos’è un LLM e le fasi di pretraining, finetuning, instruction tuning, alignment
- usare tokenizzatori e capire problemi di vocabolario, OOV, chunking
- usare API cloud (es. OpenAI, Anthropic, Google) e modelli locali (Ollama, llama.cpp, ecc.)
- valutare trade-off tra modelli locali e cloud (costo, latenza, privacy, controllo)

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Dai transformer ai LLM: evoluzione storica e motivazioni.
2. Tokenizzazione: BPE, WordPiece, SentencePiece.
3. Architettura transformer: attention, multi-head, encoder/decoder.
4. Pretraining, finetuning, instruction tuning, alignment.
5. Inferenza locale vs cloud: provider, modelli, vincoli.
6. Ottimizzazione inferenza: quantizzazione, batching, caching, speculative decoding.
7. Integrazione in pipeline: chat, analisi testo, OSINT, agenti.

---

## 2. Dai transformer ai LLM

### 2.1 Evoluzione storica (sintesi)

Prima dei transformer:

- RNN/LSTM dominanti per sequenze (testo, audio, tempo)
- problemi di parallelizzazione e dipendenze a lungo raggio

Pubblicazione chiave:

- **“Attention Is All You Need” (Vaswani et al., 2017)**  
  introduce il transformer, basato su self-attention invece che ricorrenza.

Conseguenze:

- modelli più paralleli e scalabili
- nascita di BERT (encoder-only), GPT (decoder-only), T5 (encoder-decoder)
- esplosione dei LLM su larga scala

Riferimenti:

- [Attention Is All You Need (paper)](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer (blog)](https://jalammar.github.io/illustrated-transformer/)

### 2.2 Cosa rende speciali i transformer

- **Self-attention**: ogni token può “guardare” tutti gli altri nella sequenza
- **Parallelizzazione**: tutti i token elaborati in parallelo (non sequenziale come RNN)
- **Scalabilità**: più dati + più parametri → performance migliori (fino a certi limiti)

---

## 3. Tokenizzazione

### 3.1 Cos’è un token

Un **token** è un’unità di testo su cui lavora il modello:

- può essere una parola intera, un sotto-parola, un carattere
- dipende dal vocabolario e dall’algoritmo di tokenizzazione

### 3.2 Algoritmi comuni

- **BPE (Byte Pair Encoding)**  
  usato da GPT, RoBERTa, ecc.
- **WordPiece**  
  usato da BERT, molti modelli Google
- **SentencePiece**  
  tratta il testo come sequenza di byte/char, utile per lingue diverse

Problemi tipici:

- token diversi per stessa parola (maiuscole/minuscole, punteggiatura)
- OOV (out-of-vocabulary) gestiti con subword
- lunghezza massima della sequenza (context window)

Riferimenti:

- [Hugging Face Tokenizers docs](https://huggingface.co/docs/tokenizers/index)

---

## 4. Architettura transformer

### 4.1 Attention

Idea di base:

- per ogni token, calcolo quanto “prestare attenzione” a ciascun altro token
- ottengo una rappresentazione contestuale che dipende da tutta la sequenza

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: Self-Attention</p>
  <p>Passa il mouse sopra ogni parola della frase per vedere i <strong>pesi di attenzione</strong>. Una parola (la <em>Query</em>) cerca informazioni in altre parole (le <em>Key</em>) per disambiguare il proprio significato, e "assorbe" i loro valori (<em>Value</em>). Nota come il pronome "esso" debba guardare a "robot" per essere decodificato correttamente.</p>
  <iframe src="../widgets/attention.html" style="width: 100%; height: 500px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Formula semplificata (scaled dot-product attention):

\[
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]

dove:

- \(Q\) (query), \(K\) (key), \(V\) (value) sono proiezioni lineari degli input
- \(d_k\) è la dimensione delle key/query

### 4.2 Multi-head attention

- invece di una sola attention, uso più “teste” in parallelo
- ogni testa impara pattern diversi (sintassi, relazioni a lungo raggio, ecc.)
- le uscite delle teste sono concatenate e proiettate

### 4.3 Encoder, decoder, encoder-decoder

- **Encoder-only** (es. BERT): vede tutto il contesto, usato per rappresentazioni, classification
- **Decoder-only** (es. GPT): genera token uno alla volta, usato per LLM generativi
- **Encoder-decoder** (es. T5): traduzione, summarization, task seq2seq

Altri componenti:

- **Positional encoding**: informa il modello sulla posizione dei token
- **LayerNorm + residui**: stabilizzano il training di reti molto profonde

Riferimenti:

- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Hugging Face Course – Transformers](https://huggingface.co/learn/nlp-course)

---

## 5. Pretraining, finetuning, instruction tuning, alignment

### 5.1 Pretraining

- addestramento su grandi corpora non etichettati (web, libri, codice, ecc.)
- obiettivi tipici:
  - language modeling (predire il token successivo)
  - masked language modeling (predire token mascherati)

Risultato:

- modello “base” con conoscenza linguistica e fattuale compressa nei pesi

### 5.2 Finetuning

- addestramento ulteriore su task specifici (classification, QA, ecc.)
- dataset etichettati, loss supervisionata
- il modello si specializza mantenendo gran parte della conoscenza generale

### 5.3 Instruction tuning

- addestramento su coppie (istruzione, risposta desiderata)
- obiettivo: far seguire meglio le istruzioni (chat, task vari)
- usato per modelli “chat” e assistant-like

### 5.4 Alignment (RLHF, DPO, ecc.)

- tecniche per allineare il modello a preferenze umane:
  - RLHF (Reinforcement Learning from Human Feedback)
  - DPO (Direct Preference Optimization)
  - altre varianti

Scopo:

- ridurre output dannosi, allucinati, non allineati
- migliorare utilità, sicurezza, coerenza

Riferimenti:

- [InstructGPT paper](https://arxiv.org/abs/2203.02155)
- [DPO paper](https://arxiv.org/abs/2305.18290)

---

## 6. Inferenza locale vs cloud

### 6.1 Modelli cloud (API)

Provider tipici:

- OpenAI (GPT-4, GPT-4o, ecc.)
- Anthropic (Claude)
- Google (Gemini)
- Altri (Cohere, Mistral via API, ecc.)

Vantaggi:

- accesso a modelli frontier senza gestire infrastruttura
- aggiornamenti continui, scaling automatico

Svantaggi:

- costo per token
- dipendenza da provider esterni
- limiti di privacy e controllo sui dati

### 6.2 Modelli locali

Strumenti comuni:

- **Ollama** – gestione semplice di modelli locali (Llama, Mistral, Qwen, ecc.)
- **llama.cpp** – inference ottimizzata in C++ con quantizzazione
- **vLLM** – serving ad alte prestazioni per LLM
- **Hugging Face Transformers** – caricamento modelli PyTorch

Vantaggi:

- controllo totale su dati e configurazione
- possibilità di usare modelli open (Llama, Mistral, Qwen, Phi, ecc.)
- integrazione con pipeline locali (OSINT, agenti, RAG)

Svantaggi:

- richiede hardware adeguato (GPU/TPU o CPU potente + RAM)
- gestione di aggiornamenti, sicurezza, performance

Riferimenti:

- [Ollama](https://ollama.com/)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [vLLM](https://github.com/vllm-project/vllm)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

---

## 7. Ottimizzazione dell’inferenza

### 7.1 Quantizzazione

- ridurre precisione dei pesi (es. da FP16 a INT8/INT4)
- vantaggi:
  - meno memoria
  - inferenza più veloce su certi hardware
- svantaggi:
  - possibile perdita di qualità

Strumenti:

- quantizzazione GGUF (llama.cpp)
- quantizzazione in Hugging Face (bitsandbytes, GPTQ, AWQ, ecc.)

### 7.2 Batching e caching

- **batching**: elaborare più richieste insieme per sfruttare meglio GPU
- **caching**: riutilizzare stati (es. key/value cache in decoder) per velocizzare generazione

### 7.3 Speculative decoding e tecniche avanzate

- **speculative decoding**: usare un modello piccolo per “indovinare” token, poi verificare con modello grande
- altre tecniche:
  - distillazione
  - pruning
  - early exit

Riferimenti:

- [Speculative decoding paper](https://arxiv.org/abs/2304.11336)

---

## 8. Integrazione in pipeline

### 8.1 Pattern comuni

- **Chat / assistant**: loop di prompt → modello → risposta → memoria conversazione
- **Analisi testo**: classificazione, estrazione entità, summarization
- **OSINT**: analisi documenti, correlazione eventi, generazione report
- **Agenti**: LLM come “cervello” che chiama tool, legge file, scrive note

### 8.2 Considerazioni pratiche

- gestione del contesto (context window, chunking, RAG)
- logging e audit delle chiamate
- gestione errori (timeout, rate limit, fallback)
- sicurezza (prompt injection, data leakage, allucinazioni)

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Usare un’API cloud

**Obiettivo:** chiamare un’API LLM cloud e analizzare output.

**Passi:**

1. Scegliere un provider (OpenAI, Anthropic, Google, ecc.).
2. Ottenere una API key.
3. Scrivere uno script che:
   - invia un prompt semplice
   - riceve e stampa la risposta
4. Provare prompt diversi (domanda fattuale, task creativo, analisi testo).
5. Annotare:
   - tempi di risposta
   - qualità delle risposte
   - eventuali allucinazioni o errori

**Deliverable:**

- script di chiamata API
- nota con osservazioni su costi, latenza, qualità

---

### Laboratorio 2 — Usare un modello locale (Ollama o llama.cpp)

**Obiettivo:** eseguire inferenza con un modello locale.

**Passi:**

1. Installare Ollama o llama.cpp.
2. Scaricare un modello (es. Llama 3, Mistral, Qwen).
3. Eseguire inferenza via CLI o API locale.
4. Confrontare con un modello cloud (stesso prompt).
5. Annotare:
   - differenze di velocità
   - differenze di qualità/stile
   - limiti hardware

**Deliverable:**

- script/note con comandi usati
- nota di confronto locale vs cloud

---

### Laboratorio 3 — Tokenizzazione e context window

**Obiettivo:** capire come funziona la tokenizzazione e i limiti di contesto.

**Passi:**

1. Usare un tokenizzatore (Hugging Face o libreria del provider).
2. Tokenizzare testi di diversa lunghezza e lingua.
3. Contare token e confrontare con lunghezza in caratteri/parole.
4. Provare a superare la context window e osservare comportamenti (truncation, errore, ecc.).
5. Annotare:
   - come cambia il numero di token tra lingue e stili
   - implicazioni per prompt lunghi e RAG

**Deliverable:**

- script di tokenizzazione
- nota con osservazioni su token, contesto e strategie di chunking

---

### Laboratorio 4 — Integrare un LLM in una pipeline semplice

**Obiettivo:** usare un LLM in un mini-workflow (es. analisi testo o OSINT).

**Passi:**

1. Scegliere un task semplice:
   - classificazione di documenti
   - estrazione di entità
   - generazione di riassunti
2. Usare un modello (cloud o locale) per elaborare un piccolo dataset.
3. Salvare output e confrontare con baseline (es. regole semplici, keyword).
4. Annotare:
   - vantaggi dell’uso del LLM
   - limiti e errori tipici
   - possibili miglioramenti (prompt, modello, post-processing)

**Deliverable:**

- script/pipeline completa
- nota con risultati e riflessioni

---

## 10. Rubriche e checklist

### Checklist — D09 completato

- [ ] So spiegare cos’è un transformer e perché ha scalato meglio delle RNN.
- [ ] So descrivere le fasi: pretraining, finetuning, instruction tuning, alignment.
- [ ] Ho usato almeno un’API cloud e un modello locale per inferenza.
- [ ] So usare un tokenizzatore e contare token di un testo.
- [ ] Ho integrato un LLM in una pipeline semplice (analisi testo, OSINT, chat, ecc.).
- [ ] So discutere trade-off tra modelli locali e cloud (costo, latenza, privacy, controllo).

### Errori tipici da evitare

- trattare i LLM come oracoli infallibili (ignorare allucinazioni e bias).
- usare prompt vaghi e aspettarsi risultati precisi.
- non considerare limiti di context window e tokenizzazione.
- esporre API key o dati sensibili in log o repo pubblici.
- scegliere modelli senza considerare vincoli hardware e di latenza.

### Segnali che “ho davvero capito” D09

- posso leggere la doc di un modello (Hugging Face, repo GitHub) e capire architettura, limiti e uso.
- so scegliere tra modello locale e cloud in base a task, budget e vincoli.
- so spiegare a un collega cos’è l’attention e perché i transformer sono diversi dalle RNN.
- non vedo più i LLM come “magia”, ma come modelli statistici con punti di forza e debolezze.

---

## 11. Come ripartire dopo una pausa

Se torno su D09 dopo giorni o settimane:

1. Riapro uno script di inferenza (cloud o locale).
2. Eseguo qualche chiamata per ricordare il flusso.
3. Modifico un parametro (modello, prompt, temperatura) e osservo differenze.
4. Aggiorno una nota con:
   - cosa ho cambiato
   - effetto su output e performance

Scopo: mantenere fresco il legame tra teoria (transformer, tokenizzazione) e pratica (chiamate, pipeline).

---

## 12. Risorse consigliate

### 12.1 Paper e articoli fondamentali

- **Attention Is All You Need**  
  Il paper originale sui transformer.  
  https://arxiv.org/abs/1706.03762  

- **The Illustrated Transformer**  
  Spiegazione visiva e intuitiva dell’architettura.  
  https://jalammar.github.io/illustrated-transformer/  

- **InstructGPT paper**  
  Istruzioni e allineamento per modelli chat.  
  https://arxiv.org/abs/2203.02155  

- **DPO paper**  
  Direct Preference Optimization per alignment.  
  https://arxiv.org/abs/2305.18290  

### 12.2 Corsi e tutorial

- **Hugging Face NLP Course**  
  Corso gratuito su transformer, tokenizzazione, finetuning.  
  https://huggingface.co/learn/nlp-course  

- **Dive into Deep Learning (D2L)**  
  Capitoli su attention, transformer, LLM.  
  https://d2l.ai/  

### 12.3 Strumenti e librerie

- **Hugging Face Transformers**  
  Libreria principale per modelli transformer.  
  https://huggingface.co/docs/transformers  

- **Ollama**  
  Gestione semplice di modelli locali.  
  https://ollama.com/  

- **llama.cpp**  
  Inference ottimizzata in C++ con quantizzazione.  
  https://github.com/ggerganov/llama.cpp  

- **vLLM**  
  Serving ad alte prestazioni per LLM.  
  https://github.com/vllm-project/vllm  

Queste risorse non vanno studiate per intero: D09 serve a darti una mappa operativa
per usare transformer e LLM in modo consapevole, e a collegarti a paper/corsi quando serve approfondire.


### Strumenti Visivi e Animazioni Esterne (Web)
- **[LLM Visualization (bbycroft.net)](https://bbycroft.net/llm)**: **Come usarlo**: il "pezzo forte". Ti mostra un Transformer intero in 3D. Clicca su un token di input e naviga attraverso i blocchi di Attention per vedere letteralmente le matrici Q, K, V popolarsi di numeri reali.
- **[The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)**: **Come usarlo**: scorri lentamente le GIF della Self-Attention matrix; fermati dove le matrici si moltiplicano per formare il punteggio e confrontalo con il widget che abbiamo creato per vedere la formula in azione.
