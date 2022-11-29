# PromLib


The promlib module has the following functions which provide the following results:

    machine_total(_host_list_) : A list of tuples (one tuple per host) that contains machine max resources.
    machine_current(_host_list_) : A list of tuples (one tuple per host) that contains machine instantaneous resource state.
    machine_average(_host_list_) : A list of tuples (one tuple per host) that contains current machine resource state by averaging over specified window.
    appication_average(_app_id_list_) : A list of tuples (one tuple per host) that contains application average resource usage over the specified window.

The prometheus source and the window size for average resouce utilization of hosts and the application can be configure in the config.yaml file.

_host_list_ is the list of ip(s) of the target hosts/VMs whose resource state need to obtained.
_app_id_list_ is the list of pod id(s) whose resource utilization need to be obtained.

The tuples returned are of the format:

    machine_total(_host_list_): (MAX CPU CORES, MAX MEMORY, MAX DISK SPACE, MAX NETWORK BANDWIDTH)
    machine_current(_host_list_) : (INST. available CPU CORES, INST. available MEMORY, INST. available  DISK SPACE, INST. available  NETWORK BANDWIDTH)
    machine_average(_host_list_) : (AVG. available CPU CORES, AVG. available  MEMORY, AVG. available  DISK SPACE, AVG. available  NETWORK BANDWIDTH)
    appication_average(_app_id_list_) : (AVG. used CPU CORES, AVG. used MEMORY,AVG. used DISK SPACE, AVG. used NETWORK BANDWIDTH)

The units used (in order as in tuple):

    (Cores, GB, GB, Gbps)
    
See and run sample.py to see how to pass hosts/application with respective ids and use the functions present in promlib to get resource availabiliry/utilization. 

Note : Currently there is some issue with app metrics exporter in default prometheus source so app tuple may not work right now. Has been verified to be working on another prometheus instance with working app metrics.
