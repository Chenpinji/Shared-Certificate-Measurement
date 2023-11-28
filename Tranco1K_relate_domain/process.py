import json
from tqdm import tqdm
with open("relate_dom_tranco1w.json", 'r') as file:
    # with open("relate_dom_tranco1w.json", 'w') as wfile:
    subcnt = 0
    othercnt = 0
    for line in file:
        json_object = json.loads(line)
        apex = json_object['domain']
        for each in json_object['relate domain']:
            name = each.split('.')
            length = len(name)
            if name[length-2] + '.' + name[length-1] == apex:
                subcnt += 1
            else:
                othercnt += 1
        # cnt += json_object['cnt']
    print(subcnt)
    print(othercnt) 
        # w_object = {}
        # w_object['domain'] = json_object['domain']
        # w_object['rank'] = json_object['rank']
        # relatelist = []
        # for domain in json_object['relate domain']:
        #     if domain[0] != '*' and domain not in relatelist:
        #         relatelist.append(domain)
        # w_object['relate domain'] = relatelist
        # w_object['cnt'] = len(relatelist)
            
