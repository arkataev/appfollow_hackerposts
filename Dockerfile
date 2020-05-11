FROM python:3.8.2-slim

ADD ./src /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt
