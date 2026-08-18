# D08 — Deep Learning e PyTorch

## Meta-modulo D08

**Target**  
Me stesso oggi, e chiunque voglia capire e usare reti neurali profonde con PyTorch:
dai tensori e autograd, a MLP, CNN, LSTM/GRU, fino a training loop, regolarizzazione e debug.

**Prerequisiti consigliati**

- D02 — Python refresher e software engineering essentials
- D03 — Data foundations (NumPy, Pandas, SQL, data quality)
- D04 — Matematica e statistica just-in-time (algebra lineare, derivate, probabilità)
- D05 — Fondamenti di Machine Learning (workflow supervised, metriche, overfitting)
- D06 — ML classico (alberi, ensemble, valutazione su dati tabellari)

**Durata indicativa**

- **Modalità minima (~3–4 ore)**  
  - tensori, operazioni base, autograd  
  - MLP semplice su dati tabellari  
  - training loop minimale (forward, loss, backward, optimizer step)

- **Modalità standard (~8–10 ore)**  
  - Dataset/DataLoader, moduli `nn.Module`  
  - CNN base per immagini (es. MNIST/CIFAR-10)  
  - regolarizzazione (dropout, weight decay, early stopping)  
  - saving/loading modelli

- **Modalità deep dive (più giornate)**  
  - LSTM/GRU per sequenze (testo, serie temporali)  
  - training loop più strutturato (validation, checkpoint, logging)  
  - esperimenti su dataset reali con error analysis e tuning

**Quando considerare il modulo “completato”**

- so spiegare a parole mie cos’è un tensore, cos’è il gradiente e come funziona l’autograd
- so costruire un MLP, una CNN e una rete sequenziale (LSTM/GRU) in PyTorch
- so scrivere un training loop corretto con training/validation e salvare i pesi
- so interpretare curve di loss e riconoscere overfitting/underfitting
- ho almeno un progetto DL funzionante (immagini o sequenze) con codice pulito e riproducibile

---

## Perché questo documento

Dopo D05–D07 ho gli strumenti per ML classico e unsupervised.  
D08 introduce il **deep learning** con PyTorch, che è:

- il framework più usato per ricerca e prototipazione di modelli neurali
- la base per capire meglio i transformer e i LLM (D09)
- lo strumento principale per lavorare con immagini, testo, audio e sequenze

PyTorch è scelto perché:

- API chiara e “pythonica”
- autograd automatico e flessibile
- ecosistema ricco (torchvision, torchaudio, Hugging Face, ecc.)

---

## Obiettivi di apprendimento

Dopo questo modulo dovrei essere in grado di:

- usare tensori, operazioni e autograd in PyTorch
- costruire moduli `nn.Module` (MLP, CNN, LSTM/GRU)
- preparare dataset con `Dataset` e `DataLoader`
- scrivere training loop completi (train/val, checkpoint, logging)
- applicare tecniche di regolarizzazione e interpretare curve di apprendimento
- caricare e usare modelli pre-addestrati (transfer learning base)

---

## 1. Mappa dei concetti

### 1.1 Blocchi principali

1. Tensori e autograd: operazioni, gradienti, computational graph.
2. `nn.Module`: layer, modelli, parametri.
3. Dataset e DataLoader: caricamento, batching, trasformazioni.
4. MLP su dati tabellari.
5. CNN per immagini.
6. RNN (LSTM/GRU) per sequenze.
7. Training loop, regolarizzazione, saving/loading.
8. Transfer learning base (cenni).

---

## 2. Tensori e autograd

### 2.1 Tensori

In PyTorch, un **tensore** è un array n-dimensionale (simile a NumPy) che vive su CPU o GPU.

Operazioni base:

- creazione: `torch.tensor`, `torch.zeros`, `torch.randn`, ecc.
- shape: `tensor.shape`, `tensor.view`, `tensor.reshape`
- operazioni: `+`, `*`, `@` (matmul), funzioni in `torch` (es. `torch.mean`, `torch.sum`)

Differenze rispetto a NumPy:

- può stare su GPU (`tensor.to("cuda")`)
- tiene traccia del gradiente se `requires_grad=True`

Riferimenti:

- [PyTorch Tensors](https://pytorch.org/docs/stable/tensors.html)

### 2.2 Autograd

PyTorch costruisce un **grafo computazionale dinamico**:

- ogni operazione su tensori con `requires_grad=True` viene tracciata
- chiamando `loss.backward()` PyTorch calcola i gradienti rispetto a tutti i parametri
- gli optimizer usano questi gradienti per aggiornare i pesi

Esempio minimale:

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)  # dy/dx = 2x + 3 = 7
```

Riferimenti:

- [Autograd documentation](https://pytorch.org/docs/stable/autograd.html)

---

## 3. `nn.Module`: layer e modelli

### 3.1 Layer base

PyTorch offre layer predefiniti in `torch.nn`:

- `nn.Linear(in_features, out_features)` — layer fully connected
- `nn.Conv2d`, `nn.Conv1d` — convoluzioni per immagini/sequenze
- `nn.LSTM`, `nn.GRU` — reti ricorrenti
- funzioni di attivazione: `nn.ReLU`, `nn.Tanh`, `nn.Sigmoid`, ecc.

### 3.2 Definire un modello

Si crea una classe che eredita da `nn.Module`:

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)
```

