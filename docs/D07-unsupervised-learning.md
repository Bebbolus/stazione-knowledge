---
aliases:
- D07
- Apprendimento Non Supervisionato
- Clustering
- Riduzione Dimensionale
- PCA
- t-SNE
- UMAP
- Anomaly Detection
resources:
- title: K-Means Clustering Visualizer
  url: https://www.naftaliharris.com/blog/visualizing-k-means-clustering/
  type: lab
---
# Apprendimento Non Supervisionato (Clustering, Riduzione Dimensionale e Anomaly Detection)

L'apprendimento non supervisionato (Unsupervised Learning) è il paradigma del machine learning in cui i modelli estraggono pattern latenti, regolarità geometriche e densità probabilistiche da matrici di dati prive di etichette target o segnali di supervisione esterni. Trova applicazione critica nell'analisi esplorativa di dataset multidimensionali, nella segmentazione comportamentale degli utenti, nella visualizzazione topologica di embedding semantici per l'intelligence OSINT e nell'identificazione di intrusioni informatiche o frodi mediante anomaly detection. Esiste per superare la barriera fondamentale del costo e dell'impossibilità pratica dell'annotazione manuale dei dati, permettendo ai sistemi computazionali di organizzare autonomamente la complessità informativa e di comprimere lo spazio delle feature preservandone la struttura geometrica essenziale.

## Il Paradosso dell'Assenza di Ground Truth

Nei modelli supervisionati, l'ottimizzazione dei parametri è guidata da una funzione di perdita che calcola l'errore esatto rispetto a una verità fondamentale (*ground truth*). Nell'apprendimento non supervisionato, il sistema riceve esclusivamente una matrice di osservazioni $X \in \mathbb{R}^{n \times d}$, dove $n$ indica il numero di campioni e $d$ la dimensionalità dello spazio delle feature. Senza un vettore target $y$, non esiste un segnale d'errore deterministico, trasformando la valutazione in una stima della compattezza geometrica, della separabilità probabilistica o della conservazione della varianza.

Questa assenza di vincoli esterni costringe gli algoritmi non supervisionati a formulare precise ipotesi a priori sulla natura dei dati. La scelta del modello definisce implicitamente cosa costituisce un "gruppo coerente" o una "deviazione anomala": K-Means assume che i cluster siano sfere convesse equi-estese nello spazio euclideo, DBSCAN cerca regioni continue ad alta densità separate da vuoti, mentre la PCA assume che l'informazione di maggior valore coincida con le direzioni di massima varianza lineare. Comprendere queste assunzioni geometriche è il prerequisito indispensabile per evitare di scambiare artefatti algoritmici per autentiche strutture dei dati.

```
========================================================================================
           TASSONOMIA ARCHITETTURALE DELL'UNSUPERVISED LEARNING
========================================================================================
 [Matrice di Dati X (n × d)]
       │
       ├──► 1. CLUSTERING (Partizionamento dello Spazio)
       │      ├─ Centroidi & Voronoi: K-Means (Lloyd, K-Means++)
       │      ├─ Gerarchie Agglomerative: Ward, Complete, Average Linkage, Dendrogrammi
       │      └─ Basati su Densità: DBSCAN (Core/Border/Noise), HDBSCAN
       │
       ├──► 2. RIDUZIONE DIMENSIONALE (Compressione & Manifold Learning)
       │      ├─ Lineare: PCA (Covarianza, Eigendecomposition, SVD, Scree Plot)
       │      └─ Non-Lineare: t-SNE (Student-t, Divergenza KL), UMAP (Fuzzy Simplicial Sets)
       │
       └──► 3. ANOMALY DETECTION (Isolamento & Stima di Densità)
              ├─ Partizionamento Casuale: Isolation Forest (Profondità del Cammino)
              ├─ Iperpiani di Supporto: One-Class SVM (Kernel RBF nel RKHS)
              └─ Densità Relativa Locale: Local Outlier Factor (LOF)
========================================================================================
```

## Algoritmi di Clustering: Partizionamento, Gerarchie e Densità

Il clustering organizza un insieme di punti non etichettati in sottoinsiemi omogenei (*cluster*), massimizzando la similarità intra-cluster e minimizzando la similarità inter-cluster secondo una metrica di distanza formale.

### K-Means e la Partizione dello Spazio di Voronoi

L'algoritmo **K-Means** (implementato nella classe `KMeans` della libreria [Scikit-learn](https://scikit-learn.org/)) modella la struttura dei dati individuando $K$ punti rappresentativi detti **centroidi** $\mu_1, \dots, \mu_K \in \mathbb{R}^d$. Lo spazio multidimensionale viene così partizionato in celle di Voronoi convesse, in cui ogni punto $x_i$ appartiene al cluster del centroide più vicino.

