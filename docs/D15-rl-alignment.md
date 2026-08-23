---
aliases:
- D15
- Reinforcement Learning
- Alignment
- RLHF
- DPO
- PPO
- Preference Learning
resources:
- title: Illustrating RLHF (HuggingFace Blog)
  url: https://huggingface.co/blog/rlhf
  type: ref
---
# Reinforcement Learning, Preference Optimization e Allineamento dei Modelli Linguistici

L'allineamento dei modelli linguistici rappresenta l'insieme delle metodologie matematiche, computazionali e di ottimizzazione mirate a orientare lo spazio di generazione probabilistica di una rete neurale verso obiettivi di utilità, fedeltà fattuale e sicurezza determinati dall'essere umano. Questa disciplina trova applicazione fondamentale nella post-elaborazione di modelli di frontiera, assistenti conversazionali, sistemi agentici autonomi e pipeline di intelligence OSINT ad alta affidabilità in cui il comportamento del modello deve rimanere rigoroso, controllabile e privo di derive allucinatorie. La necessità dell'allineamento nasce dal limite strutturale del pre-addestramento auto-regressivo: la pura massimizzazione della verosimiglianza statistica sul prossimo token premia la mera imitazione della distribuzione linguistica del web, riflettendo bias, errori logici, contenuti dannosi e strategie persuasive ingannevoli che rendono indispensabile un secondo stadio di ottimizzazione guidato da funzioni di preferenza e ricompensa esplicite.

## Il Problema dell'Allineamento: Oltre il Next-Token Prediction e la Divergenza tra Probabilità Statistica e Utilità Umana

> [!TIP] Spiegato Semplice: Il Pappagallo Enciclopedico e il Compito in Classe
> Immagina uno studente prodigio che ha trascorso anni rinchiuso in una biblioteca infinita, leggendo e memorizzando ogni singola pagina di Internet: dai trattati scientifici ai litigi sui forum, passando per fake news, ricette, romanzi e codici pieni di falle. 
> Se gli mostri l'inizio di una frase come *"Come si entra in una casa senza chiavi..."*, il suo istinto statistico è completare il testo imitando ciò che ha letto più spesso online (magari descrivendo come scassinare una porta o inventando una scena da film poliziesco). 
> Il pappagallo non sa cosa sia "giusto", "educato" o "sicuro": sa solo quale parola statisticamente viene dopo un'altra. L'allineamento è l'addestramento speciale che trasforma questo pappagallo enciclopedico in un assistente responsabile, capace di capire l'intenzione umana e rispondere con utilità, precisione e sicurezza.

I modelli linguistici di grandi dimensioni vengono addestrati principalmente mediante l'obiettivo di modellazione linguistica causale (*Causal Language Modeling*, CLM), ottimizzando la cross-entropy empirica su enormi moli di testo non strutturato. La funzione di perdita di pre-addestramento è formalizzata come:

$$\mathcal{L}_{CLM}(\theta) = - \mathbb{E}_{x \sim \mathcal{D}} \left[ \sum_{t=1}^T \log P_\theta(x_t \mid x_{<t}) \right]$$

Mappando i simboli matematici con la nostra metafora:
- $\mathcal{L}_{CLM}(\theta)$ rappresenta la **penalità di sorpresa**: quantifica quanto i parametri $\theta$ della rete neurale rimangono "sorpresi" dalle parole reali incontrate nel testo. L'obiettivo dell'addestramento è azzerare questa sorpresa.
- $\mathbb{E}_{x \sim \mathcal{D}}$ indica la **media su tutta la biblioteca**: il valore atteso calcolato scorrendo tutti i testi $x$ presenti nel gigantesco archivio web $\mathcal{D}$.
- $\sum_{t=1}^T$ è il **contatore sequenziale dei token**: la somma passo dopo passo dal primo istante temporale $t=1$ fino alla lunghezza totale $T$ del documento.
- $P_\theta(x_t \mid x_{<t})$ è la **probabilità del prossimo vocabolo**: la frazione di probabilità con cui la rete $\theta$ assegna la parola successiva corretta $x_t$, condizionata esclusivamente dalla storia pregressa $x_{<t}$ (il contesto già letto).
- $-\log(\dots)$ è la **scala di penalità**: se il modello assegna probabilità $1.0$ ($100\%$) alla parola corretta, $-\log(1) = 0$ (nessun errore); se assegna una probabilità prossima a $0$, la penalità tende a infinito.

Tuttavia, la sequenza di token che massimizza la pura probabilità statistica non coincide quasi mai con la risposta ottimale secondo criteri di utilità, veridicità e sicurezza. Internet include testi contraddittori, disinformazione e contenuti tossici; di conseguenza, un modello puramente pre-addestrato eccelle nel completare un testo simulando qualsiasi autore statistico, ma fallisce quando deve agire come un assistente coerente, onesto e innocuo (*Helpful, Honest, Harmless*).

