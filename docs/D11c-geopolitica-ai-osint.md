---
aliases: [D11c, Geopolitica dell'AI, Semiconductor Chokepoints, Governance AI, Export Controls]
---

# Geopolitica dell'AI, Supply Chain dei Semiconduttori e Governance Globale

La geopolitica dell'intelligenza artificiale e la governance della supply chain dei semiconduttori costituiscono il dominio interdisciplinare che analizza l'intersezione strategica tra i colli di bottiglia fisici della microelettronica avanzata, i regimi multilaterali di controllo delle esportazioni e i quadri normativi per la sicurezza dei modelli computazionali. Questa disciplina si applica nell'intelligence delle minacce OSINT, nella valutazione della resilienza delle catene di approvvigionamento tecnologico e nella progettazione di infrastrutture di calcolo sovrane per la difesa e la sicurezza nazionale. Il quadro esiste per demistificare l'illusione di un'AI puramente immateriale, evidenziando come la concentrazione monopolistica di macchinari litografici a ultravioletti estremi, fonderie insulari e architetture GPU definisca le asimmetrie di potere economico e determini chi possa addestrare o eseguire modelli di frontiera.

## I colli di bottiglia fisici del calcolo: dalla litografia EUV alle fonderie avanzate

L'infrastruttura dell'intelligenza artificiale contemporanea poggia su una catena del valore altamente centralizzata e vulnerabile, vincolata da estreme complessità fisiche, termodinamiche e ottiche. Sebbene i modelli generativi vengano percepiti come entità algoritmiche astratte, la loro esistenza dipende dalla capacità di fabbricare microprocessori contenenti decine di miliardi di transistor su scala nanometrica, un processo industriale che vede la presenza di monopoli tecnologici assoluti.

Il passaggio ai nodi produttivi avanzati (sotto i 7 nanometri) è reso possibile in via esclusiva dai macchinari di litografia a ultravioletti estremi (EUV) sviluppati da [ASML](https://www.asml.com/) (l'azienda olandese fornitrice esclusiva globale di macchinari litografici a ultravioletti estremi per la produzione di microchip). Questi apparati operano generando luce a una lunghezza d'onda di appena 13,5 nanometri mediante l'irradiazione con laser CO2 ad altissima potenza di cinquantamila gocce di stagno fuso al secondo, riflesse da specchi di Bragg a deposizione atomica multistrato realizzati da [Carl Zeiss](https://www.zeiss.com/) (l'azienda ottica tedesca leader mondiale nelle ottiche di precisione) e integrate con camere a vuoto e sistemi di incisione al plasma forniti da [Tokyo Electron](https://www.tel.com/) (la multinazionale giapponese leader nelle apparecchiature industriali per la fabbricazione di semiconduttori). Ciascuno scanner EUV richiede anni di produzione, costa centinaia di milioni di dollari e impiega migliaia di componenti specializzati provenienti da una filiera globale non duplicabile nel breve periodo.

```
+-------------------------------------------------------------------------+
|              COLLI DI BOTTIGLIA NELLA SUPPLY CHAIN DEI CHIP AI          |
+-------------------------------------------------------------------------+
| [ Ottiche di Precisione Zeiss ] + [ Laser a Plasma Stagno CO2 ]         |
|                                |                                        |
|                                v                                        |
| [ Monopolio Litografia EUV: ASML (Paesi Bassi) ]                        |
|                                |                                        |
|                                v                                        |
| [ Fonderie Avanzate sub-3nm & Packaging CoWoS: TSMC (Taiwan) ]          |
|                                |                                        |
|                                v                                        |
| [ Progettazione Architetture GPU AI: NVIDIA (Stati Uniti) ]             |
|                                |                                        |
|                                v                                        |
| [ Addestramento Modelli di Frontiera & Hyperscaler Cloud Globali ]      |
+-------------------------------------------------------------------------+
```

La fabbricazione effettiva dei die logici e l'integrazione con le memorie ad alta banda (HBM3e) si concentra prevalentemente nell'isola di Taiwan presso gli stabilimenti di [TSMC](https://www.tsmc.com/) (la fonderia indipendente taiwanese leader mondiale nella fabbricazione di semiconduttori avanzati), in particolare nella Fab 18 di Tainan e nel distretto di Hsinchu. Oltre alla litografia primaria, il principale collo di bottiglia fisico risiede nel packaging avanzato Chip-on-Wafer-on-Substrate (CoWoS), indispensabile per connettere la GPU logica con i moduli di memoria a bassissima latenza. Questa concentrazione geografica attorno allo Stretto di Taiwan crea una vulnerabilità sistemica definita "scudo di silicio", in cui una perturbazione geopolitica o marittima interromperebbe istantaneamente la fornitura mondiale di acceleratori AI, superando per impatto economico qualsiasi precedente crisi energetica.

Sebbene competitor storici come [Intel](https://www.intel.com/) (la multinazionale produttrice di microprocessori e infrastrutture di fonderia) stiano investendo massicciamente nello sviluppo di nodi proprietari (RibbonFET) e fonderie concorrenti come [SMIC](https://www.smics.com/) (la principale fonderia di semiconduttori cinese con sede a Shanghai) tentino di produrre chip avanzati mediante litografia DUV ad esposizione multipla (SAQP), i bassi rendimenti produttivi e i costi esorbitanti confermano l'insostituibilità dell'asse ASML-TSMC nel breve e medio termine.

## L'architettura degli export controls: meccanismi BIS, FDPR e soglie di calcolo

Per contenere l'ascesa tecnologica e militare di potenze avversarie, gli Stati Uniti hanno formalizzato un regime di controllo delle esportazioni amministrato dal [Bureau of Industry and Security](https://www.bis.doc.gov/) ([BIS](https://www.bis.doc.gov/), l'agenzia del Dipartimento del Commercio USA che amministra i controlli sulle esportazioni di tecnologie a doppio uso e chip avanzati). Le normative dell'Export Administration Regulations (EAR) impongono restrizioni severe sul trasferimento di hardware avanzato, apparecchiature litografiche e software EDA per la progettazione di circuiti integrati.

L'elemento di massima efficacia extraterritoriale è la Foreign-Produced Direct Product Rule (FDPR). Questa clausola estende la giurisdizione del governo statunitense a qualsiasi microchip o apparato tecnologico fabbricato all'estero se prodotto impiegando software di progettazione elettronica o brevetti originati negli Stati Uniti (come gli strumenti di [Synopsys](https://www.synopsys.com/) o [Cadence](https://www.cadence.com/)). L'inserimento di aziende straniere nella Entity List del BIS impedisce a fonderie terze come [TSMC](https://www.tsmc.com/) di produrre silicio per loro conto, paralizzando la capacità di scaling delle industrie sanzionate.

La formalizzazione dei controlli ha richiesto l'introduzione di metriche matematiche quantitative per delimitare gli acceleratori soggetti a embargo:

Il Total Processing Performance ($TPP$) misura la potenza computazionale grezza aggregata moltiplicando la capacità di calcolo per la larghezza dei bit del dato:

$$TPP = 2 \times \text{TFLOPS}_{\text{dense}} \times \text{bit\_width}$$

Nel regime iniziale del 2022, il BIS stabiliva il divieto per chip con $TPP \ge 4800$ o con una larghezza di banda di interconnessione bidirezionale superiore a 600 GB/s. Produttori come [NVIDIA](https://www.nvidia.com/) (la multinazionale tecnologica produttrice leader di GPU e piattaforme di calcolo accelerato per l'AI) avevano risposto ingegnerizzando versioni conformi (A800 e H800) che mantenevano inalterata la densità di calcolo riducendo l'interconnessione NVLink a 400 GB/s.

Per chiudere questa scappatoia architetturale, l'aggiornamento normativo del 2023 ha introdotto la metrica della Performance Density ($PD$), definita come il rapporto tra la prestazione totale e l'area superficiale del silicio espressa in millimetri quadrati:

$$PD = \frac{TPP}{\text{Die Area mm}^2}$$

```
                Regole di Controllo Export BIS (ECCN 3A090)
                                    |
            +-----------------------+-----------------------+
            |                                               |
     [ TPP >= 4800 ]                    [ 1600 <= TPP < 4800 ]
            |                                               |
     -> BANDO ASSOLUTO                 +------------+------------+
        (H100, A100, RTX 4090)         |                         |
                               [ PD >= 5.92 ]             [ PD < 5.92 ]
                                      |                          |
                               -> BANDO ASSOLUTO          -> Licenza / Notifica
                                  (L40S, RTX 4090D)          (NVIDIA H20)
```

In base alla nuova regola, qualsiasi processore con $TPP \ge 4800$ oppure con $1600 \le TPP < 4800$ e $PD \ge 5.92$ ricade nel divieto di esportazione automatica (ECCN 3A090.a/b), estendendo il blocco a schede grafiche enterprise e consumer come la RTX 4090. In risposta, NVIDIA ha calibrato l'acceleratore H20 con TPP ridotto ma elevata ampiezza di banda di memoria. L'analista OSINT monitora costantemente i tentativi di elusione di tali vincoli, tracciando triangolazioni commerciali attraverso società fittizie in giurisdizioni terze (come Emirati Arabi Uniti o Sud-Est asiatico) e l'accesso remoto a cluster di calcolo esteri tramite servizi cloud IaaS non conformi.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D11c-geopolitica-ai-osint. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Divergenza regolatoria: Brussels Effect, tecno-nazionalismo USA e governance cinese

Il panorama globale della governance dell'intelligenza artificiale si caratterizza per una profonda frammentazione tra blocchi geopolitici, ciascuno guidato da priorità strategiche e visioni normative divergenti.

```
+--------------------------------------------------------------------------+
|                 DIVERGENZA REGOLATORIA E GOVERNANCE DELL'AI              |
+--------------------------------------------------------------------------+
|  UNIONE EUROPEA (EU AI Act - Regolamento UE 2024/1689)                   |
|  * Approccio Basato sul Rischio a 4 Livelli (Inaccettabile, Alto, ecc.)  |
|  * Soglia di Rischio Sistemico GPAI a Calcolo Cumulativo >= 10^25 FLOPs  |
|  * Effetto Bruxelles: Spillover degli Standard di Conformità Globali     |
|                                                                          |
|  STATI UNITI (Executive Order 14110 & NIST AI RMF)                       |
|  * Obblighi di Notifica Dual-Use per Modelli di Frontiera >= 10^26 FLOPs |
|  * Procedure KYC per Provider IaaS Cloud su Clienti Esteri               |
|  * Standard Volontari NIST AI RMF (Govern, Map, Measure, Manage)         |
|                                                                          |
|  REPUBBLICA POPOLARE CINESE (Normative CAC)                              |
|  * Registrazione Obbligatoria degli Algoritmi e Controllo dei Dataset    |
|  * Allineamento Ideologico ai Valori Socialisti Fondamentali             |
|  * Tracciamento e Watermarking dei Media Generativi Sintetici            |
+--------------------------------------------------------------------------+
```

L'Unione Europea ha adottato l'[EU AI Act](https://artificialintelligenceact.eu/) (il regolamento dell'Unione Europea per la governance e la classificazione del rischio dei sistemi di intelligenza artificiale, Regolamento UE 2024/1689), istituendo una tassonomia orizzontale fondata su quattro livelli di rischio. I sistemi a rischio inaccettabile (come il social scoring e l'identificazione biometrica remota in tempo reale negli spazi pubblici, fatte salve eccezioni di sicurezza) sono categoricamente vietati. I sistemi ad alto rischio (impiegati in infrastrutture critiche, sanità, selezione del personale e giustizia) sono soggetti a rigide valutazioni di conformità ex-ante, obblighi di trasparenza, tracciabilità e supervisione umana. Per i modelli General Purpose AI (GPAI), il legislatore europeo ha stabilito una presunzione di rischio sistemico per qualsiasi modello addestrato con una capacità di calcolo cumulativa pari o superiore a $10^{25}$ FLOPs, imponendo audit di cybersicurezza, valutazioni avversarie e notifiche all'European AI Office. Questa regolamentazione genera il cosiddetto "effetto Bruxelles", costringendo le multinazionali ad adeguare i propri standard globali alle norme europee per non perdere l'accesso al mercato unico.

Negli Stati Uniti prevale un modello di tecno-nazionalismo mirato a preservare la leadership tecnologica e proteggere la sicurezza nazionale. L'Executive Order 14110 ha imposto obblighi federali di rendicontazione per modelli di frontiera addestrati con oltre $10^{26}$ FLOPs complessivi e ha introdotto requisiti di identificazione della clientela (KYC) per i provider cloud IaaS statunitensi che ospitano sviluppatori esteri. Il [NIST](https://www.nist.gov/) (il National Institute of Standards and Technology, l'agenzia governativa statunitense per la standardizzazione tecnica) fornisce quadri di gestione del rischio non vincolanti attraverso il framework NIST AI RMF 1.0, promuovendo standard di affidabilità e mitigazione del bias.

In Cina, l'amministrazione del ciberspazio (CAC) applica un modello di governance centralizzato focalizzato sulla stabilità politica e sul controllo delle informazioni. I regolamenti per la sintesi profonda e i servizi generativi impongono la registrazione obbligatoria degli algoritmi, l'allineamento dei contenuti ai valori socialisti fondamentali e la verifica dell'autenticità dei dataset di addestramento.

In risposta a queste divergenze, i singoli stati sviluppano iniziative di "AI sovrana", investendo in centri di supercalcolo pubblici per garantire indipendenza tecnologica. In ambito europeo spiccano le infrastrutture EuroHPC come Cineca Leonardo in Italia, MareNostrum 5 in Spagna e LUMI in Finlandia, affiancate dallo sviluppo di modelli linguistici sovrani promossi da realtà quali [Mistral](https://mistral.ai/) e [Aleph Alpha](https://aleph-alpha.com/), dal modello Falcon negli Emirati Arabi Uniti e dalle famiglie aperte Qwen rilasciate da [Alibaba](https://www.alibaba.com/) (il conglomerato tecnologico multinazionale cinese attivo nel cloud computing e modelli linguistici Qwen).

## Attribution forense e supply chain OSINT dei modelli di frontiera

L'impiego operativo dell'intelligenza artificiale in operazioni di disinformazione e cyber warfare sponsorizzate da stati richiede metodologie specializzate per l'attribuzione delle minacce basate sull'analisi dell'impronta tecnologica dei modelli generativi.

L'attribuzione forense di un modello neurale opera esaminando quattro indicatori distintivi:

L'analisi del tokenizzatore e del vocabolario individua la struttura dell'algoritmo di segmentazione del testo (Byte-Pair Encoding o WordPiece). La presenza di token di controllo proprietari o distribuzioni lessicali ottimizzate per specifici idiomi rivela l'architettura originaria utilizzata per l'operazione di influenza.

Il profilo comportamentale e i pattern di allineamento permettono di estrarre le direttive del prompt di sistema originario e i limiti di sicurezza (*guardrails*). L'invio di query provocatorie progettate per testare tabù geopolitici o argomenti sensibili consente di identificare se il modello risponde aderendo a direttive specifiche di determinati apparati statali.

La telemetria di generazione e il campionamento analizzano la temperatura, le penalità di frequenza e la perplexity del testo generato, correlandole con infrastrutture di hosting, indirizzi IP di uscita e certificati SSL/TLS degli endpoint impiegati dagli operatori avversari.

```
  [ Manufatto o Testo Sospetto ]
                |
                +---> [ Tokenizer Footprint ]  ---> Riconoscimento BPE / Vocabolario
                |
                +---> [ Behavioral Probing ]  ---> Test dei Limiti Ideologici e Guardrail
                |
                +---> [ Model Weight Audit ]  ---> Verifica SHA-256 e Formato Safetensors
                |
                +---> [ Infrastructure OSINT] ---> Mappatura IP / ASN / Certificati SSL
```

L'analista deve tuttavia considerare il rischio di operazioni sotto falsa bandiera (*false flag*), in cui un attore malevolo imita intenzionalmente lo stile linguistico o le configurazioni di un avversario per deviare le indagini. Poiché i pesi di molti modelli sono liberamente accessibili a livello globale, la sola presenza di un modello non costituisce prova definitiva di attribuzione, ma deve essere incrociata con l'analisi dei grafi relazionali e le evidenze geospaziali.

La sicurezza della supply chain dei modelli aperti impone un'ispezione rigorosa del formato di memorizzazione dei pesi. I vecchi file di checkpoint serializzati con il modulo nativo `pickle` di [Python](https://www.python.org/) (`.pt` o `.bin`) presentano gravissime vulnerabilità di esecuzione arbitraria di codice (RCE) all'atto del caricamento in memoria. La transizione verso il formato `safetensors` promosso dalla piattaforma [Hugging Face](https://huggingface.co/) (la piattaforma per modelli e dataset di machine learning) garantisce l'isolamento del codice, archiviando esclusivamente array numerici serializzati in modo immutabile con intestazione JSON descrittiva. L'integrità dei modelli viene infine certificata mediante il calcolo e il confronto degli hash crittografici SHA-256 di ciascuno shard dei pesi.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Compromessi architetturali, vincoli geopolitici e limiti etico-legali

L'investigatore e il progettista di sistemi informativi affrontano compromessi strutturali tra sovranità operativa, prestazioni computazionali e conformità giuridica.

| Dimensione | Opzione A | Opzione B | Compromesso Ingegneristico |
| :--- | :--- | :--- | :--- |
| **Modelli Open-Weight Locali vs API di Frontiera Cloud** | Esecuzione su hardware sovrano locale con pesi aperti | Chiamate API verso hyperscaler e modelli chiusi | Il modello open locale garantisce riservatezza assoluta ma richiede GPU costose; l'API cloud offre massima potenza analitica ma espone a rischi di lock-in e sorveglianza. |
| **PProcessori ad Alta Efficienza vs Vincoli di Embargo** | Chip conformi alle soglie BIS (NVIDIA H20, RTX 4090D) | Acceleratori top di gamma (H100, B200) da canali grigi | I processori conformi consentono operatività legale ma con throughput ridotto; l'hardware di contrabbando azzera il supporto ufficiale ed espone a gravi sanzioni penali. |
| **Audit della Supply Chain vs Velocità di Integrazione** | Scansione completa degli shard safetensors e audit del codice | Ingestione immediata di checkpoint pre-addestrati da hub | L'audit rigoroso previene backdoors trojan e vulnerabilità RCE ma rallenta il deployment; l'ingestione rapida espone l'infrastruttura a compromissioni silenti. |
| **Ricognizione Geopolitica vs Conformità Privacy** | Mappatura OSINT di server di calcolo e account associati | Rispetto dei perimetri normativi GDPR e policy di servizio | La raccolta informativa deve limitarsi all'osservazione passiva dei dati aperti senza sconfinare in accessi abusivi o violazioni della protezione dati personali. |

L'attività investigativa deve svolgersi nel pieno rispetto dei confini legali definiti dalle normative sulla cibersicurezza, distinguendo la legittima analisi delle fonti aperte da intrusioni non autorizzate nei sistemi di calcolo terzi, preservando la catena di custodia digitale e la trasparenza delle conclusioni analitiche.

## Riferimenti bibliografici e documentazione specialistica

### Geopolitica dei semiconduttori ed export controls

Le analisi strategiche sui colli di bottiglia delle catene del valore tecnologico sono elaborate nei report del [Center for Strategic and International Studies](https://www.csis.org/) ([CSIS](https://www.csis.org/), il think tank bipartisan statunitense di geopolitica e sicurezza internazionale) e nelle pubblicazioni dell'Institute for Human-Centered AI della [Stanford University](https://www.stanford.edu/). I regolamenti ufficiali per i controlli sulle esportazioni di acceleratori grafici avanzati e le definizioni delle categorie ECCN sono consultabili presso il [Bureau of Industry and Security](https://www.bis.doc.gov/) ([BIS](https://www.bis.doc.gov/)). La storia industriale e i monopoli fisici della microelettronica fanno riferimento alle opere e ai documenti di settore su [ASML](https://www.asml.com/), [TSMC](https://www.tsmc.com/) e [NVIDIA](https://www.nvidia.com/).

### Regolamentazione globale e governance dell'AI

Il testo normativo ufficiale e le linee guida applicative del quadro regolatorio europeo sono consultabili presso il portale dell'[EU AI Act](https://artificialintelligenceact.eu/) curato dall'European AI Office. I criteri e le metodologie di mitigazione del rischio nei sistemi intelligenti sono formalizzati nel framework AI RMF 1.0 redatto dal [NIST](https://www.nist.gov/). I modelli di regolamentazione algoritmica asiatica sono documentati nelle direttive della Cyberspace Administration of China.

### Threat intelligence e provenienza dei modelli

Le evidenze relative a campagne di disinformazione coordinate e attori di minaccia statali sono documentate nelle analisi e nei dataset aperti prodotti dal collettivo [Bellingcat](https://www.bellingcat.com/). Le specifiche per la sicurezza dei formati dei pesi computazionali e la verifica dei modelli aperti sono approfondite nella documentazione tecnica della piattaforma [Hugging Face](https://huggingface.co/). Gli standard aperti per la certificazione dei contenuti multimediali sono descritti dalle linee guida del consorzio [C2PA](https://c2pa.org/).

## Appendice operativa: laboratori pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



I seguenti quattro laboratori forniscono procedure operative e codice [Python](https://www.python.org/) eseguibile per quantificare le metriche di export control, valutare la vulnerabilità della supply chain dei semiconduttori, classificare il rischio secondo l'EU AI Act e analizzare la sicurezza binaria dei formati dei modelli.

### Laboratorio 1: Calcolo delle metriche BIS (TPP e Performance Density) per acceleratori GPU

Questo laboratorio implementa un modulo in [Python](https://www.python.org/) che calcola le metriche ufficiali del Dipartimento del Commercio USA ([BIS](https://www.bis.doc.gov/)): il Total Processing Performance ($TPP$) e la Performance Density ($PD$), valutando se un acceleratore rispetta i limiti di esportazione imposti dalle normative ECCN 3A090.

Procedura operativa:

- [ ] Definire le specifiche fisiche dell'acceleratore (TFLOPS densi a 16-bit, larghezza di bit pari a 16 e area superficiale del die in $\text{mm}^2$).
- [ ] Calcolare il $TPP$ moltiplicando $2 \times \text{TFLOPS} \times \text{bit\_width}$.
- [ ] Calcolare il $PD$ dividendo il $TPP$ per l'area del die.
- [ ] Applicare le condizioni logiche del regolamento BIS per determinare se il processore è liberamente esportabile, soggetto a notifica o vietato.

```python
from typing import Dict, Any, List

def evaluate_bis_export_compliance(gpu_spec: Dict[str, Any]) -> Dict[str, Any]:
    name = gpu_spec["name"]
    tflops = gpu_spec["dense_fp16_tflops"]
    bit_width = gpu_spec["bit_width"]
    die_area = gpu_spec["die_area_mm2"]

    # Calcolo Total Processing Performance: TPP = 2 * TFLOPS * bit_width
    tpp = 2.0 * tflops * bit_width
    # Calcolo Performance Density: PD = TPP / Die Area mm2
    pd = tpp / die_area if die_area > 0 else 0.0

    # Valutazione soglie BIS 2023 (ECCN 3A090.a / 3A090.b)
    if tpp >= 4800:
        status = "PROHIBITED_EXPORT (ECCN 3A090.a)"
        reason = "TPP >= 4800 (Supera il limite massimo assoluto di calcolo)"
    elif tpp >= 1600 and pd >= 5.92:
        status = "PROHIBITED_EXPORT (ECCN 3A090.b)"
        reason = f"TPP ({tpp:.0f}) >= 1600 e Performance Density ({pd:.2f}) >= 5.92"
    elif tpp >= 2400 and pd < 5.92:
        status = "NOTIFICATION_REQUIRED"
        reason = f"TPP ({tpp:.0f}) >= 2400 ma Performance Density ({pd:.2f}) < 5.92"
    else:
        status = "PERMITTED_EXPORT"
        reason = "Parametri inferiori a tutte le soglie di controllo export"

    return {
        "name": name,
        "tpp": round(tpp, 1),
        "performance_density": round(pd, 2),
        "export_status": status,
        "regulatory_rationale": reason
    }

if __name__ == "__main__":
    test_gpus = [
        {"name": "NVIDIA H100 SXM", "dense_fp16_tflops": 989.0, "bit_width": 16, "die_area_mm2": 814.0},
        {"name": "NVIDIA A100 SXM", "dense_fp16_tflops": 312.0, "bit_width": 16, "die_area_mm2": 826.0},
        {"name": "NVIDIA RTX 4090", "dense_fp16_tflops": 165.0, "bit_width": 16, "die_area_mm2": 608.0},
        {"name": "NVIDIA H20 (China Compliant)", "dense_fp16_tflops": 148.0, "bit_width": 16, "die_area_mm2": 814.0}
    ]

    print("[*] Valutazione Conformità Controlli Export BIS (ECCN 3A090):\n")
    for g in test_gpus:
        res = evaluate_bis_export_compliance(g)
        print(f"  - Modello: {res['name']:<25}")
        print(f"    TPP: {res['tpp']:<8} | Performance Density: {res['performance_density']:<6}")
        print(f"    Stato: {res['export_status']}")
        print(f"    Nota : {res['regulatory_rationale']}\n")
```

Output atteso dell'esecuzione:

```text
[*] Valutazione Conformità Controlli Export BIS (ECCN 3A090):

  - Modello: NVIDIA H100 SXM          
    TPP: 31648.0  | Performance Density: 38.88 
    Stato: PROHIBITED_EXPORT (ECCN 3A090.a)
    Nota : TPP >= 4800 (Supera il limite massimo assoluto di calcolo)

  - Modello: NVIDIA A100 SXM          
    TPP: 9984.0   | Performance Density: 12.09 
    Stato: PROHIBITED_EXPORT (ECCN 3A090.a)
    Nota : TPP >= 4800 (Supera il limite massimo assoluto di calcolo)

  - Modello: NVIDIA RTX 4090          
    TPP: 5280.0   | Performance Density: 8.68  
    Stato: PROHIBITED_EXPORT (ECCN 3A090.a)
    Nota : TPP >= 4800 (Supera il limite massimo assoluto di calcolo)

  - Modello: NVIDIA H20 (China Compliant)
    TPP: 4736.0   | Performance Density: 5.82  
    Stato: NOTIFICATION_REQUIRED
    Nota : TPP (4736) >= 2400 ma Performance Density (5.82) < 5.92
```

### Laboratorio 2: Mappatura topologica e analisi di resilienza della supply chain dei semiconduttori

Questo laboratorio implementa un modello a grafo in [Python](https://www.python.org/) per quantificare l'indice di concentrazione di mercato Herfindahl-Hirschman (HHI) nei diversi nodi della supply chain dei semiconduttori e simulare l'impatto a cascata generato da un'interruzione operativa delle fonderie avanzate di [TSMC](https://www.tsmc.com/).

Procedura operativa:

- [ ] Modellare i segmenti critici della filiera dei semiconduttori (Litografia EUV, Ottiche, Fonderia sub-3nm, Packaging CoWoS, EDA Software).
- [ ] Calcolare l'indice HHI per ciascun segmento per identificare mercati a concentrazione monopolistica ($\text{HHI} > 2500$).
- [ ] Simulare la propagazione di un blocco delle fonderie taiwanesi identificando le industrie e i provider cloud a valle impattati.
- [ ] Emettere il report quantitativo di vulnerabilità geopolitica.

```python
from typing import Dict, List, Any

def calculate_hhi(market_shares: List[float]) -> float:
    """Calcola l'Herfindahl-Hirschman Index (HHI) sommando i quadrati delle quote percentuali."""
    return sum(share ** 2 for share in market_shares)

def simulate_supply_chain_disruption() -> Dict[str, Any]:
    supply_chain_nodes = {
        "Litografia EUV": {"leader": "ASML", "shares": [100.0]},
        "Ottiche Litografiche": {"leader": "Carl Zeiss", "shares": [100.0]},
        "Fonderia Avanzata (<5nm)": {"leader": "TSMC", "shares": [90.0, 10.0]}, # TSMC 90%, Samsung 10%
        "Packaging CoWoS": {"leader": "TSMC", "shares": [85.0, 15.0]},
        "EDA Software": {"leader": "Synopsys/Cadence", "shares": [65.0, 30.0, 5.0]}
    }

    hhi_results = {}
    for node, data in supply_chain_nodes.items():
        hhi_val = calculate_hhi(data["shares"])
        hhi_results[node] = {
            "leader": data["leader"],
            "hhi": hhi_val,
            "monopoly_risk": "MONOPOLIO_CRITICO" if hhi_val > 5000 else "ELEVATA_CONCENTRAZIONE"
        }

    # Simulazione interruzione nodo TSMC
    affected_downstream = [
        "NVIDIA AI Accelerators (H100, B200)",
        "Apple Silicon (M-Series, A-Series)",
        "AMD Instinct Accelerators (MI300X)",
        "Qualcomm Snapdragon Flagship",
        "Hyperscaler Cloud AI Infrastructure (AWS, Microsoft Azure, Google Cloud)"
    ]

    return {
        "node_metrics": hhi_results,
        "tsmc_cascade_impact": affected_downstream
    }

if __name__ == "__main__":
    res = simulate_supply_chain_disruption()
    print("[*] Analisi di Concentrazione della Supply Chain dei Semiconduttori:\n")
    for node, info in res["node_metrics"].items():
        print(f"  - Segmento : {node:<25}")
        print(f"    Leader   : {info['leader']}")
        print(f"    Indice HHI: {info['hhi']:.0f} -> {info['monopoly_risk']}\n")

    print("[*] Simulazione d'Impatto per Interruzione Operativa Fonderie TSMC:")
    for target in res["tsmc_cascade_impact"]:
        print(f"  [BLOCCATO] {target}")
```

Output atteso dell'esecuzione:

```text
[*] Analisi di Concentrazione della Supply Chain dei Semiconduttori:

  - Segmento : Litografia EUV          
    Leader   : ASML
    Indice HHI: 10000 -> MONOPOLIO_CRITICO

  - Segmento : Ottiche Litografiche     
    Leader   : Carl Zeiss
    Indice HHI: 10000 -> MONOPOLIO_CRITICO

  - Segmento : Fonderia Avanzata (<5nm)
    Leader   : TSMC
    Indice HHI: 8200 -> MONOPOLIO_CRITICO

  - Segmento : Packaging CoWoS         
    Leader   : TSMC
    Indice HHI: 7450 -> MONOPOLIO_CRITICO

  - Segmento : EDA Software            
    Leader   : Synopsys/Cadence
    Indice HHI: 5150 -> MONOPOLIO_CRITICO

[*] Simulazione d'Impatto per Interruzione Operativa Fonderie TSMC:
  [BLOCCATO] NVIDIA AI Accelerators (H100, B200)
  [BLOCCATO] Apple Silicon (M-Series, A-Series)
  [BLOCCATO] AMD Instinct Accelerators (MI300X)
  [BLOCCATO] Qualcomm Snapdragon Flagship
  [BLOCCATO] Hyperscaler Cloud AI Infrastructure (AWS, Microsoft Azure, Google Cloud)
```

### Laboratorio 3: Motore di classificazione del rischio EU AI Act e identificazione GPAI a rischio sistemico

Questo laboratorio implementa un motore di conformità in [Python](https://www.python.org/) che valuta sistemi intelligenti rispetto ai criteri dell'[EU AI Act](https://artificialintelligenceact.eu/) (Regolamento UE 2024/1689), categorizzandoli nelle classi di rischio stabilite dalla normativa europea.

Procedura operativa:

- [ ] Strutturare il profilo funzionale del sistema di intelligenza artificiale indicando il dominio di impiego, la tecnologia e il calcolo cumulativo di addestramento in FLOPs.
- [ ] Verificare se l'applicazione ricade nei divieti assoluti dell'Articolo 5 (Rischio Inaccettabile).
- [ ] Verificare se l'applicazione rientra nell'Allegato III dei sistemi ad Alto Rischio (Articolo 6).
- [ ] Verificare se i modelli GPAI superano la soglia computazionale di $10^{25}$ FLOPs per la presunzione di rischio sistemico (Articoli 51–52).

```python
from typing import Dict, Any

def classify_eu_ai_act_compliance(system_profile: Dict[str, Any]) -> Dict[str, Any]:
    domain = system_profile.get("domain", "").lower()
    purpose = system_profile.get("purpose", "").lower()
    compute_flops = system_profile.get("training_compute_flops", 0.0)
    is_generative = system_profile.get("is_generative_ai", False)

    # 1. Articolo 5: Rischio Inaccettabile (Pratiche Vietate)
    if "social_scoring" in purpose or ("biometric_realtime_public" in purpose and not system_profile.get("authorized_law_enforcement", False)):
        tier = "RISCHIO_INACCETTABILE (Art. 5)"
        requirements = "Divieto assoluto di commercializzazione e impiego nell'Unione Europea."
    # 2. Articolo 6 e Allegato III: Alto Rischio
    elif domain in ["infrastrutture_critiche", "sanita", "selezione_personale", "giustizia", "controllo_frontiere"]:
        tier = "ALTO_RISCHIO (Art. 6 & Allegato III)"
        requirements = "Valutazione di conformità ex-ante, marcatura CE, log continui, supervisione umana obbligatoria."
    # 3. Articoli 51-52: General Purpose AI (GPAI) con Rischio Sistemico
    elif compute_flops >= 1e25:
        tier = "GPAI_RISCHIO_SISTEMICO (Art. 51-52)"
        requirements = "Audit di sicurezza, red-teaming avversario, stima energetica, notifica all'European AI Office."
    # 4. Articolo 50: Rischio Specifico di Trasparenza
    elif is_generative:
        tier = "SPECIFICO_RISCHIO_TRASPARENZA (Art. 50)"
        requirements = "Etichettatura obbligatoria dei contenuti generati, watermarking leggibile da macchine."
    else:
        tier = "RISCHIO_MINIMO"
        requirements = "Nessun vincolo normativo vincolante; adesione a codici di condotta volontari."

    return {
        "system_name": system_profile.get("name"),
        "compliance_tier": tier,
        "mandatory_obligations": requirements
    }

if __name__ == "__main__":
    test_systems = [
        {
            "name": "SocialScoreCitizen AI",
            "domain": "governance",
            "purpose": "social_scoring_behavioral",
            "training_compute_flops": 1e23,
            "is_generative_ai": False
        },
        {
            "name": "HR-TalentRecruiter Pro",
            "domain": "selezione_personale",
            "purpose": "curriculum_screening_evaluation",
            "training_compute_flops": 5e22,
            "is_generative_ai": False
        },
        {
            "name": "Frontier-LLM 100B",
            "domain": "general_purpose",
            "purpose": "multimodal_reasoning",
            "training_compute_flops": 2.5e25,
            "is_generative_ai": True
        },
        {
            "name": "NewsSummarizer Bot",
            "domain": "media",
            "purpose": "text_summarization",
            "training_compute_flops": 1e23,
            "is_generative_ai": True
        }
    ]

    print("[*] Valutazione di Conformità al Regolamento EU AI Act (UE 2024/1689):\n")
    for sys in test_systems:
        res = classify_eu_ai_act_compliance(sys)
        print(f"  - Sistema     : {res['system_name']}")
        print(f"    Livello     : {res['compliance_tier']}")
        print(f"    Obbligazioni: {res['mandatory_obligations']}\n")
```

Output atteso dell'esecuzione:

```text
[*] Valutazione di Conformità al Regolamento EU AI Act (UE 2024/1689):

  - Sistema     : SocialScoreCitizen AI
    Livello     : RISCHIO_INACCETTABILE (Art. 5)
    Obbligazioni: Divieto assoluto di commercializzazione e impiego nell'Unione Europea.

  - Sistema     : HR-TalentRecruiter Pro
    Livello     : ALTO_RISCHIO (Art. 6 & Allegato III)
    Obbligazioni: Valutazione di conformità ex-ante, marcatura CE, log continui, supervisione umana obbligatoria.

  - Sistema     : Frontier-LLM 100B
    Livello     : GPAI_RISCHIO_SISTEMICO (Art. 51-52)
    Obbligazioni: Audit di sicurezza, red-teaming avversario, stima energetica, notifica all'European AI Office.

  - Sistema     : NewsSummarizer Bot
    Livello     : SPECIFICO_RISCHIO_TRASPARENZA (Art. 50)
    Obbligazioni: Etichettatura obbligatoria dei contenuti generati, watermarking leggibile da macchine.
```

### Laboratorio 4: Analisi forense e validazione di integrità dei pesi di modelli open-weight

Questo laboratorio implementa un modulo di scansione di sicurezza in [Python](https://www.python.org/) che analizza la struttura binaria dei file di checkpoint, verificando l'integrità crittografica SHA-256 e leggendo l'header dei file `safetensors` per prevenire vulnerabilità di esecuzione di codice arbitrario (RCE) associate ai formati `pickle` non protetti.

Procedura operativa:

- [ ] Creare una struttura di byte conforme al formato standard `safetensors` (lunghezza header a 8 byte little-endian seguita da metadati JSON).
- [ ] Simulare un file di checkpoint legacy con payload malevolo `pickle`.
- [ ] Effettuare il parsing dell'header `safetensors` estraendo la mappa dei tensori e i metadati senza eseguire codice.
- [ ] Scansionare il file legacy identificando le istruzioni pericolose (`REDUCE`, `GLOBAL`, `system`) e calcolare l'hash SHA-256 di audit.

```python
import hashlib
import json
import struct
from typing import Dict, Any, Tuple

def inspect_safetensors_header(raw_bytes: bytes) -> Tuple[bool, Dict[str, Any]]:
    """Estrae i metadati da un file safetensors leggendo l'header binario a 8 byte."""
    if len(raw_bytes) < 8:
        return False, {"error": "File troppo piccolo per contenere un header safetensors"}
    
    header_len = struct.unpack("<Q", raw_bytes[:8])[0]
    if len(raw_bytes) < 8 + header_len:
        return False, {"error": "Lunghezza header dichiarata non coerente con i byte disponibili"}

    header_json_bytes = raw_bytes[8:8 + header_len]
    try:
        header_data = json.loads(header_json_bytes.decode("utf-8"))
        file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        return True, {
            "format": "safetensors",
            "is_safe": True,
            "header_size_bytes": header_len,
            "tensors_count": len([k for k in header_data.keys() if k != "__metadata__"]),
            "metadata": header_data.get("__metadata__", {}),
            "sha256_audit_hash": file_sha256
        }
    except Exception as e:
        return False, {"error": f"Parsing header fallito: {e}"}

def scan_legacy_pickle_checkpoint(raw_bytes: bytes) -> Dict[str, Any]:
    """Scansiona un file pickle alla ricerca di op-code pericolosi per vulnerabilità RCE."""
    dangerous_opcodes = [b"posix", b"system", b"subprocess", b"builtin", b"eval", b"exec"]
    detected_threats = []

    for op in dangerous_opcodes:
        if op in raw_bytes:
            detected_threats.append(op.decode("latin1"))

    return {
        "format": "pytorch_legacy_pickle (.bin / .pt)",
        "is_safe": len(detected_threats) == 0,
        "security_risk": "CRITICAL_RCE_VULNERABILITY" if detected_threats else "UNSAFE_FORMAT_LEGACY",
        "suspicious_opcodes": detected_threats,
        "sha256_audit_hash": hashlib.sha256(raw_bytes).hexdigest()
    }

if __name__ == "__main__":
    # 1. Creazione file sintetico safetensors valido
    mock_meta = {
        "model.layers.0.weight": {"dtype": "F16", "shape": [4096, 4096], "data_offsets": [0, 33554432]},
        "__metadata__": {"format": "pt", "author": "Sovereign AI Foundation"}
    }
    meta_encoded = json.dumps(mock_meta).encode("utf-8")
    safetensors_bytes = struct.pack("<Q", len(meta_encoded)) + meta_encoded + b"\x00" * 1024

    # 2. Creazione file pickle simulato con injection di comando malevolo
    malicious_pickle_bytes = b"\x80\x04\x95\x2c\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x8c\x06system\x93\x8c\x08whoami\x85\x52."

    print("[*] Ispezione Forense Supply Chain Pesi Modelli:\n")
    ok, safe_res = inspect_safetensors_header(safetensors_bytes)
    print(f"  - Checkpoint 1 (Safetensors):")
    print(f"    Formato  : {safe_res['format']} | Sicuro: {safe_res['is_safe']}")
    print(f"    Tensori  : {safe_res['tensors_count']} | Autore: {safe_res['metadata'].get('author')}")
    print(f"    SHA-256  : {safe_res['sha256_audit_hash'][:16]}...\n")

    pickle_res = scan_legacy_pickle_checkpoint(malicious_pickle_bytes)
    print(f"  - Checkpoint 2 (Legacy Pickle):")
    print(f"    Formato  : {pickle_res['format']} | Sicuro: {pickle_res['is_safe']}")
    print(f"    Minaccia : {pickle_res['security_risk']}")
    print(f"    Op-Codes : {pickle_res['suspicious_opcodes']}")
    print(f"    SHA-256  : {pickle_res['sha256_audit_hash'][:16]}...")
```

Output atteso dell'esecuzione:

```text
[*] Ispezione Forense Supply Chain Pesi Modelli:

  - Checkpoint 1 (Safetensors):
    Formato  : safetensors | Sicuro: True
    Tensori  : 1 | Autore: Sovereign AI Foundation
    SHA-256  : a102d84c3e8a911f...

  - Checkpoint 2 (Legacy Pickle):
    Formato  : pytorch_legacy_pickle (.bin / .pt) | Sicuro: False
    Minaccia : CRITICAL_RCE_VULNERABILITY
    Op-Codes : ['posix', 'system']
    SHA-256  : f593bc141b7128de...
```