# D05 — Fondamenti di Machine Learning

## Meta-modulo D05

**Target**  
Me stesso oggi, e chiunque voglia capire *come funziona davvero* il machine learning classico:
cosa significa “allenare un modello”, come leggere una curva di training, come scegliere una metrica
e perché a volte un modello semplice è meglio di uno complesso.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D03 — Data foundations (NumPy, Pandas, SQL, data quality)
- D04 — Matematica e statistica just-in-time (intuizione su algebra lineare, probabilità, overfitting)

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - concetti chiave: supervised/unsupervised, dataset, feature/target  
  - workflow base: split train/test, fit, predict, valutare  
  - esempi con scikit-learn su dataset piccoli

- **Modalità standard (~8–10 ore)**  
  - introduzione pratica a scikit-learn (pipeline, cross-validation)  
  - confronto tra modelli semplici (baseline, regressione lineare, kNN)  
  - prime esperienze di tuning e diagnosi di over/underfitting

- **Modalità deep dive (più giornate)**  
  - leggere parti selezionate di CS229 / Elements of Statistical Learning / ISLR  
  - lavorare su 1–2 dataset reali con workflow completo (data card, pipeline, valutazione)

**Quando considerare il modulo “completato”**

- so descrivere la pipeline ML standard (dati → feature/target → split → training → valutazione → iterazione)
- so costruire e addestrare almeno un modello di regressione e uno di classificazione con scikit-learn
- so interpretare metriche base (accuracy, precision/recall, MSE/RMSE, R²)
- so riconoscere segnali di overfitting/underfitting in curve di training/validation
- ho almeno un progetto semplice salvato nel mio workspace con codice + note + risultati

---

## Perché questo documento

Questo documento introduce i **fondamenti concettuali del machine learning classico**:

- cos’è un modello, cosa significa “imparare dai dati”
- come costruire un workflow affidabile (non solo “prova un algoritmo e guarda il numero di accuracy”)
- come usare scikit-learn come laboratorio standard per modelli classici, prima di passare a DL/LLM.

È il ponte naturale tra:

- blocco dati/matematica (D03/D04)
- blocco modelli più complessi (D06 ML classico approfondito, D07 DL, D09 LLM)

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- distinguere chiaramente supervised/unsupervised/other (RL, ecc.) a livello concettuale
- descrivere gli elementi di un problema supervised (feature, target, loss, metrica)
- costruire un modello semplice con scikit-learn e valutarlo in modo sensato
- applicare concetti di train/validation/test e cross-validation
- capire quando sto misusando un modello (overfitting, scelta sbagliata di metrica, leakage nei dati)

---

## 1. Mappa dei concetti

### 1.1 Tipi di problemi ML

1. **Supervised learning**  
   - input + target: voglio prevedere una variabile di output  
   - classificazione, regressione

2. **Unsupervised learning**  
   - solo input, niente target: voglio trovare struttura nei dati  
   - clustering, riduzione dimensionale

3. **Altri paradigmi** (citazione, non focus di D05)  
   - semi-supervised, self-supervised, reinforcement learning

### 1.2 Pipeline standard ML (scikit-learn style)

Pipeline concettuale (scikit-learn la formalizza esplicitamente):

1. definire il problema (dominio, obiettivo, vincoli)
2. esplorare i dati (EDA, data quality → D03)
3. definire feature/target
4. split train/validation/test
5. scegliere/modellare baseline
6. addestrare modelli + tuning di base
7. valutare con metriche appropriate
8. fare error analysis e iterare

---

## 2. Supervised learning: classificazione e regressione

### 2.1 Elementi di un problema supervised

Per un problema supervised servono:

- **Feature (X)**: input, rappresentazione dei dati (es. misure, parole, pixel)
- **Target (y)**: ciò che voglio predire
- **Modello**: famiglia di funzioni \(f_\theta\) che mappano X in y
- **Loss**: misura di quanto le predizioni sono sbagliate
- **Metrica**: misura di qualità usata per confrontare modelli

