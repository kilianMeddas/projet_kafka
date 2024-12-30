FROM python:3.11


# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    && apt-get clean


COPY requirement.txt .
COPY tickets/tickets.py /app/tickets.py
COPY producer.py .


RUN pip3 install --no-cache-dir -r requirement.txt
RUN pip install flask kafka-python requests

EXPOSE 5001

CMD ["python", "producer.py"] 
