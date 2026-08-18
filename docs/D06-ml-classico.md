# D06 — Machine Learning classico: alberi, ensemble e gradient boosting

## Meta-modulo D06

**Target**  
Me stesso oggi, e chiunque voglia capire e usare i modelli ML “classici” più potenti su dati tabellari:
alberi decisionali, random forest, gradient boosting (XGBoost/LightGBM/CatBoost), con consapevolezza
di come funzionano, quando usarli e come non farsi ingannare dalle metriche.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D03 — Data foundations (NumPy, Pandas, SQL, data quality)
- D04 — Matematica e statistica just-in-time
- D05 — Fondamenti di Machine Learning (workflow supervised, scikit-learn, metriche, overfitting)

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - idea di albero decisionale, split, impurity  
  - concetto di ensemble (bagging vs boosting)  
  - uso di RandomForest e GradientBoosting in scikit-learn

- **Modalità standard (~8–10 ore)**  
  - confronto tra Random Forest, Gradient Boosting, XGBoost  
  - tuning di iperparametri base  
  - error analysis su dataset tabellari reali

- **Modalità deep dive (più giornate)**  
  - studio di capitoli selezionati di ISLR/ESL su alberi/boosting  
  - implementazione di pipeline complete con cross-validation e tuning  
  - confronto tra librerie (scikit-learn, XGBoost, LightGBM)

**Quando considerare il modulo “completato”**

- so spiegare a parole mie come funziona un albero decisionale e perché un ensemble è più robusto
- so usare RandomForest e GradientBoosting in scikit-learn e XGBoost in Python
- so fare tuning di base e interpretare feature importance
- ho almeno un progetto che usa questi modelli su un dataset reale (classificazione o regressione)

---

## Perché questo documento

Dopo D05 (ML base) serve un passo in più: capire i **modelli più usati in pratica su dati tabellari**:

- alberi decisionali: modelli interpretabili, base per ensemble
- Random Forest: bagging di alberi, robusto, buona baseline
- Gradient Boosting / XGBoost / LightGBM / CatBoost: modelli ad alte prestazioni, spesso molto competitivi sui dati tabellari strutturati; la scelta dipende da dataset, preprocessing, metrica, vincoli operativi e confronto sperimentale con altri modelli

Questo modulo è il ponte verso:

- D07 (apprendimento non supervisionato) → per clustering, riduzione dimensionale e analisi esplorativa
- D08 (Deep Learning e PyTorch) → quando i dati non sono tabellari (immagini, testo, sequenze)
- D09/D10 (LLM, RAG) → quando la rappresentazione è testuale e semantica

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere come un albero decisionale prende decisioni (split, impurity, profondità)
- distinguere bagging (Random Forest) e boosting (Gradient Boosting, XGBoost)
- usare RandomForest, GradientBoosting e XGBoost in Python
- interpretare feature importance e limiti di queste misure
- fare tuning di base e capire quando un modello è troppo complesso per i dati

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Alberi decisionali: struttura, split, impurity, overfitting.
2. Ensemble methods: bagging, boosting, stacking.
3. Random Forest: bootstrap aggregating di alberi.
4. Gradient Boosting: correzione sequenziale degli errori.
5. XGBoost / LightGBM / CatBoost: ottimizzazioni e differenze pratiche.
6. Feature importance e interpretazione.

---

## 2. Alberi decisionali

### 2.1 Come funziona un albero

Un albero decisionale:

- divide i dati con **split** basati su condizioni del tipo “feature X ≤ soglia?”
- ogni split cerca di rendere i sottoinsiemi più “puri” rispetto al target
- criteri comuni:
  - classificazione: Gini impurity, entropy
  - regressione: varianza ridotta

Problema tipico:

- alberi profondi tendono a **overfittare** (memorizzano il training set)

Contromisure:

- limitare `max_depth`
- richiedere un minimo di campioni per split/foglia
- pruning (post-training o pre-pruning)

---

## 3. Ensemble methods: bagging e boosting

### 3.1 Bagging (Bootstrap Aggregating)

Idea:

- addestrare molti modelli indipendenti su sottoinsiemi diversi (con ripetizione) dei dati
- aggregare le predizioni (media per regressione, voto per classificazione)

Effetto:

- riduce la **varianza** senza aumentare troppo il bias
- Random Forest è l’esempio più famoso di bagging applicato ad alberi.

Riferimenti:

- [scikit-learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)

### 3.2 Boosting

Idea:

- addestrare modelli in **sequenza**, ognuno cerca di correggere gli errori del precedente
- ogni nuovo modello pesa di più gli esempi sbagliati dal modello precedente

Effetto:

- può ridurre il bias rispetto a modelli molto semplici, ma la sua varianza e il rischio
  di overfitting dipendono da profondità, numero di alberi, learning rate, regolarizzazione
  e qualità dei dati
- Gradient Boosting e XGBoost sono esempi di boosting basato su alberi.

Riferimenti:

- [scikit-learn Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting)
- [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/)

---

## 4. Random Forest

### 4.1 Concetto

Random Forest:

- costruisce molti alberi decisionali
- ogni albero vede:
  - un bootstrap sample dei dati
  - un sottoinsieme casuale delle feature ad ogni split

Risultato:

- ensemble robusto, spesso migliore di un singolo albero
- meno sensibile a rumore e outlier

In scikit-learn:

- `RandomForestClassifier`, `RandomForestRegressor`
- parametri chiave: `n_estimators`, `max_depth`, `max_features`, `min_samples_leaf`

Riferimenti:

- [Random Forest in scikit-learn](https://scikit-learn.org/stable/modules/ensemble.html#forest)

### 4.2 Quando usarlo

- buona baseline per problemi tabellari
- quando serve un modello robusto senza tuning estremo
- quando l’interpretabilità parziale (feature importance) è utile

---

## 5. Gradient Boosting e XGBoost

### 5.1 Gradient Boosting (GBDT)

Idea:

- ogni nuovo albero approssima il **gradiente della loss** rispetto alle predizioni correnti
- in pratica: ogni albero cerca di correggere gli errori residui del modello precedente

In scikit-learn:

- `GradientBoostingClassifier`, `GradientBoostingRegressor`
- parametri chiave: `n_estimators`, `learning_rate`, `max_depth`, `subsample`

Riferimenti:

- [Gradient Boosting in scikit-learn](https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting)

### 5.2 XGBoost (e cenni a LightGBM/CatBoost)

XGBoost:

- implementazione ottimizzata di gradient boosting
- caratteristiche:
  - regolarizzazione esplicita (L1/L2)
  - gestione efficiente di dati sparsi
  - parallelizzazione e ottimizzazioni per velocità

Librerie correlate:

- **LightGBM**: enfasi su velocità e dataset grandi
- **CatBoost**: gestione nativa di feature categoriche

In Python:

- uso tipico con API simile a scikit-learn (`XGBClassifier`, `XGBRegressor`)
- parametri chiave: `n_estimators`, `learning_rate`, `max_depth`, `subsample`, `colsample_bytree`

Riferimenti:

- [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/)
- [LightGBM documentation](https://lightgbm.readthedocs.io/en/stable/)
- [CatBoost documentation](https://catboost.ai/en/docs/)

---

## 6. Feature importance e interpretazione

### 6.1 Feature importance negli alberi/ensemble

Tipi comuni:

- **Gini importance** (o “impurity-based”): quanto ogni feature riduce l’impurity media negli split
- **Permutation importance**: quanto peggiora la performance se si “rompe” una feature (shuffling)

Avvertenze:

- feature correlate possono “dividersi” l’importanza
- scale diverse e leakage possono distorcere l’interpretazione

Buona pratica:

- usare permutation importance come controllo aggiuntivo
- non fidarsi ciecamente della ranking di importance per decisioni critiche

Riferimenti:

- [Permutation importance in scikit-learn](https://scikit-learn.org/stable/modules/permutation_importance.html)

---

## 7. Laboratori ed esercizi

### Laboratorio 1 — Primo albero decisionale

**Obiettivo:** capire come un albero prende decisioni.

**Passi:**

1. Scegliere un dataset di classificazione o regressione (es. `iris`, `diabetes`, o un CSV proprio).
2. Splittare in train/test.
3. Addestrare un `DecisionTreeClassifier` o `DecisionTreeRegressor`.
4. Visualizzare l’albero (es. con `plot_tree` o export in testo).
5. Annotare:
   - quali feature vengono usate per primi split
   - profondità dell’albero
   - segnali di overfitting (es. training accuracy molto alta, test più bassa)

**Deliverable:**

- script/notebook con albero addestrato
- nota con interpretazione degli split e valutazione overfitting

---

### Laboratorio 2 — Random Forest vs albero singolo

**Obiettivo:** vedere l’effetto del bagging.

**Passi:**

1. Usare lo stesso dataset del laboratorio 1.
2. Addestrare:
   - un albero decisionale
   - una Random Forest con parametri ragionevoli
3. Confrontare:
   - training e test accuracy (o MSE per regressione)
   - feature importance nei due modelli
4. Annotare differenze e vantaggi dell’ensemble.

**Deliverable:**

- script/notebook con confronto
- nota che descrive cosa cambia passando da albero singolo a foresta

---

### Laboratorio 3 — Gradient Boosting e XGBoost

**Obiettivo:** confrontare boosting “vanilla” e XGBoost.

**Passi:**

1. Usare un dataset di dimensioni medie (es. `breast_cancer`, o un CSV con qualche migliaio di righe).
2. Addestrare:
   - `GradientBoostingClassifier` (scikit-learn)
   - `XGBClassifier` (XGBoost)
3. Fare tuning leggero (es. `n_estimators`, `learning_rate`, `max_depth`) con cross-validation.
4. Confrontare:
   - performance (accuracy, F1, AUC, ecc.)
   - tempi di training
5. Annotare pro/contro delle due librerie.

**Deliverable:**

- script/notebook con confronto
- nota su quale modello preferiresti per quel tipo di problema e perché

---

### Laboratorio 4 — Feature importance e error analysis

**Obiettivo:** interpretare il modello e capire dove sbaglia.

**Passi:**

1. Prendere il modello migliore tra quelli dei laboratori precedenti (RF, GB, XGB).
2. Calcolare:
   - feature importance (impurity-based)
   - (opzionale) permutation importance
3. Fare error analysis:
   - guardare esempi sbagliati nel test set
   - cercare pattern (es. certe classi più confuse, certi range di feature problematici)
4. Annotare:
   - quali feature sembrano davvero decisive
   - quali errori potrebbero essere dovuti a dati sporchi o leakage

**Deliverable:**

- script/notebook con importance ed error analysis
- nota che collega importance, errori e possibili miglioramenti nei dati

---

## 8. Rubriche e checklist

### Checklist — D06 completato

- [ ] So spiegare come funziona un albero decisionale (split, impurity, profondità).
- [ ] So distinguere bagging (Random Forest) e boosting (Gradient Boosting/XGBoost).
- [ ] Ho addestrato almeno un modello Random Forest e uno Gradient Boosting/XGBoost.
- [ ] Ho fatto tuning di base (almeno 2–3 parametri) con cross-validation.
- [ ] Ho interpretato feature importance e fatto almeno una semplice error analysis.
- [ ] Ho un progetto che usa questi modelli su un dataset reale (anche piccolo).

### Errori tipici da evitare

- usare alberi molto profondi senza controllo (overfitting garantito).
- fidarsi solo della accuracy senza guardare matrici di confusione o altre metriche.
- interpretare la feature importance come “verità assoluta” senza considerare correlazioni e leakage.
- confrontare modelli su split diversi o senza fissare `random_state`.
- usare XGBoost/LightGBM senza capire prima le basi di boosting e gradient descent.

### Segnali che “ho davvero capito” D06

- quando vedo un problema tabellare, so dire se un Random Forest o un Gradient Boosting sono candidati ragionevoli.
- so spiegare a un collega perché un ensemble è più robusto di un singolo albero.
- non ho più bisogno di “provare a caso” parametri: ho un minimo di metodo (baseline, CV, tuning).
- so leggere un grafico di feature importance e collegarlo a ciò che so del dominio.

---

## 9. Come ripartire dopo una pausa

Se torno su D06 dopo giorni o settimane:

1. Riapro uno dei notebook dei laboratori (RF, GB, XGBoost).
2. Rieseguo training e valutazione per ricordare la struttura del codice.
3. Scelgo un micro-miglioramento:
   - aggiungere una metrica nuova
   - provare un altro dataset
   - fare un confronto più sistematico tra modelli
4. Aggiorno una nota in `private/notes/` con:
   - quale esperimento ho rifatto
   - cosa ho consolidato o scoperto di nuovo

Scopo: tenere salda l’idea che **alberi + ensemble sono strumenti pratici**, non solo teoria.

---

## 10. Risorse consigliate

### 10.1 scikit-learn: ensemble methods

- **Ensemble methods — scikit-learn User Guide**  
  Documentazione ufficiale su Random Forest, Gradient Boosting, AdaBoost, bagging, stacking.  
  https://scikit-learn.org/stable/modules/ensemble.html  

- **Ensemble examples — scikit-learn**  
  Esempi pratici di confronto tra Random Forest e Gradient Boosting, feature transformations con ensemble, ecc.  
  https://scikit-learn.org/stable/auto_examples/ensemble/index.html  

### 10.2 XGBoost e gradient boosting in pratica

- **Get Started with XGBoost**  
  Quickstart ufficiale con snippet per classificazione/regressione.  
  https://xgboost.readthedocs.io/en/stable/get_started.html  

- **What is XGBoost? (IBM Think)**  
  Introduzione chiara a XGBoost, differenze con Random Forest e boosting.  
  https://www.ibm.com/think/topics/xgboost  

- **XGBoost in Python from Start to Finish (StatQuest, video)**  
  Tutorial completo su XGBoost per classificazione, con tuning e cross-validation.  
  https://www.youtube.com/watch?v=GrJP9FLV3FE  

- **A Complete Introduction to XGBoost for Machine Learning Engineers (video)**  
  Corso sintetico su XGBoost per ML engineer.  
  https://www.youtube.com/watch?v=9nxJr8XzkcM  

- **Ensemble Methods in Scikit Learn (video)**  
  Panoramica su voting, bagging, AdaBoost, Random Forest e Gradient Boosting.  
  https://www.youtube.com/watch?v=NqdyfMbVo1Q  

### 10.3 Libri e capitoli su alberi/ensemble

- **Introduction to Statistical Learning (ISLR)**  
  Capitoli su alberi, bagging, boosting, SVM.  
  https://www-bcf.usc.edu/~gareth/ISL/  

- **The Elements of Statistical Learning (ESL)**  
  Trattazione più avanzata di alberi, random forest, boosting.  
  https://hastie.su.domains/ElemStatLearn/  

Queste risorse non vanno studiate per intero: D06 serve a darti una mappa operativa
per usare alberi ed ensemble in modo sensato, e a collegarti ai testi classici quando serve approfondire.