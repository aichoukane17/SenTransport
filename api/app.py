import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(__file__)

# =====================================================================
# FONCTION UTILITAIRE : Lecture dynamique du fichier lignes_ddd.json (Exo 2)
# =====================================================================
def charger_lignes_en_temps_reel():
    file_path = os.path.join(base_dir, "lignes_ddd.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Sûreté au cas où le fichier n'est pas renommé ou possède une autre extension
        alt_path = os.path.join(base_dir, "Lignes_ddd.js")
        if os.path.exists(alt_path):
            with open(alt_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

# =====================================================================
# ROUTE D'ACCUEIL
# =====================================================================
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue sur l'API SènTransport !"})

# =====================================================================
# LAB 5 - EXO 1 & 2 : Liste globale de toutes les lignes
# =====================================================================
@app.route('/lignes', methods=['GET'])
def get_lignes():
    lignes = charger_lignes_en_temps_reel()
    return jsonify(lignes)

# =====================================================================
# LAB 5 - EXO 3 : Détails d'une ligne spécifique via son ID au clic
# =====================================================================
@app.route('/lignes/<int:ligne_id>', methods=['GET'])
def get_ligne(ligne_id):
    lignes = charger_lignes_en_temps_reel()
    # Recherche de la ligne par son identifiant unique
    ligne = next((l for l in lignes if l.get('id') == ligne_id), None)
    
    if ligne is None:
        return jsonify({"erreur": "Ligne non trouvée"}), 404
    return jsonify(ligne)

# =====================================================================
# ROUTE /arrets : Fusion de l'étape géolocalisée et des arrêts uniques
# =====================================================================
@app.route("/arrets", methods=['GET'])
def get_arrets():
    arrets_path = os.path.join(base_dir, "arrets.json")
    
    # Si le fichier arrets.json existe (Étape 2 du nouveau module), on l'envoie directement
    if os.path.exists(arrets_path):
        with open(arrets_path, "r", encoding="utf-8") as f:
            arrets_geolocalises = json.load(f)
        return jsonify(arrets_geolocalises)
    
    # ANCIEN EXO 1 (Secours) : Extraction sans doublons depuis les lignes
    lignes = charger_lignes_en_temps_reel()
    arrets_uniques = set()
    for ligne in lignes:
        # Prise en compte de 'listeArrets' ou 'arrets' selon la structure du JSON
        liste_arrets = ligne.get('listeArrets', ligne.get('arrets', []))
        for arret in liste_arrets:
            arrets_uniques.add(arret)
            
    return jsonify(list(arrets_uniques))

# =====================================================================
# AUTRE EXO : Statistiques du réseau de transport
# =====================================================================
@app.route('/stats', methods=['GET'])
def get_stats():
    lignes = charger_lignes_en_temps_reel()
    total_lignes = len(lignes)
    total_arrets_cumules = 0
    
    ligne_max_arrets = None
    max_arrets_count = -1

    for ligne in lignes:
        liste_arrets = ligne.get('listeArrets', ligne.get('arrets', []))
        nb_arrets_ligne = len(liste_arrets)
        
        total_arrets_cumules += nb_arrets_ligne
        
        if nb_arrets_ligne > max_arrets_count:
            max_arrets_count = nb_arrets_ligne
            ligne_max_arrets = ligne.get('numero', ligne.get('id')) 

    return jsonify({
        "nombre_total_lignes": total_lignes,
        "somme_totale_arrets": total_arrets_cumules,
        "ligne_ayant_le_plus_d_arrets": ligne_max_arrets
    })

# =====================================================================
# AUTRE EXO : Recherche et filtrage de lignes par terminus (?q=...)
# =====================================================================
@app.route('/lignes/recherche', methods=['GET'])
def chercher_lignes():
    lignes = charger_lignes_en_temps_reel()
    query = request.args.get('q', '').lower()
    lignes_trouvees = []
    
    for ligne in lignes:
        depart = ligne.get('depart', '').lower()
        arrivee = ligne.get('arrivee', '').lower()
        
        if query in depart or query in arrivee:
            lignes_trouvees.append(ligne)
            
    return jsonify(lignes_trouvees)

if __name__ == "__main__":
    # Lancement du serveur sur le port 5000 avec rechargement automatique
    app.run(debug=True, port=5000)