# 🎓 Système de Gestion d'Invités avec QR Codes

Système complet de gestion d'invités pour événements (cérémonies de remise de diplômes, etc.) avec génération et scan de QR codes.

## 📋 Fonctionnalités

- **Chargement automatique** des invités depuis un fichier CSV
- **Génération de QR codes uniques** pour chaque invité
- **Interface de scan** avec webcam (HTML5 + JavaScript)
- **Validation en temps réel** des QR codes
- **Base de données SQLite** pour le suivi des accès
- **Interface web responsive** pour mobile et desktop
- **Statistiques en temps réel** des scans

## 🚀 Installation

### 1. Prérequis
- Python 3.7+
- Webcam (pour le scan des QR codes)

### 2. Cloner et installer les dépendances

```bash
# Créer un dossier pour le projet
mkdir gestion-invites
cd gestion-invites

# Copier les fichiers fournis dans ce dossier

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Structure des fichiers
Votre dossier doit contenir :
```
gestion-invites/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── invites.csv           # Fichier CSV des invités
├── templates/
│   └── scan.html         # Interface de scan
├── qrcodes/              # Dossier des QR codes (créé automatiquement)
├── invites.db            # Base SQLite (créée automatiquement)
└── README.md             # Ce fichier
```

### 4. Préparer le fichier CSV

Le fichier `invites.csv` doit avoir **2 colonnes sans en-têtes** :
- **Colonne 1** : Nom de l'étudiant
- **Colonne 2** : Nom de l'invité

Exemple :
```csv
Jean Dupont,Marie Dupont
Jean Dupont,Pierre Dupont  
Marie Martin,Sophie Martin
Marie Martin,Paul Martin
```

## 🎯 Utilisation

### 1. Démarrer l'application

```bash
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

### 2. Fonctionnement

1. **Chargement automatique** : Au démarrage, l'app charge automatiquement le fichier `invites.csv`
2. **Génération des QR codes** : Un QR code unique est créé pour chaque invité dans le dossier `qrcodes/`
3. **Page d'accueil** (`/`) : Affiche les statistiques et les liens de navigation
4. **Scanner** (`/scan`) : Interface de scan avec webcam
5. **Liste des invités** (`/invites`) : Vue d'ensemble de tous les invités et leur statut

### 3. Scan des QR codes

Sur la page `/scan` :
- Cliquez sur **"Démarrer Scanner"**
- Autorisez l'accès à la caméra
- Pointez la caméra vers un QR code
- Résultats possibles :
  - ✅ **Accès autorisé** : QR valide et première utilisation
  - ⚠️ **Déjà scanné** : QR valide mais déjà utilisé
  - ❌ **Invalide** : QR code non reconnu

### 4. Saisie manuelle

En cas de problème avec la caméra, utilisez la **saisie manuelle** en bas de la page de scan.

## 📊 Interface Web

### Page d'accueil (`/`)
- Statistiques en temps réel
- Total des invités, scannés, en attente
- Liens vers toutes les fonctionnalités

### Page de scan (`/scan`)
- Interface caméra responsive
- Statistiques de scan en temps réel
- Saisie manuelle de secours
- Feedback visuel et sonore

### Liste des invités (`/invites`)
- Tableau complet de tous les invités
- Statut de chaque invité (scanné ou non)
- Date et heure de scan
- Liens vers les QR codes individuels

## 🔧 Configuration

### Modifier le port
Dans `app.py`, ligne finale :
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Changer le port ici
```

### Rechargement du CSV
- Bouton **"Recharger CSV"** sur la page d'accueil
- ⚠️ **Attention** : Supprime tous les scans existants

### Accès aux QR codes
Les QR codes sont accessibles via : `http://localhost:5000/qr/[ID].png`

## 📱 Utilisation Mobile

L'interface est **responsive** et fonctionne parfaitement sur mobile :
- Scanner optimisé pour mobile
- Interface tactile
- Caméra arrière privilégiée automatiquement

## 🗃️ Base de données

Structure de la table `invites` :
```sql
- id (TEXT) : Identifiant unique (UUID)
- nom_invite (TEXT) : Nom de l'invité
- nom_etudiant (TEXT) : Nom de l'étudiant référent
- qr_code (TEXT) : Contenu du QR code (même que l'ID)
- utilise (BOOLEAN) : Statut de scan
- date_scan (TIMESTAMP) : Date/heure de scan
- created_at (TIMESTAMP) : Date de création
```

## 🚨 Dépannage

### Problème de caméra
- Vérifiez les permissions de la caméra dans le navigateur
- Utilisez HTTPS pour un meilleur support caméra
- Testez avec différents navigateurs (Chrome recommandé)

