import json
import matplotlib.pyplot as plt
with open('rank_dependency_Withsub.json', 'r') as file:
    subcnt = 0
    othercnt = 0
    cnt = []
    for line in file:
        json_object = json.loads(line)
        apex = json_object['domain']
        cmplist = json_object['rely on top 100'] + json_object['rely on top 1000'] + json_object['rely on top 1w'] + json_object['rely on out 1w'] + json_object['rely on out 1m']
        cnt.append(len(cmplist))
    x = []
    for i in range(1,1001):
        x.append(i)
    plt.plot(x,cnt)
    plt.savefig('1.png')
    #     for each in cmplist:
    #         name = each.split('.')
    #         length = len(name)
    #         if name[length-2] + '.' + name[length-1] == apex:
    #             subcnt += 1
    #         else:
    #             othercnt += 1
    #     # cnt += json_object['cnt']
    # print(cnt)
    # print(subcnt)
    # print(othercnt)
