# D01 — Workspace local-first, Git, Obsidian e LLM Wiki

## Meta-modulo D01

**Target**  
Me stesso oggi, e in futuro chiunque voglia usare un workspace *local-first* per AI / LLM / OSINT
con Git + Obsidian + wiki-LLM, senza essere DevOps full-time.

**Prerequisiti consigliati**

- uso base di terminale (cd, ls, mkdir, git clone/pull/commit)
- concetti minimi di Git (commit, branch main, remote)
- familiarità base con file di testo e Markdown
- nessuna conoscenza obbligatoria di ML/LLM, ma curiosità per AI e automazione

**Durata indicativa**

- **Modalità minima (~1,5–2 ore)**  
  - creare la cartella `Stazione/`  
  - clonare il repo `stazione-knowledge`  
  - configurare il primo vault Obsidian  
  - capire a grandi linee il flusso sorgente → nota → lezione

- **Modalità standard (~4 ore)**  
  - completare struttura cartelle (pubblico/privato/inbox)  
  - creare AGENTS.md e prime regole di uso degli agenti  
  - eseguire almeno 1–2 laboratori  
  - impostare un piano di backup minimo

- **Modalità deep dive (più sessioni)**  
  - definire in dettaglio ICM e flussi raw → source note → wiki → artefatti  
  - integrare LLM wiki stile Karpathy  
  - impostare automazioni (task per agenti, script di sincronizzazione)

**Quando considerare il modulo “completato”**

- esiste la cartella `Stazione/` con sottostruttura chiara
- il repo `stazione-knowledge` è funzionante (clone locale + remote GitHub)
- Obsidian può aprire `Stazione/` come vault e mostrare D01
- ho almeno una nota che segue il flusso:
  sorgente → distillazione → collegamento nel wiki
- esiste una bozza di `AGENTS.md` con permessi e limiti per gli agenti

---

## Perché questo documento

Questo documento definisce il mio *workspace* di studio e lavoro per AI / agenti / OSINT:
come organizzo i file, dove vive la conoscenza, come tengo tutto sincronizzato
tra Mac, Windows e mobile, e come preparo il terreno per un wiki mantenuto da LLM.

L’obiettivo è avere:

- una struttura stabile e portabile nel tempo (plain-text + Git)
- un unico deposito di conoscenza leggibile da Obsidian, da GitHub e da strumenti AI
- una base pronta per diventare in futuro un vero corso per altre persone
- un flusso chiaro e auditabile tra sorgenti grezze, note distillate e lezioni stabili

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere l’architettura della mia “Stazione” (cartelle, repo, vault, backup)
- creare e mantenere il repository GitHub pubblico `stazione-knowledge`
- capire come si incastrano Obsidian (vault locale) e repo GitHub (pubblico)
- definire il flusso ICM (raw → note → wiki → artefatti) e dove si collocano gli agenti
- impostare regole base per usare LLM e agenti sulla mia knowledge base senza rovinarla

---

## 1. Architettura generale della Stazione

### 1.1 Componenti principali

La mia Stazione è composta da quattro elementi:

1. **Repo GitHub pubblico** `stazione-knowledge`  
   raccoglie le lezioni (D01–D16) e alcune note curate, leggibile anche da cellulare.

2. **Cartella locale sincronizzata** (SSD / cloud)  
   contiene il clone del repo pubblico più altri file non pubblici; è la “root” del vault.

3. **Vault Obsidian personale**  
   punta alla stessa cartella locale, per avere backlink, grafi, query e viste personalizzate.

4. **Strumenti AI / agenti**  
   leggono i file Markdown e li usano come contesto (modelli locali sul Mac, API cloud ovunque),
   seguendo regole chiare definite in `AGENTS.md` e nei prompt di sistema.

Questa architettura deve funzionare sia su Mac (M4 Max) sia su portatile Windows,
con la stessa identica struttura di cartelle e file.

---

### 1.2 Struttura di cartelle di base

A livello locale (su disco, Mac o Windows):

```text
Stazione/
├── stazione-knowledge/        # clone del repo GitHub pubblico
│   ├── README.md
│   ├── index.md
│   └── docs/
│       ├── D01-workspace-llm-wiki.md
│       ├── D02-python-refresher.md
│       └── ...
├── private/                   # note, script, config non pubblici
│   ├── notes/                 # note di lavoro, journaling, appunti grezzi
│   ├── code/                  # script, prototipi, tool non destinati al pubblico
│   └── infra/                 # config, docker-compose, VM, AGENTS.md (se non pubblico)
└── inbox/                     # materiale grezzo (download, PDF, export da LLM, web clip)
```

