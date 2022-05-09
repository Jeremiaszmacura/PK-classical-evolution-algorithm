FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .