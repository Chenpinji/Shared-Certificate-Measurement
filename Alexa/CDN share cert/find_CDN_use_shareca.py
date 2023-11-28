import json
# with open('Alexa_CN_SAN.json','r') as j_file:
#     cadata = json.load(j_file)
flag = 0
# for i in cadata:
#     # print(i)
#     namelist = i.split('.')
#     length = len(namelist)
#     if cadata[i]['TLS'] == "error":
#         continue
#     cnt = 0
#     for j in range(length-1):
#         for san in cadata[i]['SAN']:
#             if namelist[j] in san:
#                 cnt += 1
#     if cnt < len(cadata[i]['SAN']) / 2 and cnt < 5 and int(cadata[i]['rank']) > 500:
#         print(i,end=" ")
#         print(cadata[i]['rank'])
#         flag += 1
#         if flag > 20:
#             break
    # print(namelist)
    # print(cadata[i])
    
with open('Alexa_CN_SAN_1w.json', 'r') as file:
    json_objects = []
    current_json = ""
    cnt = 0
    for line in file:
        if line != '}\n' and line:  # 如果该行不为空
            line = line.strip()
            current_json += line
        else:
            current_json += '}'
            if current_json:  # 如果当前 JSON 非空
                json_objects.append(current_json)
                current_json = ""  # 重置当前 JSON 字符串
    if current_json:  # 处理最后一个 JSON 对象
        json_objects.append(current_json)

    for line in json_objects:
        # print(line)
        json_object = json.loads(line)
        if json_object['TLS'] == "error":
            continue
        namelist = json_object["domain"].split('.')
        length = len(namelist)
        cnt = 0
        for san in json_object['SAN']:
            for j in range(length-1):
                if namelist[j] in san:
                    cnt += 1
                    break
        if cnt < len(json_object['SAN']) / 2 and cnt < 10 and int(json_object['rank']) > 1000 and json_object["domain"] != json_object["CN"]: 
            print(json_object['domain'],end=" ")
            print(json_object['rank'],end="-----")
            print(json_object['CN'])
            flag += 1
            if flag > 200:
                break