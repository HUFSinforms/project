import pandas as pd
import numpy as np
import pickle
from cplex_kdm import portfolio



class informs:
    def __init__(self,omega_multi):
        f0 = open('d:/pic/dic_sector.txt', 'rb')
        f1 = open('d:/pic/dic_bench.txt', 'rb')
        f2 = open('d:/pic/risk_sedol.txt', 'rb')
        f3 = open('d:/pic/dic_MCAP.txt', 'rb')
        f4 = open('d:/pic/dic_beta.txt', 'rb')
        f5 = open('d:/pic/alpha.txt', 'rb')
        f6 = open('d:/pic/qmat.txt', 'rb')
        f7 = open('d:/pic/Q_con.txt', 'rb')
        f8 = open('d:/pic/risk_mat.txt', 'rb')

        self.dic_sector = pickle.load(f0)
        self.dic_bench = pickle.load(f1)
        self.risk_sedol = pickle.load(f2)
        self.dic_MCAP = pickle.load(f3)
        self.dic_beta = pickle.load(f4)
        self.alpha = pickle.load(f5)
        self.qmat = pickle.load(f6)
        self.risk_mat = pickle.load(f8)
        self.omegamulti = omega_multi
        self.conlist = [0,1,2,3,4,5]
        q_con1 = []
        q_con2 = []
        q_val = []

        for i in range(len((self.risk_mat[0]))):
            for j in range(len(self.risk_mat[0])):
                if j >= i:
                    q_con1.append(i)
                    q_con2.append(j)
                    if i == j:
                        ex_list = list(self.risk_mat[i])
                        q_val.append(omega_multi * ex_list[j])
                    else:
                        ex_list = list(self.risk_mat[i])
                        q_val.append(2*omega_multi * ex_list[j])

        Q_cons = []
        Q_cons.append(q_con1)
        Q_cons.append(q_con2)
        Q_cons.append(q_val)
        self.Q_con = Q_cons


    def set_omega(self,risk_mat):

        self.qmat = []

        sedol_var_list = []

        for i in self.risk_sedol:
            sedol_var_list.append("d" + str(i))



        sedol_var_list.append("assum")

        for i in range(len(risk_mat)):
            qmat_1 = []
            qmat_1.append(sedol_var_list)
            new_risk_mat = []
            for j in risk_mat[i]:
                new_risk_mat.append(j*self.omegamulti)
            new_risk_mat.append(0)
            qmat_1.append(new_risk_mat)
            self.qmat.append(qmat_1)

        for i in range(1):
            qmat_1 = []
            qmat_1.append(sedol_var_list)
            new_risk_mat = []
            for j in risk_mat[i]:
                new_risk_mat.append(0)
            new_risk_mat.append(0)
            qmat_1.append(new_risk_mat)
            self.qmat.append(qmat_1)

        a = np.full((len(self.alpha), len(self.alpha)), self.omegamulti)

        self.risk_mat = risk_mat * a

    def set_alpha(self,alphas):
        self.alpha = alphas


    def set_con(self,cons):
        self.conlist = cons


    def solve(self,end_cond):
        mins_list = []
        mins_list2 = []


        rss = []

        self.returns = 0

        w_up_dic = {}

        for i in self.risk_sedol:
            w_up_dic.update({i: 0})

        list_result = portfolio(sector=self.dic_sector, bench=self.dic_bench, asset=self.risk_sedol, MCAPQ=self.dic_MCAP, beta=self.dic_beta,
                                alpha=self.alpha, qmat=self.qmat, Q_con=self.Q_con,
                                returns=self.returns, sols=self.conlist, big_w_dic=w_up_dic, w_upsums=0 , multiple=self.omegamulti)

        w_dic = list_result[0]
        d_dic = list_result[1]
        rs = list_result[2]
        rss.append(rs)
        sum_min = 0
        mat_1 = np.empty(shape=[0, len(self.alpha)])
        mat_2 = np.zeros((len(self.risk_sedol), 1))

        for i in w_dic.keys():
            sum_min += min(w_dic[i], self.dic_bench[i])

        print("sum_min : " + str(1 - sum_min))
        mins_list.append(1 - sum_min)

        active_share = 1 - sum_min

        print("AC")
        print(active_share)

        k = 0

        for i in d_dic.keys():
            mat_1 = np.append(mat_1, d_dic[i])
            mat_2[k] = np.array([d_dic[i]])
            k += 1

        # print(mat_1)
        # print(mat_2)

        # mins_list.append(1-sum_min)

        a = np.dot(mat_1, self.risk_mat)
        b = np.dot(a, mat_2)
        print("TE")
        print(b)
        mins_list2.append(b)

        TE = b

        w_upsum = 0

        for i in w_dic.keys():
            if w_dic[i] > self.dic_bench[i]:
                w_up_dic.update({i: 1})
                w_upsum += w_dic[i]

        end = False

        if active_share >= 0.6 and TE >= 0.0025*self.omegamulti:
            return list_result
            end = False
        else:
            end = True

        dist = 1
        w_upsum2 = 1
        Feasible_check = 0
        final_result_dic = {}

        while (end):
            if dist < end_cond:
                if active_share < 0.6 or TE < 0.0025*self.omegamulti:
                    if Feasible_check == 0:
                        print("No Solution")
                    else:
                        return final_result_dic
                else:
                    return final_result_dic
                break

            w_upsum_in = (w_upsum + w_upsum2) * 0.5
            list_result2 = portfolio(sector=self.dic_sector, bench=self.dic_bench, asset=self.risk_sedol, MCAPQ=self.dic_MCAP,
                                     beta=self.dic_beta,
                                     alpha=self.alpha, qmat=self.qmat, Q_con=self.Q_con, returns=self.returns, sols=self.conlist,
                                     big_w_dic=w_up_dic, w_upsums=w_upsum_in, multiple=self.omegamulti)

            w_dic = list_result2[0]
            d_dic = list_result2[1]
            rs = list_result2[2]
            sum_min = 0
            mat_1 = np.empty(shape=[0, len(self.alpha)])
            mat_2 = np.zeros((len(self.risk_sedol), 1))

            for i in w_dic.keys():
                sum_min += min(w_dic[i], self.dic_bench[i])

            active_share = 1 - sum_min

            k = 0

            for i in d_dic.keys():
                mat_1 = np.append(mat_1, d_dic[i])
                mat_2[k] = np.array([d_dic[i]])
                k += 1

            a = np.dot(mat_1, self.risk_mat)
            b = np.dot(a, mat_2)
            TE = b

            print(TE)
            print(active_share)
            if active_share < 0.6 or TE < 0.0025*self.omegamulti:
                dist = w_upsum2 - w_upsum_in
                w_upsum = w_upsum_in
            else:
                dist = w_upsum_in - w_upsum
                w_upsum2 = w_upsum_in
                final_result_dic = list_result2
                Feasible_check += 1