"""
meta_architect.py - RinDig/icm-architect Walk Test Implementation
Valida un workspace ICM controllando l'esistenza e la completezza formale dei contratti.
"""
import os
import sys

def run_walk_test(workspace_path: str) -> bool:
    print(f"[*] Inizio Walk Test sul workspace: {workspace_path}")
    
    if not os.path.isdir(workspace_path):
        print("[-] Errore: Path non trovato.")
        return False
        
    stages = [d for d in os.listdir(workspace_path) if os.path.isdir(os.path.join(workspace_path, d))]
    if not stages:
        print("[-] Errore: Nessuna cartella di stadio trovata.")
        return False
        
    all_passed = True
    for stage in sorted(stages):
        stage_path = os.path.join(workspace_path, stage)
        identity_file = os.path.join(stage_path, "IDENTITY.md")
        context_file = os.path.join(stage_path, "CONTEXT.md")
        
        print(f"\n[+] Valutazione Stadio: {stage}")
        
        # 1. Verifica Esistenza
        if not os.path.exists(identity_file):
            print("  [-] MANCANTE: IDENTITY.md")
            all_passed = False
        else:
            with open(identity_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if "ruolo" not in content or "vincoli" not in content:
                    print("  [!] WARNING: IDENTITY.md potrebbe essere incompleto (mancano 'ruolo' o 'vincoli').")
                else:
                    print("  [+] IDENTITY.md presente e strutturato.")
                    
        if not os.path.exists(context_file):
            print("  [-] MANCANTE: CONTEXT.md")
            all_passed = False
        else:
            with open(context_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if "obiettivo" not in content:
                    print("  [!] WARNING: CONTEXT.md potrebbe essere incompleto (manca 'obiettivo').")
                else:
                    print("  [+] CONTEXT.md presente e strutturato.")

    print("\n===============================")
    if all_passed:
        print("[+] WALK TEST SUPERATO. Il workspace è pronto per l'agentic handoff.")
        return True
    else:
        print("[-] WALK TEST FALLITO. Correggere i file mancanti prima dell'esecuzione.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python meta_architect.py <percorso_workspace>")
        sys.exit(1)
    run_walk_test(sys.argv[1])
