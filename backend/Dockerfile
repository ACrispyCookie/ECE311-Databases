FROM python:3.10 AS backend

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y openvpn

COPY . .

WORKDIR /app/django_server

CMD ["sh", "entrypoint.sh"]
