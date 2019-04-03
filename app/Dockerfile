FROM ubuntu:16.04

MAINTANER Aleksandra Shlychkova "aleksandrashlychkova@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt
COPY ./web_app/  web_app/
COPY ./first_app.py first_app.py
COPY ./config.py config.py

WORKDIR /

RUN pip install -r requirements.txt
RUN export FLASK_APP=first_app.py
RUN flask db init
RUN flask db migrate -m "users table"
RUN flask db upgrade

ENTRYPOINT [ "bash" ]

CMD [ "flask run" ]