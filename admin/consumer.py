import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")

django.setup()

from products.models import Product

# https://www.cloudamqp.com/ use this site to create a rabitmq and gave that below

params = pika.URLParameters('rabitmq url')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print("product likes increased")

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started consuming')

channel.start_consuming()

channel.close()