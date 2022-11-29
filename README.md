# Prometheus-query-python

The prometheus source, hosts whose metrics are to be pulled and the window size for average resouce utilization of hosts can be configure in the config.yaml file.

Run main.py to get the following results:
   *Machine max resources
   *Machine current resource state
   *Machine resource state ny averaging over specified window

The tuples returned are of the format:
    *(CPU CORES, MEMORY, DISK SPACE, NETWORK BANDWIDTH)

The units used (in order as in tuple):
    *(cores, GB, GB, Gbps)
