---
aliases: [12-Factor Agents, Twelve Factor Agents, Principi di Ingegneria degli Agenti, Agenti Deterministici, HumanLayer 12 Factor]
---
# Principi di Ingegneria degli Agenti: I 12-Factor Agents

I **12-Factor Agents** sono un insieme di dodici principi ingegneristici per costruire sistemi AI agentici affidabili in produzione, formulati da [Dex Horthy](https://humanlayer.dev/) (fondatore di [HumanLayer](https://github.com/humanlayer/humanlayer), la piattaforma open-source per integrare l'approvazione umana nei flussi agentici) e ispirati alla celebre metodologia dei [12-Factor App](https://12factor.net/) originariamente codificata dagli ingegneri di [Heroku](https://www.heroku.com/) (la piattaforma cloud che ha definito le best practice per il software cloud-native). I dodici fattori si applicano ovunque un Large Language Model venga utilizzato come componente decisionale all'interno di software deterministico, e il loro scopo è eliminare la fragilità che affligge il 90% dei prototipi agentici che non sopravvivono al passaggio in produzione.

## Il Problema: Prototipi Magici che Crollano in Produzione

La maggior parte degli sviluppatori che costruiscono agenti AI commette un errore fondamentale. Trattano l'agente come un **loop autonomo magico** che, ricevendo un obiettivo, dovrebbe risolvere tutto da solo iterando all'infinito fino al risultato. In un demo di cinque minuti questa architettura funziona: l'agente chiama un tool, legge il risultato, decide il passo successivo, e alla fine produce un output accettabile. Ma quando lo stesso codice viene esposto a utenti reali, a dati sporchi e a sessioni che durano ore, il sistema collassa.

Il collasso avviene per ragioni prevedibili. La **finestra di contesto** si riempie di tentativi falliti e il modello inizia ad allucinare. Lo **stato interno** dell'agente (cosa ha già fatto, cosa deve ancora fare) vive solo nella conversazione chat e svanisce se il processo crolla. I **costi dei token** esplodono perché ogni tentativo ed errore aggiunge migliaia di token alla catena. L'**approvazione umana** non è prevista nel loop, quindi l'agente compie azioni irreversibili senza supervisione.

[Dex Horthy](https://humanlayer.dev/) ha sintetizzato questi fallimenti ricorrenti in un framework diagnostico preciso. La tesi centrale è controintuitiva rispetto alla narrativa dominante: **i sistemi agentici di successo in produzione sono per la maggior parte software deterministico**, dove il Large Language Model interviene soltanto in punti decisionali specifici e circoscritti. L'agente non è un mago che improvvisa; è un componente software con input, output e contratti ben definiti.

## I Dodici Fattori: Anatomia di un Agente Affidabile

### Fattore 1 — Dal Linguaggio Naturale alle Chiamate di Tool

Il primo principio stabilisce la separazione tra **decisione** ed **esecuzione**. Il modello linguistico non esegue azioni nel mondo reale: emette una struttura dati (tipicamente un oggetto JSON) che descrive quale tool chiamare e con quali parametri. Il codice deterministico dell'applicazione riceve questo JSON, valida i parametri, esegue la chiamata e restituisce il risultato al modello. Questa separazione è cruciale perché permette di intercettare, validare e limitare ogni azione dell'agente prima che venga effettivamente eseguita. Se il modello decide di cancellare un file, il codice deterministico può verificare i permessi, chiedere conferma all'utente o rifiutare l'operazione, indipendentemente da quanto il modello sia "convinto" della sua decisione.

### Fattore 2 — Possedere i Propri Prompt

I prompt sono codice sorgente a tutti gli effetti e vanno trattati come tale. Devono risiedere in file versionati (nel caso della metodologia ICM di [Jake Van Clief](https://github.com/RinDig) (il creatore della Interpretable Context Methodology), nei file `IDENTITY.md` e `CONTEXT.md` delle cartelle di progetto), devono essere sottoposti a review tramite merge request e devono essere testati con casi specifici. Il secondo fattore vieta di delegare la gestione dei prompt a framework di terze parti che li nascondono dentro astrazioni opache. Quando un framework costruisce il prompt per te concatenando template interni, perdi la capacità di diagnosticare perché l'agente si comporta in un certo modo. Possedere i prompt significa possedere il comportamento del sistema.

### Fattore 3 — Possedere la Propria Finestra di Contesto

La finestra di contesto è il confine fisico del sistema. Ogni token che entra nella finestra costa denaro e occupa spazio che potrebbe essere usato per informazioni più rilevanti. Il terzo fattore impone di **curare attivamente** ciò che entra nel contesto, invece di scaricarvi tutto lo storico della conversazione, tutti i log delle chiamate precedenti e tutti i file del progetto. Strumenti come [Headroom](https://github.com/headroomlabs-ai/headroom) (il compressore di token open-source creato da Tejas Chopra, ingegnere senior di [Netflix](https://www.netflix.com/)) possono ridurre il consumo del 60-95% comprimendo output JSON, log e frammenti RAG prima che raggiungano il modello. Ma anche senza strumenti dedicati, la regola è semplice: l'agente deve ricevere **solo** i file e le informazioni strettamente necessarie allo stadio corrente del lavoro.

### Fattore 4 — I Tool Sono Output Strutturati

Questo fattore demistifica il concetto di "tool calling" che molti framework presentano come una capacità magica dei modelli. In realtà, quando un modello "chiama un tool", sta semplicemente generando un blocco di testo strutturato (JSON) che il codice dell'applicazione interpreta. Non c'è nessuna connessione diretta tra il modello e il tool: il modello produce dati, il codice agisce. Comprendere questa meccanica elimina il misticismo e permette di diagnosticare i problemi con gli stessi strumenti del debugging software tradizionale.

### Fattore 5 — Compattare gli Errori nella Finestra di Contesto

Quando un tool fallisce, l'errore non deve essere ignorato né propagato nella sua interezza. Il quinto fattore impone di **formattare l'errore** in modo conciso e strutturato (ad esempio: `{"tool": "web_search", "error": "timeout after 30s", "suggestion": "retry with simpler query"}`) e iniettarlo nella finestra di contesto dell'agente affinché possa correggere autonomamente la propria azione. Scaricare un traceback Python di 200 righe nella finestra di contesto è uno spreco di token che degrada la qualità delle risposte successive. L'errore deve essere un segnale, non un rumore.

### Fattore 6 — Pre-Caricare il Contesto

Il sesto fattore affronta un anti-pattern comune: l'agente che decide autonomamente quali dati recuperare durante l'esecuzione. In un sistema affidabile, il contesto necessario viene **pre-caricato** prima che il modello inizi a ragionare. Se l'agente deve analizzare un documento, quel documento viene letto e iniettato nel contesto **prima** della prima chiamata al modello, non durante un loop intermedio dove il modello potrebbe decidere di leggere il file sbagliato o di non leggerlo affatto. Nella struttura ICM, questo avviene naturalmente: il file `CONTEXT.md` della cartella corrente definisce esplicitamente quali file di riferimento caricare.

### Fattore 7 — Unificare lo Stato di Esecuzione e lo Stato di Business

Il settimo fattore è il più insidioso per chi costruisce agenti. Molti sistemi mantengono due stati paralleli: lo **stato di esecuzione** (in quale punto del loop si trova l'agente, quali tool ha già chiamato) e lo **stato di business** (qual è lo stato del task nel mondo reale, ad esempio "la bozza del capitolo è completa al 60%"). Quando questi due stati vivono in strutture separate, si desincronizzano inevitabilmente. La soluzione è unificarli in un unico oggetto di stato persistente — che nella filosofia ICM è semplicemente un file Markdown sul disco contenente sia il log delle azioni compiute sia lo stato corrente del deliverable.

### Fattore 8 — Lanciare, Sospendere, Riprendere

Un agente di produzione deve supportare le operazioni di **launch** (avvio), **pause** (sospensione con salvataggio dello stato) e **resume** (ripresa dallo stato salvato). Se il processo crolla, se l'utente chiude il terminale o se il server si riavvia, l'agente deve poter ricominciare esattamente dal punto in cui si era fermato. Questo è possibile solo se lo stato è persistito su disco (Fattore 7) e non vive esclusivamente nella memoria volatile della sessione di chat.

### Fattore 9 — Possedere il Proprio Flusso di Controllo

Il nono fattore è il più polemico. Afferma che **l'applicazione**, non il modello, deve possedere il flusso di controllo. Il modello sceglie l'azione successiva (quale tool chiamare, quale testo generare), ma il codice dell'applicazione possiede il loop, le condizioni di terminazione, i timeout e i budget di spesa. Se l'agente ha consumato il 90% del budget di token senza completare il task, il codice deterministico lo ferma — indipendentemente dal fatto che il modello "voglia" continuare. Se l'agente è in un loop di retry da più di 5 iterazioni, il codice deterministico interrompe e richiede l'intervento umano.

### Fattore 10 — Attivabile da Qualsiasi Sorgente

Un agente non deve essere attivabile solo da una chat. Il decimo fattore impone che il sistema supporti **webhook**, cron job, eventi del file system e trigger programmatici. Nella pratica ICM, questo significa che un agente può essere attivato quando un file appare in una cartella specifica, quando un merge request viene aperto su [GitLab](https://about.gitlab.com/) (la piattaforma DevOps open-source per la gestione del codice), o quando un timer scade.

### Fattore 11 — Agenti Piccoli e Focalizzati

Il principio della **modularità** si applica anche agli agenti. Invece di costruire un agente monolitico che sa fare ricerca, analisi, scrittura e revisione, il fattore undici impone di creare **micro-agenti specializzati** per ogni responsabilità. Nella struttura ICM, ogni cartella (`01_Ricerca`, `02_Analisi`, `03_Redazione`) ospita un agente con un `IDENTITY.md` diverso. L'agente nella cartella di ricerca non scrive documenti; l'agente nella cartella di redazione non fa ricerca web. La specializzazione riduce drasticamente le allucinazioni perché l'agente opera in un dominio ristretto con istruzioni precise.

### Fattore 12 — L'Agente come Riduttore Senza Stato

L'ultimo fattore è il più elegante dal punto di vista dell'ingegneria del software. Tratta l'agente come una **funzione pura** nel senso della programmazione funzionale: dato uno stato corrente e un input (un evento, un messaggio, il risultato di un tool), l'agente produce un nuovo stato. La formula è `nuovo_stato = f(stato_corrente, input)`. Non ci sono effetti collaterali nascosti, non c'è memoria implicita che vive solo nella sessione del processo. Tutto lo stato è esplicito, serializzabile e ispezionabile. Questo permette di **replayare** qualsiasi esecuzione passata, di debuggare un comportamento anomalo rieseguendo la stessa sequenza di (stato, input), e di scalare orizzontalmente senza preoccuparsi di conflitti di stato.

### Il Tredicesimo Principio — Contattare gli Umani con Chiamate di Tool

Sebbene il framework originale ne conti dodici, la community ha adottato un tredicesimo principio che Horthy enfatizza costantemente: l'**approvazione umana** non è un canale esterno al sistema, ma un'operazione strutturata implementata come tool call. Quando l'agente ha bisogno di una decisione umana (ad esempio: "Questo report è pronto per la pubblicazione?"), emette una chiamata di tool `request_human_approval(artifact="report.md", question="Conforme ai criteri?")`. L'applicazione intercetta questa chiamata, notifica l'utente (via email, via interfaccia, o semplicemente creando un file `REVIEW_NEEDED.md` nella cartella ICM) e sospende l'agente fino alla risposta.

## Convergenza con la Metodologia ICM

La sovrapposizione tra i 12-Factor Agents e la **Interpretable Context Methodology** di [Jake Van Clief](https://github.com/RinDig) non è casuale. Entrambe le metodologie nascono dalla stessa osservazione empirica: i framework multi-agente complessi (quelli che orchestrano sciami di agenti in conversazioni parallele) falliscono sistematicamente in produzione a causa del **context bloat**, delle **race condition** sui file e dell'impossibilità di auditare le decisioni intermedie.

La struttura ICM implementa nativamente almeno otto dei dodici fattori. Le **cartelle numerate** (`01_Ricerca`, `02_Analisi`) implementano il Fattore 11 (agenti piccoli e focalizzati). Il **file system come stato** implementa i Fattori 7 e 8 (stato unificato, launch/pause/resume). I file **IDENTITY.md** implementano il Fattore 2 (possedere i prompt). Il **CONTEXT.md** implementa il Fattore 6 (pre-caricamento del contesto). Il **passaggio sequenziale** tra cartelle (single-agent sequential handoff) implementa il Fattore 9 (possedere il flusso di controllo).

La differenza principale è che ICM raggiunge questi obiettivi **senza scrivere codice**: la struttura delle cartelle e i file Markdown sono il framework. I 12-Factor Agents forniscono il vocabolario ingegneristico per spiegare **perché** questa semplicità funziona meglio delle alternative complesse.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D16b-twelve-factor-agents. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Quando i 12-Factor Non Bastano

I dodici fattori sono ottimizzati per task **convergenti**: task che hanno un obiettivo chiaro, criteri di accettazione definiti e un percorso ragionevolmente prevedibile verso la soluzione. Per task **divergenti** (brainstorming creativo, esplorazione di uno spazio di soluzioni sconosciuto, generazione artistica), il rigore deterministico può diventare una gabbia. Un agente costretto a produrre output strutturato JSON quando dovrebbe esplorare liberamente idee finirà per generare output formalmente corretto ma intellettualmente sterile.

La raccomandazione della community è pragmatica: applicare i 12-Factor ai task operativi (deploy, analisi, reportistica, coding) e rilassare deliberatamente i vincoli per i task esplorativi, documentando esplicitamente nel `CONTEXT.md` della cartella ICM che quello specifico stadio opera in "modalità creativa" con budget di token più ampio e criteri di accettazione più flessibili.

Un altro limite emerge quando il task richiede **conoscenza conversazionale accumulata**. Il Fattore 12 (stateless reducer) impone che tutto lo stato sia esplicito e serializzabile, ma alcune interazioni umane producono sfumature di contesto (tono, preferenze implicite, storia della relazione) che sono difficili da catturare in un file JSON senza perdere informazione. In questi casi, un approccio ibrido (stato esplicito per le decisioni operative, conversazione fluida per l'interazione umana) è più realistico di un'applicazione dogmatica del principio.

## Laboratorio 1 — Il Riduttore Senza Stato

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



Questo laboratorio implementa il cuore del Fattore 12: un loop agente che tratta ogni iterazione come una funzione pura `(stato, evento) → nuovo_stato`. Lo stato è un dizionario Python serializzabile su disco; l'agente non conserva alcuna memoria implicita tra un'iterazione e l'altra.

```python
"""
lab_stateless_reducer.py
Dimostra il pattern del 12-Factor Agent #12: Stateless Reducer.
L'agente è una funzione pura che mappa (stato, evento) -> nuovo_stato.
"""
import json, pathlib, datetime

STATE_FILE = pathlib.Path("agent_state.json")

def load_state() -> dict:
    """Carica lo stato corrente dal disco, oppure inizializza."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {
        "phase": "init",
        "tasks_completed": [],
        "tasks_pending": ["ricerca", "analisi", "redazione"],
        "errors": [],
        "created_at": datetime.datetime.now().isoformat()
    }

def save_state(state: dict) -> None:
    """Persiste lo stato su disco per launch/pause/resume (Fattore 8)."""
    state["updated_at"] = datetime.datetime.now().isoformat()
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def reduce(state: dict, event: dict) -> dict:
    """
    La funzione riduttrice: dato lo stato corrente e un evento,
    produce un nuovo stato senza effetti collaterali nascosti.
    """
    new_state = state.copy()
    new_state["tasks_completed"] = list(state["tasks_completed"])
    new_state["tasks_pending"] = list(state["tasks_pending"])
    new_state["errors"] = list(state["errors"])

    if event["type"] == "task_complete":
        task = event["task"]
        if task in new_state["tasks_pending"]:
            new_state["tasks_pending"].remove(task)
            new_state["tasks_completed"].append(task)
            # Avanza la fase
            if not new_state["tasks_pending"]:
                new_state["phase"] = "done"
            else:
                new_state["phase"] = new_state["tasks_pending"][0]

    elif event["type"] == "error":
        # Fattore 5: compatta l'errore in un segnale conciso
        compact_error = {
            "tool": event.get("tool", "unknown"),
            "message": event.get("message", "")[:200],
            "timestamp": datetime.datetime.now().isoformat()
        }
        new_state["errors"].append(compact_error)

    elif event["type"] == "human_approval":
        # Fattore 13: l'approvazione umana come tool call strutturato
        new_state["human_approved"] = event.get("approved", False)
        if event.get("approved"):
            new_state["phase"] = "approved"

    return new_state

# --- Simulazione del loop agente ---
if __name__ == "__main__":
    state = load_state()
    print(f"Stato iniziale: fase={state['phase']}, "
          f"pending={state['tasks_pending']}")

    # Simula una sequenza di eventi
    events = [
        {"type": "task_complete", "task": "ricerca"},
        {"type": "error", "tool": "web_search", "message": "Timeout 30s"},
        {"type": "task_complete", "task": "analisi"},
        {"type": "task_complete", "task": "redazione"},
        {"type": "human_approval", "approved": True}
    ]

    for event in events:
        state = reduce(state, event)
        print(f"  Evento: {event['type']:20s} -> "
              f"fase={state['phase']}, "
              f"completati={state['tasks_completed']}")

    save_state(state)
    print(f"\nStato finale salvato in {STATE_FILE}")
    print(f"Errori compattati: {len(state['errors'])}")
```

L'output del laboratorio mostra la transizione deterministica tra stati. Lo stato è sempre ispezionabile (basta leggere il file JSON), sempre replayable (basta rieseguire la stessa sequenza di eventi) e sopravvive ai crash del processo perché viene persistito su disco.

## Laboratorio 2 — Tool Calling come Output Strutturato

Questo secondo laboratorio dimostra il Fattore 4: i tool non sono magia, sono output strutturati. Il modello genera un JSON che descrive quale funzione chiamare e con quali argomenti; il codice deterministico esegue la funzione e restituisce il risultato.

```python
"""
lab_tool_calling.py
Dimostra il pattern del 12-Factor Agent #4: Tools are Structured Outputs.
Simula un agente che emette JSON per le chiamate di tool,
con il codice deterministico che possiede il flusso di controllo (Fattore 9).
"""
import json

# --- Registro dei tool disponibili (l'applicazione li possiede) ---
TOOL_REGISTRY = {}

def register_tool(name: str):
    """Decoratore per registrare tool nel registro deterministico."""
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator

@register_tool("search_knowledge_base")
def search_kb(query: str, max_results: int = 5) -> dict:
    """Simula una ricerca nella Knowledge Base locale."""
    return {
        "results": [
            {"file": "D12-rag-knowledge-osint.md", "score": 0.92},
            {"file": "D14-agentic-mcp.md", "score": 0.87}
        ],
        "total": 2
    }

@register_tool("write_file")
def write_file(path: str, content: str) -> dict:
    """Simula la scrittura di un file (con validazione dei permessi)."""
    # Fattore 9: il codice deterministico valida PRIMA di eseguire
    forbidden_paths = ["/etc/", "/sys/", "C:\\Windows\\"]
    if any(path.startswith(p) for p in forbidden_paths):
        return {"error": "Permission denied", "path": path}
    return {"status": "written", "path": path, "bytes": len(content)}

def execute_tool_call(tool_call: dict) -> dict:
    """
    Esegue una chiamata di tool emessa dal modello.
    Il modello produce il JSON, l'applicazione lo esegue deterministicamente.
    """
    name = tool_call.get("tool")
    args = tool_call.get("arguments", {})

    if name not in TOOL_REGISTRY:
        # Fattore 5: errore compattato, non traceback completo
        return {"error": f"Tool '{name}' not found", "available": list(TOOL_REGISTRY.keys())}

    try:
        result = TOOL_REGISTRY[name](**args)
        return {"status": "success", "result": result}
    except TypeError as e:
        return {"error": f"Invalid arguments: {str(e)[:100]}"}

# --- Simulazione ---
if __name__ == "__main__":
    # Simula l'output del modello: un JSON strutturato, non testo libero
    model_outputs = [
        {"tool": "search_knowledge_base",
         "arguments": {"query": "come funziona l'hybrid search", "max_results": 3}},
        {"tool": "write_file",
         "arguments": {"path": "output/report.md",
                        "content": "# Report\n\nAnalisi completata."}},
        {"tool": "delete_database",
         "arguments": {"target": "production"}}
    ]

    print("=== Loop Agente con Tool Calling Deterministico ===\n")

    # Fattore 9: il CODICE possiede il loop, non il modello
    MAX_ITERATIONS = 10
    budget_tokens = 50000
    tokens_used = 0

    for i, tool_call in enumerate(model_outputs):
        if i >= MAX_ITERATIONS:
            print(f"STOP: raggiunto il limite di {MAX_ITERATIONS} iterazioni")
            break

        tokens_used += 500  # stima semplificata
        if tokens_used > budget_tokens:
            print(f"STOP: budget token esaurito ({tokens_used}/{budget_tokens})")
            break

        print(f"Iterazione {i+1}: tool={tool_call['tool']}")
        result = execute_tool_call(tool_call)
        print(f"  Risultato: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
```

Il laboratorio mostra tre aspetti cruciali. Il modello non "chiama" i tool: emette JSON che il codice deterministico interpreta ed esegue. Il codice possiede i limiti (budget, iterazioni massime, permessi sui path). E quando il modello tenta di chiamare un tool inesistente (`delete_database`), l'errore viene compattato in un messaggio conciso che può essere iniettato nel contesto successivo per auto-correzione.
