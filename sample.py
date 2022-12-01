import promlib
import all_list

#list all machines and apps
print("\nAll available machines:\n")
print(all_list.get_all_machine_id())

print("\nMaximum resources machine tuples:\n")
print(all_list.get_all_app_list())

#get usages
hosts=["10.24.24.2:9100","bibha.cds.iisc.ac.in:9100"] #host id

app_list=["deathstar:consul","deathstar:frontend"] #pod id

print("\nMaximum resources machine tuples:\n")
print(promlib.machine_total(hosts))

print("\nCurrent resources machine tuples:\n")
print(promlib.machine_current(hosts))

print("\nAverage resources machine tuples:\n")
print(promlib.machine_average(hosts))

print("\nAverage resources application tuples:\n")
print(promlib.application_average(app_list))

print("\nQuantile resources application tuples:\n")
print(promlib.application_quantile(app_list))


