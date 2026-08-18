# D04 — Matematica e statistica just-in-time per ML / LLM

## Meta-modulo D04

**Target**  
Me stesso oggi, e chiunque voglia avere la **matematica minima ma sufficiente**
per capire e usare ML, deep learning e LLM, senza fare un corso universitario completo.

**Prerequisiti consigliati**

- D02 (Python refresher) e D03 (data foundations) completati o quasi
- confidenza base con:
  - vettori e matrici “a livello intuitivo”
  - uso di NumPy/Pandas e dataset tabellari
- nessuna necessità di dimostrazioni formali, ma disponibilità a vedere formule e grafici

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - algebra lineare essenziale (vettori, matrici, prodotto, autovettori)  
  - concetti base di derivate/gradiente e chain rule  
  - probabilità elementare (eventi, media, varianza)  
  - overfitting e bias/varianza a livello concettuale

- **Modalità standard (~8–10 ore)**  
  - visione intuitiva di algebra lineare (3Blue1Brown)  
  - sezioni selezionate di MIT 18.06 per consolidare  
  - probabilità e statistica con esempi strutturati (Khan Academy)  
  - esercizi Feynman su concetti chiave

- **Modalità deep dive (più giornate)**  
  - seguire un percorso completo (es. Essence of Linear Algebra + blocchi di Khan + parti di CS229)  
  - fare esercizi manuali su backpropagation, likelihood, Bayes, modelli semplici

**Quando considerare il modulo “completato”**

- so leggere formule e diagrammi base di ML/LLM senza panico
- capisco intuitivamente vettori, matrici, prodotto scalare, norma, autovettori/autovalori
- so cosa sono derivata, gradiente e chain rule in relazione al training di reti neurali
- ho una comprensione operativa di probabilità di base, media, varianza e concetti di overfitting
- ho almeno una lista di “punti deboli” personali da rafforzare con risorse esterne

---

## Perché questo documento

Questo documento raccoglie **la matematica essenziale** che userò in ML/LLM,
organizzata per blocchi e pensata come **riferimento just-in-time**:

- non sostituisce corsi completi (CS229, 18.06, ecc.)
- mi permette di tornare rapidamente a concetti chiave quando in altri moduli
  (D07/D09/D10/D13) incontro formule o idee non chiare
- è progettato per sessioni brevi (15–30 minuti), compatibili con tempo spezzato/ADHD

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- visualizzare vettori e matrici e capire cosa fa una trasformazione lineare
- interpretare il gradiente come direzione di massima crescita della loss
- capire la chain rule come base concettuale della backpropagation
- gestire concetti base di probabilità (eventi, variabili aleatorie, media, varianza)
- ragionare su overfitting/underfitting e bias/varianza in parole semplici

---

## 1. Mappa dei concetti chiave

### 1.1 Blocchi principali

Userò quattro blocchi di matematica:

1. **Algebra lineare essenziale**  
   vettori, matrici, prodotto matrice-vettore, combinazioni lineari, norma, prodotto scalare, autovettori.

2. **Calcolo differenziale essenziale**  
   derivate di base, gradiente, chain rule per la backpropagation.

3. **Probabilità di base**  
   eventi, variabili aleatorie, distribuzioni, media, varianza, regole di somma/prodotto.

4. **Statistica di base e overfitting**  
   campioni, popolazioni, stima, bias/varianza, over/underfitting.

Ogni blocco è pensato per essere **richiamato al bisogno** nei moduli successivi.

---

## 2. Algebra lineare essenziale

### 2.1 Vettori e matrici (intuizione geometrica)

Immagine mentale:

- Un **vettore** è un punto o una freccia in uno spazio di dimensione \(n\).  
  Esempio: un embedding di parola è un vettore in uno spazio a 512 o 1536 dimensioni.

- Una **matrice** è una funzione lineare che trasforma vettori in altri vettori.  
  Esempio: un layer lineare \(y = Wx + b\) è una matrice \(W\) che “ruota, scala, schiaccia”
  lo spazio degli input.

Punti chiave:

- somma di vettori = combinare caratteristiche
- prodotto scalare = “quanto due vettori puntano nella stessa direzione”
- norma = “lunghezza” del vettore

La serie *Essence of Linear Algebra* di 3Blue1Brown visualizza proprio queste intuizioni.

### 2.2 Combinazioni lineari, span e base

Concetti fondamentali:

- **Combinazione lineare**: \(a_1 v_1 + \dots + a_k v_k\).  
  Un vettore può essere espresso come combinazione di altri vettori base.

- **Span**: insieme di tutti i vettori ottenibili come combinazione di un insieme di vettori.

- **Base**: insieme minimo di vettori linearmente indipendenti che genera tutto lo spazio.

