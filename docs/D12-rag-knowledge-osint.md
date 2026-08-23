---
aliases:
- D12
- RAG
- Retrieval Augmented Generation
- Knowledge Base
- Vector DB
- Grafi OSINT
- Neo4j
- GraphRAG
resources:
- title: LangChain Documentation
  url: https://python.langchain.com/docs/get_started/introduction
  type: ref
- title: OSINT Framework
  url: https://osintframework.com/
  type: ref
---
# Retrieval-Augmented Generation, Database Vettoriali e Knowledge Graph per l'Intelligence OSINT

Il pattern architetturale di **Retrieval-Augmented Generation (RAG)** integra modelli generativi basati su Transformer con sistemi di recupero informativo esterni, arricchendo dinamicamente il contesto d'inferenza con porzioni documentali pertinenti estratte da basi di conoscenza eterogenee. Questa tecnologia trova impiego primario nell'analisi di intelligence su fonti aperte ([D11](D13-osint-avanzato.md)), nell'investigazione forense su corpus non strutturati e nei sistemi aziendali di question answering ad alta precisione dove i modelli linguistici pre-addestrati soffrono di obsolescenza conoscitiva o allucinazioni fattuali. Il RAG esiste per disaccoppiare la capacità di ragionamento logico-linguistico dell'LLM dalla memorizzazione statica dei parametri sinaptici, consentendo aggiornamenti tempestivi dei dati, verificabilità delle fonti tramite citazioni puntuali e pieno controllo sulla sovranità informativa.

## Il Limite Strutturale dei Pesi Parametrici e la Genesi del RAG

### La Metafora: L'Esame a Memoria vs l'Esame con la Biblioteca Aperta
Immagina uno studente brillante che deve sostenere un esame di medicina o condurre un'indagine poliziesca complessa. Se gli imponi di fare affidamento solo su ciò che ha imparato a memoria tre anni fa (la **memoria parametrica** congelata nei suoi neuroni), si troverà completamente disarmato di fronte a una legge approvata ieri mattina o al rapporto confidenziale su una nuova società offshore. Se prova a rispondere comunque a ogni costo, per non ammettere di non sapere tenderà a inventare dettagli convincenti ma totalmente inventati: le famigerate **allucinazioni**.

Costringerlo a ristudiare da capo l'intera enciclopedia medica ogni singola notte tramite riaddestramento supervisionato (fine-tuning) richiederebbe mesi di lavoro, costi esorbitanti e rischierebbe di fargli dimenticare le nozioni di base (*catastrophic forgetting*). 

La soluzione più intelligente è trasformare l'esame in una prova a "libro aperto": invece di fargli memorizzare trilioni di fatti, gli affianchiamo un **archivista iper-veloce** (il *Retriever*). Quando l'analista pone una domanda, l'archivista corre nella biblioteca esterna, seleziona i 3 o 4 fascicoli rilevanti e li mette aperti sul tavolo del nostro studente. A quel punto lo studente (il Large Language Model) deve soltanto leggere quei fogli, estrarre le evidenze e sintetizzare la risposta citando il numero esatto della pagina.

### Fondamenti Teorici e Disaccoppiamento
I Large Language Model descritti nel modulo [D09](D11-transformers-llm.md) codificano la propria conoscenza all'interno di matrici di pesi sinaptici calcolate durante fasi di pre-addestramento statico. Questa memoria parametrica presenta tre vulnerabilità sistemiche insormontabili nelle investigazioni su dati dinamici:
1. **Knowledge Cutoff**: la conoscenza si arresta alla data di chiusura del dataset di addestramento.
2. **Allucinazioni Fattuali**: il modello colma le lacune informative generando sequenze statisticamente probabili ma prive di riscontro oggettivo.
3. **Mancanza di Tracciabilità e Accesso a Dati Riservati**: l'accesso a note investigative o feed OSINT in tempo reale risulta strutturalmente impossibile senza un meccanismo di iniezione contestuale.

