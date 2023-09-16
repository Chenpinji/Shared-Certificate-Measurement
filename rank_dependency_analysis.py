import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt

csvpath = "../alexa-top-1m/csv/1m.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]
# print(len(domain))
domain2rank = {}
#建立域名与排名的映射
for i in range(1, len(domain) + 1):
    domain2rank[domain[i-1]] = i
cnt = 0
d1_100 = 0
d100_1000 = 0
d1000_10000 = 0
d10000_1000000 = 0
out1M = 0# if "google2.com" in domain2rank:
#     print("A")
file_path = 'rank_dependency.json'
with open(file_path, 'w') as wfile:
    with open('domain_in_ca_CN_SAN.json', 'r') as file:
        for line in file:
            json_object = json.loads(line)
            # valid_domain_in_ca_cnt": 2, "have_apex_domain_cnt
            # a = json_object['valid_sub_domain_cnt']
            a = json_object['domain_in_ca_data']
            b = json_object['domain']
            flag = 0
            data = {}
            data["domain"] = b
            out1w = []
            out1m = []
            for keys in a:
                # cnt += 1
                if keys in domain2rank and a[keys]["have apex domain"] == True:
                    if domain2rank[keys] <= 100:
                        d1_100 += 1                
                    elif domain2rank[keys] <=1000:
                        d100_1000+=1
                    elif domain2rank[keys] <=10000:
                        d1000_10000 += 1
                    else:
                        d10000_1000000 += 1
                        out1w.append(keys)
                        # flag = 1
                elif a[keys]["have apex domain"] == True:
                    flag = 1
                    out1m.append(keys)
                    out1M += 1
            if flag:
                cnt+=1
            data["rely on out 1w domain"] = out1w
            data["rely on out 1m domain"] = out1m
            json.dump(data, wfile, indent = 4)  # 将 JSON 数据写入文件
            wfile.write('\n')

print(cnt)
print("1-100:", end = ' ')
print(d1_100)
print("100-1000:", end = ' ')
print(d100_1000)
print("1000-10000:", end = ' ')
print(d1000_10000)
print("10000-1000000:", end = ' ')
print(d10000_1000000)
print("out of 1M:", end = ' ')
print(out1M)