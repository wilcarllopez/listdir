import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='listdir')


def callback(body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback, queue='listdir', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