- `stazione-knowledge/` è ciò che vede il mondo esterno e GitHub.
- `private/` e `inbox/` restano locali o su un repo separato (anche privato).
- Obsidian apre **tutta** `Stazione/` come vault, così può navigare sia pubblico che privato.

---

## 2. Struttura concettuale: raw → note → wiki → artefatti

### 2.1 I livelli ICM delle note

Per non perdere provenance e tenere tutto auditabile,
il materiale segue questi livelli (in parte ispirati a ICM e wiki‑LLM):

1. **Raw / Sorgenti**  
   - file originali in `inbox/` (PDF, HTML, esport di chat, ritagli web)
   - immutabili: non li modifico, solo li aggiungo o elimino

2. **Note distillate**  
   - note in `private/notes/` che riassumono e analizzano le sorgenti
   - includono link alla sorgente, concetti chiave, domande aperte

3. **Wiki / Lezioni stabili**  
   - file in `stazione-knowledge/docs/` e collegamenti in `index.md`
   - testo curato, più stabile e “pubblicabile”, usato per corsi, articoli, briefing

4. **Artefatti / Output**  
   - report, slide, script pronti, modelli di agenti, workflow
   - possono finire in repo dedicati o in sezioni specifiche del vault

Il passaggio è:

```text
inbox/ (raw) → private/notes/ (distillato) → stazione-knowledge/docs/ (wiki/lezioni) → deliverable
```

Ogni passaggio aggiunge struttura e riduce rumore.

---

### 2.2 Mappare questa struttura nel vault Obsidian

Nel vault Obsidian posso modellare questa logica in modo leggermente diverso,
mantenendo la tua preferenza per una struttura piatta con cartelle “Sistema” e “Analisi”:

- **Sistema**  
  - note su architettura, workflow, regole, AGENTS.md, documentazione del sistema stesso  
  - include la descrizione di come funziona la Stazione, di fatto “manuale d’uso”

- **Analisi**  
  - note di contenuto (OSINT, AI, agenti, geopolitica, ecc.)
  - qui finiscono le note distillate e i draft che, se maturi, diventano lezioni Dxx pubbliche

Fisicamente, posso far corrispondere:

- `stazione-knowledge/docs/` ↔ sottoinsieme delle note “stabili” che vivono anche sul repo
- `private/notes/` ↔ bozze, appunti, log giornalieri, analisi non ancora promosse

---

## 3. Repo GitHub `stazione-knowledge`

### 3.1 Scopo del repo

Il repository pubblico `stazione-knowledge` serve per:

- raccogliere le **lezioni** del mio percorso (D01–D16) in formato Markdown
- dare una **mappa leggibile** (`index.md`) del percorso e dei livelli (Fondamenti / Operativo / Avanzato / Specialistico)
- permettermi di leggere e ripassare le lezioni da qualunque dispositivo (desktop, laptop, smartphone)
- offrire in futuro una base per un corso pubblico, senza esporre materiale sensibile

Non contiene:

- dati sensibili o indagini reali
- appunti troppo grezzi o personali
- configurazioni con credenziali o segreti

---

### 3.2 Struttura del repo

Richiamo la struttura base:

```text
stazione-knowledge/
├── README.md       # descrizione generale del progetto
├── index.md        # mappa del percorso e tabella D01–D16
└── docs/
    ├── D01-workspace-llm-wiki.md
    ├── D02-python-refresher.md
    ├── D03-...md
    └── ...
```

Caratteristiche:

- ogni `Dxx-...md` è una *lezione autonoma*, con:
  - titolo chiaro
  - obiettivi
  - sezioni leggibili anche su schermo piccolo
  - link ad altre lezioni e risorse esterne
- `index.md` è la *home page* (GitHub Pages) con:
  - spiegazione dei livelli (Fondamenti, Operativo, Avanzato, Specialistico)
  - tabella D01–D16 → livello → file

---

### 3.3 Lettura come sito (GitHub Pages)

Abilitando GitHub Pages:

