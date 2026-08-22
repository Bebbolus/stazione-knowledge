---
aliases:
- LLM Gateway
- Routing LLM
- LiteLLM
- BYOK
- Proxy LLM
- Gestione Costi AI
resources:
- title: LiteLLM Official Documentation
  url: https://docs.litellm.ai/
  type: ref
---
# Gateway e Routing LLM: Il Controllo del Flusso API

Il **Gateway LLM** è un'infrastruttura middleware (un server proxy) che si posiziona tra le applicazioni client (gli agenti AI, i notebook Jupyter, i frontend chat) e i provider dei modelli linguistici (come OpenAI, Anthropic, Google o server locali). L'implementazione open-source di riferimento è [LiteLLM](https://github.com/BerriAI/litellm) (il router proxy sviluppato da BerriAI), che traduce automaticamente le chiamate API scritte per uno specifico formato (tipicamente lo standard OpenAI) nel formato richiesto dal provider di destinazione. Il gateway esiste perché collegare direttamente gli script applicativi alle singole API cloud crea debito tecnico insostenibile, vincola l'infrastruttura a un singolo fornitore (vendor lock-in) ed espone l'utente a interruzioni di servizio non mitigate.

## Il Problema: Frammentazione API e Vendor Lock-in

L'ecosistema dei Large Language Models è intrinsecamente volatile. Quando uno sviluppatore scrive il codice per interrogare [Anthropic Claude 3.5](https://www.anthropic.com/) (il modello di punta per compiti di programmazione logica), deve utilizzare l'SDK specifico di Anthropic. Se la settimana successiva viene rilasciato [DeepSeek V3](https://deepseek.com/) (il modello open-source altamente competitivo) e lo sviluppatore desidera testarlo, deve riscrivere le funzioni di chiamata di rete per adattarle alla sintassi del nuovo provider. Questa riscrittura continua frammenta il codice, impedisce la comparazione rapida dei modelli (A/B testing) e rende i repository software rapidamente obsoleti.

Un problema correlato è la gestione delle chiavi di accesso (API keys). Negli strumenti proprietari, l'utente è costretto a inserire la propria chiave all'interno delle interfacce di terze parti o a pagare abbonamenti premium per accedere ai modelli. Questo approccio viola il principio del **Bring Your Own Key (BYOK)**, costringendo l'analista a frammentare il budget su decine di servizi e a perdere il controllo granulare sulla spesa (token economy). Inoltre, se il provider subisce un disservizio (outage) o introduce rate-limit restrittivi, le applicazioni direttamente accoppiate a quel provider smettono immediatamente di funzionare, paralizzando le pipeline di produzione.

L'adozione di un Gateway LLM locale risolve simultaneamente queste patologie. Funge da punto di ingresso unico, normalizza la comunicazione e accentra la logica di fallback, di bilanciamento del carico e di monitoraggio della spesa. 

## LiteLLM: Traduzione e Uniformazione del Formato

L'intuizione architetturale alla base di [LiteLLM](https://github.com/BerriAI/litellm) è l'adozione dello standard API di OpenAI come lingua franca. Il gateway espone un server locale (`http://localhost:4000`) che si comporta esattamente come le API ufficiali di OpenAI. Qualsiasi libreria client, agent harness o script Python progettato per usare OpenAI può essere dirottato verso il gateway semplicemente cambiando l'URL di base (Base URL). 

Quando il gateway riceve la richiesta standard, esamina il parametro `model` specificato (ad esempio `model="anthropic/claude-3-5-sonnet-20240620"`). Esegue quindi una traduzione sintattica del payload JSON: adatta la struttura dei messaggi, mappa il formato dei ruoli (`system`, `user`, `assistant`), converte i parametri come `temperature` e `max_tokens` nelle convenzioni del provider di destinazione, e inietta la chiave API corretta prelevata in modo sicuro dalle variabili d'ambiente locali. Infine, invia la richiesta ad Anthropic, riceve la risposta, la riconverte nel formato OpenAI e la restituisce al client. Il client non è mai a conoscenza della traduzione avvenuta; percepisce di aver parlato con un server OpenAI.

## Fallback e Resilienza dell'Infrastruttura

La capacità più critica di un Gateway LLM in produzione è la gestione automatica dei fallimenti. I provider cloud introducono frequentemente limitazioni temporanee (rate-limit HTTP 429) o vanno incontro a disservizi completi (HTTP 500). Un gateway implementa meccanismi di **Fallback** invisibili all'applicazione chiamante. 

Nella configurazione del router (tramite un file `config.yaml`), lo sviluppatore può definire gerarchie di salvataggio. Se il modello primario (es. Claude 3.5 Sonnet) fallisce o va in timeout, il gateway intercetta l'errore e ritenta immediatamente la stessa query con il modello secondario (es. GPT-4o). Se anche il secondario fallisce, il traffico viene deviato verso un modello locale leggero ospitato su [Ollama](https://ollama.com/) (il gestore di modelli open-source locale). Il client riceve la risposta senza che l'errore interrompa l'esecuzione dell'agente. Questo disaccoppiamento trasferisce la gestione della resilienza dal codice dell'agente (che dovrebbe implementare complessi loop di retry e try/except) all'infrastruttura di rete.

## Bilanciamento del Carico e Monitoraggio dei Costi

Il gateway gestisce anche il traffico ad alto volume distribuendolo su chiavi diverse o endpoint differenti, una tecnica nota come **Load Balancing**. Se un task OSINT richiede l'analisi parallela di mille pagine web, superando il limite di chiamate al minuto di una singola chiave API, il router distribuisce le richieste a rotazione tra più chiavi valide o tra diverse implementazioni cloud dello stesso modello open-source, evitando i blocchi di rete.

Centralizzare tutte le chiamate attraverso il gateway fornisce una visibilità totale sulla **Token Economy**. Il gateway traccia ogni token generato o consumato, registrando quale specifico agente o task lo ha speso. Questo permette di impostare budget massimi giornalieri per specifici flussi di lavoro, bloccando automaticamente l'agente se supera la spesa prevista a causa di un loop infinito o di una finestra di contesto esplosa. L'ottimizzazione dei costi non avviene più "a sensazione", ma basandosi sui metriche deterministiche archiviate dal gateway locale in database SQL leggeri.

## Compromessi Operativi

L'uso di un Gateway LLM locale introduce specifici compromessi ingegneristici. Il primo è l'aggiunta di un singolo punto di fallimento locale (Single Point of Failure): se il container Docker di LiteLLM si ferma (crash per mancanza di memoria, errore di configurazione), tutti gli script applicativi perdono istantaneamente l'accesso ai modelli, anche se le API cloud originali funzionano perfettamente. 

Il secondo limite riguarda il ritardo (lag) nell'adozione di nuove funzionalità proprietarie. Quando un provider annuncia una nuova caratteristica API radicale (come formati di caching del prompt non standardizzati o nuove modalità di structured output), il supporto nel gateway richiede tempo per essere mappato sulla lingua franca OpenAI. Fino all'aggiornamento del parser di traduzione, i client non possono sfruttare nativamente le innovazioni proprietarie attraverso il proxy.

## Laboratorio 1 — Configurazione e Routing YAML

Questo laboratorio mostra come configurare il file di routing di LiteLLM per mappare modelli multipli su un unico endpoint e impostare regole di fallback automatiche.

```yaml
# config.yaml
# Configurazione router per LiteLLM (montata nel container Docker)

model_list:
  # Modello primario: Claude 3.5 via Anthropic
  - model_name: claude-3-5
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20240620
      api_key: "os.environ/ANTHROPIC_API_KEY"
      # Timeout massimo in secondi
      timeout: 30

  # Modello secondario di backup: GPT-4o via OpenAI
  - model_name: gpt-4-fallback
    litellm_params:
      model: openai/gpt-4o
      api_key: "os.environ/OPENAI_API_KEY"

  # Modello locale gratuito, privacy assoluta
  - model_name: local-llama3
    litellm_params:
      model: ollama/llama3
      api_base: "http://host.docker.internal:11434"

# Regole di Fallback
router_settings:
  fallbacks:
    # Se il primario (claude) fallisce (429, 500, timeout),
    # devia automaticamente la query al fallback (gpt-4)
    - {"claude-3-5": ["gpt-4-fallback", "local-llama3"]}
```

Con questa configurazione attiva, qualsiasi agente che richiede il modello logico generico `claude-3-5` viene instradato verso l'infrastruttura reale e gestito con le regole di resilienza. Se le chiavi API a pagamento sono esaurite, la richiesta viene silenziosamente servita dal modello locale gratuito ospitato dall'utente.

## Laboratorio 2 — Interrogare Modelli Eterogenei con Codice Uniforme

Questo script Python dimostra come interrogare i modelli definiti nel gateway locale usando esclusivamente la libreria ufficiale `openai`, simulando un agente che interagisce in modo provider-agnostic.

```python
"""
lab_gateway_client.py
Test di chiamata API standard verso il gateway locale LiteLLM.
Requisiti: pip install openai
Il gateway converte il formato dietro le quinte.
"""
from openai import OpenAI
import time

# Configura il client OpenAI per puntare al Gateway LiteLLM locale
# NOTA: api_key non serve se LiteLLM usa quelle ambientali, ma la libreria la richiede
client = OpenAI(
    base_url="http://localhost:4000", 
    api_key="sk-not-needed-here"
)

def query_model(model_identifier: str, prompt: str) -> None:
    """Interroga il modello passando attraverso il Gateway."""
    print(f"\n[*] Interrogando modello logico: '{model_identifier}'")
    try:
        start_time = time.time()
        
        # Questa chiamata usa lo standard OpenAI (messages, model, temperature)
        # Il gateway la tradurrà per Anthropic, Ollama, ecc.
        response = client.chat.completions.create(
            model=model_identifier,
            messages=[
                {"role": "system", "content": "Sei un analista tecnico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        latency = (time.time() - start_time) * 1000
        content = response.choices[0].message.content.strip()
        provider = response.model # LiteLLM restituisce l'ID del modello reale usato
        
        print(f"[+] Latenza: {latency:.0f}ms | Provider Reale: {provider}")
        print(f"[+] Risposta: {content[:100]}...\n")
        
    except Exception as e:
        print(f"[-] Errore durante la chiamata: {str(e)}")

if __name__ == "__main__":
    test_prompt = "Spiega in una frase cosa è il protocollo HTTP."
    
    # L'agente cambia motore senza modificare la logica di rete
    
    # 1. Chiama Claude (via Anthropic API)
    query_model("claude-3-5", test_prompt)
    
    # 2. Chiama Llama3 (locale via Ollama)
    query_model("local-llama3", test_prompt)
    
    # 3. Testa il Fallback forzando un errore (es. modello inesistente 
    # se configurato nelle regole di routing yaml)
    # query_model("claude-3-5", test_prompt) # Se Anthropic fosse offline
```

Questo disaccoppiamento architetturale è il pilastro del "Future-Proofing": quando nel 2027 emergeranno nuovi leader di mercato nel panorama dei modelli linguistici, il codice dell'analista non subirà alcuna modifica. Si aggiornerà unicamente il file YAML del gateway locale per puntare al nuovo servizio.
