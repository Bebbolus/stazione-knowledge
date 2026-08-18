# Il Manifesto dell'Apprendimento (Versione Definitiva Unificata)

Questo manifesto definisce le regole architetturali, narrative e stilistiche per la stesura di materiale didattico e note tecniche. È ottimizzato per l'apprendimento degli adulti, la riduzione del carico cognitivo (ADHD-friendly) e la massima profondità ingegneristica.

### 1. Architettura della Nota (MoSS + Inverted Pyramid)
*   **Titoli e Alias:** Il titolo principale (H1) utilizza sempre il termine più affermato in letteratura. I sinonimi devono essere inseriti negli alias YAML per evitare la frammentazione del knowledge graph.
*   **Monografia Autoconclusiva:** Ogni singola nota deve funzionare in modo indipendente e fornire un quadro completo senza dipendere rigidamente da file esterni.
*   **Piramide Rovesciata (Densità Immediata):** Il primissimo paragrafo del documento (immediatamente sotto l'H1) contiene la **definizione massima e densa**. Il lettore deve potervi estrarre immediatamente tre risposte: COS'È, DOVE SI USA e PERCHÉ ESISTE. 

### 2. Struttura Narrativa (McKinsey + Problem-Driven)
*   **Apertura SCQA:** Una volta fornita la definizione densa, il contesto si sviluppa secondo lo schema logico: *Situation* (Status quo) -> *Complication* (Il problema insorto) -> *Question* (Qual è la sfida da risolvere?) -> *Answer* (L'introduzione della soluzione).
*   **Evoluzione Logica (Dialettica):** La progressione dei concetti non è mai casuale ma guidata dai problemi. Si segue la formula: *Soluzione precedente -> Nuovi limiti o costi introdotti -> Nuova soluzione*. I limiti di una tecnologia fungono da "gancio" narrativo per introdurre l'argomento successivo.
*   **MECE (Mutually Exclusive, Collectively Exhaustive):** Qualsiasi classificazione o tassonomia (es. tipologie di database, architetture di rete) deve essere strutturata in categorie che non si sovrappongono e che, sommate, coprono l'intero perimetro dell'argomento.

### 3. Rigore Ingegneristico (Kleppmann + Karpathy)
*   **Demistificazione (Approccio Karpathy):** Sono vietate le spiegazioni basate su "scatole magiche" o metafore puramente astratte. È obbligatorio spiegare cosa avviene a livello di dato grezzo (es. "L'embedding è un array di 768 numeri decimali. La semantica è calcolata tramite la distanza matematica tra array").
*   **Trade-offs over Truths (Approccio Kleppmann):** Nessuna tecnologia è considerata una "pallottola d'argento". È obbligatorio esplicitare i costi operativi (es. Latenza vs Throughput, Costo vs Accuratezza) e descrivere dettagliatamente gli *use-case* in cui la soluzione fallisce o è controproducente.
*   **Operational Neutrality (NPOV):** Sono vietate prese di posizione personali o esortative ("Noi dovremmo", "È fondamentale"). Il testo riporta i fatti, i compromessi e lo stato del dibattito industriale in modo rigorosamente oggettivo.

### 4. Anti-Slop e Carico Cognitivo (Stile Feynman + Ottimizzazione ADHD)
*   **Titoli e Sottotitoli Obbligatori:** Ogni sezione o blocco logico di paragrafi deve essere introdotto da un titolo esplicito (H2) e, ove utile, da un sottotitolo (H3) per dichiararne immediatamente il focus, facilitando la creazione di una mappa mentale e la scansione visiva della pagina.
*   **Soglia degli Elenchi Puntati (Max 10%):** L'informazione deve viaggiare su **prosa continua e argomentativa**. L'utilizzo di elenchi puntati è tollerato per un massimo del 10% delle righe totali del documento e non deve mai costituire lo scheletro della spiegazione.
*   **Semplicità Radicale:** Utilizzo sistematico di verbi d'azione concreti. È vietato l'uso del burocratese, delle nominalizzazioni eccessive e degli "arzigogoli" accademici che appesantiscono la lettura senza aggiungere precisione tecnica.
*   **Formattazione per la Scansione:** La prosa deve essere suddivisa in micro-paragrafi densi (massimo 3-4 frasi ciascuno). Il grassetto semantico deve essere usato in modo tattico per ancorare l'occhio ai concetti chiave durante la lettura veloce.
*   **Ban delle Emoji:** Vige il divieto assoluto di utilizzo di emoji nel corpo enciclopedico del testo (sono ammesse esclusivamente come icone strutturali di cartelle o macro-categorie nel frontend).

### 5. Preservazione e Refactoring dell'Informazione (No Data Loss)
*   **Invarianza del Carico Informativo:** Durante la riscrittura o il refactoring di documenti preesistenti, è severamente vietato omettere o scartare porzioni di conoscenza (risorse esterne, bibliografia, link di approfondimento, log operativi o laboratori pratici) già presenti nell'originale.
*   **Adattamento Strutturale:** Il materiale di approfondimento e i link testuali preesistenti devono essere preservati e ri-formattati per aderire alle regole del manifesto (ad esempio trasformando lunghe liste di link in paragrafi di prosa densa e narrativamente coesa, nel rigoroso rispetto della soglia del 10% per gli elenchi puntati).
