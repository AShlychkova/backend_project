import pika
import sys
from sendmail import sendEmail
import time

time.sleep(10)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) ##!!!
channel = connection.channel()
channel.queue_declare(queue='confirming_email')


def callback(ch, method, properties, body):
    email = (str(body)[2:-1]).split()[0]
    text  = (str(body)[2:-1]).split()[1]
    sendEmail(email, text)
    sys.stdout.flush()


channel.basic_consume(on_message_callback=callback,
                      queue='confirming_email')

channel.start_consuming()
