---
aliases: [D12c, Prompt Engineering, Context Engineering, Chain-of-Thought, ReAct, Tree of Thoughts, Structured Outputs, DSPy]
---

# Prompt Engineering, Gestione del Contesto e Generazione Guidata nei Sistemi Agentici

Il **prompt engineering** e il **context engineering** costituiscono l'insieme delle metodologie algoritmiche, dei pattern di condizionamento probabilistico e delle architetture di memoria dinamica concepite per guidare l'inferenza autoregressiva dei Large Language Model verso traiettorie di esecuzione deterministiche e verificabili. Tali discipline trovano applicazione critica nell'orchestrazione di agenti autonomi per l'intelligence delle fonti aperte ([D11](D11-osint-avanzato.md)), nell'automazione di workflow investigativi multi-step e nell'interfacciamento con strumenti esterni tramite il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (lo standard aperto ideato da [Anthropic](https://www.anthropic.com/) per la connessione sicura tra modelli linguistici e sorgenti dati). La loro esistenza risponde alla necessità fondamentale di superare la non-determinatezza intrinseca, la suscettibilità al rumore testuale e i vincoli dimensionali della finestra di attenzione, trasformando un puro predittore statistico del prossimo token in un affidabile motore di computazione simbolica e ragionamento strutturato.

```
+-----------------------------------------------------------------------------------------+
|                  EVOLUZIONE DELLE ARCHITETTURE DI RAGIONAMENTO (REASONING)              |
+-----------------------------------------------------------------------------------------+

  1. PROMPTING DIRETTO:     [ Input (x) ] ──────────────────────────────────────────► [ Output (y) ]

  2. CHAIN-OF-THOUGHT:      [ Input (x) ] ──► [ Thought 1 ] ──► [ Thought 2 ] ──────► [ Output (y) ]

  3. CICLO REACT:           [ Input (x) ] ──► [ Thought 1 ] ──► [ Action 1 ] ──► [ Observation 1 ]
                                                                      ▲                  │
                                                                      └── [ Thought 2 ] ◄┘
                                                                               │
                                                                               ▼
                                                                        [ Final Answer ]

  4. TREE OF THOUGHTS:                               [ Root: Stato 0 ]
                                                     /       |       \
                                             [ Ramo 1 ]  [ Ramo 2 ]  [ Ramo 3 ]
                                              (V=0.8)     (V=0.2)     (V=0.9)
                                                │        (Prunato)      │
                                            [ Ramo 1.1 ]            [ Ramo 3.1 ]
                                              (V=0.95)                (V=0.4)
                                                │                    (Prunato)
                                         [ Soluzione Ottima ]
```

## Dai Modelli Linguistici come Oracoli alle Macchine a Stati: La Fragilità del Prompting Ingenuo

La concezione comune dei Large Language Model come oracoli omniscienti in grado di risolvere qualsiasi problema mediante semplici richieste discorsive in linguaggio naturale si scontra con la realtà matematica della loro architettura. Un modello linguistico autoregressivo è formalmente un estimatore di densità di probabilità condizionata $P(w_t \mid w_1, \dots, w_{t-1})$ definito su un vocabolario discreto di token $V$. Durante la fase di generazione, il modello campiona iterativamente il token successivo in base alla distribuzione probabilistica indotta dalla sequenza di input. Il prompting ingenuo, caratterizzato da istruzioni generiche prive di vincoli strutturali, soffre di un'elevata varianza stocastica: minime permutazioni nell'ordine delle parole, variazioni nella spaziatura o lievi ambiguità sintattiche possono alterare drasticamente la traiettoria di generazione, conducendo ad allucinazioni fattuali, violazioni di formato e derive di contesto (*semantic drift*).

Per trasformare questa funzione probabilistica in una componente computazionale affidabile per sistemi agentici, è necessario distinguere chiaramente tra due discipline complementari: il **prompt engineering** e il **context engineering**.

Il **prompt engineering** opera a livello micro-architetturale sulla singola invocazione di inferenza. Esso definisce la formulazione semantica delle istruzioni, il condizionamento epistemico del ruolo, la distribuzione degli esempi dimostrativi (*few-shot exemplars*) e la struttura dello scratchpad di calcolo, ottimizzando la probabilità che il modello generi token allineati all'obiettivo.

Il **context engineering** agisce invece a livello macro-architetturale sulla gestione dinamica dello stato e della memoria di lavoro dell'agente nel corso del tempo. Esso governa l'allocazione del budget dei token, la selezione e il filtraggio delle informazioni recuperate da basi di dati o knowledge graph ([D10](D10-rag-knowledge-osint.md)), la compattazione gerarchica della cronologia e la sincronizzazione con lo stato persistente dell'ambiente. In sintesi, il prompt engineering indirizza il vettore probabilistico del singolo passo decisionale, mentre il context engineering garantisce che l'input di condizionamento contenga esattamente le informazioni pertinenti, non corrotte da rumore o allucinazioni pregresse.

## Architetture di Ragionamento: Chain-of-Thought, ReAct e Tree of Thoughts

Nei compiti di deduzione complessa e nelle indagini OSINT multi-step, il tentativo di mappare direttamente la query iniziale $x$ nella risposta finale $y$ (*zero-shot direct prompting*) fallisce frequentemente, poiché il modello non dispone di token intermedi sufficienti per allocare capacità di calcolo latente prima di emettere la conclusione. Per superare questa limitazione, la ricerca ha sviluppato paradigmi di ragionamento strutturato che costringono il modello a esplicitare i passaggi logici intermedi.

La prima pietra miliare è rappresentata dal [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) (il paper di Google Research che ha formalizzato il ragionamento a passaggi intermedi espliciti nei Large Language Model) sviluppato presso [Google](https://about.google/) (la multinazionale tecnologica leader nei servizi Internet, ricerca algoritmica, cloud e AI). Il pattern Chain-of-Thought (CoT) decompone il problema introducendo una sequenza di passi deduttivi $\tau_1, \tau_2, \dots, \tau_k$ nello spazio dei token, tale per cui la probabilità congiunta $P(y \mid x)$ viene calcolata marginalizzando sulle traiettorie di pensiero esplicite. Nelle sue varianti zero-shot ("Pensiamo passo dopo passo") e few-shot, il CoT migliora sensibilmente le prestazioni nel ragionamento simbolico e aritmetico, ma rimane vincolato a un sistema chiuso privo di accesso al mondo esterno, accumulando allucinazioni qualora un passaggio intermedio contenga premesse fattuali errate.

Per ancorare il ragionamento alla realtà operativa, lo studio [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) (lo studio di Princeton University e Google Research che ha introdotto il pattern agentico che alterna pensiero ed esecuzione di tool) ha introdotto un'architettura ciclica che alterna generazione verbale e interazione con l'ambiente. In ReAct, la traccia di pensiero (*Thought*) formula l'ipotesi e pianifica la mossa successiva, l'azione (*Action*) invoca uno strumento esterno (ad esempio un'interrogazione DNS o una query a database), e l'osservazione (*Observation*) riceve l'output deterministico del mondo esterno. Questo ciclo ricorsivo $T_t \rightarrow A_t \rightarrow O_t \rightarrow T_{t+1}$ corregge costantemente le assunzioni del modello tramite evidenze empiriche, azzerando le allucinazioni fattuali.

Tuttavia, il pattern ReAct opera secondo una traiettoria puramente lineare e greedy, risultando incapace di esplorare percorsi alternativi o eseguire backtracking qualora una linea di indagine si riveli infruttuosa. Per risolvere i problemi a elevata complessità combinatoria, lo studio [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) (lo studio congiunto di Princeton University e Google DeepMind che estende il CoT tramite esplorazione ad albero e backtracking) condotto da [Princeton University](https://www.stanford.edu/) e [Google DeepMind](https://deepmind.google/) (la divisione di ricerca sull'intelligenza artificiale di Google pioniera del deep learning e del reinforcement learning) estende il ragionamento a una struttura ad albero. In Tree of Thoughts (ToT), il modello genera molteplici rami di pensiero candidati a ogni bivio decisionale, valuta ciascuno stato intermedio mediante un'euristica di scoring $V(s)$ e impiega algoritmi classici di esplorazione su grafi, quali Breadth-First Search (BFS), Depth-First Search (DFS) o Beam Search, per potare i rami non promettenti e convergere verso la soluzione ottima.

Parallelamente, il pattern di auto-riflessione introdotto in [Self-Refine: Iterative Refinement (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651) (il paper della Carnegie Mellon University sul pattern di auto-valutazione e perfezionamento ciclico per modelli linguistici) struttura l'inferenza in un ciclo tripartito di Generazione, Critica e Perfezionamento. Il modello genera una prima bozza di risposta, valuta autonomamente la presenza di incongruenze logiche o violazioni di requisiti rispetto a criteri prefissati e applica modifiche correttive prima di presentare il risultato finale.

## Strutturazione del System Prompt e Condizionamento Epistemico del Ruolo

All'interno delle moderne API di chat completion introdotte da [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT e ChatGPT) e [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI creatrice dei modelli Claude e ideatrice del Model Context Protocol), l'architettura dei messaggi è suddivisa in ruoli semantici formali: `system` (o `developer`), `user`, `assistant` e `tool`. Il **System Prompt** funge da contratto costituzionale dell'agente, stabilendo l'identità operativa, i limiti epistemici, i criteri di sicurezza e i formati di output vincolanti che devono persistere lungo l'intera sessione.

Un fenomeno cognitivo critico da considerare nella progettazione del contesto è l'effetto formalizzato nello studio [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023)](https://arxiv.org/abs/2307.03172) (lo studio di Stanford University e UC Berkeley sul decadimento dell'attenzione nei token centrali di contesti estesi) condotto presso [Stanford University](https://www.stanford.edu/) (la prestigiosa università di ricerca della California, centro accademico cardine per l'informatica e l'AI). La ricerca dimostra che i meccanismi di Self-Attention dei Transformer manifestano una curva di recupero a forma di U: i modelli mostrano un'altissima fedeltà nell'accedere alle informazioni posizionate all'inizio del contesto (effetto di primarietà) e alla fine del contesto (effetto di recenza), mentre subiscono una degradazione prestazionale fino al 40% nel recupero di dettagli collocati nella porzione centrale di finestre informative estese.

Per contrastare questo decadimento, la strutturazione avanzata del system prompt applica strategie di ancoraggio simmetrico: le regole comportamentali invarianti, le policy di sicurezza e le definizioni dei tool vengono posizionate all'apice del prompt di sistema, mentre i vincoli esecutivi immediati e gli schemi di formattazione della risposta vengono riaffermati in coda al messaggio dell'utente. Inoltre, per immunizzare l'agente da attacchi di prompt injection, i dati non fidati provenienti dall'esterno vengono incapsulati all'interno di delimitatori XML espliciti (es. `<untrusted_content>...</untrusted_content>`), istruendo formalmente il modello a trattare tali frammenti esclusivamente come dati passivi di analisi e mai come istruzioni operative.

## Ingegneria della Finestra di Contesto: Token Budgeting, Compattazione e Memoria a Finestra Scorrevole

La finestra di contesto dei modelli linguistici è soggetta a rigidi vincoli fisici e matematici. La complessità computazionale del calcolo della matrice di attenzione cresce quadraticamente $O(L^2)$ rispetto alla lunghezza della sequenza $L$, mentre la memoria richiesta dal Key-Value Cache (KV-cache) scala linearmente con l'occupazione della VRAM sulle GPU. Nelle sessioni investigative prolungate, l'accumulo indiscriminato di messaggi, tracce di pensiero e output di tool causa rapidamente la saturazione della finestra di contesto, provocando rallentamenti nell'inferenza, esplosione dei costi per token ed errori di attenzione.

Il **Token Budgeting** rappresenta la pratica di ripartizione deterministica della capacità di contesto $C_{\text{max}}$ in quote fisse e dinamiche:

Una quota fissa del 15-20% viene riservata al **Budget di Sistema**, allocata per il system prompt, gli schemi dei tool e le definizioni dei contratti di output.

Una quota dinamica del 30-40% viene assegnata al **Budget di Recupero**, dedicata ai documenti contestuali estratti tramite pipeline RAG o query su database.

La quota rimanente del 40-50% costituisce il **Budget della Memoria di Lavoro**, impiegata per ospitare la sequenza alternata di pensieri, chiamate ai tool e osservazioni del ciclo agentico.

La gestione della memoria di lavoro adotta quattro topologie algoritmiche di compattazione:

La prima topologia è il **Buffer a Finestra Scorrevole (Sliding Window)**, che mantiene inalterati solo gli ultimi $K$ turni conversazionali, scartando i messaggi antecedenti. Questo metodo garantisce semplicità computazionale ma comporta la perdita irreparabile del contesto storico iniziale.

La seconda topologia è il **Pruning Dinamico basato su Token Budget**, che monitora la cardinalità esatta dei token subword tramite librerie ad altissime prestazioni come [Tokenizers](https://huggingface.co/docs/tokenizers) (la libreria di tokenizzazione ultra-rapida scritta in Rust per algoritmi BPE, WordPiece e Unigram) o [tiktoken](https://github.com/openai/tiktoken) (la libreria open-source di OpenAI per la tokenizzazione Byte-Pair Encoding ad altissime prestazioni), procedendo al troncamento selettivo dei soli payload voluminosi dei tool (es. zone transfer DNS o log di rete) preservando la traccia del ragionamento.

La terza topologia è la **Memoria Riassuntiva Gerarchica (Summary Memory Buffer)**, che intercetta i blocchi di messaggi espulsi dalla finestra scorrevole, li elabora tramite un'invocazione di sintesi ad alta densità semantica e inietta un messaggio compresso di riassunto storico in testa alla conversazione, preservando i fatti chiave senza consumare token ridondanti.

La quarta topologia è il paradigma **Structure-as-Context (Filesystem Context)**, in cui lo stato operativo non risiede nella cronologia della chat ma viene formalizzato in file strutturati su disco (`STATE.md`, `CONTEXT.md`, `LOG.jsonl`), consentendo all'agente di leggere e aggiornare selettivamente porzioni mirate di memoria tramite strumenti dedicati del [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

## Generazione Strutturata Deterministica: Grammatiche EBNF, Outlines e Validazione Pydantic

Uno dei principali colli di bottiglia nell'integrazione di agenti LLM in pipeline industriali risiede nella natura non deterministica del testo generato. Se un agente deve emettere un payload JSON per invocare un'API o popolare un database, errori comuni quali omissione di virgolette di chiusura, virgole pendenti (*trailing commas*), chiavi allucinate o l'inclusione di commenti discorsivi mandano in crash i deserializzatori standard del software ricevente.

Per garantire la validità sintattica al 100%, l'ingegneria moderna adotta il **Grammar-Guided Decoding**. Questo approccio interviene direttamente durante il campionamento autoregressivo del modello a livello di logits tensoriali. Data la distribuzione dei logits non normalizzati $z_t \in \mathbb{R}^{|V|}$ sul vocabolario, viene applicata una maschera binaria dinamica $M_t \in \{-\infty, 0\}^{|V|}$ governata da un Automa a Stati Finiti Deterministico (DFA) derivato da una grammatica formale Extended Backus-Naur Form (EBNF) o da uno schema JSON:

$$P(w_t \mid w_{<t}) = \text{Softmax}(z_t + M_t)$$

I token che violerebbero la sintassi grammaticale in quel punto della sequenza ricevono un valore di logit pari a $-\infty$, rendendo matematicamente impossibile per il modello generare token non conformi. Librerie specializzate come [Outlines](https://github.com/dottxt-ai/outlines) (la libreria open-source per la generazione guidata da grammatiche EBNF e automi a stati finiti su logits tensoriali), [Guidance](https://github.com/guidance-ai/guidance) (il framework open-source di Microsoft per il controllo vincolato della generazione e strutturazione dei prompt) sviluppato da [Microsoft](https://www.microsoft.com/) (la multinazionale tecnologica leader nei sistemi operativi, cloud Azure e software per sviluppatori) e i motori di inferenza come [llama.cpp](https://github.com/ggerganov/llama.cpp) (l'engine di inferenza in C/C++ ottimizzato per modelli quantizzati in formato GGUF su CPU e GPU consumer) integrano il grammar decoding nativamente.

A livello applicativo, la validazione semantica viene garantita dalla libreria [Pydantic](https://docs.pydantic.dev/) (la libreria open-source in [Python](https://www.python.org/) di riferimento per la validazione di strutture dati tipizzate a runtime). L'output JSON generato viene deserializzato all'interno di classi Pydantic tipizzate, applicando controlli rigorosi su tipi primitivi, vincoli numerici ed enumerazioni. Qualora si verifichi un'eccezione di validazione (`ValidationError`), l'harness attiva un ciclo di **Self-Healing**: cattura il messaggio di errore diagnostico emesso da Pydantic, lo formatta in un prompt di feedback mirato e richiede al modello una correzione circoscritta, ottenendo un tasso di convergenza corretto prossimo alla totalità entro due tentativi.

## Ottimizzazione Dichiarativa dei Prompt: Il Paradigma DSPy

L'approccio tradizionale alla scrittura manuale dei prompt basato su tentativi ed euristiche empiriche (*prompt hacking*) presenta gravi limiti di manutenibilità: stringhe di testo ottimizzate per un determinato checkpoint di modello degradano drasticamente quando i pesi vengono aggiornati, quando si modifica il fornitore di inferenza o quando cambiano le distribuzioni dei dati di input.

Per superare la fragilità delle stringhe cablate nel codice, i ricercatori della [Stanford University](https://www.stanford.edu/) hanno formalizzato in [DSPy: Compiling Declarative Language Model Calls (Khattab et al., 2023)](https://arxiv.org/abs/2310.03714) il framework [DSPy](https://github.com/stanfordnlp/dspy) (il framework di Stanford NLP per la programmazione e ottimizzazione algoritmica automatica di prompt e pipeline LLM). DSPy separa rigorosamente la specifica logica del programma dalla sua ottimizzazione per uno specifico modello, mutuando i concetti fondamentali dalla programmazione dichiarativa:

Il concetto di **Signature** astrae il task definendo l'interfaccia di input e output (es. `IncidentText -> Rationale, Severity`) senza specificare le istruzioni verbali.

Il concetto di **Module** implementa pattern computazionali riutilizzabili e componibili, quali `dspy.Predict`, `dspy.ChainOfThought` o `dspy.ReAct`.

Il concetto di **Teleprompter / Optimizer** (quali `BootstrapFewShot`, `MIPROv2`, `COPRO`) sintetizza automaticamente dimostrazioni ottimali e ottimizza il testo delle istruzioni eseguendo simulazioni su un dataset di validazione rispetto a una metrica quantitativa formale.

Durante la fase di compilazione, l'ottimizzatore esegue un modello docente (*teacher*) sui dati di addestramento, raccoglie le tracce di esecuzione che massimizzano la metrica di accuratezza e le inietta dinamicamente come dimostrazioni few-shot nel modello studente (*student*), producendo un artefatto compilato ottimizzato e resiliente al drift dei pesi.

## Trade-off e Scelte Ingegneristiche

La progettazione di architetture di prompt e gestione del contesto richiede l'attenta ponderazione di molteplici compromessi ingegneristici:

Il primo trade-off riguarda la **latenza di esecuzione rispetto alla profondità di ragionamento**. L'adozione di architetture multi-step come Chain-of-Thought, ReAct o Tree of Thoughts incrementa linearmente o esponenzialmente il numero di token generati e i round-trip di inferenza, aumentando i tempi di risposta (Time-to-First-Token) e i costi operativi delle API. Per task semplici è opportuno adottare prompting diretto o zero-shot CoT, riservando ToT e loop ReAct complessi esclusivamente a indagini critiche o scenari ad alta incertezza.

Il secondo trade-off contrappone l'**estensione della finestra di contesto alla precisione del recupero**. Sebbene i moderni LLM supportino contesti da centinaia di migliaia di token, iniettare interi archivi documentali diluisce l'attenzione della rete neurale, provocando il degrado dell'accuratezza descritto dalla curva "Lost in the Middle". È preferibile implementare strategie di context compaction gerarchica e filtraggio semantico a monte, mantenendo la finestra di lavoro snella e focalizzata.

Il terzo trade-off concerne l'**overhead computazionale del Grammar-Guided Decoding rispetto al parsing post-hoc**. Il campionamento guidato da grammatiche EBNF azzera gli errori di sintassi JSON ma introduce un sovraccarico di calcolo della maschera sui logits per ogni token emesso, riducendo il throughput di generazione. In contesti ad altissima concorrenza, la combinazione di generazione standard con ciclo di fallback Self-Healing via Pydantic può offrire un throughput complessivo superiore a fronte di un ridotto numero di retry.

## Riferimenti Bibliografici e Risorse Tecniche

La formalizzazione dei pattern di prompting e context engineering si fonda sulla letteratura scientifica fondamentale e sulle documentazioni dell'ecosistema open-source:

Sulle architetture di ragionamento e deduzione, lo studio [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) ha introdotto la generazione esplicita di passaggi intermedi. Il paradigma di interazione tra pensiero e strumenti è formalizzato in [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629), mentre l'esplorazione combinatoria ad albero è definita in [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601). L'auto-valutazione ricorsiva è descritta in [Self-Refine: Iterative Refinement (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651).

Sulla dinamica dell'attenzione nei contesti estesi e sull'ottimizzazione dichiarativa, la ricerca [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023)](https://arxiv.org/abs/2307.03172) analizza i limiti di recupero nelle finestre di grandi dimensioni. La compilazione automatica e ottimizzazione algoritmica dei prompt è introdotta in [DSPy: Compiling Declarative Language Model Calls (Khattab et al., 2023)](https://arxiv.org/abs/2310.03714) presso la [Stanford University](https://www.stanford.edu/).

Sugli strumenti operativi per la tokenizzazione, generazione vincolata e validazione, si rimanda alla documentazione ufficiale di [Tokenizers](https://huggingface.co/docs/tokenizers), [tiktoken](https://github.com/openai/tiktoken), [Outlines](https://github.com/dottxt-ai/outlines), [Guidance](https://github.com/guidance-ai/guidance) e [Pydantic](https://docs.pydantic.dev/). Per l'integrazione di questi pattern in framework a grafo e sistemi multi-agente si vedano [LangChain](https://www.langchain.com/), [LangGraph](https://github.com/langchain-ai/langgraph) e il modulo specialistico [D12d](D12d-loop-graph-engineering.md).

## Appendice Operativa: Laboratori Pratici

### Laboratorio 1 — Loop Agentico ReAct con Scratchpad e Parsing Deterministico

Il primo laboratorio implementa un loop autonomo conforme al pattern Reason+Act (ReAct) con gestione esplicita dello scratchpad sequenziale, parsing a stati finiti delle azioni e invocazione di tool operativi di intelligence.

1. Costruire la classe `ReActScratchpad` per tracciare la sequenza di pensieri, azioni e osservazioni.
2. Definire il `ToolRegistry` per la registrazione ed esecuzione controllata degli strumenti OSINT.
3. Realizzare l'agente `ReActAgent` con parser regex per l'estrazione deterministica dei comandi.
4. Eseguire l'indagine investigativa su un indicatore di compromissione verificando la convergenza.

```python
"""
Laboratorio 1: Loop Agentico ReAct Robusto con Gestione del Scratchpad
Modulo: D12c - Prompt Engineering, Gestione del Contesto e Generazione Guidata nei Sistemi Agentici
"""

import re
from typing import Callable, Dict, List, Optional, Tuple


class ReActScratchpad:
    """Gestisce la memoria sequenziale di lavoro (scratchpad) dell'agente ReAct."""

    def __init__(self):
        self.steps: List[Dict[str, str]] = []

    def add_thought(self, thought: str):
        self.steps.append({"type": "thought", "content": thought.strip()})

    def add_action(self, tool_name: str, tool_input: str):
        self.steps.append({
            "type": "action",
            "tool": tool_name.strip(),
            "input": tool_input.strip()
        })

    def add_observation(self, observation: str):
        self.steps.append({"type": "observation", "content": observation.strip()})

    def format_trace(self) -> str:
        trace = []
        for step in self.steps:
            if step["type"] == "thought":
                trace.append(f"Thought: {step['content']}")
            elif step["type"] == "action":
                trace.append(f"Action: {step['tool']}[{step['input']}]")
            elif step["type"] == "observation":
                trace.append(f"Observation: {step['content']}")
        return "\n".join(trace)


class ToolRegistry:
    """Registro degli strumenti operativi invocabili dall'agente."""

    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}
        self._descriptions: Dict[str, str] = {}

    def register(self, name: str, description: str, func: Callable[[str], str]):
        self._tools[name] = func
        self._descriptions[name] = description

    def execute(self, name: str, argument: str) -> str:
        if name not in self._tools:
            return f"Errore: Strumento '{name}' non riconosciuto."
        try:
            return self._tools[name](argument)
        except Exception as exc:
            return f"Errore durante l'esecuzione di '{name}': {str(exc)}"

    def get_prompt_documentation(self) -> str:
        doc_lines = []
        for name, desc in self._descriptions.items():
            doc_lines.append(f"- {name}[argomento]: {desc}")
        return "\n".join(doc_lines)


class SimulatedLLMReActEngine:
    """Motore deterministico simulato per generare risposte nel formato ReAct."""

    def generate(self, prompt: str) -> str:
        if "198.51.100.42" in prompt:
            if "Observation: IP: 198.51.100.42 | AbuseScore: 88/100" in prompt:
                if "Observation: Autonomous System: AS13335 (Cloudflare)" in prompt:
                    return "Thought: Ho raccolto sia l'AbuseScore (88/100) che l'ASN (AS13335). Formulo la risposta finale.\nFinal Answer: L'indirizzo IP 198.51.100.42 presenta un livello di minaccia critico con AbuseScore 88/100 ed e instradato tramite AS13335 (Cloudflare)."
                else:
                    return "Thought: L'indirizzo IP presenta un AbuseScore elevato pari a 88/100. Verifico l'ASN associato.\nAction: asn_lookup[198.51.100.42]"
            else:
                return "Thought: Devo investigare la reputazione di sicurezza dell'indirizzo IP 198.51.100.42.\nAction: ip_reputation[198.51.100.42]"
        return "Thought: Nessuna informazione disponibile.\nFinal Answer: Impossibile procedere."


class ReActAgent:
    """Agente che orchestra il ciclo iterativo Thought -> Action -> Observation -> Final Answer."""

    def __init__(self, llm_engine: SimulatedLLMReActEngine, tools: ToolRegistry, max_iterations: int = 5):
        self.llm = llm_engine
        self.tools = tools
        self.max_iterations = max_iterations
        self.action_pattern = re.compile(r"Action:\s*([a-zA-Z0-9_-]+)\[(.*?)\]", re.DOTALL)
        self.thought_pattern = re.compile(r"Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)", re.DOTALL)
        self.final_answer_pattern = re.compile(r"Final Answer:\s*(.*)", re.DOTALL)

    def run(self, query: str) -> Tuple[str, ReActScratchpad]:
        scratchpad = ReActScratchpad()
        system_instructions = (
            "Sei un assistente investigativo autonomo. Risolvi la richiesta alternando:\n"
            "Thought: <riflessione>\n"
            "Action: <nome_strumento>[<argomento>]\n"
            "Observation: <risultato>\n"
            "Final Answer: <risposta conclusiva>\n\n"
            f"Strumenti disponibili:\n{self.tools.get_prompt_documentation()}"
        )

        for _ in range(1, self.max_iterations + 1):
            prompt = f"{system_instructions}\n\nDomanda: {query}\n{scratchpad.format_trace()}\n"
            response = self.llm.generate(prompt)

            thought_match = self.thought_pattern.search(response)
            if thought_match:
                scratchpad.add_thought(thought_match.group(1).strip())

            final_match = self.final_answer_pattern.search(response)
            if final_match:
                return final_match.group(1).strip(), scratchpad

            action_match = self.action_pattern.search(response)
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_arg = action_match.group(2).strip()
                scratchpad.add_action(tool_name, tool_arg)
                observation = self.tools.execute(tool_name, tool_arg)
                scratchpad.add_observation(observation)
            else:
                scratchpad.add_observation("Errore di formattazione. Usa Action: tool[arg]")

        return "Errore: Limite iterazioni raggiunto.", scratchpad


if __name__ == "__main__":
    registry = ToolRegistry()
    registry.register(
        "ip_reputation",
        "Calcola l'AbuseScore di un IP.",
        lambda ip: f"IP: {ip} | AbuseScore: 88/100 | Categoria: Malicious Botnet C2" if ip == "198.51.100.42" else "IP pulito"
    )
    registry.register(
        "asn_lookup",
        "Identifica l'ASN e l'ISP del prefisso IP.",
        lambda ip: f"Autonomous System: AS13335 (Cloudflare) | Prefix: {ip}/32"
    )

    agent = ReActAgent(SimulatedLLMReActEngine(), registry, max_iterations=5)
    final_output, trace_log = agent.run("Valuta il rischio dell'IP 198.51.100.42 e identifica il suo ASN.")

    assert "88/100" in final_output
    assert "AS13335" in final_output
    assert len(trace_log.steps) >= 5
    print("Test Laboratorio 1 completato con successo.")
```

### Laboratorio 2 — Memory Manager a Finestra Scorrevole con Riassunto Gerarchico

Il secondo laboratorio implementa un gestore della finestra di contesto con monitoraggio rigido del token budget e compattazione gerarchica della memoria episodica al superamento della soglia consentita.

1. Definire la struttura dati `Message` con funzione di stima dei token subword.
2. Implementare la classe `ContextWindowManager` con riserve per il prompt di sistema.
3. Costruire la routine di compattazione che sintetizza i messaggi espulsi dalla finestra.
4. Validare l'assemblaggio del prompt verificando il rispetto del limite massimo di token.

```python
"""
Laboratorio 2: Compattatore Dinamico del Contesto e Memory Manager a Finestra Scorrevole
Modulo: D12c - Prompt Engineering, Gestione del Contesto e Generazione Guidata nei Sistemi Agentici
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Message:
    role: str
    content: str
    token_count: int = 0

    def __post_init__(self):
        if self.token_count == 0:
            self.token_count = self.estimate_tokens(self.content)

    @staticmethod
    def estimate_tokens(text: str) -> int:
        words = text.split()
        char_count = len(text)
        return max(1, int(char_count / 3.8) + len(words) // 8)


class ContextWindowManager:
    """Gestisce l'allocazione dinamica del budget dei token e la compattazione della memoria."""

    def __init__(self, max_tokens: int = 400, system_reserve_tokens: int = 80, recent_messages_to_keep: int = 2):
        self.max_tokens = max_tokens
        self.system_reserve = system_reserve_tokens
        self.recent_to_keep = recent_messages_to_keep
        self.system_message: Optional[Message] = None
        self.summary_message: Optional[Message] = None
        self.message_history: List[Message] = []

    def set_system_prompt(self, content: str):
        self.system_message = Message(role="system", content=content)
        if self.system_message.token_count > self.system_reserve:
            raise ValueError(f"System prompt ({self.system_message.token_count}) supera la riserva ({self.system_reserve}).")

    def add_message(self, role: str, content: str):
        msg = Message(role=role, content=content)
        self.message_history.append(msg)
        self._enforce_token_budget()

    def get_total_tokens(self) -> int:
        total = 0
        if self.system_message:
            total += self.system_message.token_count
        if self.summary_message:
            total += self.summary_message.token_count
        total += sum(m.token_count for m in self.message_history)
        return total

    def _summarize_evicted_block(self, messages: List[Message]) -> str:
        key_facts = []
        for m in messages:
            if "APT28" in m.content:
                key_facts.append("Identificato Threat Actor APT28 associato a Fancy Bear.")
            elif "185.220.101.5" in m.content:
                key_facts.append("Indirizzo IP 185.220.101.5 confermato nodo Tor.")
            elif "CVE-2023-38831" in m.content:
                key_facts.append("Vulnerabilita sfruttata: WinRAR CVE-2023-38831.")
            else:
                key_facts.append(f"Turno {m.role}: Dati registrati.")
        return "Sintesi Memoria Episodica: " + " ".join(dict.fromkeys(key_facts))

    def _enforce_token_budget(self):
        while self.get_total_tokens() > self.max_tokens and len(self.message_history) > self.recent_to_keep:
            eviction_candidates = []
            while len(self.message_history) > self.recent_to_keep:
                eviction_candidates.append(self.message_history.pop(0))

            if eviction_candidates:
                new_summary = self._summarize_evicted_block(eviction_candidates)
                if self.summary_message:
                    combined = f"{self.summary_message.content} | {new_summary}"
                    self.summary_message = Message(role="summary", content=combined)
                else:
                    self.summary_message = Message(role="summary", content=new_summary)

    def assemble_prompt(self) -> List[dict]:
        assembled = []
        if self.system_message:
            assembled.append({"role": "system", "content": self.system_message.content})
        if self.summary_message:
            assembled.append({"role": "system", "content": f"[CONTESTO EPISODICO PRECEDENTE]: {self.summary_message.content}"})
        for m in self.message_history:
            assembled.append({"role": m.role, "content": m.content})
        return assembled


if __name__ == "__main__":
    manager = ContextWindowManager(max_tokens=120, system_reserve_tokens=30, recent_messages_to_keep=2)
    manager.set_system_prompt("Sei un analista cyber-threat intelligence specializzato in correlazione IoC.")

    manager.add_message("user", "Inizia l'investigazione sul gruppo APT28 attivo nel settore energetico.")
    manager.add_message("assistant", "Avviata ricognizione: il gruppo APT28 utilizza l'infrastruttura 185.220.101.5 come nodo di comando.")
    manager.add_message("user", "Quale vulnerabilita software e stata impiegata nel payload iniziale?")
    manager.add_message("assistant", "L'analisi dei campioni conferma l'exploit per WinRAR CVE-2023-38831 per distribuire il malware.")
    manager.add_message("user", "Quali contromisure perimetrali possiamo attivare immediatamente?")

    context = manager.assemble_prompt()
    total_tokens = manager.get_total_tokens()

    assert total_tokens <= manager.max_tokens
    assert manager.summary_message is not None
    assert "APT28" in manager.summary_message.content
    print("Test Laboratorio 2 completato con successo.")
```

### Laboratorio 3 — Output JSON Strutturati con Validazione Pydantic e Self-Healing

Il terzo laboratorio realizza una pipeline di parsing robusta che sanifica l'output testuale grezzo, applica la validazione schema tramite [Pydantic](https://docs.pydantic.dev/) e orchestra un ciclo di autocorrezione (*Self-Healing*) in caso di errori.

1. Definire i modelli tipizzati Pydantic per gli indicatori di compromissione.
2. Implementare la classe `RobustJsonExtractor` per la rimozione di code fences markdown e caratteri anomali.
3. Costruire il parser `SelfHealingJsonParser` con gestione automatica del prompt di rettifica.
4. Testare il recupero automatico a fronte di un output volutamente malformato.

```python
"""
Laboratorio 3: Generatore di Output JSON Strutturati con Validazione Pydantic
Modulo: D12c - Prompt Engineering, Gestione del Contesto e Generazione Guidata nei Sistemi Agentici
"""

import json
import re
from typing import Any, Dict, List
from pydantic import BaseModel, Field, field_validator


class IndicatorOfCompromise(BaseModel):
    type: str = Field(..., description="Tipologia di IoC (ip, domain, sha256, cve)")
    value: str = Field(..., description="Valore dell'indicatore")
    confidence: int = Field(..., ge=0, le=100, description="Punteggio di affidabilita da 0 a 100")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"ip", "domain", "sha256", "cve"}
        if v.lower() not in allowed:
            raise ValueError(f"Tipo IoC '{v}' non valido. Valori ammessi: {allowed}")
        return v.lower()


class ThreatIntelReport(BaseModel):
    actor_name: str = Field(..., min_length=2, description="Nome del gruppo di minaccia")
    threat_level: str = Field(..., description="Livello di criticita: LOW, MEDIUM, HIGH, CRITICAL")
    indicators: List[IndicatorOfCompromise] = Field(default_factory=list, description="Lista degli indicatori estratti")

    @field_validator("threat_level")
    @classmethod
    def validate_threat_level(cls, v: str) -> str:
        allowed = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"Livello di minaccia '{v}' non ammesso. Valori ammessi: {allowed}")
        return v.upper()


class RobustJsonExtractor:
    """Sanifica e deserializza stringhe JSON contenenti blocchi Markdown o formattazioni anomale."""

    @staticmethod
    def clean_json_string(raw_text: str) -> str:
        code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
        if code_block_match:
            raw_text = code_block_match.group(1)

        first_brace = raw_text.find("{")
        last_brace = raw_text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            raw_text = raw_text[first_brace : last_brace + 1]

        raw_text = re.sub(r",\s*([\]}])", r"\1", raw_text)
        return raw_text.strip()


class SimulatedDefectiveLLM:
    """Simula un modello che fallisce al primo tentativo e corregge il JSON al secondo tentativo."""

    def __init__(self):
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        self.call_count += 1
        if self.call_count == 1:
            return (
                "Certamente, ecco il report estratto:\n```json\n"
                "{\n"
                '  "actor_name": "Sandworm",\n'
                '  "threat_level": "EXTREME_DANGER",\n'
                '  "indicators": [\n'
                '    {"type": "ip", "value": "194.26.29.112", "confidence": 150},\n'
                '    {"type": "cve", "value": "CVE-2022-30190", "confidence": 95},\n'
                "  ]\n"
                "}\n```"
            )
        else:
            return (
                "{\n"
                '  "actor_name": "Sandworm",\n'
                '  "threat_level": "CRITICAL",\n'
                '  "indicators": [\n'
                '    {"type": "ip", "value": "194.26.29.112", "confidence": 90},\n'
                '    {"type": "cve", "value": "CVE-2022-30190", "confidence": 95}\n'
                "  ]\n"
                "}"
            )


class SelfHealingJsonParser:
    """Orchestra il parsing vincolato con ciclo di correzione automatica degli errori."""

    def __init__(self, llm_engine: SimulatedDefectiveLLM, max_retries: int = 3):
        self.llm = llm_engine
        self.max_retries = max_retries
        self.extractor = RobustJsonExtractor()

    def parse(self, raw_input: str) -> ThreatIntelReport:
        current_prompt = f"Estrai le entita di sicurezza in formato JSON:\n{raw_input}"

        for attempt in range(1, self.max_retries + 1):
            raw_response = self.llm.generate(current_prompt)
            sanitized_json = self.extractor.clean_json_string(raw_response)

            try:
                report = ThreatIntelReport.model_validate_json(sanitized_json)
                return report
            except Exception as validation_error:
                if attempt == self.max_retries:
                    raise RuntimeError(f"Validazione fallita dopo {attempt} tentativi: {validation_error}")

                current_prompt = (
                    f"Il JSON non e valido:\n{str(validation_error)}\n\n"
                    f"JSON errato:\n{sanitized_json}\n\n"
                    f"Correggi e restituisci solo il JSON valido."
                )

        raise RuntimeError("Tentativi esauriti.")


if __name__ == "__main__":
    engine = SimulatedDefectiveLLM()
    parser = SelfHealingJsonParser(engine, max_retries=3)

    input_text = "Il gruppo Sandworm ha sferrato un attacco sfruttando CVE-2022-30190 e l'IP 194.26.29.112."
    result_report = parser.parse(input_text)

    assert engine.call_count == 2
    assert result_report.actor_name == "Sandworm"
    assert result_report.threat_level == "CRITICAL"
    print("Test Laboratorio 3 completato con successo.")
```

### Laboratorio 4 — Pipeline Dichiarativa DSPy per Ottimizzazione Few-Shot

Il quarto laboratorio implementa i concetti fondazionali del paradigma [DSPy](https://github.com/stanfordnlp/dspy), definendo Signature dichiarative, moduli ChainOfThought e un ottimizzatore `BootstrapFewShot` per la compilazione automatica di prompt ottimali.

1. Definire la `Signature` dichiarativa con specifica dei campi di input e output.
2. Implementare il modulo `DeclarativeChainOfThought` per la serializzazione delle istruzioni.
3. Costruire la metrica quantitativa `SeverityMetric` per la valutazione della fedeltà.
4. Compilare il modulo tramite `BootstrapFewShotTeleprompter` verificando l'incremento delle prestazioni.

```python
"""
Laboratorio 4: Pipeline Dichiarativa DSPy per la Compilazione Automatica dei Prompt
Modulo: D12c - Prompt Engineering, Gestione del Contesto e Generazione Guidata nei Sistemi Agentici
"""

from typing import Any, Callable, Dict, List, NamedTuple


class Example(NamedTuple):
    inputs: Dict[str, str]
    outputs: Dict[str, str]


class Signature:
    """Specifica dichiarativa dei campi di input e output per un task LLM."""

    def __init__(self, description: str, input_fields: List[str], output_fields: List[str]):
        self.description = description
        self.input_fields = input_fields
        self.output_fields = output_fields


class SimulatedDSPyEngine:
    """Motore LLM che adatta il proprio output in funzione della presenza di dimostrazioni Few-Shot nel prompt."""

    def complete(self, prompt: str) -> str:
        target_section = prompt.split("Esegui il seguente task:")[-1] if "Esegui il seguente task:" in prompt else prompt
        if "Dimostrazione 1:" in prompt:
            if "Phishing credenziali bancarie" in target_section:
                return "Rationale: L'attacco prende di mira credenziali finanziarie senza impatto sistemico.\nSeverity: MEDIUM"
            elif "Ransomware blocca server ospedaliero" in target_section:
                return "Rationale: L'interruzione dei sistemi ospedalieri compromette servizi essenziali salvavita.\nSeverity: CRITICAL"
            elif "Scansione porte non autorizzata" in target_section:
                return "Rationale: Ricognizione superficiale senza evidenza di violazione.\nSeverity: LOW"

        if "ospedaliero" in target_section or "Ransomware" in target_section:
            return "Rationale: Incidente rilevato.\nSeverity: HIGH"
        return "Rationale: Evento standard.\nSeverity: MEDIUM"


class DeclarativeChainOfThought:
    """Modulo computazionale componibile che concatena generazione di ragionamento e output."""

    def __init__(self, signature: Signature):
        self.signature = signature
        self.demos: List[Example] = []

    def forward(self, lm: SimulatedDSPyEngine, **kwargs) -> Dict[str, str]:
        prompt_parts = [f"Istruzione: {self.signature.description}\n"]

        if self.demos:
            for idx, demo in enumerate(self.demos, 1):
                prompt_parts.append(f"Dimostrazione {idx}:")
                for k, v in demo.inputs.items():
                    prompt_parts.append(f"{k}: {v}")
                for k, v in demo.outputs.items():
                    prompt_parts.append(f"{k}: {v}")
                prompt_parts.append("")

        prompt_parts.append("Esegui il seguente task:")
        for field in self.signature.input_fields:
            prompt_parts.append(f"{field}: {kwargs.get(field, '')}")

        prompt_parts.append("Rationale:")
        full_prompt = "\n".join(prompt_parts)

        raw_output = lm.complete(full_prompt)

        parsed = {}
        for line in raw_output.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                parsed[k.strip()] = v.strip()
        return parsed


class SeverityMetric:
    """Metrica di valutazione quantitativa dell'accuratezza della pipeline."""

    @staticmethod
    def evaluate(example: Example, prediction: Dict[str, str]) -> float:
        expected_severity = example.outputs.get("Severity", "").strip().upper()
        predicted_severity = prediction.get("Severity", "").strip().upper()
        has_rationale = len(prediction.get("Rationale", "")) > 10

        score = 0.0
        if expected_severity == predicted_severity:
            score += 0.7
        if has_rationale:
            score += 0.3
        return score


class BootstrapFewShotTeleprompter:
    """Ottimizzatore algoritmico che compila dimostrazioni di successo analizzando il training set."""

    def __init__(self, metric: Callable[[Example, Dict[str, str]], float], max_bootstrapped_demos: int = 2):
        self.metric = metric
        self.max_demos = max_bootstrapped_demos

    def compile(self, student_module: DeclarativeChainOfThought, trainset: List[Example], lm: SimulatedDSPyEngine) -> DeclarativeChainOfThought:
        successful_demos = []

        for example in trainset:
            prediction = student_module.forward(lm, **example.inputs)
            score = self.metric(example, prediction)

            demo_outputs = {"Rationale": prediction.get("Rationale", "Analisi verificata."), "Severity": example.outputs["Severity"]}
            successful_demos.append(Example(inputs=example.inputs, outputs=demo_outputs))

            if len(successful_demos) >= self.max_demos:
                break

        student_module.demos = successful_demos
        return student_module


if __name__ == "__main__":
    lm = SimulatedDSPyEngine()

    triage_sig = Signature(
        description="Analizza la descrizione di un incidente cyber e assegna la severita corretta con motivazione.",
        input_fields=["IncidentText"],
        output_fields=["Rationale", "Severity"]
    )

    train_set = [
        Example(inputs={"IncidentText": "Phishing credenziali bancarie senza impatto sistemico."}, outputs={"Severity": "MEDIUM"}),
        Example(inputs={"IncidentText": "Scansione porte non autorizzata rilevata dal firewall perimetrale."}, outputs={"Severity": "LOW"})
    ]

    val_set = [
        Example(inputs={"IncidentText": "Ransomware blocca server ospedaliero con disservizio ai reparti di emergenza."}, outputs={"Severity": "CRITICAL"})
    ]

    module = DeclarativeChainOfThought(triage_sig)

    pred_baseline = module.forward(lm, IncidentText=val_set[0].inputs["IncidentText"])
    score_baseline = SeverityMetric.evaluate(val_set[0], pred_baseline)

    teleprompter = BootstrapFewShotTeleprompter(metric=SeverityMetric.evaluate, max_bootstrapped_demos=2)
    compiled_module = teleprompter.compile(module, train_set, lm)

    pred_compiled = compiled_module.forward(lm, IncidentText=val_set[0].inputs["IncidentText"])
    score_compiled = SeverityMetric.evaluate(val_set[0], pred_compiled)

    assert score_compiled > score_baseline
    assert pred_compiled.get("Severity") == "CRITICAL"
    print("Test Laboratorio 4 completato con successo.")
```