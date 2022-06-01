FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /auctions

COPY requirements.txt /auctions/

RUN pip install -r requirements.txt

COPY . /auctions/
