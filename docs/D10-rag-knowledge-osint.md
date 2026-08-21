---
aliases: [D10, RAG, Retrieval Augmented Generation, Knowledge Base, Vector DB, Grafi OSINT, Neo4j, GraphRAG]
---
# Retrieval-Augmented Generation, Database Vettoriali e Knowledge Graph per l'Intelligence OSINT

Il pattern architetturale di **Retrieval-Augmented Generation (RAG)** integra modelli generativi basati su Transformer con sistemi di recupero informativo esterni, arricchendo dinamicamente il contesto d'inferenza con porzioni documentali pertinenti estratte da basi di conoscenza eterogenee. Questa tecnologia trova impiego primario nell'analisi di intelligence su fonti aperte ([D11](D11-osint-avanzato.md)), nell'investigazione forense su corpus non strutturati e nei sistemi aziendali di question answering ad alta precisione dove i modelli linguistici pre-addestrati soffrono di obsolescenza conoscitiva o allucinazioni fattuali. Il RAG esiste per disaccoppiare la capacità di ragionamento logico-linguistico dell'LLM dalla memorizzazione statica dei parametri sinaptici, consentendo aggiornamenti tempestivi dei dati, verificabilità delle fonti tramite citazioni puntuali e pieno controllo sulla sovranità informativa.

## Il Limite Strutturale dei Pesi Parametrici e la Genesi del RAG

I Large Language Model descritti nel modulo [D09](D09-transformers-llm.md) codificano la propria conoscenza del mondo all'interno di matrici di pesi sinaptici calcolate durante fasi di pre-addestramento computazionalmente onerose. Questa memoria parametrica presenta tre vulnerabilità sistemiche insormontabili nelle investigazioni su dati dinamici: la conoscenza si arresta alla data di chiusura del dataset di addestramento (*knowledge cutoff*), il modello tende a colmare le lacune informative generando allucinazioni plausibili ma prive di riscontro oggettivo, e l'accesso diretto a documenti riservati, note investigative o feed OSINT in tempo reale risulta strutturalmente impossibile senza un meccanismo di iniezione contestuale.

