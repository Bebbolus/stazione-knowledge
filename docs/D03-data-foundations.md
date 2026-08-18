# D03 — Data foundations: NumPy, Pandas, SQL e data quality

## Meta-modulo D03

**Target**  
Me stesso oggi, e in futuro chiunque voglia lavorare con dati per ML, LLM, OSINT
senza diventare “data engineer puro”, ma con abbastanza solidità da:

- leggere, pulire e trasformare dataset
- capire cosa significano shape e tipi
- riconoscere problemi di data quality e leakage

**Prerequisiti consigliati**

- aver completato D02 (Python refresher e software engineering essentials)
- sapersela cavare con:
  - strutture dati Python (`list`, `dict`, `Path`)
  - lettura/scrittura file (testo, JSON/JSONL)
  - uso base del terminale e ambiente Python

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - concetti base di NumPy (array, shape, broadcasting a grandi linee)  
  - uso di Pandas per caricare CSV e fare operazioni semplici  
  - rudimenti di SELECT/WHERE/JOIN in SQL  
  - intuizione di data quality/leakage

- **Modalità standard (~8–10 ore)**  
  - esercizi con NumPy + Pandas (manipolazione tabelle reali)  
  - query SQL più articolate su un piccolo database  
  - definizione di una prima “data card” per un dataset  
  - check-list di data quality per progetti ML/LLM

- **Modalità deep dive (più giornate)**  
  - pipeline dati end-to-end (ingest, pulizia, feature, split train/val/test)  
  - integrazione con Data Cards Playbook e Data Audit Pack  
  - casi studio di leakage e bias in dataset reali

**Quando considerare il modulo “completato”**

- so caricare un dataset da CSV/Parquet in Pandas e capire `shape`, `dtypes`, `head()`
- so fare selezioni, filtri, aggregazioni e join semplici
- so creare e interrogare un piccolo DB SQL con qualche tabella
- ho scritto almeno una bozza di “scheda dataset” (data card) per un dataset di interesse
- so elencare 3–5 rischi tipici di data quality/leakage nei progetti ML/LLM

---

## Perché questo documento

I modelli ML/LLM sono inutili senza dati solidi.  
Questo documento costruisce le **fondamenta dati**:

- NumPy → array numerici e shape (base per tensori e DL)
- Pandas → tabelle, manipolazione dati, join, aggregazioni
- SQL → interrogare e combinare dati in database relazionali
- Data quality → evitare di “allenare l’intelligenza” su dati sporchi o fuorvianti
- Dataset cards → documentare dataset in modo responsabile (trasparenza, rischio, contesto)

Serve sia per i moduli ML classico (D05/D06), sia per DL/LLM (D07/D09/D10), sia per OSINT.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- capire cosa sono array NumPy e come si collegano a tensori DL
- usare Pandas per operazioni base e intermedie su dataset tabellari
- scrivere query SQL semplici (SELECT, WHERE, GROUP BY, JOIN)
- identificare problemi comuni di data quality e leakage
- compilare una prima “data card” per descrivere un dataset

---

## 1. Mappa degli argomenti

### 1.1 Blocchi principali

1. NumPy: array, shape, tipi, operazioni base.
2. Pandas: Series, DataFrame, caricamento dati, filtri, aggregazioni, join.
3. SQL: tabelle, chiavi, query base/intermedie.
4. Formati dati: CSV, JSON/JSONL, Parquet.
5. Data quality: missing values, outlier, incoerenze, duplicati.
6. Leakage e dataset split.
7. Dataset cards e trasparenza (Data Cards Playbook).

---

## 2. NumPy: array e shape

### 2.1 Perché NumPy

NumPy è la base di quasi tutto lo stack scientifico Python:

- array n-dimensionali efficienti
- operazioni vettoriali veloci
- interoperabilità con Pandas, SciPy, PyTorch, ecc.[^numpy-doc]

Per ML/LLM:

- concetto di **array** e **shape** è esattamente ciò che in DL chiamerò *tensore*.

[^numpy-doc]: Documentazione ufficiale NumPy: https://numpy.org/doc/stable/

### 2.2 Array e shape

Concetti chiave:

- un array NumPy è un contenitore n-dimensionale di valori omogenei
- la **shape** è una tupla che indica le dimensioni: `(n,)`, `(n, m)`, `(batch, features)`, `(batch, seq_len, dim)`

Esempio:

```python
import numpy as np

x = np.array()
print(x.shape)  # (3,)

X = np.array([,
              ])
print(X.shape)  # (2, 3)
```

