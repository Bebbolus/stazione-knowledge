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

Immagina di entrare in una stanza piena di migliaia di mattoncini Lego sparsi alla rinfusa sul pavimento, senza la scatola originale, senza il libretto di istruzioni e senza nessuno che ti dica cosa devi costruire. 
Nel **Machine Learning Supervisionato**, hai un maestro al tuo fianco che ti dice subito: *"Questo pezzo è una finestra, quello è un tetto"*. Nell'**Apprendimento Non Supervisionato (Unsupervised Learning)**, sei completamente da solo: devi osservare la forma, i colori e le dimensioni dei mattoncini e trovare un senso da te, raggruppando quelli simili o scartando i pezzi rotti.

Matematicamente, il sistema riceve una matrice di osservazioni senza etichette predefinite:

$$X \in \mathbb{R}^{n \times d}$$

Spiegata a parole:
- $n$: è il numero totale di mattoncini Lego sparsi sul pavimento (i campioni o osservazioni).
- $d$: è il numero di caratteristiche misurate per ogni mattoncino (es. lunghezza, larghezza, peso, colore).
- L'assenza di un vettore target $y$ (il libretto delle risposte) significa che non esiste un errore esatto da correggere: il modello deve scommettere su un'ipotesi geometrica (es. raggruppare per vicinanza, per densità di folla o per allineamento visivo).

> [!INTERACTIVE] WIDGET: Lo Smistatore di Mattoncini Lego (Ground Truth vs Unsupervised)
> *Visualizzazione Dinamica:* Un'arena interattiva dove l'utente può attivare la modalità "Con Maestro" (Supervisionato: i punti si colorano subito con la loro etichetta $y$) o "Senza Maestro" (Non Supervisionato: i punti sono grigi e l'utente sperimenta come raggrupparli variando criteri di forma e colore, osservando l'assenza di un punteggio d'errore assoluto).

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

Immagina di essere il manager di una catena di pizzerie da asporto e di dover aprire $K$ nuovi locali in una grande città per consegnare le pizze il più in fretta possibile a tutte le case.
All'inizio pianti $K$ bandierine a caso sulla mappa della città. L'algoritmo **K-Means** procede con due mosse a ripetizione come una danza:
1. **Assegnazione (I clienti scelgono la pizzeria):** Ogni famiglia della città ordina dalla pizzeria più vicina a casa sua, tracciando i confini dei quartieri di consegna (le celle di Voronoi).
2. **Aggiornamento (I locali si spostano al centro):** Ciascun pizzaiolo guarda la mappa di tutte le famiglie che hanno ordinato da lui e sposta fisicamente il suo locale esattamente al baricentro (il centro geometrico) dei suoi clienti per far fare meno strada ai fattorini.
I clienti si riassegnano alle nuove posizioni, i locali si rispostano, e il ciclo si ripete finché le pizzerie trovano la posizione perfetta e smettono di muoversi.

Le formule matematiche formalizzano queste due fasi:

1. **Fase di Assegnazione:**
   $$c^{(i)} = \arg\min_{k} ||x_i - \mu_k||^2$$
   - $x_i$: la posizione della casa dell'utente $i$.
   - $\mu_k$: la posizione della pizzeria (centroide) $k$.
   - $c^{(i)}$: l'etichetta della pizzeria più vicina assegnata al cliente $i$.

2. **Fase di Aggiornamento (Media del quartiere):**
   $$\mu_k = \frac{1}{|S_k|} \sum_{x_i \in S_k} x_i$$
   - $|S_k|$: il numero totale di clienti nel quartiere della pizzeria $k$.
   - $\sum x_i$: la somma delle posizioni di tutti i clienti del gruppo, divisa per il loro numero (la media aritmetica delle coordinate).

3. **La fatica totale di consegna (Inerzia o WCSS):**
   $$\text{WCSS} = \sum_{k=1}^K \sum_{x_i \in S_k} ||x_i - \mu_k||^2$$
   - $\text{WCSS}$ (*Within-Cluster Sum of Squares*): la somma della "strada al quadrato" percorsa da tutti i fattorini per servire tutti i rispettivi clienti. L'obiettivo dell'algoritmo è minimizzare questa fatica complessiva.

4. **Inizializzazione furba (K-Means++):**
   Per evitare che le $K$ pizzerie partano tutte nello stesso isolato per pura sfortuna iniziale, **K-Means++** piazza la prima pizzeria a caso e le successive con una probabilità proporzionale al quadrato della distanza $D(x)$ dalla pizzeria più vicina già esistente:
   $$P(x) = \frac{D(x)^2}{\sum_{x' \in X} D(x')^2}$$
   In questo modo, le nuove pizzerie vengono "sparate" fin dall'inizio nei quartieri più sguarniti e lontani.

> [!INTERACTIVE] WIDGET: La Battaglia delle Pizzerie (K-Means & Voronoi Simulator)
> *Visualizzazione Dinamica:* Una mappa 2D dove l'utente posiziona $K$ pizzerie cliccando sullo schermo. Premendo "Step", i confini colorati dei quartieri (Voronoi) si ridisegnano in tempo reale e i centroidi scivolano dolcemente verso il baricentro dei punti. Include un cursore per testare l'avvio casuale vs K-Means++ e vedere come cambia l'inerzia finale WCSS.

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: K-Means Clustering</p>
  <p>Premi "Prossimo Passo" per vedere l'algoritmo in azione: prima assegna ogni punto al centroide (X) più vicino, poi sposta i centroidi al centro esatto dei punti appena assegnati. Il ciclo si ripete fino a trovare l'equilibrio.</p>
  <iframe src="../widgets/kmeans.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

#### Quante pizzerie aprire? Il Metodo a Gomito e il Silhouette Score

Più pizzerie apri, meno strada fanno i fattorini; ma aprire 100 pizzerie per 100 clienti non ha senso (la fatica WCSS sarebbe zero, ma il costo assurdo).
- **Metodo a Gomito (Elbow Method):** Tracciando la fatica WCSS al variare di $K$, si cerca il punto in cui la curva "fa un gomito": aggiungere un'altra pizzeria dopo quel punto riduce la fatica in modo trascurabile.
- **Silhouette Score ($s(i)$):** Misura quanto è soddisfatto il singolo cliente della sua pizzeria:
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]$$
  - $a(i)$: distanza media del cliente $i$ dai vicini del suo stesso quartiere (quanto si trova bene nel suo gruppo).
  - $b(i)$: distanza media del cliente $i$ dai clienti della pizzeria rivale più vicina (quanto è distante dal gruppo concorrente).
  - Se $s(i) \approx +1$: il cliente è felicissimo, vicinissimo alla sua pizzeria e lontano dai rivali.
  - Se $s(i) \approx 0$: il cliente è sul confine esatto tra due quartieri.
  - Se $s(i) < 0$: il cliente è stato assegnato alla pizzeria sbagliata ed è più vicino a quella rivale!

