import logging
from confluent_kafka import Producer
from settings import CONFLUENT_KAFKA


logger = logging.getLogger(__name__)


producer = Producer(**CONFLUENT_KAFKA)
