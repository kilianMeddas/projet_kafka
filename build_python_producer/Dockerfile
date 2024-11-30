FROM python:3.11


# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    && apt-get clean


COPY requirement.txt .
COPY producer.py .

RUN pip3 install --no-cache-dir -r requirement.txt

CMD ["python", "producer.py"] 