L'algoritmo classico di Stuart Lloyd ottimizza in modo iterativo la somma delle distanze quadratiche intra-cluster, alternando due fasi deterministiche:
Nella fase di assegnazione, ogni campione viene associato al centroide più vicino: $c^{(i)} = \arg\min_{k} ||x_i - \mu_k||^2$. Nella fase di aggiornamento, ciascun centroide viene ricalcolato come la media aritmetica di tutte le osservazioni assegnate a quel gruppo: $\mu_k = \frac{1}{|S_k|} \sum_{x_i \in S_k} x_i$.

La funzione obiettivo globale minimizzata da K-Means è l'**Inerzia** (detta anche *Within-Cluster Sum of Squares*, WCSS):

$$\text{WCSS} = \sum_{k=1}^K \sum_{x_i \in S_k} ||x_i - \mu_k||^2$$

L'algoritmo di Lloyd garantisce la convergenza a un minimo locale, ma è estremamente sensibile all'inizializzazione casuale dei centroidi, rischiando di convergere verso partizioni sub-ottimali. Per neutralizzare questo difetto, lo schema di inizializzazione **K-Means++** (proposto da David Arthur e Sergei Vassilvitskii) seleziona il primo centroide uniformemente a caso e i successivi con una probabilità proporzionale al quadrato della distanza euclidea $D(x)$ dal centroide più vicino già scelto:

$$P(x) = \frac{D(x)^2}{\sum_{x' \in X} D(x')^2}$$

Questo campionamento probabilistico distanzia preventivamente i centroidi iniziali nello spazio vettoriale, garantendo un'approssimazione attesa teoricamente limitata a $\mathcal{O}(\log K)$ rispetto alla soluzione ottimale.

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: K-Means Clustering</p>
  <p>Premi "Prossimo Passo" per vedere l'algoritmo in azione: prima assegna ogni punto al centroide (X) più vicino, poi sposta i centroidi al centro esatto dei punti appena assegnati. Il ciclo si ripete fino a trovare l'equilibrio.</p>
  <iframe src="../widgets/kmeans.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Poiché l'inerzia decresce monotonicamente all'aumentare di $K$, la scelta del numero ottimale di cluster richiede l'analisi del grafico WCSS tramite il **Metodo a Gomito** (*Elbow Method*), individuando il punto di flesso in cui il guadagno marginale collassa. Per una validazione analitica più rigorosa, si impiega il **Silhouette Score** ($s(i)$), che confronta la distanza media intra-cluster $a(i)$ con la distanza media dal cluster più vicino $b(i)$:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]$$

Un coefficiente prossimo a $+1$ indica che il punto è perfettamente integrato nel proprio cluster e distante dai gruppi adiacenti; valori vicini a $0$ denotano sovrapposizione tra cluster, mentre valori negativi indicano errori di assegnazione.

### Clustering Gerarchico: Agglomerazione Bottom-Up e Dendrogrammi

Mentre K-Means impone una partizione piatta e disgiunta dello spazio, molti domini complessi (come le tassonomie documentali nell'intelligence o la filogenesi biologica) presentano strutture nidificate a più livelli. Il **Clustering Gerarchico Agglomerativo** (`AgglomerativeClustering` in [Scikit-learn](https://scikit-learn.org/) e `scipy.cluster.hierarchy` in [SciPy](https://scipy.org/)) costruisce una gerarchia continua partendo dal basso: ogni singolo punto inizia come un cluster indipendente di dimensione unitaria e, a ogni iterazione successiva, i due cluster più vicini vengono fusi insieme fino a formare un unico macro-cluster radice.

La metrica che calcola la prossimità tra due insiemi di punti è definita **criterio di linkage**:
Il **Linkage di Ward** minimizza l'incremento della varianza intra-cluster complessiva derivante dalla fusione dei due gruppi $A$ e $B$, calcolato come:

$$\Delta \text{ESS}_{AB} = \frac{|A||B|}{|A| + |B|} ||\mu_A - \mu_B||^2$$

Il **Complete Linkage** (distanza massima) valuta la distanza tra i punti più lontani dei due cluster: $d_{\text{complete}}(A, B) = \max_{x \in A, y \in B} ||x - y||$, producendo gruppi compatti ma sensibili agli outlier. L'**Average Linkage** calcola la media di tutte le distanze a coppie: $d_{\text{average}}(A, B) = \frac{1}{|A||B|} \sum_{x \in A} \sum_{y \in B} ||x - y||$. Infine, il **Single Linkage** (distanza minima: $d_{\text{single}}(A, B) = \min_{x \in A, y \in B} ||x - y||$) individua strutture filiformi ma è vulnerabile al fenomeno del *chaining*, in cui singoli punti di rumore uniscono indebitamente cluster distinti.

L'intera sequenza di fusioni viene rappresentata graficamente da un **dendrogramma**, un albero binario la cui altezza sull'asse verticale misura la distanza matematica a cui è avvenuta ciascuna unione. Tagliando il dendrogramma a un'altezza specifica si ottiene una partizione con un numero esatto di cluster. La fedeltà con cui il dendrogramma preserva le distanze pairwise originali viene misurata dal **Coefficiente di Correlazione Cofenofenetica** ($c$):

$$c = \frac{\sum_{i < j} (d_{ij} - \bar{d})(t_{ij} - \bar{t})}{\sqrt{\sum_{i < j} (d_{ij} - \bar{d})^2 \sum_{i < j} (t_{ij} - \bar{t})^2}}$$

dove $d_{ij}$ è la distanza euclidea originale tra i campioni $i$ e $j$, mentre $t_{ij}$ è la distanza cofenofenetica (l'altezza del nodo in cui $i$ e $j$ si fondono per la prima volta). Valori di $c > 0.8$ indicano una fedele rappresentazione gerarchica della geometria originale.

### Clustering Basato su Densità: DBSCAN e HDBSCAN

Sia K-Means che il clustering gerarchico basato su distanze euclidee falliscono quando i cluster presentano geometrie concave, anelli concentrici o densità eterogenee immerse in rumore di fondo. L'algoritmo **DBSCAN** (*Density-Based Spatial Clustering of Applications with Noise*, implementato da [Scikit-learn](https://scikit-learn.org/)) supera questa barriera modellando i cluster come componenti connesse di regioni ad alta densità spaziale.

DBSCAN richiede due iperparametri fondamentali: il raggio di scansione locale $\epsilon$ (*epsilon*) e il numero minimo di punti $min\_samples$. L'algoritmo classifica ogni punto $p \in X$ analizzando il suo intorno sferico $N_\epsilon(p) = \{q \in X \mid ||p - q|| \le \epsilon\}$:
Se $|N_\epsilon(p)| \ge min\_samples$, il punto viene classificato come **Core Point** (nodo denso generatore di cluster). Se $|N_\epsilon(p)| < min\_samples$, ma $p$ appartiene all'intorno di un Core Point, viene etichettato come **Border Point** (punto di confine). Se un punto non è né Core né Border, viene classificato come **Noise Point** (rumore statistico o anomalia, contrassegnato dall'etichetta $-1$).

Un cluster si forma aggregando tutti i punti mutualmente **density-connected**: una catena continua di Core Point distanti meno di $\epsilon$ l'uno dall'altro. La taratura ottimale di $\epsilon$ si effettua analizzando il grafico delle distanze del $k$-esimo vicino (*k-distance graph*, con $k = min\_samples$): ordinando le distanze in ordine crescente, il valore ideale di $\epsilon$ corrisponde al punto di massima curvatura (*knee*).

Il limite principale di DBSCAN consiste nell'incapacità di gestire dataset con densità variabili tra gruppi diversi (un $\epsilon$ globale frammenta i cluster rarefatti o fonde quelli densi). L'algoritmo **HDBSCAN** (*Hierarchical DBSCAN*, ideato da Ricardo Campello, Davoud Moulavi e Jörg Sander) supera questo collo di bottiglia convertendo DBSCAN in una gerarchia su tutti i possibili valori di $\epsilon$. HDBSCAN trasforma lo spazio tramite la **Distanza di Raggiungibilità Mutua** ($d_{\text{mreach-}k}$):

$$d_{\text{mreach-}k}(a, b) = \max(\{ \text{core}_k(a), \text{core}_k(b), d(a, b) \})$$

dove $\text{core}_k(a)$ è la distanza di $a$ dal suo $k$-esimo vicino. Costruendo un albero di espansione minima (*Minimum Spanning Tree*) su questa metrica ed estraendo i cluster stabili tramite la metrica di persistenza della massa ($\lambda = 1/\epsilon$), HDBSCAN isola automaticamente cluster a densità variabile senza richiedere la specificazione manuale di $\epsilon$.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D07-unsupervised-learning. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Riduzione della Dimensionalità e Manifold Learning

Quando la dimensionalità dei dati $d$ cresce verso decine o migliaia di colonne (come accade negli embedding generati dai Large Language Model o nelle serie temporali OSINT), i dati incorrono nella **Maledizione della Dimensionalità** (*Curse of Dimensionality*). All'aumentare delle dimensioni, il volume dello spazio cresce esponenzialmente rispetto al numero di campioni, rendendo lo spazio estremamente vuoto e causando la convergenza di tutte le distanze euclidee a valori simili ($\lim_{d \to \infty} \frac{\max ||x_i - x_j|| - \min ||x_i - x_j||}{\min ||x_i - x_j||} \to 0$).

La riduzione della dimensionalità trasforma la matrice originale $X \in \mathbb{R}^{n \times d}$ in una matrice a bassa dimensione $Z \in \mathbb{R}^{n \times k}$ (con $k \ll d$), eliminando le correlazioni spurie, accelerando l'addestramento dei modelli a valle e consentendo la visualizzazione bidimensionale o tridimensionale.

### La Maledizione della Dimensionalità e la Proiezione Lineare (PCA)

L'analisi delle componenti principali (**PCA**, *Principal Component Analysis*, disponibile in `sklearn.decomposition.PCA`) è la tecnica fondamentale di riduzione dimensionale lineare. L'algoritmo cerca una sequenza di assi ortogonali ordinati, detti **Componenti Principali**, che massimizzano progressivamente la varianza dei dati proiettati.

La formulazione algebrica opera sulla matrice centrata $\tilde{X} = X - \mu_X \in \mathbb{R}^{n \times d}$ (in cui ogni feature ha media campionaria nulla). La matrice di covarianza empirica dei dati è:

$$\Sigma = \frac{1}{n-1} \tilde{X}^T \tilde{X} \in \mathbb{R}^{d \times d}$$

I componenti principali corrispondono agli autovettori $v_1, \dots, v_d$ ottenuti dalla decomposizione spettrale di $\Sigma$:

$$\Sigma v_k = \lambda_k v_k$$

dove l'autovalore $\lambda_k \ge 0$ quantifica esattamente la quantità di varianza spiegata lungo la direzione dell'autovettore $v_k$. Nelle implementazioni moderne ad alte prestazioni, il calcolo evita la matrice di covarianza esplicita e sfrutta la decomposizione ai valori singolari (**SVD**, *Singular Value Decomposition*) della matrice dei dati: $\tilde{X} = U S V^T$, in cui le colonne di $V$ sono i componenti principali e i valori singolari $s_k$ sono legati agli autovalori dalla relazione $\lambda_k = \frac{s_k^2}{n-1}$.

La frazione di informazione preservata da ciascuna componente è formalizzata dall'**Explained Variance Ratio** ($\text{EVR}_k$):

$$\text{EVR}_k = \frac{\lambda_k}{\sum_{j=1}^d \lambda_j}$$

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: PCA e Varianza Catturata</p>
  <p>Uso della PCA intuitivo: muovi lo slider per ruotare l'asse di proiezione. L'obiettivo della PCA è trovare l'angolo che <strong>massimizza la varianza catturata</strong> (cioè i punti rossi proiettati sono più sparpagliati possibile lungo la linea). Premi il bottone per vedere l'algoritmo agganciare matematicamente l'autovettore principale!</p>
  <iframe src="../widgets/pca.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Tracciando la varianza spiegata cumulativa in funzione del numero di componenti mediante uno **Scree Plot**, è possibile stabilire la dimensionalità intrinseca minima $k$ necessaria a conservare una quota prefissata di varianza totale (tipicamente il 90% o il 95%).

### Manifold Learning Non Lineare: t-SNE e UMAP

La PCA opera proiezioni rigorosamente lineari (rotazioni e traslazioni di iperpiani). Se le osservazioni giacciono su varietà topologiche non lineari (*manifold*, come la superficie arrotolata di uno *Swiss Roll* o raggruppamenti semantici complessi di embedding testuali), una proiezione lineare sovrappone regioni tra loro distanti, distruggendo le relazioni di prossimità locale.

L'algoritmo **t-SNE** (*t-Distributed Stochastic Neighbor Embedding*, introdotto da [Laurens van der Maaten](https://lvdmaaten.github.io/) e [Geoffrey Hinton](https://www.cs.toronto.edu/~hinton/) nel 2008) risolve questo problema convertendo le distanze euclidee in probabilità condizionali di vicinato. Nello spazio ad alta dimensione, la probabilità che il punto $x_i$ scelga $x_j$ come proprio vicino segue una distribuzione Gaussiana centrata su $x_i$:

$$p_{j|i} = \frac{\exp\left(-\frac{||x_i - x_j||^2}{2\sigma_i^2}\right)}{\sum_{k \neq i} \exp\left(-\frac{||x_i - x_k||^2}{2\sigma_i^2}\right)}, \quad p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$

La varianza $\sigma_i^2$ viene determinata per ogni punto mediante una ricerca binaria che soddisfa un valore di **Perplexity** fissato dall'utente, interpretabile come il numero effettivo di vicini considerati. Nello spazio a bassa dimensione di destinazione ($y_i \in \mathbb{R}^2$), le probabilità congiunte $q_{ij}$ vengono modellate utilizzando una distribuzione **t di Student con 1 grado di libertà** (distribuzione di Cauchy):

$$q_{ij} = \frac{(1 + ||y_i - y_j||^2)^{-1}}{\sum_{k} \sum_{l \neq k} (1 + ||y_k - y_l||^2)^{-1}}$$

Le posizioni ottimali $y_i$ vengono trovate minimizzando la **Divergenza di Kullback-Leibler** ($KL$) tra le due distribuzioni di probabilità tramite discesa del gradiente:

$$KL(P \parallel Q) = \sum_{i \neq j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$$

L'impiego della distribuzione t di Student risolve il celebre **Crowding Problem**: poiché il volume disponibile in 2D è infinitamente inferiore rispetto a quello in alta dimensione, le code pesanti della distribuzione Cauchy consentono ai punti moderatamente distanti nello spazio originale di essere spinti a distanze considerevoli nello spazio di proiezione, prevenendo il collasso dei cluster al centro della mappa.

L'algoritmo **UMAP** (*Uniform Manifold Approximation and Projection*, ideato dal matematico [Leland McInnes](https://github.com/lmcinnes) nel 2018) estende il manifold learning fondandolo sulla geometria Riemanniana e la topologia algebrica. Assumendo che i dati siano uniformemente distribuiti su una varietà Riemanniana locale, UMAP modella la topologia dei vicinati mediante complessi simpliciali sfumati (*fuzzy simplicial sets*).

La funzione di costo minimizzata da UMAP è la **Cross-Entropia per Insiemi Fuzzy** tra la matrice delle relazioni ad alta dimensione $\mu_{ij}$ e quella proiettata $\nu_{ij}$:

$$L_{\text{UMAP}} = \sum_{i \neq j} \left( \mu_{ij} \log \frac{\mu_{ij}}{\nu_{ij}} + (1 - \mu_{ij}) \log \frac{1 - \mu_{ij}}{1 - \nu_{ij}} \right)$$

A differenza di t-SNE (che focalizza il gradiente quasi esclusivamente sulla conservazione dei vicinati microscopici), UMAP preserva contemporaneamente sia la micro-struttura locale sia le distanze globali tra macro-cluster, garantendo al contempo un'efficienza computazionale superiore ($\mathcal{O}(n^{1.14})$ contro $\mathcal{O}(n^2)$ di t-SNE) grazie all'ottimizzazione stocastica del gradiente (SGD) e agli algoritmi di Nearest Neighbor Descent.

## Anomaly Detection e Rilevamento di Outlier

L'Anomaly Detection (o Outlier Detection) si occupa di identificare osservazioni anomale la cui firma statistica o geometrica devia in modo marcato dalla distribuzione di normalità sottostante. In contesti operativi come il monitoraggio di infrastrutture server, l'analisi forense OSINT o la prevenzione di intrusioni informatiche, gli eventi anomali costituiscono meno dell'1% del volume totale, rendendo impraticabile la classificazione supervisionata a causa della grave scarsità di esempi patologici noti.

### Isolamento Spaziale e Lunghezza del Cammino (Isolation Forest)

L'algoritmo **Isolation Forest** (sviluppato da [Fei Tony Liu](https://scholar.google.com/), Kai Ming Ting e Zhi-Hua Zhou nel 2008, disponibile come `IsolationForest` in [Scikit-learn](https://scikit-learn.org/)) ribalta l'approccio classico: invece di modellare faticosamente il profilo dei punti normali per poi cercare ciò che devia, isola direttamente le anomalie sfruttando la loro intrinseca rarità topologica.

L'algoritmo costruisce una foresta di alberi binari di isolamento (*iTree*). In ogni nodo dell'albero, una feature $q$ viene selezionata a caso e tagliata con una soglia casuale $p$ compresa tra il valore minimo e massimo della variabile. Poiché i punti normali risiedono in regioni dense, richiedono decine di partizionamenti casuali prima di essere isolati in una foglia singola. Al contrario, i punti anomali risiedono in regioni remote e rarefatte dello spazio, venendo isolati nei primissimi livelli dell'albero.

La lunghezza del cammino $h(x)$ misura il numero di archi attraversati dalla radice alla foglia terminale per isolare l'osservazione $x$. L'**Anomaly Score** normalizzato $s(x, n)$ è formulato come:

$$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$

dove $E(h(x))$ è la lunghezza media del cammino su tutti gli alberi della foresta e $c(n)$ rappresenta la profondità media attesa di una ricerca infruttuosa in un albero binario di ricerca con $n$ nodi:

$$c(n) = 2 \left( \ln(n - 1) + 0.5772156649 \right) - \frac{2(n - 1)}{n}$$

Se $s(x, n) \to 1$, la lunghezza del cammino è estremamente breve, indicando con certezza un'anomalia. Se $s(x, n) < 0.5$, l'osservazione esibisce un cammino lungo, appartenendo alla distribuzione di normalità standard. Isolation Forest offre una complessità computazionale quasi-lineare $\mathcal{O}(n \log n)$ a bassissimo consumo di memoria, rendendolo l'algoritmo di riferimento per stream di dati ad altissima velocità.

### Iperpiani di Supporto Non Lineari (One-Class SVM)

L'algoritmo **One-Class SVM** (proposto da Bernhard Schölkopf et al. nel 2001, implementato in `sklearn.svm.OneClassSVM`) adatta i principi delle Support Vector Machine all'apprendimento non supervisionato. L'algoritmo proietta i dati di addestramento in uno spazio di Hilbert a kernel riproducente (*RKHS*) ad altissima dimensione tramite una funzione kernel non lineare (tipicamente Radial Basis Function, RBF: $K(x, y) = \exp(-\gamma ||x - y||^2)$).

Nello spazio trasformato, One-Class SVM calcola l'iperpiano ottimo che separa la quasi totalità delle osservazioni dall'origine delle coordinate con il massimo margine possibile. Il compromesso tra la frazione di punti tollerati all'esterno del confine e la complessità geometrica della frontiera è regolato dall'iperparametro $\nu \in (0, 1]$, che funge simultaneamente da limite superiore alla frazione di outlier di addestramento e da limite inferiore alla frazione di vettori di supporto generati.

### Deviazione della Densità Locale (Local Outlier Factor - LOF)

Quando un dataset presenta cluster multipli con densità locali marcatamente eterogenee, una soglia di distanza globale o una frontiera uniforme falliscono: un punto situato a distanza moderata da un cluster ad altissima densità è un'autentica anomalia locale, mentre la medesima distanza euclidea all'interno di un cluster rarefatto è perfettamente fisiologica.

L'algoritmo **Local Outlier Factor** (**LOF**, formulato da Markus Breunig et al. nel 2000, implementato in `sklearn.neighbors.LocalOutlierFactor`) risolve questo dilemma confrontando la densità locale di un punto con la densità locale del suo vicinato di $k$ elementi. L'algoritmo definisce prima la **Distanza di Raggiungibilità** (*reachability distance*) del punto $p$ rispetto al vicino $o$:

$$\text{reach-dist}_k(p, o) = \max(\{ k\text{-distance}(o), d(p, o) \})$$

La **Local Reachability Density** ($\text{lrd}_k(p)$) è l'inverso della distanza media di raggiungibilità di $p$ rispetto ai suoi $k$ vicini più prossimi:

$$\text{lrd}_k(p) = \left[ \frac{\sum_{o \in N_k(p)} \text{reach-dist}_k(p, o)}{|N_k(p)|} \right]^{-1}$$

Il punteggio finale **LOF** è il rapporto medio tra la densità dei vicini e la densità del punto $p$:

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

Un valore di $\text{LOF} \approx 1$ indica che il punto possiede una densità analoga a quella dei suoi vicini (inlier omogeneo). Un valore di $\text{LOF} \gg 1$ segnala che la densità locale del punto è nettamente inferiore a quella dei suoi vicini, rivelando un'anomalia locale isolata.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Trade-off Operativi e Scelte Architetturali

La selezione dell'algoritmo non supervisionato richiede un bilanciamento rigoroso tra scalabilità computazionale, sensibilità a geometrie non lineari e interpretabilità:

Nel dominio del clustering, K-Means offre la massima velocità ($\mathcal{O}(n K d)$ per iterazione) ed è ideale per segmentazioni grossolane o compressione tramite quantizzazione vettoriale, ma presuppone cluster convessi e richiede la conoscenza a priori di $K$. DBSCAN e HDBSCAN superano ogni vincolo di forma e isolano automaticamente il rumore, ma presentano costi computazionali superiori ($\mathcal{O}(n \log n)$ con indicizzazione spaziale k-d tree, $\mathcal{O}(n^2)$ nel caso peggiore) e necessitano di calibrazione delle distanze in alta dimensione.

Nella riduzione dimensionale, la PCA è deterministica, computazionalmente istantanea e matematicamente invertibile ($X_{\text{approx}} = Z V^T$), rendendosi indispensabile per il pre-processing e la rimozione della collinearità nei modelli supervisionati. Al contrario, t-SNE e UMAP sono trasformazioni non lineari e stocastiche prive di matrice di proiezione inversa esplicita: il loro scopo primario è l'esplorazione qualitativa e la visualizzazione semantica delle varietà topologiche, non la costruzione di feature stabili per pipeline predittive di produzione.

Nell'anomaly detection, Isolation Forest è la scelta d'elezione per dataset industriali massivi e spazi ad alta dimensione grazie alla sua scalabilità $\mathcal{O}(n \log n)$ e all'immunità allo scaling delle feature. LOF è superiore quando i dati contengono sottopopolazioni a densità eterogenea, mentre One-Class SVM garantisce frontiere di supporto non lineari eccellenti in presenza di dataset compatti e ben normalizzati.

## Riferimenti Bibliografici e Risorse Tecniche

Per approfondire i fondamenti matematici e le implementazioni degli algoritmi non supervisionati, la letteratura accademica e i portali didattici offrono riferimenti essenziali.

### Testi Accademici e Dispense Teoriche
Il manuale teorico fondamentale per la formalizzazione matematica del clustering, della PCA e dei modelli di mistura è [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) (redatto dai docenti della [Stanford University](https://www.stanford.edu/) [Trevor Hastie](https://hastie.su.domains/), [Robert Tibshirani](https://tibshirani.su.domains/) e [Jerome Friedman](https://hastie.su.domains/)). Per un percorso didattico rigoroso sulle dimostrazioni analitiche degli algoritmi di clustering e scomposizione matriciale, si consultino le lecture notes del celebre corso [CS229: Machine Learning](https://cs229.stanford.edu/) della [Stanford University](https://www.stanford.edu/).

### Paper Scientifici Fondamentali
L'algoritmo t-SNE è formalizzato nello studio fondamentale di [Laurens van der Maaten](https://lvdmaaten.github.io/) e [Geoffrey Hinton](https://www.cs.toronto.edu/~hinton/) intitolato *Visualizing Data using t-SNE* (Journal of Machine Learning Research, 2008). I fondamenti topologici di UMAP sono esposti nel paper di [Leland McInnes](https://github.com/lmcinnes), John Healy e James Melville intitolato *UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction* (arXiv, 2018). L'algoritmo Isolation Forest è descritto nel paper di [Fei Tony Liu](https://scholar.google.com/), Kai Ming Ting e Zhi-Hua Zhou, *Isolation Forest* (IEEE ICDM, 2008).

### Documentazione Software e Strumenti Interattivi
Le guide operative di riferimento per gli strumenti di calcolo in [Python](https://www.python.org/) sono la [Guida al Clustering di Scikit-Learn](https://scikit-learn.org/stable/modules/clustering.html), la documentazione del modulo gerarchico di [SciPy](https://scipy.org/) e il portale open-source della libreria [UMAP](https://github.com/lmcinnes/umap). Per l'esplorazione visiva interattiva, la testata [Distill.pub](https://distill.pub/) offre la guida di riferimento [How to Use t-SNE Effectively](https://distill.pub/2016/misread-tsne/), mentre il progetto [Explained Visually](https://setosa.io/ev/) offre una simulazione geometrica sull'estrazione della varianza in [Principal Component Analysis](https://setosa.io/ev/principal-component-analysis/).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



I laboratori seguenti forniscono script Python completi, eseguibili e autocontenuti per testare il clustering, la riduzione dimensionale lineare e non lineare, e le architetture di anomaly detection.

### Laboratorio 1: Clustering K-Means, Curva a Gomito e Silhouette Analysis

Questo script genera dati sintetici multivariati, esegue una scansione sistematica su diversi valori di $K$, calcola l'inerzia WCSS e il coefficiente di Silhouette per identificare la partizione ottimale dello spazio vettoriale.

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# 1. Generazione di un dataset multivariato a 5 cluster
X_raw, y_true = make_blobs(
    n_samples=1500,
    n_features=6,
    centers=5,
    cluster_std=1.2,
    random_state=42
)

# 2. Standardizzazione delle feature (fondamentale per K-Means)
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

# 3. Scansione sistematica per la Curva a Gomito e Silhouette Score
k_values = range(2, 10)
inertia_scores = []
silhouette_scores = []

print("Valutazione quantitativa delle partizioni K-Means:")
for k in k_values:
    kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = kmeans.fit_predict(X)
    
    inertia = kmeans.inertia_
    sil_score = silhouette_score(X, labels)
    
    inertia_scores.append(inertia)
    silhouette_scores.append(sil_score)
    print(f"  K={k} | WCSS (Inerzia): {inertia:8.2f} | Silhouette Score: {sil_score:.4f}")

# 4. Individuazione automatica del K ottimale tramite massimo Silhouette
best_k = k_values[int(np.argmax(silhouette_scores))]
print(f"\nNumero ottimale di cluster identificato (max Silhouette): K = {best_k}")

# 5. Addestramento del modello finale ottimizzato
optimal_kmeans = KMeans(n_clusters=best_k, init="k-means++", n_init=10, random_state=42)
optimal_labels = optimal_kmeans.fit_predict(X)
print(f"Dimensioni dei cluster assegnati: {np.bincount(optimal_labels)}")
```

### Laboratorio 2: Clustering Gerarchico Agglomerativo e Calcolo Cofenofenetico

Questo script esegue il clustering gerarchico agglomerativo con criteri di linkage multipli (Ward, Complete, Average), calcola il coefficiente di correlazione cofenofenetica per misurare la distorsione metrica e costruisce la matrice di linkage con [SciPy](https://scipy.org/).

```python
import numpy as np
from sklearn.datasets import make_blobs
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, cophenet

# 1. Generazione di dati raggruppati
X, _ = make_blobs(n_samples=300, n_features=4, centers=4, cluster_std=0.9, random_state=42)

# 2. Calcolo della matrice delle distanze pairwise euclidee
pairwise_dist = pdist(X, metric="euclidean")

# 3. Valutazione comparativa dei criteri di linkage
linkage_methods = ["ward", "complete", "average", "single"]

print("Analisi della Fedelta' Gerarchica (Correlazione Cofenofenetica):")
for method in linkage_methods:
    Z = linkage(X, method=method, metric="euclidean")
    c_coeff, _ = cophenet(Z, pairwise_dist)
    print(f"  Metodo Linkage: {method:<10} | Indice Cofenofenetico: {c_coeff:.4f}")

# 4. Estrazione della struttura ad albero con metodo Ward
Z_ward = linkage(X, method="ward")
print(f"\nMatrice di Linkage Ward calcolata con successo: {Z_ward.shape[0]} iterazioni di fusione.")
print(f"Ultime 3 fusioni al vertice dell'albero (distanze di unione):")
for i, step in enumerate(Z_ward[-3:], start=1):
    cluster_a, cluster_b, dist, n_elem = int(step[0]), int(step[1]), step[2], int(step[3])
    print(f"  Fusione {i}: Cluster {cluster_a} + Cluster {cluster_b} a distanza {dist:.2f} ({n_elem} campioni)")
```

### Laboratorio 3: Riduzione Dimensionale Comparata (PCA, t-SNE e UMAP)

Questo script confronta la decomposizione lineare PCA rispetto agli algoritmi di manifold learning t-SNE e UMAP su un dataset ad alta dimensione, calcolando l'Explained Variance Ratio e proiettando le varietà topologiche in 2D.

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# 1. Caricamento del dataset ad alta dimensione (8x8 immagini = 64 feature)
digits = load_digits()
X_raw = digits.data
y = digits.target

scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

# 2. Decomposizione lineare tramite PCA
pca = PCA(n_components=10, random_state=42)
X_pca = pca.fit_transform(X)

evr = pca.explained_variance_ratio_
cum_evr = np.cumsum(evr)
print("Analisi PCA (Explained Variance Ratio per le prime 10 componenti):")
for i, (ratio, cum) in enumerate(zip(evr, cum_evr), start=1):
    print(f"  PC{i:02d}: Varianza spiegata = {ratio * 100:5.2f}% | Cumulativa = {cum * 100:5.2f}%")

# 3. Manifold Learning Non Lineare tramite t-SNE
tsne = TSNE(n_components=2, perplexity=30.0, max_iter=1000, random_state=42)
X_tsne = tsne.fit_transform(X)
print(f"\nt-SNE completato: Divergenza KL finale = {tsne.kl_divergence_:.4f}")

# 4. Verifica di UMAP (se installato nell'ambiente)
try:
    import umap
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
    X_umap = reducer.fit_transform(X)
    print("UMAP completato con successo: coordinate proiettate shape =", X_umap.shape)
except ImportError:
    print("Nota: Libreria 'umap-learn' non installata nell'ambiente corrente. Salto calcolo UMAP.")

print(f"\nProiezioni completate con successo su {X.shape[0]} osservazioni.")
```

### Laboratorio 4: Pipeline Multi-Algoritmica di Anomaly Detection

Questo script implementa un benchmark di rilevamento delle anomalie confrontando Isolation Forest, Local Outlier Factor (LOF) e One-Class SVM su un dataset contaminato da campioni patologici artificiali.

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report

# 1. Generazione di dati normali (95%) e iniezione di outlier (5%)
n_inliers = 950
n_outliers = 50
contamination_rate = n_outliers / (n_inliers + n_outliers)

X_inliers, _ = make_blobs(n_samples=n_inliers, n_features=5, centers=2, cluster_std=1.0, random_state=42)
rng = np.random.RandomState(42)
X_outliers = rng.uniform(low=-8, high=8, size=(n_outliers, 5))

X = np.vstack([X_inliers, X_outliers])
# Target reale: 1 per inlier, -1 per outlier
y_true = np.ones(n_inliers + n_outliers, dtype=int)
y_true[n_inliers:] = -1

# 2. Modello 1: Isolation Forest
iso_forest = IsolationForest(contamination=contamination_rate, random_state=42)
y_pred_if = iso_forest.fit_predict(X)

# 3. Modello 2: Local Outlier Factor (LOF)
lof = LocalOutlierFactor(n_neighbors=20, contamination=contamination_rate)
y_pred_lof = lof.fit_predict(X)

# 4. Modello 3: One-Class SVM con kernel RBF
oc_svm = OneClassSVM(nu=contamination_rate, kernel="rbf", gamma=0.1)
y_pred_svm = oc_svm.fit_predict(X)

# 5. Valutazione e confronto delle metriche di precisione sugli outlier (-1)
models = {
    "Isolation Forest": y_pred_if,
    "Local Outlier Factor": y_pred_lof,
    "One-Class SVM": y_pred_svm
}

print("Confronto Prestazioni nel Rilevamento delle Anomalie (Classe Outlier = -1):")
for name, preds in models.items():
    tp = np.sum((y_true == -1) & (preds == -1))
    fp = np.sum((y_true == 1) & (preds == -1))
    fn = np.sum((y_true == -1) & (preds == 1))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    print(f"  {name:<22} | Precision: {precision:.4f} | Recall: {recall:.4f} | F1-Score: {f1:.4f}")
```