Esempi:

- classificazione binaria (spam / not-spam)
- classificazione multi-classe (tipo di oggetto in un’immagine)
- regressione (prezzo, tempo, numero di eventi)

### 2.2 Classificazione

- output discreto (classi)
- tipiche metriche:
  - accuracy
  - precision, recall, F1 (soprattutto con classi sbilanciate)
  - ROC-AUC

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: Confine di Decisione (k-NN)</p>
  <p>Scegli una classe (Blu o Arancio) e aggiungi punti sul piano. Lo sfondo si colorerà in tempo reale per mostrarti il <strong>confine di classificazione</strong> (decision boundary). Il modello (k-NN con k=3) classifica ogni punto dello spazio in base alla maggioranza dei 3 punti reali più vicini.</p>
  <iframe src="../widgets/classificazione.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Modelli classici:

- regressione logistica
- k-Nearest Neighbors
- SVM
- alberi, random forest, gradient boosting (approfonditi in D06)

### 2.3 Regressione

- output continuo (valore numerico)
- tipiche metriche:
  - MSE (Mean Squared Error), RMSE
  - MAE (Mean Absolute Error)
  - R² (coefficient of determination)

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: Regressione Lineare e MSE</p>
  <p>Clicca nell'area sottostante per aggiungere punti. La retta si aggiusterà in tempo reale cercando di minimizzare l'Errore Quadratico Medio (MSE) – ovvero "tirando" il più vicino possibile a ogni punto.</p>
  <iframe src="../widgets/regressione_lineare.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Modelli classici:

- regressione lineare
- regressione Ridge/Lasso
- modelli non lineari (es. alberi, random forest, boosting)

---

## 3. Workflow pratico con scikit-learn

### 3.1 Visione “estimator API”

scikit-learn standardizza i modelli come **stimatori** con due metodi chiave:

- `fit(X, y)` — addestra il modello sui dati
- `predict(X)` — genera predizioni su nuovi dati

Workflow base:

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
```

### 3.2 Train/validation/test e cross-validation

Per valutare correttamente un modello:

- separare un **test set** da usare solo alla fine
- durante lo sviluppo, usare:
  - un validation set esplicito, oppure
  - cross-validation (`cross_val_score`, `GridSearchCV`, ecc.)

Cross-validation:

- divide il training set in K “fold”
- allena e valuta K volte, ogni volta con un fold diverso come validation
- media le performance per avere una stima più robusta

---

## 4. Bias, varianza e complessità del modello

### 4.1 Bias/varianza (collegato a D04)

Ricapitolando:

- **Bias**: errore sistematico dovuto a modello troppo semplice o sbagliato
- **Varianza**: sensibilità ai dettagli del training set (modello troppo complesso)

Effetti:

- modello ad alto bias → underfitting
- modello ad alta varianza → overfitting

In D05:

- vedo come bias/varianza si manifesta su modelli concreti (curve di training/test)
- in D06 approfondisco tecniche per controllarla (regolarizzazione, ensemble, ecc.)

### 4.2 Curve di apprendimento

Curve tipiche:

- training loss ↓ mentre training size ↑  
- validation loss:
  - scende e poi risale se c’è overfitting
  - rimane alta se il modello è troppo semplice (underfitting)

Interpretare le curve:

- se train loss è molto bassa ma test loss alta → overfitting
- se entrambe sono alte → underfitting/insufficiente capacità modello

---

## 5. Metriche e scelta del modello

### 5.1 Scelta delle metriche

Dipende dal problema:

- classificazione bilanciata → accuracy può bastare
- classificazione sbilanciata → meglio precision/recall/F1, ROC-AUC
- regressione → MSE/RMSE/MAE, a seconda della penalizzazione che voglio

scikit-learn offre molte metriche in `sklearn.metrics` (accuracy_score, precision_score, recall_score, roc_auc_score, mean_squared_error, ecc.).

### 5.2 Baseline e modelli complessi

Sempre utile partire da:

- baseline semplicissima:
  - classificazione: modello che predice sempre la classe maggioritaria
  - regressione: media dei target
- modello lineare (regressione logistica, regressione lineare)
- solo dopo modelli più complessi (alberi, ensemble)

Se un modello complesso non batte la baseline in modo chiaro:

- c’è un problema di dati, features, o valutazione
- non è (solo) un problema di “potenza del modello”

---

## 6. Laboratori ed esercizi

### Laboratorio 1 — Primo modello di classificazione (Iris)

**Obiettivo:** seguire tutta la pipeline supervised su un dataset classico.

**Passi:**

1. Usare il dataset `iris` di scikit-learn (classico esempio).
2. Splittare in train/test (es. 80/20).
3. Addestrare un classificatore semplice (es. `LogisticRegression`).
4. Calcolare accuracy e, se possibile, matrice di confusione.
5. Annotare in una nota:
   - metriche ottenute
   - errori tipici (quali classi vengono confuse)

**Deliverable:**

- script/notebook `iris_classifier.py` o `.ipynb`
- nota sintetica con risultati e interpretazione

---

### Laboratorio 2 — Modello di regressione e MSE

**Obiettivo:** vedere la differenza tra classificazione e regressione nella pratica.

**Passi:**

1. Scegliere un dataset di regressione (es. `diabetes` in scikit-learn o un CSV proprio).
2. Splittare in train/test.
3. Addestrare una regressione lineare.
4. Calcolare MSE, RMSE e R².
5. Confrontare con una baseline che predice sempre la media del target.

**Deliverable:**

- script/notebook con modello + metriche
- nota su quanto il modello migliora rispetto alla baseline

---

### Laboratorio 3 — Overfitting con modello complesso

**Obiettivo:** vedere overfitting concreto su un dataset semplice.

**Passi:**

1. Usare un dataset relativamente piccolo (es. `digits` di scikit-learn).
2. Addestrare:
   - un modello semplice (es. Logistic Regression o albero poco profondo)
   - un modello complesso (es. RandomForest con molti alberi molto profondi)
3. Confrontare:
   - training accuracy
   - test accuracy
4. Annotare in quali casi il modello complesso overfitte.

**Deliverable:**

- script/notebook con confronto tra modelli
- nota con descrizione di cosa significa “overfitting” in questo esempio

---

### Laboratorio 4 — Cross-validation e scelta modello

**Obiettivo:** usare cross-validation per scegliere tra modelli.

**Passi:**

1. Prendere un dataset di classificazione o regressione.
2. Scegliere 2–3 modelli (es. Logistic Regression, kNN, RandomForest).
3. Usare `cross_val_score` per confrontare le performance con K-fold (es. 5-fold).
4. Scegliere il modello da usare in base alla performance media e alla varianza tra fold.

**Deliverable:**

- script/notebook con risultati cross-validation
- nota che giustifica la scelta del modello finale

---

## 7. Rubriche e checklist

### Checklist — D05 completato

- [ ] So spiegare la differenza tra supervised e unsupervised (con esempi).
- [ ] So formalizzare un problema supervised in termini di X, y, modello, loss, metrica.
- [ ] Ho addestrato almeno un modello di classificazione e uno di regressione con scikit-learn.
- [ ] Ho usato train/test split (e idealmente cross-validation) in almeno un esperimento.
- [ ] Ho confrontato almeno un modello con una baseline banale.
- [ ] Ho visto un caso concreto di overfitting con un modello complesso.
- [ ] Ho una nota che riassume le metriche più importanti e quando usarle.

### Errori tipici da evitare

- giudicare un modello solo da una metrica (es. solo accuracy).
- usare tutto il dataset per il training e testarlo sugli stessi dati.
- provare modelli sempre più complessi senza avere una baseline decente.
- confondere il training set con il test set quando si fanno esperimenti iterativi.
- non fissare un `random_state` quando si vuole riproducibilità.

### Segnali che “ho davvero capito” D05

- quando vedo un problema reale, so dire se è classificazione o regressione e che tipo di metrica ha senso.
- non ho più bisogno di “indovinare” parametri a caso: ho un minimo di metodo (baseline, CV, metriche).
- posso guardare un grafico di training vs validation loss/accuracy e riconoscere over/underfitting.
- sono in grado di spiegare il workflow ML standard a un collega non tecnico usando esempi del mio progetto.

---

## 8. Come ripartire dopo una pausa

Se torno su D05 dopo giorni o settimane:

1. Riapro uno degli script/notebook dei laboratori (Iris, regressione, overfitting).
2. Rieseguo tutto e controllo se capisco ancora cosa fa ogni step.
3. Scelgo un micro-miglioramento:
   - aggiungere una metrica
   - usare cross-validation invece di singolo split
   - provare un secondo modello e confrontarlo con il primo
4. Aggiorno una nota in `private/notes/` con:
   - quale esperimento ho rifatto
   - cosa ho consolidato o scoperto di nuovo

Scopo: trattenere i concetti **agganciandoli a esperimenti reali**, non solo alla teoria.

---

## 9. Risorse consigliate

### 9.1 scikit-learn (pratica ML in Python)

- **Getting Started con scikit-learn**  
  Introduzione ai concetti chiave (estimator API, fit/predict, dataset, ecc.).  
  https://scikit-learn.org/stable/getting_started.html  

- **User Guide**  
  Documentazione approfondita su modelli supervisionati, non supervisionati, pipeline, metriche e pitfalls.  
  https://scikit-learn.org/stable/user_guide.html  

- **Introduzione al ML con scikit-learn**  
  Tutorial pratico con esempi di classificazione (digits) e regressione.  
  https://scikit-learn.org/1.4/tutorial/basic/tutorial.html  

### 9.2 Corsi ML “classici”

- **Stanford CS229 — Machine Learning**  
  Corso graduate di riferimento su ML classico, con note e materiali disponibili.  
  Sito corso / syllabus: https://cs229.stanford.edu/  
  Panoramica e contenuti online:  
  https://see.stanford.edu/Course/CS229/37  
  https://online.stanford.edu/courses/cs229-machine-learning  

### 9.3 Libri (grad-level e più accessibili)

- **The Elements of Statistical Learning (ESL)** — Hastie, Tibshirani, Friedman  
  Testo classico, free PDF, copre metodi statistici per ML classico (regressione, SVM, random forest, ecc.).  
  Sito ufficiale e PDF:  
  https://hastie.su.domains/ElemStatLearn/  

- **Introduction to Statistical Learning (ISLR)**  
  Versione più accessibile di ESL, anche questa con risorse online.  
  Info e materiali:  
  https://www.statlearning.com/  

- **Guida alla lettura di ESL** (TheoremPath)  
  Suggerimenti su quali capitoli leggere in base agli obiettivi.  
  https://theorempath.com/topics/elements-of-statistical-learning-book  

Queste risorse non vanno esaurite tutte: D05 serve a darti una mappa e gli “hook” giusti
per approfondire in D06 e oltre, senza perdersi in teoria astratta.


### Strumenti Visivi e Animazioni Esterne (Web)
- **[MLU-Explain: Logistic Regression](https://mlu-explain.github.io/logistic-regression/)**: **Come usarlo**: fai scorrere la pagina (scrollytelling) per vedere fisicamente la retta lineare piegarsi in una curva sigmoide per adattarsi ai dati di classificazione.
- **[TensorFlow Playground](https://playground.tensorflow.org/)**: **Come usarlo**: per capire la classificazione lineare, azzera gli strati nascosti (hidden layers a 0) e prova a separare il dataset a due blob.
