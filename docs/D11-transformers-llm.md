---
aliases:
- D11
- Transformers
- LLM
- Large Language Models
- Self-Attention
- Prompt Engineering
- Allucinazioni AI
resources:
- title: Attention in transformers (3Blue1Brown)
  url: https://www.youtube.com/watch?v=eMlx5fFNoYc
  type: video
- title: Transformer Explainer (Interattivo 3D)
  url: https://poloclub.github.io/transformer-explainer/
  type: lab
- title: Hugging Face NLP Course
  url: https://huggingface.co/learn/nlp-course/
  type: ref
---
# :material-robot: D11: Architettura dei Transformer e Large Language Model



!!! abstract "Sintesi: Il Salto Quantico dell'AI"
    I **Transformer** e i **Large Language Model (LLM)** rappresentano il più grande balzo in avanti nella storia dell'intelligenza artificiale moderna.
    Invece di analizzare le parole una alla volta a passo d'uomo, questi modelli osservano l'intero testo contemporaneamente, comprendendo il contesto e le sfumature come mai prima d'ora.
    Questa guida segue le intuizioni del paper fondamentale [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Il paper storico di Google del 2017 che ha introdotto l'architettura Transformer) e sfrutta le risorse interattive di [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) (Simulatore 3D visuale nel browser) ed il catalogo [Hugging Face](https://huggingface.co/) (L'ecosistema open-source per modelli e dataset).

## 1. Cos'è un Token: I Mattoncini LEGO del Linguaggio

I computer non comprendono i pensieri, i suoni o le parole scritte: sanno elaborare esclusivamente numeri binari.

Per permettere a un'intelligenza artificiale di leggere una frase, dobbiamo prima scomporla in pezzetti elementari chiamati **Token**.

!!! tip "La Metafora dei LEGO"
    Immagina un testo come un castello fatto di mattoncini colorati. 
    Ogni mattoncino può essere una parola intera (*"gatto"*), una sillaba frequente (*"in-"*, *"-credibile"*) o un segno di punteggiatura (*"!"*).
    Il modello assegna a ciascun mattoncino un numero di catalogo univoco (ID numerico) ed elabora solo questi numeri.

=== "La Scomposizione in Subword"
    Se il modello incontra una parola rara o complessa come *"indubitabilmente"*, la divide nei mattoncini più piccoli che già conosce: `["in", "dubbi", "tabil", "mente"]`.
    In questo modo, con un vocabolario di appena 50.000 mattoncini base, un LLM può leggere e scrivere qualsiasi termine del mondo!

=== "La Regola Pratica dei Token"
    In media, nel linguaggio comune:
    * **1 Token** equivale a circa **3 o 4 caratteri** di testo.
    * 100 parole italiane corrispondono all'incirca a **130-140 token**.
    * I testi in lingue con alfabeti complessi o con molte parole composte richiedono più token per esprimere lo stesso concetto.

## 2. Cos'è un Prompt: Le Istruzioni per il Costruttore

Il **Prompt** è il messaggio di testo, la domanda o il contesto che inviamo all'AI per richiedere un'azione o una risposta.

Se l'LLM è un costruttore straordinario con miliardi di mattoncini a disposizione, il tuo prompt rappresenta il **progetto architettonico** che gli indica esattamente cosa costruire.

!!! info "La Metafora del Navigatore Satellitare"
    Se dici al navigatore soltanto *"Guida!"*, non saprà dove andare e sceglierà una direzione a caso.
    Se invece imposti chiaramente: *"Portami alla Stazione Centrale, evitando i pedaggi e arrivando entro le 18:00"*, otterrai il percorso perfetto al primo tentativo.

