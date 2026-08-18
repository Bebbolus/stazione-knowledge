# D14 — Responsible AI, cybersecurity e governance

## Meta-modulo D14

**Target**  
Me stesso oggi, e chiunque voglia usare sistemi di AI/LLM in modo responsabile, sicuro e conforme
a vincoli etici, legali e organizzativi: bias, fairness, sicurezza, attacchi agli LLM, policy, governance.

**Prerequisiti consigliati**

- D09 — Transformers, LLM e inference engineering
- D11 — OSINT avanzato e discipline principali
- D12 — Agentic systems, MCP e automazione affidabile
- D13 — RL, preference learning e alignment

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - cos’è Responsible AI  
  - bias e fairness nei modelli  
  - rischi di sicurezza base (data leakage, prompt injection)

- **Modalità standard (~8–10 ore)**  
  - attacchi agli LLM (jailbreak, prompt injection, data poisoning)  
  - privacy e protezione dati (GDPR, anonymization)  
  - policy e governance AI in organizzazioni

- **Modalità deep dive (più giornate)**  
  - casi studio di incidenti AI (bias, sicurezza, governance)  
  - progettazione di policy AI per un’organizzazione  
  - threat modeling per sistemi agentici e OSINT

**Quando considerare il modulo “completato”**

- so descrivere i principali rischi etici e di sicurezza dei sistemi AI/LLM
- so riconoscere bias e problemi di fairness in modelli e dataset
- so identificare attacchi tipici agli LLM (jailbreak, prompt injection, ecc.)
- so applicare principi base di privacy e protezione dati
- ho almeno una bozza di policy AI per un contesto organizzativo

---

## Perché questo documento

Dopo D13 ho capito come i modelli vengono allineati, ma mi manca una visione più ampia:

- **etica e responsabilità**: bias, fairness, impatto sociale
- **sicurezza**: attacchi, vulnerabilità, incidenti
- **governance**: policy, ruoli, processi in organizzazioni

Questo modulo mette insieme:

- Responsible AI (etica, fairness, trasparenza)
- Cybersecurity applicata ad AI/LLM
- Governance AI in contesti professionali (aziende, PA, intelligence)

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere i principali rischi etici e di sicurezza dei sistemi AI/LLM
- riconoscere bias e problemi di fairness in modelli e dataset
- identificare attacchi tipici agli LLM (jailbreak, prompt injection, data poisoning)
- applicare principi base di privacy e protezione dati (GDPR, anonymization)
- progettare policy AI di base per un’organizzazione
- fare threat modeling per sistemi agentici e OSINT

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Responsible AI: etica, fairness, trasparenza.
2. Bias e fairness nei modelli e dataset.
3. Sicurezza AI: attacchi agli LLM.
4. Privacy e protezione dati.
5. Governance AI in organizzazioni.
6. Threat modeling per sistemi agentici e OSINT.

---

## 2. Responsible AI: etica, fairness, trasparenza

### 2.1 Cos’è Responsible AI

**Responsible AI** = insieme di principi e pratiche per usare AI in modo:

- **etico**: rispetto di diritti, dignità, autonomia delle persone
- **equo**: evitare discriminazioni e bias ingiusti
- **trasparente**: spiegare decisioni, limiti, rischi
- **responsabile**: chiarezza su ruoli, accountability, governance

Principi comuni (UE, OECD, aziende):

- fairness (equità)
- accountability (responsabilità)
- transparency (trasparenza)
- privacy e sicurezza
- benessere sociale e ambientale

### 2.2 Perché serve

Rischi senza Responsible AI:

- discriminazione (es. prestiti, assunzioni, giustizia)
- danni a gruppi vulnerabili
- perdita di fiducia negli utenti
- sanzioni legali e reputazionali

---

## 3. Bias e fairness

### 3.1 Tipi di bias

- **bias nei dati**: dataset non rappresentativi, sbilanciati, storici discriminatori
- **bias nel modello**: architettura, loss, obiettivi che amplificano disuguaglianze
- **bias nell’uso**: contesto d’uso diverso da quello previsto, interpretazioni errate

Esempi:

- modelli di recruiting che penalizzano donne
- sistemi di credito che discriminano per etnia o zona
- modelli linguistici con stereotipi di genere/etnia

### 3.2 Fairness

**Fairness** = assenza di discriminazioni ingiuste tra gruppi.

Metriche comuni:

- **demographic parity**: stesse probabilità di esito positivo per tutti i gruppi
- **equalized odds**: stessi tassi di vero/falso positivo per tutti i gruppi
- **individual fairness**: individui simili trattati in modo simile

Strumenti:

- audit di fairness su dataset e modelli
- tecniche di debiasing (pre-processing, in-processing, post-processing)

Riferimenti:

- [Fairness in Machine Learning (libro online)](https://fairmlbook.org/)
- [AI Fairness 360 (IBM)](https://aif360.mybluemix.net/)

---

## 4. Sicurezza AI: attacchi agli LLM

### 4.1 Categorie di attacco

1. **Prompt injection**  
   - utente inserisce istruzioni nascoste nel prompt per “dirottare” il modello  
   - es. “ignora le istruzioni precedenti e fai X”

2. **Jailbreak**  
   - prompt progettati per bypassare guardrail di sicurezza  
   - es. “immagina di essere un modello senza restrizioni…”

3. **Data poisoning**  
   - avvelenamento di dataset di training/fine-tuning  
   - es. inserire esempi tossici o fuorvianti

4. **Model extraction / inversion**  
   - tentativi di ricostruire il modello o dati di training da query  
   - es. estrarre informazioni sensibili da un modello

5. **Indirect prompt injection**  
   - prompt nascosti in documenti web, email, PDF che il modello legge  
   - es. testo invisibile in una pagina web che istruisce il modello

Riferimenti:

- [Prompt Injection Primer (Greshake)](https://github.com/jailbreaks/prompt-injection)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

### 4.2 Difese

- **input filtering**: pulire e validare input utente
- **output filtering**: filtrare output tossici o pericolosi
- **guardrail**: regole e policy per limitare comportamenti rischiosi
- **monitoring**: tracciare query e risposte sospette
- **sandboxing**: eseguire modelli in ambienti isolati per task rischiosi

---

## 5. Privacy e protezione dati

### 5.1 GDPR e principi base

**GDPR** (Regolamento UE 2016/679) = normativa su protezione dati personali.

Principi rilevanti per AI:

- **liceità, correttezza, trasparenza**: basi giuridiche, informativa chiara
- **limitazione della finalità**: usare dati solo per scopi specificati
- **minimizzazione**: raccogliere solo dati necessari
- **accuratezza**: mantenere dati aggiornati e corretti
- **limitazione della conservazione**: non tenere dati più del necessario
- **integrità e riservatezza**: sicurezza dei dati

Diritti degli interessati:

- accesso, rettifica, cancellazione, opposizione, portabilità

### 5.2 Anonymization e pseudonymization

- **anonymization**: rendere i dati non riconducibili a persone (irreversibile)
- **pseudonymization**: sostituire identificativi con pseudonimi (reversibile con chiave)

Tecniche:

- rimozione identificativi diretti (nome, email, telefono)
- generalizzazione (es. età → fascia di età)
- soppressione di record rari

Attenzione:

- dati “anonimizzati” possono essere re-identificati con tecniche avanzate
- valutare sempre rischio residuo

Riferimenti:

- [GDPR testo ufficiale](https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016R0679)
- [EDPB guidelines on anonymization](https://www.edpb.europa.eu/)

---

## 6. Governance AI in organizzazioni

### 6.1 Cos’è governance AI

**Governance AI** = insieme di policy, processi, ruoli per gestire rischi e opportunità dell’AI in un’organizzazione.

Elementi chiave:

- **policy AI**: principi, regole, linee guida
- **ruoli**: AI ethics officer, data protection officer, security officer
- **processi**: audit, valutazione impatto, approvazione progetti
- **strumenti**: checklist, template, registri progetti AI

### 6.2 Policy AI

Una policy AI tipica include:

- principi (fairness, transparency, accountability, privacy, sicurezza)
- ambiti di applicazione (quali sistemi, quali dati)
- requisiti per progetti AI:
  - valutazione rischi (bias, sicurezza, privacy)
  - documentazione (dataset, modelli, decisioni)
  - audit e monitoring
- sanzioni per violazioni

### 6.3 AI Act UE

**AI Act** = regolamento UE su AI (approvato 2024, in fase di attuazione).

Classifica sistemi AI per rischio:

- **rischio inaccettabile**: vietati (es. social scoring, manipolazione subliminale)
- **alto rischio**: requisiti stringenti (es. recruiting, credito, giustizia, sanità)
- **rischio limitato**: obblighi di trasparenza (es. chatbot, deepfake)
- **rischio minimo**: nessun obbligo specifico (es. giochi, spam filter)

Implicazioni:

- organizzazioni devono classificare sistemi AI
- alto rischio → valutazione conformità, documentazione, monitoring

Riferimenti:

- [AI Act UE](https://artificialintelligenceact.eu/)

---

## 7. Threat modeling per sistemi agentici e OSINT

### 7.1 Perché threat modeling

**Threat modeling** = processo strutturato per identificare e mitigare minacce a un sistema.

Per sistemi agentici e OSINT:

- agenti che leggono/scrivono file, chiamano API, usano tool
- knowledge base con dati sensibili (fonti, analisi, report)
- rischi di leakage, manipolazione, abuso

### 7.2 Approccio base

Passi:

1. **descrivere sistema**: componenti, flussi dati, attori
2. **identificare asset**: cosa proteggere (dati, modelli, reputazione)
3. **identificare minacce**: attacchi possibili (interni/esterni)
4. **valutare rischi**: probabilità × impatto
5. **definire contromisure**: tecniche, organizzative, policy

### 7.3 Minacce tipiche

- **data leakage**: agenti che espongono dati sensibili in log, output, API
- **prompt injection**: utenti o fonti esterne che manipolano agenti
- **abuso di tool**: agenti che usano tool in modo pericoloso (es. cancellano file, chiamano API critiche)
- **compromissione fonti**: fonti OSINT avvelenate o manipolate

### 7.4 Contromisure

- **isolamento**: eseguire agenti in ambienti isolati (VM, container)
- **limitazione tool**: whitelist di tool e azioni permesse
- **logging e audit**: tracciare tutte le azioni degli agenti
- **review umana**: per task critici o ad alto rischio
- **policy chiare**: cosa gli agenti possono/non possono fare

---

## 8. Laboratori ed esercizi

### Laboratorio 1 — Analisi di bias in un dataset

**Obiettivo:** riconoscere bias in un dataset reale.

**Passi:**

1. Scegliere un dataset (es. recruiting, credito, giustizia).
2. Analizzare distribuzione per gruppi (genere, etnia, età, ecc.).
3. Identificare possibili bias:
   - sbilanciamenti
   - correlazioni sospette
4. Proporre contromisure:
   - raccolta dati più equilibrata
   - tecniche di debiasing
5. Annotare:
   - limiti dell’analisi
   - implicazioni etiche

**Deliverable:**

- script/notebook con analisi
- nota con osservazioni e proposte

---

### Laboratorio 2 — Prompt injection e jailbreak

**Obiettivo:** sperimentare attacchi agli LLM.

**Passi:**

1. Scegliere un LLM (cloud o locale).
2. Provare prompt di injection e jailbreak (da liste pubbliche, es. jailbreak catalog).
3. Osservare risposte:
   - il modello cede?
   - quali guardrail saltano?
4. Proporre difese:
   - input/output filtering
   - guardrail più stringenti
5. Annotare:
   - pattern di attacco efficaci
   - limiti delle difese

**Deliverable:**

- raccolta di prompt e risposte
- nota con analisi e proposte di difesa

---

### Laboratorio 3 — Privacy e anonymization

**Obiettivo:** applicare tecniche di anonymization.

**Passi:**

1. Scegliere un dataset con dati personali (reale o simulato).
2. Identificare identificativi diretti e indiretti.
3. Applicare tecniche:
   - rimozione identificativi
   - generalizzazione
   - soppressione
4. Valutare rischio residuo:
   - possibilità di re-identificazione
5. Annotare:
   - trade-off tra utilità e privacy
   - limiti delle tecniche usate

**Deliverable:**

- script/notebook con anonymization
- nota con valutazione rischio residuo

---

### Laboratorio 4 — Bozza di policy AI

**Obiettivo:** progettare una policy AI di base.

**Passi:**

1. Scegliere un contesto (azienda, PA, laboratorio di ricerca).
2. Definire principi (fairness, transparency, accountability, privacy, sicurezza).
3. Specificare ambiti di applicazione (quali sistemi, quali dati).
4. Definire requisiti per progetti AI:
   - valutazione rischi
   - documentazione
   - audit
5. Proporre ruoli e processi:
   - chi approva progetti
   - chi fa audit
   - chi gestisce incidenti
6. Annotare:
   - punti critici
   - aspetti da approfondire

**Deliverable:**

- documento con bozza di policy AI
- nota con riflessioni

---

## 9. Rubriche e checklist

### Checklist — D14 completato

- [ ] So descrivere i principali rischi etici e di sicurezza dei sistemi AI/LLM.
- [ ] Riconosco bias e problemi di fairness in modelli e dataset.
- [ ] Identifico attacchi tipici agli LLM (jailbreak, prompt injection, data poisoning).
- [ ] Applico principi base di privacy e protezione dati (GDPR, anonymization).
- [ ] Ho progettato una bozza di policy AI per un contesto organizzativo.
- [ ] So fare threat modeling per sistemi agentici e OSINT.

### Errori tipici da evitare

- confondere Responsible AI con “buoni sentimenti” senza pratiche concrete.
- sottovalutare bias nei dataset (pensare che i dati siano “neutrali”).
- fidarsi ciecamente di guardrail e filter senza monitoring.
- ignorare GDPR e privacy in progetti con dati personali.
- progettare policy AI senza coinvolgere stakeholder reali.

### Segnali che “ho davvero capito” D14

- posso spiegare a un collega rischi etici e di sicurezza di un sistema AI.
- so riconoscere bias e proporre contromisure.
- so identificare attacchi agli LLM e difese adeguate.
- so applicare principi di privacy in progetti reali.
- so progettare policy AI e fare threat modeling in modo strutturato.

---

## 10. Come ripartire dopo una pausa

Se torno su D14 dopo giorni o settimane:

1. Riapro un’analisi di bias o un esercizio di sicurezza già fatto.
2. Rileggo policy AI o threat modeling progettati.
3. Aggiorno con:
   - nuovi casi studio (incidenti AI, attacchi)
   - nuove normative (AI Act, linee guida)
4. Aggiorno una nota con:
   - cosa ho rivisto
   - nuove intuizioni o domande

Scopo: mantenere viva la consapevolezza su etica, sicurezza e governance AI.

---

## 11. Risorse consigliate

### 11.1 Responsible AI e fairness

- **Fairness in Machine Learning (libro online)**  
  https://fairmlbook.org/  

- **AI Fairness 360 (IBM)**  
  https://aif360.mybluemix.net/  

- **Google Responsible AI Practices**  
  https://ai.google/responsibilities/  

### 11.2 Sicurezza AI

- **OWASP Top 10 for Large Language Model Applications**  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/  

- **Prompt Injection Primer (Greshake)**  
  https://github.com/jailbreaks/prompt-injection  

- **MITRE ATLAS (Adversarial Threat Landscape for AI Systems)**  
  https://atlas.mitre.org/  

### 11.3 Privacy e GDPR

- **GDPR testo ufficiale**  
  https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016R0679  

- **EDPB guidelines**  
  https://www.edpb.europa.eu/  

### 11.4 Governance AI

- **AI Act UE**  
  https://artificialintelligenceact.eu/  

- **OECD AI Principles**  
  https://oecd.ai/en/ai-principles  

- **NIST AI Risk Management Framework**  
  https://www.nist.gov/itl/ai-risk-management-framework  

Queste risorse non vanno studiate per intero: D14 serve a darti una mappa operativa
per usare AI in modo responsabile, sicuro e conforme, e a collegarti a linee guida quando serve approfondire.