# PromLib


The promlib module has the following functions which provide the following results:

    machine_total(_host_list_) : A list of tuples (one tuple per host) that contains machine max resources.
    machine_current(_host_list_) : A list of tuples (one tuple per host) that contains machine instantaneous resource state.
    machine_average(_host_list_) : A list of tuples (one tuple per host) that contains current machine resource state by averaging over specified window.
    appication_average(_app_id_list_) : A list of tuples (one tuple per host) that contains application average resource usage over the specified window (in progress)

The prometheus source and the window size for average resouce utilization of hosts and the application can be configure in the config.yaml file.

The tuples returned are of the format:

    (CPU CORES, MEMORY, DISK SPACE, NETWORK BANDWIDTH)

The units used (in order as in tuple):

    (Cores, GB, GB, Gbps)
    
See and run sample.py to see how to pass hosts/application with respective ids and use the functions present in promlib to get resource availabiliry/utilization.
