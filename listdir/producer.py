#!/usr/bin/env python
import pika
import json_save

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='listdir', durable=True)

message = json_save
for
channel.basic_publish(
    exchange='',
    routing_key='listdir',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
    ))
print(" [x] Sent %r" % message)
connection.close()