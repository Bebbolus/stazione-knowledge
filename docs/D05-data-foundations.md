---
aliases:
- D05
- Data Foundations
- Data Engineering ML
- NumPy Pandas SQL
- Data Quality
- Ingegneria dei Dati
resources:
- title: SQLBolt (Esercizi SQL Interattivi)
  url: https://sqlbolt.com/
  type: lab
- title: Google Data Cards Playbook
  url: https://developers.google.com/learn/pathways/data-cards-playbook
  type: ref
- title: Pandas Documentation
  url: https://pandas.pydata.org/docs/
  type: ref
---
# Data Foundations: NumPy, Pandas, SQL e Qualità del Dato

L'**ingegneria dei dati per il machine learning** è la disciplina che standardizza l'ingestione, la bonifica qualitativa, la trasformazione tensoriale e la serializzazione efficiente di flussi informativi eterogenei prima dell'addestramento dei modelli predittivi. Questa architettura si impiega in pipeline di intelligenza artificiale applicata, sistemi di intelligence OSINT e piattaforme analitiche enterprise per convertire dati grezzi non strutturati in matrici numeriche omogenee prive di anomalie sistematiche. La disciplina esiste perché l'accuratezza e l'affidabilità di qualsiasi algoritmo di intelligenza artificiale dipendono rigidamente dalla purezza statistica dei dati in ingresso, dall'assoluta prevenzione del data leakage tra partizioni di training e test, e dall'adozione di strutture dati allineate con l'accelerazione hardware vettoriale.

## Il Problema della Corruzione del Dato e del Data Leakage

Nella pratica ingegneristica, i dati raccolti da sorgenti aperte, sensori di rete o registri transazionali presentano un elevato tasso di entropia: valori mancanti non casuali, formati temporali eterogenei, discrepanze di codifica dei caratteri e distribuzioni fortemente sbilanciate. L'immissione diretta di dati non validati all'interno di un modello statistico innesca il fenomeno **GIGO (Garbage-In, Garbage-Out)**, in cui il sistema ottimizza i propri parametri su artefatti spuri e rumore di misurazione, compromettendo la validità di qualsiasi inferenza a valle.

L'anomalia più critica nei workflow di apprendimento automatico è il **Data Leakage** (fuga di dati), che si verifica quando informazioni appartenenti al set di test o al futuro temporale contaminano il set di addestramento prima o durante la fase di preprocessing. Un esempio tipico consiste nel calcolo di parametri statistici globali (come media e deviazione standard per la standardizzazione delle feature, o la mediana per l'imputazione dei valori nulli) sull'intero dataset prima della separazione tra train e test. Questa operazione trasmette surrettiziamente la distribuzione del test set al modello, generando metriche di accuratezza artificialmente perfette in fase di validazione ma causando un crollo catastrofico delle prestazioni non appena il sistema viene distribuito in produzione su dati reali non visti.

La risposta architetturale consiste nell'ingegnerizzazione di pipeline di trasformazione a compartimenti stagni, in cui ogni manipolazione statistica viene calcolata esclusivamente sul set di training isolato ed applicata deterministicamente ai set di validazione e test.

## Calcolo Tensoriale e Allocazione di Memoria con NumPy

