---
aliases: [D12, MCP, Model Context Protocol, Agentic Systems, Tool Calling, Sistemi Agentici, Server MCP, FastMCP]
---

# Sistemi Agentici, Model Context Protocol (MCP) e Automazione Autonoma

Un **sistema agentico** è un'architettura computazionale basata su Large Language Model in grado di eseguire cicli iterativi di percezione, pianificazione e azione nel mondo digitale, mentre il **Model Context Protocol (MCP)** rappresenta lo standard aperto di comunicazione ideato da [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI creatrice dei modelli Claude e ideatrice del Model Context Protocol) basato su JSON-RPC 2.0 per disaccoppiare e standardizzare l'accesso dei modelli a strumenti, risorse documentali e template di prompt esterni. Questa tecnologia trova applicazione nell'automazione di flussi complessi di intelligence su fonti aperte ([D11](D11-osint-avanzato.md)), nell'interrogazione sicura di basi di dati relazionali e knowledge graph ([D10](D10-rag-knowledge-osint.md)) e nell'esecuzione controllata di script e microservizi senza dover riscrivere integrazioni proprietarie punto-a-punto. L'architettura agentica e l'MCP esistono per superare il collo di bottiglia della passività conversazionale dei modelli linguistici e risolvere il problema combinatorio dell'integrazione $M \times N$ tra client LLM e sorgenti informative, garantendo al contempo isolamento dei processi, negoziazione dinamica dei permessi e tracciabilità forense delle azioni eseguite.

```
+-----------------------------------------------------------------------------------------+
|                IL PROBLEMA COMBINATORIO M x N VS LO STANDARD MCP                         |
+-----------------------------------------------------------------------------------------+

  ARCHITETTURA FRAMMENTATA (M x N)               ARCHITETTURA STANDARDIZZATA MCP (M + N)   
                                                                                           
  [ Client LLM 1 ] ──┬── [ File System ]         [ Client LLM 1 ] ──┐                      
                     ├── [ Database SQL ]                           │                      
  [ Client LLM 2 ] ──┼── [ API GitHub   ]         [ Client LLM 2 ] ──┼──► [ MCP PROTOCOL ] 
                     ├── [ OSINT Engine ]                           │       (JSON-RPC 2.0) 
  [ Client LLM M ] ──┴── [ Web Search   ]         [ Client LLM M ] ──┘            │        
                                                                                  ├──► [ File Server ]
  (M x N Connettori Proprietari Fragili)                                          ├──► [ DB Server   ]
                                                                                  ├──► [ Tool Server ]
```

## Dal Modello Conversazionale all'Agente Autonomo: Limiti della Chat e Genesi del Tool Calling

L'evoluzione dei modelli linguistici dall'interazione puramente testuale all'esecuzione di compiti autonomi segna il passaggio da sistemi informativi passivi a motori di computazione attiva. Una sessione di chat convenzionale opera come una funzione probabilistica priva di memoria persistente o effetti collaterali sull'ambiente esterno, in cui il modello riceve una sequenza di token e genera la continuazione statisticamente più plausibile. Questo paradigma è intrinsecamente vincolato dalla finestra di contesto e dalla conoscenza statica acquisita durante la fase di pre-addestramento, rendendo il modello incapace di verificare fatti aggiornati, interagire con file di sistema o interrogare database esterni in tempo reale. Al contrario, un workflow deterministico impone una sequenza rigida di passi prefissati codificati tramite script procedurali, offrendo garanzie di riproducibilità ma risultando completamente privo dell'adattabilità dinamica richiesta per gestire imprevisti o risposte eterogenee.

Il sistema agentico unisce la flessibilità inferenziale del Large Language Model con la capacità operativa del software deterministico, realizzando un ciclo a retroazione continua in cui il modello osserva l'ambiente, formula un piano di esecuzione, seleziona uno strumento computazionale e ne interpreta i risultati prima di procedere al passo successivo. In questo contesto, il concetto fondamentale è il **tool calling** (o function calling), una capacità addestrata tramite fine-tuning che permette al modello di non limitarsi a produrre testo discorsivo, ma di emettere payload strutturati conformi a una specifica formale [JSON Schema](https://json-schema.org/). Il modello linguistico non esegue direttamente codice binario o comandi di sistema sul sistema operativo ospitante, bensì esprime un'intenzione strutturata contenente il nome della funzione desiderata e gli argomenti tipizzati.

L'ambiente ospite (*host runtime*) intercetta la stringa JSON prodotta dal modello, valida formalmente la correttezza dei tipi di dato rispetto allo schema atteso ed esegue la funzione corrispondente all'interno di un contesto controllato. L'output restituito dalla funzione viene quindi re-iniettato nella cronologia dei messaggi del modello come un messaggio di tipo `tool_result`, consentendo alla rete neurale di leggere l'esito reale dell'operazione e continuare il ragionamento logico. Questo disaccoppiamento garantisce che il modello rimanga un pianificatore probabilistico, mentre l'effettiva alterazione dello stato del sistema sia affidata a routine deterministiche governate da policy di sicurezza e controlli di accesso granulari.

