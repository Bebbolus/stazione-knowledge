---
aliases:
- D10
- Deep Learning e PyTorch
- Reti Neurali Profonde
- Autograd
- Tensors
- PyTorch Essentials
resources:
- title: TensorFlow Playground (Rete Neurale nel Browser)
  url: https://playground.tensorflow.org/
  type: lab
- title: But what is a neural network? (3Blue1Brown)
  url: https://www.youtube.com/watch?v=aircAruvnKk
  type: video
---
# Deep Learning e PyTorch: Dai Tensori al Calcolo Differenziale e Reti Profonde

Il **deep learning e il framework PyTorch** costituiscono il paradigma computazionale fondamentale per l'apprendimento di rappresentazioni gerarchiche complesse attraverso grafi di calcolo differenziabili e operazioni tensoriali su acceleratori hardware. Questa metodologia si applica nell'elaborazione di dati visivi con reti convoluzionali, nella modellazione di serie temporali e flussi testuali con modelli ricorrenti o trasformativi, e nell'addestramento scalabile di architetture neurali per compiti OSINT e intelligenza artificiale avanzata. Il framework open-source esiste per eliminare la complessità del calcolo manuale dei gradienti analitici tramite differenziazione automatica dinamica, offrendo un'interfaccia flessibile ed efficiente che colma il divario tra prototipazione scientifica ed esecuzione ottimizzata a basso livello su memoria GPU.

## Il Limite dei Modelli Lineari e la Necessità di Rappresentazioni Profonde

Nei moduli dedicati all'apprendimento supervisionato classico come [D05](D07-ml-fondamenti.md) e agli algoritmi basati su alberi decisionali come [D06](D08-ml-classico.md), i modelli estraggono pattern predittivi operando su insiemi di feature tabellari preventivamente ingegnerizzate da esperti di dominio. Sebbene questo paradigma risulti altamente efficace su dati strutturati e matrici a bassa dimensionalità, collassa sistematicamente di fronte a dati non strutturati ad altissima dimensionalità, quali matrici di pixel per immagini, campioni audio continui o sequenze di testo naturale.

La limitazione intrinseca dell'ingegneria manuale delle feature risiede nella maledizione della dimensionalità (*Curse of Dimensionality*) e nell'incapacità di catturare invarianze geometriche non lineari complesse. Un modello lineare o un albero di decisione tratta ciascun pixel di un'immagine come una variabile indipendente, ignorando la coerenza spaziale locale, la gerarchia semantica e le trasformazioni affini come traslazioni o rotazioni. Di conseguenza, per riconoscere un oggetto in posizioni differenti dello spazio, i modelli classici richiederebbero un volume esponenziale di combinazioni di training, saturando la memoria e generando overfitting severo.

Il deep learning risolve questo collo di bottiglia attraverso l'**apprendimento automatico delle rappresentazioni** (*Representation Learning*). Invece di richiedere feature estratte manualmente, un'architettura neurale profonda è composta da una successione di strati parametrizzati non lineari:

$$\mathbf{h}^{(1)} = \sigma(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}), \quad \mathbf{h}^{(2)} = \sigma(\mathbf{W}^{(2)}\mathbf{h}^{(1)} + \mathbf{b}^{(2)}), \quad \dots, \quad \hat{\mathbf{y}} = \mathbf{W}^{(L)}\mathbf{h}^{(L-1)} + \mathbf{b}^{(L)}$$

dove i primi strati imparano a rilevare primitive elementari (bordi, gradienti cromatici, fonemi), mentre gli strati intermedi e profondi compongono tali primitive in concetti astratti di ordine superiore (parti di oggetti, strutture sintattiche, semantica contestuale). L'addestramento congiunto dell'intera gerarchia end-to-end richiede un framework capace di orchestrare milioni di operazioni matriciali parallele e tracciare le derivate parziali lungo catene computazionali complesse.

## Anatomia della Struttura Dati: Tensori, Strides e Layout di Memoria

Al livello fondamentale dell'infrastruttura di [PyTorch](https://pytorch.org/) (il framework open-source di deep learning e differenziazione automatica gestito dalla [Linux Foundation](https://www.linuxfoundation.org/) e originariamente sviluppato da [Meta AI](https://ai.meta.com/)), ogni entità numerica è modellata come un **tensore**. Un tensore è una generalizzazione multidimensionale di scalari, vettori e matrici che incapsula un array $n$-dimensionale omogeneo associato a metadati di forma, tipo di dato e indirizzamento in memoria.

```text
Struttura in Memoria di un Tensore Bidimensionale (Shape: [3, 4], Strides: [4, 1])
Storage 1D contiguo in RAM/VRAM:
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 0,0 | 0,1 | 0,2 | 0,3 | 1,0 | 1,1 | 1,2 | 1,3 | 2,0 | 2,1 | 2,2 | 2,3 |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
 0     1     2     3     4     5     6     7     8     9     10    11    (Offset)
```

