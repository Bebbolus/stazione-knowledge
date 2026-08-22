---
aliases:
- Virtualizzazione
- Container
- Docker
- Isolamento
- Sandboxing
- Macchine Virtuali
resources:
- title: Docker in 100 Seconds
  url: https://www.youtube.com/watch?v=Gjnup-PuquQ
  type: video
- title: Play with Docker (Simulatore)
  url: https://labs.play-with-docker.com/
  type: lab
---
# Virtualizzazione e Container: Isolamento dell'Infrastruttura AI

La **Virtualizzazione** e i **Container** sono tecnologie fondamentali per l'isolamento degli ambienti di esecuzione, essenziali per separare il codice applicativo (come agenti AI, server API e database vettoriali) dal sistema operativo host. Nello specifico, [Docker](https://www.docker.com/) (la piattaforma leader per la creazione e gestione di container Linux) rappresenta lo standard per il deployment dei componenti di backend dell'infrastruttura AI, mentre le Macchine Virtuali (VM) usa-e-getta costituiscono la difesa perimetrale obbligatoria per le attività di OSINT e l'esecuzione di codice non fidato. L'isolamento infrastrutturale esiste perché l'esecuzione di script generati dinamicamente da modelli linguistici e la navigazione in reti ostili comportano rischi catastrofici se effettuati direttamente sulla macchina fisica dell'utente.

## Il Problema: Fragilità e Vulnerabilità del Sistema Host

