import re
import time
import os
import requests
import ssl
import OpenSSL as openssl
import urllib.parse as up
import threading
import sys
import hashlib
import concurrent.futures
import dns.resolver
import socket
import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
socket.setdefaulttimeout(3)
usragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def check_tls(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443),timeout = 3) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                domainlist = []
                for i in cert['subjectAltName']:
                    domainlist.append(i[1])
                return (ssock.version()), domainlist
    except: 
        return ('error'), ('error')

csvpath = "../Tranco_Dataset/tranco-apex-1m.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]

csvpath2 = "../Tranco_Dataset/tranco-withsub-1m.csv"
with open(csvpath2) as f2:
    mill = f2.readlines()
domain_sub = [dd.split('\n')[0].split(',')[1] for dd in mill]
#建立域名与排名的映射
domain2rank = {}
for i in range(1, len(domain) + 1):
    domain2rank[domain[i-1]] = i

domain2rank_sub = {}
for i in range(1, len(domain_sub) + 1):
    domain2rank_sub[domain_sub[i-1]] = i
cnt = 0
d1_100 = 0
d100_1000 = 0
d1000_10000 = 0
d10000_1000000 = 0
out1M = 0

cnt_sub = 0
d1_100_sub = 0
d100_1000_sub = 0
d1000_10000_sub = 0
d10000_1000000_sub = 0
out1M_sub = 0


file_path = 'rank_dependency_Apex.json'
file_path2 = 'rank_dependency_Withsub.json'
with open(file_path, 'w') as wfile:
    with open(file_path2,'w') as wfile_sub:
        with open('../Tranco1W_relate_domain/relate_dom_tranco1w.json', 'r') as file:
            for line in tqdm(file):
                data = {}
                data_sub = {}
                json_object = json.loads(line)
                domain = json_object['domain']
                relate_list = json_object['relate domain']
                rank = json_object['rank']
                data['domain'] = domain
                data_sub['domain'] = domain
                data['rank'] = rank
                data_sub['rank'] = rank
                out1w = []
                out1m = []
                in100 = []
                in1000 = []
                in1w = []
                validcnt = 0
                out1w_sub = []
                out1m_sub = []
                in100_sub = []
                in1000_sub = []
                in1w_sub = []
                validcnt_sub = 0
                print(domain, end = ' ')
                print(rank)
                for relate_domain in  relate_list:
                    #see whether relate_domain contain apex domain
                    tlsver, cert = check_tls(relate_domain)
                    if tlsver == "error":
                        continue
                    validcnt += 1
                    validcnt_sub += 1
                    d1 = '*.' + domain
                    d2 = 'www.' + domain 
                    if domain in cert or d1 in cert or d2 in cert:
                        if relate_domain in domain2rank:
                            if domain2rank[relate_domain] <= 100:
                                d1_100 += 1    
                                in100.append(relate_domain)            
                            elif domain2rank[relate_domain] <=1000:
                                d100_1000+=1
                                in1000.append(relate_domain)
                            elif domain2rank[relate_domain] <=10000:
                                d1000_10000 += 1
                                in1w.append(relate_domain)
                            else:
                                d10000_1000000 += 1
                                out1w.append(relate_domain)
                        else:
                            out1m.append(relate_domain)
                            out1M += 1
                        if relate_domain in domain2rank_sub:
                            if domain2rank_sub[relate_domain] <= 100:
                                d1_100_sub += 1    
                                in100_sub.append(relate_domain)            
                            elif domain2rank_sub[relate_domain] <=1000:
                                d100_1000_sub+=1
                                in1000_sub.append(relate_domain)
                            elif domain2rank_sub[relate_domain] <=10000:
                                d1000_10000_sub += 1
                                in1w_sub.append(relate_domain)
                            else:
                                d10000_1000000_sub += 1
                                out1w_sub.append(relate_domain)
                        else:
                            out1m_sub.append(relate_domain)
                            out1M_sub += 1
                data['valid domain cnt'] = validcnt
                data['rely on top 100'] = in100
                data['rely on top 1000'] = in1000
                data['rely on top 1w'] = in1w
                data['rely on out 1w'] = out1w
                data['out1w cnt'] = len(out1w)
                data['rely on out 1m'] = out1m
                data['out1m cnt'] = len(out1m)
                data_sub['valid domain cnt'] = validcnt_sub
                data_sub['rely on top 100'] = in100_sub
                data_sub['rely on top 1000'] = in1000_sub
                data_sub['rely on top 1w'] = in1w_sub
                data_sub['rely on out 1w'] = out1w_sub
                data_sub['out1w cnt'] = len(out1w_sub)
                data_sub['rely on out 1m'] = out1m_sub
                data_sub['out1m cnt'] = len(out1m_sub)
                if len(out1m) > 0:
                    cnt += 1
                if len(out1m_sub) > 0:
                    cnt_sub += 1
                json.dump(data, wfile)  # 将 JSON 数据写入文件
                json.dump(data_sub, wfile_sub)
                wfile.write('\n')
                wfile_sub.write('\n')

with open('summary.txt', 'w') as file:
    file.write("Tranco百万以外影响顶级网站数量: " + str(cnt) + '\n')
    file.write("Tranco(withsub)百万以外影响顶级网站数量: " + str(cnt_sub) + '\n')
    file.write("1-100: " + str(d1_100) + " | " + str(d1_100_sub) + '\n')
    file.write("100-1000: " + str(d100_1000) + " | " + str(d100_1000_sub) + '\n')
    file.write("1000-10000: " + str(d1000_10000) + " | " + str(d1000_10000_sub) + '\n')
    file.write("10000-1000000: " + str(d10000_1000000) + " | " + str(d10000_1000000_sub) + '\n')
    file.write("out of 1M: " + str(out1M) + " | " + str(out1M_sub) + '\n')
# print("Tranco百万以外影响顶级网站数量: ", end =' ')
# print(cnt)
# print("Tranco(withsub)百万以外影响顶级网站数量: ", end =' ')
# print(cnt_sub)
# print("1-100:", end = ' ')
# print(d1_100, end = ' | ')
# print(d1_100_sub)
# print("100-1000:", end = ' ')
# print(d100_1000,end=' | ')
# print(d100_1000_sub)
# print("1000-10000:", end = ' ')
# print(d1000_10000,end=' | ')
# print(d1000_10000_sub)
# print("10000-1000000:", end = ' ')
# print(d10000_1000000,end=' | ')
# print(d10000_1000000_sub)
# print("out of 1M:", end = ' ')
# print(out1M,end = ' | ')
# print(out1M_sub)
