from machine_total_tuple import machine_total_tuple
from machine_current_tuple import machine_current_tuple
from machine_average_tuple import machine_average_tuple
from container_tuple import container_tuple
import yaml
import io


with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

prometheus_source=config['prometheus_source']
averaging_window=config['averaging_window']

for host in config['host_list']:
    print("Current host:",host,"\n")

    print("Max resources:")
    total = machine_total_tuple(prometheus_source, host)
    print(total.cpu_memory_disk_network())

    print("\nCurrently available resources(instantaneous)")
    current = machine_current_tuple(prometheus_source, host)
    print(current.cpu_memory_disk_network())

    print("\n Average resources over {} window".format(averaging_window))
    average = machine_average_tuple(prometheus_source, host,averaging_window)
    print(average.cpu_memory_disk_network())


container=container_tuple("192.168.150.128:9090","kube-system","kube-state-metrics-6654dd6bb-sbw8k")

#print(container.cpu())
#print(container.memory())
#print(container.disk())
#print(container.network())

#print(container.cpu_memory_disk_network())