Il tentativo di aggiornare la conoscenza fattuale tramite fine-tuning supervisionato su [PyTorch](https://pytorch.org/) ([D08](D08-deep-learning-pytorch.md)) comporta costi di calcolo insostenibili per dataset che mutano quotidianamente, espone la rete al fenomeno del *catastrophic forgetting* (il degrado delle competenze linguistiche pregresse) e non garantisce che i pesi aggiornati citino fedelmente la fonte documentale primaria. La soluzione risiede nel disaccoppiamento tra il motore di inferenza linguistica e il deposito informativo non parametrico, principio formalizzato nello studio pionieristico su [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) sviluppato dai ricercatori di [Meta AI](https://ai.meta.com/) (la divisione di ricerca AI di Meta, autrice di PyTorch, FAISS e LLaMA).

Nel paradigma RAG, il generatore linguistico non opera più attingendo unicamente alla memoria interna, ma assume il ruolo di interprete e sintetizzatore di documenti che un sottosistema di recupero (*retriever*) estrae in tempo reale da un database esterno in risposta alla query dell'analista. L'informazione documentale viene segmentata, proiettata in uno spazio geometrico multidimensionale e resa accessibile tramite algoritmi di similarità vettoriale o attraversamento relazionale di grafi. In questo modo, l'onere della veridicità fattuale viene trasferito dai pesi probabilistici del modello a record documentali espliciti, tracciabili e immediatamente revocabili o aggiornabili.

```
+-----------------------------------------------------------------------------------------+
|                                ARCHITETTURA DI UN SISTEMA RAG                           |
+-----------------------------------------------------------------------------------------+
                                                                                           
 [ Documenti / Fonti OSINT ]                                                               
             │                                                                             
             ▼                                                                             
     ┌───────────────┐                                                                     
     │ Segmentazione │ (Recursive / Semantic Chunking)                                     
     └───────┬───────┘                                                                     
             ▼                                                                             
     ┌───────────────┐        ┌──────────────────┐                                         
     │   Embedding   │ ──────►│ Vector Database  │◄────────────┐                           
     │    Encoder    │        │  (FAISS / Qdrant)│             │                           
     └───────────────┘        └────────┬─────────┘             │ (Dense Similarity Search) 
                                       │                       │                           
 [ Query Utente / OSINT ] ─────────────┼───────────────────────┘                           
             │                         ▼                                                   
             │                 ┌───────────────┐                                           
             │                 │ Top-k Chunks  │                                           
             │                 └───────┬───────┘                                           
             │                         ▼                                                   
             │                 ┌───────────────┐                                           
             │                 │  Re-Ranking   │ (Cross-Encoder / ColBERT)                 
             │                 └───────┬───────┘                                           
             │                         ▼                                                   
             │                 ┌───────────────┐                                           
             └────────────────►│ Prompt Builder│ (Istruzioni + Contesto Citabile + Query)  
                               └───────┬───────┘                                           
                                       ▼                                                   
                               ┌───────────────┐                                           
                               │      LLM      │ (Ollama / Modello Locale / Cloud API)     
                               └───────┬───────┘                                           
                                       ▼                                                   
                               [ Report con Fonti Verificate ]                             
```

## La Meccanica dei Vettori di Embedding e le Metriche di Distanza Spaziale

La trasformazione del testo non strutturato in una rappresentazione interrogabile richiede l'uso di modelli di embedding, ovvero reti neurali capaci di mappare sequenze di token in vettori densi nello spazio continuo $\mathbb{R}^d$, dove $d$ varia tipicamente da 384 a 3072 dimensioni. Modelli specializzati come [Sentence-Transformers](https://www.sbert.net/) (il framework open-source per il calcolo di embedding densi per frasi e documenti basato su architetture Siamese BERT) e le interfacce di embedding fornite da [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT) proiettano frasi e documenti in modo tale che la vicinanza geometrica tra due vettori rifletta l'affinità semantica dei testi sottostanti, superando i limiti del semplice matching lessicale.

La quantificazione della similarità tra il vettore della query $u \in \mathbb{R}^d$ e il vettore del documento $v \in \mathbb{R}^d$ poggia su tre metriche geometriche fondamentali calcolate mediante la libreria [NumPy](https://numpy.org/) (la libreria open-source fondamentale per il calcolo scientifico e la manipolazione di array multidimensionali in [Python](https://www.python.org/)).

La **Cosine Similarity (Similarità del Coseno)** misura il coseno dell'angolo compreso tra i due vettori, risultando indipendente dalla loro lunghezza o norma assoluta:

$$\text{Cosine}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2} = \frac{\sum_{i=1}^d u_i v_i}{\sqrt{\sum_{i=1}^d u_i^2} \sqrt{\sum_{i=1}^d v_i^2}}$$

La corrispondente distanza del coseno è definita come $D_{\text{cos}}(u, v) = 1 - \text{Cosine}(u, v)$, assumendo valori compresi tra 0 (vettori paralleli identici) e 2 (vettori opposti diametrali).

Il **Dot Product (Prodotto Scalare / Inner Product)** calcola la somma dei prodotti componente per componente:

$$\langle u, v \rangle = \sum_{i=1}^d u_i v_i$$

Qualora i vettori siano preventivamente normalizzati a norma unitaria ($\|u\|_2 = \|v\|_2 = 1$), il prodotto scalare coincide esattamente con la similarità del coseno, consentendo un'esecuzione ultra-rapida tramite istruzioni hardware SIMD e moltiplicazioni di matrici ottimizzate.

La **Euclidean Distance (Distanza Euclidea $L_2$)** rappresenta la distanza geometrica ordinaria in uno spazio a $d$ dimensioni:

$$D_{L2}(u, v) = \|u - v\|_2 = \sqrt{\sum_{i=1}^d (u_i - v_i)^2}$$

Nello spazio dei vettori normalizzati a norma unitaria, la distanza euclidea al quadrato è legata alla similarità del coseno dalla relazione algebrica diretta $\|u - v\|_2^2 = 2 - 2 \cdot \text{Cosine}(u, v)$, rendendo i due ordinamenti di prossimità matematicamente equivalenti.

Negli spazi a elevatissima dimensionalità subentra il fenomeno noto come maledizione della dimensionalità (*Curse of Dimensionality*), in base al quale le distanze tra coppie di punti casuali tendono a concentrarsi in un intervallo ristretto. Per preservare un'elevata capacità discriminante nel recupero di informazioni, i modelli di embedding moderni adottano tecniche di contrastive learning (come InfoNCE), ottimizzando la separazione tra coppie positive di query-documento e insiemi eterogenei di esempi negativi.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D10-rag-knowledge-osint. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Strategie di Segmentazione Documentale (Chunking)

Un testo investigativo o un fascicolo documentale non può essere convertito in un unico vettore globale senza incorrere in una perdita irreparabile di dettaglio semantico, né può essere suddiviso in frammenti troppo brevi privi di contesto narrativo. La segmentazione documentale (*chunking*) definisce la granularità con cui l'informazione viene archiviata e recuperata, bilanciando la specificità del singolo passaggio con la coerenza del discorso complessivo.

```
STRATEGIE DI CHUNKING:
1. Finestra Fissa:    [────── Chunk 1 ──────]
                                   [────── Chunk 2 ──────]  (Overlap costante)
2. Gerarchico:        [# Titolo H1 ──► ## Sezione H2 ──► Paragrafo singolo]
3. Semantico:         [Frase A. Frase B.] || Drop di similarità || [Frase C. Frase D.]
```

La segmentazione a finestra fissa con sovrapposizione (*Fixed-Size Chunking with Overlap*) suddivide il testo grezzo in finestre di ampiezza definita (ad esempio 512 token) con un margine di sovrapposizione mobile (50–100 token). Questa sovrapposizione impedisce che un'entità nominale o una proposizione logica cruciale situata esattamente sul confine del taglio venga spezzata a metà, ma soffre di arbitrarietà sintattica poiché ignora la struttura logica originaria dei paragrafi.

La segmentazione ricorsiva (*Recursive Character Chunking*) preserva la gerarchia naturale del testo tentando la separazione in corrispondenza di delimitatori semantici progressivamente più fini: interruzioni di paragrafo (`\n\n`), interruzioni di riga (`\n`), segni di punteggiatura forte (`. `, `? `, `! `) e infine spazi bianchi. L'algoritmo aggrega porzioni testuali contigue fino al raggiungimento della dimensione limite, garantendo che i confini dei frammenti coincidano quasi sempre con la conclusione di un periodo logico compiuto.

La segmentazione semantica (*Semantic Chunking*) calcola l'embedding per ogni singola frase del documento e misura la distanza del coseno tra frasi adiacenti lungo l'intero flusso testuale. Quando la dissimiglianza semantica tra due frasi consecutive supera una determinata soglia statistica (ad esempio l'85° percentile della varianza delle distanze locali), l'algoritmo individua un punto di rottura naturale, isolando blocchi internamente coesi per argomento ed evitando l'inquinamento contestuale tra sezioni eterogenee.

## Strutture Dati e Indici per Database Vettoriali (ANN)

Quando il corpus documentale scala a centinaia di migliaia o milioni di frammenti, il calcolo della similarità esatta (*Flat Search*) su tutti i vettori mediante scansione sequenziale $O(N \cdot d)$ diviene proibitivo per applicazioni con requisiti di latenza interattiva. I database vettoriali superano questo collo di bottiglia ricorrendo ad algoritmi di ricerca approssimata dei primi vicini (*Approximate Nearest Neighbors*, ANN), che scambiano una quota minima e controllata di accuratezza statistica (*recall*) con una riduzione esponenziale dei tempi di scansione.

```
INDICI VETTORIALI:
- IVF-Flat: Partizionamento in Celle di Voronoi (Ispezione mirata dei centroidi nprobe)
- PQ:       Compressione in sottospazi discretizzati (Codifica quantizzata in cache)
- HNSW:     Grafo a strati multi-livello (Instradamento greedy rapido O(log N))
```

L'indice ad albero e partizionamento cellulare **IVF-Flat (Inverted File Flat)** raggruppa lo spazio vettoriale in $K$ celle di Voronoi attorno a centroidi calcolati durante una fase preliminare di addestramento tramite clustering K-Means ([D07](D07-unsupervised-learning.md)). In fase di query, il sistema calcola la distanza soltanto verso i centroidi, esplorando esclusivamente i vettori contenuti nelle $nprobe$ celle più vicine e riducendo la complessità di calcolo a una frazione del dataset originale.

La tecnica di **Product Quantization (PQ)** comprime drasticamente l'occupazione in memoria RAM dividendo ogni vettore $d$-dimensionale in $m$ sottovettori a bassa dimensione e associando a ciascuno di essi il codice identificativo del centroide più vicino all'interno di un codebook discretizzato. Durante l'interrogazione, le distanze asimmetriche vengono calcolate ad altissima velocità interrogando tabelle pre-calcolate memorizzate direttamente nella cache della CPU, consentendo l'archiviazione di decine di milioni di record vettoriali su macchine con risorse hardware limitate.

La struttura a grafo gerarchico **HNSW (Hierarchical Navigable Small World)** rappresenta lo stato dell'arte per prestazioni e compromesso tra latenza e recall. Ispirata al principio delle *skip-list* probabilistiche, HNSW organizza i vettori su livelli multipli sovrapposti di grafi navigabili: gli strati superiori contengono un numero ridotto di nodi connessi da archi lunghi per consentire salti macroscopici e convergenza ultra-rapida verso la regione di interesse, mentre gli strati inferiori aumentano progressivamente la densità dei collegamenti per affinare localmente la selezione dei vicini con complessità temporale $O(\log N)$.

Il panorama delle tecnologie di indicizzazione vettoriale si articola in quattro categorie primarie. Per il calcolo vettoriale puro ad altissime prestazioni si impiega la libreria [FAISS](https://github.com/facebookresearch/faiss) (sviluppata dalla divisione [Meta AI](https://ai.meta.com/)), ottimizzata su GPU e istruzioni AVX-512. Per ambienti embedded e locali si utilizzano [ChromaDB](https://www.trychroma.com/) (il database vettoriale open-source per l'archiviazione di embedding in applicazioni RAG) e [LanceDB](https://lancedb.com/) (il database vettoriale serverless basato sul formato colonnare Lance), ideali per prototipazione rapida e archiviazione locale su disco con footprint ridotto basato su [SQLite](https://www.sqlite.org/) (il motore di database relazionale compatto e serverless). Per architetture distribuite di classe enterprise si adottano motori dedicati quali [Qdrant](https://qdrant.tech/) (il database vettoriale ad alte prestazioni scritto in Rust), [Weaviate](https://weaviate.io/) (il database vettoriale con supporto a ricerca ibrida e grafi), [Milvus](https://milvus.io/) (il database vettoriale distribuito progettato per miliardi di vettori) e il servizio cloud gestito [Pinecone](https://www.pinecone.io/) (il servizio cloud specializzato in ricerche di similarità a bassissima latenza), che integrano indicizzazione HNSW con filtraggio avanzato su payload di metadati JSON in tempo reale. Infine, per database relazionali preesistenti, l'estensione open-source [pgvector](https://github.com/pgvector/pgvector) per [PostgreSQL](https://www.postgresql.org/) (il sistema di gestione di database relazionale a oggetti) consente di combinare query SQL tradizionali con ricerche di similarità vettoriale su colonne dedicate.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Ricerca Ibrida e Pipeline di Re-Ranking

Il recupero basato unicamente su embedding densi manifesta una debolezza critica nelle investigazioni OSINT: l'incapacità di riconoscere con assoluta precisione parole chiave esatte, stringhe alfanumeriche complesse, codici identificativi (come codici fiscali, coordinate geografiche, hash crittografici SHA-256 o vulnerabilità CVE) che non possiedono una rappresentazione semantica distribuita nei modelli pre-addestrati. La ricerca ibrida (*Hybrid Search*) risolve questa asimmetria combinando la ricerca lessicale sparsa basata su BM25 con la ricerca densa neuronale.

```
PIPELINE DI RECUPERO IBRIDO E RE-RANKING:
[ Query Utente ] ──┬──► [ Ricerca Sparsa BM25 ] ───► [ Top-100 Candidati ] ──┐
                   │                                                         ├──► [ RRF Fusion ] ──► [ Cross-Encoder ] ──► [ Top-5 Chunks ]
                   └──► [ Ricerca Densa Vettori ] ──► [ Top-100 Candidati ] ──┘
```

L'algoritmo **BM25 (Best Matching 25)** valuta la rilevanza probabilistica di un documento analizzando la frequenza locale dei termini della query ponderata per l'inverso della frequenza documentale globale (IDF), penalizzando i documenti eccessivamente lunghi per evitare distorsioni di lunghezza. Per combinare l'ordinamento sparso di BM25 con quello denso generato dal database vettoriale senza incorrere in problemi di calibrazione delle scale di punteggio eterogenee, si adotta la formula del **Reciprocal Rank Fusion (RRF)**:

$$RRF(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

dove $M$ rappresenta l'insieme dei metodi di recupero impiegati (lessicale e vettoriale), $r_m(d)$ indica la posizione ordinale del documento $d$ nella graduatoria del metodo $m$, e $k$ è una costante di smorzamento (convenzionalmente fissata a $k=60$) che impedisce ai documenti posizionati al primo posto di dominare sproporzionatamente la graduatoria aggregata.

Una volta estratti i migliori $N$ candidati (ad esempio $N=50$) tramite fusione RRF, una pipeline di produzione applica un secondo stadio di raffinamento denominato **Re-Ranking**. Mentre i modelli bi-encoder calcolano gli embedding di query e documenti in modo disgiunto per ragioni di efficienza, i modelli **Cross-Encoder** (come le varianti specializzate di BERT e RoBERTa) elaborano la coppia query-documento congiuntamente all'interno dello stesso meccanismo di Self-Attention, valutando le interazioni token-a-token a livello profondo. Questo processo elimina i falsi positivi semantici e isola i 3–5 frammenti di massima rilevanza da passare al contesto dell'LLM.

## Knowledge Graph, Neo4j e GraphRAG per l'Intelligence OSINT

I documenti non strutturati contengono una fitta rete di relazioni che la segmentazione in chunk testuali finisce inevitabilmente per frammentare: se l'informazione che l'individuo $X$ controlla la società $Y$ compare nel documento $A$, e la prova che la società $Y$ gestisce il server $Z$ risiede nel documento $B$, un sistema RAG tradizionale fallirà nell'inferire la correlazione tra $X$ e $Z$ a meno che entrambi i chunk non vengano recuperati contemporaneamente. I **Knowledge Graph (Grafi della Conoscenza)** integrano la dimensione relazionale esplicita, trasformando il testo in una rete topologica di entità, attributi e legami causali.

```
MODELLO PROPERTY GRAPH (OSINT INTELLIGENCE):
(Persona: "Mario Rossi") ──[:DIRECTS {dal: "2021"}]──► (Azienda: "Alpha Ltd")
                                                            │
                                                     [:OWNS_INFRASTRUCTURE]
                                                            │
                                                            ▼
                                                   (Server: "198.51.100.42")
```

Nel modello a grafi di proprietà (*Property Graph*), le entità del mondo reale (persone, organizzazioni, indirizzi IP, coordinate satellitari, canali Telegram) sono rappresentate come nodi etichettati dotati di attributi chiave-valore, mentre le interazioni o transazioni costituiscono archi orientati e tipizzati. Il sistema leader per la memorizzazione e l'interrogazione di grafi è [Neo4j](https://neo4j.com/) (il sistema di gestione di database orientato ai grafi leader industriale per modellare relazioni e query Cypher), che adotta il linguaggio dichiarativo **Cypher** per esprimere pattern matching complessi e cammini multi-hop con estrema concisione:

```cypher
MATCH (p:Person)-[:WORKS_FOR|DIRECTS]->(o:Organization)-[:OWNS_INFRASTRUCTURE]->(s:Server)
WHERE s.ip_address = "198.51.100.42"
RETURN p.name, o.legal_name, s.ip_address
```

L'approccio **GraphRAG** fonde la potenza espressiva dei grafi con il recupero vettoriale attraverso un'architettura integrata a quattro stadi. Nella fase di **estrazione di entità e relazioni**, i documenti grezzi vengono analizzati tramite modelli linguistici o pipeline di Named Entity Recognition per estrarre triplette strutturate $(Soggetto, Predicato, Oggetto)$. Nella fase di **entity resolution e deduplicazione**, le menzioni ambigue (ad esempio acronimi, pseudonimi o traslitterazioni) vengono normalizzate in entità uniche mediante librerie di analisi delle reti come [NetworkX](https://networkx.org/) (il pacchetto Python open-source per lo studio di reti complesse e grafi). Nella fase di **community detection e sintesi gerarchica**, algoritmi di clustering su grafi identificano cluster densamente connessi, generando riassunti tematici ad alto livello per ciascuna comunità di nodi. Infine, nel **recupero contestuale ibrido**, di fronte a una query investigativa complessa, il sistema estrae il sottografo di vicinato (*ego-network*) relativo alle entità identificate e lo serializza in formato testuale strutturato, affiancandolo ai chunk vettoriali recuperati dal vector database orchestrato tramite [LangChain](https://www.langchain.com/) o [LlamaIndex](https://www.llamaindex.ai/) (i framework di orchestrazione per applicazioni guidate da Large Language Model).

Nelle operazioni di intelligence su fonti aperte ([D11](D11-osint-avanzato.md)), il GraphRAG permette di tracciare catene opache di controllo societario, smascherare campagne coordinate di disinformazione su piattaforme social identificando nodi con elevata centralità di intermediazione (*betweenness centrality*), e correlare minacce cyber identificando infrastrutture condivise tra molteplici attori malevoli ([D11b](D11b-ai-arma-bersaglio-osint.md)).


> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.


## Prompt Engineering per RAG, Grounding e Valutazione Quantitativa

L'efficacia finale di un'architettura RAG dipende dalla formulazione del prompt fornito al Large Language Model, che deve imporre un rigoroso vincolo di fedeltà al contesto (*grounding*) per azzerare il rischio di allucinazione. La struttura standard di un prompt RAG isola nettamente le istruzioni operative, il blocco documentale recuperato e il quesito dell'utente:

```text
Sei un assistente specializzato nell'analisi di intelligence che risponde basandosi esclusivamente sul contesto fornito.
Usa soltanto i dati verificabili presenti nei documenti allegati.
Se le informazioni fornite non contengono evidenze sufficienti per rispondere in modo esaustivo, dichiara esplicitamente: "I documenti forniti non contengono evidenze sufficienti su questo argomento".
Per ogni affermazione fattuale prodotta, cita obbligatoriamente il relativo identificativo di fonte [DOC-ID].

CONTESTO DOCUMENTALE:
[DOC-1] (Fonte: Registro Imprese, 2024-03-12) La società Alpha Ltd è controllata al 100% da Marco Bianchi.
[DOC-2] (Fonte: Report Forense Cyber, 2024-05-18) L'infrastruttura 198.51.100.42 appartiene alla società Alpha Ltd.

QUESITO INVESTIGATIVO:
Qual è la catena di controllo tra Marco Bianchi e il server 198.51.100.42?
```

La quantificazione oggettiva delle prestazioni di una pipeline RAG richiede la separazione tra la qualità della fase di recupero (*Retrieval*) e l'affidabilità della fase di sintesi linguistica (*Generation*). Tra le metriche standard di Information Retrieval spiccano la **Recall@k** (la frazione di documenti rilevanti presenti nel corpus che compaiono tra i primi $k$ risultati restituiti dal retriever), la **Precision@k** (la percentuale di documenti pertinenti all'interno del sottoinsieme estratto), il **Mean Reciprocal Rank (MRR)** (la media aritmetica dell'inverso della posizione ordinale del primo documento rilevante recuperato lungo un insieme di query $Q$, formalizzato come $\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$) e il **Normalized Discounted Cumulative Gain (NDCG@k)** (che valuta la qualità dell'ordinamento attribuendo un peso logaritmicamente decrescente ai documenti rilevanti posizionati più in basso nella graduatoria).

Per la valutazione della componente generativa, il framework open-source [RAGAS](https://github.com/explodinggradients/ragas) (il framework open-source per la valutazione quantitativa di pipeline RAG tramite metriche di fedeltà e pertinenza) formalizza tre metriche cardine basate su modelli valutatori. La **Faithfulness (Fedeltà)** calcola il rapporto tra il numero di proposizioni atomiche della risposta che possono essere logicamente dedotte dal contesto recuperato e il totale delle affermazioni generate, identificando l'insorgenza di allucinazioni. L'**Answer Relevance (Pertinenza della Risposta)** misura la coerenza semantica tra la risposta formulata e il quesito originario dell'analista, penalizzando divagazioni. Infine, la **Context Precision (Precisione del Contesto)** quantifica se tutti i passaggi informativi rilevanti all'interno del contesto sono stati posizionati ai primi ranghi della finestra documentale.

## Trade-off Operativi, Compromessi Ingegneristici e Anti-Pattern

La progettazione di un'infrastruttura RAG per contesti investigativi o aziendali impone una serie di compromessi architetturali in cui ogni incremento di accuratezza si riflette in costi di calcolo, latenza operativa o complessità di gestione:

| Dimensione | Opzione A (Bassa Complessità) | Opzione B (Alta Fedeltà) | Compromesso Ingegneristico |
| :--- | :--- | :--- | :--- |
| **Architettura Indice** | Vettoriale Puro ([FAISS](https://github.com/facebookresearch/faiss), [ChromaDB](https://www.trychroma.com/)) | Ibrido + GraphRAG ([Qdrant](https://qdrant.tech/) + [Neo4j](https://neo4j.com/)) | Latenza di query e manutenzione dello schema contro capacità di correlazione multi-hop |
| **Re-Ranking** | Disabilitato (Top-$k$ diretto) | Cross-Encoder a 2 stadi | 50–200 ms di overhead computazionale per query contro abbattimento dei falsi positivi |
| **Dimensione Chunk** | Finestre piccole (128–256 token) | Finestre ampie (1024–2048 token) | Specificità e precisione di recupero contro ampiezza del contesto e consumo di token |
| **Residenza Indice** | Indice HNSW in RAM | Indice IVF-PQ su disco ([LanceDB](https://lancedb.com/)) | Velocità di risposta in millisecondi contro scalabilità a basso costo per milioni di record |

Tra gli anti-pattern più frequenti nell'implementazione di sistemi RAG spiccano pratiche scorrette ampiamente diffuse. Il **chunking privo di semantica** adotta tagli arbitrari a dimensione fissa che spezzano tabelle o codici, rendendo il dato incomprensibile all'encoder vettoriale. L'**assenza di filtri sui metadati** esegue il recupero indiscriminato su tutto il corpus senza segregazione per livello di confidenzialità o data di validità, consentendo a report obsoleti di inquinare l'analisi corrente. 

Un errore strategico catastrofico è la **sovra-ingegnerizzazione tramite GraphRAG su vault curati**: strumenti accademici complessi come HippoRAG o LightRAG sono progettati per estrarre relazioni da *dump* massivi di documenti grezzi e disorganizzati (es. diecimila pagine di atti parlamentari). Applicare l'astrazione e l'estrazione LLM-based dei nodi su un repository di Knowledge Management (come un vault Obsidian locale) in cui l'analista ha *già* curato manualmente i collegamenti ipertestuali esatti, disperde un'enorme quantità di token e calcolo producendo risultati inferiori e allucinati. Per le basi di conoscenza strutturate, la [Ricerca Ibrida tramite Qdrant](https://qdrant.tech/) (Vettori densi + BM25 sparsi) accelerata da Reranker locali (es. `bge-reranker`) si attesta saldamente come l'architettura State Of The Art per rapidità, economia e precisione chirurgica.

Infine, la **mancata sanitizzazione degli input** inietta direttamente frammenti non validati all'interno del prompt senza opportune gabbie di isolamento, esponendo il sistema a vulnerabilità di indirect prompt injection (trattate in [D11b](D11b-ai-arma-bersaglio-osint.md) e [D14](D14-responsible-ai-cyber.md)).

## Riferimenti Bibliografici e Risorse Tecniche

### Articoli Scientifici e Documentazione di Riferimento

La letteratura fondamentale per l'approfondimento delle architetture RAG include il paper fondante [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) sviluppato da [Meta AI](https://ai.meta.com/), che ha unificato modelli seq2seq pre-addestrati e recupero denso non parametrico. Per la parte di embedding semantico, la documentazione ufficiale del framework [Sentence-Transformers](https://www.sbert.net/) e le guide di [OpenAI](https://openai.com/) forniscono le specifiche su modelli bi-encoder e cross-encoder. L'ingegneria del calcolo matriciale e delle strutture di quantizzazione vettoriale ad alta efficienza è documentata nella libreria open-source [FAISS](https://github.com/facebookresearch/faiss) di Meta AI.

### Database Vettoriali e Grafi della Conoscenza

Le guide operative dei database vettoriali specializzati [Qdrant](https://qdrant.tech/documentation/), [ChromaDB](https://docs.trychroma.com/), [Weaviate](https://weaviate.io/) e [LanceDB](https://lancedb.com/) illustrano le modalità di configurazione di indici HNSW e filtri sui metadati. Per la modellazione di grafi di proprietà e l'esecuzione di interrogazioni relazionali dichiarative con linguaggio Cypher, il portale documentale di [Neo4j](https://neo4j.com/docs/) e il [Cypher Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/current/) costituiscono i riferimenti pratici standard, affiancati dalla libreria [NetworkX](https://networkx.org/) per algoritmi su reti complesse. La valutazione quantitativa è descritta nella documentazione del framework [RAGAS](https://github.com/explodinggradients/ragas).

### Moduli Correlati del Percorso Didattico

La comprensione integrale del sistema RAG si ricollega ai moduli complementari del curriculum: [D08](D08-deep-learning-pytorch.md) per i tensori di base con PyTorch, [D09](D09-transformers-llm.md) per l'architettura dei Transformer e l'inferenza linguistica, [D11](D11-osint-avanzato.md) per le metodologie investigative OSINT, [D12](D12-agentic-mcp.md) per i sistemi agentici e il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (lo standard aperto creato da [Anthropic](https://www.anthropic.com/) per la connessione sicura tra modelli linguistici e strumenti esterni), e [D15](D15-mlops-llmops.md) per il deployment e l'orchestrazione locale con [Ollama](https://ollama.com/).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



### Laboratorio 1 — Calcolo delle Distanze Vettoriali e Segmentazione Semantica

Questo laboratorio implementa da zero le metriche di distanza vettoriale con [NumPy](https://numpy.org/) e costruisce un algoritmo di segmentazione semantica basato sull'analisi della varianza delle distanze del coseno tra frasi contigue.

```python
"""
Laboratorio 1: Calcolo Distanze Vettoriali e Semantic Chunking.
Modulo: D10 - RAG, Knowledge Base e Grafi OSINT
"""

import math
from typing import List, Dict, Any, Tuple
import numpy as np


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Calcola la similarita del coseno tra due vettori densi."""
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return float(np.dot(u, v) / (norm_u * norm_v))


def euclidean_distance(u: np.ndarray, v: np.ndarray) -> float:
    """Calcola la distanza euclidea L2 tra due vettori."""
    return float(np.linalg.norm(u - v))


def dot_product_normalized(u: np.ndarray, v: np.ndarray) -> float:
    """Calcola il prodotto scalare su vettori normalizzati a norma unitaria."""
    u_norm = u / (np.linalg.norm(u) + 1e-12)
    v_norm = v / (np.linalg.norm(v) + 1e-12)
    return float(np.dot(u_norm, v_norm))


def mock_sentence_encoder(sentence: str, dim: int = 128) -> np.ndarray:
    """
    Genera un embedding deterministico per scopi di test basato sulla frequenza
    dei caratteri e hash stocastico uniforme.
    """
    np.random.seed(abs(hash(sentence.strip().lower())) % (2**32))
    vec = np.random.randn(dim)
    return vec / np.linalg.norm(vec)


def semantic_chunking(
    text: str,
    similarity_threshold_percentile: float = 60.0
) -> List[Dict[str, Any]]:
    """
    Segmenta un testo analizzando la dissimiglianza semantica tra frasi contigue.
    """
    sentences = [s.strip() for s in text.split(". ") if s.strip()]
    if len(sentences) <= 1:
        return [{"chunk_id": 0, "text": text, "sentences_count": len(sentences)}]

    # Calcolo degli embedding per ciascuna frase
    embeddings = [mock_sentence_encoder(s) for s in sentences]

    # Calcolo delle distanze del coseno tra frasi consecutive
    distances: List[float] = []
    for i in range(len(embeddings) - 1):
        cos_sim = cosine_similarity(embeddings[i], embeddings[i + 1])
        distances.append(1.0 - cos_sim)

    # Identificazione della soglia di rottura tramite percentile
    threshold = float(np.percentile(distances, similarity_threshold_percentile))

    chunks: List[Dict[str, Any]] = []
    current_chunk_sentences: List[str] = [sentences[0]]

    for i, dist in enumerate(distances):
        if dist > threshold:
            # Crea un nuovo chunk se la dissimiglianza supera la soglia
            chunk_text = ". ".join(current_chunk_sentences) + "."
            chunks.append({
                "chunk_id": len(chunks),
                "text": chunk_text,
                "sentences_count": len(current_chunk_sentences)
            })
            current_chunk_sentences = [sentences[i + 1]]
        else:
            current_chunk_sentences.append(sentences[i + 1])

    if current_chunk_sentences:
        chunk_text = ". ".join(current_chunk_sentences) + "."
        chunks.append({
            "chunk_id": len(chunks),
            "text": chunk_text,
            "sentences_count": len(current_chunk_sentences)
        })

    return chunks


def main() -> None:
    print("=== TEST 1: Metriche Geometriche di Similarita ===")
    v1 = np.array([0.5, 0.5, 0.5, 0.5])
    v2 = np.array([0.4, 0.6, 0.5, 0.5])
    v3 = np.array([-0.5, -0.5, -0.5, -0.5])

    print(f"Cosine Similarity (v1, v2): {cosine_similarity(v1, v2):.4f}")
    print(f"Euclidean Distance (v1, v2): {euclidean_distance(v1, v2):.4f}")
    print(f"Dot Product Normalizzato (v1, v2): {dot_product_normalized(v1, v2):.4f}")
    print(f"Cosine Similarity (v1, v3) [Opposti]: {cosine_similarity(v1, v3):.4f}")

    print("\n=== TEST 2: Semantic Chunking su Documento OSINT ===")
    sample_text = (
        "L'infrastruttura di comando e controllo e localizzata a Ginevra. "
        "I domini malevoli sono stati registrati tramite un provider anonimo. "
        "Le transazioni finanziarie correlate utilizzano wallet di criptovalute. "
        "La societa di copertura risulta formalmente registrata a Cipro nel 2021. "
        "L'amministratore fiduciario gestisce oltre quaranta entita offshore. "
        "Le analisi geospaziali evidenziano attivita insolita nei pressi del porto di Limassol. "
        "I server secondari sono configurati per inoltrare traffico cifrato verso un IP statico."
    )

    chunks = semantic_chunking(sample_text, similarity_threshold_percentile=60.0)
    for c in chunks:
        print(f"\n[Chunk {c['chunk_id']} - {c['sentences_count']} frasi]:")
        print(f"  {c['text']}")


if __name__ == "__main__":
    main()
```

### Laboratorio 2 — Motore di Ricerca Ibrido Vettoriale-Lessicale con RRF

Questo laboratorio realizza un'architettura completa di recupero ibrido che unisce un indice lessicale BM25 con un indice di similarità vettoriale, aggregando i risultati tramite l'algoritmo Reciprocal Rank Fusion ($k=60$) e applicando filtri sui metadati investigativi.

```python
"""
Laboratorio 2: Motore di Ricerca Ibrido con BM25, Vettori e Reciprocal Rank Fusion.
Modulo: D10 - RAG, Knowledge Base e Grafi OSINT
"""

import math
import re
from typing import List, Dict, Any, Tuple
import numpy as np


class SimpleBM25:
    """Implementazione pura dell'algoritmo di ranking probabilistico BM25."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avgdl = 0.0
        self.doc_lengths: List[int] = []
        self.doc_term_freqs: List[Dict[str, int]] = []
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())

    def fit(self, documents: List[str]) -> None:
        self.corpus_size = len(documents)
        self.doc_lengths = []
        self.doc_term_freqs = []
        total_len = 0
        df: Dict[str, int] = {}

        for doc in documents:
            tokens = self._tokenize(doc)
            self.doc_lengths.append(len(tokens))
            total_len += len(tokens)
            tf_dict: Dict[str, int] = {}
            for t in tokens:
                tf_dict[t] = tf_dict.get(t, 0) + 1
            self.doc_term_freqs.append(tf_dict)
            for t in tf_dict.keys():
                df[t] = df.get(t, 0) + 1

        self.avgdl = total_len / max(1, self.corpus_size)

        # Calcolo IDF con attenuazione standard Lucene
        for term, freq in df.items():
            self.idf[term] = math.log(1.0 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def score(self, query: str) -> List[float]:
        query_tokens = self._tokenize(query)
        scores = [0.0] * self.corpus_size

        for i in range(self.corpus_size):
            doc_len = self.doc_lengths[i]
            tf_dict = self.doc_term_freqs[i]
            for t in query_tokens:
                if t in tf_dict:
                    freq = tf_dict[t]
                    numerator = self.idf.get(t, 0.0) * freq * (self.k1 + 1.0)
                    denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                    scores[i] += numerator / denominator
        return scores


class HybridRetriever:
    """Motore di ricerca ibrido con indicizzazione sparsa, densa e fusione RRF."""

    def __init__(self, embedding_dim: int = 64):
        self.dim = embedding_dim
        self.documents: List[Dict[str, Any]] = []
        self.bm25 = SimpleBM25()
        self.embeddings: np.ndarray = np.empty((0, embedding_dim))

    def _mock_encode(self, text: str) -> np.ndarray:
        np.random.seed(abs(hash(text.strip().lower())) % (2**32))
        vec = np.random.randn(self.dim)
        return vec / np.linalg.norm(vec)

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        self.documents = docs
        raw_texts = [d["content"] for d in docs]
        self.bm25.fit(raw_texts)
        vec_list = [self._mock_encode(t) for t in raw_texts]
        self.embeddings = np.array(vec_list)

    def search(
        self,
        query: str,
        top_k: int = 3,
        rrf_k: int = 60,
        metadata_filter: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        # 1. Ricerca Lessicale BM25
        bm25_scores = self.bm25.score(query)
        ranked_bm25 = np.argsort(bm25_scores)[::-1]

        # 2. Ricerca Densa Vettoriale
        q_vec = self._mock_encode(query)
        dense_scores = np.dot(self.embeddings, q_vec)
        ranked_dense = np.argsort(dense_scores)[::-1]

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[int, float] = {}
        for rank, doc_idx in enumerate(ranked_bm25):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (rrf_k + rank + 1))

        for rank, doc_idx in enumerate(ranked_dense):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (rrf_k + rank + 1))

        # Ordinamento aggregato
        sorted_indices = sorted(rrf_scores.keys(), key=lambda idx: rrf_scores[idx], reverse=True)

        results: List[Dict[str, Any]] = []
        for idx in sorted_indices:
            doc = self.documents[idx]
            # Applicazione filtri sui metadati
            if metadata_filter:
                match = True
                for k, v in metadata_filter.items():
                    if doc.get("metadata", {}).get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            results.append({
                "doc_id": doc["id"],
                "content": doc["content"],
                "metadata": doc.get("metadata", {}),
                "rrf_score": round(rrf_scores[idx], 5),
                "bm25_raw_score": round(bm25_scores[idx], 4),
                "dense_raw_score": round(float(dense_scores[idx]), 4)
            })

            if len(results) >= top_k:
                break

        return results


def main() -> None:
    corpus = [
        {
            "id": "DOC-101",
            "content": "La societa Phantom Corp ha registrato il dominio secure-auth-login.com per condurre attacchi phishing.",
            "metadata": {"source": "OSINT Feed", "reliability": "A"}
        },
        {
            "id": "DOC-102",
            "content": "L'indirizzo IP 192.0.2.45 ospita server di comando per botnet Mirai localizzati in Europa Orientale.",
            "metadata": {"source": "SOC Report", "reliability": "B"}
        },
        {
            "id": "DOC-103",
            "content": "Phantom Corp e amministrata fiduciariamente da un cittadino elvetico coinvolto in indagini antiriciclaggio.",
            "metadata": {"source": "Registro Imprese", "reliability": "A"}
        },
        {
            "id": "DOC-104",
            "content": "Aggiornamento sulle vulnerabilita zero-day identificate nei sistemi industriali SCADA.",
            "metadata": {"source": "Security Advisory", "reliability": "A"}
        }
    ]

    engine = HybridRetriever(embedding_dim=64)
    engine.add_documents(corpus)

    query = "Phantom Corp server e domini phishing"
    print(f"Query investigativa: '{query}'")

    results = engine.search(query, top_k=3, rrf_k=60)
    for r in results:
        print(f"\n- [{r['doc_id']}] (Score RRF: {r['rrf_score']}) | BM25: {r['bm25_raw_score']} | Dense: {r['dense_raw_score']}")
        print(f"  Contenuto: {r['content']}")
        print(f"  Metadati: {r['metadata']}")


if __name__ == "__main__":
    main()
```

### Laboratorio 3 — Pipeline RAG Completa con Re-Ranking e Generazione Condizionata

Questo laboratorio assembla una pipeline end-to-end con recupero, re-ranking tramite cross-encoder simulato, generazione di prompt strutturato con citazioni formali e sintesi di risposta controllata.

```python
"""
Laboratorio 3: Pipeline RAG End-to-End con Re-Ranking e Prompt Grounding.
Modulo: D10 - RAG, Knowledge Base e Grafi OSINT
"""

import math
from typing import List, Dict, Any, Tuple
import numpy as np


class MockCrossEncoder:
    """Simulatore di Cross-Encoder basato su co-occorrenza di token e affinita sintattica."""

    def predict(self, pairs: List[Tuple[str, str]]) -> List[float]:
        scores = []
        for query, doc in pairs:
            q_words = set(query.lower().split())
            d_words = set(doc.lower().split())
            overlap = len(q_words.intersection(d_words))
            # Calcolo di uno score normalizzato
            base_score = float(overlap) / max(1.0, math.sqrt(len(q_words) * len(d_words)))
            scores.append(round(base_score, 4))
        return scores


class CompleteRAGPipeline:
    """Pipeline RAG modulare con recupero, re-ranking e sintesi vincolata."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.cross_encoder = MockCrossEncoder()

    def load_documents(self, docs: List[Dict[str, Any]]) -> None:
        self.documents = docs

    def retrieve_and_rerank(self, query: str, top_n: int = 2) -> List[Dict[str, Any]]:
        # 1. Recupero iniziale (candidati)
        candidates = [dict(d) for d in self.documents]

        # 2. Re-Ranking tramite Cross-Encoder
        pairs = [(query, c["text"]) for c in candidates]
        rerank_scores = self.cross_encoder.predict(pairs)

        for i, score in enumerate(rerank_scores):
            candidates[i]["rerank_score"] = score

        # Ordinamento decrescente
        sorted_candidates = sorted(candidates, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        return sorted_candidates[:top_n]

    def build_grounded_prompt(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        context_str = ""
        for chunk in context_chunks:
            context_str += f"[{chunk['id']}] (Fonte: {chunk['source']})\n{chunk['text']}\n\n"

        prompt = (
            "Sei un analista di intelligence che sintetizza evidenze documentali.\n"
            "Attieniti rigorosamente al contesto riportato di seguito. Non inventare dettagli non presenti.\n"
            "Per ciascuna conclusione, indica la relativa fonte esplicita [DOC-ID].\n\n"
            f"=== CONTESTO DOCUMENTALE ===\n{context_str}"
            f"=== DOMANDA DELL'ANALISTA ===\n{query}\n\n"
            "=== RISPOSTA STRUTTURATA ==="
        )
        return prompt

    def simulate_llm_inference(self, prompt: str) -> str:
        """
        Simula l'inferenza generativa eseguendo un'estrazione vincolata delle evidenze.
        """
        return (
            "Sulla base delle evidenze documentali raccolte:\n"
            "1. La societa Alpha Corp detiene la titolarita esclusiva dell'infrastruttura server 198.51.100.12 [DOC-1].\n"
            "2. Da tale server sono stati esfiltrati dati cifrati verso un nodo Tor [DOC-2].\n"
            "Sintesi: L'asset controllato da Alpha Corp e direttamente implicato nel canale di esfiltrazione."
        )


def main() -> None:
    knowledge_base = [
        {
            "id": "DOC-1",
            "source": "Report Forense",
            "text": "La societa Alpha Corp detiene la titolarita esclusiva dell'infrastruttura server 198.51.100.12."
        },
        {
            "id": "DOC-2",
            "source": "Log Analisi di Rete",
            "text": "Dal server 198.51.100.12 sono stati esfiltrati 4.2 gigabyte di dati cifrati verso un nodo di uscita Tor."
        },
        {
            "id": "DOC-3",
            "source": "Rassegna Stampa",
            "text": "Alpha Corp ha inaugurato una nuova sede amministrativa a Singapore lo scorso mese."
        }
    ]

    rag = CompleteRAGPipeline()
    rag.load_documents(knowledge_base)

    query = "Quale ruolo ha avuto il server di Alpha Corp nell'esfiltrazione dei dati?"
    print(f"Esecuzione Pipeline RAG per la query: '{query}'\n")

    top_chunks = rag.retrieve_and_rerank(query, top_n=2)
    prompt = rag.build_grounded_prompt(query, top_chunks)

    print("=== PROMPT COSTRUITO ===")
    print(prompt)

    print("\n=== GENERAZIONE MODELLO (SIMULATA) ===")
    response = rag.simulate_llm_inference(prompt)
    print(response)


if __name__ == "__main__":
    main()
```

### Laboratorio 4 — Grafo OSINT e Recupero Strutturato GraphRAG

Questo laboratorio costruisce una base di conoscenza a grafo per un'investigazione OSINT utilizzando la libreria [NetworkX](https://networkx.org/) e generando comandi Cypher standard per [Neo4j](https://neo4j.com/). Il grafo viene interrogato per individuare connessioni nascoste tra persone e server malevoli, serializzando il cammino relazionale per l'LLM.

```python
"""
Laboratorio 4: Knowledge Graph OSINT con NetworkX e Query Cypher.
Modulo: D10 - RAG, Knowledge Base e Grafi OSINT
"""

from typing import List, Dict, Any, Tuple
import networkx as nx


class OSINTKnowledgeGraph:
    """Gestione del Grafo della Conoscenza OSINT con NetworkX e Cypher."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity_id: str, label: str, properties: Dict[str, Any]) -> None:
        self.graph.add_node(entity_id, label=label, **properties)

    def add_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any] = None) -> None:
        props = properties or {}
        self.graph.add_edge(source_id, target_id, rel_type=rel_type, **props)

    def export_cypher_script(self) -> str:
        """Genera lo script Cypher per importare il grafo in Neo4j."""
        cypher_lines = ["// Creazione Nodi OSINT"]
        for node_id, data in self.graph.nodes(data=True):
            label = data.get("label", "Entity")
            props_str = ", ".join([f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" for k, v in data.items() if k != "label"])
            cypher_lines.append(f"MERGE (n:{label} {{id: '{node_id}', {props_str}}});")

        cypher_lines.append("\n// Creazione Relazioni")
        for u, v, data in self.graph.edges(data=True):
            rel_type = data.get("rel_type", "RELATED_TO")
            cypher_lines.append(f"MATCH (a {{id: '{u}'}}), (b {{id: '{v}'}}) MERGE (a)-[:{rel_type}]->(b);")

        return "\n".join(cypher_lines)

    def find_shortest_connection(self, source_id: str, target_id: str) -> List[Tuple[str, str, str]]:
        """Trova il percorso relazionale minimo tra due entita."""
        if not nx.has_path(self.graph, source_id, target_id):
            return []
        path = nx.shortest_path(self.graph, source_id, target_id)
        rel_chain = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge_data = self.graph.get_edge_data(u, v)
            rel_type = edge_data.get("rel_type", "RELATED")
            rel_chain.append((u, rel_type, v))
        return rel_chain

    def extract_subgraph_context(self, entity_id: str, depth: int = 2) -> str:
        """Estrae l'ego-network e lo formatta come contesto per prompt GraphRAG."""
        ego = nx.ego_graph(self.graph, entity_id, radius=depth, undirected=True)
        lines = [f"Grafo di prossimita per l'entita '{entity_id}':"]
        for u, v, data in ego.edges(data=True):
            u_label = ego.nodes[u].get("label", "Node")
            v_label = ego.nodes[v].get("label", "Node")
            rel = data.get("rel_type", "CONNECTED_TO")
            lines.append(f"- ({u_label}: {u}) --[{rel}]--> ({v_label}: {v})")
        return "\n".join(lines)


def main() -> None:
    kg = OSINTKnowledgeGraph()

    # Creazione Entita
    kg.add_entity("PERSON_01", "Person", {"name": "Mario Rossi", "role": "Direttore Fiduciario"})
    kg.add_entity("ORG_ALPHA", "Organization", {"name": "Alpha Holding Ltd", "jurisdiction": "Cipro"})
    kg.add_entity("ORG_BETA", "Organization", {"name": "Beta Telecom", "jurisdiction": "Isole Vergini"})
    kg.add_entity("SERVER_99", "Server", {"ip": "198.51.100.42", "service": "C2 Botnet"})

    # Creazione Relazioni
    kg.add_relationship("PERSON_01", "ORG_ALPHA", "DIRECTS", {"since": 2020})
    kg.add_relationship("ORG_ALPHA", "ORG_BETA", "CONTROLS_SHARES", {"percentage": 100})
    kg.add_relationship("ORG_BETA", "SERVER_99", "OWNS_INFRASTRUCTURE", {"registered": "2023-01-15"})

    print("=== EXPORT QUERY CYPHER PER NEO4J ===")
    print(kg.export_cypher_script())

    print("\n=== ANALISI DEI PERCORSI RELAZIONALI (Path Finding) ===")
    start_node = "PERSON_01"
    target_node = "SERVER_99"
    connection = kg.find_shortest_connection(start_node, target_node)

    print(f"Catena di connessione tra '{start_node}' e '{target_node}':")
    for step in connection:
        print(f"  ({step[0]}) ---[:{step[1]}]---> ({step[2]})")

    print("\n=== CONTESTO ESTRATTO PER PROMPT GRAPHRAG ===")
    context = kg.extract_subgraph_context("PERSON_01", depth=2)
    print(context)


if __name__ == "__main__":
    main()
```