### Clustering Gerarchico: Agglomerazione Bottom-Up e Dendrogrammi

Pensa a come si formano i gruppi di amici durante il primo mese di scuola superiore.
Il primo giorno, ogni singolo studente è un'isola a sé (un gruppo da una sola persona). Dopo pochi giorni, i due compagni di banco più affini si uniscono in una coppietta inseparabile. Poi, due coppiette che amano gli stessi videogiochi o sport si fondono in una comitiva da 4. Man mano che passano le settimane, le comitive continuano a fondersi tra loro fino a formare un unico grande pullman di classe. Questo approccio "dal basso verso l'alto" è il **Clustering Gerarchico Agglomerativo**.

Come decidono due gruppi $A$ e $B$ se vale la pena fondersi? Ci sono diverse regole matematiche (**Criteri di Linkage**):
1. **Ward Linkage (Minima confusione):**
   $$\Delta \text{ESS}_{AB} = \frac{|A||B|}{|A| + |B|} ||\mu_A - \mu_B||^2$$
   - $|A|$ e $|B|$: il numero di studenti nei due gruppi.
   - $||\mu_A - \mu_B||^2$: la distanza tra i "centri di interesse" (baricentri) dei due gruppi.
   - Traduzione: unisce i due gruppi che fanno aumentare il meno possibile il disordine (varianza) complessivo.
