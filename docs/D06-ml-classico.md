---
aliases: [D06, Alberi Decisionali, Random Forest, XGBoost, Gradient Boosting, Machine Learning Tabellare]
---
# Machine Learning Classico (Alberi, Random Forest e XGBoost)

Il Machine Learning applicato ai dati tabellari strutturati è dominato dalla famiglia degli alberi decisionali e dei loro ensemble avanzati: Random Forest e Gradient Boosting. Mentre le architetture neurali profonde eccellono su dati percettivi non strutturati come immagini, segnali audio e sequenze testuali, i modelli basati su alberi rappresentano lo standard industriale per accuratezza, robustezza e velocità di convergenza su tabelle relazionali e dataset numerici o categorici. Operano partizionando ricorsivamente lo spazio delle feature mediante iperpiani ortogonali, combinando centinaia o migliaia di stimatori per massimizzare la capacità predittiva e controllare rigorosamente il compromesso tra bias e varianza.

## Il Problema dei Modelli Lineari e la Soluzione ad Albero

I modelli lineari tradizionali, come la regressione lineare e la regressione logistica, tentano di separare le classi o stimare i valori continui proiettando un singolo iperpiano nello spazio euclideo. Quando le relazioni tra variabili predittive e target presentano forti non-linearità, discontinuità o interazioni complesse (ad esempio soglie condizionali in cui una feature è rilevante solo se un'altra assume un intervallo specifico), un iperpiano rigido fallisce inevitabilmente, incorrendo in un grave errore di underfitting (alto bias).

### Partizionamento Ortogonale dello Spazio (Decision Tree)

Per catturare frontiere di decisione arbitrarie senza imporre ipotesi parametriche globali, l'**Albero Decisionale** (`DecisionTreeClassifier` e `DecisionTreeRegressor` in [Scikit-learn](https://scikit-learn.org/)) adotta una strategia di partizionamento ricorsivo dello spazio (*recursive binary splitting*). L'algoritmo analizza l'intero dataset alla radice e seleziona in modo ingordo (*greedy*) la feature $j$ e la soglia di taglio $t$ che massimizzano la purezza dei due sottoinsiemi generati, tagliando lo spazio con un iperpiano ortogonale all'asse della variabile selezionata.

Nei problemi di classificazione con $C$ classi, l'omogeneità di un nodo viene quantificata tramite la **Gini Impurity** ($I_G$) oppure l'**Entropia di Shannon** ($H$):

$$I_G(p) = 1 - \sum_{i=1}^C p_i^2$$

$$H(p) = -\sum_{i=1}^C p_i \log_2(p_i)$$

dove $p_i$ rappresenta la proporzione di campioni appartenenti alla classe $i$ nel nodo corrente. L'algoritmo valuta ogni possibile split calcolando l'**Information Gain** (riduzione dell'impurità):

$$\Delta I = I(D_{\text{padre}}) - \left( \frac{|D_L|}{|D|} I(D_L) + \frac{|D_R|}{|D|} I(D_R) \right)$$

Il processo si ripete ricorsivamente su ciascun sotto-nodo finché non viene soddisfatto un criterio di arresto (come il raggiungimento della purezza totale o una profondità massima prefissata). Nei compiti di regressione, il criterio di partizionamento sostituisce l'impurità con la minimizzazione dell'errore quadratico medio (MSE) rispetto alla media locale del nodo.

## Il Rischio di Memorizzazione del Rumore e la Risposta Ensembling

L'albero decisionale isolato soffre di un'intrinseca instabilità strutturale: piccole variazioni nei dati di training possono alterare drasticamente il primo split alla radice, propagando cambiamenti a cascata lungo tutti i rami sottostanti. Se lasciato crescere senza vincoli di regolarizzazione, l'albero continuerà a ramificare fino a isolare ogni singolo punto di addestramento in una foglia dedicata, memorizzando il rumore statistico e le oscillazioni casuali del campione anziché la funzione generatrice sottostante.

Questo comportamento genera un modello ad **altissima varianza** e forte **overfitting**: l'errore sul set di addestramento si annulla, ma la capacità di generalizzazione su dati non visti degrada catastroficamente.

### Riduzione della Varianza tramite Bagging (Random Forest)

Per neutralizzare l'alta varianza senza reintrodurre il bias dei modelli rigidi, la tecnica del **Bagging** (*Bootstrap Aggregating*, introdotta da [Leo Breiman](https://www.stat.berkeley.edu/~breiman/) nel 2001) costruisce un comitato di alberi indipendenti e aggrega le loro predizioni. L'algoritmo di riferimento per questa strategia è la **Random Forest** (`RandomForestClassifier` in [Scikit-learn](https://scikit-learn.org/)).

La Random Forest introduce una doppia fonte di stocasticità per decorrelare i singoli stimatori:
In primo luogo, ogni albero viene addestrato su un campione bootstrap generato estraendo con reimmissione $n$ istanze dal dataset originale, garantendo che circa il 63.2% delle osservazioni uniche sia presente nel set di addestramento mentre il restante 36.8% formi il set *Out-Of-Bag* (OOB), utilizzabile per la validazione interna. In secondo luogo, a ogni singolo split, l'albero non valuta tutte le $d$ variabili disponibili, ma un sottoinsieme casuale di dimensione ridotta ($m \approx \sqrt{d}$ per la classificazione, $m \approx d/3$ per la regressione).

Matematicamente, se aggreghiamo $B$ alberi con varianza individuale $\sigma^2$ e correlazione a coppie $\rho$, la varianza della predizione media $\bar{X} = \frac{1}{B}\sum_{b=1}^B X_b$ risulta:

$$\text{Var}(\bar{X}) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$

Al crescere del numero di alberi ($B \to \infty$), il secondo termine si annulla e la varianza totale dell'ensemble converge al limite inferiore $\rho \sigma^2$. Il campionamento casuale delle feature riduce attivamente la correlazione $\rho$, consentendo alla foresta di abbattere la varianza complessiva mantenendo inalterato il basso bias dei singoli alberi profondi.

## Riduzione Sequenziale del Bias: Il Gradient Boosting

Mentre il Bagging allena stimatori ad alta capacità in parallelo per ridurne la varianza, esistono contesti operativi in cui i singoli modelli sono troppo semplici (alto bias) o necessitano di una convergenza guidata su residui complessi. In questi scenari, la strategia vincente è il **Boosting**, che costruisce una sequenza deterministica di stimatori deboli (*weak learners*), ciascuno dedicato a correggere gli errori residui commessi dai predecessori.

### Ottimizzazione nello Spazio delle Funzioni (Gradient Boosted Trees)

Nel **Gradient Boosting** (formalizzato da [Jerome Friedman](https://hastie.su.domains/) nel 2001), l'addestramento dell'ensemble viene formulato come una discesa del gradiente nello spazio delle funzioni per minimizzare una funzione di perdita differenziabile $L(y, f(x))$.

Il modello inizia con una stima costante iniziale $f_0(x) = \arg\min_\gamma \sum_{i=1}^n L(y_i, \gamma)$. A ogni iterazione $m = 1, \dots, M$, l'algoritmo calcola i residui pseudo-gradiente per ciascun campione $i$:

$$r_{im} = -\left[ \frac{\partial L(y_i, f(x_i))}{\partial f(x_i)} \right]_{f=f_{m-1}}$$

Un nuovo albero decisionale $h_m(x)$ viene addestrato non sui target originali $y_i$, ma per fittare i vettori dei residui $r_{im}$. L'output del nuovo albero viene scalato tramite un parametro di regolarizzazione chiamato **learning rate** o shrinkage ($\eta \in (0, 1]$) e sommato al modello globale:

$$f_m(x) = f_{m-1}(x) + \eta \gamma_m h_m(x)$$

Lo shrinkage costringe ogni albero a compiere passi microscopici lungo la direzione del gradiente negativo, prevenendo l'overfitting immediato e garantendo una convergenza progressiva e altamente accurata.

## Scalabilità Computazionale: XGBoost, LightGBM e CatBoost

Il Gradient Boosting classico calcolato in modo esatto richiede la scansione esaustiva di tutte le feature ordinate per identificare la soglia ottimale di ogni split, un'operazione computazionalmente proibitiva su dataset industriali con milioni di record. Per superare questa barriera prestazionale, la ricerca ha sviluppato motori di calcolo altamente ottimizzati a livello hardware.

### Ingegneria dei Sistemi per il Gradient Boosting

La libreria [XGBoost](https://xgboost.readthedocs.io/) (eXtreme Gradient Boosting, sviluppata da Tianqi Chen) ha rivoluzionato il machine learning tabellare introducendo l'approssimazione di Taylor al secondo ordine della funzione di perdita:

$$\tilde{L}^{(m)} \approx \sum_{i=1}^n \left[ g_i f_m(x_i) + \frac{1}{2} h_i f_m^2(x_i) \right] + \Omega(f_m)$$

dove $g_i = \partial_{\hat{y}} L(y_i, \hat{y})$ e $h_i = \partial^2_{\hat{y}} L(y_i, \hat{y})$ rappresentano rispettivamente il gradiente del primo e secondo ordine, mentre $\Omega(f_m) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$ penalizza esplicitamente il numero di foglie $T$ e la magnitudo dei pesi $w$. XGBoost implementa strutture dati *Compressed Column* (CSC) pre-ordinate in memoria RAM e algoritmi di quantizzazione approssimata per quantili ponderati.

Il framework [LightGBM](https://lightgbm.readthedocs.io/) (sviluppato da [Microsoft](https://www.microsoft.com/)) ottimizza ulteriormente il throughput mediante la discretizzazione continua in istogrammi a 256 bin (*Histogram-based splitting*), l'esclusione di feature mutualmente esclusive (*Exclusive Feature Bundling*, EFB) e il campionamento selettivo delle istanze con gradienti più ampi (*Gradient-based One-Side Sampling*, GOSS). Inoltre, LightGBM adotta una strategia di crescita dell'albero *leaf-wise* (espandendo prima la foglia con massimo guadagno) anziché *depth-wise* (livello per livello), massimizzando la riduzione dell'errore a parità di nodi.

La libreria [CatBoost](https://catboost.ai/) (sviluppata da Yandex) si focalizza sulla gestione nativa e rigorosa delle variabili categoriche ad alta cardinalità tramite *Target Statistics* ordinate nel tempo, eliminando il fenomeno del *target leakage*, e costruisce alberi simmetrici (*oblivious trees*) che velocizzano drasticamente la fase di inferenza in produzione.

## Interpretabilità e Ispezione del Modello (Feature Importance)

Quando un modello di Machine Learning aggrega migliaia di regole decisionali distribuite su centinaia di alberi profondi, perde la trasparenza analitica immediata dei modelli lineari, trasformandosi in una complessa scatola nera. Per soddisfare i requisiti di verificabilità e conformità regolatoria nei settori ad alto impatto (come il credito, la diagnostica medica e la sicurezza), è necessario disporre di metodologie matematiche per quantificare il contributo di ogni singola variabile.

### Metriche di Rilevanza delle Variabili

La metrica classica **Mean Decrease in Impurity** (MDI, o *Gini Importance*) calcola il miglioramento medio ponderato dell'indice di Gini (o dell'MSE) apportato da tutti gli split che hanno utilizzato una specifica variabile $j$ lungo l'intera foresta. Sebbene computazionalmente istantanea, la MDI soffre di un noto bias statistico a favore di feature continue o categoriche ad alta cardinalità.

La metrica **Permutation Importance** (Mean Decrease in Accuracy, MDA) supera questo limite valutando il modello su un set di validazione non visto: i valori della feature $j$ vengono mescolati casualmente (rompendo la correlazione con il target) e si misura il calo percentuale delle prestazioni predittive. Se la distruzione dell'ordine di una variabile produce un crollo drammatico dell'accuratezza, quella feature è cruciale per la logica decisionale del modello. Nelle pipeline moderne, queste metriche vengono integrate dai valori SHAP (*SHapley Additive exPlanations*), basati sulla teoria dei giochi cooperativi, per attribuire a ogni feature un impatto marginale locale coerente e additivo.

## Trade-off e Scelte Operative

L'impiego operativo dei modelli basati su alberi richiede un bilanciamento consapevole tra risorse computazionali, rischio di memorizzazione del rumore e latenza di inferenza:

La complessità strutturale dei singoli alberi deve essere controllata bilanciando `max_depth`, `min_samples_leaf` e il parametro di potatura basato sul costo-complessità `ccp_alpha`. Alberi troppo profondi aumentano esponenzialmente il consumo di memoria RAM durante il salvataggio dei pesi e rendono il modello fragile di fronte a distribuzioni di dati instabili.

La scelta architetturale tra Bagging (Random Forest) e Boosting (XGBoost / LightGBM) dipende dalla natura del dataset e dai vincoli infrastrutturali: Random Forest scala in modo perfettamente parallelo su tutti i core CPU disponibili e tollera elevati livelli di rumore nelle etichette senza richiedere una calibrazione maniacale degli iperparametri. Al contrario, Gradient Boosting raggiunge prestazioni predittive nettamente superiori sui segnali deboli ma richiede un'attenta regolarizzazione del learning rate, l'implementazione dell'early stopping e un monitoraggio costante per evitare la memorizzazione degli outlier.

La velocità di training e il footprint di memoria vedono LightGBM e CatBoost dominare su dataset di grandi dimensioni grazie alla discretizzazione in istogrammi, mentre XGBoost offre il controllo più granulare sulle penalizzazioni matematiche L1/L2 e sull'integrazione hardware specializzata.

## Riferimenti Bibliografici e Risorse Tecniche

La letteratura fondamentale e le implementazioni di riferimento per il machine learning basato su alberi includono trattati teorici, librerie open-source e simulatori visivi.

### Fondamenti Teorici e Manuali di Riferimento
Lo studio accademico di riferimento per gli alberi decisionali, il Bagging e il Gradient Boosting è [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) (il testo accademico fondamentale scritto dai docenti della [Stanford University](https://www.stanford.edu/) [Trevor Hastie](https://hastie.su.domains/), [Robert Tibshirani](https://tibshirani.su.domains/) e [Jerome Friedman](https://hastie.su.domains/)). Per una panoramica operativa completa sull'implementazione standard in [Python](https://www.python.org/), la documentazione di riferimento è [Scikit-Learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html).

### Framework di Produzione
Per il deployment su larga scala e l'addestramento distribuito, le risorse ufficiali primarie sono la [Documentazione Ufficiale di XGBoost](https://xgboost.readthedocs.io/en/stable/), il portale di [LightGBM](https://lightgbm.readthedocs.io/) e la documentazione del framework [CatBoost](https://catboost.ai/).

### Strumenti Visivi e Risorse Didattiche
Per esplorare geometricamente come gli algoritmi partizionano lo spazio e come l'aggregazione smussa le superfici di decisione, la piattaforma didattica [MLU-Explain](https://mlu-explain.github.io/) di [Amazon](https://www.amazon.science/) mette a disposizione i simulatori interattivi [Decision Trees](https://mlu-explain.github.io/decision-tree/) e [Random Forest](https://mlu-explain.github.io/random-forest/). Inoltre, il canale divulgativo [StatQuest](https://statquest.org/) dell'informatico [Josh Starmer](https://statquest.org/) offre analisi visive dettagliate sui passaggi matematici del gradient boosting e sul calcolo dei residui.

## Appendice Operativa: Laboratori Pratici

I laboratori seguenti forniscono script Python completi, eseguibili e autocontenuti per riprodurre empiricamente il comportamento dei singoli alberi, l'effetto stabilizzante del bagging e la potenza ottimizzativa del gradient boosting.

### Laboratorio 1: Sovradimensionamento dell'Albero Singolo e Potatura

Questo script addestra un albero decisionale non vincolato su dati sintetici tabellari, evidenziando il divario di accuratezza tra training e test causato dall'overfitting, e mostra come la limitazione della profondità ristabilisca la capacità di generalizzazione.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1. Generazione del dataset sintetico tabellare
X, y = make_classification(
    n_samples=2000,
    n_features=20,
    n_informative=12,
    n_redundant=4,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 2. Albero profondo non vincolato (overfitting puro)
unconstrained_tree = DecisionTreeClassifier(random_state=42)
unconstrained_tree.fit(X_train, y_train)

train_acc_unconstrained = accuracy_score(y_train, unconstrained_tree.predict(X_train))
test_acc_unconstrained = accuracy_score(y_test, unconstrained_tree.predict(X_test))

# 3. Albero regolarizzato tramite profondità massima
regularized_tree = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10, random_state=42)
regularized_tree.fit(X_train, y_train)

train_acc_reg = accuracy_score(y_train, regularized_tree.predict(X_train))
test_acc_reg = accuracy_score(y_test, regularized_tree.predict(X_test))

print(f"Albero non vincolato - Profondita': {unconstrained_tree.get_depth()} nodi")
print(f"  Train Accuracy: {train_acc_unconstrained * 100:.2f}% | Test Accuracy: {test_acc_unconstrained * 100:.2f}%")
print(f"Albero regolarizzato - Profondita': {regularized_tree.get_depth()} nodi")
print(f"  Train Accuracy: {train_acc_reg * 100:.2f}% | Test Accuracy: {test_acc_reg * 100:.2f}%")
```

### Laboratorio 2: La Saggezza della Folla con Random Forest e Feature Importance

Questo script dimostra come l'aggregazione di stimatori decorrelati abbatta la varianza del modello, ed estrae i pesi di importanza delle feature per identificare le variabili predittive dominanti.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Creazione dataset con feature informative e rumore
X, y = make_classification(
    n_samples=2500,
    n_features=15,
    n_informative=6,
    n_redundant=2,
    n_classes=2,
    random_state=42
)

feature_names = [f"feature_{i:02d}" for i in range(X.shape[1])]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 2. Addestramento Random Forest con 150 stimatori
rf_model = RandomForestClassifier(
    n_estimators=150,
    max_features="sqrt",
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
rf_model.fit(X_train, y_train)

# 3. Valutazione e punteggio Out-Of-Bag
y_pred = rf_model.predict(X_test)
print(f"Punteggio Out-Of-Bag (OOB Score): {rf_model.oob_score_ * 100:.2f}%")
print("\nReport di Classificazione sul Test Set:")
print(classification_report(y_test, y_pred, digits=4))

# 4. Estrazione della Feature Importance (Mean Decrease in Impurity)
importances = pd.Series(rf_model.feature_importances_, index=feature_names)
top_features = importances.sort_values(ascending=False)

print("Top 5 Feature piu' rilevanti:")
print(top_features.head(5).to_string())
```

### Laboratorio 3: Ottimizzazione e Early Stopping con XGBoost

Questo script implementa una pipeline di classificazione ad alte prestazioni con XGBoost, impiegando la regolarizzazione L2, il learning rate ridotto e l'early stopping per prevenire la sovra-ottimizzazione sui residui.

```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, log_loss

# 1. Generazione di un dataset tabellare su larga scala
X, y = make_classification(
    n_samples=10000,
    n_features=30,
    n_informative=18,
    n_classes=2,
    random_state=42
)

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# 2. Configurazione e addestramento del modello XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_lambda=1.5,
    early_stopping_rounds=30,
    eval_metric="logloss",
    random_state=42
)

# 3. Addestramento con monitoraggio sul set di validazione
xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_val, y_val)],
    verbose=False
)

# 4. Valutazione sul set di test indipendente
best_iter = xgb_model.best_iteration
y_probs = xgb_model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_probs)
test_loss = log_loss(y_test, y_probs)

print(f"Migliore iterazione trovata: {best_iter}")
print(f"Test ROC-AUC: {auc_score:.4f} | Test Log-Loss: {test_loss:.4f}")
```
