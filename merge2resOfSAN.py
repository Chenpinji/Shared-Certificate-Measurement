import csv
import json
data = {}
with open("./Alexa_CN_SAN_1k.csv") as f1:
    record = f1.readlines()
# print(record[1])

with open("./Alexa_CN_SAN_1k_China.csv") as f2:
    Chinarecord = f2.readlines()

for i in range(len(record)):
    temp = record[i].split(',')
    temp2 = Chinarecord[i].split(',')
    rank = temp[0]
    domain = temp[1]
    data[domain] = {}
    data[domain]["rank"] = rank
    if(temp[2].strip('\n') == "error" and temp2[2] == "error"):
        data[domain]["TLS"] = "error"
        continue
    else:
        if temp[2].strip('\n') == "error":
            print("Chinarecord: " + temp2[2])
            data[domain]["TLS"] = temp2[2]
            data[domain]["country"] = temp2[3]
            data[domain]["CN"] = temp2[4]
            SAN = []
            for j in range(5, len(temp2)):
                if(temp2[j]!=''):
                    SAN.append(temp2[j])
                else:
                    break
            data[domain]["SAN"] = SAN
        elif temp2[2] == "error":
            data[domain]["TLS"] = temp[2]
            data[domain]["country"] = temp[3]
            data[domain]["CN"] = temp[4]
            SAN = []
            for j in range(5, len(temp)):
                if(temp[j]!=''):
                    SAN.append(temp[j].strip('\n'))
                else:
                    break
            data[domain]["SAN"] = SAN
        else:
            data[domain]["TLS"] = temp[2]
            if temp[2] != temp2[2]:
                data[domain]["TLS"] = data[domain]["TLS"] + " " + temp2[2]
            #print(i)
            data[domain]["country"] = temp[3]
            if temp[3] != temp2[3]:
                data[domain]["country"] = data[domain]["country"] + " " + temp2[3]
            data[domain]["CN"] = temp[4]
            if temp[4] != temp2[4]:
                data[domain]["CN"] = data[domain]["CN"]  + " " + temp2[4]
            SAN = []
            for j in range(5, len(temp)):
                if(temp[j]!=''):
                    SAN.append(temp[j].strip('\n'))
                else:
                    break
            for j in range(5, len(temp2)):
                if(temp2[j] != ''):
                    if temp2[j] not in SAN:
                        print("China add")
                        SAN.append(temp2[j])
                else:
                    break
            data[domain]["SAN"] = SAN
# filename
json_filename = "Alexa_CN_SAN.json"

# convert to json
with open(json_filename, "w") as json_file:
    json.dump(data, json_file, indent=4)