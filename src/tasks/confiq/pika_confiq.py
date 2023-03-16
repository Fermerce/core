from src.lib.base.settings import config
import pika


class PikaConnection:
    _instance = None

    def __new__(cls, queue_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=config.broker_host,
                    port=config.broker_port,
                    virtual_host=config.broker_virtual_host,
                    credentials=pika.PlainCredentials(
                        username=config.broker_user, password=config.broker_password
                    ),
                    heartbeat=60,
                )
            )
            cls._instance.channel = cls._instance.connection.channel()
            cls._instance.channel.queue_declare(queue=queue_name)
        return cls._instance

    def close(self):
        self.connection.close()
