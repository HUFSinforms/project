from Cplex_KDM import portfolio
import pickle
import numpy as np


def binary_search(asset_index_list,end_cond):


    f0 = open('d:/pic/dic_sector.txt', 'rb')
    f1 = open('d:/pic/dic_bench.txt', 'rb')
    f2= open('d:/pic/risk_sedol.txt', 'rb')
    f3= open('d:/pic/dic_MCAP.txt', 'rb')
    f4= open('d:/pic/dic_beta.txt', 'rb')
    f5= open('d:/pic/alpha.txt', 'rb')
    f6= open('d:/pic/qmat.txt', 'rb')
    f7= open('d:/pic/Q_con.txt', 'rb')
    f8 = open('d:/pic/risk_mat.txt', 'rb')



    dic_sector = pickle.load(f0)
    dic_bench = pickle.load(f1)
    risk_sedol = pickle.load(f2)
    dic_MCAP = pickle.load(f3)
    dic_beta = pickle.load(f4)
    alpha = pickle.load(f5)
    qmat = pickle.load(f6)
    Q_con = pickle.load(f7)
    risk_mat = pickle.load(f8)




    sols = asset_index_list




    mins_list=[]
    mins_list2=[]


    rss=[]


    returns = 0

    w_up_dic = {}
    for i in risk_sedol:
        w_up_dic.update({i:0})

    list_result = portfolio(sector=dic_sector,bench=dic_bench,asset=risk_sedol,MCAPQ=dic_MCAP,beta=dic_beta,alpha=alpha,qmat=qmat, Q_con=Q_con,
                           returns=returns,sols=sols,big_w_dic=w_up_dic, w_upsums=0)

    w_dic = list_result[0]
    d_dic = list_result[1]
    rs = list_result[2]
    rss.append(rs)
    sum_min = 0
    mat_1 = np.empty(shape=[0, len(alpha)])
    mat_2 = np.zeros((len(risk_sedol), 1))


    for i in w_dic.keys():
        sum_min += min(w_dic[i],dic_bench[i])



    mins_list.append(1-sum_min)

    active_share = 1-sum_min



    k = 0


    for i in d_dic.keys():
        mat_1 = np.append(mat_1,d_dic[i])
        mat_2[k] = np.array([d_dic[i]])
        k+=1


    a=np.dot(mat_1,risk_mat)

    b=np.dot(a,mat_2)

    mins_list2.append(b)

    TE = b

    w_upsum = 0

    for i in w_dic.keys():
        if w_dic[i] > dic_bench[i]:
            w_up_dic.update({i: 1})
            w_upsum += w_dic[i]


    end = False

    if active_share >= 0.6 and TE >= 0.0025:
        return list_result
        end = False
    else:
        end = True

    dist = 1
    w_upsum2= 1
    Feasible_check = 0
    final_result_dic = {}

    while(end):
        if dist < end_cond:
            if active_share < 0.6 or TE < 0.0025:
                if Feasible_check == 0:
                    print("No Solution")
                else:
                    return final_result_dic
            else:
                return final_result_dic
            break


        w_upsum_in = (w_upsum+w_upsum2)*0.5
        list_result2 = portfolio(sector=dic_sector, bench=dic_bench, asset=risk_sedol, MCAPQ=dic_MCAP, beta=dic_beta,
                                alpha=alpha, qmat=qmat, Q_con=Q_con,returns=returns, sols=sols, big_w_dic=w_up_dic, w_upsums=w_upsum_in)

        w_dic = list_result2[0]
        d_dic = list_result2[1]
        rs = list_result2[2]
        sum_min = 0
        mat_1 = np.empty(shape=[0, len(alpha)])
        mat_2 = np.zeros((len(risk_sedol), 1))

        for i in w_dic.keys():
            sum_min += min(w_dic[i], dic_bench[i])

        active_share = 1 - sum_min

        k = 0

        for i in d_dic.keys():
            mat_1 = np.append(mat_1, d_dic[i])
            mat_2[k] = np.array([d_dic[i]])
            k += 1

        a = np.dot(mat_1, risk_mat)
        b = np.dot(a, mat_2)
        TE = b



        if active_share < 0.6 or TE < 0.0025:
            dist = w_upsum2 - w_upsum_in
            w_upsum = w_upsum_in
        else:
            dist = w_upsum_in - w_upsum
            w_upsum2 = w_upsum_in
            final_result_dic = list_result2
            Feasible_check += 1



