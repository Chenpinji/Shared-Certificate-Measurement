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

csvpath = "../alexa-top-1m/csv/1m.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]
#建立域名与排名的映射
domain2rank = {}
for i in range(1, len(domain) + 1):
    domain2rank[domain[i-1]] = i
cnt = 0
d1_100 = 0
d100_1000 = 0
d1000_10000 = 0
d10000_1000000 = 0
out1M = 0
file_path = 'rank_dependency_new.json'
with open(file_path, 'w') as wfile:
    with open('relate_dom_Alexa1K.json', 'r') as file:
        for line in tqdm(file):
            data = {}
            json_object = json.loads(line)
            domain = json_object['domain']
            relate_list = json_object['relate domain']
            rank = json_object['rank']
            data = {}
            data['domain'] = domain
            data['rank'] = rank
            out1w = []
            out1m = []
            validcnt = 0
            print(domain, end = ' ')
            print(rank)
            for relate_domain in  relate_list:
                #see whether relate_domain contain apex domain
                tlsver, cert = check_tls(relate_domain)
                if tlsver == "error":
                    continue
                validcnt += 1
                d1 = '*.' + domain
                d2 = 'www.' + domain 
                if domain in cert or d1 in cert or d2 in cert:
                    if relate_domain in domain2rank:
                        if domain2rank[relate_domain] <= 100:
                            d1_100 += 1                
                        elif domain2rank[relate_domain] <=1000:
                            d100_1000+=1
                        elif domain2rank[relate_domain] <=10000:
                            d1000_10000 += 1
                        else:
                            d10000_1000000 += 1
                            out1w.append(relate_domain)
                    else:
                        out1m.append(relate_domain)
                        out1M += 1
            data['valid domain cnt'] = validcnt
            data['rely on out 1w'] = out1w
            data['out1w cnt'] = len(out1w)
            data['rely on out 1m'] = out1m
            data['out1m cnt'] = len(out1m)
            if len(out1m) > 0:
                cnt += 1
            json.dump(data, wfile)  # 将 JSON 数据写入文件
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
