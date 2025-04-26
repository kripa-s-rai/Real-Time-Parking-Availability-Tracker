
# 🚗Real-Time Parking Availability Tracker

## 📖 Introduction

The **Real-Time Parking Availability Tracker** is a scalable system designed to monitor and analyze parking slot availability in real-time.  
It uses **Apache Kafka** for event streaming, **Apache Spark Streaming** for real-time processing, and **MySQL** for persistent storage and historical batch analytics.

---

## 🚀 Features

- 🔴 **Real-Time Monitoring:** Track live parking availability.  
- 🔗 **Multiple Data Sources:** Sensor devices, mobile apps, external systems.  
- ⚡ **Event-Driven Architecture:** Using Apache Kafka.  
- 🔥 **Real-Time Processing:** Spark Structured Streaming.  
- 🗂️ **Persistent Storage:** MySQL database for historical analysis.  
- 📊 **Batch Analytics:** Spark SQL queries over historical data.  

---

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.8 or above  
- Apache Kafka and Zookeeper  
- Apache Spark  
- MySQL Server  
- Git (optional for cloning)

### Install Python Dependencies

```bash
pip install kafka-python pyspark mysql-connector-python
```

---

## 🖥️ Setup Guide

### 1. Start Kafka and Zookeeper

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker
bin/kafka-server-start.sh config/server.properties
```

### 2. Create Kafka Topics

```bash
bin/kafka-topics.sh --create --topic sensor-topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic app-topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic external-topic --bootstrap-server localhost:9092
```

### 3. Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Inside MySQL shell
source sql/parkingdb.sql;
```

### 4. Run Kafka Producers

```bash
# In separate terminals
python kafka_producer/produce_sensor.py
python kafka_producer/produce_app.py
python kafka_producer/produce_external.py
```

### 5. Run Spark Streaming Job

```bash
spark-submit spark_streaming/spark_streaming.py
```

### 6. Run Spark Batch Job (Optional)

```bash
spark-submit spark_batch/spark_batch.py
```

---

## 📂 Project Structure

```
├── kafka_producer/
│   ├── produce_app.py
│   ├── produce_external.py
│   └── produce_sensor.py
│
├── spark_streaming/
│   └── spark_streaming.py
│
├── spark_batch/
│   └── spark_batch.py
│
├── sql/
│   └── parkingdb.sql
│
└── README.md
```

---

## 📢 Important Commands Summary

| Purpose                       | Command                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| Start Zookeeper               | `bin/zookeeper-server-start.sh config/zookeeper.properties`            |
| Start Kafka Broker            | `bin/kafka-server-start.sh config/server.properties`                   |
| Create Kafka Topics           | `bin/kafka-topics.sh --create --topic <topic-name> --bootstrap-server localhost:9092` |
| Run Kafka Producer (Sensor)   | `python kafka_producer/produce_sensor.py`                              |
| Run Kafka Producer (App)      | `python kafka_producer/produce_app.py`                                 |
| Run Kafka Producer (External) | `python kafka_producer/produce_external.py`                            |
| Run Spark Streaming Job       | `spark-submit spark_streaming/spark_streaming.py`                      |
| Run Spark Batch Job           | `spark-submit spark_batch/spark_batch.py`                              |

---

## 🏁 Final Notes

- Ensure all services (**Kafka**, **Zookeeper**, **MySQL**) are running before starting producers and consumers.  
- Modify connection parameters (like MySQL username/password or Kafka broker address) in scripts if needed.  
- Extend the project easily by adding more producers or real-time analytics logic!
