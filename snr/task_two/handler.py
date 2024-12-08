import pika
import time
import os

from snr.utils.logging import logger


class BasicQueueService:
    def __init__(self, queue_name='test_queue'):
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message="Hello, World!") -> str:
        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=message)

        message = f"Sent: {message}"
        print(message)
        logger.info(message)

        return message

    def receive_messages(self):

        def callback(ch, method, properties, body):
            message = f"Received: {body.decode()}"
            print(message)
            logger.info(message)
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)

        print('Waiting for messages.')
        logger.info('Waiting for messages.')

        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()


class WorkQueueService:
    def __init__(self, queue_name='test_queue'):
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=message, properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ))

        print(f"Sent to work queue: {message}")
        logger.info(f"Sent to work queue: {message}")

    def receive_messages(self):
        def callback(ch, method, properties, body):
            print(f"Received {body.decode()}")
            logger.info(f"Received {body.decode()}")
            time.sleep(body.count(b'.'))
            print("Done")
            logger.info("Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Ensure that each worker only processes one message at a time
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback)

        print('Waiting for work queue messages.')
        logger.info('Waiting for work queue messages.')

        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()


class PubSubService:
    def __init__(self, exchange_name='test_exchange'):
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.exchange_name = exchange_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='fanout')

    def publish_message(self, message="Hello, Subscribers!"):
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key='', body=message)

        print(f"Published: {message}")
        logger.info(f"Published: {message}")

    def subscribe(self):
        # Create a unique queue for this subscriber,
        # which will be deleted when the connection is closed
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange
        self.channel.queue_bind(exchange=self.exchange_name, queue=queue_name)

        def callback(ch, method, properties, body):
            print(f"Received from pub/sub: {body.decode()}")
            logger.info(f"Received from pub/sub: {body.decode()}")

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        print('Waiting for messages in pub/sub.')
        logger.info('Waiting for messages in pub/sub.')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()


# if __name__ == "__main__":
#     basic_queue_service = BasicQueueService()
#     basic_queue_service.send_message()
#     basic_queue_service.receive_messages()
#     basic_queue_service.close()

#     work_queue_service = WorkQueueService()
#     for i in range(1, 6):
#         work_queue_service.send_message(f"Task {i}")
#     work_queue_service.receive_messages()

#     work_queue_service.close()

#     pubsub_service = PubSubService()
#     pubsub_service.publish_message("Hello to all subscribers!")
#     pubsub_service.subscribe()
#     pubsub_service.close()
