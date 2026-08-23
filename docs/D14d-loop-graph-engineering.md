---
aliases: [D12d, Loop Engineering, Graph Engineering, LangGraph, State Graph, Macchine a Stati Cicliche, Checkpointing, Multi-Agent Routing]
---

# Architettura dei Loop Agenti, Grafi di Stato Ciclici e Sistemi Multi-Agente

L'**architettura a grafi di stato ciclici (State Graph Engineering)** modella i sistemi di intelligenza artificiale agentica come macchine a stati a grafo orientato, in cui i nodi eseguono computazioni o chiamate a modelli linguistici e gli archi diretti e condizionali governano le transizioni di controllo in base all'evoluzione di uno stato tipizzato e immutabile. Questo paradigma trova impiego primario nell'orchestrazione di investigazioni complesse su fonti aperte ([D11](D13-osint-avanzato.md)), nell'analisi forense iterativa, nei processi di generazione e debug autonomo del codice e nei flussi di lavoro aziendali che richiedono validazione umana nel ciclo (*Human-in-the-Loop*). L'ingegneria dei grafi di stato esiste per superare i limiti strutturali delle pipeline lineari acicliche (DAG), conferendo agli agenti la capacità di eseguire cicli di auto-correzione, persistere la memoria operativa su database relazionali tramite checkpointing incrementale e coordinare topologie multi-agente gerarchiche o collaborative con garanzie formali di terminazione e ripristino.

```
+-----------------------------------------------------------------------------------------+
|                    DAG LINEARE VS GRAFO DI STATO CICLICO (STATEGRAPH)                   |
+-----------------------------------------------------------------------------------------+

  1. DAG Lineare (Fragile su Errori):
     [ Input ] ──► [ Pianificazione ] ──► [ Esecuzione Tool ] ──► [ Sintesi ] ──► [ Output ]
                                                  │
                                                  ▼ (Errore / Fallimento)
                                             [ CRASH / ABORT ]

  2. Grafo di Stato Ciclico (Resiliente con Feedback Loop):
     [ START ] ──► [ Pianificatore ] ◄─────────────────────────────────────┐
                          │                                                 │
                          ▼                                                 │ (Retry / Refine)
                  [ Esecutore Tool ] ──► [ Validatore / Reflection ] ───────┘
                          │                       │
                          │ (Successo)            │ (Superato Budget Retry)
                          ▼                       ▼
                   [ Sintesi Finale ]       [ Fallback Node ]
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                                   [ END ]
```

## Il Limite dei Grafi Aciclici (DAG) e la Genesi delle Macchine a Stati Cicliche

Le prime architetture di orchestrazione per modelli linguistici modellavano i flussi di lavoro come catene sequenziali rigide o Grafi Aciclici Diretti (Directed Acyclic Graphs, DAG). In un DAG, l'esecuzione procede in modo rigorosamente monodirezionale dall'input iniziale verso l'output terminale attraverso una sequenza di nodi di elaborazione prefissati. Sebbene questa topologia risulti adeguata per pipeline di data processing deterministiche, essa collassa quando applicata a compiti cognitivi complessi caratterizzati da elevata incertezza stocastica. Se un Large Language Model all'interno di un DAG genera codice sintatticamente errato, formula una chiamata a un tool con argomenti non validi o interroga una fonte OSINT che restituisce una risposta vuota, l'intera pipeline si interrompe bruscamente con un fallimento irrecuperabile.

Al contrario, i processi di indagine umana e di problem solving operano secondo cicli iterativi di esplorazione, sperimentazione, osservazione dell'errore, riflessione e rettifica progressiva. Per conferire queste medesime capacità agli agenti artificiali, è necessario superare il vincolo dell'aciclicità introducendo cicli di retroazione (*feedback loops*) all'interno della topologia di controllo. Una **macchina a stati ciclica** per agenti viene formalmente definita come una quintupla matematica:

$$M = (S, \Sigma, \delta, s_0, F)$$

In questa formulazione, $S$ rappresenta lo spazio degli stati globali tipizzati del sistema, $\Sigma$ costituisce l'alfabeto degli eventi, dei messaggi e delle osservazioni esterne, $\delta: S \times \Sigma \to S$ è la funzione di transizione di stato, $s_0 \in S$ è lo stato iniziale di ingresso (`START`), e $F \subseteq S$ è l'insieme degli stati terminali di convergenza (`END`). L'introduzione di cicli orientati nel grafo permette all'agente di ritornare sui propri passi, iterare su nodi di auto-correzione a fronte di eccezioni del compilatore o di fallimenti dei tool, ed esplorare ipotesi alternative fino al raggiungimento dei criteri di successo prefissati o all'esaurimento del budget computazionale.

## Anatomia di uno StateGraph: Nodi, Canali di Stato e Funzioni Reducer

L'implementazione concreta di un grafo di stato ciclico, resa celebre dalla libreria [LangGraph](https://github.com/langchain-ai/langgraph) (la libreria di orchestrazione di LangChain per costruire architetture agentiche cicliche a grafo con stato persistente) di [LangChain](https://www.langchain.com/) (il framework open-source per la costruzione di applicazioni, catene e integrazioni guidate da Large Language Model), scompone l'architettura in quattro primitive cardine: Nodi, Canali di Stato, Funzioni Reducer e Archi Condizionali.

