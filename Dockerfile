FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements-prod.txt

CMD ["python", "main.py"]