2. **Complete Linkage (Regola dei più distanti):** $d(A, B) = \max_{x \in A, y \in B} ||x - y||$. Due gruppi si fondono solo se anche i due membri più antipatici o distanti tra loro sono comunque vicini. Crea gruppi compatti ma è sensibile a persone isolate.
3. **Single Linkage (Regola del singolo contatto):** $d(A, B) = \min_{x \in A, y \in B} ||x - y||$. Basta che due persone dei rispettivi gruppi siano vicine per unire tutti (rischia l'effetto "trenino infinito" o *chaining*).
4. **Average Linkage (Armonia media):** $d(A, B) = \frac{1}{|A||B|} \sum_{x \in A} \sum_{y \in B} ||x - y||$. Misura la media di simpatia tra tutte le coppie possibili tra i due gruppi.

#### L'Albero Genealogico (Dendrogramma) e la Fedeltà Cofenofenetica

L'intera sequenza di unioni viene disegnata in un **Dendrogramma**, un albero genealogico rovesciato la cui altezza verticale indica la distanza a cui è avvenuta la fusione. Tagliando l'albero con una linea orizzontale a una determinata quota, scegli esattamente quanti gruppi ottenere.

La fedeltà con cui l'albero rispetta le distanze reali senza distorcerle si misura con il **Coefficiente di Correlazione Cofenofenetica** ($c$):

$$c = \frac{\sum_{i < j} (d_{ij} - \bar{d})(t_{ij} - \bar{t})}{\sqrt{\sum_{i < j} (d_{ij} - \bar{d})^2 \sum_{i < j} (t_{ij} - \bar{t})^2}}$$

- $d_{ij}$: la distanza reale tra gli studenti $i$ e $j$ nello spazio originale.
- $t_{ij}$: l'altezza del ramo nel dendrogramma in cui $i$ e $j$ si sono uniti per la prima volta.
- Se $c > 0.8$, l'albero rappresenta fedelmente le distanze originali senza imbrogliare.

> [!INTERACTIVE] WIDGET: L'Albero delle Amicizie (Dendrogram Builder)
> *Visualizzazione Dinamica:* Un pannello sdoppiato: a sinistra i punti nello spazio 2D, a destra il dendrogramma che cresce passo dopo passo. L'utente muove un cursore a ghigliottina orizzontale (livello di taglio dell'albero) per vedere istantaneamente come i cluster si colorano e si separano nello spazio a sinistra in tempo reale.

### Clustering Basato su Densità: DBSCAN e HDBSCAN

Immagina un concerto rock o una festa in discoteca all'aperto.
Ci sono capannelli densi di centinaia di persone che ballano pigiate al centro della pista, persone ai margini che chiacchierano a contatto con il gruppo, e tizi solitari dispersi nell'oscurità del parcheggio o vicino alle transenne.
Algoritmi come K-Means cercano solo cerchi o sfere perfette e fallirebbero se la pista da ballo avesse la forma di una mezzaluna o di una spirale. **DBSCAN** invece segue semplicemente la folla: dove c'è tanta gente ammassata, c'è un gruppo; chi è solo nel buio viene scartato come "rumore".

DBSCAN usa due parametri chiave: $\epsilon$ (*epsilon*, il raggio delle braccia aperte) e $min\_samples$ (il numero minimo di persone per formare un capannello).
Ogni punto $p$ analizza il suo intorno sferico di raggio $\epsilon$:

$$N_\epsilon(p) = \{q \in X \mid ||p - q|| \le \epsilon\}$$

L'algoritmo classifica ogni persona in tre categorie:
- **Core Point (Cuore della pista):** Se nel raggio $\epsilon$ ci sono almeno $min\_samples$ persone ($|N_\epsilon(p)| \ge min\_samples$). È il motore che genera il gruppo.
- **Border Point (Bordo pista):** Ha meno di $min\_samples$ amici attorno a sé, ma tocca almeno un Core Point. Viene aggregato al gruppo.
- **Noise Point (Intruso isolato / Rumore):** Non tocca nessun Core Point ed è isolato nel buio. Viene contrassegnato con l'etichetta $-1$ (anomalia o rumore).

Un cluster nasce collegando tutti i punti uniti da una catena continua di Core Point a distanza inferiore a $\epsilon$ (*density-connected*).

#### L'Evoluzione con HDBSCAN (Piste a densità variabile)

Se in un festival hai sia un tendone techno stipato come una scatola di sardine sia un'area relax rilassata con persone più distanziate, un unico raggio $\epsilon$ globale fallirà. **HDBSCAN** supera questo limite esplorando tutti i possibili valori di $\epsilon$ e trasformando lo spazio tramite la **Distanza di Raggiungibilità Mutua**:

