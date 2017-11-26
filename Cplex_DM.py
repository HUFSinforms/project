import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



def portfolio(sector,bench,asset,MCAPQ,beta,alpha,qmat):
    c = cplex.Cplex()
    t = c.variables.type


    c.variables.add(names=["d"+str(i) for i in asset],obj=alpha,lb=[-1*bench[j] for j in asset])

    # print(c.variables.get_lower_bounds())
    c.variables.add(names= ["q"+str(i) for i in asset] ,types=[t.binary for j in range(len(asset))])

    c.variables.add(names=["y"+str(i) for i in asset],lb=[-99999999999 for j in asset])

    c.variables.add(names=["c" + str(i) for i in range(2)], types=[t.binary for j in range(2)])





    for i in asset:
        # c.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = ["d"+str(i)], val = [1.0])],senses=["G"],rhs=[-1*bench[i]],names=[str(i)+"di_wi"])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["L"],
                                 rhs=[0.05], names=["st_5_1"])
        c.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=["d" + str(i)], val=[1.0])], senses=["G"],
                                 rhs=[-0.05], names=["st_5_2"])


    bench_sum = 0

    for i in bench:
        bench_sum += bench[i]

    print(bench_sum)



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


    for i in asset:
        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["q" + str(i)], val=[1.0])], senses=["G"],
            rhs=[bench[i]], names=["st_q"+str(i)])
        c.linear_constraints.set_linear_components("st_q"+str(i), [["d" + str(i)], [-1.0]])

        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["q" + str(i)], val=[1.0])], senses=["L"],
            rhs=[0.999+bench[i]], names=["st_qq" + str(i)])
        c.linear_constraints.set_linear_components("st_qq" + str(i), [["d" + str(i)], [-1.0]])

        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["y" + str(i)], val=[1.0])], senses=["L"],
            rhs=[bench[i]], names=["st_y1" + str(i)])
        c.linear_constraints.set_linear_components("st_y1" + str(i), [["d" + str(i)], [-1.0]])

        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["y" + str(i)], val=[1.0])], senses=["L"],
            rhs=[bench[i]], names=["st_y2" + str(i)])

        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["y" + str(i)], val=[1.0])], senses=["G"],
            rhs=[bench[i]-99999999999.0], names=["st_y3" + str(i)])
        c.linear_constraints.set_linear_components("st_y3" + str(i), [["d" + str(i)], [-1.0]])
        c.linear_constraints.set_linear_components("st_y3" + str(i), [["c" + str(0)], [-99999999999.0]])

        c.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=["y" + str(i)], val=[1.0])], senses=["G"],
            rhs=[bench[i]-99999999999.0], names=["st_y4" + str(i)])
        c.linear_constraints.set_linear_components("st_y4" + str(i), [["c" + str(1)], [-99999999999.0]])





    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["q" + str(i) for i in asset], val=[1.0]*len(asset))], senses=["G"],
        rhs=[50], names=["st_9_1"])


    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["q" + str(i) for i in asset], val=[1.0]*len(asset))], senses=["L"],
        rhs=[70], names=["st_9_2"])

    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["y" + str(i) for i in asset], val=[1.0] * len(asset))], senses=["G"],
        rhs=[0], names=["st_10_1"])

    c.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind=["y" + str(i) for i in asset], val=[1.0] * len(asset))], senses=["L"],
        rhs=[0.4], names=["st_10_2"])


    c.objective.set_quadratic(qmat)

    c.objective.set_sense(c.objective.sense.minimize)
    c.solve()

    ab={}

    for i in asset:
        print("d" + str(i)  + " : " + str(c.solution.get_values("d" + str(i))))
        ab.update({str(i):c.solution.get_values("d" + str(i))})

    print(c.solution.get_objective_value())


    return ab