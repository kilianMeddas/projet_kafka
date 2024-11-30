FROM python:3.11



COPY requirement.txt .
COPY mangodb.py .

RUN pip3 install --no-cache-dir -r requirement.txt

CMD ["python", "mangodb.py"] 