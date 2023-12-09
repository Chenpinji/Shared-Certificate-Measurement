import requests
import re
from dns import resolver, rdatatype
from tqdm import tqdm
csvpath = "../Tranco_Dataset/tranco-apex-1m.csv"
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
with open(csvpath) as f:
    mill = f.readlines()
mill = [dd.split('\n')[0].split(',')[1] for dd in mill] 
cnt = 0
for domain in tqdm(mill[1000:1010]): 
    url = 'https://api.secrank.cn/dtree/' + domain
    headers = {
        'fdp-access': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'fdp-secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
    params = {
        'limit': 500
    }

    response = requests.get(url, headers=headers, params=params)

    # 处理响应数据
    if response.status_code == 200:
        res = response.json()
        for jsondata in res['data']:
            if is_valid_domain(jsondata['domain']) and len(jsondata['domain'].split('.')) == 3 and jsondata['lastSeen'][0] == '2' and jsondata['lastSeen'][1] == '3' and jsondata['domain'][0]!='-' and jsondata['domain'][0]!='0' and check_domain_exists(jsondata['domain']):
                print(jsondata['domain'],end ='   ')
                print(jsondata['lastSeen'])
        # 处理返回的 JSON 数据
        # ...
    else:
        print('请求失败:', response.status_code)