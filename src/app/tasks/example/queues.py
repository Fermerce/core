import typing as t
from kombu import Queue, Exchange

# from src.celery.config import channel

test_queue = Queue(
    name="tasks",
    exchange=Exchange("tasks", type="direct"),
    routing_key="tasks",
)
