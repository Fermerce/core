from src.dramatiq_tasks.app import celery_app
from tasks.example.publisher import producer
from src.dramatiq_tasks.example.callback import consumer


@celery_app.task
def publish_message(message):
    producer(message)


@celery_app.task(bind=True, max_retries=3)
def consume_messages(self):
    try:
        consumer()
    except Exception as exc:
        self.retry(exc=exc, countdown=10)


@celery_app.task
def mul(number: int):
    for i in range(number):
        print("Mul %d" % i)
