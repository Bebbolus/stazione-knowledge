---
aliases: [Agent Plugins, agent-plugins.org, Standard Plugin Agenti, Packaging MCP, Skill Distribution]
---
# Standard Agent Plugins: Pacchettizzazione e Distribuzione Universale

Lo standard **Agent Plugins** (definito dal consorzio industriale su [agent-plugins.org](https://agent-plugins.org/)) è un formato di pacchettizzazione universale e neutrale rispetto ai fornitori, progettato per distribuire competenze agentiche (Skills) e connettori dati (server MCP) all'interno di una singola directory portatile. Rilasciato nell'agosto del 2026 dal Technical Steering Committee composto da [OpenAI](https://openai.com/), [Microsoft](https://www.microsoft.com/), [AWS](https://aws.amazon.com/), [Cursor](https://cursor.sh/) e [Vercel](https://vercel.com/), lo standard fornisce un wrapper strutturale attorno al Model Context Protocol. Questo formato esiste per risolvere il problema della frammentazione della distribuzione: permette a uno sviluppatore di scrivere una singola cartella di integrazione (contenente le istruzioni per l'agente e le dipendenze software) che viene riconosciuta e installata istantaneamente da qualsiasi client, da Visual Studio Code a DeepSeek Harness, senza richiedere adattamenti proprietari.

## Il Problema: Configurazione Manuale e Incompatibilità dei Client

L'affermazione del [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) ha risolto il problema della standardizzazione delle comunicazioni tra l'agente e i tool, ma ha generato un nuovo collo di bottiglia operativo: la **complessità di installazione e distribuzione**. Per dotare un agente di una nuova abilità (ad esempio, l'accesso a un database vettoriale per la ricerca di sentenze giuridiche), l'utente doveva compiere una serie di passi manuali complessi e disconnessi. 

In primo luogo, l'utente doveva scaricare il server MCP da GitHub. In secondo luogo, doveva installare manualmente le dipendenze di sistema (come Python, Node.js, librerie specifiche). In terzo luogo, doveva modificare il file di configurazione specifico del proprio client (un JSON per Claude Desktop, un pannello UI per Cursor) inserendo manualmente i percorsi degli eseguibili, i parametri della riga di comando e le variabili d'ambiente necessarie (come le chiavi API). Infine, doveva istruire l'agente fornendogli un prompt di sistema per spiegare *come e quando* utilizzare quei nuovi tool, poiché l'agente vedeva solo una lista di funzioni matematiche senza comprenderne il contesto di business.

Questo attrito ingegneristico impediva la rapida adozione dei tool da parte di analisti non programmatori. Ogni client AI (Cursor, VS Code, OpenWork) adottava formati proprietari per la gestione dei prompt e l'installazione delle estensioni, ricreando i "silos chiusi" tipici del mercato del software pre-standardizzazione.

## La Soluzione: La Directory del Plugin

Lo standard Agent Plugins risolve la frammentazione non introducendo un nuovo protocollo di comunicazione (ruolo già assolto da MCP), ma definendo un **formato di pacchettizzazione prevedibile**. Un Agent Plugin non è altro che una directory strutturata in modo rigoroso, che il client AI è in grado di ispezionare (crawling) per auto-configurarsi senza intervento umano.

Il cuore di questa directory è il manifesto `plugin.json` (o `.yml`), che dichiara la versione dello standard, il nome del plugin, gli autori e i metadati. Più importante, il manifesto mappa le risorse interne alla directory. Se il plugin espone un server MCP, la configurazione di esecuzione viene descritta in un file `mcp.json` o dichiarata direttamente nel manifesto, esplicitando il layer di trasporto (`stdio`, `HTTP+SSE`) e le variabili d'ambiente necessarie. Il client AI legge questa dichiarazione e avvia automaticamente il server in background quando il plugin viene caricato.

L'innovazione decisiva dello standard è l'integrazione delle **Agent Skills** insieme al codice esecutivo. All'interno della sotto-directory `skills/`, lo sviluppatore include file Markdown testuali (spesso chiamati `SKILL.md`) che contengono istruzioni in linguaggio naturale. Queste istruzioni spiegano all'agente il contesto di business (es. "Quando ti viene chiesto di cercare una sentenza, utilizza il tool MCP `search_case_law` per trovare le massime, e poi sintetizzale mantenendo i riferimenti legislativi"). Installando il plugin, l'utente installa simultaneamente il "muscolo" (il codice del server MCP) e il "cervello" (le istruzioni per utilizzarlo).

## L'Architettura Vendor-Neutral e i Namespace

La natura agnostica dello standard è garantita dal modello di governance open-source e dall'uso dei **Namespace di Estensione**. Poiché client diversi possono avere funzionalità esclusive (ad esempio, Cursor potrebbe supportare l'inserimento diretto di codice nell'editor, mentre DeepSeek Harness no), lo standard permette agli sviluppatori di inserire nel `plugin.json` configurazioni specifiche per client all'interno di chiavi dedicate (es. `"cursor": {...}`, `"vscode": {...}`). 

Quando un client compatibile carica il plugin, estrae la configurazione base standardizzata e ignora i namespace proprietari che non riconosce, o processa quelli destinati a sé stesso. Questo compromesso architetturale permette a una singola directory di essere distribuita universalmente (Vendor-Neutral), pur mantenendo la capacità di sfruttare le caratteristiche avanzate di editor specifici, evitando il problema del "minimo comune denominatore" che spesso affligge gli standard universali.

## Compromessi Architetturali

L'adozione dello standard Agent Plugins introduce sfide significative in termini di **Sicurezza e Sandboxing**. Distribuire un plugin che auto-installa ed esegue un server MCP locale significa distribuire codice che, di default, eredita i permessi dell'utente sul file system. Sebbene lo standard dichiari quali variabili d'ambiente sono richieste, non impone (né potrebbe farlo) un meccanismo rigido di isolamento in container, demandando l'implementazione della sicurezza al client. Se un utente installa un Agent Plugin scaricato da una fonte non verificata su un client privo di sandboxing, un server MCP malevolo potrebbe esfiltrare file sensibili o stabilire connessioni esterne.

Un secondo compromesso è il **Versioning delle Dipendenze**. Il plugin dichiara come avviare il server MCP (es. `python server.py`), ma la gestione dell'ambiente di esecuzione (virtual environment) rimane problematica. Se il client non orchestra la creazione di ambienti isolati per ogni plugin, due plugin diversi potrebbero richiedere versioni in conflitto della stessa libreria (es. due versioni diverse di `pydantic`), causando il blocco del sistema. Le implementazioni più robuste dello standard superano questo limite fornendo eseguibili pre-compilati (binari nativi in Rust o Go) anziché script interpretati.

## Laboratorio 1 — Struttura di un Agent Plugin

Questo laboratorio dimostra l'alberatura fisica (directory tree) e i file di configurazione essenziali per costruire un Agent Plugin compatibile con lo standard 2026. Il plugin ipotetico, `it.osint.registry`, dota l'agente delle competenze e del codice per interrogare i registri pubblici italiani.

```bash
# Alberatura del pacchetto Agent Plugin
it.osint.registry/
├── plugin.json             # Manifesto dello standard (Obbligatorio)
├── README.md               # Documentazione per l'utente umano
├── mcp.json                # Configurazione di avvio del server (Opzionale)
├── skills/                 # Directory delle competenze testuali
│   └── company_search.md   # Istruzioni in linguaggio naturale per l'agente
└── src/                    # Codice sorgente del server MCP
    ├── main.py
    └── requirements.txt
```

Il file `plugin.json` dichiara i metadati e mappa le risorse.

```json
{
  "$schema": "https://agent-plugins.org/draft-01/schema.json",
  "name": "it.osint.registry",
  "version": "1.0.0",
  "description": "Connettore MCP e Skill per l'interrogazione dei registri camerali italiani.",
  "authors": ["Analista OSINT <analista@example.com>"],
  "license": "MIT",
  "capabilities": {
    "mcpServers": {
      "registry_api": {
        "configPath": "./mcp.json"
      }
    },
    "skills": {
      "path": "./skills"
    }
  },
  "extensions": {
    "openwork": {
      "uiMode": "headless"
    }
  }
}
```

Il file `mcp.json` definisce come il client AI deve avviare il processo, esplicitando la richiesta di una variabile d'ambiente (la chiave API del registro).

```json
{
  "transport": "stdio",
  "command": "python",
  "args": ["src/main.py"],
  "env": {
    "REQUIRED": ["REGISTRO_API_KEY"]
  }
}
```

## Laboratorio 2 — Scrittura di uno SKILL.md

Questo laboratorio mostra come scrivere il file `SKILL.md` (collocato nella directory `skills/` del plugin). Questo file viene letto dal modello linguistico durante la fase di auto-configurazione, istruendolo su *quando e come* invocare i tool MCP forniti dal pacchetto.

```markdown
---
name: Ricerca Societaria Italiana
description: Istruzioni per l'analisi di assetti societari italiani.
triggers: ["cerca azienda", "visura camerale", "chi possiede l'azienda"]
---
# Competenze di Ricerca Societaria

Sei stato equipaggiato con il server MCP `registry_api` per interrogare i registri pubblici italiani. Quando l'utente ti chiede informazioni su un'azienda italiana, DEVI seguire rigorosamente questa procedura:

## 1. Validazione dell'Input
Prima di invocare qualsiasi tool, verifica se l'utente ha fornito un nome azienda o una Partita IVA. Se l'input è ambiguo (es. "Cerca informazioni su Ferrari"), chiedi chiarimenti all'utente, poiché il registro contiene centinaia di aziende omonime.

## 2. Invocazione dei Tool
- Utilizza il tool `search_company_by_name` per trovare l'identificativo univoco (Codice Fiscale o P.IVA) dell'azienda.
- Una volta ottenuto l'identificativo, utilizza SEMPRE il tool `get_company_structure` per recuperare i titolari effettivi e le partecipazioni di primo livello.

## 3. Gestione degli Errori e Formato Output
- Se il tool restituisce `HTTP 404 (Not Found)`, informa l'utente esplicitamente: "L'azienda non risulta iscritta ai registri attivi". Non tentare di inventare dati o dedurli dal nome.
- Formatta SEMPRE la tua risposta finale utilizzando tabelle Markdown, separando il blocco "Dati Anagrafici" dal blocco "Struttura Proprietaria".
```

L'esistenza di questo file disaccoppia il prompt di sistema dal client. Invece di configurare un lungo prompt globale all'interno del frontend (che verrebbe perso cambiando software), la logica di business viaggia incapsulata insieme al codice eseguibile, garantendo che l'agente esegua l'investigazione esattamente come progettata dall'autore del plugin, indipendentemente dal software ospite utilizzato.
