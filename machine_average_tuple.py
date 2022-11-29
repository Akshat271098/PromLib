import requests
from machine_total_tuple import machine_total_tuple

class machine_average_tuple:


    def __init__(self,prometheus,instance,window):
        self.prometheus="http://"+prometheus+"/"
        self.instance='"'+instance+':9100"'
        self.window=window
        self.total = machine_total_tuple(prometheus,instance)

    def cpu(self):
        query='(1 - avg(rate(node_cpu_seconds_total{{ mode="idle",instance={} }} [{}])) by ( instance )) *100'.format(self.instance,self.window)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        #print(float(results[0]['value'][1]))
        cpu_use=self.total.cpu()-float(results[0]['value'][1])/100*self.total.cpu()
        return cpu_use

    def memory(self):
        query=' sum_over_time(node_memory_MemAvailable_bytes{{ instance={}  }}[10m]) /((10*60/15)*(1024^3))'.format(self.instance)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        mem=float(results[0]['value'][1])
        return mem


    def disk(self):
        query='sum_over_time(node_filesystem_avail_bytes{{ instance={},device!~"rootfs",mountpoint="/" }}[10m]) /((10*60/15)*(1024^3))'.format(self.instance)
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