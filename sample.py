import promlib

hosts=["10.24.24.2:9100","bibha.iisc.cds.ac.in:9100"] #host id

app_list=["cadvisor-n9w5s","etcd-minikube","kube-state-metrics-6654dd6bb-sbw8k"] #pod id

print(promlib.machine_total(hosts))

print(promlib.machine_current(hosts))

print(promlib.machine_average(hosts))

print(promlib.application_average(app_list))


