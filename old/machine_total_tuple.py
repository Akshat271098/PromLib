import requests

class machine_total_tuple:
    def __init__(self,prometheus,instance):
        self.prometheus="http://"+prometheus+"/"
        self.instance='"'+instance+':9100"'


    def cpu(self):
        query='count(count(node_cpu_seconds_total{{ instance={} }}) by (cpu))'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        cores=float(results[0]['value'][1])
        return cores

    def memory(self):
        query=' node_memory_MemTotal_bytes{{ instance={}  }} / (1024^3)'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        mem=float(results[0]['value'][1])
        return mem

    def disk(self):
        query='node_filesystem_size_bytes{{ instance={},device!~"rootfs",mountpoint="/" }} / (1024^3)'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        space=float(results[0]['value'][1])
        return space

    def network(self):
        query='node_network_speed_bytes{{ instance={} }} * 8/(10^9)'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        speed=[]
        for result in results:
            speed.append(float(result['value'][1]))
        return float(max(speed))

    def cpu_memory_disk_network(self):
        result=(self.cpu(),self.memory(),self.disk(),self.network())
        return result