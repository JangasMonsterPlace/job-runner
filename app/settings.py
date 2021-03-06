import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME")
}

CONFLUENT_KAFKA = {
    "bootstrap.servers": os.getenv("KAFKA_CLUSTER_SERVER"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_CLUSTER_API_KEY"),
    'sasl.password': os.getenv("KAFKA_CLUSTER_API_SECRET")
}
