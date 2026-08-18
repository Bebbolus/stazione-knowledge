# D07 — Apprendimento non supervisionato: clustering e riduzione dimensionale

## Meta-modulo D07

**Target**  
Me stesso oggi, e chiunque voglia capire come estrarre struttura dai dati **senza etichette**:
cluster, pattern nascosti, rappresentazioni compatte, anomalie.

**Prerequisiti consigliati**

- D03 — Data foundations (NumPy, Pandas, formati dati, data quality)
- D04 — Matematica e statistica just-in-time (algebra lineare, PCA, probabilità di base)
- D05 — Fondamenti di Machine Learning (concetti supervised, pipeline ML, metriche)
- D06 — Machine Learning classico (alberi, ensemble e valutazione su dati tabellari)

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - concetto di apprendimento non supervisionato  
  - k‑means + un altro algoritmo di clustering (es. DBSCAN o clustering gerarchico)  
  - idea intuitiva di PCA e t‑SNE/UMAP come tecniche di visualizzazione

- **Modalità standard (~8–10 ore)**  
  - uso pratico di scikit‑learn per clustering (k‑means, DBSCAN, Agglomerative)  
  - PCA per riduzione dimensionale, trasformazioni e visualizzazione  
  - valutazione del clustering (silhouette, confronto con ground truth se disponibile)

- **Modalità deep dive (più giornate)**  
  - studio delle note di CS229 su clustering, Mixture of Gaussians e EM, PCA, ICA  
  - esperimenti su dataset reali (OSINT, log, embedding) per scoprire cluster e anomalie  
  - collegamento con representation learning e pretraining di foundation models

**Quando considerare il modulo “completato”**

- so spiegare cosa fa un algoritmo di clustering e cosa fa una tecnica di riduzione dimensionale
- ho applicato almeno due algoritmi di clustering a un dataset reale e li ho confrontati
- ho usato PCA (o simili) per ridurre la dimensione e visualizzare i dati in 2D/3D
- so calcolare e interpretare almeno una metrica interna di clustering (es. silhouette score)
- ho una nota con esempi concreti di quando usare k‑means, DBSCAN, clustering gerarchico, PCA

---

## Perché questo documento

L’apprendimento non supervisionato è la parte del ML in cui **non ho etichette** e chiedo al modello:
“Quali strutture interessanti ci sono nei dati?”.

Mi serve per:

- esplorare dataset prima di definire task supervised  
- trovare gruppi “naturali” (cluster) in utenti/documenti/eventi  
- ridurre la dimensione per:
  - visualizzare dati ad alta dimensione (embedding, feature, log)  
  - costruire feature più compatte per modelli successivi

È collegato al pretraining moderno perché molti modelli vengono addestrati su grandi
quantità di dati privi di etichette manuali, anche se il pretraining dei foundation model
può usare obiettivi self-supervised specifici e non coincide semplicemente con il clustering.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- distinguere i principali tipi di algoritmi non supervisionati
- usare scikit‑learn per applicare clustering e PCA a dataset reali
- interpretare output di clustering (etichette di cluster, centri) e mappe 2D/3D di dati
- valutare almeno qualitativamente la qualità di un clustering
- collegare queste tecniche a casi OSINT/LLM (es. cluster di documenti, embedding, anomalie)

---

## 1. Che cos’è l’apprendimento non supervisionato

### 1.1 Idea generale

In supervised learning conosco i target; in unsupervised, no:

- ho solo una **matrice di feature** \(X\) di shape \((n\_samples, n\_features)\)
- voglio scoprire struttura:
  - cluster
  - direzioni principali di varianza
  - componenti indipendenti
  - anomalie

### 1.2 Esempi concreti

- raggruppare utenti per comportamento di navigazione
- segmentare domini/URL in un contesto OSINT
- capire come si distribuiscono embedding di documenti o frasi
- trovare outlier in log di sicurezza

---

## 2. Clustering: trovare gruppi nei dati

### 2.1 k‑means

**Idea:**

- voglio dividere i dati in \(K\) cluster
- ogni cluster è descritto dal **centroide** (media dei punti del cluster)
- l’algoritmo alterna:
  1. assegnare i punti al centroide più vicino
  2. ricalcolare i centroidi come media dei punti assegnati

