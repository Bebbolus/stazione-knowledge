---
aliases: [D05, ML Fondamenti, Machine Learning Classico, Scikit-Learn, Workflow ML]
---
# Fondamenti di Machine Learning e Metriche Diagnostiche

L'**apprendimento automatico classico** è la disciplina computazionale che ottimizza algoritmi predittivi direttamente da collezioni di dati empirici, identificando funzioni matematiche di mappatura senza richiedere la codifica manuale di regole deterministiche. Questa metodologia costituisce il nucleo operativo per compiti di classificazione binaria e multiclasse, stima quantitativa di grandezze continue e individuazione di pattern comportamentali in contesti industriali e di intelligence OSINT. La formalizzazione di un workflow rigoroso tramite [Scikit-learn](https://scikit-learn.org/) (la libreria open-source fondamentale in [Python](https://www.python.org/) per il machine learning classico, classificazione, regressione e validazione) garantisce l'isolamento metodologico delle fasi di addestramento e collaudo, prevenendo distorsioni da memorizzazione acritica e validando la capacità di generalizzazione statistica del sistema prima del rilascio in produzione.

## Il Paradosso della Memorizzazione e il Rischio di Overfitting

Nella progettazione di sistemi di intelligenza artificiale, l'errore metodologico più frequente consiste nel valutare l'efficacia di un modello impiegando i medesimi dati utilizzati per l'ottimizzazione dei parametri. Un modello ad elevata capacità espressiva (come un albero decisionale profondo o una rete complessa) può raggiungere un'accuratezza perfetta sul campione di addestramento semplicemente memorizzando le oscillazioni casuali e il rumore di misura del dataset, senza estrarre alcuna autentica regolarità della funzione generatrice sottostante.

Questa condizione genera una grave asimmetria tra prestazioni apparenti e comportamento operativo reale. Quando il sistema viene esposto a distribuzioni di dati non visti in ambiente di produzione, la presenza di elevata varianza statistica (*Overfitting*) provoca un crollo repentino delle metriche predittive. All'estremo opposto, l'adozione di un'architettura eccessivamente rigida e semplificata induce un errore sistematico costante (*Underfitting* o alto Bias), rendendo il modello incapace di catturare le non-linearità intrinseche del fenomeno.

La soluzione ingegneristica impone la rigorosa formalizzazione del ciclo di vita del dato, separando deterministicamente le partizioni di addestramento, validazione e test, e verificando costantemente il guadagno marginale rispetto a modelli di riferimento banali (*baseline*).

## Tassonomia dell'Apprendimento Automatico

I paradigmi algoritmici dell'apprendimento automatico si differenziano in base alla natura e alla disponibilità dei segnali informativi forniti durante la fase di fitting.

Nell'**Apprendimento Supervisionato**, l'algoritmo riceve una matrice di feature indipendenti $\mathbf{X} \in \mathbb{R}^{n \times d}$ accoppiata a un vettore di etichette target note $\mathbf{y} \in \mathbb{R}^n$. Il compito consiste nell'approssimare una funzione $f: \mathbf{X} \to \mathbf{y}$ che minimizzi una metrica di discrepanza attesa. Se il target $\mathbf{y}$ è costituito da categorie discrete, il problema si configura come **Classificazione**; se $\mathbf{y}$ è uno scalare continuo, il problema si definisce **Regressione**.

Nell'**Apprendimento Non Supervisionato**, il sistema analizza unicamente la matrice delle osservazioni $\mathbf{X}$ in assenza di etichette target, con l'obiettivo di individuare raggruppamenti geometrici naturali nello spazio latente (Clustering) o identificare sottospazi a dimensionalità ridotta che massimizzino la varianza conservata (Riduzione Dimensionale).

## L'Architettura del Workflow con Scikit-Learn

La libreria Scikit-Learn standardizza lo sviluppo di pipeline di machine learning attraverso un'interfaccia a oggetti omogenea basata sul pattern **Estimator**.

### Come funzionano gli Stimatori

Ogni modello implementa tre metodi fondamentali: `fit(X, y)` per l'ottimizzazione dei parametri interni sui dati di addestramento, `predict(X)` per l'inferenza predittiva su nuove matrici di feature, e `score(X, y)` per il calcolo della metrica di performance predefinita. Per i modelli probabilistici, il metodo `predict_proba(X)` restituisce le distribuzioni di probabilità calibrate per ciascuna classe target.

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Caricamento del dataset e partizionamento isolato
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Istanziazione stimatore conforme all'API Scikit-Learn
classificatore = LogisticRegression(max_iter=500, random_state=42)

# Fase 1: Addestramento sui dati di train
classificatore.fit(X_train, y_train)

# Fase 2: Inferenza predittiva e stima probabilistica sui dati di test
predizioni = classificatore.predict(X_test)
probabilita = classificatore.predict_proba(X_test)

# Fase 3: Valutazione accuratezza media
accuratezza_test = classificatore.score(X_test, y_test)

