# Installation rapide de GeoLite2-City.mmdb

## Option 1: Installation Automatique (Recommandée)

### Prérequis:
1. Compte MaxMind gratuit: https://www.maxmind.com/en/geolite2/signup
2. Clé de licence: https://www.maxmind.com/en/account/login → "Manage License Keys"

### Commande d'installation:
```bash
cd backend
python install_geolite2.py
```

Puis entrez votre clé de licence quand demandée.

---

## Option 2: Installation Manuelle (5 minutes)

### Étape 1: Créer un compte MaxMind
- Allez su: https://www.maxmind.com/en/geolite2/signup
- Remplissez le formulaire (gratuit)

### Étape 2: Obtenir votre clé de licence
1. Connectez-vous: https://www.maxmind.com/en/account/login
2. Cliquez sur "Manage License Keys"
3. Copiez votre clé (commence par des caractères alphanumériques)

### Étape 3: Télécharger la base de données

**URL de téléchargement direct:**
```
https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=YOUR_LICENSE_KEY&suffix=tar.gz
```

Remplacez `YOUR_LICENSE_KEY` par votre clé.

**Ou cliquez directement:**
1. Connecté dans MaxMind: https://www.maxmind.com/en/account/login
2. Section "Download" → "GeoLite2-City"
3. Téléchargez le fichier `.tar.gz` ou `.zip`

### Étape 4: Extraire le fichier

**Windows:**
```powershell
# Avec 7-Zip ou WinRAR (clic droit → Extraire)
# Ou avec PowerShell:
tar -xzf GeoLite2-City_*.tar.gz
```

**Linux/Mac:**
```bash
tar -xzf GeoLite2-City_*.tar.gz
```

### Étape 5: Copier le fichier

Trouvez `GeoLite2-City.mmdb` dans l'archive extraite et copiez-le vers:
```
backend/app/GeoLite2-City.mmdb
```

**Ou en ligne de commande:**
```bash
# Windows
copy "chemin\vers\GeoLite2-City.mmdb" "backend\app\"

# Linux/Mac
cp chemin/vers/GeoLite2-City.mmdb backend/app/
```

---

## Option 3: Vérifier après installation

```bash
cd backend
python
>>> from app.modules.network.geo_service import GeoService
>>> result = GeoService.get_geo_info('8.8.8.8')
>>> print(result)
{
    'ip': '8.8.8.8',
    'country': 'United States',  # ← Doit afficher le pays
    'city': 'Mountain View',
    'latitude': 37.386,
    'longitude': -122.084,
    'timezone': 'America/Los_Angeles'
}
```

Si country n'est plus `None`, ✓ c'est bon!

---

## Dépannage

**Erreur: "Database not found"**
- Vérifie que le fichier est dans: `backend/app/GeoLite2-City.mmdb`
- Vérifié le nom exact du fichier (case-sensitive sur Linux/Mac)

**Erreur: "Geolocation lookup failed"**
- Le fichier GeoLite2-City.mmdb est corrompu
- Retélécharge depuis MaxMind

**Erreur: License key invalid**
- Vérifie que tu as copié la **clé complète**
- Les clés commencent généralement par plusieurs caractères

---

## Quick Links

- 📝 Signup MaxMind: https://www.maxmind.com/en/geolite2/signup
- 🔑 Manage Keys: https://www.maxmind.com/en/account/login
- 📚 Documentation: https://dev.maxmind.com/geoip/geolite2-city

---

## Alternative: Sans GeoService

Si tu ne veux pas installer la base de données maintenant:

1. **Le service retourne `country: None`** - C'est normal sans DB
2. **Les autres services fonctionnent:** IP Resolution, ASN, Discovery
3. **Tu peux ajouter GeoLite2 plus tard** sans changer le code

Pour l'instant: les 3 autres services sont prêts à être testés! ✓
