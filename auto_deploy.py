import paramiko as pk
import subprocess as sp
import os
import re
import yaml



with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

def deploy(vm_selected,app_list,namespace):
    print('Deployment started... \n ')
    rootdir = "../deathstar"
    regex_str=''
    for i in app_list:
        regex_str+='('+i+')|'
    regex_str=regex_str[:len(regex_str)-1]

    #print(regex_str)
    regex = re.compile(regex_str)


    vm_list = ['vm-1', 'vm-2', 'vm-3', 'vm-4']
    file_list = []

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                file_list.append(file)
    print('Files related to these deployments:\n',file_list,'\n')

    str='cd ~/hotelReservation/kubernetes/\n'

    for i in vm_list:
        if vm_selected!=i:
            str+=('kubectl taint nodes {} key1=value1:NoSchedule\n'.format(i))

    for i in file_list:
        str+=('kubectl apply -f {} -n {}\n'.format(i,namespace))

    for i in vm_list:
        if vm_selected!=i:
            str+=('kubectl taint nodes {} key1=value1:NoSchedule-\n'.format(i))

    str += 'kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName={} | head -n 1\n'.format(vm_selected,namespace)
    str+='kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName={} | grep {}'.format(vm_selected,namespace)

    #print(str)



    ssh = pk.SSHClient()
    ssh.set_missing_host_key_policy(pk.AutoAddPolicy())

    ssh.connect(hostname=config['k8s_control_plane'], username='akshat', password='2716')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(str)

    print('Error:')
    for line in iter(ssh_stderr.readline, ""):
        print(line, end="")
    print('finished. \n ')

    print('Output:')
    for line in iter(ssh_stdout.readline, ""):
        print(line, end="")
    print('finished.\n \nDeployment complete \n ')

def clear_namespace(namespace):
    print('Clearing namespace {}...\n'.format(namespace))
    str=''
    str+='kubectl delete daemonsets,replicasets,services,deployments,pods,rc,ingress --all -n {}'.format(namespace)
    ssh = pk.SSHClient()
    ssh.set_missing_host_key_policy(pk.AutoAddPolicy())

    ssh.connect(hostname=config['k8s_control_plane'], username='akshat', password='2716')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(str)

    print('Error:')
    for line in iter(ssh_stderr.readline, ""):
        print(line, end="")
    print('finished. \n')

    print('Output:')
    for line in iter(ssh_stdout.readline, ""):
        print(line, end="")
    print('finished. \n \nNamespace "{}" cleared'.format(namespace))