Questi concetti sono importanti per:

- capire cosa significa che un layer “riduce la dimensione”
- interpretare rank di una matrice e capacità di rappresentare l’informazione
- ragionare su spazi latenti ed embedding

### 2.3 Prodotto matrice-vettore e layer lineari

Per un layer lineare:

\[
y = Wx + b
\]

- \(x\) è il vettore input (es. embedding di token)
- \(W\) è la matrice dei pesi
- \(b\) è il bias (vettore di traslazione)
- \(y\) è il vettore output (nuova rappresentazione)

Intuizione:

- le righe/colonne di \(W\) determinano quali direzioni dello spazio input vengono
  preservate, amplificate o attenuate
- cambiare \(W\) significa cambiare come il modello “vede” i dati

---

## 3. Autovettori, autovalori e decomposizioni

### 3.1 Autovettori/autovalori (a grandi linee)

Definizione operativa:

- Un **autovettore** \(v\) di una matrice \(A\) è un vettore che viene solo scalato da \(A\), non “girato”:
  \[
  Av = \lambda v
  \]
- \(\lambda\) è l’**autovalore** corrispondente.

Intuizione:

- autovettori = direzioni speciali che una trasformazione lineare non ruota, ma solo allunga/accorcia
- autovalori = fattori di scala su quelle direzioni

In ML:

- appaiono dietro le quinte in PCA, SVD, analisi di stabilità, analisi di layer e embedding.

### 3.2 PCA e SVD (senza formule pesanti)

Concetti utili:

- **PCA** (Principal Component Analysis) trova le direzioni principali di varianza nei dati  
  → riduzione dimensionale, compressione, visualizzazione.

- **SVD** (Singular Value Decomposition) scompone una matrice in tre matrici speciali
  che rendono evidente la sua struttura interna.

Non serve implementarle a mano, ma è utile:

- sapere che esistono
- intuire che molti metodi di compressione e analisi di embedding si basano su idee simili

---

## 4. Calcolo differenziale essenziale

### 4.1 Derivata e gradiente

Per ML/LLM è sufficiente:

- Derivata di una variabile: pendenza della curva in un punto.
- **Gradiente** = vettore delle derivate parziali di una funzione multivariata.

Se \(L(\theta)\) è la loss e \(\theta\) il vettore di parametri:

- il gradiente \(\nabla_\theta L\) indica la direzione di massima crescita della loss
- per discendere la loss, ci si muove nella direzione opposta:

\[
\theta_{\text{nuovo}} = \theta_{\text{vecchio}} - \eta \nabla_\theta L
\]

con \(\eta\) learning rate.

### 4.2 Chain rule (backpropagation)

La **chain rule** per funzioni composte:

\[
\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)
\]

In una rete neurale:

- l’output è composizione di tanti layer \(f_L \circ f_{L-1} \circ \dots \circ f_1(x)\)
- la **backpropagation** è un’applicazione meccanica della chain rule per calcolare
  gradiente e aggiornare parametri layer per layer

Importante:

- non devo fare a mano la backpropagation per reti complesse  
- devo però capire che:
  - l’errore fluisce all’indietro  
  - ogni layer riceve un contributo di errore proporzionale all’effetto che ha sull’output

---

## 5. Probabilità di base

### 5.1 Eventi, probabilità, variabili aleatorie

Concetti:

- **evento**: risultato o insieme di risultati di un esperimento casuale
- **probabilità**: misura da 0 a 1 di quanto un evento è probabile  
  (es. “test positivo”, “piove domani”, “token X in output”)

- **variabile aleatoria**: funzione che associa valori numerici ai risultati
- **distribuzione**: descrive come sono distribuiti i valori (es. binomiale, normale)

La definizione base vista spesso in Khan Academy:

