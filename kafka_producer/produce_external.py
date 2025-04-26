from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

lots = ['L101', 'L102', 'L103']
external_sources = ['API_1', 'API_2', 'API_3']

while True:
    data = {
        'lot_id': random.choice(lots),
        'source': random.choice(external_sources),
        'availability': random.choice(['available', 'occupied']),
        'timestamp': datetime.now().isoformat(),
        'source': 'external'
    }
    producer.send('external-topic', value=data)
    print(f"Sent: {data}")
    time.sleep(5)
