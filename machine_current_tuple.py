import requests
from machine_total_tuple import machine_total_tuple

class machine_current_tuple:


    def __init__(self,prometheus,instance):
        self.prometheus="http://"+prometheus+"/"
        self.instance='"'+instance+':9100"'

        self.total = machine_total_tuple(prometheus,instance)

    def cpu(self):
        query='100 - 100 * avg by (instance) (irate(node_cpu_seconds_total{{ mode="idle",instance={} }} [1m]))'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        #print(float(results[0]['value'][1]))
        cpu_use=self.total.cpu()-((float(results[0]['value'][1]) * self.total.cpu())/100)
        return cpu_use

    def memory(self):
        query=' node_memory_MemAvailable_bytes{{ instance={}  }} / (1024^3)'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        mem=float(results[0]['value'][1])
        return mem


    def disk(self):
        query='node_filesystem_avail_bytes{{ instance={},device!~"rootfs",mountpoint="/" }} / (1024^3)'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        space=float(results[0]['value'][1])
        return space

    def network(self):
        query='(irate(node_network_receive_bytes_total{{ instance={},device!="lo" }}[1m])' \
              '+ irate(node_network_transmit_bytes_total{{ instance={},device!="lo" }}[1m])) *8/ (10^9)'.format(self.instance,self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        speed=[]
        for result in results:
            speed.append(float(result['value'][1]))
        return self.total.network()-float(max(speed))

    def cpu_memory_disk_network(self):
        result=(self.cpu(),self.memory(),self.disk(),self.network())
        return result