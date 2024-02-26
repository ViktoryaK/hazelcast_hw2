import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
        cluster_name="hw2",
    )

    my_map = client.get_map("distributed-map").blocking()
    for i in range(1000):
        my_map.put(i, i)
    client.shutdown()