Fisicamente, la memoria di un computer non archivia array multidimensionali, ma un unico blocco di memoria lineare e contiguo a una dimensione detto `Storage`. Il tensore è semplicemente una **vista logica** (*view*) sovrapposta a questo storage lineare, definita da tre proprietà algebriche fondamentali: la **forma** (`shape`), che definisce il numero di elementi lungo ciascun asse dimensionale; il **passo di memoria** (`stride`), che rappresenta il numero esatto di elementi che l'interprete deve saltare nel buffer lineare sottostante per avanzare di una posizione lungo una specifica dimensione; lo **spiazzamento iniziale** (`storage_offset`), che indica l'indice dell'elemento iniziale del tensore all'interno dello storage continuo.

In un tensore bidimensionale memorizzato con convenzione *Row-Major* (C-contiguous) di dimensioni $(M, N)$, lo stride lungo le righe è pari a $N$, mentre lo stride lungo le colonne è pari a $1$. L'indirizzo lineare dell'elemento $(i, j)$ nello storage fisico viene calcolato istantaneamente tramite la formula di indicizzazione:

$$\text{Indice\_Lineare}(i, j) = \text{storage\_offset} + i \cdot \text{stride}[0] + j \cdot \text{stride}[1]$$

Questa architettura consente a PyTorch di eseguire operazioni di trasposizione, slicing, estrazione di diagonali e ridimensionamento con costo computazionale nullo $O(1)$ e senza duplicazione di memoria, modificando unicamente la tupla degli strides. Tuttavia, operazioni come la trasposizione (`tensor.t()`) rendono il tensore **non contiguo** in memoria. Quando è richiesta una visualizzazione contigua lineare tramite `tensor.view()`, PyTorch solleva un'eccezione se il layout di memoria non è contiguo, imponendo l'uso di `tensor.contiguous()` o del metodo flessibile `tensor.reshape()`, il quale esegue una copia fisica dei dati nella memoria RAM o VRAM solo se strettamente necessario.

La coesistenza trasparente tra calcolo su processore centrale (CPU) e acceleratore grafico (GPU) avviene tramite l'oggetto `torch.device`. Il trasferimento di un tensore tra lo spazio di indirizzamento della memoria host (RAM di sistema) e la memoria dedicata della GPU (VRAM) tramite il bus PCI Express viene formalizzato dal metodo `.to(device)` o `.cuda()`, consentendo di allocare tensori direttamente sui registri ad altissimo parallelismo di schede grafiche prodotte da [NVIDIA](https://www.nvidia.com/) (la multinazionale tecnologica produttrice leader di GPU e calcolo accelerato).

## Il Motore di Differenziazione Automatica: Grafo Computazionale e Autograd

L'addestramento di una rete neurale consiste nell'ottimizzare una funzione scalare di costo $\mathcal{L}$ rispetto a milioni di parametri continui $\mathbf{W}$ e $\mathbf{b}$. Il calcolo simbolico manuale delle derivate parziali per reti profonde è impraticabile, mentre la differenziazione numerica tramite differenze finite richiede $O(P)$ forward pass (dove $P$ è il numero totale di parametri), risultando computazionalmente insostenibile.

PyTorch risolve questo problema implementando un motore di **differenziazione automatica dinamica** (*tape-based reverse-mode autodiff*) chiamato **Autograd**. Durante il passaggio in avanti (*forward pass*), quando un tensore possiede l'attributo `requires_grad=True`, il runtime registra dinamicamente ogni operazione matematica eseguita all'interno di un **Grafo Aciclico Diretto** (*Directed Acyclic Graph*, DAG). I nodi foglia del grafo rappresentano i tensori di input e i pesi del modello, mentre i nodi intermedi rappresentano gli operatori differenziabili (`torch.autograd.Function`), ciascuno dotato di un puntatore alla funzione gradiente inversa `grad_fn`.

<div class="admonition abstract">
  <p class="admonition-title">Animazione Interattiva: Discesa del Gradiente</p>
  <p>Immagina che la funzione sottostante sia la tua Loss calcolata da PyTorch. Usa lo slider per regolare il Learning Rate (&alpha;), poi premi "Fai un passo" per vedere come il parametro (la pallina) "scivola" verso il minimo locale sfruttando la pendenza (gradiente) della curva.</p>
  <iframe src="../widgets/discesa_gradiente.html" style="width: 100%; height: 680px; border: none; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>
</div>

Quando viene invocato il metodo `loss.backward()`, il motore Autograd esegue un attraversamento topologico inverso del grafo computazionale. Applicando la regola della catena multivariata formalizzata in [D04](D06-math-stat.md), il motore calcola i prodotti Vettore-Jacobiano (*Vector-Jacobian Products*, VJP):

$$\mathbf{v}^T \mathbf{J} = \frac{\partial \mathcal{L}}{\partial \mathbf{y}} \cdot \frac{\partial \mathbf{y}}{\partial \mathbf{x}}$$

Questo algoritmo propaga l'errore all'indietro dalla radice scalare della Loss fino a tutti i nodi foglia con complessità temporale $O(1)$ proporzionale a un singolo passaggio in avanti. I gradienti calcolati per ciascun parametro vengono accumulati nel rispettivo attributo `.grad`.

L'esempio minimale sottostante illustra il tracciamento del grafo per un polinomio scalare $y = x^2 + 3x + 1$:

```python
import torch

# Inizializzazione del tensore foglia con tracciamento del gradiente
x = torch.tensor(2.0, requires_grad=True)

# Definizione del grafo computazionale: y = x^2 + 3x + 1
y = x ** 2 + 3 * x + 1

# Esecuzione del backward pass (retropropagazione del gradiente)
y.backward()

# Verifica analitica: dy/dx = 2x + 3 = 2(2.0) + 3 = 7.0
print(f"Valore del gradiente calcolato: {x.grad.item()}")  # dy/dx = 7.0
```

