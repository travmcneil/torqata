FROM python:slim

RUN useradd torqata

WORKDIR /home/torqata

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY torqata.py config.py boot.sh ./
COPY app.db app.db
RUN chmod a+x boot.sh
RUN apt update
RUN apt-get install python-tk -y
# RUN apt install gcc -y
# RUN apt install linux-headers -y
# RUN apt install musl-dev -y
RUN venv/bin/pip install tk
RUN venv/bin/pip install pandas

ENV FLASK_APP torqata.py

RUN chown -R torqata:torqata ./
USER torqata

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]