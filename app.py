from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import sqlite3
import uuid
import qrcode
import os
from datetime import datetime
import hashlib

app = Flask(__name__)

# Configuration
DATABASE = 'invites.db'
QR_CODES_DIR = 'qrcodes'
CSV_FILE = 'invites.csv'

def init_database():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invites (
            id TEXT PRIMARY KEY,
            nom_invite TEXT NOT NULL,
            nom_etudiant TEXT NOT NULL,
            qr_code TEXT UNIQUE NOT NULL,
            utilise BOOLEAN DEFAULT FALSE,
            date_scan TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_qr_code(invite_id, nom_invite, nom_etudiant):
    """Génère un QR code pour un invité"""
    if not os.path.exists(QR_CODES_DIR):
        os.makedirs(QR_CODES_DIR)
    
    # Contenu du QR code (l'ID unique de l'invité)
    qr_content = invite_id
    
    # Création du QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    # Génération de l'image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Nom du fichier
    filename = f"{invite_id}.png"
    filepath = os.path.join(QR_CODES_DIR, filename)
    
    # Sauvegarde
    img.save(filepath)
    
    return qr_content, filepath

def load_csv_to_database():
    """Charge le fichier CSV dans la base de données"""
    if not os.path.exists(CSV_FILE):
        print(f"Fichier {CSV_FILE} non trouvé. Créez-le d'abord.")
        return False
    
    try:
        # Lecture du CSV avec pandas
        df = pd.read_csv(CSV_FILE, header=None, names=['nom_etudiant', 'nom_invite'])
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Vider la table existante
        cursor.execute('DELETE FROM invites')
        
        total_invites = 0
        
        for index, row in df.iterrows():
            nom_etudiant = str(row['nom_etudiant']).strip()
            nom_invite = str(row['nom_invite']).strip()
            
            # Générer un ID unique
            invite_id = str(uuid.uuid4())
            
            # Générer le QR code
            qr_content, qr_filepath = generate_qr_code(invite_id, nom_invite, nom_etudiant)
            
            # Insérer dans la base
            cursor.execute('''
                INSERT INTO invites (id, nom_invite, nom_etudiant, qr_code, utilise)
                VALUES (?, ?, ?, ?, FALSE)
            ''', (invite_id, nom_invite, nom_etudiant, qr_content))
            
            total_invites += 1
            print(f"Ajouté: {nom_invite} (étudiant: {nom_etudiant}) - QR: {qr_filepath}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ {total_invites} invités chargés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False

@app.route('/')
def index():
    """Page d'accueil avec statistiques"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Statistiques
    cursor.execute('SELECT COUNT(*) FROM invites')
    total_invites = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM invites WHERE utilise = TRUE')
    invites_utilises = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM invites WHERE utilise = FALSE')
    invites_restants = cursor.fetchone()[0]
    
    conn.close()
    
    return f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestion des Invités</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #007bff;
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                margin: 10px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }}
            .btn:hover {{
                background: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Gestion des Invités - Cérémonie de Remise de Diplômes</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_invites}</div>
                    <div>Total invités</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{invites_utilises}</div>
                    <div>Déjà scannés</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{invites_restants}</div>
                    <div>En attente</div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/scan" class="btn">📱 Scanner les QR Codes</a>
                <a href="/invites" class="btn">📋 Liste des Invités</a>
                <button onclick="chargerCSV()" class="btn">🔄 Recharger CSV</button>
                <button onclick="document.getElementById('csv-upload').click()" class="btn">📁 Charger nouveau CSV</button>
            </div>
            
            <!-- Upload CSV caché -->
            <input type="file" id="csv-upload" accept=".csv" style="display: none;" onchange="uploadCSV(this)">
            
            <div style="margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 8px;">
                <h3>📱 Accès depuis d'autres appareils :</h3>
                <p><strong>URL de votre réseau :</strong></p>
                <div style="font-family: monospace; background: white; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    http://192.168.1.131:5000
                </div>
                <p><small>💡 Remplacez [VOTRE_IP] par l'IP de cet ordinateur sur votre réseau local</small></p>
            </div>
        </div>
        
        <script>
            async function chargerCSV() {{
                if(confirm('Voulez-vous recharger le fichier CSV? Cela supprimera tous les scans existants.')) {{
                    const response = await fetch('/reload-csv', {{method: 'POST'}});
                    const result = await response.json();
                    alert(result.message);
                    location.reload();
                }}
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/scan')
def scan_page():
    """Page de scan des QR codes"""
    return render_template('scan.html')

@app.route('/verify-qr', methods=['POST'])
def verify_qr():
    """Vérifie un QR code scanné"""
    data = request.get_json()
    qr_content = data.get('qr_code', '').strip()
    
    if not qr_content:
        return jsonify({
            'status': 'error',
            'message': 'QR code vide'
        })
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Rechercher l'invité par QR code
    cursor.execute('SELECT id, nom_invite, nom_etudiant, utilise FROM invites WHERE qr_code = ?', (qr_content,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return jsonify({
            'status': 'invalid',
            'message': '❌ QR code invalide'
        })
    
    invite_id, nom_invite, nom_etudiant, utilise = result
    
    if utilise:
        conn.close()
        return jsonify({
            'status': 'already_used',
            'message': f'⚠️ QR code déjà utilisé',
            'invite': nom_invite,
            'etudiant': nom_etudiant
        })
    
    # Marquer comme utilisé
    cursor.execute('''
        UPDATE invites 
        SET utilise = TRUE, date_scan = ? 
        WHERE id = ?
    ''', (datetime.now(), invite_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': f'✅ Accès autorisé',
        'invite': nom_invite,
        'etudiant': nom_etudiant
    })

@app.route('/invites')
def list_invites():
    """Liste de tous les invités"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nom_invite, nom_etudiant, utilise, date_scan, qr_code
        FROM invites 
        ORDER BY nom_etudiant, nom_invite
    ''')
    
    invites = cursor.fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Liste des Invités</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f2f2f2; }
            .utilise { background-color: #d4edda; }
            .non-utilise { background-color: #f8d7da; }
            .btn { padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>📋 Liste des Invités</h1>
        <a href="/" class="btn">← Retour</a>
        
        <table>
            <tr>
                <th>Nom de l'Invité</th>
                <th>Étudiant</th>
                <th>Statut</th>
                <th>Date de Scan</th>
                <th>QR Code</th>
            </tr>
    '''
    
    for invite in invites:
        nom_invite, nom_etudiant, utilise, date_scan, qr_code = invite
        status_class = "utilise" if utilise else "non-utilise"
        status_text = "✅ Scanné" if utilise else "⏳ En attente"
        date_text = date_scan if date_scan else "-"
        
        html += f'''
            <tr class="{status_class}">
                <td>{nom_invite}</td>
                <td>{nom_etudiant}</td>
                <td>{status_text}</td>
                <td>{date_text}</td>
                <td><a href="/qr/{qr_code}.png" target="_blank">Voir QR</a></td>
            </tr>
        '''
    
    html += '''
        </table>
    </body>
    </html>
    '''
    
    return html

@app.route('/qr/<filename>')
def serve_qr(filename):
    """Sert les images de QR codes"""
    return send_from_directory(QR_CODES_DIR, filename)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Upload et traite un nouveau fichier CSV"""
    if 'csv_file' not in request.files:
        return jsonify({'status': 'error', 'message': '❌ Aucun fichier sélectionné'})
    
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '❌ Aucun fichier sélectionné'})
    
    if not file.filename.lower().endswith('.csv'):
        return jsonify({'status': 'error', 'message': '❌ Le fichier doit être au format CSV'})
    
    try:
        # Sauvegarder le fichier uploadé
        file.save(CSV_FILE)
        
        # Charger dans la base de données
        success = load_csv_to_database()
        if success:
            return jsonify({'status': 'success', 'message': '✅ CSV uploadé et chargé avec succès!'})
        else:
            return jsonify({'status': 'error', 'message': '❌ Erreur lors du traitement du CSV'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'❌ Erreur: {str(e)}'})

@app.route('/reload-csv', methods=['POST'])
def reload_csv():
    """Recharge le fichier CSV existant"""
    success = load_csv_to_database()
    if success:
        return jsonify({'status': 'success', 'message': '✅ CSV rechargé avec succès!'})
    else:
        return jsonify({'status': 'error', 'message': '❌ Erreur lors du rechargement du CSV'})

if __name__ == '__main__':
    # Initialisation
    print("🚀 Initialisation de l'application...")
    init_database()
    
    # Charger le CSV s'il existe
    if os.path.exists(CSV_FILE):
        print("📁 Chargement du fichier CSV...")
        load_csv_to_database()
    else:
        print(f"⚠️  Fichier {CSV_FILE} non trouvé. Créez-le pour commencer.")
    
    print("✅ Application prête!")
    print("🌐 Accès local: http://localhost:5000")
    print("📱 Accès réseau: http://100.91.177.3:5000")
    print("💡 Pour connaître votre IP: ipconfig (Windows) ou ifconfig (Mac/Linux)")
    app.run(debug=True, host='0.0.0.0', port=5000)