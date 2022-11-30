import yaml
import requests

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

prometheus = "http://" + config['prometheus_source'] + "/"

def get_all_machine_id():
    query = 'group by (instance) (node_load5!=0)'
    # print(query)
    response = requests.get(prometheus + '/api/v1/query', params={
        'query': query})
    results = response.json()['data']['result']
    machine_list=[]
    for i in results:
        machine_list.append(i['metric']['instance'])
    #print(machine_list)
    return machine_list

def get_all_app_list():
    query = ' (kube_pod_status_ready!=0)'
    # print(query)
    response = requests.get(prometheus + '/api/v1/query', params={
        'query': query})
    results = response.json()['data']['result']
    app_list=[]
    for i in results:
        app_list.append(i['metric']['pod'])
    return app_list