I modelli di machine learning e le architetture neurali operano esclusivamente su vettori, matrici e tensori numerici a dimensione fissa. La libreria cardine per la manipolazione di tali strutture in [Python](https://www.python.org/) (il linguaggio di programmazione di riferimento per l'AI) è [NumPy](https://numpy.org/) (la libreria cardine per il calcolo scientifico e la gestione efficiente di array multidimensionali in memoria).

### L'Array e le sue Dimensioni (Shape)

L'oggetto fondamentale di NumPy è l'`ndarray`, una struttura dati contigua in memoria RAM caratterizzata da un tipo di dato omogeneo (`dtype`) e da una tupla di dimensioni (`shape`). A differenza delle liste native di Python (che memorizzano puntatori sparsi a oggetti eterogenei allocati nella heap), l'`ndarray` alloca un blocco continuo di byte, consentendo l'accesso diretto alla memoria tramite il meccanismo degli *strides* (il numero di byte da attraversare per avanzare di un elemento lungo ciascun asse dimensionale). Le strutture tensoriali di NumPy costituiscono il fondamento computazionale diretto per i tensori di [PyTorch](https://pytorch.org/) (il framework di deep learning open-source basato sul calcolo tensoriale e differenziazione automatica).

```python
import numpy as np

# Creazione di tensori con specificazione esplicita del tipo di dato (dtype)
vettore_1d = np.array([1.5, 2.7, 3.2, 4.8], dtype=np.float64)
matrice_2d = np.arange(12, dtype=np.float32).reshape(3, 4)

print("Vettore 1D shape:", vettore_1d.shape, "| Dtype:", vettore_1d.dtype)
print("Matrice 2D shape:", matrice_2d.shape, "| Dimensioni (ndim):", matrice_2d.ndim)
print("Memory Strides (passo in byte per asse):", matrice_2d.strides)
print("Occupazione di memoria totale (bytes):", matrice_2d.nbytes)
```

### Esecuzione Vettorizzata e Broadcasting

L'elaborazione di grandi moli di dati numerici tramite cicli iterativi in Python puro comporta un grave degrado prestazionale dovuto all'overhead dell'interprete e al continuo controllo dinamico dei tipi (*type dispatching*). NumPy elimina questo collo di bottiglia delegando le operazioni matematiche a routine scritte in C e Fortran, ottimizzate per sfruttare i registri SIMD (Single Instruction, Multiple Data) dei moderni processori. Il meccanismo del **Broadcasting** estende automaticamente le dimensioni di array con forme compatibili, consentendo operazioni aritmetiche tra matrici e scalari o vettori senza allocazione ridondante di memoria.

```python
import time
import numpy as np

dimensione = 1_000_000
lista_python = list(range(dimensione))
array_numpy = np.arange(dimensione, dtype=np.float64)

# 1. Esecuzione con ciclo iterativo Python standard
start_time = time.perf_counter()
risultato_loop = [valore * 2.5 + 1.0 for valore in lista_python]
tempo_loop = time.perf_counter() - start_time

# 2. Esecuzione vettorizzata NumPy con istruzioni SIMD e broadcasting
start_time = time.perf_counter()
risultato_numpy = array_numpy * 2.5 + 1.0
tempo_numpy = time.perf_counter() - start_time

print(f"Tempo ciclo Python standard: {tempo_loop:.4f} s")
print(f"Tempo vettorizzazione NumPy:  {tempo_numpy:.6f} s")
print(f"Fattore di accelerazione vettoriale: {tempo_loop / tempo_numpy:.1f}x")
```

## Manipolazione Dati Tabellari e Bonifica Qualitativa con Pandas

Prima della conversione in matrici numeriche pure, i dati tabellari richiedono un'elaborazione strutturata a livello di colonne, gestita primariamente tramite [Pandas](https://pandas.pydata.org/) (la libreria open-source fondamentale in Python per la manipolazione e l'analisi di dati tabellari strutturati).

### Lavorare sui DataFrame

L'astrazione centrale di Pandas è il `DataFrame`, una struttura dati bidimensionale eterogenea indicizzata per righe e colonne. Il DataFrame consente di applicare maschere booleane, eseguire proiezioni e trasformare tipi di dato con sintassi compatta, facilitando la preparazione dei dati prima del training.

```python
import pandas as pd
import numpy as np

dati_grezzi = {
    "id_transazione": [1001, 1002, 1003, 1004, 1005],
    "cliente": ["Alfa Corp", "Beta LLC", "Gamma Spa", "Alfa Corp", "Delta Inc"],
    "valore_euro": [1250.0, 450.0, 3100.0, 890.0, 150.0],
    "stato_approvazione": ["APPROVATO", "SOSPESO", "APPROVATO", "RESPINTO", "APPROVATO"]
}

df_transazioni = pd.DataFrame(dati_grezzi)

# Filtraggio booleano e selezione per colonne
filtro_approvati = (df_transazioni["stato_approvazione"] == "APPROVATO") & (df_transazioni["valore_euro"] >= 1000.0)
df_rilevanti = df_transazioni.loc[filtro_approvati, ["id_transazione", "cliente", "valore_euro"]]

print("Transazioni filtrate ad alto valore:")
print(df_rilevanti)
```

### Bonifica dei Dati e Prevenzione Anomalie

La fase di data quality identifica e corregge sistematicamente quattro tipologie di difetti: duplicati di riga, formattazione incoerente delle stringhe categoriche, tipi di dato non allineati e valori nulli (`NaN`). L'imputazione dei valori mancanti deve seguire logiche conservative (ad esempio la mediana campionaria per distribuzioni asimmetriche con outlier) per evitare distorsioni arbitrarie della varianza originale.

```python
import pandas as pd
import numpy as np

dati_sporchi = {
    "id_utente": [1, 2, 3, 4, 5, 5],
    "eta": [28.0, np.nan, 45.0, 33.0, np.nan, np.nan],
    "reddito": [35000.0, 62000.0, np.nan, 48000.0, 95000.0, 95000.0],
    "livello_account": [" premium ", "BASIC", "Premium", " STANDARD", "basic", "basic"],
    "data_creazione": ["2023-01-10", "2023-02-14", "2022-11-01", "2023-05-20", "2021-09-15", "2021-09-15"]
}

df_bonifica = pd.DataFrame(dati_sporchi)

# 1. Deduplicazione record
df_bonifica = df_bonifica.drop_duplicates(subset=["id_utente"]).copy()

# 2. Normalizzazione testo e stringhe categoriche
df_bonifica["livello_account"] = df_bonifica["livello_account"].str.strip().str.upper()

# 3. Conversione tipi di dato e parsing temporale
df_bonifica["data_creazione"] = pd.to_datetime(df_bonifica["data_creazione"])

# 4. Imputazione mirata dei valori mancanti tramite mediana
mediana_eta = df_bonifica["eta"].median()
mediana_reddito = df_bonifica["reddito"].median()
df_bonifica["eta"] = df_bonifica["eta"].fillna(mediana_eta)
df_bonifica["reddito"] = df_bonifica["reddito"].fillna(mediana_reddito)

print("DataFrame post-bonifica:")
print(df_bonifica)
```

### Fusione Relazionale (Merge e Join)

L'integrazione di sorgenti informative eterogenee richiede la combinazione relazionale di tabelle tramite chiavi primarie ed esterne. Le operazioni di `merge` (left, inner, outer join) consentono l'arricchimento contestuale dei log operativi senza perdita di integrità referenziale.

```python
import pandas as pd

df_utenti = pd.DataFrame({
    "id_utente": [1, 2, 3],
    "nome_ente": ["Ministero Interno", "Agenzia Dogane", "Polizia Postale"]
})

df_eventi = pd.DataFrame({
    "id_evento": [101, 102, 103, 104],
    "id_utente": [1, 2, 1, 4],
    "tipo_accesso": ["LOGIN", "EXPORT", "QUERY", "LOGIN"]
})

# Left Join relazionale per arricchimento dei log di audit
df_audit = pd.merge(df_eventi, df_utenti, on="id_utente", how="left")
print("Audit Log con join relazionale:")
print(df_audit)
```

## Estrazione e Pipeline Analitiche su Database Relazionali (SQL)

Quando i volumi di dati superano la capacità della memoria RAM locale, il caricamento integrale in un DataFrame diventa impraticabile. In questi scenari, il preprocessing e l'aggregazione vengono delegati direttamente al motore del database relazionale tramite [SQL](https://www.sqlite.org/) (il linguaggio standard per l'interrogazione e la manipolazione di basi di dati relazionali).