- `index.md` diventa la home di un sito statico  
- i link a `docs/Dxx-...md` diventano pagine navigabili
- da mobile posso leggere le lezioni come se fossero un piccolo libro tecnico

Questo modulo non richiede di configurare un generatore statico complesso:
Markdown puro + GitHub Pages basta come primo step.

---

## 4. Vault Obsidian e vista personale

### 4.1 Obsidian come “vista privata” sulla stessa knowledge

Il vault Obsidian punta alla cartella `Stazione/`:

- vede il clone del repo `stazione-knowledge/`
- vede anche `private/` e `inbox/`

Vantaggi:

- posso avere backlink e grafi tra note private e lezioni Dxx
- posso usare proprietà/frontmatter per classificare note e lezioni
- posso creare viste (Dataview, query, dashboard) per seguire il progresso e le relazioni

### 4.2 Convenzioni per le note (nome, proprietà)

Per tenere ordine:

- **lezione pubblica** → file in `stazione-knowledge/docs/`  
- **nota privata di lavoro** su quella lezione → file in `private/notes/`, con link a `Dxx-...md`
- **materiale grezzo** → file in `inbox/` + link dalle note

Esempio di proprietà che posso usare in Obsidian:

```yaml
***
tipo: lezione
codice: D01
livello: fondamenti
stato: stabile
tags:
  - workspace
  - obsidian
  - git
***
```

Per note private:

```yaml
***
tipo: nota
relazione:
  - D01
stato: bozza
***
```

---

## 5. LLM wiki e agenti: come si inseriscono

### 5.1 LLM wiki stile Karpathy

L’idea di LLM wiki è:

- LLM + agenti non rispondono solo “al volo”, ma aggiornano un wiki persistente
- le risposte sostanziali diventano nuove pagine o aggiornano pagine esistenti
- la knowledge base *compone* nel tempo invece di restare effimera

Nel mio caso:

- layer “Raw” = `inbox/`
- layer “Wiki” = `stazione-knowledge/docs/` + eventuali pagine wiki in altre cartelle
- layer “Schema” = documenti come D01, AGENTS.md, CLAUDE.md/SCHEMA.md che spiegano struttura e regole

Lo scopo di D01 è definire il *schema* e i confini,
in modo che in moduli successivi possa collegare un agente wiki a questo vault
senza perdere controllo.

### 5.2 AGENTS.md e permessi

`AGENTS.md` (pubblico o in `private/infra/`) descrive:

- quali agenti esistono (es. `@curator`, `@auditor`, `@devil`, `@sherman`)
- quali cartelle possono leggere e/o scrivere
- quali operazioni devono sempre lasciare log

Esempio di convenzioni:

- agenti **leggono**:
  - sempre `stazione-knowledge/docs/` (wiki/lezioni)
  - opzionalmente `private/notes/` per lavoro personale
- agenti **scrivono**:
  - solo in cartelle specifiche (es. `private/notes_agent/` o `private/drafts/`)
  - mai direttamente in `stazione-knowledge/docs/` senza review umana

---

## 6. Backup, sicurezza, privacy

### 6.1 Backup

Minimo indispensabile:

- `Stazione/` sincronizzata su:
  - SSD esterno o NAS
  - servizio cloud (GitHub per repo pubblico, altro per privato)

- per il repo pubblico:
  - Git è già un backup incrementale
  - eventuali tag o release per milestone importanti

### 6.2 Privacy e separazione

Anche se qui non tratto dati classificati:

- distinguo chiaramente fra:
  - contenuti pubblicabili (lezioni, schemi, materiali didattici)
  - contenuti sensibili (casi studio reali, dati di terzi, log di lavoro)
- tutto ciò che non deve mai uscire va in:
  - repo privati
  - `private/` non sincronizzato su servizi esterni che non controllo

---

## 7. Workflow quotidiano (bozza)

Un flusso minimo di lavoro:

1. **Quando trovo materiale interessante**  
   - lo salvo in `inbox/` (PDF, MD con link, ritaglio web)

2. **Quando studio o distillo**  
   - creo/aggiorno una nota in `private/notes/` con sintesi, concetti chiave, domande
   - se il contenuto è “modello” (riutilizzabile), creo/aggiorno una lezione Dxx in `docs/`

3. **Quando faccio un passo significativo**  
   - `git add`, `git commit`, `git push` nel repo `stazione-knowledge`
   - opzionale: commit separati per note private in un repo dedicato

