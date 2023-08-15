import json
from tqdm import tqdm
import csv

with open('Sub_domain_CN_SAN_0-67.json', 'r') as file1:
    json_objects = []
    current_json = ""
    cnt = 0
    for line in file1:
        if line != '}\n' and line:  # 如果该行不为空
            line = line.strip()
            current_json += line
        else:
            current_json += '}'
            if current_json:  # 如果当前 JSON 非空
                json_objects.append(json.loads(current_json))
                current_json = ""  # 重置当前 JSON 字符串
    if current_json:  # 处理最后一个 JSON 对象
        json_objects.append(json.loads(current_json))

with open('Sub_domain_CN_SAN_68-500.json', 'r') as file2:
    json_objects2 = []
    current_json = ""
    # cnt = 0
    for line in file2:
        if line != '}\n' and line:  # 如果该行不为空
            line = line.strip()
            current_json += line
        else:
            current_json += '}'
            if current_json:  # 如果当前 JSON 非空
                json_objects2.append(json.loads(current_json))
                current_json = ""  # 重置当前 JSON 字符串
    if current_json:  # 处理最后一个 JSON 对象
        json_objects2.append(json.loads(current_json))

with open('Sub_domain_CN_SAN_498-1000.json', 'r') as file3:
    json_objects3 = []
    current_json = ""
    # cnt = 0
    for line in file3:
        if line != '}\n' and line:  # 如果该行不为空
            line = line.strip()
            current_json += line
        else:
            current_json += '}'
            if current_json:  # 如果当前 JSON 非空
                json_objects3.append(json.loads(current_json))
                current_json = ""  # 重置当前 JSON 字符串
    if current_json:  # 处理最后一个 JSON 对象
        json_objects3.append(json.loads(current_json))

file_path = 'Subdomain_in_ca_SAN.json'
with open(file_path, 'w') as file:
    for record in tqdm(json_objects):
        data = {}
        data['domain'] = record['domain']
        data['sub_domain_data'] = record['sub_domain_data']
        for key in data['sub_domain_data']:
            del data['sub_domain_data'][key]['SAN']
        data['valid_sub_domain_cnt'] = record['valid_sub_domain_cnt']
        data['have_apex_domain_cnt'] = record['have_apex_domain_cnt']
        data['have_each_other_cnt'] = record['have_each_other_cnt']
        json.dump(data, file)  # 将 JSON 数据写入文件
        file.write('\n')
        # break
    for record in tqdm(json_objects2):
        data = {}
        data['domain'] = record['domain']
        data['sub_domain_data'] = record['sub_domain_data']
        # for key in data['sub_domain_data']:
        #     del data['sub_domain_data'][key]['SAN']
        data['valid_sub_domain_cnt'] = record['valid_sub_domain_cnt']
        data['have_apex_domain_cnt'] = record['have_apex_domain_cnt']
        data['have_each_other_cnt'] = record['have_each_other_cnt']
        json.dump(data, file)  # 将 JSON 数据写入文件
        file.write('\n')

    for record in tqdm(json_objects3):
        data = {}
        data['domain'] = record['domain']
        data['sub_domain_data'] = record['sub_domain_data']
        # for key in data['sub_domain_data']:
        #     del data['sub_domain_data'][key]['SAN']
        data['valid_sub_domain_cnt'] = record['valid_sub_domain_cnt']
        data['have_apex_domain_cnt'] = record['have_apex_domain_cnt']
        data['have_each_other_cnt'] = record['have_each_other_cnt']
        json.dump(data, file)  # 将 JSON 数据写入文件
        file.write('\n')

# with open('Alexa_Sub_domain_http-response.json', 'r') as file2:
#     json_objects = file.readlines()
