
csvpath = "../Tranco_Dataset/tranco-apex-1m.csv"
with open(csvpath) as f:
    mill = f.readlines()
domain = [dd.split('\n')[0].split(',')[1] for dd in mill]

csvpath2 = "../Tranco_Dataset/tranco-withsub-1m.csv"
with open(csvpath2) as f2:
    mill = f2.readlines()
domain_sub = [dd.split('\n')[0].split(',')[1] for dd in mill]
print(domain_sub[0:100])