4. **Periodicamente**  
   - rivedo `index.md` per vedere dove mancano lezioni
   - aggiorno la tabella D01–D16 con titoli e livelli più accurati
   - aggiorno `AGENTS.md` se il modo di usare agenti/LLM cambia

---

## 8. Laboratori ed esercizi

### Laboratorio 1 — Creare la Stazione base

**Obiettivo:** avere la struttura di cartelle e il repo Git pronti su una macchina (Mac o Windows).

**Passi:**

1. Creare la cartella `Stazione/` in una posizione comoda (home o SSD esterno).
2. Clonare il repo `stazione-knowledge` dentro `Stazione/`.
3. Creare `private/` e `inbox/` accanto a `stazione-knowledge/`.
4. Aprire `README.md` e `index.md` dal filesystem locale, verificare i link alle lezioni.

**Deliverable:**

- screenshot o nota che descrive dove si trova `Stazione/` e come è strutturata.

---

### Laboratorio 2 — Primo vault Obsidian

**Obiettivo:** vedere la knowledge base dal punto di vista di Obsidian.

**Passi:**

1. Aprire Obsidian e creare/aprire un vault puntando alla cartella `Stazione/`.
2. Verificare che `stazione-knowledge/`, `private/` e `inbox/` compaiano nella vista file.
3. Aprire `docs/D01-workspace-llm-wiki.md` da Obsidian e aggiungere un piccolo commento personale
   (es. una sezione “Note personali” in fondo, anche se non verrà pubblicata).

**Deliverable:**

- screenshot della vista dei file Obsidian con la struttura `Stazione/`;
- breve nota in `private/notes/` che descrive l’impressione sull’uso di Obsidian con il repo.

---

### Laboratorio 3 — Primo flusso ICM: da sorgente a nota wiki

**Obiettivo:** esercitarsi nel flusso “sorgente → distillazione → wiki” usando una singola fonte reale.

**Passi:**

1. Scegliere un articolo, video o documento OSINT/AI e salvarlo in `inbox/`
   (es. file PDF o `.md` con link).
2. Creare una nota distillata in `private/notes/` che riassume i concetti chiave,
   include link alla sorgente e annota eventuali dubbi.
3. Aggiungere un riferimento nel repo pubblico:
   - per esempio una riga in una sezione “Letture consigliate” di una lezione Dxx,
     descrivendo in 2–3 frasi cosa aggiunge quella fonte al percorso.

**Deliverable:**

- file sorgente in `inbox/`;
- nota distillata in `private/notes/`;
- aggiornamento in una lezione Dxx che punta alla nota o alla sorgente.

---

### Laboratorio 4 — Definire AGENTS.md e regole di base

**Obiettivo:** preparare il terreno per agenti/LLM che lavorano sul vault senza creare caos.

**Passi:**

1. Creare un file `AGENTS.md` (nel repo pubblico o in `private/infra/`) con:
   - elenco dei tipi di agenti che intendo usare (es. `@curator`, `@auditor`, `@devil`, `@sherman`);
   - permessi e limiti (cosa possono leggere, cosa possono scrivere, dove non toccano nulla).
2. Aggiungere almeno 3–5 regole chiare per proteggere il vault, per esempio:
   - “gli agenti non modificano mai i file in `stazione-knowledge/docs/` direttamente”;
   - “le modifiche passano prima da `private/notes/` o `private/drafts/` e poi, se verificate, vengono promosse”;
   - “ogni esecuzione di un agente deve lasciare un log minimal in una nota dedicata o in un file JSONL”.

**Deliverable:**

- file `AGENTS.md` con una prima bozza di policy;
- eventuale nota in `private/notes/` che documenta come usare questi agenti nei moduli successivi.

---

## 9. Rubriche e checklist

### Checklist — Setup D01 completo

- [ ] Esiste la cartella `Stazione/` con:
  - [ ] `stazione-knowledge/` (repo clonato e funzionante)
  - [ ] `private/` (note e codice non pubblici)
  - [ ] `inbox/` (materiale grezzo)
- [ ] Posso aprire il vault Obsidian puntando a `Stazione/` senza errori.
- [ ] Riesco a leggere D01 sia da Obsidian sia da GitHub / GitHub Pages.
- [ ] Ho creato almeno una nota distillata a partire da una sorgente reale.
- [ ] Esiste un file `AGENTS.md` con permessi/limiti anche se abbozzati.
- [ ] Ho deciso dove verranno salvati i backup (cloud / disco esterno / altro) e l’ho annotato.

