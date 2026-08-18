# D01 — Workspace local-first, Git, Obsidian e LLM Wiki

## Perché questo documento

Questo documento definisce il mio *workspace* di studio e lavoro per AI / agenti / OSINT:
come organizzo i file, dove vive la conoscenza, come tengo tutto sincronizzato tra Mac, Windows e mobile.

L'obiettivo è avere:

- una struttura stabile e portabile nel tempo (plain-text + Git)
- un unico deposito di conoscenza leggibile da Obsidian, da GitHub e da strumenti AI
- una base pronta per diventare in futuro un vero corso per altre persone

---

## Obiettivi di apprendimento

Dopo questo modulo devo essere in grado di:

- descrivere l'architettura della mia "Stazione" (cartelle, repo, vault, backup)
- creare e mantenere il repository GitHub `stazione-knowledge`
- capire come si incastra Obsidian (vault locale) con il repo pubblico
- definire le regole base per usare LLM e agenti sulla mia knowledge base

---

## 1. Architettura generale della Stazione

### 1.1 Componenti principali

La mia Stazione è composta da:

- **Repo GitHub pubblico** `stazione-knowledge`  
  per le lezioni (D01–D16) e alcune note curate, leggibile anche da cellulare.
- **Cartella locale sincronizzata** (SSD / cloud)  
  che contiene sia il clone del repo pubblico, sia altri file non pubblici.
- **Vault Obsidian personale**  
  che punta alla stessa cartella locale, per avere backlink, grafi e ricerca full-text.
- **Strumenti AI / agenti**  
  che leggono i file Markdown e li usano come contesto (locale sul Mac, via API ovunque).

Questa architettura deve funzionare sia su Mac (M4 Max) sia su portatile Windows,
con la stessa identica struttura di cartelle e di file.

### 1.2 Struttura di cartelle di base

A livello locale (su disco):

```text
Stazione/
├── stazione-knowledge/        # clone del repo GitHub pubblico
│   ├── README.md
│   ├── index.md
│   └── docs/
│       ├── D01-workspace-llm-wiki.md
│       └── ...
├── private/                   # note, script, config non pubblici
│   ├── notes/
│   ├── code/
│   └── infra/
└── inbox/                     # materiale grezzo (download, PDF, export da LLM)
```

- `stazione-knowledge/` è ciò che vedono il mondo esterno e GitHub.
- `private/` e `inbox/` possono rimanere solo locali o in un altro repo (anche privato).

---

## 2. Repo GitHub `stazione-knowledge`

### 2.1 Scopo del repo

Il repository pubblico serve per:

- raccogliere le **lezioni** del mio percorso (D01–D16) in formato Markdown
- dare una **mappa leggibile** (`index.md`) del percorso e dei livelli (Fondamenti / Operativo / Avanzato / Specialistico)
- permettermi di leggere e ripassare le lezioni da qualunque dispositivo (desktop, laptop, smartphone)

Non contiene:

- dati sensibili
- appunti troppo grezzi o personali
- configurazioni con credenziali o segreti

### 2.2 Struttura del repo

Richiamo la struttura base:

```text
stazione-knowledge/
├── README.md       # descrizione generale del progetto
├── index.md        # mappa del percorso e tabella D01–D16
└── docs/
    ├── D01-workspace-llm-wiki.md
    ├── D02-...md
    └── ...
```

Ogni documento `Dxx-...md` è una lezione autonoma, con:

- titolo chiaro
- obiettivi
- sezioni leggibili anche su schermo piccolo
- link ad altre lezioni quando serve

---

## 3. Vault Obsidian e vista personale

### 3.1 Obsidian come “vista privata” sulla stessa knowledge

Il vault Obsidian punta alla cartella `Stazione/`:

- così vede sia il clone del repo `stazione-knowledge/`
- sia le note private in `private/` e il materiale in `inbox/`

In Obsidian posso:

- collegare le lezioni Dxx con wikilink
- aggiungere proprietà (tag, tipo di documento, livello, stato)
- creare viste personalizzate (dashboard, mappe concettuali) che **non devono** per forza finire nel repo pubblico

### 3.2 Convenzioni per le note

Per tenere ordine:

- lezione pubblica → file in `stazione-knowledge/docs/`  
- nota privata di lavoro su quella lezione → file in `private/notes/` con link alla lezione Dxx
- materiale grezzo (PDF, link, export) → file in `inbox/` o riferimenti in note dedicate

---

## 4. LLM, agenti e uso della knowledge base

### 4.1 Regole base

Quando uso LLM e agenti sulla mia knowledge base:

- **non** do in pasto direttamente `inbox/` senza filtro (rischio rumore e confusione)
- uso le lezioni Dxx e le note curate come fonte principale di verità
- aggiorno i documenti quando un agente produce qualcosa di utile e verificato

### 4.2 Esempi di prompt di sistema (idea)

In futuro questo documento potrà includere:

- convenzioni per i prompt di sistema che spiegano all'agente dove leggere (docs/, private/notes/)
- regole su cosa può modificare e cosa no
- linee guida per l'uso di modelli locali sul Mac vs API cloud sul portatile

Per ora mi basta sapere che:

- il repo pubblico è **read-only** per gli agenti (non scrivono direttamente lì)
- le modifiche passano prima per il vault / note private, poi eventualmente vengono promosse al repo

---

## 5. Workflow quotidiano (bozza)

Un flusso minimo di lavoro:

1. **Quando trovo materiale interessante**  
   - lo salvo in `inbox/` (PDF, link, estratti)
2. **Quando studio / sintetizzo**  
   - creo o aggiorno una lezione Dxx in `stazione-knowledge/docs/`
   - oppure creo una nota privata collegata a una lezione
3. **Quando ho fatto un passo significativo**  
   - `git add`, `git commit`, `git push` nel repo pubblico
4. **Periodicamente**  
   - ripasso l’`index.md` per vedere dove mancano lezioni
   - aggiorno i titoli/tabelle per riflettere meglio i contenuti reali

---

## 6. Prossimi passi per D01

- Rifinire i nomi delle cartelle e delle note in base a come utilizzo davvero Mac e Windows.
- Aggiungere esempi concreti di configurazione (percorsi reali su macOS e Windows).
- Documentare una prima versione delle regole per gli agenti (es. file `AGENTS.md` separato).