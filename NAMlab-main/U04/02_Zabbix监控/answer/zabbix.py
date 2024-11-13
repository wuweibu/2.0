import json
from pyzabbix.api import ZabbixAPI

class Zabbix:
    def __init__(self, zabbix_url, token):
        # Create ZabbixAPI class instance
        self.zapi = ZabbixAPI(server=zabbix_url)     #zabbix的url IP地址加端口号
        self.zapi.login(api_token=token)            #zabbix的token 值
        self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')} #获取正在监控的主机名和ID
        self.data = {}
        self.old_data = {'huawei':
                         {'Huawei VRP: ICMP ping': '1',
                          'Huawei VRP: ICMP loss': '0',
                          'Huawei VRP: ICMP response time': '0.0',
                          'Interface GigabitEthernet1/0/0.505(HUAWEI, GigabitEthernet1/0/0.505 Interface): Inbound packets discarded':'0'},
                          'huawei2':
                         {'Huawei VRP: ICMP ping': '1',
                          'Huawei VRP: ICMP loss': '0',
                          'Huawei VRP: ICMP response time': '0.0',
                          'Interface GigabitEthernet1/0/0.505(HUAWEI, GigabitEthernet1/0/0.505 Interface): Inbound packets discarded':'0'}}


    def collector_host(self, device_name, prepare=True, metric_id_list=None):
        self.data[device_name] = {}
        host_id = self.inventory[device_name]    #在inventory里面 获取这个主机ID
        result = self.zapi.item.get(hostids=host_id)  #根据主机ID主机值获取所有监控指标
        metrics: dict = {info['itemid']: info['name'] for info in result}    #便利这个监控指标 形成字典metrics
        # 如果对监控指标不太了解，请将prepare在使用函数时定义为True
        if prepare:
            with open(device_name + '_CheckMe.txt', 'w') as f:
                json.dump(metrics, f, indent=4)
        else:
            #根据hostid获取对应的值
            item_list = self.zapi.item.get(hostids=host_id, itemids=metric_id_list) 
            for info in item_list:
                item_id = info['itemid']       #监控itemid
                item_name = metrics[item_id]   #监控指标名字
                item_lastvalue = round(float(info['lastvalue']), 8)      #当前能监控到的最后一个指标
                self.data[device_name][item_name] = item_lastvalue       #填值