Il disaccoppiamento tra il motore di inferenza linguistica e il deposito informativo non parametrico, formalizzato nello studio pionieristico su [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) sviluppato da [Meta AI](https://ai.meta.com/), trasferisce l'onere della veridicità fattuale dai pesi probabilistici del modello a record documentali espliciti, tracciabili e immediatamente revocabili o aggiornabili.

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

> [!INTERACTIVE] WIDGET: Il Detective a Memoria Chiusa vs con Fascicolo RAG
> Un simulatore a doppio pannello: a sinistra l'utente interroga un LLM a memoria pura (senza contesto) su un bersaglio OSINT recente, osservando la generazione di allucinazioni evidenziate in rosso su date e società inesistenti; a destra, attivando il toggle "RAG Pipeline", il simulatore mostra l'estrazione in tempo reale dei frammenti documentali da un database vettoriale, l'assemblaggio del prompt contestualizzato e la generazione di una sintesi verificabile con badge cliccabili delle fonti `[DOC-1]`, `[DOC-2]`.

## La Meccanica dei Vettori di Embedding e le Metriche di Distanza Spaziale

### La Metafora: La Mappa delle Costellazioni e lo Spazio dei Sapori
Immagina di voler catalogare centinaia di cibi in una grande stanza tridimensionale non in base all'ordine alfabetico, ma in base al loro "profilo di gusto". Immagina che l'asse $X$ rappresenti la *dolcezza*, l'asse $Y$ la *salinità* e l'asse $Z$ la *croccantezza*.
- Se infili nella stanza una "torta al cioccolato" e una "crostata di fragole", entrambe avranno valori altissimi di dolcezza e bassi di salinità: le due frecce che partono dal centro della stanza per indicare questi due dolci punteranno quasi nella stessa identica direzione!
- Se invece posizioni una "pizza margherita", la sua freccia punterà verso la salinità, distante dalla torta.

Nei modelli di **embedding**, invece di avere soltanto 3 assi di sapore, abbiamo uno spazio vettoriale continuo $\mathbb{R}^d$ con centinaia o migliaia di dimensioni (es. $d=384, 768, 1536, 3072$). Ogni asse rappresenta una sfumatura concettuale astratta appresa dalla rete neurale. Due testi che parlano dello stesso argomento (anche usando parole diverse come "incursione informatica" e "cyber attack") generano due frecce che puntano nella stessa direzione nello spazio multidimensionale.

### Formule Matematiche e Traduzione dei Simboli

Per confrontare matematicamente la freccia della domanda dell'analista $u \in \mathbb{R}^d$ con la freccia di un documento archiviato $v \in \mathbb{R}^d$, utilizziamo tre metriche geometriche fondamentali calcolate mediante la libreria [NumPy](https://numpy.org/).

#### 1. Cosine Similarity (Similarità del Coseno)
Misura il coseno dell'angolo $\theta$ compreso tra le due frecce, valutando se puntano nella stessa direzione a prescindere dalla loro lunghezza assoluta (ossia senza farsi ingannare dalla lunghezza del testo):

$$\text{Cosine}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2} = \frac{\sum_{i=1}^d u_i v_i}{\sqrt{\sum_{i=1}^d u_i^2} \sqrt{\sum_{i=1}^d v_i^2}}$$

