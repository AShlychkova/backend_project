FROM python:3.7-alpine
ADD . /
WORKDIR /
RUN sleep 10
RUN pip install -r requirements.txt
CMD ["python", "consume.py"]