=== "Prompt Debole vs Prompt Potente"
    * ❌ **Prompt Debole**: *"Parlami dei Transformer."* (L'AI produrrà un testo generico, troppo lungo o troppo accademico).
    * ✅ **Prompt Potente**: *"Spiega l'architettura dei Transformer a uno studente delle superiori, usando la metafora dei LEGO, in un elenco puntato di massimo 5 punti."*

=== "L'Anatomia di un Prompt Efficace"
    Un prompt professionale include quattro ingredienti fondamentali:
    1. **Ruolo**: *"Sei un esperto sviluppatore Python..."*
    2. **Contesto**: *"Sto creando un'applicazione web per studenti..."*
    3. **Istruzione**: *"Scrivi una funzione per validare un indirizzo email..."*
    4. **Formato di Output**: *"Restituisci solo il codice commentato senza introduzioni."*

## 3. La Self-Attention: Come le Parole si Guardano tra Loro

Prima del 2017, i vecchi modelli linguistici leggevano le parole in **fila indiana** (come nel gioco del telefono senza fili): arrivati alla fine di un paragrafo lungo, avevano già dimenticato l'inizio.

La vera rivoluzione dei Transformer si chiama **Self-Attention** (Auto-Attenzione): un meccanismo che permette a tutte le parole di una frase di guardarsi contemporaneamente nello stesso istante.

!!! tip "La Metafora della Festa in Stanza Rotonda"
    Immagina tutte le parole di una frase riunite al centro di una stanza rotonda.
    Quando compare la parola ambigua **"banca"**, essa si volta immediatamente verso tutte le altre parole presenti:
    * Se vicino a sé vede *"fiume"*, *"pesca"* e *"riva"*, capisce subito che si tratta dell'argine erboso di un corso d'acqua.
    * Se invece vede *"conto"*, *"soldi"* e *"interessi"*, comprende all'istante che si riferisce a un istituto finanziario.

=== "I Tre Ruoli della Comunicazione (Q, K, V)"
    Senza formule complicate, ogni parola indossa tre distintivi per interagire con le altre:
    * **Query (Cosa cerco?)**: La domanda che la parola pone alle vicine (*"Chi mi aiuta a chiarire il mio senso?"*).
    * **Key (Chi sono?)**: Il cartellino descrittivo che ogni parola mostra (*"Io sono un sostantivo legato al denaro"*).
    * **Value (Cosa so dire?)**: Il contenuto reale e il significato che la parola offre a chi le dà retta.

=== "Perché la Self-Attention è Rivoluzionaria?"
    * **Parallelismo totale**: Le schede grafiche (GPU) possono calcolare tutte le relazioni contemporaneamente alla velocità della luce.
    * **Contesto a lungo raggio**: Il modello non perde il filo del discorso, anche all'interno di documenti lunghi decine di pagine.

## 4. Cos'è un Large Language Model (LLM)

Un **Large Language Model (LLM)** è una gigantesca rete neurale basata sull'architettura Transformer, addestrata su centinaia di miliardi di parole provenienti dal web, da libri e da archivi di codice.

Nel suo nucleo più profondo, un LLM è un potentissimo **predittore statistico del prossimo token**.

!!! info "La Metafora del T9 su Scala Planetaria"
    Hai presente la tastiera predittiva dello smartphone che suggerisce la parola successiva mentre digiti un messaggio?
    Un LLM fa la stessa cosa, ma invece di considerare solo le ultime due parole, tiene conto di un intero libro di contesto e attinge a una conoscenza sterminata.
    Se inserisci *"Il sole sorge a..."*, il modello assegna il 99% di probabilità al token *"est"*.

=== "Parametri vs Finestra di Contesto"
    * **Parametri (Pesi)**: Sono la memoria a lungo termine del modello (miliardi di connessioni neurali scolpite durante l'addestramento).
    * **Finestra di Contesto (Context Window)**: È la memoria di lavoro a breve termine (quanti token il modello può tenere a mente contemporaneamente durante una singola chat).

=== "Dai Modelli Base agli Assistenti Conversazionali"
    * **Pre-Training (Modello Base)**: Il modello legge enormi biblioteche e impara la struttura della grammatica e della conoscenza umana completando frasi a ciclo continuo.
    * **Fine-Tuning e Allineamento (RLHF)**: Attraverso istruzioni umane e feedback guidato, il modello grezzo impara a comportarsi come un assistente cortese, sicuro e utile (come ChatGPT o Claude).

## 5. Le Allucinazioni: Quando l'AI Inventa con Sicurezza

Nonostante la loro apparente intelligenza, gli LLM non possiedono una coscienza, non "comprendono" la realtà fisica e non memorizzano un database di verità assolute.

Quando un modello linguistico non conosce un'informazione o viene confuso dal contesto, genera una **Allucinazione**: un'affermazione completamente falsa o inventata, esposta con tono estremamente sicuro e convincente.

!!! warning "Perché si verificano le allucinazioni?"
    L'obiettivo matematico dell'LLM è produrre la sequenza di parole **più armonica e statisticamente plausibile**, non necessariamente quella vera.
    Se chiedi all'AI la biografia di un personaggio inventato, non risponderà *"Non esiste"*, ma inventerà una carriera credibile e date di nascita fittizie.

=== "Come Ridurre le Allucinazioni"
    * **Grounding e RAG**: Fornisci all'AI documenti ufficiali e chiedile di rispondere basandosi solo su di essi.
    * **Controllo della Temperatura**: Imposta valori bassi di temperatura per rendere le risposte più deterministiche e meno creative.
    * **Richiesta di Citazioni**: Chiedi esplicitamente al modello di citare le fonti o di ammettere con sincerità quando non conosce una risposta.

=== "Quiz di Verifica: Riconosci l'Allucinazione"
    **Domanda**: Un assistente AI afferma con assoluta certezza: *"Nel 1821 Napoleone Bonaparte ordinò un caffè espresso via WhatsApp durante la battaglia di Waterloo"*. Come interpreti questa risposta?
    * **A)** L'AI ha avuto accesso a documenti storici segreti inediti.
    * **B)** È una classica **Allucinazione**: il modello ha combinato elementi sintatticamente perfetti ma temporalmente e fattualmente incompatibili.
    * **C)** Il processore del server ha calcolato un errore di divisione per zero.
    
    *(Risposta corretta: **B**)*