print("Accuratezza su Test Set isolato:", f"{accuratezza_test:.4f}")
print("Predizione prima istanza di test:", predizioni[0], "| Probabilita per classe:", np.round(probabilita[0], 3))
```

### Pipeline di Preprocessing e Prevenzione del Data Leakage

L'incapsulamento delle trasformazioni statistiche (standardizzazione numerica, codifica one-hot e imputazione dei valori nulli) all'interno di una `Pipeline` con `ColumnTransformer` garantisce che i parametri di riscalamento vengano appresi unicamente sui dati di training ed applicati passivamente al test set, eliminando qualsiasi rischio di data leakage.

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

dataset_demo = pd.DataFrame({
    "eta": [25.0, 45.0, np.nan, 35.0, 52.0, 23.0],
    "reddito": [30000.0, 85000.0, 50000.0, np.nan, 120000.0, 28000.0],
    "canale_acquisizione": ["WEB", "DIRETTO", "PARTNER", "WEB", "WEB", "PARTNER"],
    "ha_convertito": [0, 1, 0, 1, 1, 0]
})

X = dataset_demo[["eta", "reddito", "canale_acquisizione"]]
y = dataset_demo["ha_convertito"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Definizione trasformatori per colonne numeriche e categoriche
trasformatore_numerico = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

trasformatore_categorico = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessore = ColumnTransformer(transformers=[
    ("num", trasformatore_numerico, ["eta", "reddito"]),
    ("cat", trasformatore_categorico, ["canale_acquisizione"])
])

# Incapsulamento totale del workflow in una Pipeline integrata
pipeline_completa = Pipeline(steps=[
    ("preprocessor", preprocessore),
    ("classifier", LogisticRegression(random_state=42))
])

# Il fitting calcola le statistiche SOLO sui dati di train, evitando data leakage
pipeline_completa.fit(X_train, y_train)
accuratezza = pipeline_completa.score(X_test, y_test)
print(f"Pipeline addestrata con successo. Score di test: {accuratezza:.4f}")
```

### Validazione Incrociata (Cross-Validation)

Il partizionamento statico train/test può produrre stime instabili in presenza di dataset ridotti o distribuzioni disomogenee. La validazione incrociata $K$-Fold (e la sua variante `StratifiedKFold` per preservare il bilanciamento delle classi) partiziona il dataset in $K$ blocchi disgiunti, iterando l'addestramento $K$ volte in modo che ogni blocco funga a rotazione da set di test. La media e la deviazione standard dei punteggi forniscono una stima robusta dell'errore di generalizzazione atteso.

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X_sintetico, y_sintetico = make_classification(
    n_samples=1200, n_features=15, n_informative=8, random_state=42
)

modello_rf = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=100, random_state=42))

# Configurazione schema di validazione a 5 fold stratificati
cv_schema = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
punteggi_cv = cross_val_score(modello_rf, X_sintetico, y_sintetico, cv=cv_schema, scoring="accuracy")

print(f"Punteggi per ogni fold: {[round(p, 4) for p in punteggi_cv]}")
print(f"Accuratezza media CV:   {punteggi_cv.mean():.4f}")
print(f"Deviazione standard CV: {punteggi_cv.std():.4f}")
```


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D05-ml-fondamenti. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Trade-off Operativi e Diagnostica delle Prestazioni

La valutazione quantitativa di un modello richiede l'analisi comparativa rispetto a modelli ingenui di riferimento e l'impiego di metriche insensibili allo sbilanciamento delle classi.

### Bias contro Varianza e Curve di Apprendimento

Le curve di apprendimento (*Learning Curves*) tracciano l'andamento della metrica di performance al variare della dimensione del set di training. Se l'errore di addestramento e quello di validazione convergono entrambi su valori mediocri, il sistema è dominato da **Bias** (necessità di aumentare la complessità del modello o aggiungere nuove feature). Se invece sussiste un ampio divario (*Generalization Gap*) tra errore nullo in training ed errore elevato in validazione, il sistema è affetto da **Varianza** (necessità di regolarizzazione, riduzione delle feature o acquisizione di ulteriori campioni).

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve

dati_cifre = load_digits()
X_cifre, y_cifre = dati_cifre.data, dati_cifre.target

modelli_confronto = {
    "DecisionTree (Sottodimensionato, max_depth=2)": DecisionTreeClassifier(max_depth=2, random_state=42),
    "RandomForest (Ensemble Complesso, n_est=100)": RandomForestClassifier(n_estimators=100, random_state=42)
}

volumi_addestramento = np.linspace(0.2, 1.0, 5)

for etichetta, stimatore in modelli_confronto.items():
    dimensioni, score_train, score_val = learning_curve(
        stimatore, X_cifre, y_cifre, cv=5, train_sizes=volumi_addestramento, scoring="accuracy", random_state=42
    )
    acc_train_finale = score_train.mean(axis=1)[-1]
    acc_val_finale = score_val.mean(axis=1)[-1]
    generalization_gap = acc_train_finale - acc_val_finale
    
    print(f"Modello: {etichetta}")
    print(f"  Training Accuracy finale:   {acc_train_finale:.4f}")
    print(f"  Validation Accuracy finale: {acc_val_finale:.4f}")
    print(f"  Divario di Generalizzazione (Gap): {generalization_gap:.4f}\n")
```

