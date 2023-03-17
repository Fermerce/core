import typing as t
from kombu import Queue, Exchange

task_list: t.List[t.Callable[..., t.Any]] = [
    Queue("default", Exchange("default"), routing_key="default"),
    # Queue("mail", Exchange("mail"), routing_key="mail"),
    # Queue("file", Exchange("file"), routing_key="file"),
]
