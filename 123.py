import pandas as pd

file_path='http://192.168.220.132:9000/networkauto/123.xlsx'

df=pd.read_excel(file_path)
print(df.head())