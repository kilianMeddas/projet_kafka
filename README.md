# Kafka-MongoDB Integration with Python Producers and Consumers

This project demonstrates how to integrate Kafka and MongoDB using Docker. The setup includes Python-based producer and consumer services, Kafka for message streaming, and MongoDB for data storage.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Services Description](#services-description)
- [Usage](#usage)
- [Contributors](#contributors)
- [Useful links](#useful-links)

---

## Overview

This project comprises:
1. A Kafka producer generating random tickets and publishing them to a Kafka topic.
2. A Kafka consumer that consumes messages from Kafka and stores them in MongoDB.
3. A user-friendly interface to monitor Kafka topics using Kafdrop.
4. A web interface to view MongoDB data using Mongo-Express.

---

## Architecture du projet
![Architecture](Architecture.jpg)


---
## Project Structure

```plaintext
.
├── build_python_mongo
│   ├── Dockerfile
│   ├── mangodb.py               # Python script for MongoDB consumer
│   └── requirements.txt     # Python dependencies
├── build_python_producer
│   ├── Dockerfile
│   ├── producer.py          # Python script for Kafka producer
│   └── requirements.txt     # Python dependencies
├── docker-compose.yml       # Docker Compose configuration file
├── stats
│   ├── Dockerfile
│   ├── api_stat.py          # Python script for API statistics
│   ├── connect.py           # Python script to connect to database (MongoDB)
│   ├── requirements.txt
│   ├── statistics.py        # Collect total revenue
│   ├── statistics2.py       # Collect average revenue
│   ├── statistics3.py       # Collect revenue by product
│   ├── statistics4.py       # Collect sales by day and month
│   └── statistics5.py       # Collect revenue by day and month
└── README.md
```
---

## Technologies Used
* Docker: For containerizing services.
* Kafka: As the message broker.
* MongoDB: For storing consumed messages.
* Kafdrop: Kafka monitoring tool.
* Mongo-Express: Web-based MongoDB administration tool.
* Python: For the producer and consumer scripts.

---
## Setup and Installation

#### Prerequisites
* Docker
* Docker Compose

### Steps
1) Clone the repository:
``` bash
git clone https://github.com/kilianMeddas/projet_kafka.git
cd projet_kafka
```

2) Build Docker images for the producer and consumer: (optionnal if image still available in dockerhub) :

```bash
docker build -t kmeddas/producer_api_without_flask ./build_python_producer
docker build -t kmeddas/consumer_api ./build_python_mongo
```

3) Start all services:
```bash
docker compose up
```
or
```bash
docker-compose up
```

4) Access the services:
* Kafdrop: http://localhost:9000
* Mongo-Express: http://localhost:8081
* Producer API: http://localhost:5000
* Consumer API: http://localhost:5050


## Useful links
* https://hub.docker.com/r/kmeddas/consumer_api
* https://hub.docker.com/r/kmeddas/producer_api_without_flask
* https://hub.docker.com/r/apache/kafka
* https://hub.docker.com/_/mongo