Poiché PyTorch accumula i gradienti per default mediante operazione di somma interna (`x.grad += nuovo_gradiente`) per supportare naturalmente architetture con diramazioni e gradient accumulation, è imperativo azzerare esplicitamente i gradienti all'inizio di ciascuna iterazione di addestramento invocando `optimizer.zero_grad()`. Durante le fasi di inferenza e validazione, il tracciamento del grafo computazionale deve essere disabilitato incapsulando il codice nel blocco di contesto `with torch.no_grad():`, eliminando l'allocazione del grafo e riducendo drasticamente il consumo di memoria RAM e VRAM.


> [!NOTE]
> **Checkpoint di Ancoraggio: Riepilogo Concettuale**
> A questo punto abbiamo esaminato i concetti chiave di D08-deep-learning-pytorch. Assicurati di aver compreso la struttura logico-matematica e i trade-off discussi finora prima di proseguire con la sezione successiva.


## Architettura a Moduli: Astrazione nn.Module e Parametrizzazione

Sebbene sia possibile implementare reti neurali manipolando direttamente tensori e moltiplicazioni matriciali con [NumPy](https://numpy.org/) (la libreria open-source per il calcolo scientifico e matriciale in [Python](https://www.python.org/)), la gestione manuale dello stato dei parametri e delle trasformazioni diventa rapidamente ingestibile all'aumentare della profondità architetturale. Il modulo `torch.nn` standardizza la progettazione attraverso la classe base `nn.Module`.

Un modulo PyTorch è un contenitore strutturato che incapsula sia i parametri apprendibili della rete (`nn.Parameter`) sia la logica di calcolo del passaggio in avanti. Ogni classe personalizzata deve ereditare da `nn.Module`, invocare il costruttore della superclasse `super().__init__()` e sovrascrivere il metodo `forward(*inputs)`.

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    """Architettura Multi-Layer Perceptron modulare basata su nn.Sequential."""
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
```

L'ereditarietà da `nn.Module` fornisce funzionalità ingegneristiche essenziali per la gestione di modelli complessi. In primo luogo, invocando `model.parameters()`, il framework raccoglie ricorsivamente tutti i tensori di peso e bias registrati nei sotto-moduli, rendendoli immediatamente accessibili all'ottimizzatore. In secondo luogo, i metodi `model.train()` e `model.eval()` propagano lo stato esecutivo a tutti i layer, alterando il comportamento di operatori sensibili alla fase di addestramento come `nn.Dropout` e `nn.BatchNorm`. Inoltre, il comando `model.to(device)` migra istantaneamente tutti i pesi e i buffer registrati dalla memoria host alla GPU target. Infine, il dizionario `model.state_dict()` mappa in modo deterministico i nomi dei singoli layer ai rispettivi tensori di peso, costituendo la base per il salvataggio e la serializzazione su disco.

## Pipeline dei Dati: Astrazioni Dataset e DataLoader

Nelle pipeline di deep learning su larga scala, il trasferimento di dati da disco a memoria costituisce frequentemente il collo di bottiglia principale dell'intero sistema. Se la GPU rimane inattiva in attesa che la CPU completi la lettura e la trasformazione del batch successivo (*GPU starvation*), l'efficienza computazionale crolla. PyTorch disaccoppia la memorizzazione dei dati dalla logica di campionamento attraverso due astrazioni complementari: `Dataset` e `DataLoader`.

### La Classe Base Dataset

La classe astratta `torch.utils.data.Dataset` definisce un'interfaccia a mappatura per indici (*map-style dataset*). L'implementazione personalizzata richiede la sovrascrittura di due metodi fondamentali: `__len__()`, che restituisce la cardinalità totale del dataset, e `__getitem__(idx)`, che gestisce l'accesso e la restituzione dell'istanza $i$-esima sotto forma di tensori formattati:

```python
from typing import Tuple
import torch
from torch.utils.data import Dataset

class MyDataset(Dataset):
    """Dataset personalizzato con conversione deterministica a tensori float32."""
    def __init__(self, X: torch.Tensor, y: torch.Tensor):
        self.X = torch.as_tensor(X, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.X[idx], self.y[idx]
```

Per l'elaborazione di dati visivi standard, l'ecosistema [Torchvision](https://pytorch.org/vision/stable/) (la libreria ufficiale del framework PyTorch per computer vision) fornisce implementazioni preconfigurate per benchmark noti come `MNIST` e `CIFAR10`.

### Il DataLoader e l'Esecuzione Parallela

L'oggetto `torch.utils.data.DataLoader` avvolge il `Dataset` e gestisce l'iterazione efficiente, il raggruppamento in mini-batch, il rimescolamento stocastico e l'elaborazione asincrona multi-processo.

```python
from torch.utils.data import DataLoader

# Istanziazione del Dataset e configurazione del DataLoader ad alte prestazioni
train_dataset = MyDataset(X_train, y_train)
train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=2,
    pin_memory=torch.cuda.is_available(),
    drop_last=False
)
```

La configurazione del parametro `num_workers > 0` genera un pool di processi worker dedicati al precaricamento e alla trasformazione asincrona dei batch futuri nella memoria RAM. Il flag `pin_memory=True` alloca i batch in memoria bloccata (*page-locked / pinned memory*), abilitando trasferimenti diretti ad altissima velocità verso la VRAM della GPU tramite accessi diretti alla memoria (DMA), bypassando l'overhead del sistema operativo.

## Architetture Fondamentali: MLP, CNN e Reti Ricorrenti

La modellazione neurale in PyTorch copre una tassonomia esaustiva e non sovrapposta di architetture, ciascuna specializzata per specifiche topologie di dato: dati tabellari vettoriali, matrici bidimensionali a struttura spaziale e sequenze temporali unidimensionali.

### Multi-Layer Perceptrons per Dati Tabellari

Per vettori di feature densi e non strutturati, il Multi-Layer Perceptron esegue una successione di proiezioni lineari alternate a funzioni di attivazione non lineari (come `ReLU(z) = \max(0, z)`). La parametrizzazione flessibile consente di definire topologie a profondità arbitraria:

```python
from typing import List
import torch
import torch.nn as nn

class TabularMLP(nn.Module):
    """Rete neurale densa parametrizzabile per dati tabellari e classificazione."""
    def __init__(self, input_dim: int, hidden_dims: List[int], output_dim: int, num_classes: int):
        super().__init__()
        layers: List[nn.Module] = []
        prev_dim = input_dim
        
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.ReLU()
            ])
            prev_dim = h_dim
            
        final_dim = output_dim if num_classes == 1 else num_classes
        layers.append(nn.Linear(prev_dim, final_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
```

L'alternanza di trasformazioni lineari e non lineari conferisce all'MLP la proprietà di approssimatore universale, permettendo al modello di separare spazi decisionali altamente non lineari che risulterebbero inseparabili per una regressione logistica classica.

### Reti Convoluzionali per Dati Spaziali e Visione

Le reti neurali convoluzionali (*Convolutional Neural Networks*, CNN) sfruttano la proprietà di **invarianza per traslazione** e la correlazione locale dei dati bidimensionali (immagini o matrici spettrali). Un layer convoluzionale `nn.Conv2d` fa scorrere un insieme di filtri o kernel di dimensione ridotta (tipicamente $3 \times 3$ o $5 \times 5$) sull'immagine di input:

$$(\mathbf{I} * \mathbf{K})(i, j) = \sum_{m} \sum_{n} \mathbf{I}(i - m, j - n) \mathbf{K}(m, n)$$

I filtri estraggono mappe di feature locali condividendo i medesimi pesi su tutta la superficie spaziale (*weight sharing*), riducendo drasticamente il numero di parametri rispetto a un layer completamente connesso. Gli strati di pooling (`nn.MaxPool2d`) riducono progressivamente la risoluzione spaziale, aumentando il campo recettivo dei layer successivi.

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    """Architettura convoluzionale 2D per classificazione di immagini standard."""
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        # Calcolo dimensione appiattita per input 32x32: 32 canali * 8 * 8 pixel
        self.classifier = nn.Linear(32 * 8 * 8, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = x.view(x.size(0), -1)  # Appiattimento spaziale conservando la dimensione del batch
        return self.classifier(x)
```

Al termine della cascata di convoluzioni ed estrazioni, le mappe di feature bidimensionali vengono appiattite in un vettore monodimensionale tramite `x.view(x.size(0), -1)` e trasmesse al classificatore lineare terminale.

### Reti Ricorrenti e Meccanismi a Gate per Sequenze

Quando i dati presentano dipendenze temporali o sequenziali (serie temporali, log di eventi, testo prima dell'avvento dei modelli basati su attenzione trattati in [D09](D11-transformers-llm.md)), le architetture feedforward classiche risultano inadeguate perché non mantengono memoria degli input passati.

Le reti ricorrenti standard (*Recurrent Neural Networks*, RNN) mantengono uno stato nascosto $\mathbf{h}_t = \tanh(\mathbf{W}_{hh}\mathbf{h}_{t-1} + \mathbf{W}_{xh}\mathbf{x}_t + \mathbf{b})$, ma soffrono del collasso esponenziale dei gradienti (*vanishing gradient problem*) su sequenze estese. I modelli **Long Short-Term Memory (LSTM)** e **Gated Recurrent Unit (GRU)** superano questa patologia introducendo porte di regolazione differenziabili: la **porta di oblio** (*forget gate*) $\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)$, che determina quanta informazione pregressa cancellare dallo stato di cella $\mathbf{C}_{t-1}$; la **porta di ingresso** (*input gate*) $\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)$, che seleziona quali nuove informazioni candidati $\tilde{\mathbf{C}}_t$ aggiungere alla memoria persistente; lo **stato di cella** (*cell state*) $\mathbf{C}_t = \mathbf{f}_t \odot \mathbf{C}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{C}}_t$, che funge da canale di memoria a lungo termine a gradiente costante; la **porta di uscita** (*output gate*) $\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)$, che filtra lo stato di cella per produrre il nuovo stato nascosto $\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{C}_t)$.

