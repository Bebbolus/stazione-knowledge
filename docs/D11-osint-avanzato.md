# D11 — OSINT avanzato e discipline principali

## Meta-modulo D11

**Target**  
Me stesso oggi, e chiunque voglia praticare OSINT in modo strutturato e professionale:
metodologie, fonti, correlazione di eventi, disinformazione, OPSEC, e integrazione con LLM e RAG.

**Prerequisiti consigliati**

- D01 — Workspace local-first, Git, Obsidian, LLM wiki
- D03 — Data foundations (NumPy, Pandas, SQL, data quality)
- D09 — Transformers, LLM e inference engineering
- D10 — RAG, knowledge base e grafi OSINT

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - cos’è OSINT e perché è rilevante oggi  
  - ciclo di vita dell’intelligence (planning, collection, processing, analysis, dissemination)  
  - fonti OSINT principali (web, social, media, dati pubblici)

- **Modalità standard (~8–10 ore)**  
  - metodologie di ricerca e correlazione  
  - disinformazione e campagne di influenza  
  - OPSEC base per analisti OSINT  
  - integrazione con LLM/RAG per analisi e report

- **Modalità deep dive (più giornate)**  
  - casi studio complessi (geopolitica, crimine organizzato, cyber threat)  
  - costruzione di knowledge base OSINT (documenti + grafi)  
  - automazione di flussi con agenti e script

**Quando considerare il modulo “completato”**

- so descrivere il ciclo di intelligence e il ruolo dell’OSINT
- so pianificare e condurre una ricerca OSINT su un tema complesso
- so riconoscere pattern di disinformazione e campagne coordinate
- applico OPSEC base per proteggere me stesso e le mie fonti
- ho almeno un caso studio OSINT documentato (note, fonti, analisi, report)

---

## Perché questo documento

Dopo D10 ho gli strumenti per costruire knowledge base e RAG, ma mi manca una **metodologia OSINT solida**:

- come pianificare una ricerca
- come selezionare e valutare le fonti
- come correlare eventi e entità
- come riconoscere disinformazione
- come proteggere me stesso e il lavoro

Questo modulo mette insieme:

- metodologie di intelligence tradizionali (ciclo di intelligence)
- pratiche OSINT moderne (web, social, dati aperti)
- integrazione con LLM/RAG per scalare analisi e report

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere il ciclo di intelligence e il ruolo dell’OSINT
- pianificare una raccolta OSINT su un tema (geopolitica, sicurezza, economia, ecc.)
- usare fonti OSINT principali (motori di ricerca, social, registri, mappe, ecc.)
- correlare eventi, entità e relazioni in un caso studio
- riconoscere pattern di disinformazione e campagne coordinate
- applicare OPSEC base per analisti OSINT
- integrare LLM/RAG per analisi, sintesi e report

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Cos’è OSINT e perché è rilevante oggi.
2. Ciclo di intelligence e ruolo dell’OSINT.
3. Fonti OSINT: categorie e esempi.
4. Metodologie di ricerca e correlazione.
5. Disinformazione e campagne di influenza.
6. OPSEC per analisti OSINT.
7. Integrazione con LLM/RAG e knowledge base.

---

## 2. Cos’è OSINT

### 2.1 Definizione

**OSINT** (Open Source Intelligence) = intelligence prodotta da fonti aperte e pubblicamente accessibili:

- web (siti, forum, blog)
- social media (X/Twitter, Facebook, Telegram, TikTok, ecc.)
- media tradizionali (TV, radio, giornali)
- dati pubblici (registri, bilanci, bandi, dati governativi)
- immagini e mappe (satellitari, street view, geolocalizzazione)

Non è:

- hacking o accesso non autorizzato a sistemi
- raccolta di dati coperti da segreto o classificati

### 2.2 Perché OSINT oggi

Fattori che hanno reso l’OSINT centrale:

- esplosione di dati digitali e social
- crisi geopolitiche, conflitti, disinformazione
- strumenti accessibili (motori di ricerca, API, LLM)
- domanda di analisi rapida e basata su fonti verificabili

Riferimenti:

- [NATO OSINT overview](https://www.osintframework.com/)
- [OSINT Handbook (varie edizioni online)](https://www.osinthandbook.com/)

---

## 3. Ciclo di intelligence

### 3.1 Fasi del ciclo

Modello classico (es. intelligence community USA/NATO):

1. **Planning & Direction**  
   - definire obiettivi, domande, priorità
   - identificare stakeholder e destinatari

2. **Collection**  
   - raccogliere informazioni da fonti OSINT (e altre se disponibili)

3. **Processing**  
   - organizzare, tradurre, normalizzare dati
   - estrarre entità, relazioni, eventi

4. **Analysis**  
   - correlare informazioni
   - costruire ipotesi, scenari, valutazioni

5. **Dissemination**  
   - produrre report, briefing, dashboard
   - distribuire a chi deve decidere o agire

Il ciclo è iterativo: i risultati alimentano nuove domande e nuove raccolte.

### 3.2 Ruolo dell’OSINT nel ciclo

OSINT è soprattutto in:

- **Collection**: fonti aperte
- **Processing**: pulizia, traduzione, estrazione
- **Analysis**: correlazione, valutazione, scenari

Ma può influenzare anche:

- **Planning**: nuove domande da pattern osservati
- **Dissemination**: report pubblici o interni basati su OSINT

---

## 4. Fonti OSINT

### 4.1 Categorie principali

1. **Web generale**  
   - motori di ricerca (Google, Bing, DuckDuckGo)  
   - siti istituzionali, ONG, think tank  
   - forum, blog, paste site

2. **Social media**  
   - X/Twitter, Facebook, Instagram, TikTok  
   - Telegram, Discord, Reddit  
   - LinkedIn (professionale)

3. **Media tradizionali**  
   - agenzie di stampa (Reuters, AP, AFP)  
   - giornali, TV, radio

4. **Dati pubblici**  
   - registri imprese, bilanci, appalti  
   - dati governativi (open data)  
   - documenti legali, sentenze

5. **Immagini e mappe**  
   - Google Maps, Bing Maps, OpenStreetMap  
   - immagini satellitari (Sentinel, Landsat, Maxar)  
   - EXIF, geolocalizzazione

6. **Cyber e sicurezza**  
   - CVE, advisory, blog di vendor  
   - leak pubblici (con cautela legale/etica)  
   - forum e marketplace (osservazione passiva)

### 4.2 Valutare le fonti

Criteri:

- **affidabilità**: quanto la fonte è attendibile storicamente
- **proximity**: quanto è vicina all’evento (testimone diretto vs terzo)
- **corroborazione**: quante fonti indipendenti confermano
- **trasparenza**: quanto la fonte spiega metodi e limiti

Buona pratica:

- non basarsi mai su una sola fonte
- tracciare sempre fonte e data nelle note

---

## 5. Metodologie di ricerca e correlazione

### 5.1 Pianificare la ricerca

Prima di cercare:

- definire domande chiave (es. “Chi?”, “Cosa?”, “Dove?”, “Quando?”, “Perché?”)
- identificare entità di interesse (persone, organizzazioni, luoghi, eventi)
- elencare fonti potenziali per ciascuna domanda

### 5.2 Tecniche di ricerca

- **query avanzate** (Google dorks, operatori booleani)
- **ricerca inversa** (immagini, numeri di telefono, email)
- **timeline** (ordinare eventi per data)
- **geolocalizzazione** (mappe, shadow, landmark)

### 5.3 Correlazione

- collegare entità tramite relazioni (lavora_per, partecipa_a, cita, ecc.)
- costruire grafi mentali o reali (Neo4j, Obsidian graph)
- cercare pattern:
  - stesse persone in contesti diversi
  - stesse narrazioni su piattaforme diverse
  - coordinazione temporale (stessi orari, stessi hashtag)

---

## 6. Disinformazione e campagne di influenza

### 6.1 Cos’è disinformazione

- **misinformation**: informazioni false, ma senza intento di ingannare
- **disinformation**: informazioni false, diffuse intenzionalmente per ingannare
- **malinformation**: informazioni vere usate in modo dannoso (es. doxxing)

### 6.2 Pattern comuni

- **narrative ricorrenti** (stessi temi, stessi nemici)
- **amplificazione coordinata** (bot, reti di account)
- **uso emotivo** (paura, rabbia, indignazione)
- **fonti opache** (siti senza redazione, domini sospetti)

### 6.3 Riconoscere campagne

Segnali:

- stessi messaggi su piattaforme diverse con piccole varianti
- picchi improvvisi di attività su certi hashtag/topic
- account creati di recente con poca storia
- immagini/video decontestualizzati

Strumenti:

- fact-checking (Snopes, Bellingcat, Pagella Politica, ecc.)
- analisi di reti (chi condivide cosa, quando)
- reverse image search

Riferimenti:

- [Bellingcat guides](https://www.bellingcat.com/category/resources/)
- [EUvsDisinfo](https://euvsdisinfo.eu/)

---

## 7. OPSEC per analisti OSINT

### 7.1 Perché OPSEC

**OPSEC** (Operational Security) = proteggere sé stessi, le proprie fonti e il proprio lavoro:

- evitare di esporre identità, ubicazione, abitudini
- proteggere fonti sensibili (es. whistleblower)
- ridurre rischi di retaliation, doxxing, sorveglianza

### 7.2 Pratiche base

- **identità separate**: account dedicati per OSINT, non mischiati con vita personale
- **browser e profili isolati**: profili separati, container, VM
- **VPN / Tor**: nascondere IP, soprattutto per ricerche sensibili
- **gestione password**: password manager, 2FA
- **log e trace**: tenere traccia di cosa si fa, per audit e sicurezza

### 7.3 Aspetti legali ed etici

- rispettare termini di servizio delle piattaforme
- non accedere a sistemi senza autorizzazione
- rispettare privacy e leggi locali (GDPR, ecc.)
- distinguere tra osservazione passiva e attività intrusive

---

## 8. Integrazione con LLM/RAG e knowledge base

### 8.1 Pattern di uso LLM

LLM come:

- **assistente di ricerca**: suggerire query, fonti, angolazioni
- **sintetizzatore**: riassumere documenti, estrarre punti chiave
- **correlatore**: aiutare a collegare entità e eventi
- **redattore**: bozze di report, briefing, timeline

Attenzione:

- verificare sempre le affermazioni del LLM su fonti primarie
- non usare LLM come unica fonte di verità

### 8.2 RAG per OSINT

Usare RAG per:

- Q&A su grandi volumi di documenti (report, articoli, trascrizioni)
- tracciare fonti delle risposte (citazioni)
- ridurre allucinazioni su fatti specifici

### 8.3 Knowledge base OSINT

Costruire una knowledge base:

- documenti (PDF, Markdown, HTML) in vector DB
- grafi (entità, relazioni, eventi) in Neo4j
- note in Obsidian con link a fonti e analisi

Flusso:

1. raccolta → 2. processing → 3. storage (doc + grafo) → 4. retrieval → 5. analisi/report

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Pianificare una ricerca OSINT

**Obiettivo:** pianificare una ricerca su un tema reale.

**Passi:**

1. Scegliere un tema (es. conflitto geopolitico, campagna elettorale, crisi economica).
2. Definire 3–5 domande chiave.
3. Elencare fonti potenziali per ciascuna domanda.
4. Scrivere un mini-piano di ricerca (fonti, query, timeline).
5. Annotare:
   - quali fonti sono più promettenti
   - quali rischi (disinformazione, bias)

**Deliverable:**

- documento con piano di ricerca
- nota con riflessioni su fonti e rischi

---

### Laboratorio 2 — Ricerca e correlazione

**Obiettivo:** condurre una ricerca OSINT e correlare informazioni.

**Passi:**

1. Eseguire ricerche secondo il piano del laboratorio 1.
2. Raccogliere fonti (link, screenshot, note).
3. Estrarre entità (persone, organizzazioni, luoghi, eventi).
4. Collegare entità con relazioni (lavora_per, partecipa_a, cita, ecc.).
5. Costruire una timeline o un grafo semplice.
6. Annotare:
   - connessioni scoperte
   - punti deboli (mancanze, contraddizioni)

**Deliverable:**

- raccolta fonti (note, link)
- timeline o grafo
- nota con analisi e connessioni

---

### Laboratorio 3 — Analisi di disinformazione

**Obiettivo:** riconoscere pattern di disinformazione.

**Passi:**

1. Scegliere un tema con narrazioni contrastanti (es. conflitto, elezioni, pandemia).
2. Raccogliere post/articoli da fonti diverse.
3. Confrontare narrazioni:
   - stessi fatti raccontati in modo diverso?
   - stesse immagini/video usati in contesti diversi?
4. Cercare segnali di coordinazione (stessi orari, stessi hashtag).
5. Annotare:
   - pattern di disinformazione individuati
   - fonti più affidabili e perché

**Deliverable:**

- raccolta di post/articoli
- nota con analisi di narrazioni e pattern

---

### Laboratorio 4 — OPSEC e setup operativo

**Obiettivo:** configurare un ambiente OSINT sicuro.

**Passi:**

1. Creare account dedicati per OSINT (email, social, forum).
2. Configurare browser con profili separati (es. Chrome profiles, Firefox containers).
3. Valutare uso di VPN o Tor per ricerche sensibili.
4. Configurare password manager e 2FA.
5. Scrivere una mini-policy OPSEC personale:
   - cosa fare/non fare
   - come gestire fonti sensibili
   - come tracciare attività

**Deliverable:**

- documento con policy OPSEC
- nota con setup e riflessioni

---

## 10. Rubriche e checklist

### Checklist — D11 completato

- [ ] So descrivere il ciclo di intelligence e il ruolo dell’OSINT.
- [ ] Ho pianificato e condotto una ricerca OSINT su un tema reale.
- [ ] So correlare entità ed eventi in un caso studio.
- [ ] Riconosco pattern di disinformazione e campagne coordinate.
- [ ] Applico OPSEC base per proteggere me stesso e le fonti.
- [ ] Ho integrato LLM/RAG in almeno un flusso di analisi OSINT.
- [ ] Ho un caso studio OSINT documentato (note, fonti, analisi, report).

### Errori tipici da evitare

- basarsi su una sola fonte o su fonti non verificate.
- confondere opinioni con fatti verificati.
- sottovalutare rischi OPSEC (account personali, IP esposto, ecc.).
- usare LLM come unica fonte di verità senza verificare su fonti primarie.
- non tracciare fonti e data nelle note (impossibile audit o verifica).

### Segnali che “ho davvero capito” D11

- posso prendere un tema complesso e pianificare una ricerca OSINT strutturata.
- so riconoscere narrazioni sospette e campagne coordinate.
- applico OPSEC in modo naturale, non come “extra”.
- uso LLM/RAG come amplificatori, non come sostituti del pensiero critico.
- so produrre report chiari, tracciati e utili per decisori.

---

## 11. Come ripartire dopo una pausa

Se torno su D11 dopo giorni o settimane:

1. Riapro un caso studio OSINT già fatto.
2. Rileggo note, fonti, analisi.
3. Aggiungo una piccola attività:
   - nuova fonte da controllare
   - nuova query per aggiornare timeline
   - nuova entità da collegare nel grafo
4. Aggiorno una nota con:
   - cosa ho aggiunto
   - cosa è cambiato nella comprensione del caso

Scopo: mantenere viva la metodologia OSINT e la traccia delle fonti.

---

## 12. Risorse consigliate

### 12.1 OSINT e metodologia

- **NATO OSINT overview**  
  Panoramica sul ruolo dell’OSINT nella NATO.  
  https://www.osintframework.com/  

- **OSINT Handbook**  
  Raccolta di risorse e metodologie OSINT.  
  https://www.osinthandbook.com/  

- **Bellingcat guides**  
  Guide pratiche su OSINT, geolocalizzazione, verifica.  
  https://www.bellingcat.com/category/resources/  

### 12.2 Disinformazione

- **EUvsDisinfo**  
  Database di casi di disinformazione.  
  https://euvsdisinfo.eu/  

- **Fact-checking italiani**  
  Pagella Politica, Bufale un tanto al così, ecc.  

### 12.3 OPSEC e sicurezza

- **EFF Surveillance Self-Defense**  
  Guide su privacy e sicurezza digitale.  
  https://ssd.eff.org/  

- **Tor Project**  
  Documentazione su Tor e anonimato.  
  https://www.torproject.org/  

### 12.4 Strumenti OSINT

- **Google Dorks**  
  Guida a query avanzate.  
  https://www.google.com/advanced_search  

- **Reverse image search**  
  Google Images, TinEye, Yandex.  

Queste risorse non vanno studiate per intero: D11 serve a darti una mappa operativa
per praticare OSINT in modo strutturato, e a collegarti a guide/tool quando serve approfondire.