**Traduzione dei simboli dalla metafora:**
- $u$ e $v$: le due frecce direzionali nello spazio (il vettore della query e il vettore del documento).
- $d$: il numero di dimensioni o assi concettuali dello spazio semantico (da 384 a 3072 assi).
- $u_i, v_i$: la coordinata del testo lungo il singolo asse $i$-esimo (quanto "pesa" quel concetto sull'asse $i$).
- $\sum_{i=1}^d u_i v_i$: il prodotto scalare al numeratore, che somma le coincidenze asse per asse.
- $\|u\|_2 = \sqrt{\sum_{i=1}^d u_i^2}$ e $\|v\|_2 = \sqrt{\sum_{i=1}^d v_i^2}$: la lunghezza complessiva (norma euclidea $L_2$) delle frecce.
- **Valori**: Se l'angolo è $0^\circ$ (frecce parallele concordi, significato identico), il coseno vale **$1$**. Se l'angolo è $90^\circ$ (ortogonali, nessun legame), vale **$0$**. Se puntano in direzioni opposte, vale **$-1$**.
- La corrispondente **Distanza del Coseno** misura la separazione: $D_{\text{cos}}(u, v) = 1 - \text{Cosine}(u, v)$, assumendo valori compresi tra 0 (vettori identici) e 2 (vettori opposti).

#### 2. Dot Product (Prodotto Scalare / Inner Product)
Calcola la somma delle moltiplicazioni asse per asse tra le due frecce:

$$\langle u, v \rangle = \sum_{i=1}^d u_i v_i$$

**Traduzione dei simboli dalla metafora:**
- Se preventivamente accorciamo o allunghiamo tutte le frecce per avere lunghezza esattamente unitaria ($\|u\|_2 = \|v\|_2 = 1$), il prodotto scalare coincide esattamente con la similarità del coseno, permettendo calcoli ultra-veloci tramite istruzioni hardware SIMD e moltiplicazioni matriciali su GPU.

#### 3. Euclidean Distance (Distanza Euclidea $L_2$)
Rappresenta la distanza ordinaria in linea d'aria tra le punte delle due frecce, come se tirassimo un righello tra i due punti nello spazio:

$$D_{L2}(u, v) = \|u - v\|_2 = \sqrt{\sum_{i=1}^d (u_i - v_i)^2}$$

**Traduzione dei simboli dalla metafora:**
- $(u_i - v_i)$: lo scarto tra le coordinate del documento e della query sull'asse $i$-esimo.
- Quando i vettori sono normalizzati a norma unitaria, vale l'equivalenza geometrica $\|u - v\|_2^2 = 2 - 2 \cdot \text{Cosine}(u, v)$, rendendo l'ordinamento di prossimità identico a quello del coseno.

Negli spazi a elevatissima dimensionalità subentra il fenomeno noto come **maledizione della dimensionalità** (*Curse of Dimensionality*), per cui le distanze tra coppie di punti casuali tendono a concentrarsi in un intervallo ristretto. Per mantenere una forte capacità discriminante, i moderni modelli di embedding ([Sentence-Transformers](https://www.sbert.net/), OpenAI) adottano tecniche di *contrastive learning* (come la funzione di perdita InfoNCE), che attraggono tra loro frasi semanticamente simili e respingono energicamente esempi negativi dissimili.

> [!INTERACTIVE] WIDGET: Bussola Semantica 3D & Misuratore di Angoli Vettoriali
> Un ambiente tridimensionale interattivo in cui l'utente può ruotare lo spazio e muovere due vettori (freccia Blu = Query, freccia Arancione = Documento) tramite slider di coordinate o selezionando coppie di frasi preimpostate (es. "Attacco Hacker" vs "Incursione Cyber" vs "Torta di mele"). Il widget calcola e aggiorna in tempo reale l'angolo $\theta$, la Cosine Similarity, il Prodotto Scalare e la Distanza Euclidea $L_2$, mostrando graficamente la sfera unitaria e il cono di prossimità.

> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D10-rag-knowledge-osint. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.

## Strategie di Segmentazione Documentale (Chunking)

### La Metafora: Tagliare un Rotolo di Pergamena o Montare un Film
Immagina di dover archiviare un lungo rotolo di pergamena contenente la trascrizione di un processo o un fascicolo d'intelligence:
1. **Finestra fissa (Taglio col righello)**: prendi le forbici e tagli il rotolo ogni 20 centimetri esatti. Il rischio? Taglierai a metà un nome decisivo ("Mario [TAGLIO] Rossi") o un numero di conto. Per limitare i danni, introduci la *sovrapposizione (overlap)*: fai in modo che ogni striscia contenga gli ultimi 5 centimetri della striscia precedente.
2. **Ricorsivo (Taglio secondo i paragrafi)**: rispetti la gerarchia naturale del testo. Tagli prima dove ci sono i capitoli (`\n\n`), poi dove finiscono i paragrafi (`\n`), poi ai punti delle frasi (`. `), e tagli a livello di singola parola solo se il testo è ancora troppo lungo per entrare nella cartellina.
3. **Semantico (Il montatore cinematografico)**: un montatore esperto non taglia la pellicola a intervalli fissi di secondi, ma ascolta il dialogo. Finché i protagonisti parlano dello stesso argomento, la scena continua; non appena la conversazione cambia bruscamente tema, il montatore fa scattare il "ciak" e separa le scene.

```
STRATEGIE DI CHUNKING:
1. Finestra Fissa:    [────── Chunk 1 ──────]
                                   [────── Chunk 2 ──────]  (Overlap costante)
2. Gerarchico:        [# Titolo H1 ──► ## Sezione H2 ──► Paragrafo singolo]
3. Semantico:         [Frase A. Frase B.] || Drop di similarità || [Frase C. Frase D.]
```

### Meccanismi Operativi di Segmentazione

La segmentazione a finestra fissa con sovrapposizione (*Fixed-Size Chunking with Overlap*) suddivide il testo grezzo in finestre di ampiezza definita (ad esempio 512 token) con un margine di sovrapposizione mobile (50–100 token). Questa sovrapposizione impedisce che un'entità nominale o una proposizione logica cruciale situata sul confine del taglio venga spezzata, ma soffre di arbitrarietà sintattica.

La segmentazione ricorsiva (*Recursive Character Chunking*) preserva la gerarchia naturale tentando la separazione in corrispondenza di delimitatori semantici progressivamente più fini: interruzioni di paragrafo (`\n\n`), interruzioni di riga (`\n`), segni di punteggiatura forte (`. `, `? `, `! `) e infine spazi bianchi. L'algoritmo aggrega porzioni contigue fino alla dimensione limite, garantendo che i confini dei frammenti coincidano quasi sempre con la fine di un periodo di senso compiuto.

La segmentazione semantica (*Semantic Chunking*) calcola l'embedding per ogni singola frase del documento e misura la distanza del coseno tra frasi adiacenti lungo l'intero testo. Quando la dissimiglianza semantica tra due frasi consecutive supera una determinata soglia statistica (ad esempio il 60° o 85° percentile della varianza delle distanze locali), l'algoritmo individua un punto di rottura naturale, isolando blocchi internamente coesi per argomento ed evitando l'inquinamento contestuale tra sezioni eterogenee.

> [!INTERACTIVE] WIDGET: Il Taglia-Documenti Semantico (Chunking Playground)
> Uno strumento visivo in cui incollare un testo d'indagine OSINT. Un grafico dinamico sotto il testo mostra la "curva di discontinuità semantica" tra frasi consecutive calcolata tramite distanze di coseno. Muovendo uno slider della soglia di taglio (percentile di tolleranza), l'utente vede comparire istantaneamente le linee di frattura verticali colorate che evidenziano i blocchi (*chunk*) risultanti, mostrando come un taglio intelligente prevenga lo spezzamento delle relazioni logiche.

## Strutture Dati e Indici per Database Vettoriali (ANN)

### La Metafora: Trovare un Amico in una Metropoli da 10 Milioni di Abitanti
Immagina di dover rintracciare un sosia all'interno di una metropoli sterminata avendo a disposizione solo il suo identikit:
- **Scansione Esatta (Flat Search)**: suonare a tutti i 10 milioni di campanelli, uno dopo l'altro. Troverai la persona con certezza assoluta, ma ci impiegherai anni ($O(N \cdot d)$).
- **Indice IVF-Flat (I Quartieri e i Cartelli Stradali)**: raggruppi la città in 1000 quartieri (celle di Voronoi). All'ingresso di ogni quartiere c'è un cartello (centroide) con i tratti somatici prevalenti degli abitanti. Quando cerchi il sosia, visiti solo i cartelli dei 3 o 4 quartieri più compatibili ($nprobe$) e suoni solo ai campanelli di quelle poche vie.
- **Product Quantization (PQ - L'Identikit Compresso a Bassa Risoluzione)**: per non consumare tutta la memoria RAM, invece di archiviare fotografie a 50 megapixel per ogni cittadino, assegni a ciascuno una combinazione compatta di codici colore a 8 bit, calcolando le distanze istantaneamente tramite tabelle di conversione precalcolate nella cache della CPU.
- **Indice HNSW (La Rete Stradale: Voli, Autostrade e Vicoli)**: organizzi la città come una mappa stradale a strati. Al livello più alto ci sono "voli aerei" a lunghissimo raggio che ti fanno attraversare la nazione in due salti per arrivare nella regione giusta; poi scendi allo strato delle autostrade, poi alla tangenziale e infine cammini nei vicoli locali fino alla porta esatta in pochissimi passi ($O(\log N)$).

```
INDICI VETTORIALI:
- IVF-Flat: Partizionamento in Celle di Voronoi (Ispezione mirata dei centroidi nprobe)
- PQ:       Compressione in sottospazi discretizzati (Codifica quantizzata in cache)
- HNSW:     Grafo a strati multi-livello (Instradamento greedy rapido O(log N))
```

### Algoritmi di Ricerca Approssimata dei Vicini (ANN)

Quando il corpus scala a milioni di frammenti, la scansione sequenziale esatta $O(N \cdot d)$ diventa incompatibile con i tempi di risposta interattivi. Gli algoritmi ANN (*Approximate Nearest Neighbors*) scambiano una quota controllata di accuratezza statistica (*recall*) con una drastica accelerazione computazionale.

L'indice ad albero e partizionamento cellulare **IVF-Flat (Inverted File Flat)** raggruppa lo spazio vettoriale in $K$ celle di Voronoi attorno a centroidi calcolati durante una fase preliminare di addestramento tramite clustering K-Means ([D07](D09-unsupervised-learning.md)). In fase di query, il sistema calcola la distanza soltanto verso i centroidi, esplorando esclusivamente i vettori contenuti nelle $nprobe$ celle più vicine.

La tecnica di **Product Quantization (PQ)** comprime l'occupazione in memoria dividendo ogni vettore $d$-dimensionale in $m$ sottovettori a bassa dimensione e associando a ciascuno il codice identificativo del centroide più vicino all'interno di un codebook discretizzato. Le distanze asimmetriche vengono calcolate ad altissima velocità interrogando tabelle pre-calcolate memorizzate direttamente nella cache della CPU.

La struttura a grafo gerarchico **HNSW (Hierarchical Navigable Small World)** rappresenta lo stato dell'arte per prestazioni e compromesso tra latenza e recall. Ispirata alle *skip-list* probabilistiche, HNSW organizza i vettori su livelli multipli sovrapposti di grafi navigabili: gli strati superiori contengono pochi nodi connessi da archi lunghi per convergere velocemente verso la regione di interesse, mentre gli strati inferiori aumentano progressivamente la densità dei collegamenti per affinare localmente la selezione dei vicini con complessità temporale $O(\log N)$.

Il panorama delle tecnologie di indicizzazione vettoriale include:
- **Calcolo puro ad altissime prestazioni**: [FAISS](https://github.com/facebookresearch/faiss) di [Meta AI](https://ai.meta.com/) (ottimizzato su GPU e istruzioni AVX-512).
- **Ambienti embedded e locali**: [ChromaDB](https://www.trychroma.com/) e [LanceDB](https://lancedb.com/) (basati su formato colonnare o [SQLite](https://www.sqlite.org/)).
- **Database distribuiti enterprise**: [Qdrant](https://qdrant.tech/) (in Rust, con payload indexing avanzato), [Weaviate](https://weaviate.io/), [Milvus](https://milvus.io/) e il servizio cloud gestito [Pinecone](https://www.pinecone.io/).
- **Integrazione SQL relazionale**: l'estensione [pgvector](https://github.com/pgvector/pgvector) per [PostgreSQL](https://www.postgresql.org/).

> [!INTERACTIVE] WIDGET: Simulatore di Navigazione su Grafo HNSW vs Scansione Flat
> Un canvas interattivo a strati 3D che simula un indice HNSW. L'utente definisce un punto di query e avvia l'animazione: si osserva il cursore compiere salti veloci tra pochi nodi macroscopici nello strato superiore (Layer 2), scendere al livello intermedio (Layer 1) e atterrare nello strato denso (Layer 0) per localizzare i vicini più prossimi con pochissimi confronti (step counter $O(\log N)$) rispetto al contatore lineare esaustivo di una Flat Search ($O(N)$).

> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.

## Ricerca Ibrida e Pipeline di Re-Ranking

### La Metafora: L'Investigatore Intuitivo, l'Archivista Pignolo e la Giuria d'Appello
Nelle indagini reali, affidarsi solo ai vettori di embedding ha un punto debole:
- La **ricerca densa (vettori)** è come un *investigatore con intuito*: capisce i concetti astratti (se cerchi "veicolo di fuga", ti trova documenti con "auto rubata" o "furgone nero"). Ma se gli chiedi un codice fiscale preciso (`RSSMRA85T10H501Z`), un hash MD5 o una targa, il suo intuito si confonde perché quelle sigle alfanumeriche non hanno un significato concettuale nel vocabolario dei modelli.
- La **ricerca sparsa (BM25)** è come un *archivista pignolo con la lente d'ingrandimento*: cerca esattamente le lettere e i numeri della parola chiave, senza sbagliare una virgola, ma non capisce i sinonimi.
- L'algoritmo **RRF (Reciprocal Rank Fusion)** è il *tabellone dei punteggi di una gara combinata*: prende la classifica dell'investigatore intuitivo e la classifica dell'archivista pignolo e assegna punti inversamente proporzionali al piazzamento. Chi si posiziona bene in entrambe le gare vince la medaglia d'oro!
- Il **Cross-Encoder (Re-Ranking)** è il *giudice della corte d'appello*: prende i 5 migliori finalisti emersi dalla combinazione e legge attentamente, parola per parola e token per token, la domanda insieme a ciascun documento, cogliendo ogni minima sfumatura ed eliminando i falsi positivi.

```
PIPELINE DI RECUPERO IBRIDO E RE-RANKING:
[ Query Utente ] ──┬──► [ Ricerca Sparsa BM25 ] ───► [ Top-100 Candidati ] ──┐
                   │                                                         ├──► [ RRF Fusion ] ──► [ Cross-Encoder ] ──► [ Top-5 Chunks ]
                   └──► [ Ricerca Densa Vettori ] ──► [ Top-100 Candidati ] ──┘
```

### Formule Matematiche: BM25 e Reciprocal Rank Fusion (RRF)

L'algoritmo **BM25 (Best Matching 25)** valuta la frequenza locale dei termini della query ponderata per l'inverso della frequenza documentale globale (IDF), penalizzando i documenti troppo lunghi. 

Per combinare l'ordinamento lessicale di BM25 con quello denso vettoriale senza problemi di calibrazione delle scale di punteggio, si adotta la formula del **Reciprocal Rank Fusion (RRF)**:

$$RRF(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

**Traduzione dei simboli dalla metafora:**
- $d \in D$: il singolo documento candidato all'interno dell'archivio documentale $D$.
- $M$: l'insieme dei metodi di recupero impiegati (nel nostro caso $M = \{\text{BM25 (lessicale)}, \text{Vettoriale (denso)}\}$).
- $r_m(d)$: la posizione ordinale o piazzamento (rank: 1°, 2°, 3°...) assegnata al documento $d$ dal metodo $m$.
- $k$: la costante di smorzamento (convenzionalmente fissata a $k=60$). Agisce come "cuscinetto di sicurezza": impedisce che una vittoria al 1° posto su un singolo metodo sbaragli ingiustamente un documento che è arrivato 2° o 3° in modo solido e consistente su entrambi i canali.

Una volta estratti i migliori $N$ candidati (es. $N=50$) tramite RRF, la pipeline applica il **Cross-Encoder Re-Ranking**. A differenza dei Bi-Encoder che elaborano query e documenti separatamente, i modelli Cross-Encoder elaborano la coppia congiuntamente all'interno dello stesso meccanismo di Self-Attention, valutando le interazioni token-a-token a livello profondo per selezionare i 3–5 frammenti di massima rilevanza da passare al contesto dell'LLM.

> [!INTERACTIVE] WIDGET: Banco di Prova Ricerca Ibrida (BM25 + Dense + RRF Explorer)
> Un'interfaccia interattiva a tre colonne affiancate: la Colonna 1 mostra la graduatoria lessicale BM25, la Colonna 2 mostra la graduatoria vettoriale densa, e la Colonna 3 calcola istantaneamente il punteggio RRF combinato. L'utente può digitare query con codici alfanumerici (es. "CVE-2024-1234 exploit buffer overflow") o concetti astratti, regolare lo slider della costante $k$ ($1 \le k \le 100$) e trascinare i candidati in un modulo Cross-Encoder finale per visualizzare la scrematura dei falsi positivi.

## Knowledge Graph, Neo4j e GraphRAG per l'Intelligence OSINT

### La Metafora: La Bacheca Investigativa coi Fili Rossi di Lana
Immagina la tipica bacheca di sughero di un commissariato di polizia: foto di sospettati, fotocopie di visure camerali, indirizzi di server e coordinate GPS, tutti collegati da **fili rossi di lana** con etichette scritte col pennarello (*"è socio di"*, *"amministra l'azienda"*, *"possiede il server"*).

Se prendi tutti i tuoi verbali investigativi e li triti in piccoli coriandoli rettangolari (i *chunk* vettoriali classici), tagli inevitabilmente tutti i fili di lana. Se il Documento A afferma che *"Marco Bianchi è titolare della società Alpha"* e il Documento B dice che *"La società Alpha possiede l'indirizzo IP malevolo 198.51.100.42"*, un RAG vettoriale tradizionale non collegherà mai Marco Bianchi all'indirizzo IP, a meno che non estragga per pura fortuna entrambi i foglietti contemporaneamente.

Il **Knowledge Graph (Grafo della Conoscenza)** preserva intatta l'intera rete di fili rossi. Con una semplice interrogazione a grafo, puoi chiedere: *"Segui i fili rossi e mostrami qualsiasi persona collegata a questo server con un massimo di 3 passaggi di distanza"*. L'architettura **GraphRAG** unisce la navigazione di questi fili con l'elaborazione dei testi dell'LLM!

```
MODELLO PROPERTY GRAPH (OSINT INTELLIGENCE):
(Persona: "Mario Rossi") ──[:DIRECTS {dal: "2021"}]──► (Azienda: "Alpha Ltd")
                                                            │
                                                     [:OWNS_INFRASTRUCTURE]
                                                            │
                                                            ▼
                                                   (Server: "198.51.100.42")
```

### Il Modello Property Graph, Neo4j e i Quattro Stadi di GraphRAG

Nel modello a grafi di proprietà (*Property Graph*), le entità del mondo reale (persone, organizzazioni, server, wallet crypto) sono rappresentate come nodi etichettati con attributi chiave-valore, mentre le interazioni costituiscono archi orientati e tipizzati. Il sistema di riferimento è [Neo4j](https://neo4j.com/), che adotta il linguaggio dichiarativo **Cypher** per esprimere pattern matching complessi e cammini multi-hop con estrema concisione:

```cypher
MATCH (p:Person)-[:WORKS_FOR|DIRECTS]->(o:Organization)-[:OWNS_INFRASTRUCTURE]->(s:Server)
WHERE s.ip_address = "198.51.100.42"
RETURN p.name, o.legal_name, s.ip_address
```

L'approccio **GraphRAG** fonde la potenza dei grafi con il recupero vettoriale attraverso quattro stadi operativi:
1. **Estrazione di Entità e Relazioni**: i documenti vengono analizzati tramite LLM o Named Entity Recognition per estrarre triplette strutturate $(Soggetto, Predicato, Oggetto)$.
2. **Entity Resolution e Deduplicazione**: le menzioni ambigue (acronimi, pseudonimi) vengono normalizzate in entità uniche tramite librerie come [NetworkX](https://networkx.org/).
3. **Community Detection e Sintesi Gerarchica**: algoritmi di clustering su grafi identificano comunità densamente connesse, generando riassunti tematici ad alto livello per ciascun cluster di nodi.
4. **Recupero Contestuale Ibrido**: di fronte a una query complessa, il sistema estrae il sottografo di vicinato (*ego-network*) relativo alle entità identificate e lo serializza in formato testuale strutturato, affiancandolo ai chunk vettoriali estratti tramite [LangChain](https://www.langchain.com/) o [LlamaIndex](https://www.llamaindex.ai/).

Nelle operazioni di intelligence su fonti aperte ([D11](D13-osint-avanzato.md)), il GraphRAG permette di tracciare catene societarie opache, individuare nodi cardine di disinformazione tramite metriche di centralità (*betweenness centrality*) e correlare minacce cyber identificando infrastrutture condivise ([D11b](D13b-ai-arma-bersaglio-osint.md)).

> [!INTERACTIVE] WIDGET: Bacheca Investigativa a Grafo (Multi-Hop Graph Explorer)
> Una mappa nodale dinamica interattiva raffigurante un'indagine OSINT: nodi colorati (Persone in blu, Società in verde, Server in rosso, Conti bancari in giallo) connessi da frecce direzionate. Cliccando sul pulsante "Trova Catena di Controllo", l'algoritmo calcola ed evidenzia in giallo pulsante il percorso minimo tra l'entità bersaglio e l'infrastruttura sospetta, generando istantaneamente la corrispondente clausola Cypher (`MATCH ... RETURN`) e il blocco di contesto per il prompt LLM.

> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.

## Prompt Engineering per RAG, Grounding e Valutazione Quantitativa

### La Metafora: Il Giurato in Tribunale e il Controllo delle Prove
- Il **Prompt RAG con vincolo di fedeltà (Grounding)** è identico alle istruzioni che un giudice severo dà al perito d'ufficio in un'aula di tribunale: *"Puoi formulare le tue conclusioni basandoti ESCLUSIVAMENTE sui documenti DOC-1 e DOC-2 allegati agli atti. Se una risposta non è supportata dalle carte, devi dichiarare che l'informazione è assente senza fare congetture o inventare nulla, e per ogni singola frase devi apporre il timbro della fonte [DOC-ID]"*.
- La **Valutazione del Recupero** è come valutare una rete da pesca:
  - **Precision@k**: su 5 pesci catturati nella rete, quanti sono pesci commestibili (pertinenti) e quanti sono vecchi scarponi o sassi (rumore)?
  - **Recall@k**: su 10 pesci commestibili che nuotavano nel lago, quanti ne hai presi nella rete?
  - **MRR (Mean Reciprocal Rank)**: valuta quanto rapidamente l'investigatore trova il *primo* indizio utile: se è al primo posto della lista il punteggio è $1/1 = 1.0$, se è al secondo è $1/2 = 0.5$, se è al decimo è $1/10 = 0.1$.
- La **Valutazione della Generazione (RAGAS)** è la macchina della verità per l'LLM: controlla che la risposta finale non contenga alcuna affermazione priva di riscontro nei documenti (*Faithfulness*).

### Struttura del Prompt Grounded

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

### Metriche di Valutazione Quantitativa

La quantificazione oggettiva delle prestazioni separa la qualità del recupero (*Retrieval*) dall'affidabilità della sintesi generativa (*Generation*).

#### Metriche di Information Retrieval
1. **Recall@k**: la frazione di documenti rilevanti presenti nel corpus che compaiono tra i primi $k$ risultati restituiti.
2. **Precision@k**: la percentuale di documenti pertinenti all'interno del sottoinsieme estratto di $k$ elementi.
3. **Mean Reciprocal Rank (MRR)**: la media dell'inverso della posizione ordinale del primo documento rilevante recuperato lungo un insieme di query $Q$:

$$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$

**Traduzione dei simboli dalla metafora:**
- $|Q|$: il numero totale di domande/query investigative testate.
- $\text{rank}_i$: la posizione in classifica (1°, 2°, 5°...) in cui compare il *primo* documento utile per la query $i$-esima. Se compare al 1° posto, il reciproco è $1/1 = 1$; se compare al 4° posto, vale $1/4 = 0.25$.
- La media finale misura la prontezza del sistema nel posizionare la risposta esatta in cima alla lista.

4. **Normalized Discounted Cumulative Gain (NDCG@k)**: valuta la qualità dell'ordinamento attribuendo un peso logaritmicamente decrescente ai documenti rilevanti posizionati più in basso nella graduatoria.

#### Metriche Generative (Framework RAGAS)
Il framework open-source [RAGAS](https://github.com/explodinggradients/ragas) formalizza tre metriche cardine:
- **Faithfulness (Fedeltà)**: il rapporto tra il numero di affermazioni atomiche della risposta deducibili dal contesto e il totale delle affermazioni generate, rilevando le allucinazioni.
- **Answer Relevance (Pertinenza della Risposta)**: misura la coerenza semantica tra la risposta formulata e il quesito dell'analista, penalizzando divagazioni.
- **Context Precision (Precisione del Contesto)**: quantifica se i passaggi informativi rilevanti sono stati ordinati nelle primissime posizioni della finestra documentale.

> [!INTERACTIVE] WIDGET: Valutatore RAG & Simulatore di Metriche (MRR & Faithfulness)
> Un pannello interattivo in cui l'utente può riordinare con drag-and-drop i documenti restituiti dal retriever (spostando il documento chiave tra il 1°, 2°, 3° o 5° posto) e osservare in tempo reale la variazione del punteggio MRR e NDCG. Un secondo modulo permette di modificare la risposta dell'LLM inserendo frasi non supportate per vedere crollare la barra percentuale della "Faithfulness" con evidenziazione semaforica dei passaggi privi di grounding.

## Trade-off Operativi, Compromessi Ingegneristici e Anti-Pattern

La progettazione di un'infrastruttura RAG per contesti investigativi o aziendali impone una serie di compromessi architetturali in cui ogni incremento di accuratezza si riflette in costi di calcolo, latenza operativa o complessità di gestione:

| Dimensione | Opzione A (Bassa Complessità) | Opzione B (Alta Fedeltà) | Compromesso Ingegneristico |
| :--- | :--- | :--- | :--- |
| **Architettura Indice** | Vettoriale Puro ([FAISS](https://github.com/facebookresearch/faiss), [ChromaDB](https://www.trychroma.com/)) | Ibrido + GraphRAG ([Qdrant](https://qdrant.tech/) + [Neo4j](https://neo4j.com/)) | Latenza di query e manutenzione dello schema contro capacità di correlazione multi-hop |
| **Re-Ranking** | Disabilitato (Top-$k$ diretto) | Cross-Encoder a 2 stadi | 50–200 ms di overhead computazionale per query contro abbattimento dei falsi positivi |
| **Dimensione Chunk** | Finestre piccole (128–256 token) | Finestre ampie (1024–2048 token) | Specificità e precisione di recupero contro ampiezza del contesto e consumo di token |
| **Residenza Indice** | Indice HNSW in RAM | Indice IVF-PQ su disco ([LanceDB](https://lancedb.com/)) | Velocità di risposta in millisecondi contro scalabilità a basso costo per milioni di record |

Tra gli anti-pattern più frequenti nell'implementazione di sistemi RAG spiccano pratiche scorrette ampiamente diffuse:
- **Chunking privo di semantica**: tagli arbitrari a dimensione fissa che spezzano tabelle o codici, rendendo il dato incomprensibile all'encoder vettoriale.
- **Assenza di filtri sui metadati**: recupero indiscriminato su tutto il corpus senza segregazione per livello di confidenzialità o data di validità, consentendo a report obsoleti di inquinare l'analisi corrente.
- **Sovra-ingegnerizzazione tramite GraphRAG su vault curati**: strumenti accademici complessi come HippoRAG o LightRAG sono progettati per estrarre relazioni da *dump* massivi di documenti grezzi e disorganizzati (es. diecimila pagine di atti parlamentari). Applicare l'astrazione e l'estrazione LLM-based dei nodi su un repository di Knowledge Management (come un vault Obsidian locale) in cui l'analista ha *già* curato manualmente i collegamenti ipertestuali esatti, disperde un'enorme quantità di token e calcolo producendo risultati inferiori e allucinati. Per le basi di conoscenza strutturate, la [Ricerca Ibrida tramite Qdrant](https://qdrant.tech/) (Vettori densi + BM25 sparsi) accelerata da Reranker locali (es. `bge-reranker`) si attesta saldamente come l'architettura State Of The Art per rapidità, economia e precisione chirurgica.
- **Mancata sanitizzazione degli input**: iniezione diretta di frammenti non validati all'interno del prompt senza opportune gabbie di isolamento, esponendo il sistema a vulnerabilità di indirect prompt injection (trattate in [D11b](D13b-ai-arma-bersaglio-osint.md) e [D14](D16-responsible-ai-cyber.md)).

## Riferimenti Bibliografici e Risorse Tecniche

### Articoli Scientifici e Documentazione di Riferimento
La letteratura fondamentale per l'approfondimento delle architetture RAG include il paper fondante [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) sviluppato da [Meta AI](https://ai.meta.com/), che ha unificato modelli seq2seq pre-addestrati e recupero denso non parametrico. Per la parte di embedding semantico, la documentazione ufficiale del framework [Sentence-Transformers](https://www.sbert.net/) e le guide di [OpenAI](https://openai.com/) forniscono le specifiche su modelli bi-encoder e cross-encoder. L'ingegneria del calcolo matriciale e delle strutture di quantizzazione vettoriale ad alta efficienza è documentata nella libreria open-source [FAISS](https://github.com/facebookresearch/faiss) di Meta AI.

### Database Vettoriali e Grafi della Conoscenza
Le guide operative dei database vettoriali specializzati [Qdrant](https://qdrant.tech/documentation/), [ChromaDB](https://docs.trychroma.com/), [Weaviate](https://weaviate.io/) e [LanceDB](https://lancedb.com/) illustrano le modalità di configurazione di indici HNSW e filtri sui metadati. Per la modellazione di grafi di proprietà e l'esecuzione di interrogazioni relazionali dichiarative con linguaggio Cypher, il portale documentale di [Neo4j](https://neo4j.com/docs/) e il [Cypher Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/current/) costituiscono i riferimenti pratici standard, affiancati dalla libreria [NetworkX](https://networkx.org/) per algoritmi su reti complesse. La valutazione quantitativa è descritta nella documentazione del framework [RAGAS](https://github.com/explodinggradients/ragas).

### Moduli Correlati del Percorso Didattico
La comprensione integrale del sistema RAG si ricollega ai moduli complementari del curriculum: [D08](D10-deep-learning-pytorch.md) per i tensori di base con PyTorch, [D09](D11-transformers-llm.md) per l'architettura dei Transformer e l'inferenza linguistica, [D11](D13-osint-avanzato.md) per le metodologie investigative OSINT, [D12](D14-agentic-mcp.md) per i sistemi agentici e il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (lo standard aperto creato da [Anthropic](https://www.anthropic.com/) per la connessione sicura tra modelli linguistici e strumenti esterni), e [D15](D17-mlops-llmops.md) per il deployment e l'orchestrazione locale con [Ollama](https://ollama.com/).

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