### La Baseline e la Valutazione Multi-Metrica

In presenza di classi fortemente sbilanciate (come nell'individuazione di frodi o attacchi informatici con proporzione 99:1), la pura *Accuracy* risulta fuorviante, poiché un classificatore banale che predice costantemente la classe maggioritaria otterrebbe il 99% di accuratezza senza alcun valore informativo.

L'impiego di `DummyClassifier` formalizza la baseline ingenua di confronto. Le prestazioni effettive vengono quantificate mediante la matrice di confusione, la **Precision** ($\frac{\text{TP}}{\text{TP} + \text{FP}}$), la **Recall** ($\frac{\text{TP}}{\text{TP} + \text{FN}}$), l'**F1-Score** (media armonica tra precision e recall) e l'area sotto la curva ROC (**ROC-AUC**), che misura la capacità del modello di discriminare tra le classi a qualsiasi soglia di confidenza.

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

X_dati, y_dati = make_classification(
    n_samples=1000, n_features=20, weights=[0.90, 0.10], random_state=42
)
X_tr, X_te, y_tr, y_te = train_test_split(X_dati, y_dati, test_size=0.25, random_state=42, stratify=y_dati)

# 1. Definizione Baseline Ingenua (Maggioranza di Classe)
baseline_dummy = DummyClassifier(strategy="most_frequent")
baseline_dummy.fit(X_tr, y_tr)
print(f"Accuratezza Baseline Ingenua: {baseline_dummy.score(X_te, y_te):.4f}")

# 2. Modello Logistico
modello_logistico = LogisticRegression(random_state=42)
modello_logistico.fit(X_tr, y_tr)
y_pred = modello_logistico.predict(X_te)
y_proba = modello_logistico.predict_proba(X_te)[:, 1]

print("\nMatrice di Confusione:")
print(confusion_matrix(y_te, y_pred))

print("\nReport Dettagliato di Classificazione (Precision, Recall, F1):")
print(classification_report(y_te, y_pred, target_names=["Classe Negativa", "Classe Positiva"]))

print(f"Area Sotto la Curva ROC (ROC-AUC): {roc_auc_score(y_te, y_proba):.4f}")
```

## Riferimenti Bibliografici e Risorse Tecniche

### Documentazione Ufficiale e Trattati Fondamentali

La risorsa primaria per l'architettura dei moduli e la parametrizzazione degli stimatori è la [Scikit-Learn User Guide](https://scikit-learn.org/stable/user_guide.html). La trattazione teorica rigorosa della teoria dell'apprendimento statistico è approfondita nel testo [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) (il trattato di riferimento per la teoria statistica del machine learning scritto dai docenti di [Stanford University](https://www.stanford.edu/) [Trevor Hastie](https://hastie.su.domains/) e [Robert Tibshirani](https://tibshirani.su.domains/)).

### Strumenti Interattivi e Piattaforme di Simulazione

Per l'esplorazione geometrica delle superfici decisionali e della convergenza dei classificatori lineari, consultare la piattaforma [MLU-Explain](https://mlu-explain.github.io/) (la piattaforma educativa interattiva sviluppata da [Amazon](https://www.amazon.science/) per la spiegazione visiva degli algoritmi di machine learning). L'analisi visiva delle frontiere di separazione neurale può essere condotta tramite la sandbox open-source [TensorFlow](https://www.tensorflow.org/) (la piattaforma open-source end-to-end per l'apprendimento automatico sviluppata da [Google](https://about.google/)) nel suo strumento interattivo [TensorFlow Playground](https://playground.tensorflow.org/).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



- [ ] Classificazione con partizionamento stratificato: Importare il dataset standard Iris da `sklearn.datasets`, suddividere i dati con `train_test_split` mantenendo la stratificazione delle classi, addestrare un modello di regressione logistica multinominale, calcolare la matrice di confusione e analizzare gli errori di predizione su ciascuna classe.
- [ ] Pipeline di preprocessing e classificazione integrata: Costruire una pipeline completa con `ColumnTransformer` contenente imputazione dei valori nulli e standardizzazione delle variabili continue, addestrare lo stimatore su dati eterogenei e verificare la totale assenza di data leakage tra train e test.
- [ ] Diagnostica delle curve di apprendimento: Implementare la funzione `learning_curve` su un modello a bassa capacità (DecisionTree con limitazione di profondità) e su un modello ad alta capacità (RandomForest non vincolato), plottando o stampando l'andamento del generalization gap al crescere delle istanze di training.
- [ ] Valutazione multi-metrica su dataset sbilanciato: Generare un dataset sintetico con sbilanciamento di classe 90:10, definire una baseline con `DummyClassifier`, addestrare un classificatore logistico e calcolare il report completo comprensivo di Precision, Recall, F1-Score e ROC-AUC.