$$d_{\text{mreach-}k}(a, b) = \max(\{ \text{core}_k(a), \text{core}_k(b), d(a, b) \})$$

- $\text{core}_k(a)$: lo spazio che serve al punto $a$ per trovare i suoi $k$ vicini più stretti.
- Se uno dei due punti si trova in una zona isolata, la distanza mutua "si allarga" artificialmente, impedendo al rumore di fondere per errore cluster a densità diverse.

> [!INTERACTIVE] WIDGET: Il Radar della Discoteca (DBSCAN & HDBSCAN Density Playground)
> *Visualizzazione Dinamica:* Un generatore di forme complesse (cluster a mezzaluna intrecciate, spirali e ciambelle con rumore casuale). L'utente muove gli slider $\epsilon$ e $min\_samples$ vedendo i punti illuminarsi in tempo reale di verde (Core), giallo (Border) o grigio fumo (Noise/Outlier).


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D07-unsupervised-learning. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Riduzione della Dimensionalità e Manifold Learning

Quando la dimensionalità dei dati $d$ cresce verso decine o migliaia di colonne (come accade negli embedding generati dai Large Language Model o nelle serie temporali OSINT), i dati incorrono nella **Maledizione della Dimensionalità** (*Curse of Dimensionality*). All'aumentare delle dimensioni, il volume dello spazio cresce esponenzialmente rispetto al numero di campioni, rendendo lo spazio estremamente vuoto e causando la convergenza di tutte le distanze euclidee a valori simili ($\lim_{d \to \infty} \frac{\max ||x_i - x_j|| - \min ||x_i - x_j||}{\min ||x_i - x_j||} \to 0$).

La riduzione della dimensionalità trasforma la matrice originale $X \in \mathbb{R}^{n \times d}$ in una matrice a bassa dimensione $Z \in \mathbb{R}^{n \times k}$ (con $k \ll d$), eliminando le correlazioni spurie, accelerando l'addestramento dei modelli a valle e consentendo la visualizzazione bidimensionale o tridimensionale.

### La Maledizione della Dimensionalità e la Proiezione Lineare (PCA)

Immagina di dover fotografare una scultura 3D complessa (ad esempio una bicicletta da corsa o una teiera con manico e beccuccio) per proiettarla su un foglio di carta piatto 2D (come un'ombra cinese su una parete).
Se punti la torcia da un'angolazione sfortunata (es. dall'alto), l'ombra sembrerà solo una sagoma confusa e perderai sia le ruote che il manubrio.
La **PCA** (*Principal Component Analysis*) è come un fotografo professionista che gira attorno alla scultura e cerca l'inquadratura perfetta da cui l'ombra risulta il più larga, estesa e dettagliata possibile (massima varianza), catturando quasi tutta l'informazione 3D su un piano 2D.

La matematica della PCA si sviluppa in passaggi lineari precisi:

1. **Centrare i dati:** Si porta il baricentro della scultura al centro degli assi: $\tilde{X} = X - \mu_X \in \mathbb{R}^{n \times d}$.
2. **Matrice di Covarianza (Come variano insieme le coordinate):**
   $$\Sigma = \frac{1}{n-1} \tilde{X}^T \tilde{X} \in \mathbb{R}^{d \times d}$$
   Misura se al crescere di una caratteristica (es. altezza) cresce anche un'altra (es. peso).
3. **Autovettori e Autovalori (Direzione dello scatto e Nitidezza):**
   $$\Sigma v_k = \lambda_k v_k$$
   - $v_k$ (**Autovettore / Componente Principale**): è l'asse della fotocamera (la direzione di massima estensione dell'ombra).
   - $\lambda_k$ (**Autovalore**): misura quanti dettagli e quanta varianza vengono catturati lungo quella direzione.
4. **Varianza Spiegata ($\text{EVR}_k$):**
   $$\text{EVR}_k = \frac{\lambda_k}{\sum_{j=1}^d \lambda_j}$$
   Indica la percentuale esatta di dettagli della scultura 3D conservata dalla $k$-esima foto.

