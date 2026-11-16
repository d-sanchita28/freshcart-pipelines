
import pika
import json
import random
import time
from datetime import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

cities = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "velachery"]
}

types = ["ride", "food"]

try:
    count = 0
    while True:
        
        count += 1

        if count % 10 == 0:
            message = {
        "id": count,
        "city": "bangalore",
        "type": "food",
        "ts": datetime.now().isoformat()
    }
            routing_key = "bangalore.koramangala.food"
        else:
            city = random.choice(list(cities.keys()))
            zone = random.choice(cities[city])
            order_type = random.choice(types)

            message = {
        "id": count,
        "city": city,
        "zone": zone,
        "type": order_type,
        "ts": datetime.now().isoformat()
    }
            routing_key = f"{city}.{zone}.{order_type}"

        channel.basic_publish(
    exchange="rapido-dispatch",
    routing_key=routing_key,
    body=json.dumps(message)
)

        print("Sent:", routing_key, message, flush=True)
        time.sleep(2)


except KeyboardInterrupt:
    print("Dispatcher stopped")

finally:
    connection.close()
