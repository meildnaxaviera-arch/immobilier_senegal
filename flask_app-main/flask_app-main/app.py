from flask import Flask, request, jsonify

app = Flask(__name__)

# Données en mémoire pour exemple
users = [
    {"id": 1, "name": "Alice", "age": 29},
    {"id": 2, "name": "Bob", "age": 34},
]

# -------------------------------
# Endpoint GET 1 : accueil
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return "<h1>Bienvenue sur l'API Flask !</h1>"

# -------------------------------
# Endpoint GET 2 : lister les utilisateurs
# -------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# -------------------------------
# Endpoint POST : ajouter un utilisateur
# -------------------------------
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "JSON invalide, champs 'name' et 'age' requis"}), 400

    new_id = max(user["id"] for user in users) + 1 if users else 1
    new_user = {"id": new_id, "name": data["name"], "age": data["age"]}

    users.append(new_user)
    return jsonify(new_user), 201

# -------------------------------
# Lancer le serveur Flask
# -------------------------------
if __name__ == "__main__":
    # Écoute sur toutes les interfaces pour être accessible depuis VM
    app.run(host="0.0.0.0", port=5000, debug=True)
