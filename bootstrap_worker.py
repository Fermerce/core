from dramatiq import Worker
from src.tasks.confiq.dramatiq_config import rabbitmq_broker

worker = Worker(broker=rabbitmq_broker)


if "__main__" == __name__:
    worker.start()
