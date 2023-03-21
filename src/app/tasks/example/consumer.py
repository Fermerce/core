from src.dramatiq_tasks.utils import create_consumer
from src.dramatiq_tasks.example.queue import test_queue


def on_message(body):
    print(f"Consumed message: {body}")
    for i in range(body["age"]):
        print(f"Sleeping for {i} seconds")


consumer = create_consumer(queue=test_queue, callback=on_message)
