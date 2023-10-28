import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt

validcnt = 0
outcnt = 0
with open('rank_dependency_new2.json', 'r') as file:
    for line in tqdm(file):
        json_object = json.loads(line)
        validcnt += json_object['valid domain cnt']
        # outcnt +=  json_object['rely on out 1m cnt']
print(validcnt)
# print(outcnt)