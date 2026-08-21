---
aliases: [Agent Context Platform, Model Context Protocol, MCP, Separazione dei Domini, Architettura Plugin, Strumenti Agentici]
---
# Agent Context Platform e Model Context Protocol (MCP)

L'**Agent Context Platform** è l'architettura logica che separa l'interfaccia utente (l'agent harness o client di chat) dalle capacità di esecuzione effettive (lettura di file, accesso a database, ricerca web, esecuzione di codice). Questa separazione è resa possibile dal [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (il protocollo standard aperto sviluppato da [Anthropic](https://www.anthropic.com/) per uniformare l'interazione tra i modelli di intelligenza artificiale e le fonti di dati esterne). In questa architettura, l'agente non possiede nativamente gli strumenti, ma si collega tramite connessioni standard (come `stdio` o `HTTP+SSE`) a server MCP indipendenti. L'architettura esiste per risolvere il problema dell'obsolescenza rapida dei framework agentici, permettendo agli sviluppatori di mantenere un arsenale di strumenti stabili (i server) pur cambiando continuamente il client frontend in base all'evoluzione del mercato.

## Il Problema: Monoliti Agentici e Lock-in delle Capacità

Prima dell'affermazione del Model Context Protocol, ogni framework agentico implementava la propria architettura per la gestione degli strumenti (tool calling). Se un analista scriveva in Python uno script sofisticato per l'accesso a un database vettoriale da usare con l'agente [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) (il primo esperimento popolare di agenti autonomi), quello script funzionava *solo* dentro AutoGPT. Quando il mercato si spostava verso un nuovo strumento come [Cursor](https://cursor.sh/) (l'editor di codice AI-first) o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (l'assistente CLI di Anthropic), le capacità non erano portabili. L'utente doveva riscrivere l'integrazione del database per il nuovo ecosistema.

Questo accoppiamento rigido (tight coupling) tra il client (il programma che l'utente vede e usa) e le competenze tecniche (i tool per raccogliere dati o agire sul sistema) generava un enorme debito tecnico. Le aziende si trovavano bloccate in framework obsoleti semplicemente perché il costo di migrazione degli strumenti proprietari verso un nuovo client era troppo elevato. Inoltre, il codice del client diventava rapidamente un monolite instabile, gonfio di dipendenze eterogenee necessarie per supportare centinaia di strumenti diversi (dalle librerie per manipolare PDF ai driver per database SQL).

## Il Paradigma MCP: Client Agnostici e Server Specializzati

L'infrastruttura moderna risolve il problema adottando il paradigma client-server tipico dello sviluppo web, applicato all'ecosistema LLM tramite il **Model Context Protocol**. Il sistema viene diviso chirurgicamente in due parti.

Il **Client MCP** (l'Harness) è il programma con cui l'utente interagisce. Applicazioni come [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) o il desktop [OpenWork](https://openworklabs.com/) funzionano come interfacce generiche. Sanno come instradare i messaggi al modello linguistico e sanno come visualizzare l'output, ma nativamente *non sanno fare nulla*: non sanno leggere il disco, non sanno navigare sul web, non sanno interrogare database. 

Il **Server MCP** è un programma leggero e autonomo che espone una specifica competenza seguendo lo standard del protocollo. Un server MCP per il file system (es. `mcp-server-filesystem`) espone al client i tool per leggere e scrivere file. Un server MCP per [Obsidian](https://obsidian.md/) espone i tool per navigare il grafo dei collegamenti. Un server MCP per [Qdrant](https://qdrant.tech/) espone i tool per la ricerca semantica (Hybrid Search).

Quando il Client si avvia, stabilisce una connessione ai Server MCP configurati dall'utente. I server comunicano al client la lista dei tool disponibili, completi di descrizione e schema JSON dei parametri. Il client passa questa lista al modello linguistico. Se il modello decide di utilizzare un tool, il client inoltra la richiesta formattata al server MCP corrispondente, attende l'esecuzione, e restituisce il risultato testuale al modello.

## La Portabilità Assoluta

Il vantaggio fondamentale di questa separazione è la **portabilità assoluta**. L'analista può investire risorse nella creazione di un server MCP altamente specializzato per analizzare documenti aziendali protetti. Una volta creato, quel singolo server può essere collegato simultaneamente a Claude Code dal terminale, a Cursor nell'editor di codice, e a OpenWork nell'interfaccia grafica desktop. Se domani viene rilasciato un nuovo "client rivoluzionario", l'analista dovrà semplicemente aggiungere il percorso del proprio server MCP nel file di configurazione del nuovo client, portando con sé l'intero arsenale di strumenti personalizzati senza riscrivere una singola riga di codice logico. L'investimento ingegneristico si sposta dal client (volatile) ai server MCP (stabili e riutilizzabili).

L'aggiornamento critico delle specifiche di Luglio/Agosto 2026 ha rifondato il protocollo su un'architettura **completamente stateless** (senza stato). Nelle versioni precedenti, i server MCP richiedevano il mantenimento di sessioni persistenti ("sticky sessions"), complicando il bilanciamento del carico. L'eliminazione dello stato persistente consente oggi ai server MCP di essere eseguiti come micro-funzioni effimere (es. Cloudflare Workers), riducendo drasticamente i costi di hosting per gli strumenti cloud-based.

## Le Nuove Primitive MCP: Tasks e Apps (Agosto 2026)

Oltre ai tradizionali Tools e Resources, lo standard MCP ha recentemente introdotto due primitive avanzate per flussi operativi complessi:
- **Tasks**: Progettati per operazioni asincrone a lunga esecuzione (long-running jobs). A differenza dei tool immediati, i Task supportano il *polling*, il mantenimento di *durable handles* e l'iniezione di input intermedi (mid-flight input) mentre il job è in esecuzione (es. un job di addestramento modello o uno scraping web intensivo di 30 minuti).
- **Apps**: Un ponte visivo tra il backend e l'agente. Le App permettono al server MCP di restituire componenti UI interattivi (come grafici D3.js, form di compilazione o riproduttori video) che vengono renderizzati in tempo reale all'interno del Single Pane of Glass (es. DeepSeek Harness), superando il limite del puro output testuale.

## Meccanismi di Trasporto e Sicurezza

Il protocollo MCP supporta diversi meccanismi di comunicazione (transport layers), adattabili al livello di sicurezza e isolamento richiesto.

Il trasporto **Stdio (Standard Input/Output)** è il più comune per l'uso locale. Il client avvia il server come processo figlio sulla stessa macchina e comunica scrivendo nello standard input del processo e leggendo dal suo standard output. Questo metodo non richiede l'apertura di porte di rete (garantendo immunità dagli attacchi di rete esterni) ed eredita naturalmente i permessi dell'utente locale.

Il trasporto **HTTP con SSE (Server-Sent Events)** è utilizzato quando il server MCP risiede su una macchina diversa o in un container Docker isolato. Il client invia richieste tramite chiamate HTTP POST standard e riceve le risposte, o aggiornamenti di stato asincroni, tramite un flusso continuo SSE. Questa separazione di rete è essenziale per la sicurezza nelle pipeline OSINT: il client gira sulla macchina sicura dell'analista, mentre il server MCP che naviga il web per estrarre dati gira su una Macchina Virtuale isolata (sandbox). Anche se il server viene compromesso da codice malevolo scaricato dalla rete, il sistema dell'analista rimane inaccessibile.

## Compromessi Operativi: Latenza e Difficoltà di Debugging

L'astrazione basata su MCP introduce un costo in termini di **latenza**. In un monolite, chiamare una funzione Python per leggere un file richiede microsecondi. Nel modello MCP, la richiesta deve essere serializzata in JSON dal client, trasmessa al server tramite uno stream, parsata dal server, eseguita, re-serializzata, trasmessa indietro e parsata nuovamente dal client. Sebbene per operazioni lente (come interrogare un database remoto o raschiare una pagina web) questo overhead di pochi millisecondi sia invisibile, per operazioni intensive ad alta frequenza (come la manipolazione di array matematici complessi all'interno di un loop agentico stretto), il bottleneck I/O diventa un problema architetturale.

Il secondo compromesso riguarda la **tracciabilità degli errori** (debugging). Quando un agente fallisce un compito, la causa originaria potrebbe risiedere in un'allucinazione del modello linguistico, in un bug del client MCP (che formatta male i parametri), nel livello di trasporto (un timeout dello stream), o nel server MCP (un errore di permessi sul file system locale). Disaccoppiare i componenti richiede un'infrastruttura di logging centralizzata molto più matura rispetto a quella necessaria per uno script monolitico.

## Laboratorio 1 — Configurazione Client MCP (DeepSeek Harness)

Questo laboratorio mostra come un'applicazione Client (es. DeepSeek Harness o Claude Desktop) configura la connessione ai propri Server MCP tramite un file JSON, definendo i percorsi eseguibili o gli URL di rete.

```json
{
  "mcpServers": {
    "filesystem_locale": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\Analyst\\Progetti\\Investigazioni",
        "C:\\Users\\Analyst\\Download"
      ]
    },
    "qdrant_hybrid_search": {
      "command": "python",
      "args": [
        "-m",
        "mcp_qdrant_hybrid",
        "--url",
        "http://localhost:6333",
        "--collection",
        "obsidian_vault"
      ]
    },
    "osint_sandbox": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "osint_vm_container",
        "node",
        "/app/mcp-server-puppeteer/build/index.js"
      ]
    }
  }
}
```

La configurazione dimostra la potenza dell'architettura: il client delega l'accesso ai file locali a un pacchetto Node.js, la ricerca semantica a un modulo Python, e lo scraping web a un ambiente isolato Docker, coordinando il tutto come un'interfaccia unificata.

## Laboratorio 2 — Implementazione di un Server MCP Minimale in Python

Questo script dimostra quanto sia semplice costruire un server MCP custom utilizzando l'SDK Python ufficiale. Il server espone un singolo strumento in grado di calcolare la distanza di Levenshtein tra due stringhe.

```python
"""
lab_mcp_server.py
Implementazione di un server MCP locale tramite trasporto Stdio.
Requisiti: pip install mcp
Esecuzione per test (con client compatibile): npx @modelcontextprotocol/inspector python lab_mcp_server.py
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 1. Inizializzazione del Server
app = Server("StringDistanceTool")

# 2. Registrazione dei Metadati del Tool (esposti al Client)
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Informa il client dei tool disponibili in questo server."""
    return [
        Tool(
            name="calculate_distance",
            description="Calcola la distanza di Levenshtein tra due stringhe (utilità per matching OSINT).",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Stringa di partenza"},
                    "target": {"type": "string", "description": "Stringa di destinazione"}
                },
                "required": ["source", "target"]
            }
        )
    ]

# 3. Logica di Esecuzione del Tool
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Esegue la logica quando il client richiede l'uso del tool."""
    if name != "calculate_distance":
        raise ValueError(f"Tool non riconosciuto: {name}")

    source = arguments.get("source", "")
    target = arguments.get("target", "")

    # Implementazione ingenua della distanza (per scopi dimostrativi)
    def levenshtein(s1: str, s2: str) -> int:
        if len(s1) < len(s2): return levenshtein(s2, s1)
        if len(s2) == 0: return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    distance = levenshtein(source, target)
    
    # Restituisce il risultato strutturato al Client MCP
    result = f"Distanza di Levenshtein tra '{source}' e '{target}': {distance}"
    return [TextContent(type="text", text=result)]

# 4. Avvio del Server tramite loop asincrono su STDIO
async def main():
    print("Avvio del server MCP su STDIO (Log diretti a stderr disabilitati)", flush=True)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

Il codice espone nativamente il tool a qualsiasi client conforme, isolando la logica di calcolo matematico. Se si volesse sostituire l'implementazione in Python con una in C++ o Rust per migliorare le prestazioni, basterebbe avviare un nuovo eseguibile MCP; il client non richiederebbe alcuna configurazione aggiuntiva né subirebbe interruzioni di servizio, poiché il contratto JSON in ingresso e in uscita rimarrebbe inalterato.
