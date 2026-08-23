---
aliases:
- D01
- Workspace LLM
- Personal Knowledge Base Git
- Second Brain Locale
- Architettura Workspace Local-First
resources:
- title: Learn Git Branching (Simulatore Visuale)
  url: https://learngitbranching.js.org/
  type: lab
- title: Obsidian Official Help
  url: https://help.obsidian.md/
  type: ref
---
# :material-laptop: D01: Architettura Workspace Local-First

![Workspace Locale e Sicuro](assets/local_workspace.jpg)

!!! abstract "Sintesi: Riprendere il Controllo"
    Le app cloud (Notion, Evernote) intrappolano i tuoi dati nei loro server (*lock-in*).
    Se vuoi far leggere i tuoi appunti a un'AI locale per farti aiutare, il cloud ti blocca o viola la tua privacy.
    **La Soluzione**: Salvare tutto in semplici file di testo (Markdown) sul tuo computer, usando Obsidian e Git.

## :material-note-edit: Passo 1: Il Potere del Markdown e Obsidian

Prima di costruire architetture complesse, sporchiamoci le mani. Il segreto di tutto il nostro sistema si chiama **Markdown** (`.md`).
È un modo per scrivere testo formattato (grassetto, titoli, liste) usando solo caratteri normali, senza bisogno di Word.

Per gestire migliaia di questi file senza impazzire, usiamo **Obsidian**, un'app che trasforma i tuoi file `.md` in un "cervello digitale" (Knowledge Base) collegato visivamente.

!!! tip ":fontawesome-solid-download: Azione: Il tuo primo file Markdown"
    1. Scarica e installa **[Obsidian](https://obsidian.md/)** (è gratuito e non richiede account).
    2. Apri Obsidian e crea un nuovo *Vault* (chiamalo `Sandbox`).
    3. Crea una nuova nota chiamata `IlMioPrimoFile`.
    4. Prova a scrivere questo testo:
       ```markdown
       # Questo è un titolo grande
       Questo è testo normale con una parola in **grassetto**.
       ```
    Hai appena creato il tuo primo nodo di conoscenza "Local-First"!

## :material-source-branch: Passo 2: Cos'è Git e cos'è un Repository?

Ora che sai creare i file, sorge un problema: cosa succede se cancelli per sbaglio metà del testo e chiudi l'app? Hai perso tutto.
Ecco dove entra in gioco **[Git](https://git-scm.com/)**.

??? info ":material-gamepad-variant: L'Analogia del Videogioco (Come funziona Git)"
    Hai presente quando affronti un boss difficilissimo e salvi la partita un secondo prima? Se muori, non ricominci da capo, "ricarichi" il salvataggio.
    **Git** è esattamente questo, ma per i tuoi file di testo. Ti permette di scattare una "fotografia" (Commit) della tua cartella. Se fai un disastro, puoi viaggiare nel tempo e tornare indietro!

*   **Cos'è un Repository?** È semplicemente una normale cartella del tuo computer in cui hai "attivato" Git. Git inizia a sorvegliare segretamente ogni modifica che fai ai file lì dentro.
*   **Cos'è Clonare (Clone)?** È l'azione di scaricare un Repository (che qualcuno ha salvato su un server cloud come GitHub) e copiarlo identico sul tuo computer, portandoti dietro tutta la cronologia dei "salvataggi"!

## :material-folder-network: Passo 3: Costruire la "Stazione"

Ora che sai cos'è un file Markdown e cos'è un Repository Git, andiamo a costruire la struttura reale del tuo sistema.
Vogliamo separare nettamente gli appunti pubblici (il corso) da quelli privati (i tuoi segreti o password).

Crea una cartella principale chiamata `Stazione/` e organizzala rigorosamente in questo modo:

```text
Stazione/
├── stazione-knowledge/        # Questo è il Repository Git (clonato da GitHub)
│   ├── README.md
│   ├── index.md               
│   └── docs/                  # Monografie pubbliche (es. questo file D01)
├── private/                   # I tuoi appunti segreti (NESSUN GIT QUI)
│   ├── notes/                 # Note di lavoro
│   └── code/                  # Script Python usa-e-getta
└── inbox/                     # Parcheggio per PDF scaricati da smistare
```

### Come configurare tutto in 3 mosse:

=== "1. Clona il Pubblico"
    Apri il terminale e digita il comando magico per "clonare" il progetto:
    `git clone https://github.com/Bebbolus/stazione-knowledge.git`
    Ora hai una copia locale di tutti i file pubblici!

=== "2. Crea il Privato"
    Di fianco alla cartella appena clonata, crea a mano le cartelle `private/` e `inbox/`.
    Essendo *fuori* dalla cartella tracciata da Git, sei sicuro che i tuoi appunti segreti non finiranno mai su internet per sbaglio.

=== "3. Collega Obsidian"
    Apri Obsidian e digli di aprire l'intera cartella radice `Stazione/`.
    In questo modo potrai collegare (con i link Wiki `[[ ]]`) i tuoi appunti privati direttamente ai manuali pubblici!

## :material-shield-account: Sandboxing per l'Intelligenza Artificiale

Quando avremo il nostro Agente AI locale, lui leggerà questi file. Per evitare che cancelli le tue lezioni per sbaglio, useremo una regola d'oro (Sandboxing).
Nella cartella `private/infra/` creeremo un file `AGENTS.md` in cui scriveremo in inglese semplice: 
*"Caro Agente AI, puoi LEGGERE tutto, ma puoi SCRIVERE solo nella cartella temporanea"*.

***

## :material-tools: I Comandi Magici di Git (Cheat Sheet)

Quando lavorerai sui tuoi file, userai questi 5 comandi come il tuo pane quotidiano:

1. `git init`: Accende la macchina del tempo su una cartella vuota.
2. `git add .`: Prepara tutti i file modificati per il salvataggio.
3. `git commit -m "messaggio"`: Scatta la fotografia definitiva!
4. `git remote add origin https://...`: Collega la tua cartella al cloud (es. GitHub).
5. `git push -u origin main`: Invia la fotografia al cloud come backup.