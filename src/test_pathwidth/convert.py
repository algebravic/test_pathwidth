"""
  Convert a MaxSat model to a pyomo one.
"""
from typing import Tuple
from pysat.formula import WCNF
import pyomo.environ as pyo

def wcnf_to_pyomo(cnf: WCNF) -> pyo.ConcreteModel:

    # cnf.nv: number of Variables
    # cnf.hard: hard clauses
    # cnf.soft: soft clauses
    # cnf.wght: weights for soft clauses

    model = pyo.ConcreteModel()
    model.clauses = pyo.RangeSet(len(cnf.hard))
    model.vars = pyo.RangeSet(cnf.nv)
    model.x = pyo.Var(model.vars, domain=pyo.Binary)

    def make_clause(clause) -> pyo.expr:

        lhs = sum(((1 - 2 * int(_ < 0)) * model.x[abs(_)] for _ in clause))
        return lhs + sum(map(lambda _: int(_ < 0), clause))

    def clause_rule(model, ind):
        return make_clause(cnf.hard[ind - 1]) >= 1

    model.hard = pyo.Constraint(model.clauses, rule = clause_rule)
    # Now for the objective
    # First find how many non-unit soft clauses there are
    obj = sum((_[1] * make_clause(_[0]) for _ in zip(cnf.soft, cnf.wght)))

    model.OBJ = pyo.Objective(expr = obj, sense = pyo.maximize)

    return model
