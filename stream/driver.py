
import pika
import json
import sys

name = sys.argv[1]
pattern = sys.argv[2]

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(queue="", exclusive=True)
queue = result.method.queue

channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue,
    routing_key=pattern
)

print(f"{name} listening on {pattern}", flush=True)

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)

        if not message.get("zone"):
            print("NACK:", message, flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        print(f"{name} received {method.routing_key}: {message}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print("Error:", error, flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

channel.basic_consume(
    queue=queue,
    on_message_callback=callback,
    auto_ack=False
)

channel.start_consuming()
