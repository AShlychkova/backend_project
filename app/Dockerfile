FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev


EXPOSE 5000

ENV FLASK_APP=first_app.py

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

#WORKDIR /


COPY ./web_app/  web_app/
COPY ./first_app.py first_app.py
COPY ./config.py config.py


COPY ./fin.sh fin.sh

RUN chmod +x fin.sh

CMD /fin.sh