```python
import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    """Modello sequenziale basato su LSTM per classificazione di serie e testi."""
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, num_classes: int):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Input x shape: (batch_size, sequence_length, input_dim)
        _, (h_n, _) = self.lstm(x)
        # h_n shape: (num_layers, batch_size, hidden_dim)
        last_hidden = h_n[-1]
        return self.fc(last_hidden)
```

L'impostazione `batch_first=True` allinea la convenzione dei tensori allo standard industriale $(B, T, D)$, semplificando l'integrazione con pipeline di preprocessing e batching multi-sorgente.


> [!NOTE]
> **Checkpoint di Ancoraggio: Autovalutazione**
> Riesci a mappare mentalmente i passaggi chiave appena descritti? Un buon test è provare a spiegare a un collega junior il meccanismo fondamentale analizzato in questa sezione.


## Il Ciclo di Addestramento: Forward, Loss, Backward e Ottimizzazione

L'esecuzione pratica del deep learning richiede l'orchestrazione deterministica di un **Training Loop** strutturato. A differenza di framework ad alto livello come [Keras](https://keras.io/) (l'interfaccia di programmazione ad alto livello per il deep learning multi-backend) o [TensorFlow](https://www.tensorflow.org/) (la piattaforma open-source end-to-end sviluppata da [Google](https://about.google/)), PyTorch espone esplicitamente ogni singolo passaggio dell'iterazione algoritmica, garantendo pieno controllo diagnostico.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Inizializzazione di modello, funzione di costo e ottimizzatore
model = TabularMLP(input_dim=10, hidden_dims=[64, 32], output_dim=2, num_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
num_epochs = 10

# Configurazione del dispositivo di calcolo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    # 1. Fase di Addestramento
    model.train()
    running_loss = 0.0
    
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        
        # Azzeramento preventivo dei gradienti accumulati
        optimizer.zero_grad()
        
        # Forward pass: calcolo dei logits non normalizzati
        logits = model(X_batch)
        
        # Calcolo della funzione di perdita
        loss = criterion(logits, y_batch)
        
        # Backward pass: propagazione all'indietro dei gradienti
        loss.backward()
        
        # Step dell'ottimizzatore: aggiornamento dei pesi W = W - lr * grad
        optimizer.step()
        
        running_loss += loss.item() * X_batch.size(0)

    # 2. Fase di Validazione e Valutazione
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            val_logits = model(X_val)
            val_loss += criterion(val_logits, y_val).item() * X_val.size(0)
            
            predictions = torch.argmax(val_logits, dim=1)
            correct += (predictions == y_val).sum().item()
            total += y_val.size(0)
            
    epoch_train_loss = running_loss / len(train_dataset)
    epoch_val_loss = val_loss / len(val_dataset)
    val_accuracy = correct / total if total > 0 else 0.0
    
    print(f"Epoca [{epoch+1:02d}/{num_epochs:02d}] | Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f} | Val Acc: {val_accuracy:.4f}")
```

La selezione della funzione di perdita è determinata dalla natura del compito computazionale. Nella classificazione binaria si impiega `nn.BCEWithLogitsLoss()`, che unisce internamente la funzione Sigmoide e la Binary Cross Entropy, garantendo stabilità numerica contro underflow logaritmici. Nella classificazione multi-classe si utilizza `nn.CrossEntropyLoss()`, che calcola la perdita direttamente sui logits lineari non normalizzati combinando `LogSoftmax` e `NLLLoss`. Nella regressione continua si adottano `nn.MSELoss()` (Mean Squared Error) o `nn.L1Loss()` (Mean Absolute Error per robustezza agli outlier).

Gli ottimizzatori governano la traiettoria di discesa lungo la superficie di perdita. Mentre la discesa stocastica del gradiente con momento (`optim.SGD(..., momentum=0.9)`) accelera lungo le direzioni di discesa costante riducendo le oscillazioni, l'algoritmo **Adam** (`optim.Adam`) calcola tassi di apprendimento adattivi per ciascun parametro stimando i momenti del primo ordine (media dei gradienti) e del secondo ordine (varianza non centrata).

## Regolarizzazione, Esecuzione CUDA e Serializzazione

La transizione da un prototipo sperimentale a un modello scalabile pronto per la produzione richiede tecniche rigorose per mitigare l'overfitting, massimizzare il throughput hardware su GPU e persistere lo stato dei parametri.

### Tecniche di Regolarizzazione e Diagnostica delle Curve di Apprendimento

La capacità esponenziale di memorizzazione delle reti neurali profonde comporta un rischio costante di overfitting sul rumore statistico del set di addestramento. Le tecniche di regolarizzazione standard comprendono diverse strategie integrate: **Dropout** (`nn.Dropout(p=0.5)`), che disattiva casualmente una frazione $p$ di neuroni durante ciascun forward pass nella fase di addestramento, forzando la rete ad apprendere rappresentazioni ridondanti e distribuite; **Weight Decay** (`optimizer = Adam(..., weight_decay=1e-4)`), che aggiunge una penalità $L_2$ quadratica alla funzione di perdita $\mathcal{L}_{\text{tot}} = \mathcal{L} + \frac{\lambda}{2} \|\mathbf{W}\|_2^2$, scoraggiando la crescita eccessiva dei coefficienti matriciali; **Early Stopping**, che monitora la curva della Validation Loss arrestando l'addestramento non appena la perdita sul validation set cessa di decrescere per un numero prefissato di epoche (*patience*), prevenendo la fase di divergenza generalizzativa.

```text
Dinamica delle Curve di Apprendimento (Loss vs Epoche):
Loss ^
     |  \
     |   \   Training Loss (scende costantemente)
     |    \________
     |     \       \________
     |      \_______\---------------- Validation Loss (minimo ottimale)
     |               \      /^^^^^^^^ Overfitting (la validation loss risale)
     +----------------\----/----------> Epoche
```

### Esecuzione su Acceleratori Hardware CUDA e Precisione Mista

Le GPU [NVIDIA](https://www.nvidia.com/) moderne integrano unità di calcolo specializzate per operazioni su tensori (*Tensor Cores*). L'esecuzione di default in virgola mobile a 32 bit (`float32` o `FP32`) garantisce elevata precisione numerica ma satura rapidamente la banda di memoria della GPU.

L'adozione del paradigma di **precisione mista automatica** (*Automatic Mixed Precision*, AMP) esegue le moltiplicazioni matriciali e le convoluzioni in formato a 16 bit (`float16` o `bfloat16`), conservando i pesi primari e il calcolo della loss in `float32`. Ciò raddoppia la velocità di elaborazione e dimezza il consumo di VRAM. Per evitare che gradienti estremamente ridotti collassino a zero durante la quantizzazione a 16 bit (*underflow*), PyTorch impiega `torch.amp.GradScaler`, che moltiplica la loss per un fattore di scala prima del backward pass e la riscala prima dell'aggiornamento dell'ottimizzatore:

```python
# Schema concettuale di training con Automatic Mixed Precision (AMP)
scaler = torch.amp.GradScaler("cuda", enabled=torch.cuda.is_available())

for X_batch, y_batch in train_loader:
    X_batch, y_batch = X_batch.to(device), y_batch.to(device)
    optimizer.zero_grad()
    
    with torch.amp.autocast("cuda", enabled=torch.cuda.is_available()):
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Persistenza del Modello: Serializzazione e Deserializzazione dello State Dict

Nel ciclo di vita del machine learning formalizzato in [D15](D17-mlops-llmops.md), i modelli addestrati devono essere salvati su storage persistente per l'erogazione di servizi di inferenza. In PyTorch, l'approccio ingegneristico corretto e sicuro consiste nel salvare esclusivamente il dizionario dei parametri pesati (`state_dict`), evitando la serializzazione diretta dell'intero oggetto Python tramite modulo pickle, la quale genera vulnerabilità di sicurezza e fragilità di accoppiamento al codice sorgente:

```python
from pathlib import Path
import torch

checkpoint_path = Path("checkpoints") / "model_tabular.pth"
checkpoint_path.parent.mkdir(exist_ok=True)

# 1. Salvataggio deterministico dello state_dict
torch.save(model.state_dict(), checkpoint_path)
print(f"Pesi del modello serializzati con successo in: {checkpoint_path}")

# 2. Ripristino del modello su nuova istanza
loaded_model = TabularMLP(input_dim=10, hidden_dims=[64, 32], output_dim=2, num_classes=2)
loaded_model.load_state_dict(torch.load(checkpoint_path, map_location=device))

# Impostazione obbligatoria in modalita valutazione
loaded_model.eval()
print("Modello deserializzato e pronto per l'inferenza.")
```

Il parametro `map_location` garantisce la portabilità cross-environment, consentendo di ripristinare pesi addestrati su GPU multi-nodo anche su macchine di inferenza dotate esclusivamente di processori CPU standard (`map_location="cpu"`).

## Compromessi Architetturali e Limiti Operativi

L'adozione del deep learning con PyTorch impone una valutazione rigorosa dei vincoli fisici e computazionali del sistema di calcolo.

```text
Matrice dei Compromessi di Esecuzione in Deep Learning:
+-----------------------------------+-----------------------------------+
| Vincolo Computazionale            | Conseguenza Architetturale        |
+-----------------------------------+-----------------------------------+
| Compute Bound vs Memory Bound     | Calcolo intensivo (MatMul grandi) |
|                                   | vs saturazione VRAM (batch enormi)|
| Flessibilità Grafi Dinamici       | Facilità di debug imperativo      |
| vs Ottimizzazione Grafi Statici   | vs overhead runtime PyTorch C++   |
| Modelli Neurali Profondi          | Eccellenza su immagini e testo    |
| vs Ensemble GBDT su Tabellari     | vs inefficienza e costo su CSV    |
+-----------------------------------+-----------------------------------+
```

### Limite di Banda di Memoria vs Saturazione della Capacità di Calcolo

Durante l'addestramento e l'inferenza, le operazioni si dividono rigidamente tra carichi limitati dalla velocità di elaborazione dei core (*Compute Bound*, come matrici dense di grandi dimensioni) e carichi limitati dalla velocità di trasferimento dati tra la memoria VRAM e i registri dei chip (*Memory Bandwidth Bound*, come attivazioni puntuali, normalizzazioni e dropout). L'aumento indiscriminato della dimensione del batch (*batch size*) riduce l'overhead del framework saturando il parallelismo della GPU, ma oltrepassata la capienza della VRAM provoca un arresto anomalo per esaurimento memoria (*CUDA Out-Of-Memory*).

### Overhead dei Grafi Dinamici vs Compilazione Statica

Il paradigma dinamico *define-by-run* di PyTorch ricostruisce il grafo computazionale a ogni iterazione, offrendo flessibilità nativa per sequenze a lunghezza variabile e debugging immediato tramite debugger standard Python. Tuttavia, questo dinamismo introduce un overhead di interprete C++ a ogni forward pass. Quando le architetture sono stabili e destinate a volumi di inferenza industriali su larga scala, l'ingegnere deve ricorrere alla compilazione del grafo tramite `torch.compile()` per fondere i kernel elementari (*kernel fusion*) ed eliminare i trasferimenti ridondanti in memoria.

### Deep Learning vs Gradient Boosted Trees su Dati Tabellari

Un grave errore architetturale consiste nell'impiegare indiscriminatamente reti neurali profonde per qualunque problema predittivo. Su dataset tabellari strutturati a bassa e media scala, gli algoritmi di Gradient Boosted Decision Trees trattati in [D06](D08-ml-classico.md) (quali [XGBoost](https://xgboost.readthedocs.io/) (la libreria open-source per gradient boosting scalabile), [LightGBM](https://lightgbm.readthedocs.io/) (il framework di gradient boosting sviluppato da [Microsoft](https://www.microsoft.com/)) e [CatBoost](https://catboost.ai/) (la libreria per alberi decisionali ottimizzata per variabili categoriche da Yandex)) superano costantemente le reti neurali in termini di accuratezza, velocità di addestramento, robustezza a valori nulli e interpretabilità diagnostica, richiedendo frazioni marginali dell'energia e dell'hardware necessari per addestrare un MLP. Il deep learning diventa conveniente unicamente in presenza di relazioni gerarchiche complesse, segnali multimodali combinati (testo e immagini simultanee) o volumi di dati dell'ordine dei milioni di istanze.

## Riferimenti Bibliografici e Risorse Tecniche

### Risorse Didattiche Visive e Interattive

La comprensione visiva e intuitiva dell'algebra lineare, della discesa del gradiente e della retropropagazione dell'errore è esposta nella celebre serie di lezioni prodotta dal canale didattico [3Blue1Brown](https://www.3blue1brown.com/) (il canale didattico dedicato alla matematica visuale) del divulgatore matematico [Grant Sanderson](https://www.3blue1brown.com/) (il divulgatore matematico creatore del canale didattico 3Blue1Brown). Per sperimentare visivamente la formazione di confini decisionali non lineari al variare di strati e neuroni nel browser, lo strumento interattivo open-source [TensorFlow](https://www.tensorflow.org/) Playground (l'applicazione web sviluppata dal team di [Google](https://about.google/) e [Google DeepMind](https://deepmind.google/)) consente di osservare l'evoluzione dei pesi in tempo reale su dataset sintetici complessi.

### Documentazione Ufficiale e Guide PyTorch

L'indice completo delle primitive tensoriali e delle classi di algebra differenziale è consultabile nella [Documentazione Ufficiale di PyTorch](https://pytorch.org/docs/stable/index.html) e nella sezione dedicata ai [PyTorch Tutorials](https://pytorch.org/tutorials/). Per un'introduzione ingegneristica rapida ma rigorosa all'ecosistema dei tensori e dell'autograd, la guida [Deep Learning with PyTorch: A 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html) costituisce il riferimento pratico standard. I manuali dedicati all'astrazione ad alto livello e alla serializzazione sono reperibili nelle specifiche di [torch.nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html), [Dataset & DataLoader](https://pytorch.org/docs/stable/data.html) e [Serialization Semantics](https://pytorch.org/docs/stable/notes/serialization.html).

### Trattati Accademici e Manuali di Riferimento

I fondamenti teorici del calcolo differenziale e delle rappresentazioni profonde sono formalizzati nel trattato enciclopedico *Deep Learning* curato da Ian Goodfellow, Yoshua Bengio e Aaron Courville presso il [MIT](https://web.mit.edu/) (il Massachusetts Institute of Technology, prestigioso istituto universitario di ricerca tecnologica), consultabile su [Deep Learning Book](https://www.deeplearningbook.org/). Il percorso operativo e implementativo completo con codice PyTorch integrato è dettagliato nel manuale interattivo open-source [Dive into Deep Learning (D2L)](https://d2l.ai/). Le architetture pre-addestrate per compiti di visione artificiale e modelli sequenziali avanzati sono documentate all'interno di [Torchvision Models](https://pytorch.org/vision/stable/models.html) e [Hugging Face Transformers](https://huggingface.co/docs/transformers) (la libreria open-source di [Hugging Face](https://huggingface.co/) per modelli di linguaggio e visione).

## Appendice Operativa: Laboratori Pratici

> [!TIP]
> **Zero-Draft Offloading (Delega dell'Inizio)**
> Per abbattere la "Task Initiation Paralysis", non scrivere mai questo codice da zero. Usa un agente AI (es. DeepSeek Harness) o un LLM per farti generare lo scheletro iniziale dei file, passandogli come prompt i requisiti tecnici indicati sotto. Il tuo lavoro deve essere quello di *revisore* e *ingegnere*, non di dattilografo.



I laboratori seguenti contengono procedure sequenziali e script eseguibili in Python per testare sul campo i concetti di tensori, differenziazione automatica, classificazione tabellare con MLP, visione artificiale con CNN e modellazione sequenziale con LSTM.

- [ ] **Laboratorio 1: Manipolazione di Tensori, Strides e Autograd Scalare**  
   Inizializzare un ambiente virtuale dedicato, creare uno script `lab1_tensors.py` e verificare le proprietà di allocazione e calcolo del gradiente:
   ```python
   import torch

   # Creazione di un tensore 2D e verifica di strides e continuita
   A = torch.arange(12, dtype=torch.float32).reshape(3, 4)
   print(f"Shape: {A.shape}, Strides: {A.stride()}, Contiguo: {A.is_contiguous()}")
   
   # Trasposizione e verifica perdita di continuita
   A_t = A.t()
   print(f"A_t Shape: {A_t.shape}, Strides: {A_t.stride()}, Contiguo: {A_t.is_contiguous()}")
   
   # Autograd su equazione polinomiale
   w = torch.tensor([2.0, -3.0], requires_grad=True)
   x = torch.tensor([4.0, 5.0])
   loss = torch.sum(w * x) ** 2
   loss.backward()
   print(f"Gradiente dLoss/dw: {w.grad}")
   ```

- [ ] **Laboratorio 2: Addestramento End-to-End di un TabularMLP con Validation Set**  
   Generare un dataset sintetico non lineare di classificazione binaria, preparare `Dataset` e `DataLoader`, addestrare il modello e tracciare la discesa della perdita:
   ```python
   import torch
   import torch.nn as nn
   import torch.optim as optim
   from torch.utils.data import Dataset, DataLoader

   torch.manual_seed(42)
   X_raw = torch.randn(500, 8)
   y_raw = ((X_raw[:, 0] + X_raw[:, 1] ** 2) > 1.0).long()

   class SyntheticData(Dataset):
       def __init__(self, X, y):
           self.X, self.y = X, y
       def __len__(self):
           return len(self.X)
       def __getitem__(self, idx):
           return self.X[idx], self.y[idx]

   dataset = SyntheticData(X_raw, y_raw)
   train_set, val_set = torch.utils.data.random_split(dataset, [400, 100])
   train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
   val_loader = DataLoader(val_set, batch_size=32, shuffle=False)

   model = nn.Sequential(
       nn.Linear(8, 32),
       nn.ReLU(),
       nn.Linear(32, 2)
   )
   criterion = nn.CrossEntropyLoss()
   optimizer = optim.Adam(model.parameters(), lr=0.01)

   for epoch in range(1, 11):
       model.train()
       total_loss = 0.0
       for X_b, y_b in train_loader:
           optimizer.zero_grad()
           out = model(X_b)
           loss = criterion(out, y_b)
           loss.backward()
           optimizer.step()
           total_loss += loss.item() * len(X_b)
       print(f"Epoca {epoch:02d} | Loss di Addestramento: {total_loss/len(train_set):.4f}")
   ```

- [ ] **Laboratorio 3: Classificazione di Immagini Sintetiche con SimpleCNN**  
   Costruire e testare una rete convoluzionale su un batch di immagini RGB di dimensioni $32 \times 32$:
   ```python
   import torch
   import torch.nn as nn

   class SimpleCNN(nn.Module):
       def __init__(self, num_classes=10):
           super().__init__()
           self.features = nn.Sequential(
               nn.Conv2d(3, 16, 3, padding=1),
               nn.ReLU(),
               nn.MaxPool2d(2),
               nn.Conv2d(16, 32, 3, padding=1),
               nn.ReLU(),
               nn.MaxPool2d(2),
           )
           self.classifier = nn.Linear(32 * 8 * 8, num_classes)

       def forward(self, x):
           x = self.features(x)
           x = x.view(x.size(0), -1)
           return self.classifier(x)

   cnn = SimpleCNN(num_classes=10)
   fake_images = torch.randn(4, 3, 32, 32)
   output_logits = cnn(fake_images)
   print(f"Dimensione output del batch di immagini: {output_logits.shape}")
   ```

- [ ] **Laboratorio 4: Modellazione Sequenziale con LSTM e Checkpoint su Disco**  
   Implementare un classificatore per serie temporali, eseguire il passaggio in avanti e salvare i pesi del modello su storage locale:
   ```python
   from pathlib import Path
   import torch
   import torch.nn as nn

   class LSTMClassifier(nn.Module):
       def __init__(self, input_dim, hidden_dim, num_layers, num_classes):
           super().__init__()
           self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
           self.fc = nn.Linear(hidden_dim, num_classes)

       def forward(self, x):
           _, (h_n, _) = self.lstm(x)
           return self.fc(h_n[-1])

   lstm_net = LSTMClassifier(input_dim=5, hidden_dim=16, num_layers=1, num_classes=2)
   fake_seq = torch.randn(8, 20, 5)  # 8 campioni, sequenza lunga 20, 5 feature
   out = lstm_net(fake_seq)
   print(f"Output sequenziale: {out.shape}")

   save_dir = Path("saved_models")
   save_dir.mkdir(exist_ok=True)
   model_file = save_dir / "lstm_weights.pth"
   torch.save(lstm_net.state_dict(), model_file)
   print(f"Stato del modello salvato correttamente in: {model_file}")
   ```