Scikit‑learn implementa k‑means come `KMeans` e `MiniBatchKMeans`.

Punti chiave:

- serve scegliere \(K\)
- funziona bene se i cluster sono “compatti” e relativamente sferici
- sensibile a outlier e scaling delle feature

Riferimenti:

- [Clustering in scikit-learn](https://scikit-learn.org/stable/modules/clustering.html)
- [KMeans API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

### 2.2 Clustering gerarchico (Agglomerative)

**Idea:**

- inizia con ogni punto come proprio cluster
- iterativamente unisce i cluster più vicini secondo un criterio (linkage):
  - single, complete, average, ward…

Risultato:

- **dendrogramma** che mostra gerarchia di cluster
- posso “tagliare” il dendrogramma a diversi livelli per ottenere più o meno cluster

Scikit‑learn: `AgglomerativeClustering`.

Riferimenti:

- [AgglomerativeClustering API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html)

### 2.3 DBSCAN e clustering basato su densità

**DBSCAN** (Density-Based Spatial Clustering of Applications with Noise):

- trova cluster come zone ad alta densità separate da regioni a bassa densità
- parametri principali:
  - `eps`: raggio di vicinanza
  - `min_samples`: numero minimo di punti per definire un “core point”

Vantaggi:

- non richiede di specificare \(K\)
- può trovare cluster di forma arbitraria
- identifica outlier (noise)

Svantaggi:

- sensibile alla scelta di `eps` e `min_samples`
- meno adatto a dati molto ad alta dimensione senza una buona metrica

Scikit‑learn: `DBSCAN`.

Riferimenti:

- [DBSCAN API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)

### 2.4 Altri algoritmi (cenno)

Altri metodi di clustering:

- Mean Shift
- Spectral Clustering
- HDBSCAN, OPTICS
- Gaussian Mixture Models (GMM) con EM (approfondibili via CS229/ESL)

D07 non entra nei dettagli di tutti: l’obiettivo è conoscere **i principali trade‑off**.

---

## 3. Riduzione dimensionale: PCA, t‑SNE, UMAP

### 3.1 PCA — Principal Component Analysis

**Obiettivo:**

- trovare le direzioni principali di varianza dei dati
- proiettare i dati in uno spazio di dimensione più bassa preservando il più possibile la varianza

Collegamento con D04:

- PCA si basa su autovettori/autovalori della matrice di covarianza  
- i primi componenti principali corrispondono agli autovettori con autovalori maggiori

Uso:

- compressione
- decorrelazione delle feature
- visualizzazione 2D/3D

In scikit‑learn: `sklearn.decomposition.PCA`.

Riferimenti:

- [PCA in scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)

### 3.2 t‑SNE e UMAP

**t‑SNE (t‑Distributed Stochastic Neighbor Embedding)**:

- tecnica non lineare per visualizzare dati ad alta dimensione in 2D/3D
- preserva relazioni di vicinanza locale
- ottima per visualizzare cluster in embedding (es. output di LLM)

**UMAP** (Uniform Manifold Approximation and Projection):

- simile a t‑SNE, spesso più veloce e meglio scalabile
- costruisce una rappresentazione basata sulla struttura locale del vicinato e può
  mantenere anche alcune relazioni globali; il risultato dipende dai parametri e non va
  interpretato automaticamente come una mappa fedele dello spazio originale

Entrambe sono spesso usate per:

- visualizzare embedding di parole, frasi, documenti
- esplorare cluster, outlier, pattern in dati high‑dimensionali

Riferimenti:

- [t‑SNE e UMAP cheat sheet](https://omkamal.github.io/dimensionalityreduction.html)

---

## 4. Valutare un clustering

### 4.1 Metriche interne

Usano solo la struttura dei dati (nessuna ground truth):

- **Silhouette score**: misura quanto i punti sono vicini al proprio cluster e lontani dagli altri:
  - valori tra \(-1\) e 1
  - vicino a 1 → cluster ben separati e compatti
- **Inertia / SSE**: somma delle distanze quadratiche dai centroidi (per k‑means)

Scikit‑learn: `silhouette_score`, `silhouette_samples`, inertia come attributo dei modelli.

Riferimenti:

- [Silhouette score API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)

### 4.2 Metriche esterne

Richiedono etichette “vere” per confronto:

- **Adjusted Rand Index (ARI)**: confronto tra assegnazioni del clustering e etichette reali
- **Mutual information**, **Fowlkes-Mallows index**, ecc.

Utile per esperimenti controllati (es. dataset come Iris con etichette note).

Riferimenti:

- [Adjusted Rand Score API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)

---

## 5. Collegamento con CS229 e teoria

CS229 dedica un intero blocco all’apprendimento non supervisionato:

- note su k‑means (`cs229-notes7a.pdf`)
- Mixture of Gaussians (`cs229-notes7b.pdf`)
- EM algorithm (`cs229-notes8.pdf`)
- Factor analysis (`cs229-notes9.pdf`)
- PCA (`cs229-notes10.pdf`)
- ICA (`cs229-notes11.pdf`)

D07 non entra nei dettagli analitici di EM, factor analysis, ICA, ma:

- usa k‑means, DBSCAN, clustering gerarchico e PCA come strumenti pratici
- punta a essere un ponte verso queste note quando (e se) servirà più teoria

Riferimenti:

- [CS229 Lecture Notes](https://cs229.stanford.edu/main_notes.pdf)
- [CS229 Unsupervised Learning](https://see.stanford.edu/Course/CS229/43)

---

## 6. Laboratori ed esperimenti

### Laboratorio 1 — k‑means su dataset semplice

**Obiettivo:** applicare k‑means a un dataset reale e visualizzare i cluster.

**Passi:**

1. Scegliere un dataset tabellare con poche feature (es. Iris) oppure un dataset proprio.
2. Standardizzare le feature (es. con `StandardScaler`).
3. Applicare `KMeans` con diversi valori di \(K\) (es. 2, 3, 4).
4. Visualizzare i cluster in 2D, usando due feature o PCA a 2 componenti.
5. Se le etichette reali esistono, confrontare qualitativamente cluster vs classi.

**Deliverable:**

- notebook/script con implementazione
- nota che discute:
  - come cambia il clustering al variare di \(K\)
  - se i cluster “somigliano” alle classi reali (quando ci sono)

---

### Laboratorio 2 — DBSCAN e outlier

**Obiettivo:** usare un algoritmo di clustering basato su densità per trovare cluster e outlier.

**Passi:**

1. Usare un dataset bidimensionale (reale o sintetico) ideale per visualizzazione.
2. Applicare `DBSCAN` con vari valori di `eps` e `min_samples`.
3. Visualizzare i punti colorati per cluster, con outlier in un colore distinto.
4. Annotare come i parametri influenzano:
   - numero di cluster
   - numero di outlier
   - forma dei cluster

**Deliverable:**

- notebook/script con grafici
- nota sulle scelte di `eps` e `min_samples` e sul trade‑off cluster/outlier

---

### Laboratorio 3 — PCA e visualizzazione di embedding

**Obiettivo:** usare PCA (o t‑SNE/UMAP) per visualizzare dati ad alta dimensione.

**Passi:**

1. Scegliere un dataset con molte feature (es. embedding generati da un modello, se disponibili; altrimenti dataset standard).
2. Applicare PCA a 2 o 3 componenti.
3. Visualizzare i dati in 2D/3D, colorando per etichette note (se presenti) o per cluster ottenuti in precedenza.
4. Se possibile, confrontare con una proiezione t‑SNE/UMAP.

**Deliverable:**

- grafici di PCA (e optional t‑SNE/UMAP)
- nota che descrive cosa si vede:
  - cluster visibili
  - outlier
  - eventuali pattern per classe

---

### Laboratorio 4 — Valutazione del clustering

**Obiettivo:** calcolare metriche interne/esterne per un clustering.

**Passi:**

1. Riprendere un clustering di laboratorio 1 o 2.
2. Calcolare:
   - silhouette score medio
   - (se etichette disponibili) ARI o altra metrica esterna
3. Variare il modello/parametri e vedere come cambiano le metriche.
4. Mettere in tabella i risultati.

**Deliverable:**

- tabella con modelli/parametri ↔ metriche
- nota con commenti su quale configurazione sembra più ragionevole e perché

---

## 7. Rubriche e checklist

### Checklist — D07 completato

- [ ] So spiegare cosa fa il clustering e cosa fa la riduzione dimensionale.
- [ ] Ho applicato k‑means a un dataset reale e visualizzato i cluster.
- [ ] Ho usato almeno un’altra tecnica di clustering (DBSCAN o gerarchico).
- [ ] Ho usato PCA per ridurre la dimensione e visualizzare dati ad alta dimensione.
- [ ] So calcolare e interpretare silhouette score (o altra metrica interna).
- [ ] Ho confrontato almeno due algoritmi/configurazioni di clustering sullo stesso dataset.
- [ ] Ho una nota con esempi di uso di clustering in contesti OSINT/embedding/LLM.

### Errori tipici da evitare

- trattare clustering come se fosse “etichettatura vera”: i cluster non sono verità assoluta.
- scegliere \(K\) a caso senza nessuna analisi/intuizione.
- dimenticare di scalare le feature quando necessario (k‑means è sensibile alle scale).
- interpretare t‑SNE/UMAP come rappresentazioni metricamente fedeli (sono strumenti di visualizzazione, non di misura).
- ignorare completamente la valutazione del clustering (nessuna metrica, nessun confronto tra modelli).

### Segnali che “ho davvero capito” D07

- posso prendere un dataset senza etichette e proporre almeno un esperimento di clustering sensato.
- so quando preferire un metodo basato su centroidi (k‑means) vs uno basato su densità (DBSCAN).
- riesco a guardare una proiezione PCA/t‑SNE/UMAP e usarla per guidare analisi successive (es. costruire feature, fare data cleaning).
- non confondo più “cluster” con “classi vere”.

---

## 8. Come ripartire dopo una pausa

Se torno su D07 dopo giorni o settimane:

1. Riapro il notebook più visivo (es. quello di PCA + clustering).
2. Eseguo le celle e guardo i grafici senza modificare nulla.
3. Aggiungo una sola variazione:
   - nuovo valore di \(K\)
   - diverso algoritmo (es. provo DBSCAN su un dataset già usato)
   - nuova metrica (es. silhouette)
4. Aggiorno una nota con:
   - cosa ho modificato
   - cosa ho imparato da questa modifica

Obiettivo: mantenere un **legame visivo-intuitivo** con clustering e riduzione dimensionale, non solo teorico.

---

## 9. Risorse consigliate

### 9.1 scikit-learn: clustering e unsupervised

- **User Guide — Unsupervised learning**  
  Panoramica completa degli algoritmi non supervisionati (clustering, decomposizione, manifold learning).  
  https://scikit-learn.org/stable/user_guide.html  

- **Clustering (overview + algoritmi)**  
  Sezione dedicata a k‑means, affinity propagation, mean shift, spectral, gerarchico, DBSCAN, OPTICS, BIRCH.  
  https://scikit-learn.org/stable/modules/clustering.html  

- **API `sklearn.cluster`**  
  Lista e documentazione degli algoritmi di clustering implementati.  
  https://scikit-learn.org/stable/api/sklearn.cluster.html  

- **Dispense su clustering con scikit-learn (slides)**  
  Introduzione pratica a clustering e metriche (silhouette, ARI, ecc.).  
  https://dbdmg.polito.it/dbdmg_web/wp-content/uploads/2023/04/5-ScikitLearn-Clustering.pdf  

### 9.2 CS229 — Unsupervised learning

- **CS229 Lecture Notes** (versione completa)  
  Include sezione su clustering, Mixture of Gaussians, EM, PCA, ICA, factor analysis.  
  https://cs229.stanford.edu/main_notes.pdf  

- **CS229 Unsupervised Learning (indice dettagliato)**  
  Panoramica delle note non supervisionate (cs229-notes7a…11).  
  https://see.stanford.edu/Course/CS229/43  

### 9.3 Dimensionality reduction (t‑SNE, UMAP)

- **t‑SNE e UMAP cheat sheet (implementazioni Python)**  
  Esempi di codice per applicare t‑SNE e UMAP e confrontarne le visualizzazioni.  
  https://omkamal.github.io/dimensionalityreduction.html  

Queste risorse vanno usate come toolbox: D07 definisce concetti e pattern, i link servono per approfondimenti mirati quando lavorerò su dataset e problemi concreti.