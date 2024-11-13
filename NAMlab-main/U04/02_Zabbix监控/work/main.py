from zabbix import Zabbix

# 这里修改为你的Zabbix Url 和 API Token
url = "http://10.10.100.20:3031/"
api_token = "3bd58993148a529c1264f2e0d21bc7d4120debf7f4226115f62cc7234c7abb79"
zabbix_inst = Zabbix(url, api_token)
print(zabbix_inst.inventory)
for host_name in [ 'huawei','huawei2']:
    zabbix_inst.collector_host(host_name, prepare=True)
