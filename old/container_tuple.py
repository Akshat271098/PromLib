import requests

class container_tuple:
    def __init__(self,prometheus,namespace,container):
        self.prometheus="http://"+prometheus+"/"
        self.namespace='"'+namespace+'"'
        self.pod='"'+container+'"'

    def cpu(self):
        query='sum by (container_label_io_kubernetes_pod_name)' \
              ' (rate(container_cpu_usage_seconds_total{{ image!="", container_label_io_kubernetes_pod_namespace=~{},  container_label_io_kubernetes_pod_name=~{} }}[20s]))'.format(self.namespace,self.pod)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        return float(results[0]['value'][1])

    def memory(self):
        query='container_memory_working_set_bytes{{ container_label_io_kubernetes_pod_namespace={},' \
              'container_label_io_kubernetes_pod_name={} }} / (1024^2)'.format(self.namespace,self.pod)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        return float(results[0]['value'][1])

    def disk(self):
        '''query='node_filesystem_size_bytes{{ instance={},job={},device!~"rootfs",mountpoint="/data" }} / (1024^3)'.format(self.instance,self.job)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']
        return float(results[0]['value'][1])'''
        return 0

    def network(self):
        query='(sum by (container_label_io_kubernetes_pod_name) (rate(container_network_transmit_bytes_total{{ container_label_io_kubernetes_pod_name=~{},interface=~"eth0|ens.*" }}[20s]))' \
              '+ sum by (container_label_io_kubernetes_pod_name) (rate(container_network_receive_bytes_total{{ container_label_io_kubernetes_pod_name=~{},interface=~"eth0|ens.*" }}[20s]))) ' \
              ' * 8 / (10^6)'.format(self.pod,self.pod)
        #print(query)
        response = requests.get(self.prometheus + '/api/v1/query', params={
            'query': query})
        #print(response.json())
        results = response.json()['data']['result']

        return float(results[0]['value'][1])

    def cpu_memory_disk_network(self):
        result=(self.cpu(),self.memory(),self.disk(),self.network())
        return result