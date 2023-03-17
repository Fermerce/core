import json
from celery import Celery
from src.lib.base.settings import config
from src.celery.task_queues import task_list

import kombu

connection = kombu.Connection(
    transport=config.broker_type,
    hostname=config.get_broker_url(include_virtue=False),
    virtual_host=config.broker_virtual_host,
    username=config.broker_user,
    password=config.broker_password,
    port=config.broker_port,
)
k_channel = connection.channel()


def publish(exchange, routing_key):
    with k_channel as channel:
        exchange = kombu.Exchange(
            name="default", exchange=exchange, channel=channel, declare=True
        )
        data = json.dumps({"message": "hello world", "routing_key": routing_key})
        producer = connection.Producer(k_channel)
        producer.publish(
            body=data,
            content_type="application/json",
            exchange=exchange,
            routing_key=routing_key,
            serializer="json",
        )


def consume_from_queue(
    exchange_name, queue_name, routing_key, callback_func, type: str = "direct"
):
    exchange = kombu.Exchange(exchange_name, type=type)
    queue = kombu.Queue(queue_name, exchange, routing_key=routing_key)

    def callback(body, message):
        callback_func(body)
        message.ack()

    with k_channel as _:
        queue.declare()
        consumer = queue.consume(callback)
        print("Started Consuming")
        while True:
            try:
                connection.drain_events()
            except KeyboardInterrupt:
                consumer.cancel()
                break


def create_celery_app(app_name) -> Celery:
    celery_app: Celery = Celery(app_name)
    celery_app.conf.update(
        CELERY_EMAIL_BACKEND=config.email_backend,
        CELERY_EMAIL_HOST=config.email_host,
        CELERY_EMAIL_PORT=config.email_port,
        CELERY_EMAIL_USER=config.admin_email,
        CELERY_EMAIL_PASSWORD=config.admin_password,
        CELERY_EMAIL_USE_TLS=True,
        CELERY_EMAIL_USE_SSL=False,
    )
    celery_app.conf.update(
        CELERY_SEND_TASK_ERROR_EMAILS=True,
        CELERY_TEMPLATE_DEBUG=True,
        CELERY_TASK_ERROR_WHITELIST=(),
        CELERY_TEMPLATE_DIRS=config.email_template_dir,
    )
    # Set the broker and result backend URLs
    # this `celery_app.conf.result_backend`may be set to None in production if this is not needed in the service
    celery_app.conf.broker_url = config.get_broker_url()
    celery_app.conf.result_backend = config.get_broker_result_backend_url()
    celery_app.conf.result_expires = 3600
    # Set the default serializer and content types for messages
    celery_app.conf.task_serializer = "json"
    celery_app.conf.result_serializer = "json"
    celery_app.conf.accept_content = ["json"]

    # Set timezone and UTC flag
    celery_app.conf.timezone = "UTC"
    celery_app.conf.enable_utc = True

    # Define the default exchange and queues
    celery_app.conf.task_queues = tuple(task_list)

    # Load task modules from all registered Django app configs.
    celery_app.autodiscover_tasks()

    return celery_app


celery_app: Celery = create_celery_app(__file__)
