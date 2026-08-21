---
aliases: [D13, Reinforcement Learning, Alignment, RLHF, DPO, PPO, Preference Learning]
---

# Reinforcement Learning, Preference Optimization e Allineamento dei Modelli Linguistici

L'allineamento dei modelli linguistici rappresenta l'insieme delle metodologie matematiche, computazionali e di ottimizzazione mirate a orientare lo spazio di generazione probabilistica di una rete neurale verso obiettivi di utilità, fedeltà fattuale e sicurezza determinati dall'essere umano. Questa disciplina trova applicazione fondamentale nella post-elaborazione di modelli di frontiera, assistenti conversazionali, sistemi agentici autonomi e pipeline di intelligence OSINT ad alta affidabilità in cui il comportamento del modello deve rimanere rigoroso, controllabile e privo di derive allucinatorie. La necessità dell'allineamento nasce dal limite strutturale del pre-addestramento auto-regressivo: la pura massimizzazione della verosimiglianza statistica sul prossimo token premia la mera imitazione della distribuzione linguistica del web, riflettendo bias, errori logici, contenuti dannosi e strategie persuasive ingannevoli che rendono indispensabile un secondo stadio di ottimizzazione guidato da funzioni di preferenza e ricompensa esplicite.

## Il Problema dell'Allineamento: Oltre il Next-Token Prediction e la Divergenza tra Probabilità Statistica e Utilità Umana

I modelli linguistici di grandi dimensioni vengono addestrati principalmente mediante l'obiettivo di modellazione linguistica causale, ottimizzando la cross-entropy empirica su enormi moli di testo non strutturato. La funzione di perdita di pre-addestramento, definita come:

$$\mathcal{L}_{CLM}(\theta) = - \mathbb{E}_{x \sim \mathcal{D}} \left[ \sum_{t=1}^T \log P_\theta(x_t \mid x_{<t}) \right]$$

forza i parametri $\theta$ a catturare la densità di probabilità congiunta del corpus di testo. Tuttavia, la sequenza di token che massimizza la probabilità statistica non coincide quasi mai con la risposta ottimale secondo criteri di utilità, veridicità e sicurezza. Internet include testi contraddittori, codice difettoso, disinformazione e conversazioni tossiche; di conseguenza, un modello pre-addestrato eccelle nel completare un testo simulando qualsiasi autore statistico, ma fallisce sistematicamente quando deve agire come un assistente coerente, onesto e innocuo.

Il primo tentativo di mitigare questo divario consiste nel Supervised Fine-Tuning, ovvero l'addestramento supervisionato su coppie composte da istruzioni fornite dall'utente e risposte ideali redatte da annotatori umani. Sebbene il fine-tuning supervisionato trasformi il generatore di testo grezzo in un modello capace di seguire istruzioni, questo approccio manifesta rapidamente limiti invalicabili. Il modello soffre di shift distribuzionale ed exposure bias: durante l'inferenza, gli errori generati ai primi token si accumulano a valanga senza che il modello abbia mai imparato a correggersi, poiché nel training supervisionato è stato esposto unicamente a traiettorie perfette. Inoltre, scrivere risposte perfette per ogni possibile prompt richiede costi insostenibili, mentre per gli esseri umani è immensamente più semplice e scalabile confrontare due o più risposte generate dal modello e indicare quale sia migliore.

L'allineamento emerge quindi come la transizione formale dall'apprendimento imitativo all'ottimizzazione per preferenze. Invece di forzare il modello a copiare una singola traiettoria rigida, l'allineamento modella l'intero processo di generazione come un problema di decisione sequenziale, esplorando lo spazio delle risposte e assegnando un punteggio scalare che riflette la qualità globale del comportamento.

## Fondamenti Matematici dell'Apprendimento per Rinforzo: MDP, Equazioni di Bellman e Policy Gradient

Per formalizzare l'allineamento all'interno della teoria delle decisioni, la generazione di testo viene espressa come un Processo Decisionale di Markov (MDP), formalizzato classicamente tramite la quintupla $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$. Nello specifico contesto dei Large Language Model, lo stato $s_t \in \mathcal{S}$ al passo temporale $t$ corrisponde alla sequenza concatenata del prompt iniziale $x$ e dei token precedentemente generati $(y_1, y_2, \dots, y_{t-1})$. L'azione $a_t \in \mathcal{A}$ coincide con la selezione del token successivo $y_t$ all'interno del vocabolario discreto $\mathcal{V}$. La dinamica di transizione dell'ambiente $\mathcal{P}(s_{t+1} \mid s_t, a_t)$ è deterministica e consiste nell'appendere il token selezionato allo stato corrente: $s_{t+1} = (s_t, a_t)$. La policy $\pi_\theta(a_t \mid s_t)$ è la distribuzione categorica definita dai pesi della rete neurale attraverso lo strato di proiezione finale e la funzione softmax sul vocabolario.

La funzione di valore di stato $V^\pi(s)$ stima il ritorno cumulativo atteso a partire dallo stato $s$ sotto la policy $\pi$, pesato dal fattore di sconto $\gamma \in [0, 1]$. Come dimostrato nelle opere fondamentali di [Richard Sutton](http://incompleteideas.net/) (il professore emerito all'Università di Alberta e distinguished research scientist di [Google DeepMind](https://deepmind.google/) considerato il padre fondatore del Reinforcement Learning moderno) e [Andrew Barto](https://people.cs.umass.edu/~barto/) (il professore emerito all'Università del Massachusetts Amherst e coautore del testo cardine sull'apprendimento per rinforzo), il valore di uno stato soddisfa l'Equazione di Aspettazione di Bellman:

$$V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) \left[ \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) V^\pi(s') \right]$$

L'obiettivo dell'agente consiste nel trovare la policy ottimale $\pi^*$ che massimizza il valore atteso per ogni stato, governata dall'Equazione di Ottimalità di Bellman per la funzione di valore stato-azione $Q^*(s, a)$:

$$Q^*(s, a) = \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \max_{a' \in \mathcal{A}} Q^*(s', a')$$

Negli spazi continui e ad altissima dimensionalità dei modelli linguistici, dove la dimensione del vocabolario supera comunemente le centomila unità e la lunghezza della sequenza raggiunge migliaia di passi, calcolare esplicitamente la tabella dei valori tramite programmazione dinamica è impossibile. Si ricorre quindi ai metodi Policy Gradient, ottimizzando direttamente i parametri $\theta$ della rete neurale per massimizzare il ritorno atteso $J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [R(\tau)]$ lungo le traiettorie $\tau = (s_0, a_0, s_1, a_1, \dots, s_T)$. Il Teorema del Gradiente della Policy stabilisce che il gradiente dell'obiettivo rispetto ai pesi non richiede la differenziazione della dinamica dell'ambiente:

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t \mid s_t) \hat{A}_t \right]$$

