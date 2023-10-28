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

csvpath = "../alexa-top-1m/csv/1m.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]
#建立域名与排名的映射
domain2rank = {}
for i in range(1, len(domain) + 1):
    domain2rank[domain[i-1]] = i

trancopath = "../tranco-top-1m/tranco.csv"
with open(trancopath) as f2:
    mill2 = f2.readlines()
trancodomain = [dd.split('\n')[0].split(',')[1] for dd in mill2]
trancodomain2rank = {}
for i in range(1, len(trancodomain) + 1):
    trancodomain2rank[trancodomain[i-1]] = i

#这个测量是因为Alexa只有顶级域名，但对子域名则没有排名，因此我们针对子域名增加两种排名方式
# 1. 子域名只取二级域名部分，看排名
# 2. 子域名查tranco1M（包含子域名）
#<--- method1 ---> only see subdomain
# file_path = 'rank_dep_onlyApex.json'
# with open(file_path, 'w') as wfile:
#     with open('rank_dependency_new.json', 'r') as file:
#         for line in tqdm(file):
#             data = {}
#             json_object = json.loads(line)
#             data['domain'] = json_object['domain']
#             data['rank'] = json_object['rank']
#             out1m = json_object['rely on out 1m']
#             data['rely on out 1w'] = json_object['rely on out 1w']
#             rely1m = []
#             for domain in out1m:
#                 name = domain.split('.')
#                 if len(name) <= 2:
#                     rely1m.append(domain)
#                 else:
#                     apex = name[-2] + '.' + name[-1]
#                     if apex in domain2rank:
#                         if domain2rank[apex] > 10000:
#                             data['rely on out 1w'].append(domain)
#                     else:
#                         rely1m.append(domain)
#             data['rely on out 1m cnt'] = len(rely1m)
#             data['rely on out 1m'] = rely1m
#             json.dump(data, wfile)  # 将 JSON 数据写入文件
#             wfile.write('\n')
#<--- method2 ---> see tranco domain
file_path = 'rank_dep_tranco.json'
with open(file_path, 'w') as wfile:
    with open('rank_dependency_new.json', 'r') as file:
        for line in tqdm(file):
            data = {}
            json_object = json.loads(line)
            data['domain'] = json_object['domain']
            data['rank'] = json_object['rank']
            out1m = json_object['rely on out 1m']
            out1w = json_object['rely on out 1w']
            rely1m = []
            rely1w = []
            for domain in out1m:
                if domain in trancodomain2rank:
                    if trancodomain2rank[domain] > 10000:
                        rely1w.append(domain)
                else:
                    rely1m.append(domain)
            data['rely on out 1w cnt'] = len(rely1w)
            data['rely on out 1w'] = rely1w
            data['rely on out 1m cnt'] = len(rely1m)
            data['rely on out 1m'] = rely1m
            json.dump(data, wfile)  # 将 JSON 数据写入文件
            wfile.write('\n')