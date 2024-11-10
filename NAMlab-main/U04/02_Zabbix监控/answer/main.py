import time
from utils import DataWriter
from zabbix import Zabbix

# 这里修改为你的Zabbix Url 和 API Token          连接Zabbix
url = "http://10.10.100.20:3031/"
api_token = "3bd58993148a529c1264f2e0d21bc7d4120debf7f4226115f62cc7234c7abb79"
zabbix_inst = Zabbix(url, api_token)

print(zabbix_inst.inventory)

db = DataWriter()

metrics = {'huawei': ["47190", "47191", "47192"]}

def proc_restime(restime):
    return restime * 1000.

while True:
    for host_name in ['huawei']:
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






