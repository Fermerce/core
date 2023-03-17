from src.celery.app import publish


def publish_message():
    publish(exchange="default", routing_key="default")
