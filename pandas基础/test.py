import pandas as pd

# 创建一个基本的 DataFrame
data = {
    'IP地址': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
    '响应时间(ms)': [10, 15, 7, 12],
    '品牌':['huawei','rj','ck','h3c']
}

df = pd.DataFrame(data)
print(df.values)
new_list=[]
for sub in df.values:
    new_list.append(list(sub))

print(new_list)

new_new_list=[]
for sub in new_list:
    for cmd in sub:
        new_new_list.append(cmd)

print(new_new_list)