L'ecosistema dell'Intelligenza Artificiale open-source è caratterizzato da dipendenze frammentate, librerie in rapida evoluzione e requisiti di sistema in perenne conflitto. Quando uno sviluppatore tenta di installare sulla propria macchina fisica un gateway come [LiteLLM](https://github.com/BerriAI/litellm) (il router open-source per API multi-provider), un database vettoriale come [Qdrant](https://qdrant.tech/) (il motore di ricerca ibrido ad alte prestazioni scritto in Rust) e un guardrail come [LLM Guard](https://github.com/protectai/llm-guard) (il firewall applicativo di ProtectAI), si scontra inevitabilmente con la "dependency hell". Versioni incompatibili di Python, librerie C++ mancanti o conflitti sulle porte di rete rendono l'ambiente instabile e non riproducibile su altre macchine.

Il secondo problema, ben più grave, è la sicurezza. Gli agenti AI autonomi, come [Goose](https://block.github.io/goose/) (l'agente OSINT open-source sviluppato da Block), sono progettati per interagire con il sistema operativo, scaricare file da Internet ed eseguire codice generato dinamicamente. Se un attaccante riesce a manipolare l'agente tramite prompt injection (ad esempio nascondendo istruzioni malevole in una pagina web che l'agente sta analizzando), l'agente potrebbe eseguire comandi distruttivi o esfiltrare dati personali. Lasciare che un agente operi con i permessi dell'utente sulla macchina principale equivale a cedere il controllo del proprio computer a un'entità vulnerabile alla persuasione algoritmica.

[Michael Bazzell](https://inteltechniques.com/) (l'ex investigatore cyber dell'FBI e autore dei manuali di riferimento per l'OSINT) ha documentato estesamente come l'isolamento sia il prerequisito non negoziabile per qualsiasi attività investigativa o agentica. La soluzione non consiste nell'aggiungere antivirus, ma nel segregare fisicamente o logicamente l'ambiente di esecuzione, garantendo che ogni operazione compromessa possa essere neutralizzata semplicemente distruggendo l'ambiente stesso, senza alcun impatto sul sistema host.

## Lo Spettro dell'Isolamento: VM contro Container

L'industria risolve il problema dell'isolamento attraverso due approcci principali, che differiscono per il livello dello stack tecnologico in cui operano: la virtualizzazione hardware (Macchine Virtuali) e la virtualizzazione a livello di sistema operativo (Container).

Le **Macchine Virtuali** emulano un intero computer fisico, compreso il processore, la memoria, i dischi e la scheda di rete, sopra il quale viene installato un sistema operativo completo (Guest OS). Questo isolamento è garantito da un componente software chiamato Hypervisor, come [VirtualBox](https://www.virtualbox.org/) (l'hypervisor open-source di Oracle) o [KVM](https://www.linux-kvm.org/) (la soluzione di virtualizzazione nativa del kernel Linux). Il livello di sicurezza è massimo: anche se il sistema operativo guest viene compromesso, il sistema host rimane intatto. Il costo di questo isolamento è l'overhead prestazionale e l'allocazione statica delle risorse: una VM richiede gigabyte di RAM e minuti per l'avvio, rendendola inadatta per orchestrare dozzine di microservizi leggeri.

I **Container**, implementati tipicamente tramite [Docker](https://www.docker.com/), operano diversamente. Invece di emulare l'hardware, condividono il kernel del sistema operativo host isolando i processi nello spazio utente (tramite le funzionalità `namespaces` e `cgroups` del kernel Linux). Ogni container include solo l'applicazione e le sue librerie specifiche, percependosi come l'unico processo in esecuzione sul sistema. I container si avviano in millisecondi, pesano megabyte invece di gigabyte e permettono di eseguire centinaia di servizi isolati sulla stessa macchina. Il compromesso è un isolamento di sicurezza più debole rispetto alle VM: poiché condividono lo stesso kernel, una vulnerabilità nel kernel stesso potrebbe permettere a un processo malevolo di "evadere" dal container (container breakout).

## Il Modello Ibrido SOTA 2026: Container per il Backend, VM per il Frontend Ostile

Nella postazione di lavoro AI-Native, nessuna delle due tecnologie è una soluzione universale. L'architettura ottimale utilizza entrambe in domini rigorosamente separati, massimizzando l'efficienza dove serve e blindando la sicurezza dove i rischi sono asimmetrici.

### L'Infrastruttura di Backend in Docker

Tutti i servizi stabili, invisibili e che elaborano dati ma non eseguono codice arbitrario (la "Colonna Vertebrale" dell'infrastruttura) risiedono all'interno di container Docker orchestrati tramite `docker-compose`. Questo strato include il gateway LiteLLM, il database vettoriale Qdrant, la pipeline di guardrails LLM Guard, e gli eventuali motori di inferenza locali come [vLLM](https://github.com/vllm-project/vllm) o [Ollama](https://ollama.com/).

La containerizzazione del backend garantisce la **riproducibilità assoluta**. L'intera infrastruttura è definita in un singolo file YAML; un nuovo sviluppatore o analista può clonare il repository, eseguire `docker-compose up` e ottenere in trenta secondi l'esatta architettura funzionante, indipendente dal sistema operativo sottostante. I container backend comunicano tra loro su una rete virtuale isolata, esponendo all'host fisico solo le porte API strettamente necessarie.

### L'Esecuzione Agentica in Macchine Virtuali Usa-e-Getta

Quando l'architettura deve ospitare agenti autonomi come Goose o script di OSINT che estraggono dati da siti compromessi o ostili, il modello Docker non è sufficiente. In questo dominio si adottano le **Macchine Virtuali usa-e-getta** (disposable VMs). L'ambiente investigativo viene isolato in una VM Linux leggera, avviata da uno snapshot immutabile. L'agente esegue le sue azioni, scarica file potenzialmente malevoli e processa codice generato dall'LLM. 

Al termine dell'operazione, la memoria e il disco virtuale della VM vengono distrutti. L'unico output preservato sono i file JSON o Markdown estratti, validati prima di essere importati nell'ambiente host. Questo paradigma, raccomandato nei manuali di OSINT avanzato, neutralizza radicalmente il rischio di infezione persistente e di prompt injection catastrofica. Se l'agente viene manipolato per cancellare file, cancellerà solo i file temporanei all'interno della VM isolata.

## Laboratorio 1 — Orchestrazione Backend con Docker Compose

Questo laboratorio dimostra l'avvio di un'infrastruttura locale isolata utilizzando `docker-compose`. Il file definisce due servizi: Qdrant per la memorizzazione vettoriale e un mock del gateway LiteLLM, configurando la comunicazione interna e i volumi persistenti.

```yaml
# docker-compose.yml
# Infrastruttura di backend AI-Native isolata
version: '3.8'

services:
  # Servizio 1: Database Vettoriale Qdrant
  qdrant:
    image: qdrant/qdrant:latest
    container_name: kb_vector_db
    restart: unless-stopped
    ports:
      - "6333:6333" # API REST per il client
      - "6334:6334" # gRPC per comunicazioni ad alte prestazioni
    volumes:
      - ./data/qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__MAX_REQUEST_SIZE_MB=50
    # Limita l'uso della memoria per non affamare l'host
    deploy:
      resources:
        limits:
          memory: 2G

  # Servizio 2: Gateway LLM (LiteLLM)
  litellm_gateway:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: llm_router
    restart: always
    ports:
      - "4000:4000"
    volumes:
      - ./config/litellm_config.yaml:/app/config.yaml
    command: [ "--config", "/app/config.yaml", "--detailed_debug" ]
    # LiteLLM può comunicare con Qdrant usando l'hostname 'qdrant'
    depends_on:
      - qdrant

# Crea una rete virtuale isolata per i container
networks:
  default:
    name: ai_backend_network
    driver: bridge
```

Per eseguire l'infrastruttura, è sufficiente navigare nella cartella contenente il file e lanciare il comando `docker-compose up -d`. I container scaricheranno le immagini necessarie, si avvieranno in background e memorizzeranno i dati (come gli indici vettoriali di Qdrant) nella cartella locale `./data/qdrant_storage`. Questa cartella può essere esclusa dal tracciamento Git (`.gitignore`), garantendo che il codice dell'infrastruttura sia condiviso senza diffondere inavvertitamente gigabyte di dati.

## Laboratorio 2 — API Gateway Interno con Python

Questo script Python dimostra come interagire con l'infrastruttura containerizzata dal sistema host, validando che i container siano attivi e pronti a ricevere richieste.

```python
"""
lab_docker_healthcheck.py
Script diagnostico per verificare la raggiungibilità dei servizi
backend isolati nei container Docker.
Requisiti: pip install requests
"""
import requests
import json
import time

def check_qdrant_health(host: str = "http://localhost:6333") -> bool:
    """Verifica lo stato del cluster Qdrant."""
    try:
        print(f"[*] Contattando Qdrant su {host}/readyz...")
        start_time = time.time()
        response = requests.get(f"{host}/readyz", timeout=3)
        latency = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print(f"[+] Qdrant ONLINE (latenza: {latency:.2f}ms)")
            # Ottieni info sul cluster
            info = requests.get(f"{host}/collections").json()
            collections = len(info.get('result', {}).get('collections', []))
            print(f"    Collezioni vettoriali attive: {collections}")
            return True
        else:
            print(f"[-] Qdrant ha risposto con codice HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[-] Qdrant NON RAGGIUNGIBILE. Il container è in esecuzione?")
        return False
    except requests.exceptions.Timeout:
        print("[-] Qdrant TIMEOUT. Il servizio è sovraccarico o bloccato.")
        return False

def check_litellm_health(host: str = "http://localhost:4000") -> bool:
    """Verifica lo stato del router LiteLLM."""
    try:
        print(f"[*] Contattando LiteLLM su {host}/health...")
        response = requests.get(f"{host}/health", timeout=3)
        
        if response.status_code == 200:
            print(f"[+] LiteLLM ONLINE")
            return True
        else:
            # LiteLLM potrebbe restituire 401 se richiede autenticazione
            if response.status_code == 401:
                print("[+] LiteLLM ONLINE (Richiede Autenticazione API Key)")
                return True
            print(f"[-] LiteLLM ha risposto con codice HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[-] LiteLLM NON RAGGIUNGIBILE. Il container è in esecuzione?")
        return False

if __name__ == "__main__":
    print("=== Diagnostica Infrastruttura AI ===")
    qdrant_ok = check_qdrant_health()
    print("-" * 40)
    litellm_ok = check_litellm_health()
    print("=" * 40)
    
    if qdrant_ok and litellm_ok:
        print("VERDETTO: L'infrastruttura backend è pronta per le chiamate agentiche.")
    else:
        print("VERDETTO: Errore nell'infrastruttura. Esegui 'docker-compose logs' per il debug.")
```

L'isolamento via Docker garantisce che lo script diagnostico debba comunicare esclusivamente tramite chiamate di rete standard (HTTP REST). Questa astrazione di rete costringe lo sviluppatore a disaccoppiare la logica dell'agente dalla gestione del database, rispettando il principio della separazione delle responsabilità e facilitando una futura migrazione verso server remoti o cluster gestiti.
