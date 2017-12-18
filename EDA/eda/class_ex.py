import class_informs as inform
import pickle

ex = inform.informs(10000)

con = []
for i in range(70):
    con.append(i)
f8 = open('d:/pic/risk_mat.txt', 'rb')
risk_mat = pickle.load(f8)
ex.set_omega(risk_mat)

import time
start_time = time.time()

ex.set_con(cons=con)
ex.solve(0.01)

print("--- %s seconds ---" %(time.time() - start_time))