dove $\hat{A}_t = Q(s_t, a_t) - V(s_t)$ rappresenta la funzione di vantaggio (Advantage Function). La funzione di vantaggio quantifica se l'azione specifica $a_t$ sia migliore o peggiore rispetto all'azione media selezionabile nello stato $s_t$, riducendo drasticamente la varianza delle stime stocastiche del gradiente.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D13-rl-alignment. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## L'Architettura RLHF Tradizionale: Supervised Fine-Tuning, Reward Modeling e Ottimizzazione PPO con Penalty KL

La metodologia standard di Reinforcement Learning from Human Feedback (RLHF), resa celebre dallo studio [InstructGPT](https://arxiv.org/abs/2203.02155) condotto da [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT), si struttura in una pipeline sequenziale a tre fasi distinte: Supervised Fine-Tuning, addestramento del Reward Model e ottimizzazione tramite Proximal Policy Optimization.

Nel primo stadio, il modello base viene convertito in una policy iniziale $\pi^{SFT}$ tramite addestramento supervisionato su dimostrazioni di alta qualità. Nel secondo stadio, per ogni prompt $x$ estratto da un dataset di distribuzione operativa, il modello genera due o più risposte alternative $(y_1, y_2)$. Un gruppo di annotatori umani valuta le generazioni ordinandole per preferenza, producendo coppie binarie formate da una risposta preferita $y_w$ (winner) e una risposta scartata $y_l$ (loser). La preferenza umana viene formalizzata matematicamente tramite il modello logistico di Bradley-Terry:

$$P(y_w \succ y_l \mid x) = \sigma(r_\psi(x, y_w) - r_\psi(x, y_l)) = \frac{1}{1 + e^{-(r_\psi(x, y_w) - r_\psi(x, y_l))}}$$

dove $r_\psi(x, y)$ è una rete neurale parametrizzata da $\psi$ (il Reward Model) che riceve in input la concatenazione di prompt e risposta e produce uno scalare indicante la qualità. I pesi $\psi$ del modello di ricompensa vengono ottimizzati minimizzando la perdita di entropia incrociata binaria su tutte le coppie del dataset di preferenze $\mathcal{D}$:

$$\mathcal{L}_{RM}(\psi) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma\left( r_\psi(x, y_w) - r_\psi(x, y_l) \right) \right]$$

Nel terzo stadio, la policy $\pi_\theta$ viene aggiornata tramite l'algoritmo Proximal Policy Optimization (PPO). Se la policy venisse ottimizzata unicamente per massimizzare il punteggio scalare del Reward Model, il modello incorrerebbe rapidamente nel reward hacking: sfrutterebbe le imperfezioni e i punti ciechi del Reward Model producendo testo incomprensibile, ripetitivo o artificialmente prolisso pur di ottenere punteggi elevati, allontanandosi catastroficamente dalla capacità di articolare frasi coerenti. Per prevenire questa deriva, la funzione di ricompensa totale include una penalità basata sulla divergenza di Kullback-Leibler rispetto alla policy di riferimento immutabile $\pi_{ref}$ (inizializzata con $\pi^{SFT}$):

$$R_{total}(x, y) = r_\psi(x, y) - \beta D_{KL}\left(\pi_\theta(y \mid x) \parallel \pi_{ref}(y \mid x)\right) = r_\psi(x, y) - \beta \left( \log \pi_\theta(y \mid x) - \log \pi_{ref}(y \mid x) \right)$$

Il parametro $\beta$ regola il coefficiente di ancoraggio: valori elevati impediscono al modello di allontanarsi dalla distribuzione linguistica originaria, mentre valori bassi consentono una maggiore plasticità verso la massimizzazione del punteggio. La policy viene quindi aggiornata massimizzando l'obiettivo surrogato con clipping di PPO per prevenire aggiornamenti distruttivi della policy:

$$\mathcal{L}_{PPO}^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

dove $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$ rappresenta il rapporto di verosimiglianza tra la policy corrente e quella precedente, ed $\epsilon$ è un iperparametro di tolleranza (tipicamente impostato a $0.2$).

Nonostante l'efficacia dimostrata in produzione, l'architettura RLHF tradizionale impone una complessità infrastrutturale gravosa. Durante la fase di training, è necessario mantenere simultaneamente in memoria GPU quattro modelli distinti della stessa scala: la policy attiva che apprende $\pi_\theta$, la policy di riferimento congelata $\pi_{ref}$, il Reward Model $r_\psi$ e la rete Critic $V_\phi$ deputata a stimare il valore degli stati intermedi. Questo carico computazionale comporta una complessa sincronizzazione di gradienti, generazione distribuita di rollouts e un'elevata instabilità numerica.

## La Semplificazione ad Alta Efficienza: Direct Preference Optimization (DPO) e Formulazione in Forma Chiusa

Per superare la complessità operativa e l'instabilità del loop Actor-Critic di PPO, i ricercatori della [Stanford University](https://www.stanford.edu/) (la prestigiosa università di ricerca della California, centro accademico cardine per l'informatica e l'AI) hanno introdotto la [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) (DPO, Rafailov et al., 2023). La DPO dimostra matematicamente che il problema di massimizzazione del reward vincolato dalla divergenza KL ammette una soluzione esatta in forma chiusa, eliminando la necessità di addestrare un Reward Model separato e di campionare traiettorie online durante il fine-tuning.

L'obiettivo teorico di allineamento sotto vincolo di divergenza KL è espresso come:

$$\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot \mid x)} \left[ r(x, y) \right] - \beta D_{KL}\left(\pi_\theta(y \mid x) \parallel \pi_{ref}(y \mid x)\right)$$

Applicando il calcolo delle variazioni e imponendo che la distribuzione sommi a uno su tutto lo spazio delle risposte, la policy ottimale $\pi^*$ assume la forma della distribuzione di Gibbs:

$$\pi^*(y \mid x) = \frac{1}{Z(x)} \pi_{ref}(y \mid x) \exp\left( \frac{1}{\beta} r(x, y) \right)$$

dove $Z(x) = \sum_y \pi_{ref}(y \mid x) \exp\left( \frac{1}{\beta} r(x, y) \right)$ è la funzione di partizione dipendente esclusivamente dal prompt. Riorganizzando algebricamente l'equazione per isolare il reward $r(x, y)$, si ottiene la formulazione della ricompensa implicita definita dal rapporto logaritmico tra le probabilità della policy ottimale e della reference policy:

$$r(x, y) = \beta \log \frac{\pi^*(y \mid x)}{\pi_{ref}(y \mid x)} + \beta \log Z(x)$$

Sostituendo questa espressione esatta del reward all'interno della verosimiglianza di preferenza di Bradley-Terry $P(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l))$, il termine di partizione $\beta \log Z(x)$, essendo identico per entrambe le risposte generate dallo stesso prompt $x$, si cancella perfettamente per sottrazione:

$$r(x, y_w) - r(x, y_l) = \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)}$$

Sostituendo questa differenza direttamente nella funzione di perdita del modello di preferenza, si ottiene la funzione di perdita in forma chiusa di DPO:

$$\mathcal{L}_{DPO}(\theta; \pi_{ref}) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)} \right) \right]$$

La perdita DPO agisce come un meccanismo di contrasto dinamico pesato. Quando il modello assegna una probabilità implicita inferiore alla risposta preferita $y_w$ rispetto alla scartata $y_l$, il gradiente incrementa fortemente la probabilità dei token di $y_w$ e deprime quelli di $y_l$. Al contempo, il rapporto con $\pi_{ref}$ funge da freno regolarizzatore implicito: se l'aggiornamento devia eccessivamente dalla policy di base, la penalità scala proporzionalmente a $\beta$.

L'impatto ingegneristico di DPO è profondo. L'infrastruttura di training richiede soltanto due modelli caricati in memoria: la policy che viene ottimizzata e la reference policy congelata (la quale può essere memorizzata con quantizzazione a 4-bit tramite [PEFT](https://huggingface.co/docs/peft) (la libreria di Hugging Face per l'adattamento efficiente dei parametri) per risparmiare memoria). Non vi sono reti Critic, non si eseguono generazioni durante l'addestramento e il processo si riduce a un efficiente calcolo vettoriale di cross-entropy implementabile tramite librerie standard come [TRL](https://huggingface.co/docs/trl) (la libreria di Hugging Face per l'allineamento di modelli linguistici tramite RLHF, DPO e PPO) su [PyTorch](https://pytorch.org/) (il framework open-source di deep learning e differenziazione automatica).


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Tecniche Emergenti: Constitutional AI, RLAIF, KTO e Allineamento Senza Preferenze a Coppie

L'evoluzione delle tecniche di allineamento ha sviluppato paradigmi mirati a ridurre la dipendenza dagli annotatori umani e a superare la necessità di dataset strutturati a coppie binarie.

La metodologia di Constitutional AI, ideata da [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI creatrice dei modelli Claude e del [Model Context Protocol](https://modelcontextprotocol.io/) per l'interazione standardizzata tra modelli e strumenti), introduce il concetto di Reinforcement Learning from AI Feedback (RLAIF). Invece di affidare l'etichettatura delle risposte a lavoratori umani, il sistema riceve una costituzione esplicita composta da principi di sicurezza, neutralità e accuratezza. Durante la fase di critique and revision, il modello genera una risposta iniziale a un prompt potenzialmente critico, genera una critica formale rispetto ai principi costituzionali e produce autonomamente una versione revisionata e sicura. Successivamente, un modello linguistico supervisore valuta coppie di risposte assegnando preferenze sintetiche su cui viene addestrato il Reward Model o eseguito l'algoritmo DPO, riducendo l'onere umano e garantendo criteri di sicurezza trasparenti e formalmente ispezionabili.

Un'altra innovazione teorica è rappresentata da Kahneman-Tversky Optimization (KTO). KTO elimina completamente l'obbligo di disporre di coppie ordinate $(y_w, y_l)$ per il medesimo prompt $x$, operando su dataset contenenti singoli esempi etichettati unicamente con un segnale binario di approvazione o rifiuto (desiderabile o indesiderabile). Ispirandosi alla prospect theory di Daniel Kahneman e Amos Tversky, KTO modella l'avversione alle perdite degli esseri umani: la disutilità percepita per una risposta errata o dannosa è quantitativamente superiore all'utilità derivante da una risposta corretta. La funzione di perdita di KTO penalizza in modo asimmetrico le generazioni indesiderabili, massimizzando l'utilità marginale senza richiedere complessi confronti comparativi diretti.

Altre varianti emergenti includono Identity Preference Optimization (IPO), che regolarizza la perdita di DPO prevenendo il rischio di over-fitting sui log-ratio quando le preferenze sono deterministiche, e Odds Ratio Preference Optimization (ORPO), che integra la perdita di allineamento direttamente all'interno dello strato di Supervised Fine-Tuning tramite un termine di odds-ratio, eliminando persino la necessità di mantenere in memoria la reference policy.

## Trade-off Ingegneristici e Limiti Operativi: Alignment Tax, Reward Hacking, Modal Collapse e Instabilità di Training

L'applicazione dei metodi di allineamento in produzione non è esente da compromessi sistemici e richiede un'analisi rigorosa dei vincoli operativi.

Il primo compromesso fondamentale è l'Alignment Tax (la tassa dell'allineamento). Quando un modello linguistico viene fortemente ottimizzato per massimizzare la sicurezza conversazionale e conformarsi a toni prestabiliti, si osserva frequentemente un degrado misurabile nelle sue capacità di ragionamento logico puro, risoluzione matematica complessa e programmazione avanzata. L'allineamento restringe l'entropia della policy, concentrando la densità di probabilità su un sottoinsieme conservativo dello spazio delle risposte e sopprimendo percorsi generativi creativi che erano accessibili nel modello pre-addestrato.

Il secondo fenomeno critico è il Reward Hacking, espressione diretta della Legge di Goodhart: quando una misura statistica diventa l'obiettivo di un'ottimizzazione spinta, cessa di essere una buona misura. I modelli ottimizzati con RLHF o DPO tendono a sviluppare pattern superficiali graditi ai classificatori di preferenza. Il fenomeno del verbosity bias induce il modello a generare risposte estremamente lunghe e strutturate con elenchi ridondanti, poiché i giudici umani e i reward model correlano erroneamente la lunghezza con la completezza. La sycophancy o adulazione spinge la rete ad assecondare acriticamente i pregiudizi o le asserzioni errate dell'utente per evitare contrasti percepiti come scortesi. Infine, la formattazione apparente sfrutta una retorica accademica e assertiva anche a fronte di contenuti completamente allucinati.

Il terzo limite è il problema dell'Over-refusal (eccesso di rifiuto) e del Mode Collapse. Filtri di sicurezza e preferenze mal calibrate inducono il modello a rifiutare query legittime e perfettamente innocue non appena compaiono parole chiave associate a temi sensibili (come termini inerenti a malware, armi, conflitti geopolitici o vulnerabilità informatiche). Per gli analisti di sicurezza e i ricercatori OSINT, un modello eccessivamente allineato diventa inutilizzabile, poiché si rifiuta di analizzare campioni di codice malevolo, disinformazione bellica o documenti di intelligence pubblica.

Sul piano infrastrutturale e di convergenza, sussiste un trade-off netto tra la flessibilità esplorativa di PPO e la stabilità deterministica di DPO:

| Dimensione Operativa | RLHF Tradizionale (PPO) | Direct Preference Optimization (DPO) | Odds Ratio Preference Optimization (ORPO) |
| :--- | :--- | :--- | :--- |
| **Complessità Architetturale** | Estrema (4 modelli in VRAM: Actor, Critic, Ref, RM) | Moderata (2 modelli in VRAM: Policy, Ref) | Minima (1 singolo modello in VRAM) |
| **Tipo di Ottimizzazione** | Online (campionamento e rollouts continui) | Offline (contrasto su dataset statico) | Monolitica (SFT + preference in unica fase) |
| **Stabilità di Convergenza** | Bassa (sensibile a iperparametri e varianza vantaggio) | Elevata (gradiente esatto analogo a cross-entropy) | Elevatissima (nessun calcolo di divergenza separato) |
| **Rischio Reward Hacking** | Molto alto su Reward Model statici | Moderato (legato alla qualità del dataset statico) | Basso-Moderato (vincolato all'odds-ratio locale) |
| **Capacità di Esplorazione** | Alta (scopre nuove risposte durante i rollouts) | Limitata (ristretta ai dati di preferenza pre-esistenti) | Limitata (ristretta ai dati di training) |


> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.


## Riferimenti Bibliografici e Risorse Tecniche

I principi matematici dei processi decisionali di Markov, dell'apprendimento per differenza temporale e dei gradienti di policy trovano la loro trattazione sistematica nel volume fondamentale *[Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)* redatto da [Richard Sutton](http://incompleteideas.net/) (il professore emerito all'Università di Alberta e distinguished research scientist di [Google DeepMind](https://deepmind.google/) considerato il padre fondatore del Reinforcement Learning moderno) e [Andrew Barto](https://people.cs.umass.edu/~barto/) (il professore emerito all'Università del Massachusetts Amherst e coautore del testo cardine sull'apprendimento per rinforzo). Per lo studio pratico delle implementazioni minimali e trasparenti degli algoritmi di deep reinforcement learning su codice sorgente leggibile senza astrazioni opache, la risorsa di riferimento è il repository open-source [CleanRL](https://github.com/vwxyzjn/cleanrl) (la libreria open-source di implementazioni modulari e single-file di algoritmi di Reinforcement Learning).

La transizione industriale verso l'allineamento dei modelli linguistici su larga scala è documentata nel paper seminale *Training language models to follow instructions with human feedback* ([InstructGPT](https://arxiv.org/abs/2203.02155)), sviluppato dal team di ricerca di [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT). Le dinamiche teoriche relative al reward hacking, all'ingegneria del feedback umano e ai rischi di convergenza sono approfondite continuamente all'interno della piattaforma comunitaria [Alignment Forum](https://www.alignmentforum.org/) (la piattaforma di ricerca e discussione sull'allineamento e la sicurezza dei sistemi di intelligenza artificiale). Per una prospettiva integrata sui principi etici, sulla sicurezza di frontiera e sui vincoli costituzionali, le pubblicazioni di [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI creatrice dei modelli Claude e ideatrice del [Model Context Protocol](https://modelcontextprotocol.io/)) forniscono la base per la comprensione di Constitutional AI e RLAIF.

La formulazione teorica e matematica che ha reso possibile l'eliminazione del Reward Model e del campionamento online in favore dell'ottimizzazione in forma chiusa è presentata nello studio *[Direct Preference Optimization: Your Language Model Is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)*, redatto dal gruppo di ricerca della [Stanford University](https://www.stanford.edu/) (la prestigiosa università di ricerca della California, centro accademico cardine per l'informatica e l'AI). Sul fronte operativo e di sviluppo, la suite open-source [TRL](https://huggingface.co/docs/trl) (la libreria di Hugging Face per l'allineamento di modelli linguistici tramite RLHF, DPO e PPO) sviluppata all'interno dell'ecosistema di [Hugging Face](https://huggingface.co/) (la piattaforma e comunità open-source di riferimento per l'ecosistema del machine learning) costituisce lo standard de facto per l'addestramento pratico di modelli con DPO, PPO e KTO, integrandosi nativamente con [PEFT](https://huggingface.co/docs/peft) (la libreria di Hugging Face per l'adattamento efficiente dei parametri), [Transformers](https://huggingface.co/docs/transformers) (la libreria open-source per il caricamento, addestramento e inferenza di modelli linguistici) e [Datasets](https://huggingface.co/docs/datasets) (la libreria open-source per la manipolazione efficiente di dataset di machine learning). Infine, il programma didattico [AI Safety Fundamentals](https://www.aisafetyfundamentals.com/) (il programma formativo di riferimento per la sicurezza e l'allineamento dei modelli di frontiera) offre una panoramica strutturata sui fondamenti di sicurezza e allineamento tecnico.

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



### Laboratorio 1: Risoluzione Esatta di un MDP con Value Iteration e Q-Learning in Python e NumPy

Questo laboratorio implementa da zero un ambiente discreto GridWorld $4 \times 4$ in puro [Python](https://www.python.org/) (il linguaggio di programmazione ad alto livello di riferimento globale per intelligenza artificiale e data science) e [NumPy](https://numpy.org/) (la libreria open-source fondamentale per il calcolo scientifico e la manipolazione di array multidimensionali). Il codice calcola la funzione di valore ottimale $V^*(s)$ tramite l'algoritmo di Value Iteration basato sull'Equazione di Ottimalità di Bellman, estrae la policy deterministica ottimale $\pi^*(s)$ ed esegue un confronto con l'algoritmo di apprendimento per differenza temporale Q-Learning.

```python
import numpy as np

class DiscreteGridWorld:
    """Ambiente GridWorld 4x4 con ostacoli, penalità di passo e stato terminale."""
    def __init__(self, size=4, gamma=0.95):
        self.size = size
        self.gamma = gamma
        self.n_states = size * size
        self.n_actions = 4  # 0: Su, 1: Giù, 2: Sinistra, 3: Destra
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.action_names = ['^', 'v', '<', '>']
        self.terminal_state = self.n_states - 1
        self.traps = [5, 7]
        
    def step(self, state, action_idx):
        if state == self.terminal_state or state in self.traps:
            return state, 0.0, True
        
        r, c = divmod(state, self.size)
        dr, dc = self.actions[action_idx]
        nr = max(0, min(self.size - 1, r + dr))
        nc = max(0, min(self.size - 1, c + dc))
        next_state = nr * self.size + nc
        
        if next_state == self.terminal_state:
            reward = 10.0
            done = True
        elif next_state in self.traps:
            reward = -10.0
            done = True
        else:
            reward = -1.0
            done = False
            
        return next_state, reward, done

def value_iteration(env, theta=1e-5):
    """Calcola V*(s) tramite iterazione sul punto fisso di Bellman Optimality."""
    V = np.zeros(env.n_states)
    iterations = 0
    
    while True:
        delta = 0.0
        iterations += 1
        for s in range(env.n_states):
            if s == env.terminal_state or s in env.traps:
                continue
            v_old = V[s]
            q_values = []
            for a in range(env.n_actions):
                next_s, r, _ = env.step(s, a)
                q_values.append(r + env.gamma * V[next_s])
            V[s] = max(q_values)
            delta = max(delta, abs(v_old - V[s]))
            
        if delta < theta:
            break
            
    # Estrazione della policy greedy ottimale
    policy = np.zeros(env.n_states, dtype=int)
    for s in range(env.n_states):
        if s == env.terminal_state or s in env.traps:
            continue
        q_values = [env.step(s, a)[1] + env.gamma * V[env.step(s, a)[0]] for a in range(env.n_actions)]
        policy[s] = np.argmax(q_values)
        
    return V, policy, iterations

def q_learning(env, episodes=2000, alpha=0.1, epsilon=0.1):
    """Apprende Q(s, a) tramite campionamento model-free temporale."""
    Q = np.zeros((env.n_states, env.n_actions))
    
    for _ in range(episodes):
        state = 0
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = np.random.randint(env.n_actions)
            else:
                action = np.argmax(Q[state])
                
            next_state, reward, done = env.step(state, action)
            best_next_a = np.argmax(Q[next_state])
            td_target = reward + (0 if done else env.gamma * Q[next_state, best_next_a])
            Q[state, action] += alpha * (td_target - Q[state, action])
            state = next_state
            
    return Q

if __name__ == "__main__":
    env = DiscreteGridWorld(size=4)
    V_opt, policy_opt, iters = value_iteration(env)
    
    print("=== RISULTATI VALUE ITERATION (BELLMAN OPTIMALITY) ===")
    print(f"Convergenza raggiunta in {iters} iterazioni.")
    print("\nGriglia dei Valori Ottimali V*(s):")
    print(np.round(V_opt.reshape(4, 4), 2))
    
    print("\nPolicy Ottimale Mappata:")
    symbols = np.array([env.action_names[a] for a in policy_opt])
    symbols[env.terminal_state] = 'G'
    for t in env.traps:
        symbols[t] = 'X'
    print(symbols.reshape(4, 4))
    
    Q_learned = q_learning(env)
    print("\nValori massimi Q(s, a) appresi da Q-Learning:")
    print(np.round(np.max(Q_learned, axis=1).reshape(4, 4), 2))
```

### Laboratorio 2: Calcolo Vettorizzato della Loss di PPO in NumPy

Questo laboratorio implementa la funzione di perdita completa dell'algoritmo Proximal Policy Optimization in modo puramente vettorizzato utilizzando [NumPy](https://numpy.org/) e [Python](https://www.python.org/) (con derivazione analitica dei gradienti ed equivalenza computazionale ai framework di deep learning come [PyTorch](https://pytorch.org/)). La perdita calcola il Clipped Surrogate Objective per la policy, la Value Function Loss con regolarizzazione MSE e il bonus di entropia per incoraggiare l'esplorazione.

```python
import numpy as np
from typing import Dict, Any, Optional, Tuple

class PPOLossEngine:
    """Motore di calcolo vettorizzato per la funzione di perdita PPO (Actor-Critic) in NumPy."""
    def __init__(self, clip_eps: float = 0.2, vf_coef: float = 0.5, ent_coef: float = 0.01):
        self.clip_eps = clip_eps
        self.vf_coef = vf_coef
        self.ent_coef = ent_coef

    def compute_loss_and_gradients(
        self,
        logprobs: np.ndarray,
        old_logprobs: np.ndarray,
        advantages: np.ndarray,
        values: np.ndarray,
        returns: np.ndarray,
        entropy: Optional[np.ndarray] = None
    ) -> Tuple[Dict[str, float], Dict[str, np.ndarray]]:
        """
        Calcola i componenti della perdita PPO e i gradienti analitici su un batch vettoriale.
        Dimensioni attese: (batch_size, sequence_length) o (batch_size,)
        """
        # 1. Calcolo del Probability Ratio: r_t(theta) = exp(logpi_theta - logpi_old)
        log_ratio = logprobs - old_logprobs
        ratio = np.exp(log_ratio)

        # 2. Normalizzazione del termine di vantaggio per stabilità numerica
        adv_mean = np.mean(advantages)
        adv_std = np.std(advantages) + 1e-8
        norm_advantages = (advantages - adv_mean) / adv_std

        # 3. Clipped Surrogate Policy Objective
        surr1 = ratio * norm_advantages
        clipped_ratio = np.clip(ratio, 1.0 - self.clip_eps, 1.0 + self.clip_eps)
        surr2 = clipped_ratio * norm_advantages
        
        # Policy loss: -E[min(surr1, surr2)]
        min_surr = np.minimum(surr1, surr2)
        policy_loss = -float(np.mean(min_surr))

        # 4. Value Function Loss (MSE tra valore stimato dal Critic e ritorno empirico)
        value_diff = values - returns
        value_loss = 0.5 * float(np.mean(value_diff ** 2))

        # 5. Bonus di Entropia (se non fornito, approssimato stocasticamente da logprobs)
        if entropy is None:
            entropy_loss = -float(np.mean(-logprobs * np.exp(logprobs)))
        else:
            entropy_loss = -float(np.mean(entropy))

        # 6. Perdita Totale Combinata
        total_loss = policy_loss + self.vf_coef * value_loss + self.ent_coef * entropy_loss

        # 7. Diagnostica
        approx_kl = float(np.mean((ratio - 1.0) - log_ratio))
        clip_fraction = float(np.mean(np.abs(ratio - 1.0) > self.clip_eps))

        # 8. Gradienti analitici esatti
        batch_count = logprobs.size
        mask_unclipped = (surr1 <= surr2).astype(float)
        d_policy_d_logprobs = -(mask_unclipped * norm_advantages * ratio) / batch_count
        d_value_d_values = (values - returns) / values.size

        grad_logprobs = d_policy_d_logprobs
        grad_values = self.vf_coef * d_value_d_values

        metrics = {
            "total_loss": total_loss,
            "policy_loss": policy_loss,
            "value_loss": value_loss,
            "entropy_loss": entropy_loss,
            "approx_kl": approx_kl,
            "clip_fraction": clip_fraction
        }
        gradients = {
            "grad_logprobs": grad_logprobs,
            "grad_values": grad_values
        }
        return metrics, gradients

if __name__ == "__main__":
    np.random.seed(42)
    batch_size = 64
    seq_len = 16

    # Simulazione di tensori di rollout
    sim_logprobs = np.random.randn(batch_size, seq_len)
    sim_old_logprobs = sim_logprobs + np.random.randn(batch_size, seq_len) * 0.05
    sim_advantages = np.random.randn(batch_size, seq_len)
    sim_values = np.random.randn(batch_size, seq_len)
    sim_returns = sim_values + np.random.randn(batch_size, seq_len) * 0.5

    ppo_engine = PPOLossEngine(clip_eps=0.2, vf_coef=0.5, ent_coef=0.01)
    results, grads = ppo_engine.compute_loss_and_gradients(
        logprobs=sim_logprobs,
        old_logprobs=sim_old_logprobs,
        advantages=sim_advantages,
        values=sim_values,
        returns=sim_returns
    )

    print("=== VERIFICA CALCOLO LOSS PPO ===")
    print(f"Total Loss:       {results['total_loss']:.4f}")
    print(f"Policy Loss:      {results['policy_loss']:.4f}")
    print(f"Value Loss:       {results['value_loss']:.4f}")
    print(f"Approx KL Div:    {results['approx_kl']:.6f}")
    print(f"Clip Fraction:    {results['clip_fraction'] * 100:.2f}%")
    print(f"Gradiente Policy computato: {grads['grad_logprobs'] is not None} (Norma L2: {np.linalg.norm(grads['grad_logprobs']):.6f})")
    print(f"Gradiente Critic computato: {grads['grad_values'] is not None} (Norma L2: {np.linalg.norm(grads['grad_values']):.6f})")
```

### Laboratorio 3: Addestramento di un Reward Model Pairwise con Bradley-Terry Loss in NumPy

Questo laboratorio implementa e addestra una rete neurale per la stima delle preferenze umane basata sulla verosimiglianza di Bradley-Terry in [Python](https://www.python.org/) e [NumPy](https://numpy.org/). Il modello riceve coppie di risposte rappresentate da embedding sintetici, calcola i punteggi scalari $r_\psi(x, y_w)$ e $r_\psi(x, y_l)$, e ottimizza la separazione di margine tramite backpropagation vettorizzata e ottimizzazione Adam.

```python
import numpy as np
from typing import Tuple, Dict

class NeuralRewardModelNumPy:
    """Architettura neurale MLP a due livelli per la stima del Reward scalare in NumPy."""
    def __init__(self, embedding_dim: int = 64, hidden_dim: int = 128, seed: int = 42):
        rng = np.random.RandomState(seed)
        self.W1 = rng.randn(embedding_dim, hidden_dim) * np.sqrt(2.0 / embedding_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = rng.randn(hidden_dim, 1) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, 1))

    def forward(self, x: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """Forward pass con attivazione ReLU e caching per backpropagation."""
        z1 = np.dot(x, self.W1) + self.b1
        a1 = np.maximum(0, z1)
        scalar_reward = (np.dot(a1, self.W2) + self.b2).squeeze(-1)
        cache = {"x": x, "z1": z1, "a1": a1}
        return scalar_reward, cache

    def backward(self, d_reward: np.ndarray, cache: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Backpropagation dei gradienti rispetto ai pesi e bias dell'MLP."""
        x = cache["x"]
        z1 = cache["z1"]
        a1 = cache["a1"]

        d_out = d_reward.reshape(-1, 1)
        dW2 = np.dot(a1.T, d_out)
        db2 = np.sum(d_out, axis=0, keepdims=True)

        da1 = np.dot(d_out, self.W2.T)
        dz1 = da1 * (z1 > 0).astype(float)
        dW1 = np.dot(x.T, dz1)
        db1 = np.sum(dz1, axis=0, keepdims=True)

        return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}

class BradleyTerryRewardLoss:
    """Loss di preferenza a coppie: -E[log sigma(r(x, y_w) - r(x, y_l) - margin)]."""
    def __init__(self, margin: float = 0.0):
        self.margin = margin

    def compute_loss(self, rewards_chosen: np.ndarray, rewards_rejected: np.ndarray) -> Tuple[float, float, np.ndarray, np.ndarray]:
        diff = rewards_chosen - rewards_rejected - self.margin
        loss = float(np.mean(np.logaddexp(0, -diff)))
        accuracy = float(np.mean((rewards_chosen > rewards_rejected).astype(float)))

        sigma_neg_diff = 1.0 / (1.0 + np.exp(np.clip(diff, -50, 50)))
        d_diff = -sigma_neg_diff / len(diff)

        d_chosen = d_diff
        d_rejected = -d_diff
        return loss, accuracy, d_chosen, d_rejected

def generate_synthetic_preference_dataset(n_samples: int = 1200, dim: int = 64, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """Genera embedding sintetici in cui le risposte prescelte contengono un segnale positivo intrinseco."""
    rng = np.random.RandomState(seed)
    prompts = rng.randn(n_samples, dim) * 0.5
    chosen_noise = rng.randn(n_samples, dim) * 0.2
    chosen_noise[:, :10] += 0.8  # Segnale di qualità elevata
    rejected_noise = rng.randn(n_samples, dim) * 0.2
    rejected_noise[:, :10] -= 0.8 # Segnale di bassa qualità
    
    emb_chosen = prompts + chosen_noise
    emb_rejected = prompts + rejected_noise
    return emb_chosen, emb_rejected

if __name__ == "__main__":
    dim = 64
    n_samples = 1200
    emb_chosen, emb_rejected = generate_synthetic_preference_dataset(n_samples, dim, seed=42)

    # Split train / validation
    train_chosen, val_chosen = emb_chosen[:1000], emb_chosen[1000:]
    train_rejected, val_rejected = emb_rejected[:1000], emb_rejected[1000:]

    reward_model = NeuralRewardModelNumPy(embedding_dim=dim, hidden_dim=128, seed=42)
    criterion = BradleyTerryRewardLoss()
    
    # Ottimizzatore Adam
    lr = 1e-3
    beta1, beta2 = 0.9, 0.999
    eps = 1e-8
    m = {k: np.zeros_like(getattr(reward_model, k)) for k in ["W1", "b1", "W2", "b2"]}
    v = {k: np.zeros_like(getattr(reward_model, k)) for k in ["W1", "b1", "W2", "b2"]}
    t = 0

    print("=== ADDESTRAMENTO REWARD MODEL BRADLEY-TERRY ===")
    epochs = 15
    batch_size = 64

    for epoch in range(1, epochs + 1):
        perm = np.random.permutation(len(train_chosen))
        epoch_loss = 0.0
        epoch_acc = 0.0
        batches = 0

        for i in range(0, len(train_chosen), batch_size):
            t += 1
            idx = perm[i:i + batch_size]
            b_chosen = train_chosen[idx]
            b_rejected = train_rejected[idx]

            r_w, cache_w = reward_model.forward(b_chosen)
            r_l, cache_l = reward_model.forward(b_rejected)
            loss, acc, d_rw, d_rl = criterion.compute_loss(r_w, r_l)

            grads_w = reward_model.backward(d_rw, cache_w)
            grads_l = reward_model.backward(d_rl, cache_l)
            
            for k in ["W1", "b1", "W2", "b2"]:
                grad = grads_w[k] + grads_l[k]
                m[k] = beta1 * m[k] + (1.0 - beta1) * grad
                v[k] = beta2 * v[k] + (1.0 - beta2) * (grad ** 2)
                m_hat = m[k] / (1.0 - beta1 ** t)
                v_hat = v[k] / (1.0 - beta2 ** t)
                param = getattr(reward_model, k)
                param -= lr * m_hat / (np.sqrt(v_hat) + eps)
                setattr(reward_model, k, param)

            epoch_loss += loss
            epoch_acc += acc
            batches += 1

        if epoch % 3 == 0 or epoch == 1:
            val_rw, _ = reward_model.forward(val_chosen)
            val_rl, _ = reward_model.forward(val_rejected)
            val_loss, val_acc, _, _ = criterion.compute_loss(val_rw, val_rl)
            margin_mean = float(np.mean(val_rw - val_rl))
            print(f"Epoch {epoch:2d} | Train Loss: {epoch_loss/batches:.4f} | "
                  f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.1f}% | "
                  f"Mean Margin: {margin_mean:.3f}")
```

### Laboratorio 4: Implementazione della Direct Preference Optimization (DPO) Loss in NumPy

Questo laboratorio implementa la funzione di perdita esatta in forma chiusa di Direct Preference Optimization (DPO) in [Python](https://www.python.org/) e [NumPy](https://numpy.org/). Il codice calcola i log-ratio della policy rispetto alla reference policy, valuta i reward impliciti per sequenze prescelte e scartate, monitora la convergenza della perdita contrastiva e misura la divergenza implicita rispetto alla distribuzione originale.

```python
import numpy as np
from typing import Dict, Tuple

class DPOLossEngine:
    """
    Implementazione formale della Direct Preference Optimization (DPO) in NumPy.
    L_DPO = -E[log sigma(beta * log(pi(y_w|x)/pi_ref(y_w|x)) - beta * log(pi(y_l|x)/pi_ref(y_l|x)))]
    """
    def __init__(self, beta: float = 0.1, label_smoothing: float = 0.0):
        self.beta = beta
        self.label_smoothing = label_smoothing

    def compute_loss_and_gradients(
        self,
        policy_chosen_logps: np.ndarray,
        policy_rejected_logps: np.ndarray,
        reference_chosen_logps: np.ndarray,
        reference_rejected_logps: np.ndarray
    ) -> Tuple[Dict[str, float], Tuple[np.ndarray, np.ndarray]]:
        """
        Calcola la perdita DPO, le metriche diagnostiche e i gradienti analitici.
        Input: log-probabilità aggregate sulle sequenze (batch_size,)
        """
        # 1. Calcolo dei log-ratio per risposte prescelte (chosen) e scartate (rejected)
        pi_chosen_ratio = policy_chosen_logps - reference_chosen_logps
        pi_rejected_ratio = policy_rejected_logps - reference_rejected_logps

        # 2. Ricompense implicite calcolate in forma chiusa: r_theta(x, y) = beta * log(pi/pi_ref)
        implicit_rewards_chosen = self.beta * pi_chosen_ratio
        implicit_rewards_rejected = self.beta * pi_rejected_ratio

        # 3. Differenza contrastiva dei reward impliciti (logits)
        logits = implicit_rewards_chosen - implicit_rewards_rejected

        # 4. Calcolo della perdita DPO con log-sigmoide numericamente stabile
        log_sig_pos = -np.logaddexp(0, -logits)
        log_sig_neg = -np.logaddexp(0, logits)

        if self.label_smoothing > 0.0:
            loss_elements = -(log_sig_pos * (1.0 - self.label_smoothing) + log_sig_neg * self.label_smoothing)
        else:
            loss_elements = -log_sig_pos
        
        loss = float(np.mean(loss_elements))

        # 5. Metriche di monitoraggio
        accuracy = float(np.mean((implicit_rewards_chosen > implicit_rewards_rejected).astype(float)))
        reward_margin = float(np.mean(implicit_rewards_chosen - implicit_rewards_rejected))

        # 6. Gradienti analitici esatti rispetto ai parametri ottimizzabili
        sigma_pos = 1.0 / (1.0 + np.exp(np.clip(-logits, -50, 50)))
        d_loss_d_logits = -(1.0 - self.label_smoothing) * (1.0 - sigma_pos) + self.label_smoothing * sigma_pos
        d_loss_d_logits = d_loss_d_logits / len(logits)

        grad_policy_chosen = d_loss_d_logits * self.beta
        grad_policy_rejected = -d_loss_d_logits * self.beta

        metrics = {
            "loss": loss,
            "accuracy": accuracy,
            "reward_margin": reward_margin,
            "chosen_reward_mean": float(np.mean(implicit_rewards_chosen)),
            "rejected_reward_mean": float(np.mean(implicit_rewards_rejected))
        }
        gradients = (grad_policy_chosen, grad_policy_rejected)
        return metrics, gradients

if __name__ == "__main__":
    np.random.seed(42)
    batch_size = 128
    beta_param = 0.1

    # Definizione di parametri di policy simulati
    ref_chosen_logps = np.full((batch_size,), -15.0)
    ref_rejected_logps = np.full((batch_size,), -15.0)

    # Parametri ottimizzabili della policy
    policy_chosen_logps = ref_chosen_logps.copy() + np.random.randn(batch_size) * 0.1
    policy_rejected_logps = ref_rejected_logps.copy() + np.random.randn(batch_size) * 0.1

    dpo_engine = DPOLossEngine(beta=beta_param)
    
    # Ottimizzatore Adam in NumPy
    lr = 0.05
    m_chosen, v_chosen = np.zeros_like(policy_chosen_logps), np.zeros_like(policy_chosen_logps)
    m_rejected, v_rejected = np.zeros_like(policy_rejected_logps), np.zeros_like(policy_rejected_logps)
    beta1, beta2, eps = 0.9, 0.999, 1e-8

    print("=== OTTIMIZZAZIONE DIRETTA DELLE PREFERENZE (DPO) ===")
    print("Addestramento della policy per massimizzare il log-ratio implicito:")

    for step in range(1, 21):
        metrics, (g_chosen, g_rejected) = dpo_engine.compute_loss_and_gradients(
            policy_chosen_logps=policy_chosen_logps,
            policy_rejected_logps=policy_rejected_logps,
            reference_chosen_logps=ref_chosen_logps,
            reference_rejected_logps=ref_rejected_logps
        )

        # Aggiornamento policy con Adam
        m_chosen = beta1 * m_chosen + (1 - beta1) * g_chosen
        v_chosen = beta2 * v_chosen + (1 - beta2) * (g_chosen ** 2)
        m_c_hat = m_chosen / (1 - beta1 ** step)
        v_c_hat = v_chosen / (1 - beta2 ** step)
        policy_chosen_logps -= lr * m_c_hat / (np.sqrt(v_c_hat) + eps)

        m_rejected = beta1 * m_rejected + (1 - beta1) * g_rejected
        v_rejected = beta2 * v_rejected + (1 - beta2) * (g_rejected ** 2)
        m_r_hat = m_rejected / (1 - beta1 ** step)
        v_r_hat = v_rejected / (1 - beta2 ** step)
        policy_rejected_logps -= lr * m_r_hat / (np.sqrt(v_r_hat) + eps)

        if step % 5 == 0 or step == 1:
            print(f"Step {step:2d} | DPO Loss: {metrics['loss']:.4f} | "
                  f"Accuracy: {metrics['accuracy'] * 100:5.1f}% | "
                  f"Implicit Margin: {metrics['reward_margin']:+.4f} | "
                  f"r(y_w): {metrics['chosen_reward_mean']:+.3f} | "
                  f"r(y_l): {metrics['rejected_reward_mean']:+.3f}")
```