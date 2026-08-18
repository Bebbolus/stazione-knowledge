# D04 — Matematica e statistica just-in-time per ML / LLM

## Perché questo documento

Questo documento raccoglie **la matematica minima ma sufficiente** per capire e lavorare con
machine learning, deep learning e LLM, senza dover fare un corso universitario completo.

Non è un manuale di matematica generale: seleziona solo gli ingredienti che userò davvero
nei moduli successivi (D07 Deep Learning, D09 Transformers/LLM, D10 RAG, D13 RL/alignment).

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- leggere le formule e i diagrammi che compaiono nei corsi ML/LLM senza panico
- capire cosa fanno **vettori, matrici, funzioni e derivate** nei modelli
- avere una base intuitiva di **probabilità e statistica** per loss, likelihood, Bayes
- sapere dove andare ad approfondire (video, corsi, libri) se un punto è debole

---

## 1. Mappa dei concetti chiave

### 1.1 Blocchi principali

Userò quattro blocchi di matematica:

1. **Algebra lineare essenziale**  
   vettori, matrici, prodotto matrice-vettore, combinazioni lineari, norma, prodotto scalare, autovettori.

2. **Calcolo differenziale essenziale**  
   derivate di base, gradiente, chain rule per il backpropagation.

3. **Probabilità di base**  
   variabili aleatorie, distribuzioni, media, varianza, regola della somma e del prodotto.

4. **Statistica di base**  
   stima, intervalli di confidenza a grandi linee, overfitting, bias/varianza.

Ogni sotto-sezione punta a risorse esterne per teoria e esercizi guidati, così posso studiare
in sessioni brevi (15–30 minuti) e tornare quando serve.

---

## 2. Algebra lineare essenziale

### 2.1 Vettori e matrici (intuizione geometrica)

Per ML/LLM mi basta fissare queste immagini mentali:

- Un **vettore** è un punto o una freccia in uno spazio di dimensione \(n\).  
  Esempio: un embedding di parola è un vettore in uno spazio a 512 o 1536 dimensioni.

- Una **matrice** è una funzione lineare che trasforma vettori in altri vettori.  
  Esempio: un layer lineare \(y = Wx + b\) è una matrice \(W\) che “ruota, scala, schiaccia”
  lo spazio degli input.

Punti chiave:

- **somma di vettori** = “combinare caratteristiche”
- **prodotto scalare** = “quanto due vettori puntano nella stessa direzione”
- **norma** = “lunghezza” del vettore (modulo)

### 2.2 Combinazioni lineari, span e base

Concetti critici:

- **Combinazione lineare**: \(a_1 v_1 + \dots + a_k v_k\).  
  Nel contesto di embedding, un vettore può essere scritto come combinazione di vettori base.

- **Span**: tutti i vettori ottenibili come combinazione lineare di un insieme di vettori.
- **Base**: insieme minimo di vettori che genera tutto lo spazio (linearmente indipendenti).

Questi concetti compaiono nella comprensione di:

- **rank** della matrice (quanta informazione “indipendente” contiene)
- **dimensione** dello spazio latente dei modelli
- **compressione** (ridurre la dimensione mantenendo informazione importante)

### 2.3 Prodotto matrice-vettore e matrici come livelli neurali

Per un layer lineare:

\[
y = Wx + b
\]

- \(x\) vettore input (es. embedding di token)
- \(W\) matrice pesi
- \(b\) bias (vettore di traslazione)
- \(y\) vettore output (nuova rappresentazione)

Intuizione:

- \(W\) decide **quali direzioni** dello spazio input vengono preservate, amplificate o attenuate.
- Cambiare \(W\) = cambiare come il modello “vede” i dati.

---

## 3. Autovettori, autovalori e decomposizioni (quanto basta)

### 3.1 Autovettori/autovalori

Definizione operativa:

- Un **autovettore** \(v\) di una matrice \(A\) è un vettore che viene solo scalato da \(A\), non “girato”:
  \[
  Av = \lambda v
  \]
