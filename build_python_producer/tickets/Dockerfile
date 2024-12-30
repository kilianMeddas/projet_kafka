FROM python:3.9-slim

# Installer les dépendances du système (si nécessaire)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier le fichier requirements.txt dans l'image Docker
COPY requirements.txt /app/
COPY tickets.py /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans l'image Docker
COPY . /app/

EXPOSE 5000

CMD ["python", "tickets.py"]

