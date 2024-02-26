import hazelcast
from threading import Thread


def increment():
    client1 = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )
    my_map = client1.get_map("distributed-map").blocking()

    for k in range(10000):
        my_map.lock(0)
        try:
            v = my_map.get(0)
            v += 1
            my_map.put(0, v)
        finally:
            my_map.unlock(0)

    client1.shutdown()

def increment_optimistic():
    client1 = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )
    my_map = client1.get_map("distributed-map").blocking()

    for k in range(10000):
        while True:
            v_old = my_map.get(0)
            v_new = v_old
            v_new += 1
            if my_map.replace_if_same(0, v_old, v_new):
                break

    client1.shutdown()

def main():
    threads = []
    for i in range(3):
        t = Thread(target=increment_optimistic)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
