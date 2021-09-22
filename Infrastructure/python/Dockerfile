FROM python:3.9.7-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY ./work .
RUN mkdir /usr/src/app/code

RUN pip install --upgrade pip && pip uninstall django && pip install -r requirements.txt
