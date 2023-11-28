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
with open('Alexa_CN_SAN.json','r') as j_file:
    cadata = json.load(j_file)
file_path = 'domain_in_ca_SAN.json'
with open(file_path, 'w') as file:
    for i in tqdm(domain):
        outdata = {}
        outdata['domain'] = i
        outdata['domain_in_ca_data'] = {}
        haveapexcnt = 0
        # haveEachOther = 0
        # print(data[i]['Sub_domain'])
        if cadata[i]['TLS'] != "error":
            for subdomain in cadata[i]['SAN']:
                tls_ver, cert_info = check_tls(subdomain)
                if tls_ver != "error":
                    outdata['domain_in_ca_data'][subdomain] = {}
                    for k in cert_info['subject']:
                        if(k[0][0] == "commonName"):
                            outdata['domain_in_ca_data'][subdomain]['CN'] = k[0][1]
                    # subSAN = []
                    outdata['domain_in_ca_data'][subdomain]['have apex domain'] = False
                    # outdata['domain_in_ca_data'][subdomain]['have each other'] = False
                    for k in cert_info['subjectAltName']:
                        if k[1] == i:
                            outdata['domain_in_ca_data'][subdomain]['have apex domain'] = True
                        # subSAN.append(k[1])
                    if outdata['domain_in_ca_data'][subdomain]['have apex domain'] == True:
                        haveapexcnt += 1
                        # temp = subdomain.split('.')
                        # wildcard = "*"
                        # for st in range(1,len(temp)):
                        #     wildcard += "." 
                        #     wildcard += temp[st]
                        # # print(wildcard)
                        # if cadata[i]['TLS'] != "error" and (subdomain in cadata[i]['SAN'] or wildcard in cadata[i]['SAN']):
                        #     haveEachOther += 1
                        #     outdata['domain_in_ca_data'][subdomain]['have each other'] = True
                # outdata['sub_domain_data'][subdomain]['SAN'] = subSAN
        outdata['valid_domain_in_ca_cnt'] = len(outdata['domain_in_ca_data'])
        outdata['have_apex_domain_cnt'] = haveapexcnt
        # outdata['have_each_other_cnt'] = haveEachOther
        json.dump(outdata, file, indent = 4)  
        file.write('\n')
