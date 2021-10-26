import pika
from pika.adapters.blocking_connection import BlockingChannel


def consume(channel, method, properties, body):
    print(channel)
    print(method)
    print(properties)
    print(body)
    print('---')


if __name__ == '__main__':
    with pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    ) as bunny:
        channel = bunny.channel()
        channel.queue_declare(queue='hello')
        channel.basic_consume(queue='hello',
                              auto_ack=True,
                              on_message_callback=consume)

        channel.start_consuming()

        while True:
            pass
