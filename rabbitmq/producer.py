import pika

if __name__ == '__main__':
    with pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    ) as bunny:
        channel = bunny.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')
