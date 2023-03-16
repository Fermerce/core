from src.lib.base.settings import config
from tasks.confiq.dramatiq_config import rabbitmq_broker

# RabbitMQ broker configuration
RABBITMQ_BROKER = {
    "broker_class": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "options": {"url": config.get_broker_url()},
    "middleware": ["dramatiq.middleware.Retries"],
    "actor_options": {"max_retries": 3},
}

# Set up the RabbitMQ broker
rabbitmq_broker.configure(**RABBITMQ_BROKER)