### Erreur de chargement CSV
- Vérifiez le format du CSV (2 colonnes, pas d'en-têtes)
- Vérifiez l'encodage (UTF-8 recommandé)
- Regardez les logs dans le terminal

### QR codes non générés
- Vérifiez les permissions d'écriture dans le dossier
- Le dossier `qrcodes/` sera créé automatiquement

## 🔐 Sécurité

- Les QR codes contiennent des UUID uniques (non devinables)
- Validation côté serveur de tous les scans
- Base de données locale (pas d'exposition réseau)
- Logs de tous les accès avec timestamp

## 🎨 Personnalisation

### Modifier l'apparence
Éditez le CSS dans `templates/scan.html` et les styles inline dans `app.py`

### Ajouter des champs
Modifiez la structure de la base dans la fonction `init_database()` et adaptez le CSV

### Sons de notification
Le son de scan est intégré en base64, modifiable dans `scan.html`

## 📞 Support

En cas de problème :
1. Vérifiez les logs dans le terminal
2. Testez avec le fichier CSV d'exemple fourni
3. Vérifiez que toutes les dépendances sont installées

**Version testée avec :**
- Python 3.8+
- Flask 2.3.3
- Navigateurs modernes (Chrome, Firefox, Safari)
- Systèmes : Windows, macOS, Linux












# 📱 Guide d'accès réseau - Utilisation sur plusieurs appareils

## 🌐 Configuration pour accès multi-appareils

### 1. Trouver votre adresse IP

**Windows :**
```cmd
ipconfig
```
Cherchez "Adresse IPv4" (ex: 192.168.1.100)

**Mac/Linux :**
```bash
ifconfig | grep inet
```
ou
```bash
ip addr show
```

**Alternative simple :**
- Allez dans Paramètres Wi-Fi de votre ordinateur
- Cliquez sur votre réseau connecté
- Notez l'adresse IP

### 2. Lancer l'application avec accès réseau

L'application est déjà configurée pour accepter les connexions réseau :
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 3. Accéder depuis d'autres appareils

**URLs d'accès :**
- **Page principale :** `http://[VOTRE_IP]:5000`
- **Scanner mobile :** `http://[VOTRE_IP]:5000/scan`
- **Liste invités :** `http://[VOTRE_IP]:5000/invites`

**Exemple :**
Si votre IP est `192.168.1.100`, utilisez :
- `http://192.168.1.100:5000/scan`

## 📱 Utilisation sur mobile

### Fonctionnalités mobiles ajoutées :

1. **📁 Upload de fichier CSV**
   - Bouton "Charger nouveau CSV" sur la page d'accueil
   - Permet de sélectionner un fichier CSV depuis les fichiers du téléphone
   - Traitement automatique et génération des QR codes

2. **📷 Caméra optimisée**
   - Interface responsive pour mobile
   - Préférence automatique pour la caméra arrière
   - Conseils d'utilisation affichés
   - Feedback visuel et sonore

3. **⌨️ Saisie manuelle**
   - En cas de problème de caméra
   - Clavier optimisé pour mobile

## 🔧 Configuration avancée

### Sécurité réseau local
```python
# Dans app.py, pour limiter l'accès à votre réseau local uniquement
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Port personnalisé
```python
# Changer le port si 5000 est occupé
app.run(debug=True, host='0.0.0.0', port=8080)
```

### HTTPS pour caméra (optionnel)
Pour un meilleur support caméra sur certains navigateurs :
```bash
# Installer flask-talisman pour SSL
pip install flask-talisman

# Ou utiliser un reverse proxy comme ngrok
ngrok http 5000
```

## 📋 Checklist d'utilisation mobile

✅ **Avant de commencer :**
- [ ] Ordinateur et téléphones sur le même réseau Wi-Fi
- [ ] Application lancée avec `python app.py`
- [ ] IP de l'ordinateur connue
- [ ] Firewall autorise le port 5000

✅ **Sur le téléphone :**
- [ ] Navigateur moderne (Chrome, Safari recommandés)
- [ ] Autorisation caméra accordée au navigateur
- [ ] Bonne luminosité pour scanner les QR codes
- [ ] CSV préparé si upload nécessaire

## 🚨 Dépannage

### Problème de connexion
- Vérifiez que les appareils sont sur le même réseau
- Testez avec `ping [VOTRE_IP]` depuis le téléphone
- Désactivez temporairement le firewall Windows

### Caméra ne fonctionne pas
- Utilisez HTTPS si possible (`https://[IP]:5000`)
- Testez avec Chrome ou Safari
- Vérifiez les permissions caméra du navigateur
- Utilisez la saisie manuelle en dernier recours

### Upload CSV échoue
- Vérifiez le format : 2 colonnes, pas d'en-têtes
- Encodage UTF-8 recommandé
- Taille max 10MB recommandée

## 💡 Conseils d'utilisation

1. **Organisation :**
   - Une personne gère l'ordinateur principal
   - Plusieurs personnes avec téléphones pour scanner
   - QR codes imprimés lisibles (taille min 3x3cm)

2. **Performance :**
   - Redémarrez l'app si beaucoup de scans simultanés
   - Surveillez les statistiques en temps réel
   - Sauvegardez régulièrement la base `invites.db`

3. **Sécurité :**
   - Réseau Wi-Fi sécurisé uniquement
   - Pas d'accès internet requis (fonctionnement local)
   - QR codes uniques non devinables