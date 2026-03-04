from modules.osint.osint_orchestrator import OSINTOrchestrator
import json

def main():
    target = "google.com" # Ou n'importe quel domaine
    
    # Exécution
    orchestrator = OSINTOrchestrator()
    final_report = orchestrator.run_full_analysis(target)
    
    # Affichage rapide dans la console
    print("\n" + "="*50)
    print(f"RAPPORT OSINT POUR : {target}")
    print(f"Sous-domaines trouvés : {final_report['summary']['subdomains_count']}")
    print(f"Serveur détecté : {final_report['summary']['web_server']}")
    print(f"Validité SSL : {'VALIDE' if final_report['summary']['is_ssl_valid'] else 'INVALIDE'}")
    print("="*50)
    
    # Sauvegarde professionnelle
    filename = f"report_{target.replace('.', '_')}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)
    
    print(f"\n[!] Rapport complet généré : {filename}")

if __name__ == "__main__":
    main()