Riferimenti:

- [nn.Module docs](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

---

## 4. Dataset e DataLoader

### 4.1 `Dataset`

Un `Dataset` mappa un indice a un campione `(x, y)`:

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
```

Per dataset di immagini si usa spesso `torchvision.datasets` (es. `MNIST`, `CIFAR10`).

### 4.2 `DataLoader`

Il `DataLoader` gestisce:

- batching
- shuffling
- multiprocessing (opzionale)

```python
from torch.utils.data import DataLoader

train_dataset = MyDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
```

Riferimenti:

- [Dataset & DataLoader](https://pytorch.org/docs/stable/data.html)

---

## 5. MLP su dati tabellari

### 5.1 Modello

Per dati tabellari (come in D05–D06) posso usare un MLP:

```python
class TabularMLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, num_classes):
        super().__init__()
        layers = []
        prev = input_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.ReLU()])
            prev = h
        layers.append(nn.Linear(prev, output_dim if num_classes == 1 else num_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)
```

### 5.2 Loss e optimizer

- classificazione binaria: `BCEWithLogitsLoss`
- classificazione multi-classe: `CrossEntropyLoss`
- regressione: `MSELoss` o `L1Loss`

Optimizer tipici: `torch.optim.SGD`, `torch.optim.Adam`.

---

## 6. CNN per immagini

### 6.1 Concetto

Una CNN applica filtri convoluzionali per estrarre feature locali (bordi, texture, pattern).

Blocchi tipici:

- `Conv2d` + `ReLU` + (opzionale) `BatchNorm` + `MaxPool`
- alla fine: layer fully connected per la classificazione

### 6.2 Esempio minimale

```python
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
        self.classifier = nn.Linear(32 * 8 * 8, num_classes)  # per input 32x32

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)
```

Riferimenti:

- [torchvision models](https://pytorch.org/vision/stable/models.html)

---

## 7. RNN: LSTM e GRU per sequenze

### 7.1 Concetto

RNN elaborano sequenze mantenendo uno stato nascosto:

- LSTM e GRU sono varianti che gestiscono meglio le dipendenze a lungo termine
- usate per:
  - testo (prima dei transformer)
  - serie temporali
  - audio, ecc.

### 7.2 Esempio minimale

```python
class LSTMClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, num_classes):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # x: (batch, seq_len, input_dim)
        _, (h_n, _) = self.lstm(x)
        # h_n: (num_layers, batch, hidden_dim)
        last_hidden = h_n[-1]
        return self.fc(last_hidden)
```

Riferimenti:

- [nn.LSTM docs](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

---

## 8. Training loop, regolarizzazione, saving/loading

### 8.1 Training loop base

Schema tipico:

```python
import torch
import torch.nn as nn
import torch.optim as optim

model = TabularMLP(...)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(num_epochs):
    model.train()
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()

    # validation opzionale
    model.eval()
    # ... calcolare metriche su validation set
```

### 8.2 Regolarizzazione

Tecniche comuni:

- **dropout**: `nn.Dropout(p)`
- **weight decay**: `optimizer = Adam(..., weight_decay=1e-4)`
- **early stopping**: fermare il training quando la validation loss smette di scendere
- **data augmentation** (per immagini): rotazioni, flip, crop, ecc.

### 8.3 Saving/loading

```python
# salvare
torch.save(model.state_dict(), "model.pth")