> [!INTERACTIVE] WIDGET: Il Gioco delle Ombre Cinesi (PCA 3D to 2D Projector)
> *Visualizzazione Dinamica:* Una nuvola di punti 3D a forma di ellissoide allungato inclinata nello spazio. L'utente ruota una linea (asse di proiezione) tramite un controller interattivo e osserva l'ombra proiettata: quando l'asse si allinea con l'autovettore principale $v_1$, l'ombra si espande al massimo e il contatore della varianza spiegata raggiunge il 100%.

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: PCA e Varianza Catturata</p>
  <p>Uso della PCA intuitivo: muovi lo slider per ruotare l'asse di proiezione. L'obiettivo della PCA è trovare l'angolo che <strong>massimizza la varianza catturata</strong> (cioè i punti rossi proiettati sono più sparpagliati possibile lungo la linea). Premi il bottone per vedere l'algoritmo agganciare matematicamente l'autovettore principale!</p>
  <iframe src="../widgets/pca.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Tracciando la varianza spiegata cumulativa in funzione del numero di componenti mediante uno **Scree Plot**, è possibile stabilire la dimensionalità intrinseca minima $k$ necessaria a conservare una quota prefissata di varianza totale (tipicamente il 90% o il 95%).

### Manifold Learning Non Lineare: t-SNE e UMAP

Immagina di avere una sciarpa di lana arrotolata stretta a spirale su se stessa (come un dolce *Swiss Roll* o una girella), con disegnati sopra dei piccoli simboli.
Se provi a usare la PCA, è come schiacciare la girella con un ferro da stiro: i lembi di stoffa che si trovano su strati diversi della spirale vengono premuti l'uno contro l'altro, facendo sembrare vicini dei disegni che in realtà erano lontanissimi!
**t-SNE** e **UMAP** sono invece come srotolare delicatamente la sciarpa su un grande tavolo elastico fatto di molle: collegano ogni punto ai suoi vicini più stretti. Se due punti erano vicini sulla stoffa, le molle li tengono vicini anche sul tavolo 2D; se erano lontani, li lasciano allontanare liberamente senza schiacciarli.

#### L'Algoritmo t-SNE (Molle e Probabilità)

1. **Nel mondo ad alta dimensione (Gaussiana dei vicini):**
   La probabilità che il punto $x_i$ scelga $x_j$ come amico vicino segue una campana Gaussiana:
   $$p_{j|i} = \frac{\exp\left(-\frac{||x_i - x_j||^2}{2\sigma_i^2}\right)}{\sum_{k \neq i} \exp\left(-\frac{||x_i - x_k||^2}{2\sigma_i^2}\right)}, \quad p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$
   - $p_{ij}$: quanto è forte l'amicizia tra $i$ e $j$ nello spazio complesso.
   - $\sigma_i$: l'ampiezza della campana (regolata dalla **Perplexity**, ossia quanti vicini considerare).
