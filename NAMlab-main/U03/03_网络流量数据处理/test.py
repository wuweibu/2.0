import pandas as pd  


data = {'r_asn': ['A', 'B', 'A', 'C', 'B', 'D', 'A']}  
df = pd.DataFrame(data)  

value_counts = df.r_asn.value_counts()  
#print(value_counts)
frequent_values=[]
for one in value_counts[value_counts > 1]:
    frequent_values.append(one)
  
# 输出结果  
#print(frequent_values)


abc= [one for one in df.r_asn.value_counts() if one > 1]
print(abc)