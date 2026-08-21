---
aliases: [Index, Mappa del Percorso, Indice Generale, Stazione Knowledge Base]
---
# Percorso Didattico e Mappa della Knowledge Base

La **Mappa del Percorso** è l'indice sistematico della Stazione Knowledge Base, progettato per guidare la consultazione delle ventuno monografie tecniche dedicate all'ingegneria dell'Intelligenza Artificiale e all'OSINT avanzato. Questo documento struttura l'intero curriculum didattico all'interno del framework [MkDocs](https://www.mkdocs.org/) (il generatore di siti statici per documentazione tecnica), categorizzando ogni modulo in base alla complessità concettuale e ai prerequisiti operativi. L'indice consente a sviluppatori, ricercatori e analisti di orientarsi rapidamente tra i principi teorici, le architetture di sistema e i laboratori applicativi, garantendo un apprendimento progressivo, verificabile e privo di frammentazione informativa.

## Architettura dei Livelli Didattici

Il programma formativo è suddiviso in quattro livelli propedeutici continui, concepiti per trasformare una conoscenza iniziale del codice in una solida padronanza delle pipeline AI end-to-end.

Il livello **Fondamenti** stabilisce i prerequisiti metodologici e infrastrutturali indispensabili. In questo blocco iniziale si affrontano la configurazione del workspace locale con [Git](https://git-scm.com/) (il sistema di controllo versione distribuito open-source) e [Obsidian](https://obsidian.md/) (l'applicazione per la gestione di basi di conoscenza basata su grafi relazionali), le buone pratiche di ingegneria del software in [Python](https://www.python.org/) (la gestione di ambienti virtuali, parsing JSONL e test automatici), la manipolazione di vettori numerici con [NumPy](https://numpy.org/) (la libreria fondamentale per il calcolo scientifico) e [Pandas](https://pandas.pydata.org/) (la libreria per l'analisi di dati strutturati in DataFrame), e i fondamenti matematici di algebra lineare e calcolo differenziale.

Il livello **Operativo** applica la matematica alle tecniche classiche di machine learning e modellazione predittiva. I moduli analizzano la formulazione di problemi supervisionati, le metriche di diagnostica e validazione incrociata con [scikit-learn](https://scikit-learn.org/) (la libreria fondamentale per l'apprendimento automatico), l'addestramento di foreste casuali e modelli di gradient boosting come [XGBoost](https://xgboost.readthedocs.io/) (la libreria scalabile per alberi decisionali potenziati), fino agli algoritmi non supervisionati di clustering e riduzione della dimensionalità geometrica.

Il livello **Avanzato** copre l'ecosistema del deep learning moderno e dei Large Language Model. Lo studio include la differenziazione automatica con [PyTorch](https://pytorch.org/) (il framework di deep learning open-source), il funzionamento interno dell'architettura Transformer e della Self-Attention, i motori di inferenza ottimizzati come [vLLM](https://github.com/vllm-project/vllm) (l'engine di inferenza ad alto throughput con PagedAttention) e [llama.cpp](https://github.com/ggerganov/llama.cpp) (l'engine di inferenza C/C++ ottimizzato per modelli quantizzati), l'architettura dei sistemi Retrieval-Augmented Generation con database vettoriali come [Qdrant](https://qdrant.tech/) (il database vettoriale open-source per ricerca semantica e ibrida), e le metodologie di investigazione in fonti aperte (OSINT) e analisi geopolitica della tecnologia.

Il livello **Specialistico** affronta le frontiere ingegneristiche dell'autonomia software e della messa in produzione. I moduli approfondiscono la creazione di agenti autonomi tramite il protocollo [Model Context Protocol](https://modelcontextprotocol.io/) di [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI), i grafi ciclici di esecuzione con [LangGraph](https://github.com/langchain-ai/langgraph) (la libreria di orchestrazione per architetture agentiche a grafo), le difese di sicurezza contro il prompt injection conformi agli standard di [OWASP](https://owasp.org/) (la fondazione per la sicurezza delle applicazioni software), gli algoritmi di allineamento e preferenza (RLHF e DPO), le pipeline di tracciamento [MLflow](https://mlflow.org/) (la piattaforma per il ciclo di vita del machine learning) e containerizzazione [Docker](https://www.docker.com/) (la piattaforma per isolare ed eseguire applicazioni in container leggeri), fino alla sintesi strategica delle investigazioni complesse.

## Catalogo Completo delle Monografie

La tabella seguente elenca tutti i moduli formativi disponibili, specificando per ciascuno il codice identificativo, il titolo esteso, il livello di appartenenza e il collegamento diretto al documento monografico.

| Codice | Titolo Monografico | Livello Curricolare | Riferimento Documentale |
| :--- | :--- | :--- | :--- |
| **D01** | Architettura Workspace Local-First (Git, Obsidian, LLM) | Fondamenti | [D01-workspace-llm-wiki.md](D01-workspace-llm-wiki.md) |
| **D02** | Ingegneria del Software e Python Essentials per Pipeline AI | Fondamenti | [D02-python-refresher.md](D02-python-refresher.md) |
| **D02b** | Virtualizzazione e Container: Isolamento dell'Infrastruttura AI | Fondamenti | [D02b-virtualizzazione-e-container.md](D02b-virtualizzazione-e-container.md) |
| **D02c** | Gateway e Routing LLM: Il Controllo del Flusso API | Fondamenti | [D02c-gateway-e-routing-llm.md](D02c-gateway-e-routing-llm.md) |
| **D03** | Data Foundations: NumPy, Pandas, SQL e Qualità del Dato | Fondamenti | [D03-data-foundations.md](D03-data-foundations.md) |
| **D04** | Matematica e Statistica Just-in-Time per Machine Learning | Fondamenti | [D04-math-stat.md](D04-math-stat.md) |
| **D05** | Fondamenti di Machine Learning e Metriche Diagnostiche | Operativo | [D05-ml-fondamenti.md](D05-ml-fondamenti.md) |
| **D06** | Machine Learning Classico: Alberi Decisionali, Ensemble e Boosting | Operativo | [D06-ml-classico.md](D06-ml-classico.md) |
| **D07** | Apprendimento Non Supervisionato: Clustering e Riduzione Dimensionale | Operativo | [D07-unsupervised-learning.md](D07-unsupervised-learning.md) |
| **D08** | Deep Learning e Differenziazione Automatica con PyTorch | Avanzato | [D08-deep-learning-pytorch.md](D08-deep-learning-pytorch.md) |
| **D09** | Architetture Transformer, Large Language Models e Inference Engineering | Avanzato | [D09-transformers-llm.md](D09-transformers-llm.md) |
| **D10** | Retrieval-Augmented Generation (RAG), Vector Database e Grafi OSINT | Avanzato | [D10-rag-knowledge-osint.md](D10-rag-knowledge-osint.md) |
| **D11** | Metodologie Investigative OSINT e Discipline di Intelligence | Avanzato | [D11-osint-avanzato.md](D11-osint-avanzato.md) |
| **D11b** | Intelligenza Artificiale come Vettore Offensivo e Bersaglio OSINT | Avanzato | [D11b-ai-arma-bersaglio-osint.md](D11b-ai-arma-bersaglio-osint.md) |
| **D11c** | Geopolitica dei Semiconduttori, Supply Chain e Governance dell'AI | Avanzato | [D11c-geopolitica-ai-osint.md](D11c-geopolitica-ai-osint.md) |
| **D12** | Sistemi Agentici Autonomi, Model Context Protocol e Tool Calling | Specialistico | [D12-agentic-mcp.md](D12-agentic-mcp.md) |
| **D12b** | Sandboxing di AI Harness e Architetture Plugin per Agenti OSINT | Specialistico | [D12b-ai-harness-plugin-osint.md](D12b-ai-harness-plugin-osint.md) |
| **D12c** | Ingegneria Avanzata dei Prompt e Gestione Contestuale per LLM | Specialistico | [D12c-prompt-context-engineering.md](D12c-prompt-context-engineering.md) |
| **D12d** | Loop Engineering, Grafi di Stato Ciclici e Flussi Multi-Agente | Specialistico | [D12d-loop-graph-engineering.md](D12d-loop-graph-engineering.md) |
| **D13** | Reinforcement Learning, Allineamento di Modelli e Ottimizzazione DPO | Specialistico | [D13-rl-alignment.md](D13-rl-alignment.md) |
| **D14** | Sicurezza Informatica dei Sistemi LLM, Difesa OWASP e Responsible AI | Specialistico | [D14-responsible-ai-cyber.md](D14-responsible-ai-cyber.md) |
| **D14b** | Guardrails Locali e Privacy: LLM Guard e Rizzo-PII | Specialistico | [D14b-guardrails-e-privacy.md](D14b-guardrails-e-privacy.md) |
| **D15** | MLOps, LLMOps e Pipeline di Deployment Local-First | Specialistico | [D15-mlops-llmops.md](D15-mlops-llmops.md) |
| **D16** | Metodologia ICM, Orchestrazione Strategica e Comunicazione Esecutiva | Specialistico | [D16-icm-orchestrazione.md](D16-icm-orchestrazione.md) |
| **D16b** | 12-Factor Agents: Progettazione di Agenti Deterministici | Specialistico | [D16b-twelve-factor-agents.md](D16b-twelve-factor-agents.md) |
| **D17** | Agent Context Platform e Model Context Protocol (MCP) | Specialistico | [D17-agent-context-platform-mcp.md](D17-agent-context-platform-mcp.md) |
| **D17b** | Standard Agent Plugins: Pacchettizzazione e Distribuzione Universale | Specialistico | [D17b-standard-agent-plugins.md](D17b-standard-agent-plugins.md) |
| **D18** | Ecosistema Interfacce e Client: Il Single Pane of Glass | Specialistico | [D18-ecosistema-interfacce-client.md](D18-ecosistema-interfacce-client.md) |
| **D19** | Ingegneria delle Identità: Contratti Comportamentali ICM | Specialistico | [D19-ingegneria-delle-identita.md](D19-ingegneria-delle-identita.md) |
| **D20** | Tech Radar e Tool Scouting: Ingegneria della Valutazione | Specialistico | [D20-tech-radar-e-scouting.md](D20-tech-radar-e-scouting.md) |
| **D21** | Architettura SOTA Definitiva: Sintesi del Sistema | Specialistico | [D21-architettura-sota-definitiva.md](D21-architettura-sota-definitiva.md) |

## Standard Metodologico e Norme Redazionali

Tutte le monografie rispettano i principi costituzionali definiti nel [Manifesto Didattico](https://github.com/Bebbolus/stazione-knowledge/blob/main/manifesto-didattica.md): esposizione continua priva di elenchi puntati nella prosa teorica, contestualizzazione rigorosa di ogni entità esterna con apposizione e collegamento ipertestuale, demistificazione fisica dei flussi di dati e preservazione integrale dei laboratori pratici riproducibili.