- \(\lambda\) è l’**autovalore** corrispondente.

Intuizione pratica:

- Autovettori = direzioni “speciali” che la trasformazione lineare non cambia di orientamento.
- Autovalori = fattori di scala su quelle direzioni.

In ML:

- appaiono dietro le quinte in PCA, SVD, analisi di stabilità, interpretazione di layer lineari.

### 3.2 PCA, SVD (solo intuizione)

Non serve implementare la SVD a mano, ma è utile sapere:

- La **PCA** trova le direzioni principali di varianza nei dati, cioè dove i dati “si sparpagliano” di più.
- La **SVD** rappresenta una matrice come combinazione di tre matrici speciali, rivelando struttura interna.

Perché importa:

- Molti metodi di riduzione dimensionale e compressione di modelli usano queste idee.
- Alcune analisi di embedding o layer dei LLM ragionano proprio in termini di “direzioni principali”.

---

## 4. Calcolo differenziale essenziale

### 4.1 Derivata e gradiente

Per ML è sufficiente:

- Derivata di una funzione di una variabile: pendenza della curva.
- **Gradiente** = vettore delle derivate parziali di una funzione multivariata.

Se \(L(\theta)\) è la loss e \(\theta\) è il vettore di parametri:

- il gradiente \(\nabla_\theta L\) indica la direzione di massima crescita della loss;
- per **discendere** la loss, ci si muove nella direzione opposta:
  \[
  \theta_{\text{nuovo}} = \theta_{\text{vecchio}} - \eta \nabla_\theta L
  \]
  con \(\eta\) learning rate.

### 4.2 Chain rule (backpropagation)

La **chain rule** dice come derivare funzioni composte:

\[
\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)
\]

In una rete neurale profonda:

- l’output è composizione di tanti layer \(f_L \circ f_{L-1} \circ \dots \circ f_1(x)\);
- la backpropagation è un’applicazione sistematica della chain rule per calcolare
  i gradienti rispetto a tutti i parametri.

Non serve derivare a mano una rete profonda, ma:

- è utile capire che tutto si riduce alla chain rule;
- librerie come PyTorch/TensorFlow implementano autograd per farlo automaticamente.

---

## 5. Probabilità di base

### 5.1 Variabili aleatorie, media, varianza

Concetti chiave:

- **Variabile aleatoria**: variabile il cui valore dipende da un fenomeno casuale.
- **Distribuzione**: descrive come sono distribuiti i valori (es. normale, Bernoulli, binomiale).
- **Valore atteso (media)**: media pesata dei possibili valori.
- **Varianza**: misura della dispersione attorno alla media.

Nel contesto ML:

- la loss spesso è un **valore atteso** rispetto alla distribuzione dei dati;
- la varianza è connessa a rumore, instabilità, overfitting.

### 5.2 Regola della somma e del prodotto

Due regole operative fondamentali:

- **Somma**: probabilità che accada almeno uno tra eventi mutuamente esclusivi.
- **Prodotto**: probabilità che accadano due eventi indipendenti.

In ML/LLM:

- appaiono nel calcolo della **likelihood** di un dataset (prodotto di probabilità dei singoli esempi);
- nei modelli di linguaggio, la probabilità di una sequenza di token si scrive come prodotto
  delle probabilità condizionate token per token.

### 5.3 Bayes (solo l’essenziale)

La **regola di Bayes** collega probabilità a priori, verosimiglianza e posteriori.

Intuizione:

- parto da una credenza iniziale (prior);
- osservo dati (likelihood);
- aggiorno la credenza (posterior).

Questo schema mentale è utile per:

- interpretare modelli probabilistici;
- ragionare su incertezza e aggiornamento della conoscenza.

---

## 6. Statistica e overfitting (quanto basta)

### 6.1 Campioni, stima e generalizzazione

Concetti base:

- **campione**: dati che ho in mano;
- **popolazione**: tutti i dati possibili;
- **stima**: uso il campione per dire qualcosa sulla popolazione.

