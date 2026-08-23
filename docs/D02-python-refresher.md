---
aliases:
- D02
- Python Refresher
- Software Engineering Python
- Python per AI
- Ingegneria del Software Python
resources:
- title: 'Corey Schafer: Python OOP Tutorial'
  url: https://www.youtube.com/watch?v=ZDa-Z5JzLYM
  type: video
- title: Real Python Learning Paths
  url: https://realpython.com/learning-paths/
  type: ref
- title: Pytest Official Docs
  url: https://docs.pytest.org/
  type: ref
---
# Ingegneria del Software e Python per l'AI

L'Intelligenza Artificiale non vive di sola matematica. Affinché un modello diventi un "Agente" in grado di funzionare da solo, deve essere costruito su fondamenta software solide come la roccia.

In questa lezione impareremo a trattare il codice Python come i mattoncini LEGO: moduli separati, test automatici e ambienti isolati.

!!! tip "Spiegato Semplice: Perché l'Ingegneria del Software?"
    Immagina di costruire un'astronave. Se crei un blocco unico (Script Monolitico) e si rompe l'ala, devi buttare via tutta l'astronave.
    
    Se invece usi i "Moduli", puoi semplicemente staccare l'ala rotta e agganciarne una nuova.

## Jupyter Notebook: L'Area Giochi

Quando sviluppiamo un'AI, la prima cosa da fare è "sporcarsi le mani" con i dati per capirli. Non vogliamo scrivere un intero software per fare un grafico, vogliamo qualcosa di rapido e interattivo.

Qui entra in gioco **Jupyter Notebook**.

Jupyter è un quaderno digitale dove puoi scrivere una riga di codice Python, premer play, e vedere immediatamente il risultato (un numero, un grafico, una tabella) direttamente sotto.

!!! info "Come provare Jupyter (Senza installare nulla)"
    Il modo più veloce, usato anche dai professionisti, è **Google Colab**. È un Jupyter Notebook gratuito nel cloud, già configurato!
    
    1. Vai su [colab.research.google.com](https://colab.research.google.com/)
    2. Clicca su **"Nuovo blocco note"**
    3. Scrivi `print("Ciao Intelligenza Artificiale!")`
    4. Premi il tasto Play a sinistra del codice. Fatto!

### Il Lato Oscuro dei Notebook

Jupyter è fantastico per sperimentare, ma è un **incubo** per il software in produzione.

Nei notebook puoi eseguire le celle di codice in ordine sparso. Questo crea confusione in memoria. Se un agente AI deve girare 24 ore su 24 su un server, non possiamo usare un Notebook. Dobbiamo usare script Python veri e propri (`.py`).

## Ambienti Virtuali: venv e Il Nuovo Standard uv

Quando lavoriamo con Python, usiamo pacchetti creati da altri (es. pacchetti per la matematica, per interfacciarci con ChatGPT, ecc.).

Se installi tutti i pacchetti "globalmente" sul tuo PC, succederà un disastro: un progetto chiederà la versione 1 di un pacchetto, un altro progetto chiederà la versione 2, ed esploderà tutto (il temuto *Dependency Hell*).

La soluzione? **Gli Ambienti Virtuali (Virtual Environment - venv)**. 
Un `venv` crea una "bolla" isolata per ogni progetto. Le librerie che installi in quella bolla non toccano il resto del computer. Quando chiudi il progetto, la bolla si spegne.

Oggi, il Re indiscusso per gestire queste bolle si chiama **uv**. È uno strumento moderno (scritto nel velocissimo linguaggio Rust) che ha mandato in pensione i vecchi comandi lenti (`pip` e il vecchio modulo `venv` integrato in Python).

=== "Cos'è uv in pratica?"
    Invece di perdere 10 minuti a configurare cartelle virtuali a mano, con `uv` digiti un comando e lui scarica i pacchetti e crea il tuo `venv` isolato alla velocità della luce.

## Laboratorio Interattivo

Mettiamo in pratica quello che abbiamo imparato su **uv**! 
Nel prossimo esercizio interattivo in fondo alla pagina, dovrai comporre il comando per aggiungere due librerie fondamentali (`requests` e `pytest`) al tuo progetto isolato usando uv!


## Struttura Perfetta di un Progetto

Quando abbandoniamo Jupyter e creiamo un VERO progetto Python, questa è la struttura (Layout) che dobbiamo usare per non impazzire:

```text
mia-stazione-ai/
├── src/               # Qui vive il tuo codice vero e proprio
│   └── main.py
├── tests/             # I test automatici per capire se hai rotto qualcosa
│   └── test_main.py
├── config/            # File YAML con i settaggi
├── logs/              # Un diario di bordo testuale dove l'AI scrive cosa fa
└── .env               # File SEGRETO con le tue chiavi API (MAI METTERLO SU GIT!)
```

## Logging: Basta usare print()!

Quando scrivi codice per imparare, usi `print("Errore")`.
Ma un Agente AI non ha uno schermo, gira su un server. Se usa `print()`, le sue parole svaniscono nel nulla!

Dobbiamo usare il **Logging**.

Il Logging crea un file di testo (il diario di bordo) dove ogni evento viene salvato con la data, l'ora, e il livello di gravità (INFO, WARNING, ERROR).

```python
import logging
logger = logging.getLogger("AgenteOSINT")

logger.info("Ho iniziato a cercare informazioni...")
logger.error("Attenzione! Rete disconnessa!")
```

## I Test Automatici (Pytest)

Non puoi fidarti di te stesso quando programmi. Un giorno modificherai una riga e, senza accorgertene, romperai tutto.

I **Test Unitari** sono piccoli robottini che eseguono il tuo codice per conto tuo, per assicurarsi che dia il risultato corretto. In Python, usiamo una libreria magica chiamata `pytest`.

```python
# test_matematica.py
def somma(a, b):
    return a + b

def test_somma_semplice():
    assert somma(2, 2) == 4
```

Quando scrivi `pytest` nel terminale, lui controlla tutto il tuo progetto. Se vede verde, puoi rilasciare il codice in sicurezza!

## Riassunto della Lezione

1. Usa **Jupyter/Colab** per fare esperimenti sporchi e veloci.
2. Usa **uv** per creare l'ambiente virtuale (`venv`) ed evitare conflitti tra i pacchetti.
3. Organizza il codice in moduli `src/` e scrivi i test in `tests/`.
4. Non usare `print()`, usa il `logging` per tenere traccia di cosa fa il tuo agente.
