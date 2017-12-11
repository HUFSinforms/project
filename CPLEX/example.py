from binary_KDM import binary_search
import pickle
import random

f5 = open('d:/pic/alpha.txt', 'rb')
alpha = pickle.load(f5)


sams = []
for i in range(len(alpha)):
    sams.append(i)

sols = random.sample(sams, 60)

www = binary_search(asset_index_list=sols, end_cond=0.001)

print(www)