### Errori tipici da evitare

- usare Google Drive o altro cloud come **unica** fonte della verità, senza clone locale;
- mischiare materiale grezzo (`inbox/`) con note distillate e lezioni (stesso posto, nessuna distinzione);
- lasciare agenti/LLM liberi di modificare qualsiasi file senza policy o log;
- non versionare il repo `stazione-knowledge` (nessun commit/push) e perdere lo storico di modifiche;
- configurare solo una macchina (es. solo Mac) e rendere difficile ripartire da un’altra (es. portatile Windows).

### Segnali che “ho davvero capito” D01

- se si rompe un computer, so esattamente come ripristinare la Stazione altrove;
- so spiegare a voce a un collega come funziona il flusso
  “sorgente → distillazione → nota wiki → uso da parte di agenti”;
- so distinguere chiaramente tra:
  - sorgenti grezze,
  - note distillate,
  - lezioni stabili nel repo pubblico;
- so dire quali cartelle gli agenti possono toccare e quali no.

---

## 10. Come ripartire dopo una pausa

Se torno su D01 dopo giorni o settimane:

1. Apro `index.md` del repo `stazione-knowledge` su GitHub o Obsidian.
2. Controllo la checklist “Setup D01 completo” e marco cosa è già fatto.
3. Scelgo **un solo laboratorio breve** (1 o 2) e lo completo in una sessione da 25–40 minuti.
4. Aggiorno `AGENTS.md` o una nota in `private/notes/` con:
   - cosa ho fatto oggi
   - cosa vorrei fare alla prossima sessione.

L’obiettivo non è “finire tutto D01 in una volta”, ma **ricostruire il contesto** rapidamente
e lasciare tracce chiare per il “me del futuro”.

---

## 11. Risorse consigliate

### 11.1 Workspace, second brain e knowledge base

- Adam Bray — *A Personal Git Repo as a Knowledge Base Wiki*  
  Idea di usare un singolo repo Git come wiki personale in Markdown.  
  https://dev.to/adam_b/a-personal-git-repo-as-a-knowledge-base-wiki-j51

- Articoli su personal knowledge base con Markdown + Git  
  Approcci “docs as code” per knowledge base personali.  
  https://lifetips.alibaba.com/tech-efficiency/personal-knowledge-base-with-markdown-git  
  https://marklowg.medium.com/creating-a-personal-knowledgebase-on-github-d1d8bb9222a4

- Esempi di knowledge base pubblica in Markdown su GitHub  
  https://github.com/exasol/public-knowledgebase  
  https://github.com/sketchbuch/obsidian-knowledge-base

- Nagi’s Personal Knowledge Base (Obsidian vault pubblica)  
  Esempio di vault Obsidian usato come knowledge base personale versionata con Git.  
  https://github.com/brklntmhwk/npkb

### 11.2 Obsidian, LLM wiki e second brain AI

- Karpathy-style LLM wiki per Obsidian  
  Template di vault e workflow per wiki mantenuta da LLM.  
  https://github.com/shannhk/llm-wikid

- LLM-KB — LLM Knowledge Base con Obsidian  
  Architettura “LLM mantiene un wiki persistente” invece di RAG puro.  
  https://ocholuo.github.io/posts/LLM-KnowledgeBase-Obsidian/

- Articoli su knowledge base machine-readable con Obsidian  
  Esempi di uso di frontmatter e strutture per rendere la knowledge base leggibile da agenti.

### 11.3 Corsi universitari di riferimento (ML / NLP) da usare più avanti

Queste risorse non si studiano in D01, ma le collego già qui
come ancore per moduli successivi (D04, D07, D09).

- Stanford CS229 — Machine Learning  
  Sito corso: https://cs229.stanford.edu/  
  Syllabus: https://cs229.stanford.edu/syllabus-new.html  
  Versione online: https://online.stanford.edu/courses/cs229-machine-learning

- Stanford CS224N — Natural Language Processing with Deep Learning  
  Sito corso: https://web.stanford.edu/class/cs224n/  
  Archivio recente: https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/  
  Versione online:  
  https://online.stanford.edu/courses/cs224n-natural-language-processing-deep-learning