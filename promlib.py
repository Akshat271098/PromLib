import yaml
import requests

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

prometheus = "http://" + config['prometheus_source'] + "/"
averaging_window_machine = config['averaging_window_machine']


def machine_total(hosts):

    def cpu(host):
        host_node = '"' + host + ':9100"'
        query = 'count(count(node_cpu_seconds_total{{ instance={} }}) by (cpu))'.format(host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        cores = float(results[0]['value'][1])
        return cores

    def memory(host):
        host_node = '"' + host + ':9100"'
        query = ' node_memory_MemTotal_bytes{{ instance={}  }} / (1024^3)'.format(host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        mem = float(results[0]['value'][1])
        return mem

    def disk(host):
        host_node = '"' + host + ':9100"'
        query = 'sum(node_filesystem_size_bytes{{ instance={},device!~"rootfs" }}) / (1024^3)'.format(
            host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        space = float(results[0]['value'][1])
        return space

    def network(host):
        host_node = '"' + host + ':9100"'
        query = 'node_network_speed_bytes{{ instance={} }} * 8/(10^9)'.format(host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        speed = []
        for result in results:
            speed.append(float(result['value'][1]))
        return float(max(speed))

    result=[]
    for host in hosts:
        result.append((cpu(host), memory(host), disk(host), network(host)))

    return result


def machine_current(hosts):

    def cpu(host):
        host_node = '"' + host + ':9100"'
        query = '100 - 100 * avg by (instance) (irate(node_cpu_seconds_total{{ mode="idle",instance={} }} [1m]))'.format(
            host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        # print(float(results[0]['value'][1]))
        total_cpu=machine_total([host])[0][0]
        cpu_use = total_cpu - ((float(results[0]['value'][1]) * total_cpu) / 100)
        return cpu_use

    def memory(host):
        host_node = '"' + host + ':9100"'
        query = ' node_memory_MemAvailable_bytes{{ instance={}  }} / (1024^3)'.format(host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        mem = float(results[0]['value'][1])
        return mem

    def disk(host):
        host_node = '"' + host + ':9100"'
        query = 'sum(node_filesystem_avail_bytes{{ instance={},device!~"rootfs" }})/ (1024^3)'.format(
            host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        space = float(results[0]['value'][1])
        return space

    def network(host):
        host_node = '"' + host + ':9100"'
        query = '(irate(node_network_receive_bytes_total{{ instance={},device!="lo" }}[1m])' \
                '+ irate(node_network_transmit_bytes_total{{ instance={},device!="lo" }}[1m])) *8/ (10^9)'.format(
            host_node, host_node)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        speed = []
        for result in results:
            speed.append(float(result['value'][1]))
        total_net=float(machine_total([host])[0][3])
        return  total_net - float(max(speed))

    result=[]
    for host in hosts:
        result.append((cpu(host), memory(host), disk(host), network(host)))

    return result



def machine_average(hosts):

    def cpu(host):
        host_node = '"' + host + ':9100"'
        query = '(1 - avg(rate(node_cpu_seconds_total{{ mode="idle",instance={} }} [{}])) by ( instance )) *100'.format(
            host_node, averaging_window_machine)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        # print(float(results[0]['value'][1]))
        total_cpu=machine_total([host])[0][0]
        cpu_use = total_cpu - ((float(results[0]['value'][1]) * total_cpu) / 100)
        return cpu_use

    def memory(host):
        host_node = '"' + host + ':9100"'
        query = ' sum(avg_over_time(node_memory_MemAvailable_bytes{{ instance={}  }}[{}]) /(1024^3))'.format(
            host_node, averaging_window_machine)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        mem = float(results[0]['value'][1])
        return mem

    def disk(host):
        host_node = '"' + host + ':9100"'
        query = 'sum(avg_over_time(node_filesystem_avail_bytes{{ instance={},device!~"rootfs" }}[{}])) /(1024^3)'.format(
            host_node, averaging_window_machine)
        # print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        # print(response.json())
        results = response.json()['data']['result']
        space = float(results[0]['value'][1])
        return space

    def network(host):
        host_node = '"' + host + ':9100"'
        query = '(avg by (device) (rate(node_network_receive_bytes_total{{ instance={},device!="lo" }} [{}]))' \
                '+ avg by (device) (rate(node_network_transmit_bytes_total{{ instance={},device!="lo" }} [{}])))* 8 /(10^9)'.format(
            host_node,averaging_window_machine, host_node,averaging_window_machine)
        #print(query)
        response = requests.get(prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        speed = []
        for result in results:
            speed.append(float(result['value'][1]))
        total_net=float(machine_total([host])[0][3])
        return  total_net - float(max(speed))

    result=[]
    for host in hosts:
        result.append((cpu(host), memory(host), disk(host), network(host)))

    return result



