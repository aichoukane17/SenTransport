from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Chargement des données JSON sécurisé
# (Prend en compte le renommage de ton fichier en lignes_ddd.json)
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "lignes_ddd.json")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        lignes = json.load(f)
except FileNotFoundError:
    # Sûreté au cas où le fichier n'est pas encore renommé
    with open(os.path.join(base_dir, "Lignes_ddd.js"), "r", encoding="utf-8") as f:
        lignes = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue sur l'API SènTransport !"})

@app.route('/lignes', methods=['GET'])
def get_lignes():
    return jsonify(lignes)

@app.route('/lignes/<int:ligne_id>', methods=['GET'])
def get_ligne(ligne_id):
    # Recherche d'une ligne par son ID
    ligne = next((l for l in lignes if l.get('id') == ligne_id), None)
    if ligne is None:
        return jsonify({"erreur": "Ligne non trouvée"}), 404
    return jsonify(ligne)


# =====================================================================
# EXO 1 : Liste de tous les arrêts sans doublons
# =====================================================================
@app.route('/arrets', methods=['GET'])
def get_all_arrets():
    # Un 'set' en Python supprime automatiquement les valeurs dupliquées
    arrets_uniques = set()
    
    # On parcourt chaque ligne de bus
    for ligne in lignes:
        # On récupère la liste des arrêts (si elle existe, sinon liste vide [])
        for arret in ligne.get('listeArrets', []):
            arrets_uniques.add(arret)
            
    # On convertit le set en liste classique pour pouvoir la renvoyer en JSON
    return jsonify(list(arrets_uniques))


# =====================================================================
# EXO 2 : Statistiques du réseau de transport
# =====================================================================
@app.route('/stats', methods=['GET'])
def get_stats():
    total_lignes = len(lignes)
    total_arrets_cumules = 0
    
    ligne_max_arrets = None
    max_arrets_count = -1

    for ligne in lignes:
        # On récupère le nombre d'arrêts de la ligne actuelle
        nb_arrets_ligne = len(ligne.get('listeArrets', []))
        
        # Cumul pour la somme totale
        total_arrets_cumules += nb_arrets_ligne
        
        # Recherche de la ligne qui a le plus d'arrêts
        if nb_arrets_ligne > max_arrets_count:
            max_arrets_count = nb_arrets_ligne
            # On stocke le numéro/nom de la ligne
            ligne_max_arrets = ligne.get('nom', ligne.get('id')) 

    return jsonify({
        "nombre_total_lignes": total_lignes,
        "somme_totale_arrets": total_arrets_cumules,
        "ligne_ayant_le_plus_d_arrets": ligne_max_arrets
    })


# =====================================================================
# EXO 3 : Recherche et filtrage de lignes par terminus (?q=...)
# =====================================================================
@app.route('/lignes/recherche', methods=['GET'])
def chercher_lignes():
    # Récupération du paramètre d'URL 'q' (ex: ?q=Pikine), mis en minuscules
    query = request.args.get('q', '').lower()
    
    lignes_trouvees = []
    
    for ligne in lignes:
        # Extraction du départ et de l'arrivée en minuscules pour ignorer la casse
        depart = ligne.get('depart', '').lower()
        arrivee = \
        ligne.get('arrivee', '').lower()
        
        # Si le mot recherché est présent dans le départ OU l'arrivée
        if query in depart or query in arrivee:
            lignes_trouvees.append(ligne)
            
    return jsonify(lignes_trouvees)


if __name__ == "__main__":
    app.run(debug=True, port=5000)