Capire shape è fondamentale per:

- interpretare dimensioni di input/output di modelli
- debug di errori di dimensioni (es. mismatch in matrix multiply)

### 2.3 Operazioni base e broadcasting

Operazioni elementari:

- somma, sottrazione, moltiplicazione tra array
- funzioni come `np.mean`, `np.std`, `np.sum(axis=...)`

Broadasting (intuito, non teoria completa):

- permette di combinare array di shape compatibili senza copiare dati inutilmente
- es: sommare un vettore “riga” a tutte le righe di una matrice

---

## 3. Pandas: tabelle e manipolazione dati

### 3.1 Perché Pandas

Pandas è il tool standard per:

- lavorare con tabelle (CSV, Excel, database)
- fare operazioni “tipo SQL” in Python
- integrare dati con workflow ML/LLM

Documentazione e “10 minutes to pandas”:[^pandas-doc]

- https://pandas.pydata.org/docs/user_guide/index.html  
- https://pandas.pydata.org/docs/user_guide/10min.html  

[^pandas-doc]: Pandas User Guide, includendo “10 Minutes to pandas”.

### 3.2 Series e DataFrame

Elementi principali:

- `Series` → colonna con etichette (indice)
- `DataFrame` → tabella 2D (righe × colonne)

Esempio:

```python
import pandas as pd

df = pd.read_csv("data/example.csv")
print(df.head())
print(df.shape)
print(df.dtypes)
```

Operazioni base:

- selezionare colonne: `df["col"]`, `df[["col1", "col2"]]`
- filtri: `df[df["col"] > 10]`
- ordinamento: `df.sort_values("col")`

### 3.3 Aggregazioni, groupby, join

Concetti essenziali:

- `groupby` per aggregare per categoria (es. `df.groupby("country")["sales"].sum()`)
- join/merge per combinare tabelle (similarmente a SQL JOIN)

Esempio join:

```python
df_users = pd.read_csv("users.csv")
df_orders = pd.read_csv("orders.csv")

df = df_orders.merge(df_users, on="user_id", how="left")
```

---

## 4. SQL: tabelle, query e join

### 4.1 Perché SQL

SQL resta fondamentale anche in era LLM:

- molti dati vivono in database relazionali
- query complesse sono spesso più chiare in SQL che in codice
- molti strumenti di analytics e BI usano SQL come lingua principale

Per esercitarsi:

- SQLBolt (lezioni interattive): https://sqlbolt.com/  

### 4.2 Concetti base

- tabella, riga, colonna
- chiavi primarie e chiavi esterne
- relazioni 1–N, N–N

Query base:

```sql
SELECT col1, col2
FROM tabella
WHERE condizione
ORDER BY col1 DESC
LIMIT 10;
```

### 4.3 Join e aggregazioni

Join:

- INNER JOIN  
- LEFT JOIN (mantiene tutte le righe della tabella di sinistra)

Aggregazioni:

- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY` per raggruppare per categoria

---

## 5. Formati dati: CSV, JSON/JSONL, Parquet

### 5.1 CSV

Formato di testo tabellare:

- vantaggi: semplice, leggibile, supportato ovunque
- svantaggi: nessun tipo, problemi con separatori/virgolette

Uso tipico con Pandas:

```python
df = pd.read_csv("data/dataset.csv")
df.to_csv("data/dataset_clean.csv", index=False)
```

### 5.2 JSON / JSONL

- **JSON** → “documenti” complessi, utile per config e log strutturati
- **JSONL** → un JSON per riga, ideale per dataset e log che crescono nel tempo

Pandas può leggere JSONL:

```python
df = pd.read_json("logs/events.jsonl", lines=True)
```

### 5.3 Parquet

Formato colonnare compresso, ottimo per dataset grandi:

- leggibile da Pandas, Spark, molti tool
- conserva tipi
- efficiente in spazio e velocità

```python
df.to_parquet("data/dataset.parquet", index=False)
df_parquet = pd.read_parquet("data/dataset.parquet")
```

---

## 6. Data quality: problemi tipici

### 6.1 Tipi di problemi

- **valori mancanti** (missing)  
  - es: colonne con molti `NaN` o stringhe vuote
- **outlier**  
  - valori estremi che possono distorcere metriche e modelli
- **incoerenze**  
  - es: stesso concetto scritto in modi diversi (“USA”, “United States”, “U.S.”)
- **duplicati**  
  - righe duplicate, chiavi duplicate
- **tipi sbagliati**  
  - numeri salvati come stringhe, date come testo

### 6.2 Ispezione e pulizia di base

Con Pandas:

- `df.isna().sum()` per vedere missing per colonna
- `df.duplicated().sum()` per rilevare righe duplicate
- `df.describe()` per avere statistiche veloci

Strategie:

- drop: rimuovere righe/colonne problematiche (con cautela)
- imputazione: sostituire missing con mediana, media, valore speciale
- normalizzazione categorie: mapping esplicito per categorie disallineate

---

## 7. Leakage e split dei dati

### 7.1 Che cos’è il leakage

**Data leakage**: quando nel training il modello “vede” informazione che non avrebbe in produzione.

Esempi:

- usare variabili che contengono il target in forma mascherata
- calcolare statistiche di normalizzazione usando tutto il dataset (training + test)
- avere lo stesso utente/entità sia in train che in test in compiti di predizione futura

Effetti:

- performance gonfiate artificialmente
- modelli che crollano in produzione

### 7.2 Split corretto del dataset

Regole operative minime:

- separare chiaramente train / validation / test
- fare l’eventuale shuffling **prima** dello split e in modo riproducibile
- calcolare statistiche (es. media, varianza) SOLO sul training set

In D05/D06 (ML classico) e D07 (DL) queste regole tornano esplicitamente.

---

## 8. Dataset cards e trasparenza

### 8.1 Idea di dataset card

Una dataset card è un documento che riassume:

- origine del dataset
- schema e significato delle colonne
- come è stato raccolto e preprocessato
- limiti, rischi, possibili bias
- usi consentiti e sconsigliati

Il **Data Cards Playbook** di Google propone un workflow per creare artefatti di trasparenza per dataset.[^datacards]

[^datacards]: Data Cards Playbook: https://developers.google.com/learn/pathways/data-cards-playbook

### 8.2 Struttura minima di una data card

Campi minimi utili:

- Nome del dataset, versione, maintainer
- Fonte e modalità di raccolta
- Popolazione rappresentata (persone, eventi, domini)
- Scopo originale e scopi ulteriori possibili
- Preprocessamenti effettuati
- Rischi noti (bias, buchi, squilibri)
- Restrizioni d’uso

Questo modulo non richiede di usare lo schema completo del Playbook,
ma serve a fissare la pratica di **non usare mai dataset “anonimi” e non documentati**.

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Esplorare un dataset CSV con Pandas

**Obiettivo:** prendere confidenza con `DataFrame`, shape, tipi, statistiche.

**Passi:**

1. Scegliere un dataset CSV pubblico (es. da Kaggle, data.gov, ecc.).
2. Caricarlo in Pandas (`pd.read_csv`).
3. Stampare:
   - `df.shape`
   - `df.dtypes`
   - `df.head()`
4. Calcolare statistiche base (`df.describe()`).

**Deliverable:**

- breve nota in `private/notes/` con:
  - cosa contiene il dataset
  - quanti record/colonne ha
  - eventuali problemi subito visibili (missing, outlier evidenti)

---

### Laboratorio 2 — Pulizia base e trasformazioni

**Obiettivo:** applicare operazioni Pandas per pulire e trasformare dati.

**Passi:**

1. Continuare dal dataset del laboratorio 1.
2. Individuare almeno:
   - una colonna con missing
   - una con valori “sporchi” o incoerenti
3. Applicare:
   - una strategia di imputazione o drop sensata
   - una normalizzazione di categorie (es. mapping a valori standard)
4. Salvare il dataset pulito come `dataset_clean.csv` e/o Parquet.

**Deliverable:**

- `dataset_clean.csv` o `.parquet`
- nota che descrive cosa è stato pulito/cambiato e perché

---

### Laboratorio 3 — Mini-database SQL e join

**Obiettivo:** esercitarsi con SQL su un caso semplice.

**Passi:**

1. Prendere due CSV compatibili (es. `users` e `orders`) o crearli a mano.
2. Importarli in un piccolo DB SQLite (via Python o tool GUI).
3. Scrivere almeno 3 query:
   - SELECT con WHERE
   - SELECT con GROUP BY
   - JOIN tra due tabelle (es. ordini + utenti)
4. Salvare le query in un file `.sql` nel progetto.

**Deliverable:**

- file `.db` o `.sql` con le tabelle
- file `.sql` con le query
- output di esempio delle query (es. screenshot o esport)

---

### Laboratorio 4 — Prima bozza di dataset card

**Obiettivo:** documentare un dataset reale.

**Passi:**

1. Scegliere un dataset che userò in moduli ML/LLM/OSINT.
2. Creare una nota `dataset_<nome>.md` (in `private/notes/` o in un sottofolder dedicato)
   con una versione ridotta di data card:
   - descrizione
   - fonte
   - schema (colonne + significato)
   - scopo d’uso
   - rischi/limiti
3. Collegare questa nota in D03 e/o in D05/D06 dove il dataset verrà usato.

**Deliverable:**

- file `dataset_<nome>.md` con una data card minima
- eventuale link aggiunto in D03 o in index del repo

---

## 10. Rubriche e checklist

### Checklist — D03 completato

- [ ] So creare e manipolare array NumPy di base (shape, operazioni).
- [ ] So caricare un CSV in Pandas e analizzarlo con `head/shape/dtypes/describe`.
- [ ] So eseguire filtri, selezioni, aggregazioni semplici in Pandas.
- [ ] So creare e interrogare un piccolo DB SQL con almeno due tabelle e una JOIN.
- [ ] Ho usato almeno due formati dati (CSV + Parquet o CSV + JSONL).
- [ ] Ho identificato problemi di data quality in un dataset reale e fatto una pulizia minima.
- [ ] Ho scritto almeno una bozza di data card per un dataset.

### Errori tipici da evitare

- usare dataset “a scatola chiusa” senza chiedersi da dove vengono e come sono fatti.
- ignorare completamente i missing (trattare `NaN` e stringhe vuote come se non esistessero).
- fare split train/test a caso senza pensare a leakage.
- confondere comodi snippet di Pandas con “analisi” approfondite.
- non salvare decisioni sulle pulizie/trasformazioni (nessuna nota, nessun log).

### Segnali che “ho davvero capito” D03

- se mi danno un CSV sconosciuto, in 10–15 minuti so dire cosa contiene e dove sono i problemi.
- so spiegare la differenza tra CSV, JSON/JSONL e Parquet e quando usare ciascuno.
- so raccontare almeno un esempio di data leakage e come evitarlo.
- ho un dataset documentato con una data card, non solo con un filename vago.

---

## 11. Come ripartire dopo una pausa

Se torno su D03 dopo giorni o settimane:

1. Riprendo il dataset usato nei laboratori (o ne scelgo uno nuovo, ma piccolo).
2. Rilancio un notebook o script che:
   - carica il dataset
   - stampa `head/shape/dtypes`
3. Completo un micro-task:
   - aggiungere una pulizia mancante
   - scrivere una nuova query SQL
   - migliorare la data card con 2–3 campi nuovi
4. Aggiorno una nota (`private/notes/`) con:
   - decisioni prese sul dataset
   - idee per modelli o analisi da collegare ai moduli ML/LLM successivi

Scopo: mantenere il filo **tra dati, codice e documentazione**
senza dover rileggere tutto ogni volta.

---

## 12. Risorse consigliate

### 12.1 NumPy

- **NumPy documentation (stable)**  
  Documentazione principale, con guida introduttiva e reference.  
  https://numpy.org/doc/stable/  

- **NumPy: Absolute Beginner’s Guide**  
  Sezione introduttiva per chi è nuovo a NumPy (linkata dalla documentazione).  
  https://numpy.org/doc/stable/user/absolute_beginners.html  *(vedi dal sito principale)*

### 12.2 Pandas

- **Pandas User Guide**  
  Guida per argomenti: IO, missing data, groupby, join, time series, ecc.  
  https://pandas.pydata.org/docs/user_guide/index.html  

- **10 Minutes to pandas**  
  Introduzione rapida con esempi pratici.  
  https://pandas.pydata.org/docs/user_guide/10min.html  

### 12.3 SQL

- **SQLBolt** — lezioni interattive  
  Tutorial step-by-step con esercizi in-browser.  
  https://sqlbolt.com/  

### 12.4 Data cards e documentazione dei dataset

- **Data Cards Playbook (Google)**  
  Toolkit per progettare e compilare data cards per dataset ML.  
  https://developers.google.com/learn/pathways/data-cards-playbook  

- **Articolo introduttivo sul Data Cards Playbook**  
  Contesto, motivazioni e struttura del playbook.  
  https://research.google/blog/the-data-cards-playbook-a-toolkit-for-transparency-in-dataset-documentation/