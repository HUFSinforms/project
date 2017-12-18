import pandas as pd
import time,datetime
import numpy as np
from example.informs import portfolio
import cmath

#timeseries data
all_data=pd.read_csv('/TimeSeriesInputData.csv')
date_list=list(set(list(all_data['DATE'])))
for i in range(len(date_list)):
    ak=date_list[i]
    date_list[i]=ak[6:]+str('-')+ak[:2]+'-'+ak[3:5]
date_list.sort()
all_data['DATE']=pd.to_datetime(all_data['DATE'])
all_data=all_data.rename(columns={'NAME':'name','DATE':'date','SEDOL':'sedol','SECTOR':'sector','BETA':'beta','ALPHA_SCORE':'as','BENCH_WEIGHT':'bw',"MCAP_Q":'mq'})
sedol_list=all_data['sedol'].unique().tolist()



dic_data = {k: v for k, v in all_data.groupby('date')}

using_dic = dic_data[pd.to_datetime(date_list[0])]

# print(dic_data[pd.to_datetime(date_list[1])])
# print(using_dic.index)

asset_list = []
for i in using_dic["sedol"]:
    asset_list.append(i)





dic_sedol_as = {using_dic["sedol"][i] : 10000*using_dic["as"][i] for i in using_dic.index}

dic_bench = {using_dic["sedol"][i] : using_dic["bw"][i] for i in using_dic.index}

dic_beta = {using_dic["sedol"][i] : using_dic["beta"][i] for i in using_dic.index}

dic_sector = {using_dic["sector"][i] : [] for i in using_dic.index }
dic_MCAP = {using_dic["mq"][i] : [] for i in using_dic.index}

for i in using_dic.index:
    dic_sector[using_dic["sector"][i]].append(using_dic["sedol"][i])
    dic_MCAP[using_dic["mq"][i]].append(using_dic["sedol"][i])








#risk:cov_mat
def risk(date_str):
    risk_data=pd.read_csv('/Riskmodels2/cov_mat_%s.csv'%(date_str))
    risk_sedol=risk_data['ROW_INDEX'].unique().tolist()
    risk_mat = np.zeros((len(risk_sedol),len(risk_sedol)))
    risk_mat[np.triu_indices(len(risk_sedol), 0)] = list(risk_data['VALUE'])
    irows,icols = np.triu_indices(len(risk_sedol),0)
    risk_mat[icols,irows]=risk_mat[irows,icols]
    return risk_data,risk_sedol,risk_mat
risk_data,risk_sedol,risk_mat=risk(date_list[0])



sedol_var_list =[]

for i in risk_sedol:
    sedol_var_list.append("d"+str(i))



# for i in risk_sedol:
#     sedol_var_list.append("y"+str(i))
#
# for j in risk_sedol:
#     for i in range(2):
#         sedol_var_list.append("c"+str(j)+str(i))

sedol_var_list.append("assum")
alpha = []


for i in risk_sedol:
    alpha.append(-1*dic_sedol_as[i])

# asset_list.append(risk_sedol[0])

# dic_bench.update({risk_sedol[0]:0})
# dic_beta.update({risk_sedol[0]:0})

qmat=[]





for i in range(len(risk_mat)):
    qmat_1=[]
    qmat_1.append(sedol_var_list)
    new_risk_mat=[]
    for j in risk_mat[i]:
        new_risk_mat.append(j)
    new_risk_mat.append(0)
    # for j in risk_mat[i]:
    #     new_risk_mat.append(0)
    # for j in risk_mat[i]:
    #     for k in range(2):
    #         new_risk_mat.append(0)
    # qmat_1.append(list(risk_mat[i]))
    qmat_1.append(new_risk_mat)
    qmat.append(qmat_1)


for i in range(1):
    qmat_1=[]
    qmat_1.append(sedol_var_list)
    new_risk_mat=[]
    for j in risk_mat[i]:
        new_risk_mat.append(0)
    new_risk_mat.append(0)
    # for j in risk_mat[i]:
    #     new_risk_mat.append(0)
    # for j in risk_mat[i]:
    #     for k in range(2):
    #         new_risk_mat.append(0)
    qmat_1.append(new_risk_mat)
    qmat.append(qmat_1)


# for i in range(len(risk_mat)):
#     qmat_1=[]
#     qmat_1.append(sedol_var_list)
#     new_risk_mat=[]
#     for j in risk_mat[i]:
#         new_risk_mat.append(0)
#     for j in risk_mat[i]:
#         new_risk_mat.append(0)
#     for j in risk_mat[i]:
#         new_risk_mat.append(0)
#     for j in risk_mat[i]:
#         for k in range(2):
#             new_risk_mat.append(0)
#     qmat_1.append(new_risk_mat)
#     qmat.append(qmat_1)
#
# for k in range(len(risk_mat)):
#     for i in range(2):
#         qmat_1=[]
#         qmat_1.append(sedol_var_list)
#         new_risk_mat=[]
#         for j in range(len(risk_mat[i])):
#             new_risk_mat.append(0)
#         for j in range(len(risk_mat[i])):
#             new_risk_mat.append(0)
#         for j in range(len(risk_mat[i])):
#             new_risk_mat.append(0)
#         for j in risk_mat[i]:
#             for k in range(2):
#                 new_risk_mat.append(0)
#         qmat_1.append(new_risk_mat)
#         qmat.append(qmat_1)
# 픽스




