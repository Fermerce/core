from src.dramatiq_tasks.utils import create_producer
from src.dramatiq_tasks.example.queue import test_queue

producer = create_producer(test_queue)