# caricare
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()
```

Riferimenti:

- [Saving and loading models](https://pytorch.org/docs/stable/notes/serialization.html)

---

## 9. Laboratori ed esercizi

### Laboratorio 1 — Primi tensori e autograd

**Obiettivo:** familiarizzare con tensori e gradienti.

**Passi:**

1. Creare tensori con `torch.tensor`, `torch.randn`.
2. Fare operazioni (somma, matmul, ecc.).
3. Definire una funzione semplice (es. \(y = x^2 + 3x + 1\)) e calcolare il gradiente con `backward`.
4. Annotare:
   - differenza tra tensori con/senza `requires_grad`
   - come cambia il gradiente variando la funzione

**Deliverable:**

- notebook/script con esperimenti
- nota con osservazioni su tensori e autograd

---

### Laboratorio 2 — MLP su dati tabellari

**Obiettivo:** costruire e addestrare un MLP per classificazione/regressione.

**Passi:**

1. Usare un dataset tabellare (es. `iris`, `diabetes`, o un CSV proprio).
2. Preparare `Dataset` e `DataLoader`.
3. Definire un `TabularMLP`.
4. Scrivere training loop con training/validation.
5. Valutare accuracy/MSE e tracciare curve di loss.

**Deliverable:**

- notebook/script con MLP addestrato
- nota con curve di loss e interpretazione over/underfitting

---

### Laboratorio 3 — CNN per immagini (MNIST/CIFAR-10)

**Obiettivo:** addestrare una CNN semplice per classificazione di immagini.

**Passi:**

1. Caricare MNIST o CIFAR-10 con `torchvision.datasets`.
2. Definire una `SimpleCNN`.
3. Addestrare con training loop e validation.
4. Visualizzare alcune predizioni corrette/errate.

**Deliverable:**

- notebook/script con CNN addestrata
- nota con accuracy e osservazioni su errori tipici

---

### Laboratorio 4 — LSTM per sequenze (testo o serie)

**Obiettivo:** usare una LSTM per un task sequenziale semplice.

**Passi:**

1. Scegliere un dataset sequenziale (es. serie temporali, o testo tokenizzato).
2. Definire una `LSTMClassifier`.
3. Addestrare e valutare.
4. Confrontare con una baseline non sequenziale (se possibile).

**Deliverable:**

- notebook/script con LSTM
- nota su performance e limiti del modello

---

## 10. Rubriche e checklist

### Checklist — D08 completato

- [ ] So spiegare cos’è un tensore e come funziona l’autograd.
- [ ] So definire un `nn.Module` (MLP, CNN, LSTM).
- [ ] So usare `Dataset` e `DataLoader` per caricare dati.
- [ ] Ho scritto almeno un training loop completo con train/val.
- [ ] Ho applicato tecniche di regolarizzazione (dropout, weight decay, early stopping).
- [ ] Ho salvato e ricaricato un modello addestrato.
- [ ] Ho un progetto DL funzionante (immagini o sequenze) con codice pulito.

### Errori tipici da evitare

- dimenticare `model.train()` / `model.eval()` nei momenti giusti.
- non azzerare i gradienti (`optimizer.zero_grad()`) ad ogni step.
- calcolare la loss su tutto il dataset invece che per batch (problemi di memoria).
- interpretare la training loss senza guardare la validation loss.
- usare GPU senza controllare se i tensori sono realmente su CUDA.

### Segnali che “ho davvero capito” D08

- posso prendere un nuovo dataset (immagini/sequenze) e scrivere un training loop funzionante in poche ore.
- so leggere un errore di shape e capire dove sta il problema.
- so spiegare a un collega perché serve validation e come interpretare le curve di loss.
- non vedo più PyTorch come “magia”, ma come un insieme di tensori, moduli e loop.

---

## 11. Come ripartire dopo una pausa

Se torno su D08 dopo giorni o settimane:

1. Riapro il notebook di un progetto DL (MLP, CNN o LSTM).
2. Rieseguo training e validation per ricordare la struttura.
3. Aggiungo una piccola modifica:
   - nuovo optimizer
   - diverso learning rate
   - altra architettura (es. più layer, dropout)
4. Aggiorno una nota con:
   - cosa ho cambiato
   - effetto su loss e metriche

Scopo: mantenere fresco il legame tra teoria (gradienti, loss) e pratica (codice, esperimenti).

---

## 12. Risorse consigliate

### 12.1 PyTorch ufficiale

- **PyTorch Documentation**  
  Documentazione completa di tensori, autograd, nn, optim, data, ecc.  
  https://pytorch.org/docs/stable/index.html  

- **PyTorch Tutorials**  
  Tutorial ufficiali: da “60 Minutes Blitz” a esempi avanzati.  
  https://pytorch.org/tutorials/  

- **Deep Learning with PyTorch: A 60 Minute Blitz**  
  Introduzione rapida a tensori, autograd, reti e training.  
  https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html  

### 12.2 Corsi e libri

- **Dive into Deep Learning (D2L)**  
  Libro interattivo con codice PyTorch, copre MLP, CNN, RNN, transformer, ecc.  
  https://d2l.ai/  

- **Deep Learning (Goodfellow, Bengio, Courville)**  
  Testo di riferimento per la teoria del deep learning.  
  https://www.deeplearningbook.org/  

### 12.3 Vision e sequenze

- **torchvision models**  
  Modelli pre-addestrati per visione (ResNet, EfficientNet, ecc.).  
  https://pytorch.org/vision/stable/models.html  

- **Hugging Face Transformers**  
  Libreria per transformer (BERT, GPT, ecc.) basata su PyTorch.  
  https://huggingface.co/docs/transformers  

Queste risorse non vanno studiate per intero: D08 serve a darti una base operativa
per usare PyTorch in autonomia e collegarti ai testi/corsi quando serve approfondire.