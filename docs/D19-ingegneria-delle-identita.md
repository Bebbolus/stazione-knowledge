---
aliases: [Ingegneria delle Identità, IDENTITY.md, CONTEXT.md, Progettazione Identità Agente, Contratti Comportamentali, ICM Identity Engineering]
---
# Ingegneria delle Identità: Progettare i Contratti Comportamentali degli Agenti

L'**Ingegneria delle Identità** è la disciplina che insegna a progettare i file `IDENTITY.md` e `CONTEXT.md` che governano il comportamento di un agente AI all'interno di ogni stadio di un flusso di lavoro basato sulla [Interpretable Context Methodology (ICM)](https://github.com/RinDig/icm-architect) di [Jake Van Clief](https://github.com/RinDig) (il ricercatore e ingegnere che ha formalizzato la metodologia "Folders over Agents" e creato lo strumento [icm-architect](https://github.com/RinDig/icm-architect) per la generazione automatica di workspace agentici). Questi file sono **contratti comportamentali scritti in linguaggio naturale**: definiscono chi è l'agente, cosa può fare, cosa non può fare, quale formato deve avere il suo output, e quali criteri determinano il completamento del lavoro. L'Ingegneria delle Identità esiste perché l'alternativa tradizionale — mantenere librerie statiche di decine di prompt pre-scritti ("il prompt del ricercatore", "il prompt del revisore", "il prompt dell'analista OSINT") — non scala in un ecosistema dove i tool, i modelli e i task cambiano su base settimanale.

## Il Problema: Prompt Generici e Librerie Statiche

Quando un utente assegna a un Large Language Model un ruolo vago come "Sei un assistente utile", il modello produce output generico. La risposta è corretta nel senso superficiale — rispetta la grammatica, cita fatti plausibili, mantiene un tono cortese — ma manca di **specializzazione operativa**. Non sa quale formato deve avere il suo output (un file Markdown? un JSON? una tabella?). Non sa quali fonti deve consultare e quali ignorare. Non sa quando il suo lavoro è finito e quando deve continuare a iterare. Il risultato è un agente che produce testo accettabile ma inutilizzabile in una pipeline di produzione dove il file generato deve essere letto dalla cartella successiva da un altro agente con aspettative precise.

Il primo tentativo di risolvere questo problema è stato la creazione di **librerie statiche di prompt**. Repository come il vecchio approccio di `agentic-set` contenevano quaranta e più file di prompt specializzati: `griller.md` per il questioning aggressivo, `threat_modeler.md` per la modellazione delle minacce, `wisdom_extractor.md` per la sintesi di concetti, `librarian.md` per la catalogazione. Ogni file era un prompt system pre-scritto che poteva essere caricato nell'agente per dargli un'identità specifica.

Questo approccio funziona nel breve termine ma soffre di tre patologie terminali. La **fossilizzazione**: i prompt vengono scritti per un modello specifico (ad esempio Claude 3.5) e quando il modello viene aggiornato (Claude 4, Gemini 2.5, DeepSeek V3), i prompt non sfruttano le nuove capacità o peggio producono comportamenti inattesi. La **rigidità contestuale**: un prompt pre-scritto per "analisi di minacce informatiche" non funziona per "analisi di minacce finanziarie" senza modifiche, e il costo di mantenere varianti per ogni sotto-dominio cresce esponenzialmente. L'**incompatibilità ICM**: i prompt statici non contengono le informazioni strutturali necessarie per funzionare in una pipeline a cartelle — non specificano da quale file leggere l'input, in quale file scrivere l'output, e come segnalare il completamento del task.

L'Ingegneria delle Identità supera queste patologie insegnando non i prompt specifici ma la **struttura generativa** di un'identità agente. Invece di fornire il pesce (quaranta file prompt), fornisce la canna da pesca (la grammatica per costruirne di nuovi per qualsiasi dominio).

## Anatomia di un File IDENTITY.md

Il file `IDENTITY.md` risiede nella cartella di ogni stadio ICM (ad esempio `01_Ricerca/IDENTITY.md`) e definisce il **contratto comportamentale** dell'agente che opererà in quella cartella. La sua struttura non è arbitraria: ogni sezione risolve un problema specifico che emergerebbe se fosse omessa.

### La Definizione del Ruolo

La prima sezione dell'`IDENTITY.md` dichiara **chi è l'agente** in termini di competenze e responsabilità operative. Non è una descrizione di personalità ("Sei un esperto gentile e paziente") ma una specifica funzionale ("Sei un analista OSINT specializzato in fonti aperte italiane. La tua competenza copre la ricerca su registri pubblici, la verifica di identità aziendali tramite la Camera di Commercio e l'analisi di domini web tramite WHOIS"). La precisione del ruolo determina la qualità dell'output: un agente definito come "ricercatore generico" produce risultati dispersivi; un agente definito come "ricercatore di fonti aperte specializzato in registri catastali italiani" produce risultati chirurgici.

La definizione del ruolo deve includere anche il **livello di autonomia**. Un agente in una cartella di ricerca dovrebbe avere autonomia massima nella raccolta dati ma autonomia zero nella formulazione di giudizi o raccomandazioni. Un agente in una cartella di analisi dovrebbe avere autonomia nel formulare ipotesi ma zero autonomia nel contattare fonti esterne. Questa separazione implementa il Fattore 11 dei [12-Factor Agents](https://humanlayer.dev/) di [Dex Horthy](https://humanlayer.dev/) (fondatore di [HumanLayer](https://github.com/humanlayer/humanlayer)): agenti piccoli e focalizzati, ciascuno responsabile di una sola fase del processo.

### I Vincoli di Dominio

La seconda sezione definisce esplicitamente cosa l'agente **non deve fare**. I vincoli negativi sono più potenti delle istruzioni positive perché eliminano interi spazi di comportamento indesiderato con una singola regola. "Non inventare dati che non trovi nelle fonti fornite" impedisce le allucinazioni. "Non contattare fonti esterne se non tramite i tool MCP elencati" impedisce l'esfiltrazione di dati. "Non modificare file al di fuori della cartella corrente" impedisce le interferenze tra stadi.

La formulazione dei vincoli richiede attenzione ingegneristica. Un vincolo troppo ampio ("Non fare nulla di pericoloso") è inutile perché il modello non condivide la definizione umana di "pericoloso". Un vincolo troppo specifico ("Non usare la keyword DELETE nelle query SQL") è fragile perché può essere aggirato con sinonimi o con una riformulazione della query. Il bilanciamento ottimale specifica il **comportamento vietato** in termini operativi concreti ("Non emettere chiamate di tool che modificano o cancellano file. Le uniche operazioni di scrittura permesse sono la creazione di nuovi file nella sotto-cartella output/").

### La Specifica dell'Input

La terza sezione enumera i file che l'agente **deve leggere** come contesto prima di iniziare a lavorare. Nella struttura ICM, questo corrisponde al Fattore 6 dei 12-Factor Agents (pre-caricare il contesto). L'elenco è esplicito e completo: "Leggi il file `CONTEXT.md` della cartella corrente. Leggi il file `output.md` della cartella precedente `../00_Brief/`. Leggi i file di riferimento elencati nei metadati del CONTEXT.md".

Specificare l'input in modo esplicito serve a due scopi. Riduce il consumo di token perché l'agente carica **solo** i file rilevanti invece di scansionare l'intero workspace. E rende il comportamento **deterministic**: due esecuzioni successive con gli stessi file di input produrranno output comparabili, facilitando il debugging e l'auditing.

### Il Formato dell'Output

La quarta sezione definisce la **struttura esatta** del file che l'agente deve produrre. Questa è la sezione più sottovalutata e più critica dell'intero `IDENTITY.md`. Se l'agente nella cartella `01_Ricerca` produce un file di testo libero senza struttura, l'agente nella cartella `02_Analisi` dovrà spendere token per interpretare quel testo prima di poterlo analizzare. Se invece l'output della ricerca è un file Markdown con sezioni H2 fisse (`## Fonti Trovate`, `## Dati Estratti`, `## Lacune Informative`), l'agente di analisi può navigarlo programmaticamente.

Il formato dell'output deve specificare il **nome del file** (`output.md`, `dossier_ricerca.md`), la **struttura delle sezioni** (quali H2 sono obbligatori), il **formato dei dati** (tabelle Markdown per dati tabulari, blocchi di codice per JSON, prosa continua per l'analisi qualitativa), e le **condizioni di completezza** (ogni fonte deve includere URL e data di accesso; ogni dato estratto deve citare la fonte di provenienza).

### I Criteri di Successo

La quinta sezione definisce quando il lavoro dell'agente è **completo**. Senza criteri di successo espliciti, l'agente non sa quando fermarsi: potrebbe continuare a cercare fonti all'infinito (nella cartella di ricerca) o continuare a raffinare il testo all'infinito (nella cartella di redazione). I criteri di successo trasformano un loop potenzialmente infinito in un task con una condizione di terminazione chiara.

I criteri devono essere **verificabili oggettivamente**. "Il report è di buona qualità" non è un criterio verificabile. "Il report contiene almeno 5 fonti verificate, nessuna delle quali più vecchia di 12 mesi, e ogni affermazione è supportata da almeno una citazione" è un criterio che l'agente (o un agente verificatore nella cartella successiva) può controllare meccanicamente.

### I Permessi sui Tool

L'ultima sezione elenca i server [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) (il protocollo aperto creato da [Anthropic](https://www.anthropic.com/) per standardizzare la connessione tra agenti AI e tool esterni) che l'agente è autorizzato a utilizzare. Un agente nella cartella di ricerca potrebbe avere accesso al server MCP di [Agent-Reach](https://github.com/Panniantong/Agent-Reach) (per la ricerca web), al file system MCP (per leggere le note Obsidian) e al server MCP di ricerca semantica (per trovare documenti concettualmente simili). Un agente nella cartella di redazione potrebbe avere accesso **solo** al file system MCP, impedendogli di fare ricerche web che distrarrebbero dalla scrittura.

La restrizione dei tool per stadio implementa il principio della **superficie minima di attacco**: se un agente è compromesso da una prompt injection presente in un documento web, i danni sono limitati ai soli tool che ha a disposizione.

## Anatomia di un File CONTEXT.md

Mentre l'`IDENTITY.md` definisce **chi è** l'agente (e rimane stabile tra esecuzioni diverse dello stesso stadio), il `CONTEXT.md` definisce **cosa deve fare adesso** e cambia per ogni specifico task.

Il **CONTEXT.md** contiene l'obiettivo specifico del task in linguaggio naturale ("Compila un dossier sulle partecipazioni societarie dell'azienda X"), i **criteri di accettazione** che devono essere soddisfatti perché l'output sia considerato completo ("Il dossier deve includere la struttura societaria fino al secondo livello, con percentuali di partecipazione e date di ultima modifica"), i **materiali di riferimento** che l'agente deve consultare (link a file specifici della Knowledge Base, a note Obsidian, o a documenti prodotti da cartelle precedenti), e i **vincoli di budget** (numero massimo di token da consumare, timeout, numero massimo di iterazioni di retry).

La separazione tra IDENTITY.md e CONTEXT.md è una decisione architetturale deliberata. L'identità è il **ruolo permanente** dell'agente in quella posizione della pipeline: il ricercatore resta ricercatore indipendentemente dal task. Il contesto è la **missione specifica**: oggi il ricercatore deve indagare sull'azienda X, domani sull'azienda Y. Cambia il CONTEXT.md, non l'IDENTITY.md.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D19-ingegneria-delle-identita. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Il Walk Test: La Prova di Fuoco

Lo strumento [icm-architect](https://github.com/RinDig/icm-architect) di [Jake Van Clief](https://github.com/RinDig) introduce una procedura di validazione chiamata **Walk Test** che rappresenta il collaudo supremo di un workspace ICM. Il test consiste nel rilasciare nella cartella del progetto un agente **freddo** — un'istanza del modello senza alcuna memoria delle conversazioni precedenti, senza contesto implicito, senza istruzioni verbali — e verificare se riesce a orientarsi, comprendere il suo ruolo, eseguire il task e produrre un output conforme basandosi **esclusivamente** sui file Markdown presenti nella cartella.

Se il Walk Test fallisce — se l'agente freddo non capisce cosa deve fare, quale file deve leggere, o dove deve scrivere l'output — la struttura del workspace ha fallito. Non è un problema del modello: è un problema dell'ingegneria dell'identità. I file `IDENTITY.md` e `CONTEXT.md` non sono sufficientemente espliciti, o mancano informazioni che l'utente umano teneva nella propria testa senza averle mai scritte.

Il Walk Test è un filtro spietato contro il "bias dell'autore": il progettista del workspace conosce implicitamente decine di dettagli (dove sono i file, come si chiama l'output, cosa significa "qualità accettabile") che non ha mai esplicitato nei file di identità. L'agente freddo non ha accesso a nessuna di queste informazioni implicite, e il suo fallimento rivela esattamente dove l'esplicitazione è carente.

La procedura di Walk Test si esegue in tre passaggi. Il primo è il **test di orientamento**: l'agente freddo riceve solo l'istruzione "Leggi i file nella cartella corrente e dimmi cosa devi fare". Se non riesce a rispondere in modo preciso, l'IDENTITY.md o il CONTEXT.md mancano di chiarezza. Il secondo è il **test di esecuzione**: l'agente tenta di eseguire il task descritto. Se si blocca perché non sa quale tool usare o dove trovare i dati di input, i permessi o i riferimenti sono insufficienti. Il terzo è il **test di conformità**: l'output prodotto viene confrontato con i criteri di accettazione. Se non è conforme, i criteri non sono formulati in modo che il modello possa verificarli autonomamente.

## Il Principio della Tassonomia dei Ruoli

Lo strumento [icm-architect](https://github.com/RinDig/icm-architect) introduce anche una **tassonomia dei file** all'interno del workspace ICM che aiuta a mantenere ordine quando il progetto cresce. Ogni file del workspace viene classificato in una delle seguenti categorie funzionali.

I file **Catalog** sono i file di routing stabili che collegano le parti del sistema senza contenere informazioni operative. L'`IDENTITY.md` è un file Catalog: definisce il ruolo ma non contiene dati del task. I file **Contract** specificano i vincoli e i criteri: il `CONTEXT.md` con i suoi criteri di accettazione è un file Contract. I file **Factory** sono quelli che l'agente crea durante l'esecuzione: l'output della ricerca, la bozza dell'analisi, il report finale. I file **Product** sono gli artefatti finali approvati dall'umano e pronti per la pubblicazione o il passaggio allo stadio successivo. I file **Dead** sono artefatti obsoleti, tentativi falliti o versioni superate che vengono conservati per auditabilità ma non partecipano più al flusso attivo.

Questa tassonomia è invisibile all'utente casuale — non richiede tag o metadati speciali nei file — ma è fondamentale per l'agente che deve capire quali file leggere (Catalog e Contract), quali file sono il suo output atteso (Factory che diventeranno Product), e quali file può ignorare (Dead).

## Contro-Indicazioni e Limiti

L'Ingegneria delle Identità presenta rischi reali se applicata in modo dogmatico.

Un'identità **iper-vincolata** può impedire all'agente di risolvere problemi imprevisti. Se l'IDENTITY.md del ricercatore specifica "Usa solo il tool di ricerca web" e la fonte web è temporaneamente irraggiungibile, l'agente non ha la flessibilità di tentare una ricerca alternativa tramite un database locale. La soluzione è includere nei vincoli una clausola di **fallback esplicito**: "Se il tool primario fallisce dopo 3 tentativi, scrivi nel file di output il messaggio STATUS: BLOCKED con la motivazione, e termina l'esecuzione per intervento umano".

Un'identità **sotto-vincolata** produce l'effetto opposto. Un agente con istruzioni vaghe ("Fai un'analisi approfondita") interpreterà "approfondita" secondo la propria tendenza statistica, producendo talvolta output di tre paragrafi e talvolta monografie di cento pagine. La mancanza di vincoli sull'output rende il risultato imprevedibile e incompatibile con gli stadi successivi della pipeline.

Un rischio meno ovvio è la **fossilizzazione dell'identità**. Se l'IDENTITY.md viene scritto una volta e mai aggiornato, diventa progressivamente disallineato rispetto alle capacità del modello sottostante. I modelli del 2026 hanno capacità di ragionamento, output strutturato e gestione del contesto lungo che i modelli del 2024 non avevano. Un'identità scritta per un modello meno capace potrebbe contenere istruzioni ridondanti ("Ragiona passo dopo passo prima di rispondere") che con i modelli attuali producono output verboso senza migliorare la qualità.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Laboratorio 1 — Generatore di Template IDENTITY.md

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



Questo laboratorio crea un generatore automatico di file `IDENTITY.md` che produce template strutturati con tutte le sezioni necessarie, pronte per essere personalizzate.

```python
"""
lab_identity_generator.py
Genera un file IDENTITY.md strutturato con tutte le sezioni
richieste dalla metodologia ICM di Jake Van Clief.
"""
import pathlib, textwrap, datetime

def generate_identity(
    role: str,
    domain: str,
    constraints: list[str],
    input_files: list[str],
    output_format: dict,
    success_criteria: list[str],
    tools_allowed: list[str],
    output_path: str = "IDENTITY.md"
) -> str:
    """
    Genera un IDENTITY.md completo e strutturato.

    Args:
        role: Descrizione del ruolo dell'agente
        domain: Dominio di competenza
        constraints: Lista dei vincoli negativi
        input_files: File che l'agente deve leggere
        output_format: Dict con nome_file, sezioni, formato_dati
        success_criteria: Criteri di completamento
        tools_allowed: Server MCP autorizzati
        output_path: Percorso del file di output
    """
    sections = []

    # --- Sezione 1: Ruolo ---
    sections.append(f"# Identità dell'Agente\n")
    sections.append(f"## Ruolo\n")
    sections.append(f"{role}\n")
    sections.append(f"**Dominio di competenza:** {domain}\n")

    # --- Sezione 2: Vincoli ---
    sections.append(f"\n## Vincoli Operativi\n")
    for i, constraint in enumerate(constraints, 1):
        sections.append(f"**Vincolo {i}.** {constraint}\n")

    # --- Sezione 3: Input ---
    sections.append(f"\n## Specifica dell'Input\n")
    sections.append("Prima di iniziare il lavoro, leggi i seguenti file:\n")
    for f in input_files:
        sections.append(f"- `{f}`")
    sections.append("")

    # --- Sezione 4: Formato Output ---
    sections.append(f"\n## Formato dell'Output\n")
    sections.append(
        f"Produci un file chiamato `{output_format.get('filename', 'output.md')}`"
        f" nella sotto-cartella `output/` della cartella corrente.\n"
    )
    if "sections" in output_format:
        sections.append("Il file deve contenere le seguenti sezioni:\n")
        for s in output_format["sections"]:
            sections.append(f"- `## {s}`")
        sections.append("")
    if "data_format" in output_format:
        sections.append(
            f"\n**Formato dei dati:** {output_format['data_format']}\n"
        )

    # --- Sezione 5: Criteri di Successo ---
    sections.append(f"\n## Criteri di Successo\n")
    sections.append(
        "Il lavoro è considerato completo quando TUTTI i seguenti "
        "criteri sono soddisfatti:\n"
    )
    for i, criterion in enumerate(success_criteria, 1):
        sections.append(f"**{i}.** {criterion}\n")

    # --- Sezione 6: Tool MCP ---
    sections.append(f"\n## Tool MCP Autorizzati\n")
    if tools_allowed:
        sections.append(
            "I seguenti server MCP sono disponibili per questo stadio:\n"
        )
        for tool in tools_allowed:
            sections.append(f"- `{tool}`")
        sections.append(
            "\n**Qualsiasi tool non elencato sopra è vietato.**\n"
        )
    else:
        sections.append(
            "Nessun tool esterno è autorizzato. Opera esclusivamente "
            "sui file locali.\n"
        )

    # --- Metadata ---
    sections.append(f"\n---\n")
    sections.append(
        f"*Generato il {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} "
        f"da lab_identity_generator.py*\n"
    )

    content = "\n".join(sections)

    # Salva su disco
    path = pathlib.Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"IDENTITY.md generato: {path.resolve()} ({len(content)} byte)")

    return content


# --- Esempio d'uso ---
if __name__ == "__main__":
    content = generate_identity(
        role=(
            "Sei un analista OSINT specializzato in fonti aperte italiane. "
            "La tua competenza copre la ricerca su registri pubblici "
            "(Camera di Commercio, catasto, WHOIS), la verifica di identità "
            "aziendali e l'analisi di domini web."
        ),
        domain="Intelligence da fonti aperte (OSINT) - Registri italiani",
        constraints=[
            "Non inventare dati che non trovi nelle fonti fornite.",
            "Non contattare fonti esterne se non tramite i tool MCP elencati.",
            "Non formulare giudizi, valutazioni o raccomandazioni.",
            "Non modificare file al di fuori della cartella corrente.",
            "Se un tool fallisce dopo 3 tentativi, scrivi STATUS: BLOCKED "
            "nel file di output con la motivazione e termina."
        ],
        input_files=[
            "CONTEXT.md",
            "../00_Brief/output/brief.md"
        ],
        output_format={
            "filename": "dossier_ricerca.md",
            "sections": [
                "Fonti Consultate",
                "Dati Estratti",
                "Lacune Informative",
                "Stato Finale"
            ],
            "data_format": (
                "Tabelle Markdown per dati tabulari. "
                "Ogni dato deve citare la fonte con URL e data di accesso."
            )
        },
        success_criteria=[
            "Almeno 5 fonti verificate sono state consultate.",
            "Nessuna fonte è più vecchia di 12 mesi.",
            "Ogni affermazione nel dossier è supportata da almeno una citazione.",
            "La sezione 'Lacune Informative' elenca esplicitamente "
            "i dati che non è stato possibile reperire."
        ],
        tools_allowed=[
            "agent-reach (ricerca web e scraping)",
            "file_system (lettura/scrittura file locali)",
            "obsidian_graph (navigazione backlink Knowledge Base)"
        ],
        output_path="demo_workspace/01_Ricerca/IDENTITY.md"
    )
    print("\n=== Anteprima ===")
    print(content[:800])
```

## Laboratorio 2 — Validatore di IDENTITY.md

Questo secondo laboratorio implementa un validatore che controlla se un file `IDENTITY.md` contiene tutte le sezioni richieste dalla metodologia ICM e segnala le carenze.

```python
"""
lab_identity_validator.py
Valida un file IDENTITY.md verificando la presenza di tutte
le sezioni obbligatorie secondo la metodologia ICM.
"""
import pathlib, re, sys

REQUIRED_SECTIONS = {
    "ruolo": {
        "patterns": [r"##\s*ruolo", r"##\s*role", r"##\s*identit"],
        "description": "Definizione del ruolo e delle competenze"
    },
    "vincoli": {
        "patterns": [r"##\s*vincol", r"##\s*constraint", r"##\s*restrizioni"],
        "description": "Vincoli operativi (cosa NON deve fare)"
    },
    "input": {
        "patterns": [r"##\s*input", r"##\s*specifica.*input", r"##\s*file.*leggere"],
        "description": "Elenco dei file che l'agente deve leggere"
    },
    "output": {
        "patterns": [r"##\s*output", r"##\s*formato.*output", r"##\s*deliverable"],
        "description": "Formato e struttura del file di output"
    },
    "criteri": {
        "patterns": [r"##\s*criteri", r"##\s*success", r"##\s*completamento"],
        "description": "Criteri verificabili di completamento"
    },
    "tool": {
        "patterns": [r"##\s*tool", r"##\s*mcp", r"##\s*strumenti"],
        "description": "Permessi sui tool MCP autorizzati"
    }
}

def validate_identity(filepath: str) -> dict:
    """
    Valida un file IDENTITY.md e restituisce un report strutturato.
    """
    path = pathlib.Path(filepath)
    if not path.exists():
        return {"valid": False, "error": f"File non trovato: {filepath}"}

    content = path.read_text(encoding="utf-8").lower()
    report = {
        "filepath": str(path.resolve()),
        "total_lines": content.count("\n") + 1,
        "total_bytes": len(content),
        "sections_found": [],
        "sections_missing": [],
        "warnings": [],
        "valid": True
    }

    # Controlla ogni sezione obbligatoria
    for section_id, spec in REQUIRED_SECTIONS.items():
        found = any(
            re.search(pat, content, re.IGNORECASE)
            for pat in spec["patterns"]
        )
        if found:
            report["sections_found"].append(
                {"id": section_id, "description": spec["description"]}
            )
        else:
            report["sections_missing"].append(
                {"id": section_id, "description": spec["description"]}
            )
            report["valid"] = False

    # Warning: file troppo corto
    if report["total_lines"] < 20:
        report["warnings"].append(
            "Il file ha meno di 20 righe. Un IDENTITY.md completo "
            "dovrebbe avere almeno 30-50 righe."
        )

    # Warning: nessun vincolo negativo esplicito
    negative_markers = ["non deve", "non può", "vietato", "proibito",
                        "must not", "forbidden"]
    if not any(m in content for m in negative_markers):
        report["warnings"].append(
            "Nessun vincolo negativo esplicito trovato. "
            "Un IDENTITY.md robusto deve specificare cosa l'agente "
            "NON deve fare."
        )

    # Warning: nessun file di output specificato
    if "output" not in content or ".md" not in content:
        report["warnings"].append(
            "Non è specificato un nome file per l'output (es. output.md). "
            "L'agente non saprà dove salvare il risultato."
        )

    return report

def print_report(report: dict) -> None:
    """Stampa il report di validazione in formato leggibile."""
    status = "VALIDO" if report["valid"] else "NON VALIDO"
    print(f"\n{'='*60}")
    print(f"VALIDAZIONE IDENTITY.md — {status}")
    print(f"{'='*60}")
    print(f"File: {report.get('filepath', 'N/A')}")
    print(f"Righe: {report.get('total_lines', 0)} | "
          f"Byte: {report.get('total_bytes', 0)}")

    if report["sections_found"]:
        print(f"\n  Sezioni trovate ({len(report['sections_found'])}):")
        for s in report["sections_found"]:
            print(f"    [OK] {s['id']}: {s['description']}")

    if report["sections_missing"]:
        print(f"\n  Sezioni MANCANTI ({len(report['sections_missing'])}):")
        for s in report["sections_missing"]:
            print(f"    [!!] {s['id']}: {s['description']}")

    if report["warnings"]:
        print(f"\n  Avvertimenti ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"    [??] {w}")

    print(f"\n{'='*60}\n")

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "demo_workspace/01_Ricerca/IDENTITY.md"
        print(f"Uso: python {sys.argv[0]} <percorso_identity.md>")
        print(f"Esempio con file di default: {target}\n")

    result = validate_identity(target)
    print_report(result)
```

## Laboratorio 3 — Tre Identità per lo Stesso Problema

Questo terzo laboratorio dimostra come lo **stesso problema** (analizzare un'azienda) produce output radicalmente diversi a seconda dell'identità assegnata all'agente. Vengono generate tre identità per tre stadi diversi: Ricercatore, Analista ed Editore.

```python
"""
lab_three_identities.py
Dimostra come la stessa domanda produce output radicalmente diversi
a seconda dell'IDENTITY.md assegnato all'agente.
Genera tre file IDENTITY.md per tre stadi ICM.
"""
import pathlib, json

IDENTITIES = {
    "01_Ricerca": {
        "role": (
            "Sei un raccoglitore di dati da fonti aperte. "
            "Il tuo compito è trovare e documentare FATTI verificabili, "
            "senza interpretarli, giudicarli o sintetizzarli."
        ),
        "constraints": [
            "NON formulare ipotesi, giudizi o interpretazioni.",
            "NON omettere fonti trovate, anche se sembrano irrilevanti.",
            "NON modificare o parafrasare i dati estratti: cita testualmente.",
            "Se una fonte è inaccessibile, documentalo esplicitamente."
        ],
        "output_file": "dati_grezzi.md",
        "output_sections": [
            "Fonti Consultate (URL, data accesso)",
            "Dati Estratti (citazioni testuali)",
            "Fonti Inaccessibili"
        ],
        "success": "Almeno 8 fonti consultate. Zero interpretazioni nel testo.",
        "tools": ["agent-reach", "file_system"]
    },
    "02_Analisi": {
        "role": (
            "Sei un analista investigativo. Il tuo compito è leggere "
            "i dati grezzi raccolti nello stadio precedente e identificare "
            "pattern, anomalie, connessioni e contraddizioni."
        ),
        "constraints": [
            "NON fare ricerche esterne: lavora SOLO sui dati forniti.",
            "NON formulare raccomandazioni operative.",
            "Ogni affermazione analitica deve citare il dato grezzo di origine.",
            "Le ipotesi devono essere etichettate come IPOTESI, non come fatti."
        ],
        "output_file": "analisi.md",
        "output_sections": [
            "Sintesi Esecutiva (max 200 parole)",
            "Pattern Identificati",
            "Anomalie e Contraddizioni",
            "Ipotesi Investigative (etichettate come tali)",
            "Lacune Informative"
        ],
        "success": "Ogni pattern cita almeno 2 dati grezzi a supporto.",
        "tools": ["file_system"]
    },
    "03_Redazione": {
        "role": (
            "Sei un redattore tecnico specializzato in report investigativi. "
            "Il tuo compito è trasformare l'analisi grezza in un documento "
            "professionale, leggibile e pronto per la presentazione."
        ),
        "constraints": [
            "NON aggiungere informazioni che non compaiono nell'analisi.",
            "NON fare ricerche esterne.",
            "NON utilizzare elenchi puntati: scrivi prosa continua.",
            "Mantieni un registro formale e neutro (NPOV)."
        ],
        "output_file": "report_finale.md",
        "output_sections": [
            "Sommario Direzionale",
            "Profilo del Soggetto",
            "Struttura Societaria",
            "Indicatori di Rischio",
            "Conclusioni e Prossimi Passi"
        ],
        "success": "Zero elenchi puntati. Ogni sezione è prosa continua.",
        "tools": ["file_system"]
    }
}

def generate_all_identities(base_dir: str = "demo_pipeline"):
    """Genera i tre IDENTITY.md per i tre stadi."""
    base = pathlib.Path(base_dir)

    for folder_name, spec in IDENTITIES.items():
        folder = base / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# Identità dell'Agente — {folder_name}\n",
            f"## Ruolo\n",
            f"{spec['role']}\n",
            f"\n## Vincoli Operativi\n"
        ]
        for i, c in enumerate(spec["constraints"], 1):
            lines.append(f"**{i}.** {c}\n")

        lines.extend([
            f"\n## Input\n",
            f"Leggi il file `CONTEXT.md` della cartella corrente.\n"
        ])
        if folder_name != "01_Ricerca":
            prev_num = int(folder_name[:2]) - 1
            prev_folder = [k for k in IDENTITIES if k.startswith(f"{prev_num:02d}")][0]
            prev_output = IDENTITIES[prev_folder]["output_file"]
            lines.append(
                f"Leggi il file `../{prev_folder}/output/{prev_output}`.\n"
            )

        lines.extend([
            f"\n## Formato Output\n",
            f"Produci il file `output/{spec['output_file']}` con le sezioni:\n"
        ])
        for s in spec["output_sections"]:
            lines.append(f"- `## {s}`")
        lines.append("")

        lines.extend([
            f"\n## Criteri di Successo\n",
            f"{spec['success']}\n",
            f"\n## Tool MCP Autorizzati\n"
        ])
        for t in spec["tools"]:
            lines.append(f"- `{t}`")
        lines.append(
            "\n\n**Qualsiasi tool non elencato è vietato.**\n"
        )

        identity_path = folder / "IDENTITY.md"
        identity_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Generato: {identity_path}")

    # Genera anche i CONTEXT.md vuoti
    for folder_name in IDENTITIES:
        ctx_path = base / folder_name / "CONTEXT.md"
        ctx_path.write_text(
            "# Contesto del Task\n\n"
            "## Obiettivo\n\n[INSERIRE L'OBIETTIVO SPECIFICO]\n\n"
            "## Criteri di Accettazione\n\n[INSERIRE I CRITERI]\n\n"
            "## Materiali di Riferimento\n\n[LINK A FILE DELLA KB]\n\n"
            "## Budget\n\nToken massimi: 50000\n"
            "Iterazioni massime: 5\n",
            encoding="utf-8"
        )
        print(f"Generato: {ctx_path}")

if __name__ == "__main__":
    generate_all_identities()
    print("\n=== Pipeline ICM generata in demo_pipeline/ ===")
    print("Esegui il Walk Test: lancia un agente freddo nella cartella")
    print("01_Ricerca e verifica se riesce a orientarsi autonomamente.")
```

Il laboratorio genera una pipeline completa di tre cartelle ICM con identità progressivamente specializzate. Il Ricercatore raccoglie dati grezzi senza interpretarli; l'Analista identifica pattern e anomalie senza fare ricerche esterne; il Redattore trasforma l'analisi in prosa professionale senza aggiungere informazioni. Ogni agente ha accesso solo ai tool strettamente necessari al suo stadio, e l'output di ogni stadio diventa l'input dello stadio successivo attraverso il file system.
