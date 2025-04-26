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
user_ids = ['U001', 'U002', 'U003']

while True:
    data = {
        'lot_id': random.choice(lots),
        'user_id': random.choice(user_ids),
        'status': random.choice(['checked-in', 'checked-out']),
        'timestamp': datetime.now().isoformat(),
        'source': 'app'
    }
    producer.send('app-topic', value=data)
    print(f"Sent: {data}")
    time.sleep(3)
