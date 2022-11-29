import promlib

hosts=["bibha.cds.iisc.ac.in","10.24.24.2","10.24.24.128"]

print(promlib.machine_total(hosts))

print(promlib.machine_current(hosts))

print(promlib.machine_average(hosts))


