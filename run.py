#!/usr/bin/env python3
"""
Script de lancement simplifié pour le système de gestion d'invités
Usage: python run.py
"""

import os
import sys
import subprocess

def check_requirements():
    """Vérifie que les dépendances sont installées"""
    required_packages = ['flask', 'pandas', 'qrcode', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Packages manquants:", ', '.join(missing_packages))
        print("📦 Installez-les avec: pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Vérifie que les fichiers nécessaires existent"""
    required_files = ['app.py', 'templates/scan.html']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Fichiers manquants:", ', '.join(missing_files))
        return False
    
    # Créer le dossier templates s'il n'existe pas
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("📁 Dossier 'templates' créé")
    
    return True

def create_sample_csv():
    """Crée un fichier CSV d'exemple s'il n'existe pas"""
    if not os.path.exists('invites.csv'):
        sample_data = """Jean Dupont,Marie Dupont
Jean Dupont,Pierre Dupont
Marie Martin,Sophie Martin
Marie Martin,Paul Martin
Antoine Moreau,Isabelle Moreau
Sophie Bernard,Michel Bernard
Lucas Petit,Nathalie Petit
Emma Durand,Catherine Durand"""
        
        with open('invites.csv', 'w', encoding='utf-8') as f:
            f.write(sample_data)
        
        print("📄 Fichier 'invites.csv' d'exemple créé")
        return True
    
    return False

def main():
    print("🚀 Lancement du système de gestion d'invités")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_requirements():
        sys.exit(1)
    
    if not check_files():
        print("💡 Assurez-vous d'avoir tous les fichiers du projet")
        sys.exit(1)
    
    # Créer CSV d'exemple si nécessaire
    csv_created = create_sample_csv()
    
    print("✅ Vérifications terminées")
    
    if csv_created:
        print("\n📋 Fichier CSV d'exemple créé avec des données de test")
        print("   Vous pouvez modifier 'invites.csv' avec vos propres données")
    
    print("\n🌐 Démarrage du serveur...")
    print("   URL: http://localhost:5000")
    print("   Scanner: http://localhost:5000/scan")
    print("   Arrêt: Ctrl+C")
    print("-" * 50)
    
    # Lancer l'application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()