\[
\text{Probabilità di un evento} = \frac{\#\text{ modi in cui può accadere}}{\#\text{ risultati possibili}}
\]

### 5.2 Media, varianza, distribuzioni

Concetti chiave:

- **media**: valore atteso, centro della distribuzione
- **varianza**: quanto i valori si discostano dalla media
- **deviazione standard**: radice della varianza, misura della dispersione

In ML:

- la loss spesso è un valore atteso rispetto alla distribuzione dei dati
- varianza e deviazione standard compaiono ovunque (normalizzazione, errori, rumore)

---

## 6. Regole di somma, prodotto e Bayes

### 6.1 Regola della somma e del prodotto

Regole operative:

- **somma**: probabilità che accada almeno uno tra eventi mutuamente esclusivi
- **prodotto**: probabilità che accadano due eventi indipendenti

Usi:

- calcolo di probabilità in modelli semplici
- interpretazione di likelihood in modelli generativi

### 6.2 Bayes (solo l’essenziale)

La regola di Bayes collega probabilità a priori, verosimiglianza e posteriori.

Intuizione:

- ho una credenza iniziale (prior)
- osservo un dato (likelihood)
- aggiorno la credenza (posterior)

Schema:

\[
P(A\mid B) = \frac{P(B\mid A) P(A)}{P(B)}
\]

In ML:

- interpretazione di modelli probabilistici
- ragionamento su incertezza e aggiornamento delle informazioni

---

## 7. Statistica e overfitting

### 7.1 Campioni, popolazione, stima

Concetti:

- **campione**: dati osservati
- **popolazione**: insieme di tutti i possibili dati
- **stima**: uso del campione per inferire proprietà della popolazione

Nel training ML:

- dataset che ho = campione
- dati reali futuri = popolazione
- voglio che il modello generalizzi dai campioni alla popolazione

### 7.2 Overfitting, underfitting, bias/varianza

Intuizioni pratiche:

- **overfitting**: modello troppo complesso, impara il rumore del training set
- **underfitting**: modello troppo semplice, non cattura la struttura dei dati
- **bias/varianza**:
  - alto bias → modello rigido, errori sistematici
  - alta varianza → modello instabile, sensibile ai dettagli del training set

In D05/D06/D07 vedrò come questi concetti si traducono in scelte di architettura e training.

---

## 8. Come usare questo modulo nello studio

### 8.1 Strategia just-in-time

Con tempo limitato/ADHD, non ha senso studiare tutta la matematica in anticipo:

- uso D04 come **mappa di riferimento**
- quando in altri moduli incontro un concetto non chiaro (es. autovettori, chain rule),
  torno alla sezione relativa e poi guardo una risorsa esterna mirata
- se un concetto resta ostico, lo segno in una nota dedicata (“Debolezze D04”)
  e pianifico micro-sessioni su quel punto

### 8.2 Fiche/flashcard di concetto

Per ogni concetto chiave posso crearmi una mini-fiche:

- definizione in 2–3 righe
- intuizione visiva/metafora
- una formula chiave
- link a 1 video/articolo ben fatto

Queste fiche diventeranno materiale per il quaderno/study pack e per ripassi veloci.

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Vettori, matrici e trasformazioni

**Obiettivo:** vedere concretamente shape e trasformazioni lineari.

**Passi:**

1. In un notebook Python, creare alcuni vettori 2D e 3D con NumPy.
2. Definire matrici semplici (rotazioni, scaling) e applicarle ai vettori.
3. Visualizzare (anche solo tramite stampa) shape e valori prima/dopo.
4. Annotare in una nota cosa significa “trasformazione lineare” nel contesto di un layer.

**Deliverable:**

- notebook `.ipynb` o script `.py` con esempi
- breve nota in `private/notes/` che spiega la propria intuizione su vettori/matrici

---

### Laboratorio 2 — Gradiente e discesa della loss in 1D

**Obiettivo:** capire il gradiente su una funzione semplice.

**Passi:**

1. Definire in Python una funzione di una variabile, ad esempio \(L(\theta) = (\theta - 3)^2\).
2. Calcolare la derivata analitica (gradiente): \(L'(\theta) = 2(\theta - 3)\).
3. Implementare un loop di gradient descent in 1D:
   - inizializzare \(\theta\) a un valore qualunque (es. 0)
   - aggiornare \(\theta\) per alcuni passi usando la formula di GD
4. Stampare i valori di \(\theta\) e \(L(\theta)\) ad ogni iterazione.

**Deliverable:**

- script/notebook con l’implementazione
- nota che descrive cosa succede variando il learning rate

---

### Laboratorio 3 — Probabilità di eventi semplici

**Obiettivo:** usare probabilità base per un esempio concreto.

**Passi:**

1. Modellare in Python un esperimento semplice (es. lanci di moneta o dado).
2. Simulare l’esperimento molte volte e stimare probabilità empiriche.
3. Confrontarle con probabilità teoriche.
4. Riflettere su come questa logica si generalizza a eventi più complessi (es. token in sequenza).

**Deliverable:**

- script con simulazioni
- nota che collega la simulazione a concetti di probabilità in ML/LLM

---

### Laboratorio 4 — Overfitting in un modello giocattolo

**Obiettivo:** visualizzare overfitting e underfitting con un modello semplice.

**Passi:**

1. Generare dati sintetici (es. punti (x, y) da una funzione semplice con rumore).
2. Fit di un modello lineare e uno polinomiale di grado alto.
3. Confrontare errori su training set e su un test set separato.
4. Annotare cosa significa “overfitting” in questo contesto.

**Deliverable:**

- notebook con grafici o almeno valori di errore
- nota che descrive cosa ha visto e come collega il concetto a modelli più grandi

---

## 10. Rubriche e checklist

### Checklist — D04 completato

- [ ] Capisco cosa sono vettori e matrici e che ruolo hanno in un layer lineare.
- [ ] Ho un’intuizione della differenza tra trasformazione lineare e non lineare.
- [ ] So spiegare con parole mie cosa sono gradiente e chain rule.
- [ ] So definire variabile aleatoria, media, varianza, distribuzione in modo semplice.
- [ ] Ho una visione qualitativa di overfitting, underfitting e bias/varianza.
- [ ] Ho completato almeno 2 dei 4 laboratori (anche in forma semplificata).
- [ ] Ho annotato in una nota i concetti che restano più deboli.

### Errori tipici da evitare

- cercare di studiare tutto come un manuale di matematica, senza legarlo subito a esempi ML/LLM.
- sentirsi “in colpa” perché non si ricordano formule; l’obiettivo è intuizione operativa.
- ignorare completamente la parte statistica e focalizzarsi solo su algebra lineare.
- non segnare da nessuna parte i concetti difficili, rischiando di ripetere la stessa fatica ogni volta.

### Segnali che “ho davvero capito” D04

- quando vedo \(y = Wx + b\) so visualizzare \(W\) come trasformazione dello spazio input.
- se leggo “gradient descent” in un paper o in CS229, non devo più chiedermi “cos’è il gradiente?”.
- riconosco esempi di overfitting in grafici di training/validation loss.
- posso spiegare a un collega cos’è una variabile aleatoria e perché la media non è “solo” una media aritmetica, ma un valore atteso.

---

## 11. Come ripartire dopo una pausa

Se torno su D04 dopo giorni o settimane:

1. Rileggo solo la sezione di un blocco (es. algebra lineare o probabilità), non tutto il documento.
2. Scelgo un laboratorio e lo faccio in forma minima (anche solo prima metà).
3. Segno in una nota quali concetti mi sono tornati più difficili e con quali video/articoli li affronterò.
4. Collegando D04 ai moduli in corso (es. D07/D09), mi chiedo:
   - “Quale concetto matematico mi sta bloccando davvero?”
   - “Quale sezione di D04 posso usare per sbloccare questo punto?”

Obiettivo: usare D04 come **toolbox** e non come esame di matematica.

---

## 12. Risorse consigliate

### 12.1 Algebra lineare

- **3Blue1Brown – Essence of Linear Algebra (serie video)**  
  Serie che visualizza concetti come vettori, matrici, combinazioni lineari, autovettori.  
  Anteprima e link alla playlist:  
  https://www.3blue1brown.com/lessons/eola-preview  

- **Essence of Linear Algebra – corso completo**  
  Raccolta completa della serie con capitoli e descrizioni.  
  https://essence-of-linear-algebra.vercel.app/  

- **Note di corso basate su Essence of Linear Algebra**  
  Appunti strutturati che seguono l’intera serie video.  
  https://github.com/SireJeff/linear-algebra-3blue1brown-notes

- **MIT 18.06 – Linear Algebra (Gilbert Strang)**  
  Homepage e materiali del corso.  
  https://web.mit.edu/18.06/www/  

---

### 12.2 Probabilità e statistica

- **Khan Academy – Probability & Statistics**  
  Percorso completo su probabilità e statistica, con esercizi interattivi.  
  https://www.khanacademy.org/math/statistics-probability  

- **Probability library (Khan Academy)**  
  Moduli su probabilità base, somma/prodotto, eventi composti.  
  https://www.khanacademy.org/math/statistics-probability/probability-library  

- **Khan Academy on a Stick – Probability and statistics**  
  Raccolta strutturata di video su probabilità, variabili aleatorie, distribuzioni, inferenza.  
  https://ko.mujica.org/math/probability/index.html  

---

### 12.3 Collegamenti ai corsi ML / NLP

Queste risorse riprendono in pieno i prerequisiti matematici di D04:

- **Stanford CS229 — Machine Learning**  
  Sito del corso: https://cs229.stanford.edu/  
  Syllabus e requisiti matematici:  
  https://cs229.stanford.edu/syllabus-new.html  
  Handout con prerequisiti (probabilità e algebra lineare):  
  https://cs229.stanford.edu/materials/handout.pdf  

- **Stanford CS224N — Natural Language Processing with Deep Learning**  
  Sito del corso: https://web.stanford.edu/class/cs224n/  
  Archivio recente: https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/  
  Versione online:  
  https://online.stanford.edu/courses/cs224n-natural-language-processing-deep-learning