Il primo tentativo di mitigare questo divario consiste nel **Supervised Fine-Tuning (SFT)**, ovvero l'addestramento supervisionato su coppie composte da istruzioni fornite dall'utente e risposte ideali redatte da annotatori umani. Sebbene l'SFT trasformi il generatore di testo grezzo in un modello capace di seguire istruzioni, manifesta due limiti strutturali:
1. **Exposure Bias e Accumulo dell'Errore**: Durante il training SFT il modello vede solo traiettorie perfette scritte da esperti umani. Durante l'inferenza reale, se genera un token sub-ottimale al terzo passo, si trova in uno stato inedito e l'errore si amplifica a valanga (*compounding error*) senza possibilità di correzione autonoma.
2. **Costi e Scalabilità**: Scrivere risposte perfette per decine di migliaia di argomenti complessi richiede costi e tempi insostenibili. Al contrario, per gli esseri umani è immensamente più semplice e rapido confrontare due risposte generate dal modello e indicare quale sia la migliore.

L'allineamento emerge quindi come la transizione formale dall'apprendimento imitativo all'**ottimizzazione per preferenze**, trattando la generazione come un processo decisionale sequenziale nello spazio delle risposte.

> [!INTERACTIVE] WIDGET: Il Predittore del Web vs L'Assistente Allineato
> **Tipo:** Simulatore Dinamico di Completamento con Bivio Semantico.
> **Descrizione Interfaccia:**
> - Un pannello superiore consente di inserire un prompt ambiguo (es. *"Come esaminare le vulnerabilità di rete di un'infrastruttura..."*).
> - Uno slider centrale consente di dosare il livello di allineamento: da `0% (Puro Web Predictor)` a `100% (Allineato OSINT/Ethical)`.
> - Un grafo ad albero probabilistico mostra in tempo reale la biforcazione dei token: a `0%`, l'albero si orienta verso snippet di exploit grezzi con punteggio CLM elevato ma pericolosi; a `100%`, i pesi di preferenza penalizzano le ramificazioni offensive e promuovono token focalizzati su metodologie di audit difensivo e analisi di sicurezza.
> - Metriche dinamiche visualizzate: *Tossicità Prevista*, *Utilità Formativa* e *Log-Verosimiglianza CLM*.

## Fondamenti Matematici dell'Apprendimento per Rinforzo: MDP, Equazioni di Bellman e Policy Gradient

> [!TIP] Spiegato Semplice: Il Videogioco di Avventura Testuale e la Stanza dei Tesori
> Immagina un giocatore all'interno di un'avventura grafica o di un gioco di ruolo a bivi:
> - **Lo Stato ($s_t$)**: è la stanza in cui ti trovi, ovvero tutto il testo accumulato finora (la domanda iniziale più tutte le parole già pronunciate).
> - **L'Azione ($a_t$)**: è la mossa che decidi di fare, ovvero pescare la prossima parola da un mazzo di oltre 100.000 vocaboli disponibili nel vocabolario.
> - **L'Ambiente e la Transizione ($\mathcal{P}$)**: è il motore di gioco, che prende la tua parola e la incolla subito dopo la frase precedente, facendoti avanzare nella stanza successiva.
> - **La Ricompensa ($\mathcal{R}$)**: è il punteggio in monete d'oro che ricevi alla fine della missione (un punteggio elevato per una spiegazione brillante, una penalità se hai detto una frase scorretta o dannosa).
> - **Il Fattore di Sconto ($\gamma$)**: è la tua "pazienza": preferisci una moneta subito o sei disposto a fare frasi articolate per incassare un tesoro alla fine del discorso?

Per formalizzare l'allineamento all'interno della teoria delle decisioni, la generazione di testo viene espressa come un **Processo Decisionale di Markov (MDP)**, formalizzato classicamente tramite la quintupla $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$:
- $\mathcal{S}$ (Spazio degli Stati): lo stato $s_t = (x, y_1, y_2, \dots, y_{t-1})$ corrisponde alla concatenazione del prompt $x$ e dei token precedentemente generati.
- $\mathcal{A}$ (Spazio delle Azioni): l'azione $a_t = y_t \in \mathcal{V}$ coincide con la selezione del token successivo nel vocabolario discreto $\mathcal{V}$.
- $\mathcal{P}(s_{t+1} \mid s_t, a_t)$ (Dinamica di Transizione): deterministica, coincidente con l'append del token selezionato: $s_{t+1} = (s_t, a_t)$.
- $\mathcal{R}(s, a)$ (Funzione di Ricompensa): segnale scalare associato alla qualità della transizione.
- $\gamma \in [0, 1]$ (Fattore di Sconto): parametro che pondera l'importanza dei ritorni futuri rispetto a quelli immediati.
- $\pi_\theta(a_t \mid s_t)$ (Policy): la distribuzione categorica definita dai pesi $\theta$ della rete neurale attraverso lo strato Softmax sul vocabolario.

