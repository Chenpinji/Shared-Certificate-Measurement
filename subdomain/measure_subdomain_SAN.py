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
import csv
from tqdm import tqdm
import json
socket.setdefaulttimeout(3)
# socks.set_default_proxy(socks.SOCKS5, "localhost", 7890)
# socket.socket = socks.socksocket

def check_tls(domain):
	context = ssl.create_default_context()
	try:
		with socket.create_connection((domain, 443),timeout = 3) as sock:
			with context.wrap_socket(sock, server_hostname=domain) as ssock:
				return (ssock.version()), ssock.getpeercert()
	except: 
		return ('error'), ('error')
# data[domain]['Sub_domain']
csvpath = "../alexa-top-1m/csv/1000.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]
with open('ALexa_Sub_domain.json', 'r') as json_file:
    data = json.load(json_file)
with open('Alexa_CN_SAN.json','r') as j_file:
    cadata = json.load(j_file)
file_path = 'Sub_domain_CN_SAN_498-1000.json'
with open(file_path, 'w') as file:
    for i in tqdm(domain[498:1000]):
        # print(i)
        outdata = {}
        outdata['domain'] = i
        outdata['sub_domain_data'] = {}
        haveapexcnt = 0
        haveEachOther = 0
        # print(data[i]['Sub_domain'])
        for subdomain in data[i]['Sub_domain']:
            tls_ver, cert_info = check_tls(subdomain)
            if tls_ver != "error":
                outdata['sub_domain_data'][subdomain] = {}
                for k in cert_info['subject']:
                    if(k[0][0] == "commonName"):
                        outdata['sub_domain_data'][subdomain]['CN'] = k[0][1]
                # subSAN = []
                outdata['sub_domain_data'][subdomain]['have apex domain'] = False
                outdata['sub_domain_data'][subdomain]['have each other'] = False
                for k in cert_info['subjectAltName']:
                    if k[1] == i:
                        outdata['sub_domain_data'][subdomain]['have apex domain'] = True
                    # subSAN.append(k[1])
                if outdata['sub_domain_data'][subdomain]['have apex domain'] == True:
                    haveapexcnt += 1
                    temp = subdomain.split('.')
                    wildcard = "*"
                    for st in range(1,len(temp)):
                        wildcard += "." 
                        wildcard += temp[st]
                    # print(wildcard)
                    if cadata[i]['TLS'] != "error" and (subdomain in cadata[i]['SAN'] or wildcard in cadata[i]['SAN']):
                        haveEachOther += 1
                        outdata['sub_domain_data'][subdomain]['have each other'] = True
                # outdata['sub_domain_data'][subdomain]['SAN'] = subSAN
        outdata['valid_sub_domain_cnt'] = len(outdata['sub_domain_data'])
        outdata['have_apex_domain_cnt'] = haveapexcnt
        outdata['have_each_other_cnt'] = haveEachOther
        json.dump(outdata, file, indent = 4)  # 将 JSON 数据写入文件
        file.write('\n')

# def tfunc(kk):
#     with open(csv_filename, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         # for dom in mill[kk*1:(kk+1)*1]:
#         for j in tqdm(range(kk * 1000,(kk+1) * 1000)):
#             dom = mill[j]
#             tls_ver, cert_info = check_tls(dom)
#             data = []
#             rank = j+1
#             data.append(rank)
#             data.append(dom)
#             if(tls_ver == "error"):
#                 data.append("error")
#                 insertrow.append(data)
#                 # writer.writerows(insertrow)
#                 continue
#             data.append(tls_ver)
#             flag = 0
#             for i in cert_info['subject']:
#                 if(i[0][0] == "countryName"):
#                     data.append(i[0][1])
#                     flag = 1
#                 if(i[0][0] == "commonName"):
#                     if flag == 0:
#                         data.append("none")
#                     data.append(i[0][1])
#             for i in cert_info['subjectAltName']:
#                 data.append(i[1])
#             insertrow.append(data)
#         writer.writerows(insertrow)

# threads = []
# for i in range(1):
#     thread = threading.Thread(target=tfunc, args=(i,))
#     threads.append(thread)
#     thread.start()

# for t in threads:
#     t.join()