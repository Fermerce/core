import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from src.lib.base.settings import config
from src.tasks.main import tasks_list

# Set up the Dramatiq middleware

# Set up the RabbitMQ broker
rabbitmq_broker = RabbitmqBroker(
    url=config.get_broker_url(),
    confirm_delivery=True,
)

rabbitmq_broker.add_middleware(
    dramatiq.middleware.Retries(max_retries=3),
)


# Set up the Dramatiq actor system with the RabbitMQ broker and middleware
dramatiq.set_broker(rabbitmq_broker)