q_con1 = []
q_con2 = []
q_val = []


for i in range(len((risk_mat[0]))):
    for j in range(len(risk_mat[0])):
        if j >= i:
            q_con1.append(i)
            q_con2.append(j)
            if i == j:
                ex_list = list(risk_mat[i])
                q_val.append(ex_list[j])
            else:
                ex_list = list(risk_mat[i])
                q_val.append(2*ex_list[j])



Q_con = []
Q_con.append(q_con1)
Q_con.append(q_con2)
Q_con.append(q_val)


f0 = open('d:/pic/dic_sector.txt', 'wb')
f1 = open('d:/pic/dic_bench.txt', 'wb')
f2= open('d:/pic/risk_sedol.txt', 'wb')
f3= open('d:/pic/dic_MCAP.txt', 'wb')
f4= open('d:/pic/dic_beta.txt', 'wb')
f5 = open('d:/pic/alpha.txt', 'wb')
f6 = open('d:/pic/qmat.txt', 'wb')
f7 = open('d:/pic/Q_con.txt', 'wb')
f8 = open('d:/pic/risk_mat.txt', 'wb')
import pickle
pickle.dump(dic_sector, f0)
pickle.dump(dic_bench, f1)
pickle.dump(risk_sedol, f2)
pickle.dump(dic_MCAP, f3)
pickle.dump(dic_beta, f4)
pickle.dump(alpha, f5)
pickle.dump(qmat, f6)
pickle.dump(Q_con, f7)
pickle.dump(risk_mat, f8)

f0.close()
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()




# dic_result = portfolio(sector=dic_sector,bench=dic_bench,asset=risk_sedol,MCAPQ=dic_MCAP,beta=dic_beta,alpha=alpha,qmat=qmat, Q_con=Q_con)
# dic_result = portfolio(sector=dic_sector,bench=dic_bench,asset=risk_sedol,MCAPQ=dic_MCAP,beta=dic_beta,alpha=alpha,qmat=qmat, Q_con=Q_con)

# w_dic = {}
#
#
# for i in dic_result.keys():
#     w_dic.update({str(i):dic_bench[i]+dic_result[i]})
#
# pre_list = set(list(w_dic.keys()))
#
# rsrs = 0
#
# for i in risk_sedol:
#     rsrs += dic_result[i]*dic_sedol_as[i]
#
# print(rsrs)

######################################################################################################################################################
#
# using_dic = dic_data[pd.to_datetime(date_list[1])]
#
# asset_list = []
# for i in using_dic["sedol"]:
#     asset_list.append(i)
#
# dic_sedol_as = {using_dic["sedol"][i] : using_dic["as"][i] for i in using_dic.index}
#
# dic_bench = {using_dic["sedol"][i] : using_dic["bw"][i] for i in using_dic.index}
#
# dic_beta = {using_dic["sedol"][i] : using_dic["beta"][i] for i in using_dic.index}
#
# dic_sector = {using_dic["sector"][i] : [] for i in using_dic.index }
# dic_MCAP = {using_dic["mq"][i] : [] for i in using_dic.index}
#
# for i in using_dic.index:
#     dic_sector[using_dic["sector"][i]].append(using_dic["sedol"][i])
#     dic_MCAP[using_dic["mq"][i]].append(using_dic["sedol"][i])
#
#
# risk_data,risk_sedol,risk_mat=risk(date_list[1])
#
#
#
# sedol_var_list =[]
#
# for i in risk_sedol:
#     sedol_var_list.append("d"+str(i))
#
#
# alpha = []
#
#
# for i in risk_sedol:
#     alpha.append(-1*dic_sedol_as[i])
#
#
# qmat=[]
#
#
#
#
#
# for i in range(len(risk_mat)):
#     qmat_1=[]
#     qmat_1.append(sedol_var_list)
#     new_risk_mat=[]
#     for j in risk_mat[i]:
#         new_risk_mat.append(j)
#     qmat_1.append(new_risk_mat)
#     qmat.append(qmat_1)
#
#
#
# dic_result2 = portfolio(sector=dic_sector,bench=dic_bench,asset=risk_sedol,MCAPQ=dic_MCAP,beta=dic_beta,alpha=alpha,qmat=qmat)
#
#
# w_dic2 = {}
#
# for i in dic_result2.keys():
#     w_dic2.update({str(i):dic_bench[i]+dic_result2[i]})
#
# pre_list2 = set(list(w_dic2.keys()))
#
# turnover = 0
#
# add_key_1 = pre_list-pre_list2
# add_key_2 = pre_list2-pre_list
#
#
# for i in add_key_2:
#     w_dic.update({i:0})
#
# for i in add_key_1:
#     w_dic2.update({i:0})
#
# pre_list.union(pre_list2)
#
# for i in pre_list:
#     turnover += abs(w_dic2[i]-w_dic[i])
#
#
#
# rOTP = 0
#
# for i in dic_sedol_as.keys():
#     rOTP += w_dic2[i]*dic_sedol_as[i]
#
# r_Txadj_t = rOTP - turnover*0.5
#
# print("turnover : " + str(turnover))
# print("r_OTP : " + str(rOTP))
# print("r_Txadj_t : " + str(r_Txadj_t))