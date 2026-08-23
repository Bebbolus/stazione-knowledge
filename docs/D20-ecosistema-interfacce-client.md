---
aliases:
- Single Pane of Glass
- SPoG
- Ecosistema Interfacce
- Agent Harness
- Client AI
- DeepSeek Harness
- OpenWork
- Goose
resources:
- title: LM Studio
  url: https://lmstudio.ai/
  type: lab
- title: Gradio Documentation
  url: https://www.gradio.app/docs/
  type: ref
---
# Ecosistema Interfacce e Client: Il Single Pane of Glass

Quando si lavora con le AI, il **problema** più grande è la frammentazione cognitiva (il *Context Switching*). Solitamente, un utente deve aprire [Obsidian](https://obsidian.md/) per gli appunti, saltare su una scheda web (come ChatGPT) per fare una domanda copiando e incollando il testo, spostarsi sul terminale per eseguire lo script generato, e infine tornare all'editor. Questo salto continuo tra app diverse affatica il cervello, e impedisce all'AI di vedere tutto il contesto, poiché lo "stato" (file, codice, log) è disperso e inaccessibile all'agente cloud.

La **soluzione** dell'industria è il paradigma **Single Pane of Glass (SPoG)** (Singolo Pannello di Controllo). Invece di fare copia-incolla verso il cloud, portiamo il motore dell'agente direttamente nel nostro ambiente locale tramite un "Client AI" (chiamato *Agent Harness*). Attraverso un'unica interfaccia (es. **DeepSeek Harness** o **OpenWork**) che funge da orchestratore, l'agente può leggere il disco, navigare il terminale e conversare con te, tutto in un solo hub centralizzato.

```text
+-----------------------------------------------------------------------------------------+
|                  ARCHITETTURA SINGLE PANE OF GLASS (SPoG)                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ File System Locale ] ──┐                                                             |
|                           │      +-------------------------------------------+          |
|  [ Terminale / Shell  ] ──┼───►  |  AGENT HARNESS (Il Singolo Pannello)      |          |
|                           │      |  (Visualizza Log, Esegue Code, Chat AI)   |          |
|  [ Web Browser        ] ──┘      +-------------------------------------------+          |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

**DeepSeek Harness (dsh)**, in particolare, rappresenta lo stato dell'arte dell'iper-componibilità. Basato sul motore a plugin **Cordis**, non è un agente pre-confezionato ma una vera e propria infrastruttura in cui ogni componente (l'adattatore LLM, la sandbox di esecuzione, il registro dei tool, l'interfaccia e il loop decisionale) è un pacchetto npm intercambiabile. Questa natura componibile garantisce lo Zero Model Lock-in, permettendo di cablare modelli cloud o locali senza sforzo.

Un'innovazione critica di `dsh` è la **Trajectory View**: ogni singola operazione, pensiero o chiamata a tool generata dal modello viene salvata in un log di sessione immutabile. Questo log permette all'operatore di eseguire *replay*, ispezionare, forzare o creare *fork* di intere sessioni passate, risolvendo definitivamente il problema dell'opacità decisionale degli agenti AI. L'agente non è più una "scatola nera" che genera file, ma un processo di cui l'Harness espone ogni singolo passaggio esecutivo.

## Le Tre Categorie di Agent Harness

Oltre agli Harness orientati al codice, l'ecosistema comprende anche le GUI (Interfacce Grafiche) per l'utente finale che semplificano l'orchestrazione locale.

### Interfacce Grafiche (GUI) Desktop: LM Studio
Mentre framework come Ollama o llama.cpp operano tipicamente da linea di comando o come servizi headless, **LM Studio** rappresenta lo standard de-facto per le GUI desktop nello sviluppo local-first. Permette di:
- **Scaricare modelli con un click** esplorando l'hub di HuggingFace.
- **Selezionare visivamente le quantizzazioni** (es. capire istantaneamente se un Q4 o un Q5 entra nella RAM del proprio sistema).
- **Avviare un server API OpenAI-compatibile** (es. su localhost:1234) per esporre il modello in rete locale affinché altri Agent Harness (come OpenCode o DeepSeek Harness) possano interrogarlo senza accorgersi che il modello gira in locale anziché in cloud.


Il panorama delle interfacce si articola in tre macro-categorie, ciascuna ottimizzata per specifici ruoli operativi e livelli di astrazione.

I **Workspace Desktop (GUI-first)** rappresentano l'evoluzione degli editor di testo verso sistemi operativi applicativi. Progetti come [OpenWork](https://openworklabs.com/) (il desktop agentico open-source basato su OpenCode) o le iterazioni moderne di [Cursor](https://cursor.sh/) offrono un'interfaccia grafica completa. Consentono all'utente non programmatore di installare server MCP tramite un click, gestire sessioni multiple in schede visive, visualizzare grafi di dipendenza e approvare le chiamate ai tool tramite modali grafici. Sono lo standard per analisti OSINT, project manager e ricercatori che necessitano di un basso attrito visivo e non operano principalmente a riga di comando. 

Gli **Harness da Terminale (CLI-first)** si rivolgono a ingegneri di sistema e sviluppatori che operano in ambienti ristretti o headless (server remoti, container Docker). Strumenti come [Goose](https://block.github.io/goose/) (l'agente open-source di Block, nato originariamente come CLI) o [Aider](https://aider.chat/) eseguono il loop agentico direttamente all'interno della shell di sistema. Il vantaggio è il contatto intimo con il sistema operativo: l'agente "respira" le stesse variabili d'ambiente dell'utente e può eseguire comandi bash, compilare codice e navigare il file system con permessi nativi. Lo svantaggio è la difficoltà nell'ispezionare visivamente output strutturati complessi, alberi decisionali profondi o rendering grafici.

I **Framework Algoritmici (Plugin Engine)**, il cui esponente di punta è [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) (l'infrastruttura open-source rilasciata da DeepSeek, basata sul motore a plugin Cordis), rappresentano il terzo livello. Invece di forzare l'utente in una GUI predefinita o in una CLI rigida, forniscono un "motore di eventi" (Event Engine) in cui ogni componente — dal connettore al modello LLM, al renderizzatore UI, alla logica del loop — è un plugin intercambiabile. Avviando `dsh web`, il framework espone un Single Pane of Glass nel browser locale (come una webapp), ma la logica sottostante rimane disaccoppiata. È la scelta di elezione per chi deve costruire flussi ICM (Interpretable Context Methodology) deterministici, in quanto permette di sostituire l'interfaccia grafica o il modello sottostante modificando unicamente file di configurazione testuali.

## La Convergenza tra Obsidian e Harness

Un aspetto cruciale nell'implementazione di un Single Pane of Glass è il destino degli strumenti di knowledge management preesistenti, come Obsidian. Nel paradigma SPoG, **Obsidian cessa di essere l'interfaccia operativa primaria** e si trasforma in un "Motore Semantico Headless" o in un'interfaccia puramente documentale di sola lettura.

L'utente non scrive i prompt o orchestra gli agenti dentro Obsidian. Al contrario, l'Harness (es. DeepSeek Harness) si collega al vault di Obsidian tramite un server MCP dedicato (es. `obsidian-mcp-server`). Questo server espone all'agente le API per navigare il grafo (backlinks, tag, folder). Quando l'operatore chiede all'Harness di compilare un report, l'agente interroga l'MCP di Obsidian in background, estrae le note rilevanti, elabora la logica e genera l'output finale direttamente nell'interfaccia dell'Harness, salvando il risultato come file Markdown su disco. L'utente aprirà Obsidian solo per leggere o editare manualmente i documenti archiviati, non per guidare il processo esecutivo.

## Compromessi Operativi: Complessità di Debug e Superficie di Attacco

Affidare l'interazione esclusiva a un Single Pane of Glass comporta il rischio della **centralizzazione invisibile**. Se l'Harness astrae eccessivamente i processi sottostanti (mostrando solo una rotellina di caricamento mentre il modello linguistico sta impaginando 50 chiamate in background a diversi server MCP), l'operatore umano perde la consapevolezza situazionale. In caso di errore (ad esempio un timeout di rete del server MCP), un Harness mal progettato restituisce all'utente un generico messaggio di fallimento senza indicare quale nodo della catena si è rotto. Per mitigare questo rischio, gli Harness moderni implementano viste di ispezione dei trace (Trace Views) che srotolano l'intero albero delle chiamate JSON scambiate tra client e server, richiedendo però competenze di debugging da parte dell'utente.

Il secondo compromesso riguarda la **sicurezza (Superficie di Attacco Unificata)**. Se l'Harness ha i permessi per accedere simultaneamente al file system locale, al server MCP OSINT e alla rete aziendale, un attacco di prompt injection riuscito sull'Harness espone l'intero perimetro dell'utente. Questo rende indispensabile l'inserimento di filtri middleware, come [LLM Guard](https://github.com/protectai/llm-guard), descritti nei capitoli sulla sicurezza infrastrutturale.

## Laboratorio 1 — Configurazione di DeepSeek Harness (Cordis Plugin)

Questo laboratorio illustra la configurazione modulare tipica di un framework basato su plugin come DeepSeek Harness (dsh). Il file YAML non configura solo i modelli, ma l'intera applicazione SPoG.

```yaml
# dsh_config.yaml
# Definizione del Single Pane of Glass tramite architettura a plugin
plugins:
  # 1. Interfaccia di Superficie (Frontend)
  # Espone la web-UI locale sulla porta 3000
  - name: @dsh/plugin-ui-web
    config:
      port: 3000
      theme: dark

  # 2. Connettori Modello (Gateway locale)
  # Collega l'Harness al router LiteLLM configurato precedentemente
  - name: @dsh/plugin-model-adapter
    config:
      base_url: "http://localhost:4000"
      default_model: "claude-3-5"

  # 3. Gestore di Contesto e Connessioni MCP
  # Configura i server MCP disponibili per gli agenti in esecuzione
  - name: @dsh/plugin-mcp-manager
    config:
      servers:
        - id: "obsidian_backend"
          command: "python"
          args: ["-m", "mcp_obsidian", "--vault-path", "/app/Knowledge"]
        - id: "hybrid_search_qdrant"
          command: "python"
          args: ["-m", "mcp_qdrant", "--url", "http://localhost:6333"]

  # 4. Loop Agentico Deterministico (12-Factor)
  # Impone limiti rigidi sull'autonomia dell'agente
  - name: @dsh/plugin-agent-loop
    config:
      max_iterations: 10
      require_human_approval_for: ["file_system_write", "git_commit"]
      # Implementa il log in stile append-only per audit
      enable_trace_logging: true
      trace_path: "./logs/agent_traces.jsonl"
```

Avviando `dsh start --config dsh_config.yaml`, l'utente non lancia un semplice script Python, ma solleva un ambiente di orchestrazione completo e interattivo nel browser. L'interfaccia mostrerà le opzioni di chat, la vista dell'albero dei file (recuperati tramite l'MCP del file system) e un pannello laterale per approvare o bloccare manualmente le richieste di chiamata ai tool (Human-in-the-Loop), garantendo la sicurezza richiesta dal paradigma 12-Factor.

## Laboratorio 2 — Auditing dei Log SPoG

Per contrastare la centralizzazione invisibile, l'amministratore di sistema o l'analista deve periodicamente validare i log generati dall'Harness. Questo script Python processa i log JSONL (JSON Lines) nativi generati da framework come DeepSeek Harness per estrarre le statistiche di spesa e identificare potenziali loop infiniti.

```python
"""
lab_spog_audit.py
Analizza i trace log generati dal Client SPoG (es. dsh) per diagnosticare
il consumo di token e rilevare anomalie (looping).
"""
import json
import sys
from collections import defaultdict

def audit_trace_log(log_path: str) -> None:
    """Legge un file JSONL di trace e calcola le metriche di esecuzione."""
    total_tokens = 0
    tool_calls = defaultdict(int)
    errors = defaultdict(int)
    sessions = defaultdict(list)
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                try:
                    event = json.loads(line)
                    session_id = event.get('session_id', 'unknown')
                    event_type = event.get('type')
                    
                    if event_type == 'model_response':
                        # Estrai metriche di costo (tokens)
                        usage = event.get('payload', {}).get('usage', {})
                        tokens = usage.get('total_tokens', 0)
                        total_tokens += tokens
                        sessions[session_id].append(('tokens', tokens))
                        
                    elif event_type == 'tool_call':
                        tool_name = event.get('payload', {}).get('tool_name', 'unknown')
                        tool_calls[tool_name] += 1
                        sessions[session_id].append(('tool', tool_name))
                        
                    elif event_type == 'error':
                        err_msg = event.get('payload', {}).get('message', 'unknown_error')
                        errors[err_msg] += 1
                        
                except json.JSONDecodeError:
                    print(f"[Warn] Riga {line_number} malformata. Saltata.")
    except FileNotFoundError:
        print(f"Errore: File '{log_path}' non trovato.")
        return

    # --- Stampa del Report ---
    print("\n" + "="*50)
    print(" REPORT AUDIT SPoG ".center(50, "="))
    print("="*50)
    print(f"Sessioni totali analizzate: {len(sessions)}")
    print(f"Consumo Token Totale:       {total_tokens:,}")
    
    print("\n[ Frequenza Utilizzo Tool MCP ]")
    for tool, count in sorted(tool_calls.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {tool:<25}: {count} invocazioni")
        
    if errors:
        print("\n[ Top Errori Rilevati ]")
        for err, count in sorted(errors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - ({count}x) {err[:80]}...")
            
    print("\n[ Analisi Anomalie (Possibili Loop) ]")
    for sess_id, actions in sessions.items():
        # Se una sessione ha più di 15 tool call consecutive senza risposte
        # all'utente umano, potrebbe essere un loop infinito bloccato.
        tool_count = sum(1 for a in actions if a[0] == 'tool')
        if tool_count > 15:
            print(f"  - [AVVISO] Sessione {sess_id}: "
                  f"Eccessive iterazioni autonome ({tool_count} tool calls). "
                  f"Verificare i vincoli nel file IDENTITY.md dell'agente.")
            
    print("="*50 + "\n")

if __name__ == "__main__":
    # Esempio di utilizzo. Creiamo un mock file log in assenza di dati reali
    test_log = "dummy_trace.jsonl"
    with open(test_log, "w", encoding="utf-8") as f:
        f.write('{"session_id": "sess_1", "type": "tool_call", "payload": {"tool_name": "obsidian_search"}}\n')
        f.write('{"session_id": "sess_1", "type": "model_response", "payload": {"usage": {"total_tokens": 1500}}}\n')
        f.write('{"session_id": "sess_2", "type": "tool_call", "payload": {"tool_name": "agent_reach_web"}}\n')
        for _ in range(16): # Simula un loop
             f.write('{"session_id": "sess_2", "type": "tool_call", "payload": {"tool_name": "read_file"}}\n')
        f.write('{"session_id": "sess_2", "type": "error", "payload": {"message": "MCP timeout"}}\n')

    audit_trace_log(test_log)
```

Questi strumenti diagnostici sono fondamentali: delegare a un SPoG l'orchestrazione non esime l'analista dal governare il processo.
