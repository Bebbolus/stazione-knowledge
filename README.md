# Stazione: Architettura di Conoscenza per Intelligenza Artificiale e OSINT

La **Stazione Knowledge Base** è un'infrastruttura di documentazione e apprendimento open-source, progettata secondo il paradigma *local-first* per esplorare in profondità l'apprendimento automatico, i Large Language Model, i sistemi agentici e le metodologie investigative OSINT. Questo archivio organizza ventuno monografie tecniche progressive all'interno di un portale statico gestito con [MkDocs](https://www.mkdocs.org/) (il generatore di siti statici per documentazione tecnica) e versionato tramite [Git](https://git-scm.com/) (il sistema di controllo versione distribuito open-source). L'obiettivo primario consiste nel fornire una base di conoscenza sovrana, riproducibile e priva di astrazioni superflue, trasformando concetti teorici complessi in codice eseguibile, pipeline di dati resilienti e protocolli operativi pronti per la produzione.

## Architettura e Filosofia Local-First

L'intero patrimonio informativo è archiviato sotto forma di file di testo in formato standard Markdown, eliminando ogni dipendenza da database proprietari o piattaforme cloud commerciali chiuse. Questa impostazione garantisce piena interoperabilità con [Obsidian](https://obsidian.md/) (l'applicazione per la gestione di basi di conoscenza basata su grafi relazionali) e consente di eseguire modelli linguistici locali tramite [Ollama](https://ollama.com/) (lo strumento open-source per l'esecuzione di LLM in locale) o [llama.cpp](https://github.com/ggerganov/llama.cpp) (l'engine di inferenza C/C++ ottimizzato per CPU e GPU). I contenuti pubblici risiedono all'interno della directory `docs/`, mentre la configurazione del sito statico è definita in `mkdocs.yml` adottando il tema grafico [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) (il framework documentale moderno basato su Material Design).

## Struttura del Percorso Curricolare

Il percorso formativo è articolato in quattro livelli didattici consequenziali, strutturati per accompagnare lo studente dai fondamenti di sistema alle architetture agentiche più sofisticate. Il livello **Fondamenti** consolida le basi di ingegneria del software in [Python](https://www.python.org/) (il linguaggio di programmazione di riferimento per l'AI), l'isolamento degli ambienti, l'algebra lineare e le strutture dati tensoriali. Il livello **Operativo** affronta l'apprendimento supervisionato e non supervisionato, concentrandosi su alberi decisionali, ensemble gradient boosting con [scikit-learn](https://scikit-learn.org/) (la libreria cardine per il machine learning classico) e algoritmi di clustering.

Il livello **Avanzato** esplora le reti neurali profonde con [PyTorch](https://pytorch.org/) (il framework open-source di deep learning), l'architettura dei Transformer, i meccanismi di attenzione e le pipeline di Retrieval-Augmented Generation con database vettoriali. Infine, il livello **Specialistico** si focalizza sui protocolli agentici basati su [Model Context Protocol](https://modelcontextprotocol.io/) (lo standard aperto creato da Anthropic per la connessione sicura tra modelli e strumenti), sulle tecniche di sicurezza informatica, sull'allineamento dei modelli e sulle pratiche industriali di MLOps con [Docker](https://www.docker.com/) (la piattaforma per l'esecuzione di container software isolati).

## Consultazione e Rigore Metodologico

Ogni monografia della knowledge base segue standard didattici rigorosi: apertura immediata a piramide invertita, spiegazione fisica e matematica dei fenomeni senza ricorso a metafore vaghe, analisi esplicita dei compromessi operativi tra latenza, memoria e costi computazionali, e preservazione integrale del codice eseguibile. Per consultare la mappa interattiva dei moduli e accedere alle lezioni dettagliate, fare riferimento all'[Indice Generale del Percorso](docs/index.md), mentre per approfondire i criteri redazionali è possibile esaminare il [Manifesto Didattico](manifesto-didattica.md).

## Esecuzione Locale e Strumenti

Per visualizzare localmente la documentazione con ricaricamento a caldo e navigazione completa, è sufficiente clonare il repository da [GitHub](https://github.com/) (la piattaforma di hosting cloud per codice e collaborazione), predisporre l'ambiente virtuale ed eseguire il server integrato di MkDocs.

```bash
# Clonazione del repository e accesso alla directory
git clone https://github.com/tuo-utente/stazione-knowledge.git
cd stazione-knowledge

# Configurazione dell'ambiente virtuale e installazione dipendenze
python -m venv .venv
source .venv/bin/activate  # Su Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# Avvio del server locale di documentazione
mkdocs serve
```