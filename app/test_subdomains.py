from modules.osint.subdomain_service import SubdomainService
import json

def test_discovery():
    target = "google.com"  # Tu peux changer pour tesla.com ou github.com
    print(f"--- Lancement de la découverte passive pour : {target} ---")
    
    # Appel de ton service expert
    results = SubdomainService.get_subdomains(target)
    
    if "error" in results:
        print(f"Erreur lors du test : {results['error']}")
        return

    print(f"Méthode utilisée : {results['method']}")
    print(f"Nombre de sous-domaines uniques trouvés : {results['count']}")
    
    print("\n10 premiers résultats :")
    for sub in results['subdomains'][:10]:
        print(f" - {sub}")

    # Optionnel : Sauvegarder en JSON pour ton rapport
    with open("subdomains_result.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n[+] Résultats complets sauvegardés dans 'subdomains_result.json'")

if __name__ == "__main__":
    test_discovery()