I **Nodi** rappresentano unità atomiche di computazione o invocazione di modelli linguistici. Da un punto di vista formale, ogni nodo $N_i$ è una funzione pura o asincrona $f: S \to \Delta S$ che riceve in sola lettura lo stato globale corrente $S$, esegue un'elaborazione deterministica o una chiamata a LLM, e restituisce un dizionario contenente esclusivamente il delta delle modifiche $\Delta S$. Questo principio di isolamento garantisce che i singoli nodi rimangano disaccoppiati e facilmente testabili in isolamento.

I **Canali di Stato** definiscono lo schema strutturato dei dati condivisi tra i nodi, tipizzato in [Python](https://www.python.org/) (il linguaggio di programmazione ad alto livello di riferimento globale per intelligenza artificiale e data science) mediante classi `TypedDict` o modelli [Pydantic](https://docs.pydantic.dev/) (la libreria open-source per la modellazione e validazione di strutture dati tipizzate a runtime). Per evitare corruzioni di memoria e race condition durante l'aggiornamento simultaneo dello stato da parte di nodi concorrenti, la convergenza delle mutazioni è governata dalle **Funzioni Reducer**.

I canali a **sovrascrittura predefinita** (*overwrite reducers*) rimpiazzano il valore precedente con il nuovo valore emesso dal nodo, modalità adatta per variabili di stato monovalore quali flag di controllo, contatori di iterazione o stati di errore.

I canali ad **accumulo sequenziale** (*append-only reducers*), annotati tipicamente con `operator.add`, consentono a molteplici nodi di accodare messaggi, log di audit o evidenze informative a una lista condivisa senza provocare la perdita delle osservazioni storiche pregresse.

I canali con **reducer personalizzati** gestiscono il merge di dizionari complessi, la risoluzione di conflitti di scrittura tra agenti paralleli o il mantenimento di finestre scorrevoli a dimensione vincolata.

Infine, il controllo del flusso è regolato dagli **Archi Condizionali**. Un arco condizionale associa al nodo sorgente una funzione di routing deterministica $r: S \to K$ che ispeziona i campi dello stato (ad esempio lo stato di validazione o il conteggio delle iterazioni) e seleziona dinamicamente il nome del nodo destinatario all'interno di una mappa di transizione chiusa.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D12d-loop-graph-engineering. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Persistenza dello Stato, Checkpointing e Meccanica del Time-Travel

La gestione della memoria puramente in-memory all'interno dei processi applicativi espone i flussi agentici al rischio di perdita totale dello stato in caso di crash dell'interprete, riciclo del container ospite o interruzione della connettività di rete durante investigazioni che possono protrarsi per ore. Per conferire robustezza enterprise, l'architettura integra un layer di **checkpointing persistente** su basi di dati relazionali, quali [SQLite](https://www.sqlite.org/) (il motore di database relazionale compatto, serverless e standalone basato su file) in ambienti locali ed edge, o [PostgreSQL](https://www.postgresql.org/) (il sistema di gestione di database relazionale a oggetti open-source rinomato per affidabilità ed estendibilità) in cluster di produzione.

Il Checkpointer intercetta ogni transizione di stato atomica al termine dell'esecuzione di ciascun nodo, serializza l'intero stato globale in formato JSON o binario e lo registra atomicamente nel database all'interno di una tupla formale:

$$\text{Checkpoint} = \langle \text{thread\_id}, \text{checkpoint\_id}, \text{parent\_checkpoint\_id}, \text{node\_name}, S, \text{timestamp} \rangle$$

L'identificatore `thread_id` isola logicamente le sessioni investigative parallele, mentre la relazione padre-figlio tra checkpoint modella l'intera traiettoria esecutiva come un albero genealogico immutabile. Questa infrastruttura abilita la potente capacità del **Time-Travel (Viaggio nel Tempo)**.

```
+-----------------------------------------------------------------------------------------+
|                  CHECKPOINTING INCREMENTALE E ALBERO DI TIME-TRAVEL                     |
+-----------------------------------------------------------------------------------------+

 Thread: "investigazione_osint_042"

 [ CP-1: START ] ──► [ CP-2: Node_Pianifica ] ──► [ CP-3: Node_Tool_Ricerca ]
                                                          │
                               ┌──────────────────────────┴──────────────────────────┐
                               ▼ (Ramo A: Risultato Nullo)                           ▼ (Ramo B: Rollback & Modifica Query)
                     [ CP-4a: Node_Valida_KO ]                             [ CP-4b: Node_Tool_Ricerca_Avanzata ]
                               │                                                     │
                     [ CP-5a: Errore / Abort ]                                       ▼
                                                                           [ CP-5b: Node_Sintesi_OK ] ──► [ CP-6b: END ]
```

Attraverso il time-travel, l'analista o il runtime possono riavvolgere l'esecuzione a qualsiasi checkpoint storico $C_k$, ispezionare il valore esatto di ogni variabile di stato in quel preciso istante, modificare manualmente parametri errati (es. correggere un selettore di ricerca o un intervallo temporale) e riprendere l'esecuzione lungo un nuovo ramo divergente (*forking*). Oltre al ripristino trasparente dopo un crash, il checkpointing garantisce una tracciabilità forense completa e verificabile, essenziale per la conformità normativa e la revisione delle decisioni assunte dai sistemi autonomi.

## Topologie di Orchestrazione Multi-Agente: Supervisor, Gerarchie e Network P2P

All'aumentare della specializzazione richiesta per compiti investigativi complessi, l'architettura evolve da singoli agenti monolitici a sistemi multi-agente collaborativi. La letteratura e l'ingegneria del software formalizzano tre topologie principali di coordinamento:

La topologia **Supervisor / Router** adotta un modello centralizzato a stella. Un agente supervisore primario riceve l'obiettivo dell'utente, analizza lo stato complessivo delle informazioni e delega compiti atomici a nodi agenti specialisti (`OSINTCollector`, `DataAnalyst`, `SecurityAuditor`). Ciascun worker esegue il proprio compito e restituisce il controllo al supervisore, che valuta se l'evidenza raccolta sia sufficiente per formulare il report finale o se sia necessaria un'ulteriore delegazione.

La topologia **Gerarchica a Squadre (Hierarchical Teams)** modella l'organizzazione aziendale attraverso grafi di stato annidati. Il supervisore di primo livello coordina sottografi specializzati, in cui ciascun sottografo opera come un team autonomo dotato di un proprio supervisore locale e di worker dedicati (ad esempio il Team Infrastrutture di Rete e il Team Analisi Finanziaria), incapsulando la complessità interna e restituendo solo sintesi aggregate al livello superiore.

La topologia **Collaborativa Peer-to-Peer (P2P / Group Chat)**, tipica di framework come [AutoGen](https://microsoft.github.io/autogen/) (il framework open-source di Microsoft per la creazione di sistemi multi-agente conversazionali collaborativi) di [Microsoft](https://www.microsoft.com/) (la multinazionale informatica leader nei sistemi operativi, cloud computing enterprise con Azure e software per sviluppatori), [CrewAI](https://www.crewai.com/) (il framework open-source per l'orchestrazione di team di agenti autonomi basati su ruoli specializzati) e [CAMEL-AI](https://www.camel-ai.org/) (il framework di ricerca open-source pioniere nello studio di agenti autonomi comunicanti e cooperative learning), prevede che gli agenti dialoghino direttamente tra loro passando il turno di parola secondo regole di round-robin o selezioni dinamiche del prossimo oratore basate sul contenuto della discussione.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Controllo Umano nel Ciclo (Human-in-the-Loop) e Interruzioni di Grafo

Nelle applicazioni critiche di cybersecurity, intelligence e finanza, l'autonomia illimitata degli agenti comporta rischi inaccettabili. L'ingegneria dei grafi a stati implementa nativamente il paradigma **Human-in-the-Loop (HIL)** attraverso meccanismi di interruzione deterministica denominati **breakpoint**:

La direttiva `interrupt_before` arresta automaticamente l'esecuzione del grafo immediatamente prima dell'ingresso in uno o più nodi designati come critici (quali l'esecuzione di scansioni di rete intrusive, l'invio di notifiche esterne o la mutazione di database).

La direttiva `interrupt_after` sospende il grafo subito dopo che un nodo ha prodotto la propria bozza di output, prima che lo stato venga propagato ai nodi a valle o che vengano intraprese azioni conseguenti.

Quando si attiva un breakpoint, il motore persiste lo stato corrente sul checkpointer, imposta lo stato di esecuzione su `PAUSED` e rilascia il thread di calcolo. Un'interfaccia utente o un'API REST espone lo stato congelato all'analista umano, il quale può ispezionare le azioni proposte, validare l'autorizzazione o applicare un **override manuale** modificando direttamente i campi dello stato (ad esempio riducendo l'intensità di una scansione o correggendo un'ipotesi investigativa). Richiamando la funzione `resume(thread_id)`, il grafo riprende l'esecuzione esattamente dal punto di interruzione applicando le modifiche umane, garantendo un controllo operativo rigoroso e non eludibile.

## Cicli di Auto-Correzione, Reflection e Tolleranza ai Guasti

L'abilità distintiva di un'architettura ciclica risiede nella capacità di eseguire routine di **Reflection e Auto-Correzione**. In questo pattern, un nodo generatore produce un manufatto (codice sorgente, query SQL, payload di configurazione), un nodo validatore ne verifica la correttezza eseguendolo in un sandbox isolato o applicando linter deterministici, e, in caso di esito negativo, un nodo di riflessione analizza la traccia dell'eccezione formulando una diagnosi delle cause radice.

Il delta diagnostico viene re-iniettato nello stato globale e passato nuovamente al generatore, che sintetizza una versione corretta condizionata sull'errore precedente. Per prevenire loop infiniti generati da errori non risolvibili, l'architettura impone un contatore di iterazioni vincolato a una soglia massima ($k \le k_{\text{max}}$). Al raggiungimento del limite, il router condizionale devia il flusso verso un nodo di **fallback degradato**, che registra il mancato raggiungimento della convergenza ed effettua un'escalation all'operatore umano con il log dettagliato dei tentativi eseguiti.

Inoltre, è fondamentale distinguere i grafi di controllo di flusso agentico ([LangGraph](https://github.com/langchain-ai/langgraph)) dai knowledge graph di rappresentazione della conoscenza, quali [Neo4j](https://neo4j.com/) (il sistema di gestione di database orientato ai grafi leader industriale per modellare relazioni e query Cypher) e [NetworkX](https://networkx.org/) (il pacchetto Python open-source per la creazione, manipolazione e studio di reti complesse e grafi). Mentre LangGraph governa la macchina a stati computazionale del software, Neo4j funge da memoria semantica a lungo termine: i nodi dello StateGraph interrogano ed espandono le relazioni del knowledge graph mediante query Cypher per arricchire il contesto dell'agente.


> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.


## Analisi Comparativa dei Framework Multi-Agente

Il panorama dei framework per l'ingegneria dei cicli agentici presenta approcci architetturali differenziati in base al paradigma di astrazione adottato:

| Dimensione Architetturale | LangGraph | AutoGen | CrewAI | CAMEL-AI |
| :--- | :--- | :--- | :--- | :--- |
| **Modello di Controllo** | Grafo di stato esplicito con cicli e reducer | Conversazionale multi-agente / Actor model | Dichiarativo basato su ruoli e processi | Comunicativo a coppie di agenti (Inception) |
| **Gestione dello Stato** | Canali tipizzati e reducer (`TypedDict`) | Cronologia messaggi conversazionali | Memoria di contesto condivisa | Registro dei messaggi di dialogo |
| **Persistenza & Checkpoint** | Checkpointer nativo (SQLite, Postgres, Redis) | Stato conversazionale serializzabile | Memoria a breve/lungo termine integrata | Stato effimero in-memory |
| **Human-in-the-Loop** | Breakpoint precisi (`interrupt_before/after`) | Intervento umano come agente conversazionale | Validazione manuale dei task | Non nativo (sperimentale) |
| **Complessità Topologica** | Grafi arbitrari, supervisor, sottografi | Chat di gruppo, routing a broadcast/speaker | Sequenziale e gerarchico | Diadica (due agenti) o gerarchica |
| **Determinismo Esecutivo** | Elevato (transizioni di stato controllate) | Moderato (guidato da dinamiche conversazionali)| Medio (guidato da ruoli e prompt) | Basso (interamente emergente) |

[LangGraph](https://github.com/langchain-ai/langgraph) offre il massimo livello di controllo e determinismo ingegneristico, risultando la scelta d'elezione per flussi di lavoro complessi e processi mission-critical. [AutoGen](https://microsoft.github.io/autogen/) di [Microsoft](https://www.microsoft.com/) eccelle nella simulazione di dinamiche conversazionali flessibili tra agenti autonomi. [CrewAI](https://www.crewai.com/) fornisce un'astrazione dichiarativa immediata per team basati su ruoli operativi, mentre [CAMEL-AI](https://www.camel-ai.org/) rappresenta la piattaforma pionieristica per la ricerca accademica sui comportamenti cooperativi emergenti.

## Trade-off e Scelte Ingegneristiche

La progettazione di macchine a stati a grafo per sistemi agentici richiede un bilanciamento tra molteplici compromessi architetturali:

Il primo trade-off contrappone il **determinismo dei vincoli di transizione alla flessibilità autonoma emergente**. Topologie a grafo fortemente strutturate con archi condizionali rigidi garantiscono la sicurezza e la conformità del flusso operativo, ma limitano la capacità dell'agente di improvvisare piani innovativi di fronte a problemi inediti. Per compiti esplorativi aperti è opportuno concedere al router maggiore autonomia decisionale, vincolando invece i rami mutativi a nodi rigorosamente controllati.

Il secondo trade-off riguarda la **latenza di I/O del checkpointing sincrono rispetto alla resilienza operativa**. Il salvataggio dello stato completo su database relazionale dopo ogni singolo step introduce un overhead computazionale che può incidere sulle prestazioni in cicli ad altissima frequenza. In workflow distribuiti su larga scala, è possibile adottare checkpointing asincrono o selettivo, limitando la persistenza ai soli nodi di confine (*boundary nodes*) e ai punti di controllo umano.

Il terzo trade-off concerne il **consumo di token nei cicli di retry prolungati**. L'accumulo indiscriminato di tracce di errore e tentativi falliti all'interno dello stato globale provoca una rapida saturazione del contesto e un incremento esponenziale dei costi di inferenza. L'applicazione di tecniche di pruning dinamico e compattazione della memoria episodica ([D12c](D14c-prompt-context-engineering.md)) nei nodi di reflection assicura che il generatore riceva esclusivamente la diagnosi essenziale dell'errore senza sovraccarico informativo.

## Riferimenti Bibliografici e Risorse Tecniche

La formalizzazione dei grafi di stato ciclici e dei pattern di loop engineering si articola su autorevoli contributi della ricerca e della pratica ingegneristica open-source:

Sui pattern fondamentali di ragionamento iterativo e auto-correzione, lo studio [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) e la ricerca [Self-Refine: Iterative Refinement (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651) stabiliscono i principi teorici dei cicli a retroazione. Il repository [Loop Engineering (cobusgreyling)](https://github.com/cobusgreyling/loop-engineering) curato da [Cobus Greyling](https://github.com/cobusgreyling) (il ricercatore e architetto software esperto di agentic loops, prompt engineering e interfacce conversazionali) approfondisce le tassonomie e le best practice di implementazione dei loop agentici industriali.

Sui framework di orchestrazione e gestione dello stato, si rimanda alla documentazione ufficiale di [LangGraph](https://github.com/langchain-ai/langgraph), [AutoGen](https://microsoft.github.io/autogen/), [CrewAI](https://www.crewai.com/) e [CAMEL-AI](https://www.camel-ai.org/). Per l'integrazione di knowledge base su grafi e protocolli di contesto si consultino [Neo4j](https://neo4j.com/), [NetworkX](https://networkx.org/), [LlamaIndex](https://www.llamaindex.ai/) (il framework di orchestrazione dati per connettere fonti informative personalizzate ai Large Language Model) e lo standard [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) ideato da [Anthropic](https://www.anthropic.com/), con rimando a [D12](D14-agentic-mcp.md) per i trasporti MCP e a [D16](D18-icm-orchestrazione.md) per l'orchestrazione avanzata e la comunicazione esecutiva dei risultati.

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



### Laboratorio 1 — Motore di StateGraph Ciclico con TypedDict, Edge Condizionali e Reducer

Il primo laboratorio implementa da primi principi un motore di grafo a stati ciclico con canali di stato tipizzati, funzioni reducer per l'accumulo non distruttivo dei log e un ciclo di auto-correzione del codice sorgente basato su validazione sandbox e reflection.

- [ ] Definire la struttura `AgentState` con tipizzazione `TypedDict` e annotazione `operator.add` sul canale log.
- [ ] Implementare la classe `CyclicalStateGraph` per la registrazione di nodi, archi deterministici e router condizionali.
- [ ] Costruire i nodi operativi di generazione, esecuzione sandbox e reflection diagnostica.
- [ ] Compilare ed eseguire il grafo verificando la correzione automatica di un'eccezione di divisione per zero.

```python
"""
Laboratorio 1: Motore di StateGraph Ciclico con TypedDict, Edge Condizionali e Reducer.
Modulo: D12d - Loop engineering e graph engineering per agenti
"""

from typing import TypedDict, Annotated, Callable, Dict, Any, List, Optional, Tuple
import operator
import copy

START = "__START__"
END = "__END__"


class AgentState(TypedDict):
    task: str
    code: str
    error: Optional[str]
    iteration: int
    max_iterations: int
    execution_logs: Annotated[List[str], operator.add]
    status: str


class CyclicalStateGraph:
    """Motore di orchestrazione a grafo di stato ciclico con supporto a reducer."""
    
    def __init__(self, state_schema: type):
        self.state_schema = state_schema
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[Dict[str, Any]], str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        if name in (START, END):
            raise ValueError(f"Nome nodo riservato: {name}")
        self.nodes[name] = func

    def set_entry_point(self, node_name: str) -> None:
        if node_name not in self.nodes:
            raise ValueError(f"Nodo di ingresso {node_name} non registrato")
        self.entry_point = node_name

    def add_edge(self, source: str, target: str) -> None:
        if source != START and source not in self.nodes:
            raise ValueError(f"Nodo sorgente {source} non valido")
        if target != END and target not in self.nodes:
            raise ValueError(f"Nodo destinazione {target} non valido")
        self.edges[source] = target

    def add_conditional_edges(
        self,
        source: str,
        router: Callable[[Dict[str, Any]], str],
        path_map: Dict[str, str]
    ) -> None:
        if source not in self.nodes:
            raise ValueError(f"Nodo sorgente {source} non registrato")
        self.conditional_edges[source] = (router, path_map)

    def compile(self) -> "CompiledCyclicalGraph":
        if not self.entry_point and START not in self.edges:
            raise ValueError("Punto di ingresso non configurato")
        entry = self.entry_point or self.edges[START]
        return CompiledCyclicalGraph(self.nodes, self.edges, self.conditional_edges, entry)


class CompiledCyclicalGraph:
    """Rappresentazione compilata ed eseguibile dello StateGraph."""
    
    def __init__(
        self,
        nodes: Dict[str, Callable],
        edges: Dict[str, str],
        conditional_edges: Dict[str, Any],
        entry_point: str
    ):
        self.nodes = nodes
        self.edges = edges
        self.conditional_edges = conditional_edges
        self.entry_point = entry_point

    def _apply_reducers(self, current_state: Dict[str, Any], delta: Dict[str, Any]) -> Dict[str, Any]:
        new_state = copy.deepcopy(current_state)
        for key, value in delta.items():
            if key == "execution_logs" and key in new_state:
                new_state[key] = new_state[key] + value
            else:
                new_state[key] = value
        return new_state

    def invoke(self, initial_state: Dict[str, Any], max_steps: int = 20) -> Dict[str, Any]:
        state = copy.deepcopy(initial_state)
        current_node_name = self.entry_point
        step_count = 0

        while current_node_name != END and step_count < max_steps:
            step_count += 1
            node_func = self.nodes[current_node_name]
            delta = node_func(state)
            state = self._apply_reducers(state, delta)

            if current_node_name in self.conditional_edges:
                router, path_map = self.conditional_edges[current_node_name]
                route_decision = router(state)
                current_node_name = path_map.get(route_decision, END)
            elif current_node_name in self.edges:
                current_node_name = self.edges[current_node_name]
            else:
                current_node_name = END

        return state


def node_generator(state: AgentState) -> Dict[str, Any]:
    iteration = state["iteration"] + 1
    logs = [f"Iterazione {iteration}: Generazione codice"]
    if iteration == 1:
        code = "def calculate_ratio(a, b):\n    return a / b\nresult = calculate_ratio(10, 0)"
    else:
        code = "def calculate_ratio(a, b):\n    if b == 0:\n        return 0.0\n    return a / b\nresult = calculate_ratio(10, 0)"
        logs.append("Applicata patch correttiva per DivisionByZero")

    return {
        "code": code,
        "iteration": iteration,
        "status": "CODE_GENERATED",
        "execution_logs": logs
    }


def node_executor_and_validator(state: AgentState) -> Dict[str, Any]:
    code = state["code"]
    local_scope: Dict[str, Any] = {}
    logs = ["Validazione sandbox..."]
    try:
        exec(code, {}, local_scope)
        logs.append(f"Esecuzione riuscita. Risultato: {local_scope.get('result')}")
        return {"error": None, "status": "SUCCESS", "execution_logs": logs}
    except Exception as exc:
        err = f"{type(exc).__name__}: {str(exc)}"
        logs.append(f"Errore riscontrato: {err}")
        return {"error": err, "status": "VALIDATION_ERROR", "execution_logs": logs}


def node_reflection(state: AgentState) -> Dict[str, Any]:
    return {"status": "REFLECTION_COMPLETED", "execution_logs": [f"Reflection attiva su errore: {state['error']}"]}


def router_validation(state: AgentState) -> str:
    if state["status"] == "SUCCESS":
        return "success"
    if state["iteration"] >= state["max_iterations"]:
        return "max_retries_reached"
    return "retry"


if __name__ == "__main__":
    builder = CyclicalStateGraph(AgentState)
    builder.add_node("generator", node_generator)
    builder.add_node("validator", node_executor_and_validator)
    builder.add_node("reflection", node_reflection)

    builder.set_entry_point("generator")
    builder.add_edge("generator", "validator")
    builder.add_conditional_edges(
        "validator",
        router_validation,
        {"success": END, "retry": "reflection", "max_retries_reached": END}
    )
    builder.add_edge("reflection", "generator")

    app = builder.compile()
    initial: AgentState = {
        "task": "Calcolo ratio sicuro con divisore zero",
        "code": "",
        "error": None,
        "iteration": 0,
        "max_iterations": 3,
        "execution_logs": ["Inizializzazione sessione"],
        "status": "INITIALIZED"
    }

    final_state = app.invoke(initial)
    assert final_state["status"] == "SUCCESS"
    assert "if b == 0:" in final_state["code"]
    print("Test Laboratorio 1 completato con successo.")
```

### Laboratorio 2 — Checkpointed StateGraph con Persistenza SQLite e Time-Travel

Il secondo laboratorio costruisce un checkpointer relazionale su [SQLite](https://www.sqlite.org/) che registra ogni transizione di stato atomica, abilitando l'ispezione della genealogia dei checkpoint e il ripristino (*rollback*) con modifica dei parametri.

- [ ] Implementare la classe `SqliteCheckpointer` con gestione della tabella relazionale dei checkpoint.
- [ ] Costruire `CheckpointedStateGraph` per l'aggiornamento incrementale dello snapshot.
- [ ] Eseguire una prima sessione con errore forzato registrando la cronologia nel database.
- [ ] Eseguire il rollback a un checkpoint precedente modificando i parametri e completando con successo.

```python
"""
Laboratorio 2: StateGraph con Persistenza SQLite, Time-Travel e Rollback.
Modulo: D12d - Loop engineering e graph engineering per agenti
"""

import sqlite3
import json
import uuid
import datetime
import copy
from typing import Dict, Any, List, Optional, Tuple, Callable

START = "__START__"
END = "__END__"


class SqliteCheckpointer:
    """Gestore di persistenza per lo stato del grafo basato su SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    thread_id TEXT NOT NULL,
                    parent_checkpoint_id TEXT,
                    node_name TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_thread ON checkpoints(thread_id)")

    def put(self, thread_id: str, node_name: str, state: Dict[str, Any], parent_id: Optional[str] = None) -> str:
        checkpoint_id = f"chk_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.datetime.utcnow().isoformat()
        state_json = json.dumps(state)
        with self.conn:
            self.conn.execute("""
                INSERT INTO checkpoints (checkpoint_id, thread_id, parent_checkpoint_id, node_name, state_json, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (checkpoint_id, thread_id, parent_id, node_name, state_json, timestamp))
        return checkpoint_id

    def get(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT state_json FROM checkpoints WHERE checkpoint_id = ?", (checkpoint_id,))
        row = cur.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def list_history(self, thread_id: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT checkpoint_id, parent_checkpoint_id, node_name, timestamp, state_json
            FROM checkpoints WHERE thread_id = ? ORDER BY timestamp ASC
        """, (thread_id,))
        rows = cur.fetchall()
        return [
            {
                "checkpoint_id": r[0],
                "parent_id": r[1],
                "node_name": r[2],
                "timestamp": r[3],
                "state": json.loads(r[4])
            }
            for r in rows
        ]


class CheckpointedStateGraph:
    """Grafo di stato con persistenza integrata e supporto al time-travel."""

    def __init__(self, checkpointer: SqliteCheckpointer):
        self.checkpointer = checkpointer
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable, Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable) -> None:
        self.nodes[name] = func

    def set_entry_point(self, name: str) -> None:
        self.entry_point = name

    def add_edge(self, source: str, target: str) -> None:
        self.edges[source] = target

    def add_conditional_edges(self, source: str, router: Callable, path_map: Dict[str, str]) -> None:
        self.conditional_edges[source] = (router, path_map)

    def run(
        self,
        thread_id: str,
        initial_state: Optional[Dict[str, Any]] = None,
        from_checkpoint_id: Optional[str] = None,
        resume_from_node: Optional[str] = None
    ) -> Dict[str, Any]:
        parent_id = None
        if from_checkpoint_id:
            state = self.checkpointer.get(from_checkpoint_id)
            if not state:
                raise ValueError(f"Checkpoint {from_checkpoint_id} non trovato.")
            parent_id = from_checkpoint_id
            current_node = resume_from_node or self.entry_point
        else:
            state = copy.deepcopy(initial_state or {})
            current_node = self.entry_point
            parent_id = self.checkpointer.put(thread_id, START, state, parent_id=None)

        while current_node != END:
            node_fn = self.nodes[current_node]
            delta = node_fn(state)
            state.update(delta)
            parent_id = self.checkpointer.put(thread_id, current_node, state, parent_id=parent_id)

            if current_node in self.conditional_edges:
                router, path_map = self.conditional_edges[current_node]
                route = router(state)
                current_node = path_map.get(route, END)
            elif current_node in self.edges:
                current_node = self.edges[current_node]
            else:
                current_node = END

        return state


def step_query_expansion(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("target_entity", "")
    return {"expanded_queries": [f"{query} subdomains"], "step": "EXPANDED"}


def step_data_collection(state: Dict[str, Any]) -> Dict[str, Any]:
    if state.get("force_failure", False):
        return {"error": "Rate Limit 429", "step": "FAILED"}
    return {"records": [{"domain": "alpha.target.com"}], "error": None, "step": "COLLECTED"}


def step_synthesis(state: Dict[str, Any]) -> Dict[str, Any]:
    return {"final_report": f"Analizzati {len(state.get('records', []))} record.", "step": "COMPLETED"}


def router_status(state: Dict[str, Any]) -> str:
    return "error" if state.get("error") else "ok"


if __name__ == "__main__":
    checkpointer = SqliteCheckpointer(":memory:")
    graph = CheckpointedStateGraph(checkpointer)

    graph.add_node("query_expansion", step_query_expansion)
    graph.add_node("data_collection", step_data_collection)
    graph.add_node("synthesis", step_synthesis)

    graph.set_entry_point("query_expansion")
    graph.add_edge("query_expansion", "data_collection")
    graph.add_conditional_edges("data_collection", router_status, {"ok": "synthesis", "error": END})
    graph.add_edge("synthesis", END)

    thread = "osint_thread_01"
    res_1 = graph.run(thread_id=thread, initial_state={"target_entity": "TargetCorp", "force_failure": True})
    assert res_1.get("step") == "FAILED"

    history = checkpointer.list_history(thread)
    valid_cp = [h for h in history if h["node_name"] == "query_expansion"][0]["checkpoint_id"]

    state_mod = checkpointer.get(valid_cp)
    state_mod["force_failure"] = False
    new_cp = checkpointer.put(thread, "query_fixed", state_mod, parent_id=valid_cp)

    res_2 = graph.run(thread_id=thread, from_checkpoint_id=new_cp, resume_from_node="data_collection")
    assert res_2.get("step") == "COMPLETED"
    print("Test Laboratorio 2 completato con successo.")
```

### Laboratorio 3 — Workflow Multi-Agente Supervisor con Routing Dinamico

Il terzo laboratorio realizza un'architettura multi-agente centralizzata in cui un agente Supervisore coordina dinamicamente specialisti di intelligence (OSINT, Data Analyst, Security Auditor) aggregando i risultati in un consensus report finale.

- [ ] Definire lo schema `MultiAgentState` con liste condivise per i risultati specialistici.
- [ ] Implementare il nodo `node_supervisor` per l'ispezione dello stato e la pianificazione dei turni.
- [ ] Costruire i nodi worker specializzati per l'acquisizione delle evidenze.
- [ ] Eseguire l'orchestrazione con sintesi del report conclusivo.

```python
"""
Laboratorio 3: Workflow Multi-Agente Supervisor con Routing Dinamico e Sintesi di Consenso.
Modulo: D12d - Loop engineering e graph engineering per agenti
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
import copy

START = "__START__"
END = "__END__"


class MultiAgentState(TypedDict):
    objective: str
    active_worker: Optional[str]
    tasks_completed: Annotated[List[str], operator.add]
    osint_findings: Annotated[List[str], operator.add]
    analysis_findings: Annotated[List[str], operator.add]
    security_findings: Annotated[List[str], operator.add]
    supervisor_notes: List[str]
    final_consensus: Optional[str]


def node_supervisor(state: MultiAgentState) -> Dict[str, Any]:
    completed = set(state.get("tasks_completed", []))
    notes = state.get("supervisor_notes", [])
    
    if "OSINT_COLLECTION" not in completed:
        next_worker = "osint_worker"
        decision = "Delegato task di raccolta OSINT."
    elif "DATA_ANALYSIS" not in completed:
        next_worker = "analyst_worker"
        decision = "Delegato task di analisi dati."
    elif "SECURITY_AUDIT" not in completed:
        next_worker = "security_worker"
        decision = "Delegato task di audit sicurezza."
    else:
        next_worker = "consensus_synthesizer"
        decision = "Sintesi finale avviata."

    return {
        "active_worker": next_worker,
        "supervisor_notes": notes + [decision]
    }


def node_osint_worker(state: MultiAgentState) -> Dict[str, Any]:
    return {"osint_findings": ["3 sottodomini rilevati", "Bucket S3 esposto"], "tasks_completed": ["OSINT_COLLECTION"]}


def node_analyst_worker(state: MultiAgentState) -> Dict[str, Any]:
    return {"analysis_findings": ["Pattern temporale correlato a leak noto"], "tasks_completed": ["DATA_ANALYSIS"]}


def node_security_worker(state: MultiAgentState) -> Dict[str, Any]:
    return {"security_findings": ["Rischio Data Leakage elevato (CVSS 8.2)"], "tasks_completed": ["SECURITY_AUDIT"]}


def node_consensus_synthesizer(state: MultiAgentState) -> Dict[str, Any]:
    report = (
        f"Consensus Report per: {state['objective']}\n"
        f"Evidenze OSINT: {len(state.get('osint_findings', []))}\n"
        f"Analisi: {len(state.get('analysis_findings', []))}\n"
        f"Sicurezza: {len(state.get('security_findings', []))}\n"
        f"Valutazione: Intervento raccomandato."
    )
    return {"final_consensus": report, "active_worker": "COMPLETE"}


if __name__ == "__main__":
    nodes = {
        "supervisor": node_supervisor,
        "osint_worker": node_osint_worker,
        "analyst_worker": node_analyst_worker,
        "security_worker": node_security_worker,
        "consensus_synthesizer": node_consensus_synthesizer
    }

    state: MultiAgentState = {
        "objective": "Audit perimetro cloud",
        "active_worker": None,
        "tasks_completed": [],
        "osint_findings": [],
        "analysis_findings": [],
        "security_findings": [],
        "supervisor_notes": [],
        "final_consensus": None
    }

    current = "supervisor"
    steps = 0
    while current != END and steps < 10:
        steps += 1
        delta = nodes[current](state)
        for k, v in delta.items():
            if k in ("tasks_completed", "osint_findings", "analysis_findings", "security_findings") and k in state:
                state[k] = state[k] + v
            else:
                state[k] = v

        if current == "supervisor":
            current = state.get("active_worker", END)
        elif current == "consensus_synthesizer":
            current = END
        else:
            current = "supervisor"

    assert state["final_consensus"] is not None
    assert "Intervento raccomandato" in state["final_consensus"]
    print("Test Laboratorio 3 completato con successo.")
```

### Laboratorio 4 — Grafo Agentico con Breakpoint Human-in-the-Loop e Override Manuale

Il quarto laboratorio implementa un grafo agentico interrompibile dotato di breakpoint di sicurezza prima di azioni critiche, consentendo la sospensione asincrona, l'ispezione dello stato e l'iniezione di modifiche manuali da parte dell'operatore.

- [ ] Implementare la classe `HumanInTheLoopGraph` con gestione dei breakpoint `interrupt_before`.
- [ ] Definire nodi per la pianificazione, l'acquisizione ad alto impatto e la reportistica.
- [ ] Eseguire il grafo fino al blocco autorizzativo verificando lo stato di sospensione.
- [ ] Applicare un override manuale dei parametri e riprendere l'esecuzione fino al completamento.

```python
"""
Laboratorio 4: Grafo Agentico Interrompibile con Human-in-the-Loop.
Modulo: D12d - Loop engineering e graph engineering per agenti
"""

from typing import Dict, Any, List, Optional, Callable
import copy

START = "__START__"
END = "__END__"


class HumanInTheLoopGraph:
    """Motore di grafo con supporto nativo a breakpoint e ripresa asincrona."""

    def __init__(self, interrupt_before_nodes: List[str]):
        self.interrupt_before = set(interrupt_before_nodes)
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}
        self.entry_point: Optional[str] = None
        self.suspended_states: Dict[str, Dict[str, Any]] = {}

    def add_node(self, name: str, func: Callable) -> None:
        self.nodes[name] = func

    def set_entry_point(self, name: str) -> None:
        self.entry_point = name

    def add_edge(self, source: str, target: str) -> None:
        self.edges[source] = target

    def invoke(self, thread_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        current_state = copy.deepcopy(state)
        current_node = self.entry_point

        while current_node != END:
            if current_node in self.interrupt_before:
                current_state["__suspended_at_node__"] = current_node
                current_state["__execution_status__"] = "PAUSED_AWAITING_APPROVAL"
                self.suspended_states[thread_id] = current_state
                return current_state

            node_fn = self.nodes[current_node]
            delta = node_fn(current_state)
            current_state.update(delta)
            current_node = self.edges.get(current_node, END)

        current_state["__execution_status__"] = "COMPLETED"
        return current_state

    def resume(self, thread_id: str, state_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if thread_id not in self.suspended_states:
            raise ValueError(f"Nessuna sessione sospesa per '{thread_id}'")

        state = self.suspended_states.pop(thread_id)
        current_node = state.pop("__suspended_at_node__")

        if state_override:
            for k, v in state_override.items():
                state[k] = v

        while current_node != END:
            node_fn = self.nodes[current_node]
            delta = node_fn(state)
            state.update(delta)
            current_node = self.edges.get(current_node, END)

        state["__execution_status__"] = "COMPLETED"
        return state


def node_plan_investigation(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "PLAN_READY",
        "scan_intensity": "HIGH_AGGRESSIVE",
        "proposed_actions": ["Port scan full range"]
    }


def node_critical_execution(state: Dict[str, Any]) -> Dict[str, Any]:
    intensity = state.get("scan_intensity", "LOW")
    return {"status": "ACQUISITION_SUCCESS", "audit_logs": [f"Scansione eseguita con livello: {intensity}"]}


def node_final_reporting(state: Dict[str, Any]) -> Dict[str, Any]:
    return {"final_summary": f"Report validato. Livello applicato: {state.get('scan_intensity')}."}


if __name__ == "__main__":
    hil_app = HumanInTheLoopGraph(interrupt_before_nodes=["critical_execution"])
    hil_app.add_node("plan_investigation", node_plan_investigation)
    hil_app.add_node("critical_execution", node_critical_execution)
    hil_app.add_node("final_reporting", node_final_reporting)

    hil_app.set_entry_point("plan_investigation")
    hil_app.add_edge("plan_investigation", "critical_execution")
    hil_app.add_edge("critical_execution", "final_reporting")

    thread_id = "hil_thread_99"
    paused_state = hil_app.invoke(thread_id, {"target_ip": "198.51.100.25"})
    assert paused_state["__execution_status__"] == "PAUSED_AWAITING_APPROVAL"

    override = {"scan_intensity": "PASSIVE_STEALTH", "operator_id": "Analista_01"}
    final_output = hil_app.resume(thread_id, state_override=override)

    assert final_output["__execution_status__"] == "COMPLETED"
    assert "PASSIVE_STEALTH" in final_output["final_summary"]
    print("Test Laboratorio 4 completato con successo.")
```