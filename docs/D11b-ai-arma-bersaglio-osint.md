# D11b — AI come arma e come bersaglio nell'OSINT

## Meta-modulo D11b

**Target**  
Me stesso oggi, e chiunque voglia capire come l'AI (in particolare i LLM e i generatori di contenuti)
stia trasformando il panorama OSINT: sia come **arma offensiva** (disinformazione, deepfake, campagne
di influenza) sia come **bersaglio** (infrastrutture AI esposte, vulnerabilità, rischi di supply chain).

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D11 — OSINT avanzato e discipline principali

**Nota esplicita**:  
**NON serve D08 (Deep Learning e PyTorch)**. In questo modulo non si allenano modelli,
si studiano gli **effetti operativi** dell'AI su OSINT, disinformazione e sicurezza.

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - AI come arma offensiva (disinformazione, deepfake, campagne)  
  - AI come bersaglio OSINT (infrastrutture esposte, vulnerabilità MCP)  
  - cenni a rilevamento e provenance

- **Modalità standard (~8–10 ore)**  
  - analisi di casi reali di deepfake e campagne di influenza  
  - ricognizione passiva su infrastrutture AI (endpoint LLM, vector DB, server MCP)  
  - tecniche di rilevamento del sintetico e standard di provenance (C2PA)  
  - pattern per agenti autonomi OSINT con umano nel loop

- **Modalità deep dive (più giornate)**  
  - studio approfondito di paper su rilevamento deepfake e watermarking  
  - sperimentazione di pipeline OSINT con agenti autonomi (con log auditabili)  
  - analisi di vulnerabilità MCP e supply chain risk in scenari realistici

**Quando considerare il modulo "completato"**

- so descrivere come l'AI viene usata come arma offensiva nella disinformazione
- so identificare infrastrutture AI esposte come bersagli OSINT (senza accesso non autorizzato)
- conosco lo stato dell'arte del rilevamento del sintetico e i suoi limiti
- so progettare agenti autonomi OSINT mantenendo tracciabilità e umano nel loop
- ho almeno un caso studio documentato (disinformazione o infrastruttura AI)

---

## Perché questo documento

Dopo D11 ho metodologia OSINT, ma mi manca una comprensione approfondita di:

- come l'AI stia **cambiando la disinformazione** (deepfake, campagne di influenza automatizzate)
- come le **infrastrutture AI** (LLM self-hosted, vector DB, server MCP) siano esse stesse bersagli OSINT
- come **rilevare contenuti sintetici** e valutare standard di provenance (C2PA, watermarking)
- come usare **agenti autonomi** in pipeline OSINT reali senza perdere tracciabilità e controllo

Questo modulo è **operativo e difensivo**: non insegna a creare deepfake o sfruttare vulnerabilità,
ma a **riconoscerli, analizzarli e difendersi**.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere come l'AI viene usata come arma offensiva nella disinformazione
- identificare infrastrutture AI esposte (endpoint LLM, vector DB, server MCP) come bersagli OSINT
- riconoscere deepfake e contenuti sintetici (testo, immagini, video, audio)
- valutare standard di provenance e watermarking (C2PA, ecc.)
- progettare agenti autonomi OSINT con umano nel loop e log auditabili

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. AI come arma offensiva nella disinformazione.
2. AI come bersaglio OSINT (infrastrutture esposte, vulnerabilità MCP).
3. Rilevamento del sintetico e provenance (C2PA, watermarking).
4. Agenti autonomi per pipeline OSINT reali (con umano nel loop).

---

## 2. AI come arma offensiva nella disinformazione

### 2.1 Contenuti sintetici su scala

L'AI permette di generare **contenuti sintetici** (testo, immagini, video, audio) su scala industriale:

- **testo**: articoli, post social, commenti automatizzati (LLM)
- **immagini**: deepfake, immagini generate (DALL-E, Midjourney, Stable Diffusion)
- **video**: deepfake video (face swap, lip sync, voice cloning)
- **audio**: voice cloning, sintesi vocale realistica

Implicazioni per OSINT:

- difficoltà crescente nel distinguere reale da sintetico
- amplificazione di narrazioni false o manipolate
- necessità di nuovi strumenti di rilevamento e verifica

### 2.2 Deepfake: tecniche attuali e casi reali

