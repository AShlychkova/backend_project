FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /requirements.txt
COPY ./web_app/  web_app/
COPY ./first_app.py first_app.py
COPY ./config.py config.py

WORKDIR /

ENV FLASK_APP=first_app.py

RUN /bin/bash -c  'pip install -r requirements.txt; \
 flask db init; \
 flask db migrate -m "users table"; \
 flask db upgrade'
RUN echo $FLASK_APP

EXPOSE 5000
COPY ./fin.sh fin.sh 

CMD ["flask", "run"]