## 6. Usare gli LLM in Modo Responsabile: Le Regole d'Oro

I Large Language Model sono straordinari amplificatori dell'ingegno umano, ma richiedono senso critico e consapevolezza etica nell'utilizzo quotidiano.

Per sfruttare appieno il potenziale dell'AI senza rischi, segui sempre queste quattro regole fondamentali:

!!! tip "I 4 Pilastri dell'Uso Responsabile"
    1. **Human-in-the-Loop**: Mantieni sempre il controllo finale. Non fidarti mai ciecamente di codice o testi generati per decisioni mediche, legali o critiche.
    2. **Tutela della Privacy**: Non inserire mai nei prompt password aziendali, credenziali, dati sanitari o informazioni personali riservate.
    3. **Verifica delle Fonti**: Controlla sempre numeri, date e citazioni fornite dall'AI incrociandole con fonti primarie e documentazione ufficiale.
    4. **Trasparenza**: Dichiara con onestà quando un contenuto o una soluzione è stata generata o assistita dall'intelligenza artificiale.

=== "L'AI come Co-Pilota, non come Pilota Automatico"
    Ricorda: l'intelligenza artificiale è il miglior assistente che tu possa desiderare per fare brainstorming, riassumere testi e velocizzare il lavoro.
    Ma la creatività, l'etica e la responsabilità delle decisioni appartengono sempre e soltanto all'essere umano.

## Appendice Operativa: Laboratori Pratici

1. Esegui il laboratorio interattivo Attention Crush per sperimentare visivamente come i token si allineano e scambiano attenzione all'interno della rete neurale.
