# Dockerfile

# Utiliser l'image officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de votre application
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Installer Gunicorn
RUN pip install gunicorn

# Lancer Gunicorn avec votre application Flask
CMD ["gunicorn", "-b", "0.0.0.0:8000", "api_stat:app"]


