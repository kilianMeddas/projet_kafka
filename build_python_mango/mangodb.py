from flask import Flask, jsonify, request
import pymongo
from kafka import KafkaConsumer
import json
import threading
import time

app = Flask(__name__)

# Connexion à MongoDB
try:
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    db = myclient['caisse']
    collection = db['shop']
    print("Connexion MongoDB réussie.")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")

# Fonction pour créer un consumer Kafka
def create_consumer():
    for _ in range(10):  # Essayer de se connecter pendant 10 tentatives
        try:
            consumer = KafkaConsumer(
                'caisse',  # Correction du topic (était "caisse")
                bootstrap_servers='broker:9092',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("Kafka Consumer connecté avec succès.")
            return consumer
        except Exception as e:
            print(f"Tentative de connexion échouée : {e}. Retente dans 5 secondes.")
            time.sleep(5)
    raise Exception("Impossible de se connecter au broker Kafka après 10 tentatives.")

# Initialisation du consumer Kafka
consumer = create_consumer()

# Fonction de consommation des messages
def consume_messages():
    print("Démarrage de la consommation Kafka...")
    for message in consumer:
        try:
            print(f"Message reçu : {message.value}")
            collection.insert_one(message.value)  # Insérer le message dans MongoDB
            print("Message inséré dans MongoDB avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'insertion dans MongoDB : {e}")

# Lancer le consumer Kafka dans un thread séparé
consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.daemon = True  # Assurez-vous que le thread se termine lorsque l'application s'arrête
consumer_thread.start()

# Route pour récupérer tous les produits depuis MongoDB
@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = list(collection.find({}, {"_id": 0}))  # Exclure MongoDB ObjectID
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des produits : {e}"}), 500

# Route pour récupérer un produit spécifique par nom
@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):
    try:
        product = collection.find_one({"Product": product_name}, {"_id": 0})  # Correction : "name" -> "Product"
        if product:
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération du produit : {e}"}), 500

# Route pour ajouter un produit manuellement via l'API
@app.route('/products', methods=['POST'])
def add_product():
    try:
        new_product = request.json
        collection.insert_one(new_product)
        return jsonify({"message": "Product added successfully."}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'ajout du produit : {e}"}), 500

# Lancer l'application Flask
if __name__ == '__main__':
    print('Starting Flask server...')
    app.run(host='0.0.0.0', port=5050, debug=True)