from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

lots = ['L101', 'L102', 'L103']
statuses = ['available', 'occupied']

while True:
    data = {
        'lot_id': random.choice(lots),
        'status': random.choice(statuses),
        'timestamp': datetime.now().isoformat(),
        'source': 'sensor'
    }
    producer.send('sensor-topic', value=data)
    print(f"Sent: {data}")
    time.sleep(2)
