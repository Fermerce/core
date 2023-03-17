import json
from src.celery.app import consume_from_queue


def my_callback(body):
    print("Received in admin")
    # id = json.loads(body)
    print(body["body"])
    #     product = Product.objects.get(id=id)
    #     product.likes = product.likes + 1
    #     product.save()
    print("Product likes increased!")


consume_from_queue(
    exchange_name="default",
    queue_name="default",
    routing_key="default",
    my_callback=my_callback,
)
