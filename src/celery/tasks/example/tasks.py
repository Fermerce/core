from src.celery.app import celery_app
from src.celery.tasks.example.publisher import publish_message


@celery_app.task
def test_task():
    publish_message()


@celery_app.task
def mul(x, y):
    return x * y


@celery_app.task
def xsum(numbers):
    return sum(numbers)
