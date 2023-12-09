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
import re
from dns import resolver, rdatatype
import concurrent.futures
socket.setdefaulttimeout(3)
usragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    if sys.platform.startswith('win'):
        try:
            import win_unicode_console , colorama
            win_unicode_console.enable()
            colorama.init()
        except:
            HEADER = OKBLUE = OKGREEN = WARNING = FAIL = ENDC = ''
def check_tls(domain):
	context = ssl.create_default_context()
	try:
		with socket.create_connection((domain, 443),timeout = 3) as sock:
			with context.wrap_socket(sock, server_hostname=domain) as ssock:
				return (ssock.version()), ssock.getpeercert()
	except: 
		return ('error'), ('error')
def sereq(url):
    resp = requests.get(url, headers={'User-Agent': usragent, 'Connection': 'Close'}, timeout=30)
    resp.encoding = 'utf-8'
    return resp

def crtsh_enum(domain):
    # certificate logs search crt.sh
    subdomains = []
    start = time.time()
    try:
        r = requests.get("https://crt.sh/?q=" + domain, headers={'User-Agent': usragent, 'Connection': 'Close'}, timeout=30)
        r.encoding = 'utf-8'
        # print(r.text)
        for dom in re.findall("<BR>([^ \.]+\." + re.escape(domain) + ")", r.text):
            subdomains.append(dom)
        subdomains = list(set(subdomains))
        if len(subdomains) == 0 and "Too Many Requests" in r.text:
            print("Too Many Requests for CRT.SH")
        print(bcolors.FAIL + "Cert log from crt.sh for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
        # print(subdomains)
    except requests.exceptions.Timeout:
        print(bcolors.WARNING + "CRT.SH timeout for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    except:
        print(bcolors.WARNING + "Unknown error in crt.sh for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    return subdomains

def virustotal_enum(domain):
    # virus total enumeration
    subdomains = []
    start = time.time()
    try:
        r = requests.get(url = "https://www.virustotal.com/ui/domains/{0}/subdomains?limit=40".format(domain), headers={'Connection': 'Close'}, timeout=20)
        for i, entry in enumerate(r.json()['data']):
            subdomains.append(entry['id'])
        subdomains = list(set(subdomains))
        print(bcolors.FAIL + "Virustotal for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
    except requests.exceptions.Timeout:
        print(bcolors.WARNING + "Virustotal timeout for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    except:
        print(bcolors.WARNING + "Unknown error in virustotal for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    return subdomains

def threatcrowd_enum(domain):
    # threat crowd enumeration
    subdomains = []
    start = time.time()
    try:
        r = requests.get(url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={0}".format(domain), headers={'Connection': 'Close'}, timeout=20)
        for entry in r.json()['subdomains']:
            subdomains.append(entry)
        subdomains = list(set(subdomains))
        print(bcolors.FAIL + "ThreatCrowd for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
    except requests.exceptions.Timeout:
        print(bcolors.WARNING + "ThreatCrowd timeout for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    except:
        print(bcolors.WARNING + "Unknown error in ThreatCrowd for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    return subdomains

def contentdict_enum(domain):
    # direct directory dictionary from web page
    subdomains = []
    start = time.time()
    try:
        session = requests.Session()
        session.headers = {'User-Agent': usragent, 'Connection': 'Close'}
        r = session.get("http://" + domain, timeout=20)
        session.close()
        r.encoding = 'utf-8'
        aa = list(set(re.findall("htt.{2,20}" + domain, r.text)))
        if not len(aa) == 0:
            x = [up.unquote(i).split("//")[1] for i in aa if "//" in up.unquote(i)]
            y = list(set(x))
            for jj in y:
                try:
                    r = session.get("http://" + jj, timeout=3)
                    session.close()
                    r.encoding = 'utf-8'
                except:
                    continue
                bb = list(set(re.findall("htt.{2,20}" + domain, r.text)))
                if not len(bb) == 0:
                    x += [up.unquote(i).split("//")[1] for i in bb if "//" in up.unquote(i)]
            subdomains = list(set(subdomains + x))
        print(bcolors.FAIL + "Content dictionary level 2 BFS for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
    except requests.exceptions.ConnectionError:
        print(bcolors.WARNING + "Webpage Dcitionary Connection Error for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    except:
        print(bcolors.WARNING + "Unknown error in webpage dictionary for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    return subdomains

def san_enum(domain):
    # subject alternate name in x.509 certs
    subdomains = []
    a,b = check_tls(domain)
    if a != 'error':
        for i in b['subjectAltName']:
            subdomains.append(i[1])
    return subdomains

def se_enum(domain):
    # search engine result - Yahoo and Netcraft
    subdomains = []
    start = time.time()
    try:
        x1 = []
        r1 = requests.get(url = "https://search.yahoo.com/search?p=site%3A{0}".format(domain), headers={'User-Agent': usragent, 'Connection': 'Close'}, timeout=30)
        r1.encoding = 'utf-8'
        x1 += re.findall('http.{3,15}\.' + re.escape(domain), r1.text)
        if not len(x1) == 0:
            limpage = (re.findall('<span>.{2,20} results<', r1.text)[0]).split(' results')[0].split('<span>')[1]
        else:
            limpage = '10'
        limpage = min(200, int(limpage.replace(',', '')))
        urls = ["https://search.yahoo.com/search?p=site%3A{0}&b={1}".format(domain, pages) for pages in range(10, limpage, 10)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=limpage//10) as pool:
            responses = pool.map(sereq, urls)
        for rr in responses:
            x1 += re.findall('http.{3,15}\.' + re.escape(domain), rr.text)

        link = "https://searchdns.netcraft.com/?restriction=site+contains&host={0}".format(domain)
        x2 = []
        cookies = {}
        r3 = requests.get(url = link, headers={'User-Agent': usragent, 'Connection': 'Close'}, timeout=(10, None), cookies=cookies)
        r3.encoding = 'utf-8'
        if 'set-cookie' in r3.headers:
            cook = r3.headers['set-cookie']
            cook_list = cook[0:cook.find(';')].split("=")
            cookies[cook_list[0]] = cook_list[1]
            cookies['netcraft_js_verification_response'] = hashlib.sha1(up.unquote(cook_list[1]).encode('utf-8')).hexdigest()
        while True:
            try:
                r3 = requests.get(url = link, headers={'User-Agent': usragent, 'Connection': 'Close'}, timeout=(10, None), cookies=cookies)
                r3.encoding = 'utf-8'
                x2 += re.findall('http.{3,15}\.' + re.escape(domain), r3.text)
                if 'Next Page' not in r3.text:
                    break
                text = re.findall('.a.+?..Next Page', r3.text)
                link = "https://searchdns.netcraft.com" + (text[0].split("href=\"")[1]).split("\">Next")[0]
            except requests.exceptions.Timeout:
                break
        x1 = list(set(x1 + x2))
        x1 = [up.unquote(i).split("//")[1] for i in x1 if "//" in up.unquote(i) and not "<" in up.unquote(i)]

        subdomains = list(set(x1))
        print(bcolors.FAIL + "SE result for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
    except requests.exceptions.Timeout:
        print(bcolors.WARNING + "SE result timeout for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    except:
        print(bcolors.WARNING + "Unknown error in se result for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
    return subdomains

def dnsmx_enum(domain):
    # DNS resolve in x.509 certs
    subdomains = []
    flag = True
    start = time.time()
    try:
        result = dns.resolver.query(domain, 'MX')
        for exdata in result:
            subdomains.append(exdata.exchange.to_text())
    except:
        print(bcolors.WARNING + "Unknown error in dns resolver for " + domain + " - ", "%.2f" %(time.time() - start), bcolors.ENDC)
        flag = False
    subdomains = list(set(subdomains))
    if flag:
    	print(bcolors.FAIL + "DNS MX Resolver for domain " + domain + " - ", "%.2f" %(time.time() - start), len(subdomains), bcolors.ENDC)
    return subdomains

def combined_enum(domain):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        crtsh_res = executor.submit(crtsh_enum, domain)
        # virustotal_res = executor.submit(virustotal_enum, domain)
        # threatcrowd_res = executor.submit(threatcrowd_enum, domain)
        contentdict_res = executor.submit(contentdict_enum, domain)
        # san_res = executor.submit(san_enum, domain)
        # se_res = executor.submit(se_enum, domain)
        # dnsmx_res = executor.submit(dnsmx_enum, domain)
        subdlist = [crtsh_res.result(), contentdict_res.result()]
    subd = []
    for res in subdlist:
        subd += res
    subd = list(set(subd))
    return subd

def is_valid_domain(domain):
    pattern = r'^([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, domain)
    return match is not None
def check_domain_exists(domain): 
    try:
        answers = resolver.query(domain)
        for answer in answers:
            if answer.rdtype == rdatatype.A or answer.rdtype == rdatatype.CNAME:
                return True
        return False
    except:
        return False
def pdns(domain):
    originlen = len(domain.split('.'))
    url = 'https://api.secrank.cn/dtree/' + domain
    headers = {
        'fdp-access': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'fdp-secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
    params = {
        'limit': 100
    }
    response = requests.get(url, headers=headers, params=params)
    datalist = []
    # 处理响应数据
    if response.status_code == 200:
        res = response.json()
        for jsondata in res['data']:
            domainname = jsondata['domain']
            if is_valid_domain(domainname) and len(domainname.split('.')) == originlen + 1 and jsondata['lastSeen'][0] == '2' and jsondata['lastSeen'][1] == '3' and jsondata['domain'][0]!='-' and jsondata['domain'][0]!='0' and check_domain_exists(domainname):
                datalist.append(domainname)
        # 处理返回的 JSON 数据
        # ...
    else:
        print('请求失败:', response.status_code)
    return datalist




# with open('ALexa_Sub_domain.json', 'r') as json_file:
#     subdomaindata = json.load(json_file)
with open('../Tranco_SAN/Tranco_CN_SAN_1w.json','r') as j_file:
    cadata = []
    tempdata=''
    for line in j_file:
        if line != "}\n":
            tempdata += line
        else:
            tempdata += line
            # print(tempdata)
            a = json.loads(tempdata)
            cadata.append(a)
            tempdata=''
file_path = 'relate_dom_Tranco1w.json'
rank = 0
# print(cadata[0])
with open(file_path, 'w') as file:
    for i in tqdm(cadata[0:1000]):
        domain = i['domain']
        rank += 1
        data = {}
        data['domain'] = domain
        data['rank'] = rank
        # relate_list = subdomaindata[i]['Sub_domain']
        relate_list = []
        if i['TLS'] != "error":
            san_list = i['SAN']
            for line in san_list:
                # if i in line and line[0] == '*':
                #     continue
                if line == domain:
                    continue
                if line[0] != '*' and line not in relate_list:
                    relate_list.append(line)
                else:
                    templist = combined_enum(line[2:])
                    for each in templist:
                        if each not in relate_list:
                            relate_list.append(each)
                    templist2 = pdns(line)
                    for each in templist2:
                        if each not in relate_list:
                            relate_list.append(each)
        wwwSAN = "www." + domain
        nouse, wwwSANlist = check_tls(wwwSAN)
        if nouse != 'error':
            for k in wwwSANlist['subjectAltName']:
                if k[1][0] == '*':
                    one = combined_enum(k[1][2:])
                    two = pdns(k[1][2:])
                    for e in one:
                        if e not in relate_list:
                            relate_list.append(e)
                    for e in two:
                        if e not in relate_list:
                            relate_list.append(e)
                elif k not in relate_list:
                    relate_list.append(k[1])
        data['relate domain'] = relate_list
        data['cnt'] = len(relate_list)
        json.dump(data, file)
        file.write('\n')

# b = san_enum("baidu.com")
# print(b)