import hazelcast
from threading import Thread, Lock

mutex = Lock()

def produce():
    client = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )

    queue = client.get_queue("queue")

    for i in range(1, 101):
        queue.put(i).result()
        with mutex:
            print("--Produced: ", i)
    queue.put(-1).result()
    client.shutdown()


def consume():
    client = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )

    queue = client.get_queue("queue")

    while True:
        item = queue.take().result()
        with mutex:
            print("--Consumed: ", item)
        if item == -1:
            queue.put(item).result()
            break

    client.shutdown()


if __name__ == "__main__":

    threads = [Thread(target=produce)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    client = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )
    queue = client.get_queue("queue")
    queue.clear().result()
    client.shutdown()
