import pika, json

params = pika.URLParameters('rabitmq url')

connection = pika.BlockingConnection(params)

channel = connection.channel()

# def publish():
#     channel.basic_publish(exchange='', routing_key='main', body='hello main')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)