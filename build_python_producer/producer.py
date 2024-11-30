from kafka import KafkaProducer
import json
import datetime
import time
import random

# Fonction pour créer un producteur Kafka
def create_producer():
    for _ in range(10):  # Essayer de se connecter pendant 10 tentatives
        try:
            producer = KafkaProducer(
                bootstrap_servers=['broker:9092'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Kafka Producer connecté avec succès.")
            return producer
        except Exception as e:
            print(f"Tentative de connexion échouée : {e}. Retente dans 5 secondes.")
            time.sleep(5)
    raise Exception("Impossible de se connecter au broker Kafka après 10 tentatives.")

# Initialisation du producteur Kafka
producer = create_producer()

# Liste des articles disponibles
articles = [
    'Boules de Noël', 'Guirlandes lumineuses', 'Sapins de Noël',
    'Chaussettes de Noël', 'Calendriers de l Avent', 'Tasses festives',
    'Bougies parfumées', 'Papiers cadeaux', 'Peluches de Noël', 'Ornements de table'
]

# Générer un article aléatoire
def gen_article():
    nom = random.choice(articles)
    prix = int(round(random.uniform(5, 40)))  # Prix entre 5 et 50 euros
    quantite = random.randint(1, 5)
    return (nom, prix, quantite)

# Générer un ticket aléatoire
def gen_ticket_random():
    num_articles = random.randint(1, 10)
    ticket = []
    for _ in range(num_articles):
        nom, prix, quantite = gen_article()
        found = False
        for item in ticket:
            if item[0] == nom:
                item[1] += prix
                item[2] += quantite
                found = True
                break
        if not found:
            ticket.append([nom, prix, quantite])
    return ticket

# Classe Ticket
class Ticket:
    def __init__(self):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date actuelle
        self.article = gen_ticket_random()  # Articles générés aléatoirement
        self.total = sum(a[1] * a[2] for a in self.article)  # Total du ticket

# Fonction pour envoyer un ticket au broker Kafka
def send_ticket_to_kafka():
    while True:
        # Génération d'un ticket
        ticket = Ticket()

        # Structure des données du ticket
        ticket_data = {
            "date": ticket.date,
            "articles": [{"Product": a[0], "price": a[1], "quantity": a[2]} for a in ticket.article],
            "total": round(ticket.total, 2),
        }

        # Envoi du ticket au topic Kafka
        producer.send('caisse', ticket_data)
        print(f"Ticket envoyé : {ticket_data}")

        # Pause de 2 secondes entre les envois de tickets
        time.sleep(2)

# Lancer l'envoi continu des tickets
if __name__ == '__main__':
    send_ticket_to_kafka()
