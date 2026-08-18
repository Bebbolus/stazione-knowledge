# D11c — Geopolitica e governance dell'AI per l'OSINT

## Meta-modulo D11c

**Target**  
Me stesso oggi, e chiunque voglia capire come la geopolitica e la governance dell'AI influenzino
il lavoro OSINT: provider AI (open vs closed), export controls, AI sovrana, attribution di operazioni
state-sponsored, supply chain dei modelli, e regolamentazione come contesto operativo.

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D11 — OSINT avanzato e discipline principali

**Nota esplicita**:  
Questo modulo è **indipendente da D11b**. Non serve averlo completato per studiare D11c.

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - geopolitica dei provider AI (open vs closed, export controls)  
  - cenni ad AI sovrana e implicazioni per OSINT  
  - regolamentazione come contesto operativo (EU AI Act, Cina, USA)

- **Modalità standard (~8–10 ore)**  
  - analisi di casi reali di export controls e AI sovrana  
  - attribution di operazioni state-sponsored tramite firma tecnologica  
  - supply chain OSINT sui modelli (provenienza pesi, fine-tuning avvelenati, licenze)  
  - laboratori su regolamentazione e limiti etico-legali

- **Modalità deep dive (più giornate)**  
  - studio approfondito di policy e regolamenti (EU AI Act, export controls)  
  - analisi di supply chain di modelli open-weight (provenienza, finanziamenti)  
  - casi studio di attribution (state-sponsored campaigns)

**Quando considerare il modulo "completato"**

- so descrivere la geopolitica dei provider AI e le implicazioni per OSINT
- so analizzare casi di export controls e AI sovrana
- so valutare attribution di operazioni state-sponsored tramite firma tecnologica
- so verificare provenienza e supply chain di modelli open-weight
- conosco le differenze chiave tra EU AI Act, approccio cinese e USA come contesto operativo

---

## Perché questo documento

Dopo D11 ho metodologia OSINT, ma mi manca una comprensione di come **geopolitica e governance**
dell'AI influenzino il lavoro sul campo:

- quali provider AI sono disponibili a chi, e perché (open vs closed, export controls)
- come stati e attori usano l'AI per operazioni di influenza (attribution)
- come verificare la supply chain di modelli open-weight (provenienza, licenze, finanziamenti)
- come regolamentazioni (EU AI Act, Cina, USA) definiscono confini pratici per l'analista

Questo modulo è **operativo e contestuale**: non è diritto astratto, ma mappa di vincoli e opportunità
per chi fa OSINT in un mondo frammentato.

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere la geopolitica dei provider AI (open vs closed, export controls, AI sovrana)
- analizzare attribution di operazioni state-sponsored tramite firma tecnologica
- verificare provenienza e supply chain di modelli open-weight
- valutare implicazioni di regolamentazioni (EU AI Act, Cina, USA) per il lavoro OSINT
- collegare geopolitica AI a limiti etico-legali già definiti in D11 §7.3

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Geopolitica dei provider AI (open vs closed, export controls, AI sovrana).
2. Attribution di operazioni state-sponsored tramite firma tecnologica.
3. Supply chain OSINT sui modelli AI (provenienza, fine-tuning avvelenati, licenze).
4. Regolamentazione come contesto operativo (EU AI Act, Cina, USA).

---

## 2. Geopolitica dei provider AI

### 2.1 Modelli open-weight vs closed

**Open-weight** = modelli con pesi pubblicamente accessibili (es. Llama, Mistral, Qwen, Phi).

**Closed** = modelli accessibili solo via API o con pesi non pubblici (es. GPT-4, Claude, Gemini).

Strategie diverse:

- **Occidente (USA/EU)**:
  - mix di open (Meta Llama, Mistral) e closed (OpenAI, Anthropic, Google)
  - enfasi su sicurezza, allineamento, compliance
- **Cina**:
  - modelli open (Qwen, Yi, GLM) e closed (Ernie, Doubao)
  - enfasi su controllo statale, allineamento a policy cinesi
- **Altri attori emergenti** (Russia, India, Medio Oriente):
  - modelli nazionali o adattamenti di modelli open
  - enfasi su sovranità digitale, riduzione dipendenza da USA/Cina

