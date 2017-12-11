import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



def portfolio(sector,bench,asset,MCAPQ,beta,alpha,qmat,Q_con,returns,sols,w_upsums,big_w_dic):
    c = cplex.Cplex()
    t = c.variables.type


    c.variables.add(names=["d"+str(i) for i in asset],obj=alpha,lb=[-1*bench[j] for j in asset])

    c.variables.add(names=["assum"], lb=[-99999])






    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in asset], val=alpha)], senses=["E"],
        rhs=[0.0], names=["sum"])
    c.linear_constraints.set_linear_components("sum" , [["assum"], [-1.0]])



    bigeer_bench_sum = 0
    for i in asset:
        bigeer_bench_sum = bigeer_bench_sum + bench[i]*big_w_dic[i]

    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in asset], val=[big_w_dic[i] for i in asset])], senses=["E"],
        rhs=[w_upsums - bigeer_bench_sum], names=["w_big"])



    for i in asset:
        c.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = ["d"+str(i)], val = [1.0])],senses=["G"],rhs=[-1*bench[i]],names=[str(i)+"di_wi"])
        # c.linear_constraints.set_linear_components(str(i)+"di_wi", [["w" + str(i)], [1.0]])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["L"],
                                 rhs=[0.05], names=["st_5_1"])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["G"],
                                 rhs=[-0.05], names=["st_5_2"])



    for j in sector:
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in sector[j]], val=[1.0]*len(sector[j]))], senses=["L"],
                                 rhs=[0.1], names=["st_6_1"])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in sector[j]], val=[1.0]*len(sector[j]))], senses=["G"],
                                 rhs=[-0.1], names=["st_6_2"])


    for j in MCAPQ:
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in MCAPQ[j]], val=[1.0]*len(MCAPQ[j]))], senses=["L"],
                                 rhs=[0.1], names=["st_7_1"])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in MCAPQ[j]], val=[1.0]*len(MCAPQ[j]))], senses=["G"],
                                 rhs=[-0.1], names=["st_7_2"])


    c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in asset], val=[beta[i] for i in asset])], senses=["L"],
                             rhs=[0.1], names=["st_8_1"])
    c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i) for i in asset], val=[beta[i] for i in asset])], senses=["G"],
                             rhs=[-0.1], names=["st_8_2"])






    nums = 0
    for i in asset:
        if nums in sols:
            c.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["G"],
                rhs=[-1*bench[i]+0.00101], names=["st_select"+str(i)])

        else:
            c.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["E"],
                rhs=[-1*bench[i]], names=["st_select" + str(i)])
        nums += 1










    Q3 = cplex.SparseTriple(ind1=Q_con[0], ind2=Q_con[1], val=Q_con[2])
    c.quadratic_constraints.add(rhs=0.01, quad_expr=Q3, name="st_11_1", sense="L")






    c.objective.set_quadratic(qmat)

    c.objective.set_sense(c.objective.sense.minimize)
    c.solve()
    abcd=[]
    ab={}
    cd={}

    numa = 0
    for i in asset:
        if bench[i] + c.solution.get_values("d" + str(i)) > 0:
            print("w" + str(i)  + " : " + str(bench[i] + c.solution.get_values("d" + str(i))))
        ab.update({str(i):bench[i] + c.solution.get_values("d" + str(i))})
        cd.update({str(i):c.solution.get_values("d" + str(i))})
        numa += 1
    print("assum"+ " : " + str( c.solution.get_values("assum" )))
    print(c.solution.get_objective_value())
    print(c.solution.get_quadratic_slacks())
    abcd.append(ab)
    abcd.append(cd)
    abcd.append(c.solution.get_objective_value())
    return abcd