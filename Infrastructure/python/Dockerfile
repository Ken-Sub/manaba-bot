FROM python:3.9.7-slim-buster
ENV PYTHONUNBUFFERED=1
ENV TZ='Asia/Tokyo'

WORKDIR /usr/src/app
COPY ./work .
RUN mkdir /usr/src/app/code

RUN apt-get -y update && \
    apt-get install -y apt-utils && \
    apt-get install -y wget && \
    apt-get install -y curl && \
    apt-get install -y unzip && \
    wget -q -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    apt-get install -y libgbm1 libappindicator3-1 libappindicator1 fonts-liberation libasound2 libnspr4 libnss3 libxss1 lsb-release xdg-utils libfontconfig && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb

RUN export LANG=C.UTF-8
RUN export LANGUAGE=en_US:
RUN apt-get install -y fonts-ipafont

RUN pip install --upgrade pip && pip uninstall django && pip install -r requirements.txt