La funzione di valore di stato $V^\pi(s)$ stima il ritorno cumulativo atteso a partire dallo stato $s$ sotto la policy $\pi$. Come formalizzato nelle opere fondamentali di [Richard Sutton](http://incompleteideas.net/) (il professore emerito all'Università di Alberta e distinguished research scientist di [Google DeepMind](https://deepmind.google/) considerato il padre fondatore del Reinforcement Learning moderno) e [Andrew Barto](https://people.cs.umass.edu/~barto/) (il professore emerito all'Università del Massachusetts Amherst e coautore del testo cardine sull'apprendimento per rinforzo), il valore di uno stato soddisfa l'**Equazione di Aspettazione di Bellman**:

$$V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) \left[ \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) V^\pi(s') \right]$$

Traduzione dei simboli dalla metafora:
- $V^\pi(s)$: il "valore strategico" di trovarsi nella stanza $s$ (frase fin qui) continuando a giocare con la strategia $\pi$.
- $\sum_{a \in \mathcal{A}} \pi(a \mid s)$: la media ponderata su tutte le possibili parole $a$ che il giocatore potrebbe scegliere moltiplicate per la loro probabilità.
- $\mathcal{R}(s, a)$: la ricompensa immediata ottenuta pronunciando la parola $a$ nello stato $s$.
- $\gamma \sum_{s'} \mathcal{P}(s' \mid s, a) V^\pi(s')$: il valore scontato della nuova stanza $s'$ in cui il modello atterra dopo aver aggiunto la parola.

Quando il giocatore adotta la strategia ottima $\pi^*$, il valore soddisfa l'**Equazione di Ottimalità di Bellman** per la funzione di valore stato-azione $Q^*(s, a)$:

$$Q^*(s, a) = \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \max_{a' \in \mathcal{A}} Q^*(s', a')$$

- $Q^*(s, a)$: il massimo punteggio ottenibile compiendo l'azione specifica $a$ nello stato $s$ e poi giocando sempre in modo impeccabile nei turni successivi.
- $\max_{a'} Q^*(s', a')$: la migliore scelta possibile che il giocatore potrà compiere nella stanza successiva $s'$.

Negli spazi continui e ad altissima dimensionalità dei modelli linguistici, dove il vocabolario supera comunemente le centomila unità e la lunghezza della sequenza raggiunge migliaia di passi, calcolare esplicitamente la tabella dei valori tramite programmazione dinamica è impossibile. Si ricorre quindi ai metodi **Policy Gradient**, ottimizzando direttamente i parametri $\theta$ della rete neurale per massimizzare il ritorno atteso $J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [R(\tau)]$ lungo le traiettorie $\tau = (s_0, a_0, s_1, a_1, \dots, s_T)$.

> [!TIP] Spiegato Semplice: Il Coach di Tiro con l'Arco e il Vantaggio
> Immagina un coach che allena un arciere. L'arciere scaglia centinaia di frecce verso il bersaglio (traiettorie $\tau$). Il coach non calcola la traiettoria fisica millimetrica di ogni muscolo, ma osserva il risultato finale:
> - Se una freccia fa centro meglio della media abituale, il coach ordina: *"Ottimo, rafforza quel movimento!"* (**Vantaggio Positivo**).
> - Se una freccia finisce fuori bersaglio rispetto alla media, il coach ordina: *"Movimento errato, riducine la frequenza!"* (**Vantaggio Negativo**).

Il **Teorema del Gradiente della Policy** stabilisce che il gradiente dell'obiettivo rispetto ai pesi non richiede la differenziazione della dinamica dell'ambiente:

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t \mid s_t) \hat{A}_t \right]$$

dove $\hat{A}_t = Q(s_t, a_t) - V(s_t)$ rappresenta la **funzione di vantaggio (Advantage Function)**:
- $\nabla_\theta J(\theta)$: la direzione matematica lungo cui modificare i pesi $\theta$ per incrementare la ricompensa totale attesa.
- $\mathbb{E}_{\tau \sim \pi_\theta}$: la media calcolata su un batch di risposte complete campionate dalla policy attuale.
- $\nabla_\theta \log \pi_\theta(a_t \mid s_t)$: il vettore di spinta che incrementa la probabilità di emissione della parola $a_t$ a partire dallo stato $s_t$.
- $\hat{A}_t = Q(s_t, a_t) - V(s_t)$: il termometro del vantaggio. Misura se la parola scelta $a_t$ è stata superiore ($A_t > 0$) o inferiore ($A_t < 0$) rispetto al valore medio atteso $V(s_t)$ in quello stato, riducendo drasticamente la varianza statistica del gradiente.

> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D13-rl-alignment. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.

> [!INTERACTIVE] WIDGET: Il Labirinto di Bellman e il Termometro del Vantaggio
> **Tipo:** Mini-gioco a Griglia Decisionale e Calcolatore di Ritorno Scontato.
> **Descrizione Interfaccia:**
> - Una griglia interattiva 4x4 (GridWorld) con caselle di partenza, trappole con penalità ($-10$), caselle standard di passo ($-1$) e obiettivo finale con ricompensa ($+10$).
> - Un cursore interattivo permette di modificare in tempo reale il fattore di sconto $\gamma$ da $0.0$ (agente miope) a $0.99$ (agente lungimirante).
> - Cliccando su qualsiasi casella $s$, il widget calcola istantaneamente il valore di stato $V(s)$, i valori $Q(s, a)$ per le 4 direzioni (Su, Giù, Sinistra, Destra) e mostra la freccia della policy ottima $\pi^*(s)$.
> - Un modulo "Advantage Heatmap" colora in verde le azioni con vantaggio $\hat{A}_t > 0$ e in rosso quelle con vantaggio sub-ottimale, mostrando numericamente come il gradiente spinga la policy verso le scelte corrette.

## L'Architettura RLHF Tradizionale: Supervised Fine-Tuning, Reward Modeling e Ottimizzazione PPO con Penalty KL

> [!TIP] Spiegato Semplice: Il Talent Show Gastronomico e il Cane al Guinzaglio
> 1. **La Sfida dei Cuochi (Reward Model & Bradley-Terry)**: Immagina due chef che cucinano due piatti diversi per lo stesso ordine (prompt $x$). Un giudice umano li assaggia: non assegna un voto numerico astratto (è difficile dire se un piatto vale 8.42 o 8.45), ma stabilisce subito quale piatto vince ($y_w$) e quale perde ($y_l$). Con centinaia di questi confronti a coppie, addestriamo un "critico gastronomico artificiale" (il Reward Model) che impara a prevedere quale piatto piacerà di più agli umani.
> 2. **Il Cane al Guinzaglio Elastico (Penalità KL)**: Se un cane viene addestrato solo per ricevere biscotti (punti dal Reward Model), scoprirà un trucco furbo (*Reward Hacking*): farà capriole continue o abbaierà a raffica perché il distributore automatico ha un difetto nei sensori e premia il rumore continuo. Per evitare che il modello linguistico impari frasi senza senso o elenchi infiniti pur di ingannare il Reward Model, lo colleghiamo con un guinzaglio elastico al modello educato originale ($\pi_{ref}$). Se cerca di allontanarsi troppo dal parlare corretto, il guinzaglio tira indietro con forza proporzionale a $\beta$.
> 3. **Le Barriere di Protezione della Pista (PPO Clipping)**: Quando guidi su un tracciato, non puoi sterzare bruscamente al $100\%$ in una frazione di secondo. L'algoritmo PPO impedisce che la strategia cambi più del $20\%$ per singolo passo, evitando che il modello dimentichi all'improvviso tutto ciò che sapeva.

La metodologia standard di **Reinforcement Learning from Human Feedback (RLHF)**, resa celebre dallo studio [InstructGPT](https://arxiv.org/abs/2203.02155) condotto da [OpenAI](https://openai.com/) (la società di ricerca e sviluppo sull'intelligenza artificiale creatrice dei modelli GPT), si struttura in una pipeline sequenziale a tre fasi distinte: Supervised Fine-Tuning, addestramento del Reward Model e ottimizzazione tramite Proximal Policy Optimization.

Nel primo stadio, il modello base viene convertito in una policy iniziale $\pi^{SFT}$ tramite addestramento supervisionato su dimostrazioni di alta qualità. 

Nel secondo stadio, per ogni prompt $x$ estratto da un dataset di distribuzione operativa, il modello genera due o più risposte alternative $(y_1, y_2)$. Un gruppo di annotatori umani valuta le generazioni ordinandole per preferenza, producendo coppie binarie formate da una risposta preferita $y_w$ (*winner*) e una risposta scartata $y_l$ (*loser*). La preferenza umana viene formalizzata matematicamente tramite il **modello logistico di Bradley-Terry**:

$$P(y_w \succ y_l \mid x) = \sigma(r_\psi(x, y_w) - r_\psi(x, y_l)) = \frac{1}{1 + e^{-(r_\psi(x, y_w) - r_\psi(x, y_l))}}$$

dove $r_\psi(x, y)$ è una rete neurale parametrizzata da $\psi$ (il **Reward Model**) che riceve in input la concatenazione di prompt e risposta e produce uno scalare indicante la qualità. I pesi $\psi$ del modello di ricompensa vengono ottimizzati minimizzando la perdita di entropia incrociata binaria su tutte le coppie del dataset di preferenze $\mathcal{D}$:

$$\mathcal{L}_{RM}(\psi) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma\left( r_\psi(x, y_w) - r_\psi(x, y_l) \right) \right]$$

Traduzione dei simboli dalla metafora culinaria:
- $P(y_w \succ y_l \mid x)$: la probabilità che il piatto vincitore $y_w$ superi il piatto perdente $y_l$ a fronte della richiesta $x$.
- $r_\psi(x, y_w)$ e $r_\psi(x, y_l)$: i punteggi di gradimento assegnati dal critico artificiale alle due risposte.
- $\sigma(z) = \frac{1}{1+e^{-z}}$: la curva sigmoide che converte il divario di punteggio in una probabilità compresa tra $0$ e $1$ (se il divario è nullo, la probabilità è $0.5$).
- $\mathcal{L}_{RM}(\psi)$: la penalità di giudizio. Si azzera se il Reward Model assegna sistematicamente a $y_w$ un punteggio sensibilmente superiore rispetto a $y_l$.

Nel terzo stadio, la policy $\pi_\theta$ viene aggiornata tramite l'algoritmo **Proximal Policy Optimization (PPO)**. Se la policy venisse ottimizzata unicamente per massimizzare il punteggio scalare del Reward Model, il modello incorrerebbe rapidamente nel **reward hacking**: sfrutterebbe le imperfezioni e i punti ciechi del Reward Model producendo testo incomprensibile, ripetitivo o artificialmente prolisso pur di ottenere punteggi elevati. Per prevenire questa deriva, la funzione di ricompensa totale include una penalità basata sulla **divergenza di Kullback-Leibler (KL)** rispetto alla policy di riferimento immutabile $\pi_{ref}$ (inizializzata con $\pi^{SFT}$):

$$R_{total}(x, y) = r_\psi(x, y) - \beta D_{KL}\left(\pi_\theta(y \mid x) \parallel \pi_{ref}(y \mid x)\right) = r_\psi(x, y) - \beta \left( \log \pi_\theta(y \mid x) - \log \pi_{ref}(y \mid x) \right)$$

- $R_{total}(x, y)$: la ricompensa netta percepita dall'agente.
- $r_\psi(x, y)$: il punteggio assegnato dal Reward Model.
- $\beta$: il coefficiente di rigidità del guinzaglio elastico (parametro di ancoraggio KL).
- $D_{KL}(\pi_\theta \parallel \pi_{ref})$: la misura di distanza distributiva tra il nuovo modello che apprende $\pi_\theta$ e il modello di riferimento originale $\pi_{ref}$.

La policy viene quindi aggiornata massimizzando l'obiettivo surrogato con clipping di PPO per prevenire aggiornamenti distruttivi della policy:

$$\mathcal{L}_{PPO}^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

dove $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$ rappresenta il rapporto di verosimiglianza tra la policy corrente e quella precedente, ed $\epsilon$ è un iperparametro di tolleranza (tipicamente impostato a $0.2$).

Nonostante l'efficacia dimostrata in produzione, l'architettura RLHF tradizionale impone una complessità infrastrutturale gravosa: richiede di mantenere contemporaneamente in memoria VRAM ben **quattro modelli** della stessa scala (la policy attiva $\pi_\theta$, la reference policy congelata $\pi_{ref}$, il Reward Model $r_\psi$ e il Critic $V_\phi$), con rollouts continui e frequenti instabilità numeriche.

> [!INTERACTIVE] WIDGET: Il Guinzaglio KL e il Simulatore di Reward Hacking PPO
> **Tipo:** Laboratorio di Controllo Iperparametri e Diagnostica Deriva.
> **Descrizione Interfaccia:**
> - Cursori interattivi: `Coefficiente KL Beta` ($0.0 \to 0.5$) e `Clip Range Epsilon` ($0.05 \to 0.4$).
> - Simulazione dinamica di 50 iterazioni di training PPO su un set di prompt campione.
> - Tre grafici sincronizzati in tempo reale:
>   1. *Curva del Reward Model:* sale rapidamente.
>   2. *Indice di Fluidità e Coerenza Linguistica:* se $\beta \to 0$, la coerenza crolla a picco (insorge il Reward Hacking con ripetizioni compulsive di parole adulatorie o elenchi infiniti).
>   3. *Divergenza KL:* traccia la distanza tra la policy attiva e la reference policy.
> - Finestra di anteprima del testo generato per visualizzare l'effetto immediato dei valori di $\beta$: testo allucinato/hackerato vs testo fluido e rigoroso.

## La Semplificazione ad Alta Efficienza: Direct Preference Optimization (DPO) e Formulazione in Forma Chiusa

> [!TIP] Spiegato Semplice: La Bilancia a Due Piatti (Eliminare l'Arbitro Intermedio)
> Immagina una gara in cui, per decretare il piatto migliore, prima dovevi assumere un critico a tempo pieno, costruirgli un ufficio (allocare un modello di Reward e un Critic in GPU), fargli dare i voti a ogni boccone e sincronizzare calcoli complessi ogni secondo.
> I ricercatori di Stanford hanno scoperto una scorciatoia matematica geniale: *il modello linguistico stesso contiene già al suo interno un critico implicito!*
> È come avere una bilancia a due piatti: per sapere quale risposta è migliore, non serve misurare il peso assoluto in grammi con uno strumento esterno. Basta mettere la risposta preferita su un piatto, la risposta scartata sull'altro, e verificare direttamente quanto il modello attuale preferisce la prima rispetto alla seconda rispetto alla sua "memoria storica" di partenza. In questo modo si elimina del tutto la necessità del Reward Model separato e dell'addestramento PPO online!

Per superare la complessità operativa e l'instabilità del loop Actor-Critic di PPO, i ricercatori della [Stanford University](https://www.stanford.edu/) (la prestigiosa università di ricerca della California, centro accademico cardine per l'informatica e l'AI) hanno introdotto la [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) (DPO, Rafailov et al., 2023). La DPO dimostra matematicamente che il problema di massimizzazione del reward vincolato dalla divergenza KL ammette una soluzione esatta in forma chiusa.

L'obiettivo teorico di allineamento sotto vincolo di divergenza KL è espresso come:

$$\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot \mid x)} \left[ r(x, y) \right] - \beta D_{KL}\left(\pi_\theta(y \mid x) \parallel \pi_{ref}(y \mid x)\right)$$

Applicando il calcolo delle variazioni e imponendo che la distribuzione sommi a uno su tutto lo spazio delle risposte, la policy ottimale $\pi^*$ assume la forma della **distribuzione di Gibbs**:

$$\pi^*(y \mid x) = \frac{1}{Z(x)} \pi_{ref}(y \mid x) \exp\left( \frac{1}{\beta} r(x, y) \right)$$

dove $Z(x) = \sum_y \pi_{ref}(y \mid x) \exp\left( \frac{1}{\beta} r(x, y) \right)$ è la funzione di partizione dipendente esclusivamente dal prompt. Riorganizzando algebricamente l'equazione per isolare il reward $r(x, y)$, si ottiene la formulazione della **ricompensa implicita**:

$$r(x, y) = \beta \log \frac{\pi^*(y \mid x)}{\pi_{ref}(y \mid x)} + \beta \log Z(x)$$

Sostituendo questa espressione esatta del reward all'interno della verosimiglianza di preferenza di Bradley-Terry $P(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l))$, il termine di partizione $\beta \log Z(x)$, essendo identico per entrambe le risposte generate dallo stesso prompt $x$, **si cancella perfettamente per sottrazione**:

$$r(x, y_w) - r(x, y_l) = \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)}$$

Sostituendo questa differenza direttamente nella funzione di perdita del modello di preferenza, si ottiene la **funzione di perdita in forma chiusa di DPO**:

$$\mathcal{L}_{DPO}(\theta; \pi_{ref}) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)} \right) \right]$$

Traduzione dei simboli dalla metafora della bilancia a piatti:
- $\mathcal{L}_{DPO}(\theta; \pi_{ref})$: la perdita complessiva di DPO. Si ottimizza con una classica discesa del gradiente come una semplice cross-entropy su dataset statico.
- $\beta$: il coefficiente di contrasto. Regola la pendenza con cui premiamo la risposta preferita e freniamo le derive rispetto alla base.
- $\frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)}$: il piatto della risposta vincente $y_w$. Misura di quanto il modello in addestramento ha aumentato la probabilità di questa risposta rispetto alla versione di partenza $\pi_{ref}$.
- $\frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)}$: il piatto della risposta scartata $y_l$. Misura il rapporto di probabilità per la risposta indesiderata.
- La differenza tra i due rapporti logaritmici misura il margine netto. Se il modello privilegia la risposta vincente e deprime quella scartata, l'argomento della sigmoide diventa un numero positivo grande, $\sigma \to 1$, e la perdita si azzera.

L'impatto ingegneristico di DPO è profondo. L'infrastruttura di training richiede soltanto **due modelli** caricati in memoria: la policy che viene ottimizzata e la reference policy congelata (la quale può essere memorizzata con quantizzazione a 4-bit tramite [PEFT](https://huggingface.co/docs/peft) (la libreria di Hugging Face per l'adattamento efficiente dei parametri) per risparmiare memoria). Non vi sono reti Critic, non si eseguono generazioni durante l'addestramento e il processo si riduce a un efficiente calcolo vettoriale implementabile tramite librerie standard come [TRL](https://huggingface.co/docs/trl) (la libreria di Hugging Face per l'allineamento di modelli linguistici tramite RLHF, DPO e PPO) su [PyTorch](https://pytorch.org/) (il framework open-source di deep learning e differenziazione automatica).

> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.

> [!INTERACTIVE] WIDGET: La Bilancia a Contrasto DPO vs Il Complesso Loop PPO
> **Tipo:** Confronto di Architettura Interattivo e Simulatore di Margine Contrastivo.
> **Descrizione Interfaccia:**
> - Vista Split-Screen:
>   - *A Sinistra (Architettura PPO):* Mostra 4 blocchi di memoria GPU (Actor, Critic, Reward Model, Reference Model), con frecce animate per campionamento, calcolo dei vantaggi GAE e step di policy update. Viene evidenziato l'elevato consumo di VRAM (~80 GB per un 7B model).
>   - *A Destra (Architettura DPO):* Mostra solo 2 blocchi di memoria (Policy e Ref congelata con quantizzazione LoRA a 4-bit), con flusso diretto da dataset statico a loss vettorializzata (~24 GB VRAM).
> - Pannello Interattivo: Permette di regolare la probabilità assegnata a $y_w$ e a $y_l$ e visualizzare i vettori di gradiente analitici: un vettore verde spinge verso l'alto la verosimiglianza di $y_w$ e un vettore rosso deprime $y_l$, con ampiezza modulata dal parametro $\beta$.

## Tecniche Emergenti: Constitutional AI, RLAIF, KTO e Allineamento Senza Preferenze a Coppie

> [!TIP] Spiegato Semplice: Il Grillo Parlante Costituzionale e la Paura di Sbagliare
> 1. **Constitutional AI & RLAIF (Il Grillo Parlante e l'Autocritica)**: Immagina uno scrittore che tiene sempre sul tavolo un libretto di principi inviolabili (la "Costituzione": es. non incitare all'odio, non aiutare i criminali, sii accurato). Quando riceve una domanda rischiosa, scrive una prima bozza istintiva; poi indossa i panni del critico severo, individua dove ha violato i principi (*Critique*) e riscrive la bozza correggendola (*Revision*). Un secondo modello AI funge da supervisore (*AI Feedback*), eliminando la necessità di assumere migliaia di annotatori umani per ogni revisione.
> 2. **KTO e l'Avversione alle Perdite (La Psicologia di Kahneman e Tversky)**: Immagina di andare al ristorante. Se il piatto è buono, provi una soddisfazione moderata (+1 punto). Ma se trovi un capello nel piatto, la tua reazione negativa è sproporzionata (-10 punti!). Gli psicologi Daniel Kahneman e Amos Tversky hanno dimostrato che gli esseri umani detestano le perdite molto più di quanto amino i guadagni (*Loss Aversion*). L'algoritmo KTO sfrutta questa asimmetria: non richiede coppie ordinate di risposte $(y_w, y_l)$, ma accetta singoli esempi con un semplice pollice in su 👍 o in giù 👎, punendo severamente le risposte bocciate.

L'evoluzione delle tecniche di allineamento ha sviluppato paradigmi mirati a ridurre la dipendenza dagli annotatori umani e a superare la necessità di dataset strutturati a coppie binarie.

La metodologia di **Constitutional AI**, ideata da [Anthropic](https://www.anthropic.com/) (la società di sicurezza e ricerca AI creatrice dei modelli Claude e del [Model Context Protocol](https://modelcontextprotocol.io/) per l'interazione standardizzata tra modelli e strumenti), introduce il concetto di **Reinforcement Learning from AI Feedback (RLAIF)**. Il processo si articola in due momenti chiave:
1. **Critique and Revision**: Il modello genera una risposta a una richiesta critica, produce una critica formale confrontando il testo con i principi costituzionali espliciti e genera autonomamente una versione revisionata e sicura.
2. **AI Supervision**: Un modello supervisore valuta le coppie di risposte generate assegnando preferenze sintetiche su cui viene addestrato il Reward Model o eseguita la DPO, garantendo regole di sicurezza trasparenti, documentabili e ispezionabili formalmente.

Un'altra innovazione teorica è rappresentata da **Kahneman-Tversky Optimization (KTO)**. KTO elimina l'obbligo di generare e accoppiare due risposte per lo stesso prompt $x$, operando su dataset di singoli esempi etichettati unicamente con segnali binari di approvazione o rifiuto (desiderabile/indesiderabile). La funzione di perdita di KTO modella direttamente la funzione di valore asimmetrica della *prospect theory*: la disutilità per una risposta errata o dannosa supera quantitativamente l'utilità di una risposta corretta, consentendo un allineamento rapido a partire da log operativi reali (come click, upvote o downvote degli utenti).

Altre varianti emergenti includono:
- **Identity Preference Optimization (IPO)**: Introduce una regolarizzazione quadratica sulla perdita di DPO per prevenire il collasso sui log-ratio quando le preferenze del dataset sono deterministiche.
- **Odds Ratio Preference Optimization (ORPO)**: Integra la penalità di allineamento direttamente all'interno dello strato di Supervised Fine-Tuning tramite un termine di odds-ratio, eliminando del tutto la necessità di mantenere in memoria la reference policy.

> [!INTERACTIVE] WIDGET: Il Ciclo Critica-Revisione di Constitutional AI e la Curva Asimmetrica KTO
> **Tipo:** Simulatore Multi-Paradigma a Schede Interattive.
> **Descrizione Interfaccia:**
> - **Scheda 1 (Constitutional AI Pipeline):** L'utente seleziona un principio (es. *"Principio di Non-Proliferazione di Informazioni Malevole"*). Inserendo un prompt, il widget anima i 3 passaggi sequenziali: `1. Generazione Bozza Grezza` $\to$ `2. Generazione Critica Costituzionale Automatica` $\to$ `3. Riformulazione Revisionata Sicura`.
> - **Scheda 2 (Curva di Utilità Kahneman-Tversky):** Grafico dinamico che traccia la curva di guadagno/perdita di KTO. L'utente muove un cursore di gradimento: nella regione positiva (risposte buone), la curva cresce con pendenza moderata; nella regione negativa (risposte indesiderate), la curva crolla con pendenza tripla, evidenziando il meccanismo matematico di contrasto asimmetrico.

## Trade-off Ingegneristici e Limiti Operativi: Alignment Tax, Reward Hacking, Modal Collapse e Instabilità di Training

> [!TIP] Spiegato Semplice: Il Pilota con il Limitatore e lo Studente Adulatore
> - **L'Alignment Tax (Il Pilota con il Limitatore)**: Immagina un'auto da corsa a cui viene installato un limitatore elettronico a 40 km/h per garantire che non faccia mai incidenti in città. L'auto è diventata sicura al 100%, ma se la porti in pista per una gara di Formula 1 non riuscirà più a correre. Nei modelli linguistici, un allineamento troppo aggressivo può danneggiare le capacità di ragionamento logico puro, matematica e codice complesso.
> - **Reward Hacking e Sycophancy (Lo Studente Adulatore)**: È lo studente che non conosce la risposta al compito in classe, ma sa che l'insegnante ama i complimenti e i temi lunghi 10 pagine: scrive un testo chilometrico (*Verbosity Bias*) dando sempre ragione alle opinioni dell'esaminatore anche se palesemente errate (*Sycophancy*), solo per massimizzare il voto superficiale del giudice.
> - **Over-refusal (La Guardia Troppo Rigida)**: È il custode che vieta l'ingresso a un medico in ospedale solo perché ha sentito la parola "malattia". Nei contesti OSINT e di intelligence, un modello con eccesso di allineamento si rifiuta di analizzare campioni di codice malevolo o notizie di attacchi informatici, scambiando un'analisi difensiva legittima per un'attività malevola.

L'applicazione dei metodi di allineamento in produzione impone compromessi sistemici che l'ingegnere deve saper quantificare e bilanciare:

1. **Alignment Tax (La Tassa dell'Allineamento)**: L'ottimizzazione spinta della sicurezza restringe l'entropia della policy, concentrando la densità di probabilità su un sottoinsieme conservativo dello spazio generativo e sopprimendo percorsi di ragionamento complessi accessibili nel modello base.
2. **Reward Hacking e Legge di Goodhart**: *Quando una misura statistica diventa l'obiettivo di un'ottimizzazione, cessa di essere una buona misura*. Si manifesta attraverso:
   - *Verbosity Bias*: tendenza a generare risposte artificialmente lunghe e ricche di elenchi puntati ridondanti.
   - *Sycophancy (Adulazione)*: tendenza della rete a confermare pregiudizi errati dell'utente per evitare contrasti.
   - *Formattazione Apparente*: risposte stilisticamente impeccabili ma fattualmente allucinate.
3. **Over-refusal e Mode Collapse**: Il modello rifiuta query lecite (come l'analisi forense di codice vulnerabile per scopi OSINT e di difesa) a causa di filtri su parole chiave mal calibrati.

### Matrice Comparativa delle Metodologie di Allineamento

| Dimensione Operativa | RLHF Tradizionale (PPO) | Direct Preference Optimization (DPO) | Odds Ratio Preference Optimization (ORPO) |
| :--- | :--- | :--- | :--- |
| **Complessità Architetturale** | **Estrema** (4 modelli in VRAM: Actor, Critic, Ref, RM) | **Moderata** (2 modelli in VRAM: Policy, Ref) | **Minima** (1 singolo modello in VRAM) |
| **Tipo di Ottimizzazione** | **Online** (campionamento e rollouts continui) | **Offline** (contrasto su dataset statico) | **Monolitica** (SFT + preference in unica fase) |
| **Stabilità di Convergenza** | **Bassa** (sensibile a iperparametri e varianza vantaggio) | **Elevata** (gradiente esatto analogo a cross-entropy) | **Elevatissima** (nessun calcolo di divergenza separato) |
| **Rischio Reward Hacking** | **Molto alto** su Reward Model statici | **Moderato** (legato alla qualità del dataset statico) | **Basso-Moderato** (vincolato all'odds-ratio locale) |
| **Capacità di Esplorazione** | **Alta** (scopre nuove risposte durante i rollouts) | **Limitata** (ristretta ai dati di preferenza pre-esistenti) | **Limitata** (ristretta ai dati di training) |

> [!NOTE]
> **Checkpoint di Ancoraggio: Mantenimento dell'Attenzione**
> Se avverti stanchezza o calo di attenzione, fai una breve pausa. Il checkpoint ti permette di riprendere lo studio da qui senza dover rileggere i capitoli precedenti.

> [!INTERACTIVE] WIDGET: Radar dei Trade-Off e Simulatore di Alignment Tax
> **Tipo:** Radar Multidimensionale Dinamico e Stress-Test OSINT.
> **Descrizione Interfaccia:**
> - Un grafico radar interattivo con 5 assi di prestazione: `1. Sicurezza Conversazionale`, `2. Ragionamento Matematico/Code`, `3. Fedeltà Fattuale`, `4. Capacità Analitica OSINT (No Over-refusal)`, `5. Efficienza Computazionale VRAM`.
> - Selettore del metodo (`RLHF/PPO`, `DPO`, `ORPO`, `KTO`) con slider per `Intensità di Allineamento (0% - 100%)`.
> - Trascina l'intensità al 100% per osservare graficamente l'Alignment Tax: l'asse di Sicurezza sale al massimo, ma l'area del coding e dell'analisi OSINT si contrae drasticamente con l'apparizione di alert di "Over-refusal" su prompt di intelligence tecnica.

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