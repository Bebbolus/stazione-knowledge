# Refactoring Globale: Implementazione Direttive ADHD (Manifesto 2026)

L'obiettivo di questo refactoring è allineare l'intera Knowledge Base (31 documenti) alle tre nuove regole didattiche appena inserite nel `manifesto-didattica.md`:
1. **Modular Anchors**: Inserire box visivi (`> [!NOTE]` o `> [!TIP]`) ogni ~15KB per creare punti di salvataggio per l'apprendimento discontinuo.
2. **Checklist Esecutive**: Sostituire le descrizioni discorsive dei passaggi nei Laboratori Pratici con checklist interattive (`- [ ]`) per scaricare la *Working Memory*.
3. **Zero-Draft Offloading**: Introdurre esplicitamente nei Laboratori la direttiva di usare l'Harness (o l'agente) per generare lo scheletro iniziale del codice, contrastando la *Task Initiation Paralysis*.

> [!WARNING]
> **User Review Required: Portata del Refactoring**
> Dalla scansione dei file, ben **24 documenti su 31** superano la soglia dei 15KB (il più grande è D15 con oltre 65KB). Modificare 24 capitoli densi in un singolo flusso sequenziale richiederebbe ore e un altissimo consumo di contesto.

## Open Questions

1. **Strategia di Esecuzione Parallela**: Poiché il lavoro è enorme, ti consiglio caldamente di usare il comando `/teamwork-preview`. Questo permetterà di schierare una squadra di agenti autonomi in parallelo, in cui ognuno prenderà in carico 3-4 file contemporaneamente, completando il refactoring dell'intera *Stazione* in pochi minuti invece che in ore. Sei d'accordo a procedere con il comando `/teamwork-preview`?
2. **Stile dei Checkpoint**: Preferisci che i "Checkpoint di Ancoraggio" contengano un riassunto concettuale (es. "In sintesi, abbiamo visto che...") oppure una domanda di autovalutazione (es. "Sei in grado di spiegare cos'è l'embedding prima di procedere?")?

## Proposed Changes

### Componente: Moduli Core (Teoria)
Per i file massivi (>40KB) come `D09`, `D15`, `D12`, `D16`:
#### [MODIFY] D15-mlops-llmops.md
- Inserimento di 4 Modular Anchors (uno alla fine di ogni macro-sezione).
- Modifica del Laboratorio per includere la Checklist e lo Zero-Draft.

#### [MODIFY] D09-transformers-llm.md
- Inserimento di 4 Modular Anchors.
- Modifica Laboratorio.

#### [MODIFY] Tutti gli altri file >15KB (D12, D16, D10, D13...)
- Inserimento proporzionale di Anchors (1 ogni 15KB stimati).
- Aggiornamento della sezione "Laboratorio Pratico".

### Componente: Moduli Brevi (<15KB)
Per file come `D17`, `D21`, `D01`:
#### [MODIFY] File minori
- Nessun Anchor richiesto.
- Aggiornamento solo per inserire Checklist e Zero-Draft nei Laboratori.

## Verification Plan

### Manual Verification
- Prima di eseguire in massa, faremo una prova su un singolo file massiccio (es. `D15-mlops-llmops.md`) per verificare che lo stile dei Checkpoint e delle Checklist ti soddisfi pienamente.
- Una volta approvato il "pilota", potrai lanciare il team per modificare tutti gli altri.