**Deepfake** = contenuti sintetici (video, audio, immagini) che sembrano reali.

Tecniche principali:

- **face swap**: sostituzione del volto in video
- **lip sync**: sincronizzazione labiale con audio sintetico
- **voice cloning**: sintesi vocale basata su campioni reali
- **generazione completa**: video/audio generati da zero (es. Sora, ElevenLabs)

Casi reali documentati:

- **2022**: deepfake del presidente ucraino Zelensky che invita alla resa (diffuso su social russi)
- **2023**: audio deepfake di un politico slovacco che parla di brogli elettorali (influenza elezioni)
- **2024**: video deepfake di un CEO che annuncia risultati finanziari falsi (manipolazione mercati)

Riferimenti:

- [Deepfake Tracker (Stanford)](https://deepfaketracker.stanford.edu/)
- [EUvsDisinfo - Deepfakes](https://euvsdisinfo.eu/deepfakes-and-synthetic-media)

### 2.3 Campagne di influenza assistite da LLM

LLM usati per:

- **persona sintetiche**: profili social fake gestiti da LLM (post, commenti, interazioni)
- **amplificazione automatizzata**: bot che condividono, commentano, likano contenuti
- **generazione di narrazioni**: articoli, post, thread coerenti su larga scala

Pattern tipici:

- stessi temi, stessi nemici, stessi hashtag su piattaforme diverse
- picchi improvvisi di attività su certi topic
- account creati di recente con poca storia ma alta attività

---

## 3. AI come bersaglio OSINT

### 3.1 Infrastrutture AI esposte pubblicamente

Molte organizzazioni deployano infrastrutture AI **senza adeguata sicurezza**:

- **endpoint LLM self-hosted non protetti**: API esposte su Internet senza autenticazione
- **vector database mal configurati**: Chroma, Qdrant, Weaviate accessibili pubblicamente
- **dashboard di monitoring**: Grafana, Kibana esposti senza password

Queste infrastrutture sono **bersagli OSINT legittimi** (osservazione passiva):

- mappatura di endpoint esposti
- identificazione di organizzazioni che usano AI
- valutazione di rischi di data leakage

**Limite etico-legale**: solo osservazione passiva, **mai accesso non autorizzato** (coerente con D11 §7.3).

### 3.2 Vulnerabilità dei server MCP

**MCP (Model Context Protocol)** = protocollo per dare contesto strutturato agli agenti.

Vulnerabilità tipiche:

- **prompt injection su tool esterni**: agenti che eseguono tool con input non validati
- **tool poisoning**: tool di terze parti compromessi che restituiscono dati manipolati
- **permessi eccessivi**: agenti con accesso a file, API, DB senza limiti
- **supply chain risk**: plugin/connector di terze parti con vulnerabilità

Tecniche di ricognizione su server MCP esposti:

- scan di porte e endpoint (solo passivo, mai attivo)
- analisi di metadata esposti (versioni, config)
- identificazione di pattern di uso (log, errori)

Riferimenti:

- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/security) (o documentazione specifica)

---

## 4. Rilevamento del sintetico e provenance

### 4.1 Stato dell'arte del rilevamento

**Rilevamento del sintetico** = tecniche per distinguere contenuti reali da sintetici.

Per **testo**:

- modelli di detection (es. RoBERTa fine-tuned su dataset di testo AI)
- analisi di pattern (ripetizioni, coerenza, stile)
- limiti: i generatori migliorano, i detector diventano meno efficaci

Per **immagini/video**:

- analisi di artefatti (illuminazione, bordi, compressione)
- modelli di detection (es. Microsoft Video Authenticator, Intel FakeCatcher)
- limiti: deepfake di alta qualità sono sempre più difficili da rilevare

Per **audio**:

- analisi di spettro, artefatti vocali
- modelli di detection (es. Resemble Detect, Microsoft Audio Authenticator)
- limiti: voice cloning di alta qualità è quasi indistinguibile

**Arms race**: i generatori migliorano più velocemente dei detector.

Riferimenti:

- [Deepfake Detection Challenge (Google)](https://deepfakedetectionchallenge.ai/)
- [Intel FakeCatcher](https://www.intel.com/content/www/us/en/artificial-intelligence/fakecatcher.html)

### 4.2 Standard di provenance e watermarking

**Provenance** = tracciare origine e modifiche di un contenuto.

**C2PA (Coalition for Content Provenance and Authenticity)**:

- standard per firmare digitalmente contenuti (foto, video, audio)
- metadata criptati che indicano:
  - chi ha creato il contenuto
  - quando
  - con quale strumento
  - eventuali modifiche

**Watermarking**:

- segnali invisibili inseriti nei contenuti per indicare origine sintetica
- es. watermark su immagini generate da DALL-E 3, Stable Diffusion

**Affidabilità**:

- C2PA è robusto ma richiede adozione diffusa (non tutti i tool lo supportano)
- watermarking può essere rimosso o alterato

**Adozione attuale**:

- alcuni generatori (DALL-E 3, Midjourney) applicano watermark
- C2PA supportato da Adobe, Microsoft, Sony, ma non ancora universale

Riferimenti:

- [C2PA Specification](https://c2pa.org/specifications/)
- [Content Credentials (Adobe)](https://contentcredentials.org/)

---

## 5. Agenti autonomi per pipeline OSINT reali

### 5.1 Differenza tra LLM-assistente e agente autonomo

**LLM-assistente**:

- risponde a prompt dell'utente
- non agisce autonomamente nel mondo
- nessun tool calling automatico

**Agente autonomo**:

- pianifica e esegue task multi-step
- usa tool (ricerca web, lettura file, query DB)
- può operare per ore/giorni senza intervento umano

### 5.2 Rischi degli agenti autonomi

- **allucinazioni a catena**: agente basa azioni su informazioni false, peggiorando la situazione
- **perdita di tracciabilità**: difficile capire cosa ha fatto l'agente e perché
- **over-trust**: fidarsi ciecamente dell'agente senza verificare

### 5.3 Pattern per mantenere umano nel loop

- **approval step**: agente chiede approvazione prima di azioni critiche (es. pubblicare report)
- **log auditabili**: tracciare tutte le azioni (tool, input, output) in file leggibili
- **validation step**: un secondo agente (o umano) verifica risultati prima di consolidare
- **limiti di azione**: whitelist di tool e azioni permesse, limiti di step

---

## 6. Laboratori ed esercizi

### Laboratorio 1 — Analisi di un deepfake documentato

**Obiettivo:** analizzare un caso reale di deepfake.

**Passi:**

1. Scegliere un caso documentato (es. deepfake Zelensky 2022, politico slovacco 2023).
2. Raccogliere fonti (articoli, report, analisi tecniche).
3. Analizzare:
   - come è stato creato (tecnica)
   - come è stato diffuso (piattaforme, amplificazione)
   - impatto (reazioni, fact-checking)
4. Annotare:
   - segnali di deepfake (se identificabili)
   - lezioni per OSINT

**Deliverable:**

- documento di analisi (1–2 pagine)
- nota con osservazioni

---

### Laboratorio 2 — Ricognizione passiva su infrastrutture AI

**Obiettivo:** identificare infrastrutture AI esposte (senza accesso non autorizzato).

**Passi:**

1. Usare motori di ricerca (Google, Shodan, Censys) per cercare:
   - endpoint LLM esposti (es. `/v1/chat/completions`)
   - vector DB esposti (es. Chroma, Qdrant su porte standard)
   - dashboard di monitoring esposte
2. Documentare:
   - quali organizzazioni sembrano avere infrastrutture esposte
   - quali rischi (data leakage, abuso)
3. **Non accedere mai** senza autorizzazione.
4. Annotare:
   - pattern ricorrenti
   - implicazioni per sicurezza

**Deliverable:**

- documento di ricognizione (solo passiva)
- nota con osservazioni e limiti etici

---

### Laboratorio 3 — Test di rilevamento sintetico

**Obiettivo:** sperimentare strumenti di rilevamento.

**Passi:**

1. Scegliere un tool di detection (es. Intel FakeCatcher, Microsoft Video Authenticator, o detector di testo).
2. Testare su:
   - contenuti reali (baseline)
   - contenuti sintetici (se disponibili legalmente)
3. Valutare:
   - accuratezza (veri/falsi positivi)
   - limiti pratici
4. Annotare:
   - quanto è affidabile il tool
   - scenari in cui è utile/inutile

**Deliverable:**

- report di test (risultati, limiti)
- nota con osservazioni

---

### Laboratorio 4 — Pipeline OSINT con agente autonomo e log auditabili

**Obiettivo:** progettare una pipeline OSINT con agente autonomo.

**Passi:**

1. Scegliere un task OSINT (es. raccolta fonti su un tema, analisi di disinformazione).
2. Progettare agente autonomo con:
   - tool (ricerca web, RAG, analisi)
   - pianificazione multi-step
3. Implementare:
   - log auditabili (file `LOG.md` con tutte le azioni)
   - approval step per azioni critiche
   - validation step (secondo agente o umano)
4. Testare la pipeline e annotare:
   - allucinazioni o errori
   - tracciabilità delle fonti
   - utilità del log

**Deliverable:**

- script/pipeline agente
- log auditabile (`LOG.md`)
- nota con osservazioni

---

## 7. Rubriche e checklist

### Checklist — D11b completato

- [ ] So descrivere come l'AI viene usata come arma offensiva nella disinformazione.
- [ ] So identificare infrastrutture AI esposte come bersagli OSINT (senza accesso non autorizzato).
- [ ] Riconosco deepfake e contenuti sintetici (testo, immagini, video, audio).
- [ ] Conosco standard di provenance e watermarking (C2PA, ecc.) e i loro limiti.
- [ ] So progettare agenti autonomi OSINT con umano nel loop e log auditabili.
- [ ] Ho analizzato almeno un caso reale di deepfake o infrastruttura AI.

### Errori tipici da evitare

- confondere osservazione passiva (legale) con accesso non autorizzato (illegale).
- fidarsi ciecamente di detector di deepfake (hanno limiti significativi).
- sottovalutare rischi di supply chain (plugin/connector di terze parti).
- usare agenti autonomi senza log auditabili (impossibile debug o audit).
- ignorare limiti etico-legali nella ricognizione di infrastrutture AI.

### Segnali che "ho davvero capito" D11b

- posso spiegare a un colleghi come l'AI stia cambiando disinformazione e OSINT.
- so riconoscere pattern di deepfake e campagne di influenza assistite da LLM.
- so identificare infrastrutture AI esposte senza violare limiti etico-legali.
- so progettare agenti autonomi OSINT mantenendo tracciabilità e controllo umano.
- vedo l'AI sia come opportunità sia come rischio, non come magia.

---

## 8. Come ripartire dopo una pausa

Se torno su D11b dopo giorni o settimane:

1. Riapro un caso studio (deepfake o infrastruttura AI) già analizzato.
2. Rileggo analisi e log.
3. Aggiungo una piccola attività:
   - nuovo caso di deepfake da analizzare
   - nuova ricognizione passiva su infrastrutture AI
   - miglioramento pipeline agente (log, approval step)
4. Aggiorno una nota con:
   - cosa ho aggiunto
   - nuove intuizioni o domande

Scopo: mantenere viva la consapevolezza su AI come arma e bersaglio nell'OSINT.

---

## 9. Risorse consigliate

### 9.1 Deepfake e disinformazione

- **Deepfake Tracker (Stanford)**  
  https://deepfaketracker.stanford.edu/  

- **EUvsDisinfo - Deepfakes and Synthetic Media**  
  https://euvsdisinfo.eu/deepfakes-and-synthetic-media  

- **Deepfake Detection Challenge (Google)**  
  https://deepfakedetectionchallenge.ai/  

### 9.2 Sicurezza AI e vulnerabilità

- **OWASP Top 10 for Large Language Model Applications**  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/  

- **Intel FakeCatcher**  
  https://www.intel.com/content/www/us/en/artificial-intelligence/fakecatcher.html  

- **MCP Security Best Practices**  
  https://modelcontextprotocol.io/security  

### 9.3 Provenance e watermarking

- **C2PA Specification**  
  https://c2pa.org/specifications/  

- **Content Credentials (Adobe)**  
  https://contentcredentials.org/  

### 9.4 Strumenti di detection

- **Microsoft Video Authenticator**  
  https://www.microsoft.com/en-us/ai/video-authenticator  

- **Resemble Detect (audio)**  
  https://www.resemble.ai/detect  

Queste risorse non vanno studiate per intero: D11b serve a darti una mappa operativa
per capire AI come arma e bersaglio nell'OSINT, e a collegarti a tool/paper quando serve approfondire.