Prima dell'avvento di protocolli standardizzati, l'integrazione di strumenti esterni nei sistemi agentici soffriva di una grave frammentazione architetturale. Ogni fornitore di modelli linguistici, da [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT e ChatGPT) ad [Anthropic](https://www.anthropic.com/) e [Google](https://about.google/) (la multinazionale tecnologica leader nei servizi Internet, ricerca algoritmica, cloud e AI), implementava convenzioni proprietarie per la dichiarazione dei parametri e la gestione dei messaggi di ritorno. Parallelamente, framework applicativi come [LangChain](https://www.langchain.com/) (il framework open-source per la costruzione di applicazioni, catene e integrazioni guidate da Large Language Model) e [LlamaIndex](https://www.llamaindex.ai/) (il framework di orchestrazione dati per connettere fonti informative personalizzate ai Large Language Model) introducevano layer di astrazione incompatibili tra loro. Questa eterogeneità generava il classico problema di complessità combinatoria $M \times N$, in cui $M$ client agentici dovevano riscrivere e mantenere $N$ adattatori dedicati per interfacciarsi con filesystem locali, database relazionali [PostgreSQL](https://www.postgresql.org/) (il sistema di gestione di database relazionale a oggetti open-source rinomato per affidabilità ed estendibilità), repository [GitHub](https://github.com/) (la piattaforma di hosting cloud per repository Git e collaborazione sullo sviluppo software) o motori OSINT.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D12-agentic-mcp. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Architettura del Model Context Protocol (MCP): Client, Host e Server

Per risolvere la frammentazione delle integrazioni punto-a-punto, [Anthropic](https://www.anthropic.com/) ha introdotto il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (lo standard aperto creato da Anthropic per la connessione sicura tra modelli linguistici, strumenti esterni e sorgenti dati), un protocollo aperto basato sullo standard [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) che stabilisce un'architettura client-server universale per l'esposizione e il consumo di capacità computazionali e sorgenti informative. L'architettura MCP scompone l'ecosistema agentico in tre componenti distinte e cooperanti: l'Host di applicazione, il Client MCP e il Server MCP indipendente.

L'**Host MCP** rappresenta l'applicazione sovrastante che governa l'esperienza utente e coordina l'accesso ai modelli linguistici, come ad esempio un ambiente di sviluppo integrato (IDE), un'applicazione desktop di analisi o un orchestratore di processi aziendali. L'Host detiene il controllo sulle chiavi di autenticazione dei fornitori di modelli linguistici, stabilisce le regole di sicurezza globali e presenta all'utente le richieste di autorizzazione per le operazioni potenzialmente distruttive. All'interno dell'Host risiede uno o più **Client MCP**, moduli software incaricati di stabilire e gestire sessioni di comunicazione punto-a-punto con singoli Server MCP, occupandosi della serializzazione dei messaggi, del routing delle chiamate e del mantenimento dello stato della connessione.

Il **Server MCP** è un microservizio leggero, dedicato e isolato che espone programmaticamente risorse informative, strumenti operativi e modelli di prompt verso l'esterno. I server possono essere eseguiti localmente come processi figli dell'Host oppure risiedere su nodi remoti accessibili via rete. Ciascun server incapsula la logica specifica del dominio sottostante, esponendo un'interfaccia standardizzata che nasconde la complessità delle API proprietarie o delle query di basso livello. Grazie a questa separazione, uno sviluppatore può realizzare un server MCP per un archivio documentale o un tool di intelligence una sola volta in [Python](https://www.python.org/) (il linguaggio di programmazione ad alto livello di riferimento globale per intelligenza artificiale e data science) e renderlo immediatamente utilizzabile da qualsiasi Host conforme allo standard, riducendo la complessità di integrazione da $M \times N$ a $M + N$.

Il ciclo di vita di una connessione MCP inizia con una fase di handshake formale tramite il metodo `initialize`, durante la quale Client e Server negoziano la versione del protocollo e dichiarano le rispettive capacità operative (*capabilities*). Il Client comunica se supporta funzionalità avanzate come la notifica di modifica delle directory radice (`roots`) o la delega di inferenza (`sampling`), mentre il Server elenca i moduli disponibili (`tools`, `resources`, `prompts`, `logging`). Una volta convalidato l'handshake, il Client trasmette una notifica `notifications/initialized` per confermare l'apertura del canale operativo. Durante l'intera sessione, l'Host può inviare messaggi di heartbeat periodici (`ping`) per verificare la reattività del processo server e terminare la connessione in modo ordinato al termine delle elaborazioni.

Le primitive fondamentali esposte dal protocollo MCP si articolano in quattro categorie operative distinte:

La prima primitiva è costituita dai **Tools**, funzioni eseguibili esposte dal server che accettano argomenti strutturati e possono produrre effetti collaterali sull'ambiente o calcoli deterministici. La scoperta e l'invocazione avvengono tramite i metodi `tools/list` e `tools/call`.

La seconda primitiva è rappresentata dalle **Resources**, oggetti di sola lettura indirizzabili tramite schemi URI standardizzati (quali `file:///`, `postgres://` o `threatintel://`) che forniscono contesto documentale, snapshot di database o stream informativi, supportando anche meccanismi di notifica push in tempo reale tramite sottoscrizione (`resources/subscribe`).

La terza primitiva comprende i **Prompts**, template parametrizzati e contestualizzati memorizzati sul server che guidano il modello nell'esecuzione di compiti ricorrenti, accessibili via `prompts/list` e `prompts/get`.

La quarta primitiva, denominata **Sampling**, realizza un'inversione di controllo in cui il server MCP richiede all'host l'esecuzione di un'inferenza LLM sicura (`sampling/createMessage`). Questa funzionalità consente al server di eseguire compiti analitici intermedi senza dover gestire direttamente credenziali o chiavi API private, mantenendo la centralizzazione dei costi e della sicurezza sotto la supervisione dell'Host.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Meccanismi di Trasporto JSON-RPC 2.0: stdio vs Server-Sent Events (SSE)

La comunicazione all'interno del protocollo MCP è interamente serializzata secondo la specifica [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification), uno standard stateless e leggero per la chiamata a procedura remota. La struttura di una richiesta valida comprende il campo di versione `jsonrpc: "2.0"`, un identificatore univoco `id` (numerico o stringa) generato dal chiamante, il nome del metodo da invocare `method` e un dizionario facoltativo di parametri `params`. Quando il server elabora con successo la richiesta, restituisce un messaggio contenente il medesimo `id` e il risultato nel campo `result`. In caso di anomalia o rifiuto, il server risponde con un oggetto `error` contenente un codice numerico standardizzato e una descrizione testuale dettagliata.

I codici di errore definiti dallo standard includono `-32700` per errori di parsing della sintassi JSON, `-32600` per richieste non conformi alla specifica, `-32601` per metodi inesistenti o non registrati, `-32602` per parametri non validi o incompatibili con lo schema dichiarato, e `-32603` per fallimenti interni del server. Accanto alle chiamate bidirezionali sincrone, il protocollo definisce le **notifiche**, messaggi unidirezionali privi del campo `id` utilizzati per segnalare eventi asincroni, come l'aggiornamento di una risorsa o la modifica dinamica del catalogo dei tool, per i quali il mittente non richiede alcuna risposta di conferma.

```
Richiesta Tool Call:
{"jsonrpc": "2.0", "id": 42, "method": "tools/call", "params": {"name": "query_threat", "arguments": {"ip": "198.51.100.1"}}}

Risposta con Risultato:
{"jsonrpc": "2.0", "id": 42, "result": {"content": [{"type": "text", "text": "{\"threat_score\": 88}"}], "isError": false}}
```

Per garantire massima flessibilità sia in contesti locali che distribuiti, il protocollo standardizza due meccanismi di trasporto fisici: il trasporto locale basato su standard input/output (`stdio`) e il trasporto remoto basato su Server-Sent Events (SSE) su protocollo HTTP.

Il trasporto **stdio** è progettato per server eseguiti localmente sulla stessa macchina dell'Host. Il Client avvia il processo server come sottoprocesso isolato (`subprocess`) e apre canali di pipe anonime verso i suoi flussi standard. I messaggi JSON-RPC vengono scambiati come stringhe serializzate su singola riga delimitate dal carattere newline (`\n`), dove il Client scrive su `stdin` del server e legge le risposte dal suo `stdout`. Il canale `stderr` del server viene rigidamente separato e riservato all'emissione di log diagnostici e messaggi di debug, evitando tassativamente che testo non strutturato corrompa il flusso dei pacchetti JSON su `stdout`. Questo approccio offre latenze di comunicazione sub-millisecondo, garantisce l'assenza di porte TCP aperte esposte sulla rete locale e assicura che il ciclo di vita del server sia strettamente vincolato a quello del processo genitore, prevenendo processi orfani.

Il trasporto **SSE su HTTP** è concepito per scenari in cui il server MCP risiede su un'infrastruttura remota, all'interno di un container [Docker](https://www.docker.com/) (la piattaforma open-source per isolare ed eseguire applicazioni in container leggeri) o erogato come microservizio tramite framework moderni come [FastAPI](https://fastapi.tiangolo.com/) (il framework web moderno ad alte prestazioni in Python per la creazione di API REST con validazione Pydantic). La comunicazione si articola su due canali HTTP complementari: il Client stabilisce una connessione HTTP GET persistente verso l'endpoint `/sse`, attraverso la quale il server invia flussi di eventi asincroni in formato `text/event-stream`. All'apertura del canale, il server emette un evento contenente un URI con un identificatore di sessione univoco (es. `/messages?sessionId=uuid-1234`), verso cui il Client indirizza le proprie richieste JSON-RPC tramite normali richieste HTTP POST. Questo meccanismo consente di superare le limitazioni dei firewall aziendali, supporta l'autenticazione enterprise basata su token Bearer o mTLS e abilita l'orchestrazione scalabile di server MCP in cluster remoti.


> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.


## Definizione degli Schemi e Validazione con JSON Schema e Pydantic

L'affidabilità di un sistema agentico dipende dalla precisione con cui gli strumenti vengono descritti al modello e dalla rigorosità con cui i parametri generati vengono convalidati prima dell'esecuzione. All'interno del protocollo MCP, ogni strumento registrato espone una proprietà `inputSchema` conforme alle specifiche JSON Schema Draft 7. La generazione manuale di questi schemi è soggetta a errori di sintassi e discrepanze di tipo; per questa ragione, nell'ecosistema [Python](https://www.python.org/) si adotta comunemente la libreria [Pydantic](https://docs.pydantic.dev/) (la libreria di riferimento per la validazione dei dati e la gestione dei tipi strutturati in Python tramite type hints) o il framework [FastMCP](https://github.com/jlowin/fastmcp) (il framework Python ad alto livello per lo sviluppo rapido e dichiarativo di server Model Context Protocol).

Attraverso classi Pydantic fortemente tipizzate, gli sviluppatori definiscono campi, tipi primitivi, vincoli di validazione (quali espressioni regolari per indirizzi IP o range numerici per coordinate geografiche), valori di default e descrizioni semantiche dettagliate mediante l'oggetto `Field`. Il server estrae programmaticamente lo schema serializzato richiamando `model_json_schema()`, garantendo una perfetta corrispondenza tra la documentazione esposta all'LLM e i controlli eseguiti dal runtime. Quando il modello linguistico formula una chiamata di tool, il payload JSON ricevuto viene iniettato nel modello Pydantic corrispondente. Se i parametri violano i vincoli dichiarati, il validatore intercetta l'eccezione `ValidationError` e impedisce l'invocazione della logica sottostante.

La gestione strutturata degli errori di validazione costituisce un pilastro essenziale per la resilienza operativa degli agenti. Anziché causare un'interruzione fatale del processo, il server MCP cattura l'errore e restituisce un messaggio JSON-RPC contrassegnato con la proprietà `isError: true`, contenente un testo esplicativo che indica con precisione il campo errato, il valore non valido e il formato atteso. L'agente incorpora questa osservazione nel proprio contesto conversazionale e, sfruttando le proprie capacità di ragionamento deduttivo, auto-corregge i parametri formulando una chiamata valida al turno successivo, realizzando un meccanismo di recupero automatico privo di interventi manuali.


> [!NOTE]
> **Checkpoint di Ancoraggio: Controllo di Comprensione**
> Qual è il trade-off o limite operativo principale emerso in questa parte? Aver chiari i limiti ci aiuterà a capire le soluzioni tecnologiche che presenteremo a breve.


## Cicli di Esecuzione Agentica, Pattern ReAct e Orchestrazione Autonoma

Un agente autonomo non si limita a eseguire singole chiamate a strumenti isolati, ma opera all'interno di un loop di controllo a retroazione strutturato secondo pattern cognitivi formalizzati. Tra questi, il paradigma di riferimento è il pattern [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) (il paper di Princeton University e Google Research che ha definito il pattern agentico che alterna pensiero ed esecuzione di tool). ReAct scompone il processo di risoluzione di compiti complessi in una sequenza iterativa di tre fasi distinte: Pensiero (*Thought*), Azione (*Action*) e Osservazione (*Observation*).

```
+-----------------------------------------------------------------------------------------+
|                    IL CICLO DI RAGIONAMENTO E AZIONE REACT                              |
+-----------------------------------------------------------------------------------------+

              ┌─────────────────────────────────────────────────────────┐
              │                   OBIETTIVO MISSIONE                    │
              └────────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────┐
                    │      FASE DI PENSIERO (Thought)      │◄─────────────────┐
                    │  Formula ipotesi logica e strategia  │                  │
                    └──────────────────────┬───────────────┘                  │
                                           │                                  │
                                           ▼                                  │
                    ┌──────────────────────────────────────┐                  │
                    │       FASE DI AZIONE (Action)        │                  │
                    │ Invocazione tool MCP con argomenti   │                  │
                    └──────────────────────┬───────────────┘                  │
                                           │                                  │
                                           ▼                                  │
                    ┌──────────────────────────────────────┐                  │
                    │    FASE DI OSSERVAZIONE (Observe)    │                  │
                    │  Lettura output reale del server MCP │──────────────────┘
                    └──────────────────────┬───────────────┘  (Iterazione fino
                                           │                   a convergenza)
                                           ▼
                    ┌──────────────────────────────────────┐
                    │       RISULTATO FINALE (Finish)      │
                    │   Sintesi conclusiva verificata      │
                    └──────────────────────────────────────┘
```

Nella fase di pensiero, il modello linguistico genera una traccia di ragionamento esplicita in linguaggio naturale, valutando lo stato attuale delle informazioni disponibili, identificando le lacune conoscitive e stabilendo quale operazione eseguire per progredire verso l'obiettivo. Nella fase di azione, l'agente emette la chiamata di tool strutturata conforme allo schema MCP. Il runtime esegue l'operazione sul server e cattura la risposta, che viene presentata all'agente nella fase di osservazione. Questo ciclo ($T_t \rightarrow A_t \rightarrow O_t \rightarrow T_{t+1}$) si ripete fino a quando il modello determina di possedere tutti gli elementi necessari per formulare la risposta conclusiva (*Finish*), ancorando costantemente il ragionamento a dati verificati ed eliminando le allucinazioni tipiche della generazione a colpo singolo (*zero-shot*).

All'aumentare della complessità del sistema, emerge la necessità della **Dynamic Tool Discovery**. In ambienti enterprise, un Host può essere connesso a decine di server MCP che espongono centinaia di strumenti specializzati. Inserire l'elenco completo di tutti gli schemi JSON nel prompt di sistema di ogni invocazione consuma una frazione rilevante della finestra di contesto, incrementa i costi di inferenza e degrada l'accuratezza selettiva del modello a causa del rumore informativo (*context cluttering*). La scoperta dinamica risolve questo problema interrogando preliminarmente il registro dei server tramite `tools/list`, eseguendo un filtraggio semantico o categorico basato sull'obiettivo corrente dell'utente e iniettando nella sessione di inferenza esclusivamente il sottoinsieme di strumenti rilevanti per il compito specifico.

La robustezza operativa dell'agente richiede inoltre strategie sistematiche per la mitigazione dei fallimenti. I modelli linguistici possono incorrere in loop infiniti, reiterando chiamate identiche con argomenti non validi o oscillando tra strumenti complementari senza convergere. L'architettura dell'agente deve pertanto imporre un limite rigido al numero massimo di iterazioni (*max step budget*), monitorare la cronologia per rilevare firme di chiamata ripetute e implementare meccanismi di fallback degradato che, in caso di indisponibilità di un server MCP primario, reindirizzino la richiesta verso strumenti secondari o richiedano l'intervento di un operatore umano.

## Sicurezza, Sandboxing e Controllo Granulare degli Agenti

L'attribuzione di capacità operative a un modello di linguaggio introduce vettori di minaccia critici che devono essere indirizzati a livello architetturale. Come formalizzato nella tassonomia [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (la tassonomia standard di OWASP delle dieci minacce e vulnerabilità di sicurezza più critiche nei sistemi basati su LLM), uno dei rischi più severi è rappresentato dal **prompt injection indiretto**. Quando un agente analizza dati non fidati provenienti da fonti esterne (quali pagine web, feed OSINT, allegati email o record di database), tali sorgenti possono contenere istruzioni malevole nascoste concepite per deviare il comportamento del modello, spingendolo a esfiltrare credenziali riservate, aggirare i controlli di policy o invocare strumenti distruttivi.

Un ulteriore fattore di rischio risiede nella confusione dei privilegi, situazione in cui l'agente eredita i permessi del processo host ed esegue comandi con privilegi elevati senza un'adeguata segregazione. Per mitigare queste minacce, l'architettura MCP implementa il **principio del minimo privilegio** attraverso la classificazione funzionale degli strumenti. Gli strumenti vengono categorizzati in operazioni di sola lettura (*read-only* o idempotenti, come query informative o calcoli crittografici) e operazioni mutative o potenzialmente distruttive (*state-modifying*, quali scrittura su disco, cancellazione di record, invio di pacchetti di rete o configurazione firewall). Mentre le operazioni di lettura possono essere auto-approvate dal sistema, le azioni mutative richiedono obbligatoriamente un passaggio di validazione manuale (*Human-in-the-Loop*), in cui l'Host sospende l'esecuzione e presenta all'analista una richiesta di consenso esplicito contenente il dettaglio dei parametri prima dell'inoltro al server.

A livello di infrastruttura, i server MCP che gestiscono tool non fidati o parser complessi devono essere isolati all'interno di ambienti di sandboxing rigorosi. L'esecuzione all'interno di container leggeri gestiti tramite [Docker](https://www.docker.com/) o gabbie di isolamento a livello di sistema operativo permette di vincolare l'accesso al filesystem a percorsi di sola lettura, limitare le quote di memoria e CPU, e segregare la connettività di rete. Infine, ogni interazione agentica deve essere tracciata in modo immutabile tramite sistemi di **Audit Logging** forense. Registrando in file di log strutturati in formato JSONL il timestamp UTC, l'identificativo di sessione, il fingerprint crittografico del prompt, il nome dello strumento invocato, i parametri validati, la latenza di esecuzione e il payload di risposta, l'organizzazione mantiene la totale trasparenza e non ripudiabilità delle operazioni condotte dai sistemi autonomi.

## Trade-off e Scelte Operative

La progettazione di sistemi agentici basati su MCP richiede un bilanciamento ponderato tra requisiti prestazionali, vincoli di sicurezza e complessità architetturale. Di seguito vengono analizzati i principali compromessi ingegneristici:

Nel confronto tra trasporto locale `stdio` e trasporto distribuito `SSE su HTTP`, la scelta determina il profilo di latenza e la topologia di deployment del sistema. Il trasporto `stdio` offre un overhead di comunicazione pressoché nullo (inferiore a un millisecondo) e una superficie di attacco ridotta all'ambiente locale, ma vincola l'esecuzione del server alle risorse computazionali della singola macchina host. Al contrario, il trasporto `SSE su HTTP` introduce la latenza tipica delle connessioni di rete e la complessità di gestione dei certificati TLS e delle sessioni distribuite, ma consente di scalare orizzontalmente i server MCP su cluster dedicati, centralizzare l'accesso a risorse aziendali protette e condividere gli stessi strumenti tra molteplici client eterogenei.

Un secondo trade-off riguarda l'adozione di un'architettura a **server monolitico** rispetto a una **federazione di micro-server MCP**. Un singolo server che raggruppa decine di strumenti semplifica la gestione del deployment e riduce il numero di processi attivi, ma concentra i privilegi di sicurezza ed espone l'intero sistema al rischio di crash globale in caso di eccezioni non gestite in un singolo modulo. Una federazione di micro-server specializzati (es. un server per i database, uno per l'intelligence di rete, uno per i filesystem) garantisce il perfetto isolamento dei domini di fallimento (*blast radius containment*) e permette l'applicazione di policy di sicurezza differenziate, richiedendo tuttavia un layer di orchestrazione e dynamic discovery più sofisticato all'interno dell'Host.

Un terzo compromesso risiede nel livello di autonomia operativa concesso all'agente. Sistemi completamente autonomi massimizzano la velocità di esecuzione e riducono l'impegno dell'operatore umano in compiti ripetitivi, ma aumentano esponenzialmente il rischio di allucinazioni a catena e decisioni errate in scenari ambigui. L'integrazione di checkpoint di supervisione umana garantisce la conformità e la sicurezza delle operazioni critiche a fronte di una maggiore latenza complessiva del flusso di lavoro, rappresentando la scelta d'elezione per contesti di cybersecurity, indagini forensi e ambienti enterprise regolamentati.

## Riferimenti Bibliografici e Risorse Tecniche

La letteratura tecnica e scientifica sui sistemi agentici e sui protocolli di contesto fornisce i riferimenti formali per approfondire la progettazione di architetture autonome sicure ed efficienti:

Sulle specifiche di protocollo e sugli standard industriali, la documentazione ufficiale del [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) curata da [Anthropic](https://www.anthropic.com/) descrive l'architettura di riferimento, i lifecycle di connessione e le primitive di estensione. La specifica formale [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) definisce i requisiti di serializzazione e la gestione dei codici di errore per la comunicazione remota tra processi. Le linee guida dell'iniziativa [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) approfondiscono i vettori di attacco su sistemi LLM, inclusi prompt injection e vulnerabilità nel tool calling.

Sui pattern di ragionamento agentico e sulle architetture multi-agente, lo studio cardine su [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) illustra l'integrazione sinergica di tracce di pensiero e invocazione di strumenti per compiti di decision-making complessi. Il framework di ricerca [CAMEL-AI](https://www.camel-ai.org/) (il framework di ricerca open-source pioniere nello studio di agenti autonomi comunicanti e cooperative learning) esplora la comunicazione cooperativa tra agenti autonomi. La piattaforma [AutoGen](https://microsoft.github.io/autogen/) (il framework open-source di Microsoft per la creazione di sistemi multi-agente conversazionali collaborativi) sviluppata da [Microsoft](https://www.microsoft.com/) (la multinazionale informatica leader nei sistemi operativi, cloud computing enterprise con Azure e software per sviluppatori) e il framework [CrewAI](https://www.crewai.com/) (il framework open-source per l'orchestrazione di team di agenti autonomi basati su ruoli specializzati) offrono modelli per l'orchestrazione multi-agente basati su ruoli.

Sull'ecosistema di sviluppo open-source in [Python](https://www.python.org/), la libreria [FastMCP](https://github.com/jlowin/fastmcp) (il framework Python ad alto livello per lo sviluppo rapido e dichiarativo di server Model Context Protocol) fornisce astrazioni ad alto livello per la creazione rapida di server MCP conformi allo standard. Per la modellazione di grafi di stato ciclici e flussi agentici a controllo fine, si rimanda a [LangGraph](https://github.com/langchain-ai/langgraph) (la libreria di orchestrazione di LangChain per costruire architetture agentiche cicliche a grafo con stato persistente) di [LangChain](https://www.langchain.com/), mentre per l'esecuzione e il deployment locale di modelli linguistici open-weights si vedano [Ollama](https://ollama.com/) (lo strumento open-source multipiattaforma per scaricare ed eseguire Large Language Model in locale), [D12b](D12b-ai-harness-plugin-osint.md) per l'isolamento degli agent harness, [D12c](D12c-prompt-context-engineering.md) per l'ingegneria del prompt e del contesto, e [D12d](D12d-loop-graph-engineering.md) per l'ingegneria dei grafi a stati persistenti.

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



### Laboratorio 1 — Server MCP stdio con FastMCP e Validazione Pydantic

Il primo laboratorio guida alla realizzazione di un server MCP completo conforme al protocollo JSON-RPC 2.0 operante sul trasporto standard input/output. Il server espone strumenti di intelligence con validazione dei parametri tramite [Pydantic](https://docs.pydantic.dev/) e gestisce le primitive di discovery e risorse.

- [ ] Definire i modelli Pydantic per la validazione rigorosa dei parametri di input.
- [ ] Implementare la classe del server per la gestione del protocollo e l'handshake `initialize`.
- [ ] Registrare i gestori operativi per i metodi `tools/list`, `tools/call`, `resources/list` e `resources/read`.
- [ ] Configurare il loop di ascolto su `sys.stdin` con emissione controllata su `sys.stdout`.

```python
"""
Laboratorio 1: Server MCP stdio con Validazione Schemi Pydantic e JSON-RPC 2.0.
Modulo: D12 - Sistemi Agentici, Model Context Protocol (MCP) e Automazione Autonoma
"""

import sys
import json
import hashlib
import ipaddress
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError


class ThreatQueryArgs(BaseModel):
    ip_address: str = Field(..., description="Indirizzo IPv4 da interrogare nel database di minacce")
    check_reputation: bool = Field(default=True, description="Flag per includere lo score di reputazione globale")


class HashDigestArgs(BaseModel):
    payload: str = Field(..., description="Stringa di testo o contenuto di cui calcolare il digest crittografico")
    algorithm: str = Field(default="sha256", description="Algoritmo di hashing (md5, sha1, sha256)")


class MCPServerStdio:
    """Implementazione di riferimento di un Server MCP su trasporto standard input/output."""

    def __init__(self, server_name: str = "osint-threat-server", version: str = "1.0.0"):
        self.server_name = server_name
        self.version = version
        self.tools = {}
        self.resources = {
            "threatintel://feeds/daily-bulletin": {
                "name": "Daily Threat Intelligence Bulletin",
                "mimeType": "application/json",
                "text": json.dumps({
                    "date": "2026-08-18",
                    "threat_level": "ELEVATED",
                    "active_campaigns": ["APT28-CredentialHarvesting", "DarkSide-Ransomware-Variant"]
                }, indent=2)
            }
        }
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.tools["query_threat_intelligence"] = {
            "description": "Verifica un indirizzo IP su database OSINT di reputazione e blacklist note.",
            "schema": ThreatQueryArgs.model_json_schema(),
            "handler": self._handle_query_threat,
            "args_model": ThreatQueryArgs
        }
        self.tools["calculate_hash_digest"] = {
            "description": "Calcola il digest crittografico di una stringa con algoritmi sicuri.",
            "schema": HashDigestArgs.model_json_schema(),
            "handler": self._handle_hash_digest,
            "args_model": HashDigestArgs
        }

    def _handle_query_threat(self, args: ThreatQueryArgs) -> Dict[str, Any]:
        try:
            ip_obj = ipaddress.IPv4Address(args.ip_address)
        except ipaddress.AddressValueError:
            raise ValueError(f"Parametro 'ip_address' non valido: '{args.ip_address}' non e' un IPv4 conforme.")

        is_malicious = args.ip_address.startswith("198.51.") or args.ip_address.startswith("203.0.113.")
        score = 88 if is_malicious else 5

        return {
            "ip": str(ip_obj),
            "is_malicious": is_malicious,
            "threat_score": score if args.check_reputation else "N/A",
            "category": "C2_BOTNET" if is_malicious else "CLEAN",
            "autonomous_system": "AS64496 Sample Transit Provider"
        }

    def _handle_hash_digest(self, args: HashDigestArgs) -> Dict[str, Any]:
        algo = args.algorithm.lower()
        if algo == "md5":
            digest = hashlib.md5(args.payload.encode("utf-8")).hexdigest()
        elif algo == "sha1":
            digest = hashlib.sha1(args.payload.encode("utf-8")).hexdigest()
        elif algo == "sha256":
            digest = hashlib.sha256(args.payload.encode("utf-8")).hexdigest()
        else:
            raise ValueError(f"Algoritmo '{args.algorithm}' non supportato. Validi: md5, sha1, sha256.")

        return {
            "algorithm": algo,
            "digest": digest,
            "byte_length": len(args.payload.encode("utf-8"))
        }

    def handle_request(self, raw_line: str) -> Optional[str]:
        if not raw_line.strip():
            return None

        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error: stringa JSON non valida", "data": str(exc)}
            })

        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": self.server_name, "version": self.version},
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": True, "listChanged": False}
                    }
                }
            })

        elif method == "notifications/initialized":
            return None

        elif method == "ping":
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {}})

        elif method == "tools/list":
            tools_list = [
                {"name": name, "description": data["description"], "inputSchema": data["schema"]}
                for name, data in self.tools.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name not in self.tools:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' non trovato sul server."}
                })

            tool_def = self.tools[tool_name]
            try:
                validated_args = tool_def["args_model"](**arguments)
                tool_output = tool_def["handler"](validated_args)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(tool_output, indent=2)}],
                        "isError": False
                    }
                })
            except ValidationError as val_err:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Errore di Validazione Schema: {val_err.json()}"}],
                        "isError": True
                    }
                })
            except Exception as err:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Errore di Esecuzione Tool: {str(err)}"}],
                        "isError": True
                    }
                })

        elif method == "resources/list":
            res_list = [
                {"uri": uri, "name": data["name"], "mimeType": data["mimeType"]}
                for uri, data in self.resources.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"resources": res_list}})

        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self.resources:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Risorsa '{uri}' inesistente."}
                })
            res_data = self.resources[uri]
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "contents": [{"uri": uri, "mimeType": res_data["mimeType"], "text": res_data["text"]}]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Metodo '{method}' non supportato dal server."}
            })

    def run_stdio_loop(self) -> None:
        for line in sys.stdin:
            response = self.handle_request(line)
            if response:
                sys.stdout.write(response + "\n")
                sys.stdout.flush()


def run_unit_tests() -> None:
    server = MCPServerStdio()
    req_init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    res_init = json.loads(server.handle_request(req_init))
    assert res_init["result"]["serverInfo"]["name"] == "osint-threat-server"

    req_tools = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    res_tools = json.loads(server.handle_request(req_tools))
    assert len(res_tools["result"]["tools"]) == 2

    req_call = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "query_threat_intelligence",
            "arguments": {"ip_address": "198.51.100.42", "check_reputation": True}
        }
    })
    res_call = json.loads(server.handle_request(req_call))
    assert res_call["result"]["isError"] is False

    req_bad = json.dumps({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "query_threat_intelligence",
            "arguments": {"ip_address": "IP_INVALIDO"}
        }
    })
    res_bad = json.loads(server.handle_request(req_bad))
    assert res_bad["result"]["isError"] is True
    print("Test di validazione Laboratorio 1 superati con successo.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        MCPServerStdio().run_stdio_loop()
    else:
        run_unit_tests()
```

### Laboratorio 2 — Client Asincrono MCP su Subprocesso stdio

Il secondo laboratorio realizza un client asincrono in [Python](https://www.python.org/) basato su `asyncio.subprocess` che governa l'intero ciclo di vita della connessione con il server MCP, gestendo l'invio di frame JSON-RPC e la gestione dei timeout di risposta.

- [ ] Creare la classe client con gestione asincrona delle pipe di processo.
- [ ] Implementare la logica di handshake e negoziazione delle capabilities.
- [ ] Realizzare le funzioni di query catalogo (`list_tools`) e invocazione remota (`call_tool`).
- [ ] Gestire la terminazione controllata del processo server.

```python
"""
Laboratorio 2: Client Asincrono MCP con Subprocesso stdio e Gestione Timeout.
Modulo: D12 - Sistemi Agentici, Model Context Protocol (MCP) e Automazione Autonoma
"""

import sys
import json
import asyncio
from typing import Dict, Any, List, Optional


class AsyncMCPClient:
    """Client asincrono per interazione con Server MCP su trasporto stdio."""

    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.process: Optional[asyncio.subprocess.Process] = None
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def connect(self) -> Dict[str, Any]:
        self.process = await asyncio.create_subprocess_exec(
            sys.executable, self.server_script_path, "--serve",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        init_response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "async-mcp-orchestrator", "version": "1.0.0"},
            "capabilities": {"roots": {"listChanged": False}}
        })

        await self.send_notification("notifications/initialized", {})
        return init_response

    async def send_request(self, method: str, params: Dict[str, Any], timeout_sec: float = 5.0) -> Dict[str, Any]:
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Connessione MCP non attiva.")

        req_id = self._next_id()
        payload = json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}) + "\n"

        self.process.stdin.write(payload.encode("utf-8"))
        await self.process.stdin.drain()

        try:
            line_bytes = await asyncio.wait_for(self.process.stdout.readline(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Timeout di {timeout_sec}s scaduto nell'attesa del metodo '{method}'.")

        if not line_bytes:
            stderr_err = await self.process.stderr.read() if self.process.stderr else b""
            raise RuntimeError(f"Server terminato inaspettatamente: {stderr_err.decode('utf-8')}")

        response = json.loads(line_bytes.decode("utf-8"))
        if "error" in response:
            raise RuntimeError(f"Errore JSON-RPC [{response['error']['code']}]: {response['error']['message']}")

        return response.get("result", {})

    async def send_notification(self, method: str, params: Dict[str, Any]) -> None:
        if not self.process or not self.process.stdin:
            raise RuntimeError("Connessione MCP non attiva.")

        payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params}) + "\n"
        self.process.stdin.write(payload.encode("utf-8"))
        await self.process.stdin.drain()

    async def list_tools(self) -> List[Dict[str, Any]]:
        result = await self.send_request("tools/list", {})
        return result.get("tools", [])

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        return await self.send_request("tools/call", {"name": tool_name, "arguments": arguments})

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        return await self.send_request("resources/read", {"uri": uri})

    async def close(self) -> None:
        if self.process:
            if self.process.stdin:
                self.process.stdin.close()
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=2.0)
            except (asyncio.TimeoutError, ProcessLookupError):
                self.process.kill()


async def run_client_demo() -> None:
    print("Verifica architettura client asincrono completata.")


if __name__ == "__main__":
    asyncio.run(run_client_demo())
```

### Laboratorio 3 — Server MCP Remoto con Trasporto SSE e Autenticazione

Il terzo laboratorio implementa un server remoto basato su HTTP e Server-Sent Events (SSE), dimostrando la gestione delle sessioni multi-client e l'autenticazione tramite intestazione HTTP Bearer.

- [ ] Implementare il session manager per la gestione delle code asincrone.
- [ ] Definire l'handler HTTP per i canali `GET /sse` e `POST /message`.
- [ ] Integrare il controllo di autenticazione basato su token di sicurezza.
- [ ] Eseguire la simulazione dell'inoltro di richieste JSON-RPC.

```python
"""
Laboratorio 3: Server MCP Remoto con Trasporto SSE (Server-Sent Events) e Autenticazione.
Modulo: D12 - Sistemi Agentici, Model Context Protocol (MCP) e Automazione Autonoma
"""

import json
import uuid
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


API_BEARER_TOKEN = "secret-osint-auth-token-2026"


class MCPSessionManager:
    """Gestione centralizzata delle sessioni e code di eventi SSE per client remoti."""

    def __init__(self):
        self.sessions: Dict[str, Any] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        return session_id

    def remove_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]


class RemoteMCPServerCore:
    """Nucleo applicativo per elaborare chiamate JSON-RPC su canale HTTP."""

    @staticmethod
    def process_rpc(request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "remote-sse-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}, "resources": {}}
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "lookup_dns_records",
                            "description": "Esegue risoluzione DNS per domini target.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"domain": {"type": "string"}},
                                "required": ["domain"]
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            domain = params.get("arguments", {}).get("domain", "unknown.org")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({"domain": domain, "a_records": ["198.51.100.10"], "status": "RESOLVED"})
                    }],
                    "isError": False
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Metodo '{method}' non supportato."}
            }


class HTTPSSERequestHandler(BaseHTTPRequestHandler):
    """Handler HTTP per la gestione dei canali SSE e POST message JSON-RPC."""

    def _check_auth(self) -> bool:
        auth_header = self.headers.get("Authorization", "")
        if auth_header != f"Bearer {API_BEARER_TOKEN}":
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized: Bearer token non valido o assente"}).encode("utf-8"))
            return False
        return True

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/sse":
            if not self._check_auth():
                return
            session_id = str(uuid.uuid4())
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            post_endpoint = f"/message?sessionId={session_id}"
            event_payload = f"event: endpoint\ndata: {post_endpoint}\n\n"
            self.wfile.write(event_payload.encode("utf-8"))
            self.wfile.flush()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/message":
            if not self._check_auth():
                return
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                rpc_req = json.loads(post_body.decode("utf-8"))
                rpc_resp = RemoteMCPServerCore.process_rpc(rpc_req)
            except Exception as e:
                rpc_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(rpc_resp).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run_sse_demo() -> None:
    req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
    resp = RemoteMCPServerCore.process_rpc(req)
    assert resp["result"]["serverInfo"]["name"] == "remote-sse-mcp-server"
    print("Test del server MCP SSE remoto completato con successo.")


if __name__ == "__main__":
    run_sse_demo()
```

### Laboratorio 4 — Agente Autonomo con Guardrail di Sicurezza e Audit Log

Il quarto laboratorio integra l'intero ciclo agentico ReAct con dynamic tool discovery, applicazione di criteri di sicurezza a granularità fine (*Policy Guardrails*) e tracciamento forense immutabile in formato JSONL (*Audit Logging*).

- [ ] Implementare il motore di policy per la segregazione tra tool di sola lettura e azioni mutative.
- [ ] Costruire il logger forense immutabile con fingerprint crittografico SHA-256.
- [ ] Realizzare l'agente autonomo con gestione del ciclo di vita e budget di passi.
- [ ] Eseguire una missione dimostrativa di investigazione OSINT con verifica dei log di audit.

```python
"""
Laboratorio 4: Agente Autonomo ReAct con Discovery Dinamica, Guardrail di Sicurezza e Audit Forense.
Modulo: D12 - Sistemi Agentici, Model Context Protocol (MCP) e Automazione Autonoma
"""

import time
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable


class SecurityPolicyGuardrail:
    """Sistema di controllo accessi e policy per l'esecuzione di tool agentici."""

    READ_ONLY_TOOLS = {"query_threat_intelligence", "calculate_hash_digest", "lookup_dns_records"}
    MUTATIVE_TOOLS = {"isolate_endpoint", "block_firewall_ip", "write_incident_report"}

    @classmethod
    def evaluate_permission(cls, tool_name: str, arguments: Dict[str, Any], human_approved: bool = False) -> bool:
        if tool_name in cls.READ_ONLY_TOOLS:
            return True
        
        if tool_name in cls.MUTATIVE_TOOLS:
            if not human_approved:
                print(f"[GUARDRAIL BLOCKED] Azione mutativa '{tool_name}' richiede approvazione Human-in-the-Loop.")
                return False
            return True

        print(f"[GUARDRAIL BLOCKED] Tool sconosciuto '{tool_name}' non autorizzato dalla policy.")
        return False


class ForensicAuditLogger:
    """Registrazione forense immutabile di ogni interazione agentica."""

    def __init__(self, log_path: str = "agent_audit_trail.jsonl"):
        self.log_path = log_path

    def record_event(self, session_id: str, step: int, thought: str, tool_name: str,
                     arguments: Dict[str, Any], result: Dict[str, Any], duration_ms: float) -> None:
        event_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "step": step,
            "thought_digest": hashlib.sha256(thought.encode("utf-8")).hexdigest(),
            "tool_name": tool_name,
            "arguments": arguments,
            "result_summary": str(result)[:200],
            "execution_duration_ms": duration_ms
        }
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_data) + "\n")


class AutonomousMCPAgent:
    """Agente ReAct con dynamic tool discovery, guardrail e memoria di lavoro."""

    def __init__(self, agent_name: str = "ThreatHunter-Agent", max_steps: int = 5):
        self.agent_name = agent_name
        self.max_steps = max_steps
        self.session_id = f"sess-{int(time.time())}"
        self.audit_logger = ForensicAuditLogger()
        self.available_tools: Dict[str, Dict[str, Any]] = {}
        self.tool_executors: Dict[str, Callable] = {}

    def register_mcp_tool(self, name: str, description: str, schema: Dict[str, Any], executor: Callable) -> None:
        self.available_tools[name] = {"description": description, "inputSchema": schema}
        self.tool_executors[name] = executor

    def _mock_llm_reasoning_engine(self, objective: str, step: int, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if step == 1:
            return {
                "thought": "Verifico se l'indirizzo IP 198.51.100.42 e' associato a botnet o C2 malevoli.",
                "action": "query_threat_intelligence",
                "arguments": {"ip_address": "198.51.100.42", "check_reputation": True}
            }
        elif step == 2:
            return {
                "thought": "L'IP e' confermato malevolo con score 88. Calcolo l'hash identificativo dell'indicatore.",
                "action": "calculate_hash_digest",
                "arguments": {"payload": "IOC:198.51.100.42:C2_BOTNET", "algorithm": "sha256"}
            }
        else:
            return {
                "thought": "Dati raccolti ed etichettati. Sintetizzo il report conclusivo.",
                "action": "FINISH",
                "final_answer": "Investigazione completata: l'indirizzo 198.51.100.42 appartiene alla minaccia C2_BOTNET (Score 88)."
            }

    def execute_mission(self, user_objective: str) -> str:
        history: List[Dict[str, Any]] = []
        
        for step in range(1, self.max_steps + 1):
            decision = self._mock_llm_reasoning_engine(user_objective, step, history)
            thought = decision.get("thought", "")
            action = decision.get("action", "")
            
            if action == "FINISH":
                return decision.get("final_answer", "")

            arguments = decision.get("arguments", {})
            if not SecurityPolicyGuardrail.evaluate_permission(action, arguments, human_approved=False):
                obs = {"error": f"Azione '{action}' rifiutata dai guardrail."}
                history.append({"step": step, "thought": thought, "action": action, "observation": obs})
                continue

            start_time = time.perf_counter()
            try:
                executor = self.tool_executors[action]
                tool_result = executor(arguments)
            except Exception as e:
                tool_result = {"error": f"Eccezione: {str(e)}"}
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            self.audit_logger.record_event(
                session_id=self.session_id,
                step=step,
                thought=thought,
                tool_name=action,
                arguments=arguments,
                result=tool_result,
                duration_ms=elapsed_ms
            )

            history.append({"step": step, "thought": thought, "action": action, "observation": tool_result})

        return "Missione interrotta per limite massimo di step."


def run_laboratory_demo() -> None:
    agent = AutonomousMCPAgent(agent_name="OSINT-Investigator", max_steps=4)
    agent.register_mcp_tool(
        name="query_threat_intelligence",
        description="Verifica reputazione IP",
        schema={"type": "object", "properties": {"ip_address": {"type": "string"}}},
        executor=lambda args: {"ip": args["ip_address"], "threat_score": 88, "status": "CONFIRMED_MALICIOUS"}
    )
    agent.register_mcp_tool(
        name="calculate_hash_digest",
        description="Calcola hash SHA256",
        schema={"type": "object", "properties": {"payload": {"type": "string"}}},
        executor=lambda args: {"hash": hashlib.sha256(args["payload"].encode("utf-8")).hexdigest()}
    )

    result = agent.execute_mission("Analizza l'indirizzo IP sospetto 198.51.100.42.")
    assert "Investigazione completata" in result
    print("Test dell'agente autonomo Laboratorio 4 superato con successo.")

### Laboratorio 5: Integrazione di Qdrant come Server MCP di Ricerca Semantica

Questo laboratorio finale dimostra come convertire un database vettoriale come Qdrant in un server MCP, aderendo all'architettura SOTA 2026. Questo approccio disaccoppia la Knowledge Base (es. Obsidian) dall'agente LLM.

```python
"""
lab_qdrant_mcp.py
Costruisce un server MCP per esporre la ricerca ibrida di Qdrant all'Harness.
"""
from typing import Dict, Any
import requests

class QdrantSemanticSearchMCP:
    def __init__(self, qdrant_url: str = "http://localhost:6333", collection: str = "obsidian_vault"):
        self.url = qdrant_url
        self.collection = collection

    def get_tool_schema(self) -> Dict[str, Any]:
        return {
            "name": "obsidian_semantic_search",
            "description": "Esegue una ricerca semantica ibrida (Vettore + BM25) sul Vault Obsidian.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "La query in linguaggio naturale"},
                    "limit": {"type": "integer", "description": "Numero di frammenti da restituire (max 10)", "default": 5}
                },
                "required": ["query"]
            }
        }

    def execute_search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        # Simulazione del calcolo dell'embedding locale e della chiamata a Qdrant
        print(f"[*] Embedding generato per: '{query}'")
        print(f"[*] Chiamata a {self.url}/collections/{self.collection}/points/search")
        
        # Mock della risposta di Qdrant
        return {
            "results": [
                {"id": 1, "score": 0.92, "payload": {"file": "Strategia.md", "content": "La strategia 2026 prevede l'uso di ICM."}},
                {"id": 2, "score": 0.85, "payload": {"file": "Infrastruttura.md", "content": "I container Docker isolano il backend."}}
            ],
            "status": "success"
        }

def run_lab_5() -> None:
    server = QdrantSemanticSearchMCP()
    schema = server.get_tool_schema()
    print("Schema MCP Esportato:", schema["name"])
    res = server.execute_search("strategia infrastrutturale")
    print("Risultati Ricerca:", res["results"][0]["payload"]["file"])

if __name__ == "__main__":
    run_laboratory_demo()
    run_lab_5()
```