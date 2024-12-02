FROM python:3.11

# Copier les fichiers nécessaires
COPY requierement.txt .
COPY app.py .
COPY noelbd.jpg .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Installer les dépendances
RUN pip3 install --no-cache-dir -r requierement.txt

# Lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