In ML:

- alleno il modello su un campione (training set) e voglio che generalizzi alla popolazione (dati futuri);
- test/validation set sono modi di stimare quanto il modello generalizza.

### 6.2 Overfitting, underfitting, bias/varianza

Intuizioni pratiche:

- **overfitting**: il modello impara troppo bene il training set (rumore incluso) e va male su nuovi dati.
- **underfitting**: il modello è troppo semplice per catturare la struttura dei dati.
- **tradeoff bias/varianza**: modelli semplici hanno alto bias e bassa varianza, modelli complessi il contrario.

Questi concetti tornano quando valuto:

- dimensione di un modello (numero di parametri)
- numero di epoche di training
- uso di regolarizzazione, dropout, early stopping

---

## 7. Come usare questo modulo nello studio

### 7.1 Strategia “just-in-time”

Con ADHD e tempo limitato non ha senso fare un corso full di matematica prima di toccare i modelli:

- uso questo D04 come **mappa di riferimento**;
- quando in D07/D09 incontro qualcosa che non capisco (es. autovettori, gradiente),
  torno alla sezione relativa e poi guardo una risorsa esterna mirata;
- segno in una nota privata quali concetti sono ancora deboli, per pianificare micro-sessioni dedicate.

### 7.2 Note operative

Per ogni concetto importante posso farmi:

- una micro-fiche (nota breve) con:
  - definizione in 2 righe
  - intuizione visiva o metafora
  - 1–2 formule chiave
  - link a video/esercizi

Queste fiche andranno poi nel quaderno / study pack stampabile.

---

## 8. Risorse consigliate

### 8.1 Algebra lineare

- **3Blue1Brown – Essence of Linear Algebra (playlist)**  
  Serie video che visualizza concetti come vettori, matrici, combinazioni lineari, autovettori.  
  https://www.3blue1brown.com/lessons/eola-preview  
  https://essence-of-linear-algebra.vercel.app/

- **MIT 18.06 – Linear Algebra (Gilbert Strang)**  
  Homepage corso e materiali:  
  https://web.mit.edu/18.06/www/  
  Lecture notes / ZoomNotes (OCW):  
  https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/  
  Esempi strutturati nel repo GitHub del corso:  
  https://github.com/mitmath/1806

### 8.2 Probabilità e statistica

- **Khan Academy – Probability & Statistics**  
  Percorsi introduttivi su probabilità, variabili aleatorie, distribuzioni, inferenza:  
  https://www.khanacademy.org/math/statistics-probability  
  Sezioni focalizzate sulla probabilità:  
  https://www.khanacademy.org/math/statistics-probability/probability-library

- **Probability and statistics – raccolta strutturata di video Khan Academy**  
  Panoramica su probabilità, combinatoria, variabili aleatorie, distribuzioni e inferenza:  
  https://ko.mujica.org/math/probability/index.html

### 8.3 Collegamenti ai corsi ML / NLP

Queste risorse useranno in pieno i concetti di questo modulo:

- **Stanford CS229 – Machine Learning**  
  Sito del corso: https://cs229.stanford.edu/  
  Syllabus: https://cs229.stanford.edu/syllabus-new.html  
  Versione online: https://online.stanford.edu/courses/cs229-machine-learning

- **Stanford CS224N – Natural Language Processing with Deep Learning**  
  Sito del corso: https://web.stanford.edu/class/cs224n/  
  Archivio recente: https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/  
  Versione online: https://online.stanford.edu/courses/cs224n-natural-language-processing-deep-learning

---

## 9. Prossimi passi per me

- Scegliere 1–2 playlist/video per ogni blocco (es. 3Blue1Brown per algebra, Khan per probabilità).
- Segnare quali concetti sono ancora “oscuri” dopo il primo passaggio su D07/D09.
- Aggiornare questo documento con esempi e screenshot di formule che incontro davvero nei corsi e nei paper.