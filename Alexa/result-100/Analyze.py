import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt

percent = []
A = []
B = []
C = []
validcnt = 0
badcnt = 0
each = 0
with open('domain_in_ca_CN_SAN.json', 'r') as file:
    for line in file:
        json_object = json.loads(line)
        # valid_domain_in_ca_cnt": 2, "have_apex_domain_cnt
        # a = json_object['valid_sub_domain_cnt']
        a = json_object['valid_domain_in_ca_cnt']
        b = json_object['have_apex_domain_cnt']
        # c = json_object['have_each_other_cnt']
        validcnt += a
        badcnt += b
        # each += c 
        if a == 0:
            percent.append(0)
            A.append(0)
            B.append(0)
            # C.append(0)
        else:
            A.append(a)
            B.append(b)
            # C.append(c)
            percent.append(b / a)
print("Domain in the SAN of AlexaTop 1K which has valid CA:" + str(validcnt))
print("Domain in the SAN of AlexaTop 1K whose valid CA has apex domain:" + str(badcnt))
# print("Domain in the SAN of AlexaTop 1K whose valid CA has apex domain and apex domain has it:" + str(each))
x = list(range(1, 101))

plt.bar(x,A[0:100],lw=0.5,fc="r",label="Valid Domain")
plt.bar(x,B[0:100],lw=0.5,fc="b",label="Potential Malicious Domain")
# plt.bar(x,C[0:100],lw=0.5,fc="g",label="More Malicious Domain")
plt.legend()
plt.savefig('domain-in-ca-100.png')
# plt.show()
