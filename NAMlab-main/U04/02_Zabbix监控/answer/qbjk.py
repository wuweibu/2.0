import json
from pyzabbix.api import ZabbixAPI
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from utils import DataWriter


def __init__(self, zabbix_url, token):
    # Create ZabbixAPI class instance
    self.zapi = ZabbixAPI(server=zabbix_url)
    self.zapi.login(api_token=token)
    #获取正在监控的主机名和ID
    self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')}
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

def collector_host(self, device_name, prepare=False, metric_id_list=None):
    self.data[device_name] = {}
    host_id = self.inventory[device_name]    #获取这个主机ID
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
            item_id = info['itemid']
            item_name = metrics[item_id]
            item_lastvalue = round(float(info['lastvalue']), 8)
            self.data[device_name][item_name] = item_lastvalue


# 这里修改为你的Zabbix Url 和 API Token          连接Zabbix
url = "http://10.10.100.20:3031/"
api_token = "3bd58993148a529c1264f2e0d21bc7d4120debf7f4226115f62cc7234c7abb79"
zabbix_inst = Zabbix(url, api_token)

print(zabbix_inst.inventory)

db = DataWriter()

metrics = {'huawei': ["47190", "47191", "47192","47285"],
           'huawei2': ["47490", "47491", "47492","47582"]}

def proc_restime(restime):
    return restime * 1000.

while True:
    for host_name in ['huawei','huawei2']:
        zabbix_inst.collector_host(host_name, prepare=False, metric_id_list=metrics[host_name])

        for metric in zabbix_inst.data[host_name]:
            value = zabbix_inst.data[host_name][metric]
            if "ICMP response time" in metric:
                if value == zabbix_inst.old_data[host_name][metric]:
                    print('1')
                    continue
                value = proc_restime(value)
            db.write_ts_data('zabbix_'+host_name, [host_name+'_'+metric, value])
        print(zabbix_inst.data)

    zabbix_inst.old_data = zabbix_inst.data
    #print(zabbix_inst.data)
    zabbix_inst.data = {}
    time.sleep(5)


