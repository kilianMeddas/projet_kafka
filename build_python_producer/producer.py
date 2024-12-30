from kafka import KafkaProducer
import json
import datetime
import time
import random
from flask import Flask
import requests
import threading

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

app = Flask(__name__)

def get_data():
    try:    
        response = requests.get("http://tickets:5000/tickets")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching tickets: {e}")
        return None

        
@app.route('/sendTickets', methods=['GET'])
def send_ticket_to_kafka():
    # Envoi du ticket au topic Kafka
    ticket_data = get_data()
    if ticket_data:    
        producer.send('caisse', ticket_data)
        print(f"Ticket envoyé : {ticket_data}")
        return "Ticket sent successfully", 200
    else:
        return "Failed to send ticket",500

def auto_send_tickets():
    while True:
        try:
            response = requests.get("http://producer:5001/sendTickets")
            print(f"Auto-call to /sendTickets: {response.status_code}")
        except Exception as e:
            print(f"Error auto-calling /sendTickets: {e}")
        time.sleep(10) 


if __name__ == '__main__':
    threading.Thread(target=auto_send_tickets, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)
