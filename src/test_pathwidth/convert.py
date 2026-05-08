"""
  Convert a MaxSat model to a pyomo one.
"""
from typing import Tuple
from itertools import ilen
from pysat.formula import WCNF
import pyomo.environ as pyo

def wcnf_to_pyomo(cnf: WCNF) -> pyo.ConcreteModel:

    # cnf.nv: number of Variables
    # cnf.hard: hard clauses
    # cnf.soft: soft clauses
    # cnf.wght: weights for soft clauses

    model = pyo.ConcreteModel()
    model.vars = pyo.RangeSet(cnf.nv)
    model.x = pyo.Var(model.vars, domain=pyo.Binary)

    def make_clause(clause) -> Tuple[pyo.expr, int]:

        lhs = sum(((1 - 2 * int(_ < 0)) * model.x[abs(_)] for _ in clause))
        return return lhs, 1 - sum(map(lambda _, int(_ < 0), clause))

    def clause_rule(model, ind):
        expr, rhs = make_clause(cnf[ind])
        return expr >= rhs

    model.hard = pyo.Constraint(model.vars, rule = clause_rule)
    # Now for the objective
    # First find how many non-unit soft clauses there are
    uhard = [_ for _ in zip(cnf.soft, cnf.wght) if len(_) == 1]
    nhard = [_ for _ in zip(cnf.soft, cnf.wght) if len(_) > 1]

    if uhard:

        uobj = sum(((1 - 2 * int(_[0] < 0)) * _[1] * model.x[abs(_[0])]
                    for _ in uhard))
        extra = sum(map(
            lambda _, int(_[0] < 0) * _[1], uhard)))
    else:
        uobj = 0
        extra = 0

                
    # Find any complicated claues
            
    if nhard:
        # extra variables
        # since we're maximizing we only need
        # evar => clause since if eval is true then the clause if true
        model.evars = pyo.RangeSet(len(nhard))
        model.y = pyo.Var(model.evars, domain=pyo.Binary)
        # For each soft clause make an equivalent variable

        def c_constraint(model, ind):

            # extra_var ==> soft clause
            expr, rhs = make_clause(nhard[ind][0])

            return - model.y[ind] + expr >= rhs - 1

        model.Extra = pyo.Constraint(model.evars, rule = c_constraint)

        nobj = sum((_[1] * model.y[ind]
                    for ind, _ in enumerate(nhard)))
    else:
        nobj = 0

    model.OBJ = pyo.Objective(expr = uobj + nobj - extra, sense = pyo.maximize)

    return model