### Elaborazione Analitica su Database (SQL)

L'esecuzione di query complesse con clausole di join, raggruppamento (`GROUP BY`) e filtraggio aggregato (`HAVING`) all'interno di motori SQL relazionali come SQLite o database analitici avanzati come [DuckDB](https://duckdb.org/) (il database relazionale analitico OLAP in-process ad altissime prestazioni per query SQL) permette di estrarre e trasferire nella memoria di Python unicamente il sottoinsieme compatto di feature necessarie per l'addestramento.

```python
import sqlite3
import pandas as pd

connessione = sqlite3.connect(":memory:")
cursore = connessione.cursor()

# Creazione schema relazionale
cursore.execute("""
CREATE TABLE unita_operative (
    id_unita INTEGER PRIMARY KEY,
    reparto TEXT NOT NULL,
    sede TEXT NOT NULL
);
""")

cursore.execute("""
CREATE TABLE missioni (
    id_missione INTEGER PRIMARY KEY,
    id_unita INTEGER NOT NULL,
    costo_operativo REAL NOT NULL,
    data_missione TEXT NOT NULL,
    FOREIGN KEY (id_unita) REFERENCES unita_operative (id_unita)
);
""")

unita_dati = [(1, "Cyber Threat Intel", "Roma"), (2, "SOC Tier 2", "Milano"), (3, "Forensic Lab", "Torino")]
missioni_dati = [
    (101, 1, 4500.0, "2024-01-10"),
    (102, 1, 3200.0, "2024-01-15"),
    (103, 2, 8900.0, "2024-02-01"),
    (104, 3, 1200.0, "2024-02-10")
]

cursore.executemany("INSERT INTO unita_operative VALUES (?, ?, ?)", unita_dati)
cursore.executemany("INSERT INTO missioni VALUES (?, ?, ?, ?)", missioni_dati)
connessione.commit()

query_analitica = """
SELECT 
    u.reparto,
    u.sede,
    COUNT(m.id_missione) AS numero_missioni,
    SUM(m.costo_operativo) AS spesa_totale,
    AVG(m.costo_operativo) AS costo_medio
FROM unita_operative u
INNER JOIN missioni m ON u.id_unita = m.id_unita
GROUP BY u.id_unita, u.reparto, u.sede
HAVING SUM(m.costo_operativo) > 2000.0
ORDER BY spesa_totale DESC;
"""

df_report = pd.read_sql_query(query_analitica, connessione)
print(df_report)
connessione.close()
```


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D03-data-foundations. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Formati di Archiviazione e Serializzazione: CSV vs JSONL vs Parquet

La scelta del formato di serializzazione su disco determina drasticamente la velocità di I/O e l'efficienza di archiviazione nelle pipeline di intelligenza artificiale.

### Archiviazione Colonnare (Parquet e JSONL)

Mentre i file CSV memorizzano i dati riga per riga in formato testuale grezzo privo di metadati sui tipi di colonna, il formato binario [Apache Parquet](https://parquet.apache.org/) (il formato di archiviazione colonnare binario compresso standard per big data e analytics), integrato con le specifiche in-memory di [Apache Arrow](https://arrow.apache.org/) (lo standard multipiattaforma per l'archiviazione colonnare di dati in memoria) ed engine ad alte prestazioni come [Polars](https://pola.rs/) (il motore di elaborazione dati multithread ad alte prestazioni basato su Apache Arrow), adotta una suddivisione colonnare compressa (Snappy o ZSTD). L'archiviazione per colonne consente di caricare in memoria solo le variabili selezionate (*column pruning*), riducendo il tempo di scansione del disco e tagliando lo spazio occupato fino all'80-90% rispetto ai file CSV equivalenti.

```python
import os
import tempfile
import numpy as np
import pandas as pd

campioni = 50_000
dataset = {
    "id_sessione": [f"sess_{idx}" for idx in range(campioni)],
    "ip_hash": np.random.randint(1_000_000, 9_999_999, size=campioni),
    "tempo_risposta_ms": np.random.normal(45.0, 12.0, size=campioni).astype(np.float32),
    "codice_stato": np.random.choice([200, 301, 403, 500], size=campioni, p=[0.85, 0.05, 0.08, 0.02])
}

df_benchmark = pd.DataFrame(dataset)

with tempfile.TemporaryDirectory() as cartella_temp:
    path_csv = os.path.join(cartella_temp, "log_accessi.csv")
    path_parquet = os.path.join(cartella_temp, "log_accessi.parquet")
    path_jsonl = os.path.join(cartella_temp, "log_accessi.jsonl")

    # Scrittura nei vari formati
    df_benchmark.to_csv(path_csv, index=False)
    df_benchmark.to_parquet(path_parquet, engine="pyarrow", compression="snappy", index=False)
    df_benchmark.to_json(path_jsonl, orient="records", lines=True)

    dim_csv = os.path.getsize(path_csv) / (1024 * 1024)
    dim_jsonl = os.path.getsize(path_jsonl) / (1024 * 1024)
    dim_parquet = os.path.getsize(path_parquet) / (1024 * 1024)

    print(f"Dimensione file CSV:     {dim_csv:.2f} MB")
    print(f"Dimensione file JSONL:   {dim_jsonl:.2f} MB")
    print(f"Dimensione file Parquet: {dim_parquet:.2f} MB")
    print(f"Fattore di compressione CSV -> Parquet: {dim_csv / dim_parquet:.2f}x")
```

## Trasparenza Metodologica e Schede dei Dataset (Data Cards)

La corretta validazione numerica dei dati non garantisce l'assenza di bias statistici o limiti sistematici insiti nelle modalità di campionamento.

Per assicurare la verificabilità forense e la responsabilità algoritmica, ogni dataset destinato all'addestramento deve essere corredato da una scheda di documentazione standardizzata, conforme alle linee guida del [Google Data Cards Playbook](https://developers.google.com/learn/pathways/data-cards-playbook) (il framework metodologico ideato da [Google](https://about.google/) per la trasparenza e la documentazione sistematica dei dataset). La Data Card formalizza la provenienza delle fonti, l'intervallo temporale di acquisizione, le limitazioni note, le popolazioni sottorappresentate e i casi d'uso esplicitamente vietati.

```python
import json

data_card_schema = {
    "metadata": {
        "dataset_name": "Cyber_Threat_Events_Corpus",
        "version": "1.2.0",
        "maintainer": "Security Operations Center Analytics Team",
        "license": "CC-BY-4.0",
        "last_updated": "2026-08-18"
    },
    "provenance": {
        "source": "Network firewall gateway logs and honeytoken telemetry",
        "collection_method": "Automated ingestion via Kafka stream broker",
        "time_span": "2025-01-01 to 2025-12-31"
    },
    "schema_definition": {
        "id_sessione": {"type": "string", "description": "Identificativo pseudonimizzato della sessione TCP"},
        "tempo_risposta_ms": {"type": "float32", "description": "Latenza di risposta in millisecondi"},
        "codice_stato": {"type": "int32", "description": "Codice HTTP di terminazione connessione"}
    },
    "ethical_and_bias_considerations": {
        "represented_population": "Internal enterprise corporate infrastructure",
        "known_limitations": "Under-represents UDP anomalies and encrypted micro-tunnels",
        "prohibited_use_cases": "Automated attribution of physical identities without manual forensics"
    }
}

print(json.dumps(data_card_schema, indent=2))
```

## Compromessi Operativi e Scelte Architetturali

La progettazione di pipeline di dati richiede bilanciamenti consapevoli tra consumo di memoria, flessibilità dello schema e throughput computazionale.

### Esecuzione In-Memory vs Scalabilità Out-Of-Core

L'impiego di Pandas garantisce un'eccellente velocità di manipolazione ma impone che l'intero dataset risieda nella memoria RAM con un fattore di overhead che varia tipicamente da 2x a 5x rispetto alla dimensione del file su disco. Per dataset su larga scala che eccedono le risorse di memoria fisica, l'architettura deve prevedere la transizione verso engine vettorializzati out-of-core o database colonnari in-process come DuckDB o Polars, evitando blocchi di sistema per saturazione di memoria.

### Formati Flessibili (JSONL) vs Formati Rigidi Ottimizzati (Parquet)

I formati semi-strutturati come JSONL consentono l'acquisizione flessibile di eventi con schemi mutevoli nel tempo, risultando ideali per l'ingestione da scraper web o stream Kafka. Tuttavia, non supportano compressione colonnare nativa né indicizzazione statistica dei blocchi di byte, rendendo Parquet la scelta obbligata per le fasi di archiviazione definitiva e alimentazione di modelli di machine learning su larga scala.

## Riferimenti Bibliografici e Risorse Tecniche

### Guide Ufficiali e Documentazione di Riferimento

I dettagli implementativi sull'architettura interna degli array e sulla gestione della memoria sono consultabili nella [Documentazione ufficiale NumPy](https://numpy.org/doc/stable/). I pattern avanzati di pulizia e trasformazione di dati tabellari sono descritti nella [Guida per l'Utente di Pandas](https://pandas.pydata.org/docs/user_guide/index.html).

### Piattaforme Interattive e Standard di Documentazione

L'apprendimento pratico delle query relazionali e delle strategie di join è supportato dai percorsi interattivi di [SQLBolt](https://sqlbolt.com/) (la piattaforma interattiva per l'apprendimento guidato del linguaggio SQL). Per l'approfondimento della trasparenza e della governance dei dati nell'AI, fare riferimento al [Google Data Cards Playbook](https://developers.google.com/learn/pathways/data-cards-playbook) e alle relative pubblicazioni scientifiche rilasciate dal team di ricerca di [Google Research](https://research.google/).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



- [ ] Ispezione dimensionale e benchmarking vettoriale: Creare un array NumPy bidimensionale da un milione di righe e dieci colonne, ispezionarne `shape`, `dtype` e `strides`, ed eseguire un benchmark comparativo tra una trasformazione lineare vettorizzata e un ciclo iterativo su lista Python, calcolando l'accelerazione temporale ottenuta.
- [ ] Pipeline di bonifica e validazione con Pandas: Caricare un dataset tabellare contenente valori nulli, duplicati di riga e formati eterogenei, applicare una pipeline di deduplicazione, normalizzazione delle stringhe e imputazione dei valori mancanti tramite mediana, e serializzare il dataset bonificato in formato Apache Parquet compresso con Snappy.
- [ ] Query analitiche relazionali in SQLite: Inizializzare un database SQLite in memoria, creare due tabelle relazionali collegate da chiave esterna, inserire record sintetici di telemetria ed eseguire una query complessa con `INNER JOIN`, `GROUP BY` e filtraggio `HAVING`, caricando il risultato aggregato in un DataFrame Pandas.
- [ ] Redazione di una Data Card standardizzata: Redigere un file di specifica JSON o Markdown conforme al formato Data Card per un dataset reale o sintetico, documentando la provenienza delle fonti, le restrizioni etiche d'uso, le limitazioni tecniche note e le caratteristiche dello schema numerico.