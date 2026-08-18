# D13 — RL, preference learning e alignment

## Meta-modulo D13

**Target**  
Me stesso oggi, e chiunque voglia capire come si allineano i large language model (LLM)
a preferenze umane e obiettivi di sicurezza: Reinforcement Learning (RL) base, RLHF,
DPO e varianti, e implicazioni per sistemi agentici e OSINT.

**Prerequisiti consigliati**

- D04 — Matematica e statistica just-in-time (probabilità, derivate)
- D08 — Deep Learning e PyTorch (training loop, loss, optimizer)
- D09 — Transformers, LLM e inference engineering

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - concetto di Reinforcement Learning (RL)  
  - perché serve allineare i LLM  
  - idea di RLHF (Reinforcement Learning from Human Feedback)

- **Modalità standard (~8–10 ore)**  
  - RL base: agente, ambiente, reward, policy  
  - RLHF: raccolta preferenze, reward model, fine-tuning con RL  
  - DPO (Direct Preference Optimization) e alternative  
  - limiti e rischi dell’alignment

- **Modalità deep dive (più giornate)**  
  - studio di paper su RLHF, DPO, allineamento  
  - esperimenti con librerie di RL (es. TRL, CleanRL)  
  - analisi di casi di allineamento (modelli commerciali e open)

**Quando considerare il modulo “completato”**

- so spiegare a parole mie cos’è il RL e come si applica ai LLM
- so descrivere il flusso RLHF (preferenze → reward model → RL fine-tuning)
- so spiegare cos’è DPO e in cosa differisce da RLHF
- so discutere limiti e rischi dell’alignment (over-alignment, gaming, bias)
- ho almeno un esperimento minimo di preference learning (anche simulato)

---

## Perché questo documento

Dopo D12 ho sistemi agentici basati su LLM, ma mi manca capire:

- come i modelli vengono **allineati** a preferenze umane e vincoli di sicurezza
- perché certi modelli sono più “ubbidienti” o “cauti” di altri
- quali sono i trade-off tra utilità, sicurezza e libertà del modello

Questo modulo mette insieme:

- basi di Reinforcement Learning (RL)
- tecniche di allineamento (RLHF, DPO, varianti)
- implicazioni per chi usa LLM in sistemi agentici e OSINT

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- descrivere i concetti base di RL (agente, ambiente, reward, policy)
- spiegare il flusso RLHF (raccolta preferenze, reward model, PPO/RL)
- spiegare cos’è DPO e in cosa differisce da RLHF
- discutere limiti e rischi dell’alignment (over-alignment, gaming, bias)
- collegare alignment a sicurezza e affidabilità di sistemi agentici

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Reinforcement Learning (RL) base.
2. Perché allineare i LLM.
3. RLHF: raccolta preferenze, reward model, fine-tuning con RL.
4. DPO e alternative (IPO, KTO, ecc.).
5. Limiti e rischi dell’alignment.
6. Implicazioni per sistemi agentici e OSINT.

---

## 2. Reinforcement Learning base

### 2.1 Concetti chiave

**Reinforcement Learning (RL)** = paradigma in cui un **agente** impara a agire in un **ambiente** per massimizzare una **reward**:

- **agente**: entità che prende decisioni (es. modello, robot)
- **ambiente**: contesto in cui l’agente agisce
- **stato**: rappresentazione della situazione corrente
- **azione**: scelta dell’agente in uno stato
- **reward**: segnale numerico che indica quanto l’azione è “buona”
- **policy**: strategia che mappa stati ad azioni

Obiettivo:

- imparare una policy che massimizza la reward cumulativa nel tempo

### 2.2 Elementi tecnici (senza formule pesanti)

- **Q-function**: stima del valore atteso di reward per una coppia (stato, azione)
- **policy gradient**: aggiornare la policy nella direzione che aumenta reward attesa
- **PPO (Proximal Policy Optimization)**: algoritmo RL stabile, molto usato per LLM

Riferimenti:

- [Sutton & Barto, Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)
- [CleanRL](https://github.com/vwxyzjn/cleanrl) (implementazioni pulite di algoritmi RL)

---

## 3. Perché allineare i LLM

### 3.1 Problema

LLM addestrati solo con language modeling:

- ottimizzano probabilità del token successivo
- non hanno nozione intrinseca di “utile”, “sicuro”, “etico”
- possono generare:
  - allucinazioni
  - contenuti dannosi (violenza, hate speech, istruzioni pericolose)
  - risposte non allineate alle intenzioni dell’utente

### 3.2 Obiettivi dell’alignment

Allineare un LLM significa:

- farlo comportare in modo più:
  - utile (risponde bene alle domande)
  - sicuro (evita contenuti dannosi)
  - coerente con preferenze umane (tono, stile, vincoli)

Non è:

- rendere il modello “perfetto” o “infalibile”
- eliminare tutti i rischi (impossibile)

---

## 4. RLHF: Reinforcement Learning from Human Feedback

### 4.1 Flusso generale

RLHF si articola in tre fasi principali:

1. **Pretraining**  
   - modello addestrato su grandi corpora (language modeling)

2. **Supervised Fine-Tuning (SFT) + raccolta preferenze**  
   - SFT: addestramento su coppie (istruzione, risposta desiderata)  
   - raccolta preferenze: per ogni prompt, si raccolgono diverse risposte e si chiede a umani di classificarle (A > B, ecc.)

3. **Reward model + RL fine-tuning**  
   - **reward model**: addestrato a predire le preferenze umane (data una coppia di risposte, dice quale è preferita)  
   - **RL fine-tuning**: si usa il reward model come “giudice” per ottimizzare la policy del LLM (es. con PPO)

Risultato:

- modello più allineato a preferenze umane e vincoli di sicurezza

Riferimenti:

- [InstructGPT paper (Ouyang et al., 2022)](https://arxiv.org/abs/2203.02155)

### 4.2 Reward model

Il reward model:

- input: prompt + risposta (o coppia di risposte)
- output: score numerico (quanto la risposta è “buona”)

Viene addestrato su:

- dataset di preferenze umane (A > B, A = B, ecc.)

Limiti:

- può ereditare bias umani
- può essere “giocato” dal modello (reward hacking)

### 4.3 RL fine-tuning (es. PPO)

Il LLM viene ottimizzato per:

- massimizzare reward del reward model
- mantenendo una certa vicinanza al modello originale (per evitare drift eccessivo)

PPO è usato perché:

- stabile
- gestisce bene aggiornamenti “conservativi” della policy

---

## 5. DPO e alternative

### 5.1 DPO (Direct Preference Optimization)

**DPO** = metodo per allineare LLM direttamente su preferenze, senza reward model esplicito né RL complesso.

Idea:

- invece di addestrare reward model + RL, si ottimizza direttamente la policy del LLM per massimizzare la probabilità delle risposte preferite e minimizzare quelle non preferite

Vantaggi:

- più semplice da implementare (no reward model, no PPO)
- più stabile (meno iperparametri RL)
- buoni risultati in pratica

Svantaggi:

- meno flessibile di RLHF in scenari complessi
- dipende dalla qualità del dataset di preferenze

Riferimenti:

- [DPO paper (Rafailov et al., 2023)](https://arxiv.org/abs/2305.18290)

### 5.2 Altre varianti

- **IPO (Identity Preference Optimization)**  
  variante di DPO con regolarizzazione verso la policy originale

- **KTO (Kahneman-Tversky Optimization)**  
  usa principi di prospect theory per modellare preferenze

- **ORPO, SLiC, ecc.**  
  altre tecniche di preference learning

In pratica:

- RLHF è ancora molto usato in modelli commerciali
- DPO e varianti sono popolari in open source per semplicità

---

## 6. Limiti e rischi dell’alignment

### 6.1 Over-alignment

- modello diventa troppo “cauto”:
  - rifiuta task legittimi
  - risposte generiche, poco utili
- perde capacità creative o analitiche

### 6.2 Reward hacking / gaming

- modello impara a “giocare” il reward model:
  - produce risposte che sembrano buone ma sono superficiali
  - sfrutta pattern nel reward model invece di migliorare davvero

### 6.3 Bias e preferenze

- dataset di preferenze riflettono bias culturali, politici, etici
- modello può diventare:
  - troppo allineato a una certa visione del mondo
  - poco adatto a contesti diversi

### 6.4 Sicurezza e robustezza

- allineamento non garantisce sicurezza assoluta:
  - jailbreak, prompt injection, attacchi adversarial
- serve combinazione di:
  - alignment
  - guardrail (filtri, policy)
  - monitoring e audit

---

## 7. Implicazioni per sistemi agentici e OSINT

### 7.1 Agenti e allineamento

Per sistemi agentici (D12):

- agenti basati su LLM allineati sono:
  - più prevedibili
  - meno propensi a azioni pericolose
- ma possono essere:
  - troppo cauti (rifiutano task utili)
  - meno creativi in analisi complesse

### 7.2 OSINT e allineamento

Per OSINT (D11):

- modelli troppo allineati possono:
  - rifiutare analisi su temi sensibili (conflitti, crimine, ecc.)
  - censurare informazioni legittime
- serve bilanciare:
  - sicurezza (non generare contenuti dannosi)
  - utilità (permettere analisi reali)

### 7.3 Scelta del modello

Quando scelgo un modello per agenti/OSINT:

- valuto:
  - grado di allineamento (quanto è “cauto”)
  - capacità di analisi e ragionamento
  - possibilità di usare modelli meno allineati in ambiente controllato (locale, privato)

---

## 8. Laboratori ed esercizi

### Laboratorio 1 — RL base (simulato)

**Obiettivo:** capire concetti di RL con un esempio semplice.

**Passi:**

1. Scegliere un ambiente semplice (es. grid world, bandit).
2. Implementare una policy semplice (es. epsilon-greedy).
3. Addestrare policy per massimizzare reward.
4. Visualizzare:
   - reward nel tempo
   - policy appresa
5. Annotare:
   - come la policy cambia con l’addestramento
   - limiti dell’approccio

**Deliverable:**

- script/notebook con esperimento RL
- nota con osservazioni

---

### Laboratorio 2 — Preference learning simulato

**Obiettivo:** simulare preference learning su un task semplice.

**Passi:**

1. Scegliere un task (es. generare risposte a domande semplici).
2. Generare diverse risposte per ogni domanda (con un LLM o a mano).
3. Creare preferenze simulate (A > B, ecc.) basate su regole semplici (lunghezza, tono, ecc.).
4. Implementare una loss tipo DPO (in forma semplificata) per ottimizzare “policy” (es. pesi di un modello piccolo o score di risposte).
5. Valutare:
   - come cambiano le risposte “preferite” dopo ottimizzazione
6. Annotare:
   - limiti della simulazione
   - intuizioni su DPO/RLHF

**Deliverable:**

- script/notebook con preference learning simulato
- nota con osservazioni

---

### Laboratorio 3 — Analisi di modelli allineati

**Obiettivo:** confrontare modelli con diversi gradi di allineamento.

**Passi:**

1. Scegliere 2–3 modelli (es. uno “base”, uno “instruction”, uno “allineato/sicuro”).
2. Porre stesse domande/task:
   - task utili ma sensibili (es. analisi di conflitti, sicurezza)
   - task creativi
3. Confrontare:
   - qualità delle risposte
   - livello di cautela/rifiuto
   - utilità per OSINT/analisi
4. Annotare:
   - trade-off tra sicurezza e utilità
   - quale modello preferiresti per quali task

**Deliverable:**

- raccolta di prompt e risposte
- nota con confronto e riflessioni

---

## 9. Rubriche e checklist

### Checklist — D13 completato

- [ ] So spiegare cos’è il RL e come si applica ai LLM.
- [ ] So descrivere il flusso RLHF (preferenze → reward model → RL fine-tuning).
- [ ] So spiegare cos’è DPO e in cosa differisce da RLHF.
- [ ] So discutere limiti e rischi dell’alignment (over-alignment, gaming, bias).
- [ ] Ho sperimentato preference learning (anche simulato).
- [ ] So collegare alignment a sicurezza e affidabilità di sistemi agentici e OSINT.

### Errori tipici da evitare

- confondere RLHF con semplice supervised fine-tuning.
- pensare che allineamento risolva tutti i problemi di sicurezza.
- ignorare trade-off tra utilità e cautela nei modelli allineati.
- sottovalutare bias nei dataset di preferenze.

### Segnali che “ho davvero capito” D13

- posso spiegare a un collega cos’è RLHF e DPO senza usare formule pesanti.
- so valutare criticamente un modello in base al suo grado di allineamento.
- so discutere limiti e rischi dell’alignment in sistemi reali.
- vedo l’allineamento come uno strumento, non come una soluzione magica.

---

## 10. Come ripartire dopo una pausa

Se torno su D13 dopo giorni o settimane:

1. Riapro un esperimento di RL o preference learning già fatto.
2. Rieseguo una simulazione per ricordare il flusso.
3. Leggo un paper o articolo su RLHF/DPO per aggiornarmi.
4. Aggiorno una nota con:
   - cosa ho rivisto
   - nuove intuizioni o domande

Scopo: mantenere fresco il legame tra teoria (RL, preference learning) e pratica (allineamento, sicurezza).

---

## 11. Risorse consigliate

### 11.1 RL base

- **Sutton & Barto, Reinforcement Learning: An Introduction**  
  Testo di riferimento per RL.  
  http://incompleteideas.net/book/the-book-2nd.html  

- **CleanRL**  
  Implementazioni pulite di algoritmi RL.  
  https://github.com/vwxyzjn/cleanrl  

### 11.2 RLHF e allineamento

- **InstructGPT paper (Ouyang et al., 2022)**  
  Descrizione di RLHF in modelli GPT.  
  https://arxiv.org/abs/2203.02155  

- **Alignment Forum**  
  Discussioni su allineamento, sicurezza, RLHF.  
  https://www.alignmentforum.org/  

### 11.3 DPO e preference learning

- **DPO paper (Rafailov et al., 2023)**  
  Direct Preference Optimization per allineamento.  
  https://arxiv.org/abs/2305.18290  

- **TRL (Transformer Reinforcement Learning) library**  
  Libreria Hugging Face per RLHF, DPO, ecc.  
  https://huggingface.co/docs/trl  

### 11.4 Sicurezza e robustezza

- **AI Safety Fundamentals**  
  Corso su sicurezza e allineamento.  
  https://www.aisafetyfundamentals.com/  

Queste risorse non vanno studiate per intero: D13 serve a darti una mappa concettuale
per capire allineamento e preference learning, e a collegarti a paper/librerie quando serve approfondire.