2. **Sulla mappa 2D piatta (La t di Student contro l'ammassamento):**
   $$q_{ij} = \frac{(1 + ||y_i - y_j||^2)^{-1}}{\sum_{k} \sum_{l \neq k} (1 + ||y_k - y_l||^2)^{-1}}$$
   - $q_{ij}$: la probabilità di vicinanza tra i punti proiettati $y_i$ e $y_j$ sul foglio 2D.
   - La distribuzione **t di Student con 1 grado di libertà** (Cauchy) ha code larghe e risolve il **Crowding Problem**: consente ai gruppi moderatamente lontani di allontanarsi sui bordi della mappa senza schiacciarsi tutti al centro.
3. **Ottimizzazione (Rilassare le molle con Divergenza KL):**
   $$KL(P \parallel Q) = \sum_{i \neq j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$$
   Misura la tensione totale delle molle: il computer sposta i punti sul foglio finché la mappa $Q$ rispecchia al meglio le amicizie $P$.

#### L'Evoluzione con UMAP (Topologia e Velocità)

Mentre t-SNE pensa quasi solo ai vicini microscopici, **UMAP** modella la geometria globale tramite la topologia (insiemi simpliciali sfumati) e minimizza la Cross-Entropia per Insiemi Fuzzy:

$$L_{\text{UMAP}} = \sum_{i \neq j} \left( \mu_{ij} \log \frac{\mu_{ij}}{\nu_{ij}} + (1 - \mu_{ij}) \log \frac{1 - \mu_{ij}}{1 - \nu_{ij}} \right)$$

- $\mu_{ij}$ e $\nu_{ij}$: le probabilità fuzzy di connessione nello spazio originale e proiettato.
- Il primo termine attrae gli amici vicini; il secondo $(1 - \mu_{ij})$ respinge i gruppi lontani, preservando sia i piccoli dettagli locali sia le distanze globali tra macro-cluster, con una velocità computazionale nettamente superiore ($\mathcal{O}(n^{1.14})$ contro $\mathcal{O}(n^2)$ di t-SNE).

> [!INTERACTIVE] WIDGET: Lo Srotolatore Elastico di Swiss Roll (t-SNE vs UMAP Simulator)
> *Visualizzazione Dinamica:* Un modello 3D interattivo dello Swiss Roll che viene proiettato in tempo reale in 2D. L'utente sceglie l'algoritmo (PCA vs t-SNE vs UMAP) e regola lo slider di "Perplexity/N-Neighbors", vedendo la spirale 3D srotolarsi dolcemente in una striscia piana senza sovrapposizioni.

## Anomaly Detection e Rilevamento di Outlier

L'Anomaly Detection (o Outlier Detection) si occupa di identificare osservazioni anomale la cui firma statistica o geometrica devia in modo marcato dalla distribuzione di normalità sottostante. In contesti operativi come il monitoraggio di infrastrutture server, l'analisi forense OSINT o la prevenzione di intrusioni informatiche, gli eventi anomali costituiscono meno dell'1% del volume totale, rendendo impraticabile la classificazione supervisionata a causa della grave scarsità di esempi patologici noti.

### Isolamento Spaziale e Lunghezza del Cammino (Isolation Forest)

Immagina una piazza affollatissima durante una festa di paese: centinaia di persone sono tutte ammassate davanti al palco a ballare, mentre un singolo tizio solitario se ne sta sperduto in cima a una collina a 500 metri di distanza.
Se inizi a tirare delle linee rette a caso con una corda per dividere la mappa in due parti (come un colpo di spada laser):
- Per isolare il tizio solitario sulla collina basterà **un solo taglio casuale** ben piazzato.
- Per isolare una persona specifica stipata in mezzo alla calca davanti al palco, dovrai tirare **decine e decine di tagli millimetrici**!
Questo è il principio di **Isolation Forest**: le anomalie sono rare e diverse dalla massa, quindi si isolano con pochissimi tagli casuali.

L'algoritmo costruisce una foresta di alberi binari di isolamento (*iTree*), scegliendo a ogni nodo una caratteristica a caso $q$ e tagliandola con una soglia casuale $p$.

Le formule quantificano la rarità del punto:

1. **Lunghezza del cammino $h(x)$:** il numero di tagli (archi dell'albero) necessari a isolare il punto $x$ in una foglia singola.
2. **Profondità media attesa di un albero $c(n)$:**
   $$c(n) = 2 \left( \ln(n - 1) + 0.5772156649 \right) - \frac{2(n - 1)}{n}$$
   È il numero "normale" di tagli previsti per isolare un elemento generico in mezzo a una folla di $n$ campioni.
3. **Punteggio di Anomalia ($s(x, n)$):**
   $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
   - $E(h(x))$: la media dei tagli necessari per isolare $x$ in tutta la foresta di alberi.
   - Se $E(h(x)) \ll c(n)$ (bastano pochissimi tagli): l'esponente si avvicina a 0 e $s(x, n) \to 2^0 = 1 \implies$ **Anomalia accertata!**
   - Se $E(h(x)) \approx c(n)$ (servono tagli nella media): $s(x, n) \approx 0.5 \implies$ **Punto normale.**
   - Se $E(h(x)) \gg c(n)$ (servono tantissimi tagli): $s(x, n) \to 0 \implies$ **Inlier nel cuore della folla.**

> [!INTERACTIVE] WIDGET: Il Tagliatore di Spazio (Isolation Forest 2D Slicer)
> *Visualizzazione Dinamica:* Uno spazio 2D con un gruppo denso di punti al centro e 3 punti anomali isolati. L'utente preme "Taglia Casuale": compaiono linee di partizionamento. Un contatore mostra come i punti isolati vengano recintati in appena 1-2 tagli, mentre i punti al centro rimangono raggruppati anche dopo decine di divisioni.

### Iperpiani di Supporto Non Lineari (One-Class SVM)

Immagina un recinto di sicurezza con un campo di forza invisibile costruito attorno a un gregge di pecore in una vallata.
Il guardiano non ha mai visto cosa sia un lupo, una volpe o un ladro; conosce solo l'aspetto e la posizione abituale delle sue pecore.
La **One-Class SVM** prende la mappa del prato e, tramite una formula speciale (il Kernel), la solleva verso l'alto nello spazio 3D come un telo elastico. Lì costruisce una cupola protettiva aderente attorno a tutte le pecore, lasciando fuori l'origine del mondo. Se un nuovo animale atterra al di fuori della cupola, scatta subito l'allarme!

Le formule matematiche definiscono la forma della cupola:

1. **Kernel RBF (Il sollevatore di dimensioni):**
   $$K(x, y) = \exp(-\gamma ||x - y||^2)$$
   - Proietta i dati in uno spazio a dimensioni infinite dove è facile avvolgere i punti normali.
   - $\gamma$ (*gamma*): regola quanto la cupola deve essere aderente e attillata attorno ai punti normali.
2. **Il parametro di tolleranza $\nu$ ($\nu \in (0, 1]$):**
   - Regola la percentuale di pecore un po' distratte che accettiamo di lasciare fuori dalla cupola durante l'addestramento (la quota massima di falsi allarmi / outlier ammessi).

> [!INTERACTIVE] WIDGET: La Cupola Protettiva (One-Class SVM Frontier Tuning)
> *Visualizzazione Dinamica:* Un piano 2D con punti normali e outlier sparsi. L'utente muove gli slider $\gamma$ e $\nu$ osservando la frontiera di decisione colorarsi in tempo reale: con $\gamma$ basso la frontiera è morbida e circolare, con $\gamma$ alto si trasforma in isole sagomate strettamente attorno a ogni singolo gruppo di punti.

### Deviazione della Densità Locale (Local Outlier Factor - LOF)

Immagina di confrontare lo stile di vita di due persone:
- **Marco** vive in un grattacielo nel centro di New York: sul suo pianerottolo ci sono 10 appartamenti in 20 metri. Se una persona si piazza da sola in un corridoio vuoto a 30 metri da tutti, a New York è una cosa insolita e sospetta!
- **Sara** vive in una fattoria isolata nella campagna toscana: la casa del suo vicino più prossimo è a 300 metri. Per lei, avere un vicino a 300 metri è la perfetta e tranquilla normalità.
Un algoritmo rigido guarderebbe solo la distanza in metri e direbbe che Sara è un'anomalia perché è lontana da tutti. **LOF** (*Local Outlier Factor*) invece valuta il contesto locale: confronta la densità di una persona con la densità tipica dei suoi vicini diretti!

Le formule calcolano la densità relativa:

1. **Distanza di Raggiungibilità ($\text{reach-dist}_k(p, o)$):**
   $$\text{reach-dist}_k(p, o) = \max(\{ k\text{-distance}(o), d(p, o) \})$$
   - La distanza tra te ($p$) e il tuo vicino ($o$), che non può mai essere inferiore al raggio abituale del suo quartiere ($k\text{-distance}$).
2. **Densità di Raggiungibilità Locale ($\text{lrd}_k(p)$):**
   $$\text{lrd}_k(p) = \left[ \frac{\sum_{o \in N_k(p)} \text{reach-dist}_k(p, o)}{|N_k(p)|} \right]^{-1}$$
   - Misura quanto sei pigiato rispetto ai tuoi $k$ vicini (l'inverso dello spazio vitale medio).
3. **Punteggio LOF Finale (Il confronto con il vicinato):**
   $$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$
   - È la media del rapporto tra la densità dei tuoi vicini e la tua densità.
   - Se $\text{LOF} \approx 1$: la tua densità è identica a quella dei tuoi vicini (sia che siate tutti stipati a New York, sia che siate tutti sparsi in campagna). Sei un **normale inlier**.
   - Se $\text{LOF} \gg 1$: i tuoi vicini sono pigiatissimi in un grattacielo ma tu sei isolato lontano da loro. Sei un **outlier locale!**

> [!INTERACTIVE] WIDGET: Il Radar Metropolitano vs Campagna (LOF Density Inspector)
> *Visualizzazione Dinamica:* Un piano con due gruppi: un cluster ultra-denso (New York) e un cluster rado e allargato (Campagna). Cliccando su qualsiasi punto, compare un radar che disegna le distanze dai $k$ vicini e calcola all'istante il punteggio $\text{LOF}$, mostrando visivamente perché un punto a distanza $D$ è un'anomalia a New York ma normale in Campagna.


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
