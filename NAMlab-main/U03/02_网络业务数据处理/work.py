import json
import pandas as pd

# json_to_excel: 将导入的JSON文件转换为Excel表格
'''
[Params]
file_path(str): JSON文件的路径
col_names(list): 生成的Excel表格的列头名称
excel_file(str): 生成的Excel表格文件的路径
'''
def json_to_excel(file_path,col_names,excel_file):
    # 导入JSON文件
    with open(file_path) as f:
        json_data = json.load(f)
       # print(json_data)
    data_list = [] #一级列表
    result_dict={}
    ## Task1.按照每个工单数据来取需要的数值
    for cmd in json_data['datas']:
        t_id =cmd['id']
        c_time =cmd['created_time']['display_value']
        pri =cmd['priority']['name']
        site = cmd["site"]["name"]
        status = cmd["status"]["name"]
        data_list.append([t_id, c_time, pri, site, status])
       

    ## Task2.通过Pandas的DataFrame输出Excel文件
    pd_data = pd.DataFrame(data_list, columns=col_names)
    pd_data.to_excel(excel_file, index=False)




if __name__ == "__main__":
    tt=['ID', '创建时间', '优先级', '站点', '状态']
    json_to_excel('D:/python自动化+AI/2.0/NAMlab-main/U03/02_网络业务数据处理/network_tech.json',tt,'123.xlsx')
    ## Task3.设定列头名称并执行函数