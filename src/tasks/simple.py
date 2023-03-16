import dramatiq
import sys


@dramatiq.actor
def count_number_of_actors(n):
    for i in range(n):
        print(i)


if "__main__" == __name__:
    sys.exit(count_number_of_actors.send(int(sys.argv[1])))
