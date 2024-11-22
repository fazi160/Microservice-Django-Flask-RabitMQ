import pika, json
import logging
from main import app, Product, db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


params = pika.URLParameters('rabitmq url')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

# Callback function for message processing
def callback(ch, method, properties, body):
    print('Received in main')
    logging.info('Received in main')
    data = json.loads(body)
    print(data)

    with app.app_context():  # Push the Flask application context
        if properties.content_type == 'product created':
            print(f'{properties.content_type} process started')
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print(f'{properties.content_type} process completed')

        elif properties.content_type == 'product updated':
            print(f'{properties.content_type} process started')
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print(f'{properties.content_type} process completed')

        elif properties.content_type == 'Product deleted':
            print(f'{properties.content_type} process started')
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print(f'{properties.content_type} process completed')

# Start consuming messages from RabbitMQ
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming')
logging.info('Started consuming')
channel.start_consuming()
channel.close()
