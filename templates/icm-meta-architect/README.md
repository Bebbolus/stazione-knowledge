# ICM Meta-Architect (La Fabbrica)

Benvenuto ne **La Fabbrica**, l'implementazione in riferimento al progetto *RinDig/icm-architect*. Questo template funge da Meta-Architetto: è un ambiente progettato per generare, strutturare e validare *altri* workspace ICM.

## Obiettivo
Quando devi affrontare un'indagine sconosciuta o un task di sviluppo complesso, non crei le cartelle a mano e non usi sciami multi-agente. Utilizzi questo meta-workspace per far generare a un agente specializzato (L'Architetto) la gerarchia di directory ottimali, i file `IDENTITY.md` per ogni stadio, e i `CONTEXT.md` appropriati.

## Componenti
1. `meta_architect.py`: Lo script di validazione che implementa il **Walk Test**.
2. `IDENTITY.md`: Il contratto dell'agente Architetto.

## Il Walk Test
Il "Walk Test" è il collaudo definitivo di un workspace ICM. Viene rilasciato un agente "freddo" (senza memoria conversazionale pregressa) nella cartella generata. Se l'agente riesce a comprendere quale sia il suo ruolo, quali dati deve leggere e dove deve scrivere l'output basandosi ESCLUSIVAMENTE sui file Markdown presenti, l'architettura ICM è valida.
