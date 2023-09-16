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
import json
from tqdm import tqdm
socket.setdefaulttimeout(3)
# socks.set_default_proxy(socks.SOCKS5, "localhost", 7890)
# socket.socket = socks.socksocket
csvpath = "../alexa-top-1m/csv/10000.csv"
with open(csvpath) as f:
    mill = f.readlines()
mill = [dd.split('\n')[0].split(',')[1] for dd in mill] 

def check_tls(domain):
	context = ssl.create_default_context()
	try:
		with socket.create_connection((domain, 443),timeout = 3) as sock:
			with context.wrap_socket(sock, server_hostname=domain) as ssock:
				return (ssock.version()), ssock.getpeercert()
	except: 
		return ('error'), ('error')
a, b = check_tls("google.com")
print(b)
# csv_filename = "Alexa_CN_SAN_1w.json"
# def tfunc(kk):
#     with open(csv_filename, mode='w') as file:    
#         # for dom in mill[kk*1:(kk+1)*1]:
#         for j in tqdm(range(kk * 10000,(kk+1) * 10000)):
#             insertrow = {}
#             dom = mill[j]
#             insertrow["domain"] = dom
#             tls_ver, cert_info = check_tls(dom)
#             rank = j+1
#             insertrow["rank"] = rank
#             if(tls_ver == "error"):
#                 insertrow["TLS"] = "error"
#                 # writer.writerows(insertrow)
#                 continue
            
#             insertrow["TLS"] = tls_ver
#             flag = 0
#             for i in cert_info['subject']:
#                 if(i[0][0] == "countryName"):
#                     insertrow["country"] = i[0][1]
#                     flag = 1
#                 if(i[0][0] == "commonName"):
#                     if flag == 0:
#                         insertrow["country"] = "none"
#                     insertrow["CN"] = i[0][1]
#             SANlist = []
#             for i in cert_info['subjectAltName']:
#                 SANlist.append(i[1])
#             insertrow["SAN"] = SANlist
#             json.dump(insertrow, file, indent = 4) 
#             file.write('\n')
# threads = []
# for i in range(1):
#     thread = threading.Thread(target=tfunc, args=(i,))
#     threads.append(thread)
#     thread.start()

# for t in threads:
#     t.join()