Implicazioni per OSINT:

- accesso a modelli diversi a seconda di giurisdizione e alleanze
- rischi di censura o allineamento politico nei modelli closed
- opportunità di usare open-weight per analisi indipendenti

### 2.2 Export controls su compute e modelli

**Export controls** = restrizioni all'esportazione di tecnologie sensibili (chip AI, modelli, accesso).

Casi recenti:

- **2022–2024**: USA limitano export di chip NVIDIA (A100, H100) verso Cina
- **2023**: restrizioni su accesso a modelli avanzati (GPT-4, Claude) da certi paesi
- **2024**: proposte di limitare export di modelli open-weight pesanti (>100B parametri)

Impatto pratico:

- alcuni attori non possono accedere a chip o modelli avanzati
- incentivi a sviluppare alternative nazionali (AI sovrana)
- frammentazione dell'ecosistema AI globale

Riferimenti:

- [BIS Export Controls on AI Chips (2023)](https://www.bis.doc.gov/)
- [CSIS - AI Export Controls](https://www.csis.org/ai-export-controls)

### 2.3 Iniziative di "AI sovrana"

**AI sovrana** = sforzi di stati per sviluppare capacità AI autonome:

- **data center nazionali**: infrastrutture controllate dallo stato
- **modelli nazionali**: addestrati su dati locali, allineati a policy nazionali
- **ecosistemi chiusi**: riduzione dipendenza da provider esteri

Esempi:

- **Cina**: modelli Qwen, Ernie, allineati a policy cinesi
- **Russia**: modelli GigaChat, Yandex, allineati a narrative statali
- **UE**: iniziative per AI europea (es. Aleph Alpha, Mistral)
- **Medio Oriente**: modelli Falcon (UAE), allineati a interessi regionali

Implicazioni per OSINT:

- quali capacità AI sono disponibili a quali attori/popolazioni
- cosa significa per lavoro air-gapped o in giurisdizioni con accesso limitato
- necessità di adattare strategie a vincoli locali

---

## 3. Attribution di operazioni state-sponsored

### 3.1 Firma tecnologica nelle campagne

**Attribution** = attribuire una campagna di influenza a un attore specifico (stato, gruppo).

Segnali di firma tecnologica:

- **stack AI**: modelli usati (es. Qwen per attori cinesi, GPT per occidentali)
- **stile di prompting**: pattern ricorrenti (lingua, tono, struttura)
- **infrastrutture usate**: server, domini, tool (es. piattaforme cinesi vs occidentali)

Esempi:

- campagne di influenza russe: uso di modelli locali, server in Russia, narrazioni specifiche
- campagne cinesi: uso di Qwen/Earnie, server in Cina, narrazioni allineate a policy cinesi

### 3.2 Limiti e rischi di attribution errata

**False flag**: attori che usano tool/stack di altri attori per confondere attribution.

**Riuso di tool open source**: stessi tool usati da attori diversi (es. Llama usato da USA, Cina, Russia).

Rischi:

- attribution errata → risposte politiche/diplomatiche sbagliate
- sovrattribuzione a stati (quando potrebbero essere gruppi indipendenti)
- sottovalutazione di attori non statali

Collegamento esplicito:

- **D11 §6 (disinformazione)**: pattern di narrazioni e amplificazione
- **D11b §1 (AI come arma)**: deepfake, campagne assistite da LLM

---

## 4. Supply chain OSINT sui modelli AI

### 4.1 Provenienza dei pesi di modelli open-weight

**Provenienza** = da dove vengono i pesi di un modello open-weight.

Verifica:

- **hub ufficiali**: Hugging Face, GitHub, siti delle aziende
- **hash e signature**: verificare checksum dei pesi
- **documentazione**: paper, report tecnici che descrivono training

Segnali di rischio:

- pesi distribuiti su canali non ufficiali (Telegram, forum oscuri)
- mancanza di documentazione o paper
- checksum non verificabili

### 4.2 Fine-tuning "avvelenati"

**Fine-tuning avvelenato** = modelli open-weight modificati con dati malevoli.

Segnali di rischio:

- performance anomale (es. modello che risponde in modo strano a certi prompt)
- bias insoliti (es. narrazioni politiche specifiche)
- mancanza di trasparenza su dati di fine-tuning

Come riconoscere:

- testare modello su prompt standardizzati
- confrontare con versione originale (se disponibile)
- verificare reputazione di chi distribuisce il fine-tuning

### 4.3 Licenze, proprietà e finanziamento

**Licenze**: alcuni modelli hanno restrizioni (es. uso commerciale vietato, attribution richiesta).

**Proprietà**: chi possiede il modello (azienda, stato, università)?

**Finanziamento**: legami con attori statali o industriali (es. modelli cinesi finanziati da stati).

Implicazioni per OSINT:

- rischi di allineamento a interessi specifici
- necessità di verificare indipendenza dei modelli usati

---

## 5. Regolamentazione come contesto operativo

### 5.1 EU AI Act, approccio cinese, approccio USA

**EU AI Act**:

- classificazione per rischio (inaccettabile, alto, limitato, minimo)
- requisiti stringenti per alto rischio (documentazione, audit, monitoring)
- enfasi su trasparenza, diritti fondamentali

**Approccio cinese**:

- controllo statale su AI
- allineamento a policy e narrative statali
- enfasi su sicurezza nazionale, ordine sociale

**Approccio USA**:

- mix di regolamentazione settoriale (sanità, finanza, difesa)
- enfasi su innovazione, competitività
- meno regolamentazione federale, più a livello statale/settoriale

### 5.2 Cosa cambia legalmente per l'analista

**Coerente con D11 §7.3 (limiti etico-legali)**:

- **EU**: analisi di sistemi AI deve rispettare GDPR, AI Act (es. no accesso non autorizzato)
- **Cina**: limiti su cosa si può analizzare (sistemi statali, dati sensibili)
- **USA**: più flessibilità, ma attenzione a leggi settoriali (es. CFAA per accesso non autorizzato)

Implicazioni pratiche:

- osservare passivamente, mai accedere senza autorizzazione
- documentare fonti e metodi per audit
- adattare strategie a giurisdizione

---

## 6. Laboratori ed esercizi

### Laboratorio 1 — Mappatura di un caso reale di export control

**Obiettivo:** analizzare un caso di export control su AI.

**Passi:**

1. Scegliere un caso (es. export control USA su chip NVIDIA verso Cina, 2023).
2. Raccogliere fonti (articoli, report, policy).
3. Analizzare:
   - cosa è stato limitato (chip, modelli, accesso)
   - perché (motivi strategici)
   - impatto pratico (chi non può usare cosa)
4. Annotare:
   - implicazioni per OSINT
   - lezioni per geopolitica AI

**Deliverable:**

- documento di analisi (1–2 pagine)
- nota con osservazioni

---

### Laboratorio 2 — Attribution di una campagna di influenza

**Obiettivo:** analizzare attribution di una campagna state-sponsored.

**Passi:**

1. Scegliere una campagna documentata (es. influenza russa 2016, cinese 2020).
2. Raccogliere fonti (report, analisi tecniche).
3. Analizzare:
   - stack AI usato (se noto)
   - stile di prompting, narrazioni
   - infrastrutture (server, domini)
4. Valutare:
   - quanto è affidabile l'attribution
   - rischi di false flag

**Deliverable:**

- documento di attribution (1–2 pagine)
- nota con osservazioni e limiti

---

### Laboratorio 3 — Checklist di verifica provenance per modello open-weight

**Obiettivo:** costruire checklist per verificare provenienza di un modello.

**Passi:**

1. Scegliere un modello open-weight (es. Llama 3, Qwen, Mistral).
2. Raccogliere informazioni:
   - hub di distribuzione (Hugging Face, GitHub)
   - documentazione (paper, report)
   - checksum/signature
3. Costruire checklist:
   - hub ufficiale?
   - documentazione disponibile?
   - checksum verificabile?
   - licenza chiara?
   - proprietà/finanziamento trasparenti?
4. Testare checklist su 2–3 modelli.

**Deliverable:**

- checklist di verifica provenance
- nota con risultati test

---

### Laboratorio 4 — Analisi di regolamentazione e limiti etico-legali

**Obiettivo:** analizzare regolamentazione AI in una giurisdizione.

**Passi:**

1. Scegliere una giurisdizione (EU, Cina, USA).
2. Raccogliere fonti (AI Act, policy cinesi, leggi USA).
3. Analizzare:
   - cosa è permesso/vietato per analisti OSINT
   - limiti etico-legali (accesso, uso dati, privacy)
4. Collegare a D11 §7.3 (limiti etico-legali).
5. Annotare:
   - implicazioni pratiche per lavoro OSINT
   - scenari di rischio

**Deliverable:**

- documento di analisi regolamentazione (1–2 pagine)
- nota con osservazioni e limiti

---

## 7. Rubriche e checklist

### Checklist — D11c completato

- [ ] So descrivere la geopolitica dei provider AI (open vs closed, export controls, AI sovrana).
- [ ] So analizzare attribution di operazioni state-sponsored tramite firma tecnologica.
- [ ] So verificare provenienza e supply chain di modelli open-weight.
- [ ] Conosco differenze chiave tra EU AI Act, approccio cinese e USA come contesto operativo.
- [ ] So collegare regolamentazione a limiti etico-legali (D11 §7.3).
- [ ] Ho analizzato almeno un caso reale di export control o attribution.

### Errori tipici da evitare

- confondere geopolitica AI con teoria astratta (qui è contesto operativo per OSINT).
- sottovalutare rischi di supply chain (fine-tuning avvelenati, licenze oscure).
- attribuire campagne senza considerare false flag o riuso di tool open source.
- ignorare limiti etico-legali nella regolamentazione (accesso non autorizzato, privacy).
- trattare regolamentazione come diritto astratto invece che come confini pratici.

### Segnali che "ho davvero capito" D11c

- posso spiegare a un collega come geopolitica e governance AI influenzino OSINT.
- so analizzare casi di export control e AI sovrana con esempi concreti.
- so valutare attribution di campagne state-sponsored con consapevolezza di limiti.
- so verificare provenienza di modelli open-weight con checklist strutturata.
- vedo regolamentazione come contesto operativo, non come teoria astratta.

---

## 8. Come ripartire dopo una pausa

Se torno su D11c dopo giorni o settimane:

1. Riapro un caso studio (export control, attribution, supply chain) già analizzato.
2. Rileggo analisi e checklist.
3. Aggiungo una piccola attività:
   - nuovo caso di export control o AI sovrana
   - nuova verifica di provenance su modello open-weight
   - aggiornamento analisi regolamentazione
4. Aggiorno una nota con:
   - cosa ho aggiunto
   - nuove intuizioni o domande

Scopo: mantenere viva la consapevolezza su geopolitica e governance AI per OSINT.

---

## 9. Risorse consigliate

### 9.1 Geopolitica e export controls

- **BIS Export Controls on AI Chips (2023)**  
  https://www.bis.doc.gov/  

- **CSIS - AI Export Controls**  
  https://www.csis.org/ai-export-controls  

- **Stanford AI Index Report (Geopolitics chapter)**  
  https://aiindex.stanford.edu/  

### 9.2 Attribution e campagne state-sponsored

- **Mandiant - State-Sponsored Campaigns**  
  https://www.mandiant.com/resources/reports  

- **Microsoft Threat Intelligence**  
  https://www.microsoft.com/en-us/security/threat-intelligence  

### 9.3 Supply chain e provenance

- **Hugging Face Model Hub**  
  https://huggingface.co/models  

- **C2PA Specification (provenance)**  
  https://c2pa.org/specifications/  

### 9.4 Regolamentazione

- **EU AI Act**  
  https://artificialintelligenceact.eu/  

- **China AI Governance Framework**  
  https://www.csis.org/china-ai-governance  

- **US AI Policy (OSTP)**  
  https://www.whitehouse.gov/ostp/ai-bill-of-rights/  

Queste risorse non vanno studiate per intero: D11c serve a darti una mappa operativa
per capire geopolitica e governance AI per OSINT, e a collegarti a report/policy quando serve approfondire.