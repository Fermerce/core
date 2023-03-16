import typing as t

from tasks.simple import count_number_of_actors

tasks_list: t.List[t.Callable] = [count_number_of_actors]
