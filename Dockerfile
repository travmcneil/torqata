FROM python:3.7-alpine

RUN adduser -D torqata

WORKDIR /home/torqata

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN apk add gcc linux-headers musl-dev
RUN pip install pandas

COPY app app
COPY migrations migrations
COPY torqata.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP torqata.py

RUN chown -R torqata:torqata ./
USER torqata

EXPOSE 5000
ENTRYPOINT ['./boot.sh']