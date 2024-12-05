import pymongo
from kafka import KafkaConsumer
import json
import threading
import time

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
def consume_messages(number_max):
    print("Démarrage de la consommation Kafka...")
    liste = []
    for message in consumer:
        try:
            print(f"Message reçu : {message.value}")
            liste.append(message.value)
            if len(liste) >= number_max:
                collection.insert_many(liste)  # Insérer le message dans MongoDB
                print(f"{len(liste)} messages inséré dans MongoDB avec succès.")
                liste = []
        except Exception as e:
            print(f"Erreur lors de l'insertion dans MongoDB : {e}")

# Lancer le consumer Kafka dans un thread séparé
consumer_thread = threading.Thread(target=consume_messages(5))
consumer_thread.daemon = True  # Assurez-vous que le thread se termine lorsque l'application s'arrête
consumer_thread.start()