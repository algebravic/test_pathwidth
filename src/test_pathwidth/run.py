"""
  Contast the MaxSat implementation of pathwidth with the MIP implementation

  
"""
import argparse
from separation import pathwidth_order
from graph_families import square_graph, grid_graph, king_graph
from graph_families import knight_graph, square_diff_graph, hamming_graph
from milp_separation import pyomo_pathwidth_model
import pyomo.environ as pyo

def run_pathwidth():

    parser = argparse.ArgumentParser(description="Test Pathwidth implementations")
    parser.add_argument('graph', type=str, default='square',
                        help = 'The graph family')
    parser.add_argument('args', type=int, nargs='*',
                        help='The parameters for the family')
    parser.add_argument('--solver', type=str, nargs = '*',
                        default=['scip'],
                        help='The MIP solvers to use')
    parser.add_argument('--verbose', type=int, default=10,
                        help='The verbosity level for RC2')
    parser.add_argument('--adapt', type=bool, default=False,
                        help='Whether to use the adapt option for RC2')
    parser.add_argument('--minz', type=bool, default=False,
                        help='Whether to use the minz option for RC2')
    parser.add_argument('--exhaust', type=bool, default=False,
                        help='Whether to use the exhaust option for RC2')
    parser.add_argument('--stratified', type=bool, default=False,
                        help='Whether to use the stratified solver')
    families = {'knight': (knight_graph, 2),
                'square': (square_graph, 1),
                'square_diff' : (square_diff_graph, 1),
                'hamming': (hamming_graph, 1),
                'grid'   : (grid_graph, 2),
                'king'   : (king_graph, 2)
                }
    args = parser.parse_args()
    if args.graph not in families:
        print(f'Unknown graph family: {args.graph}')
        return
    fcn, nargs = families[args.graph]
    if nargs > len(args.args):
        print(f'Extra arguments ignored: {args.args[nargs: ]}')
    gph = fcn(*args.args[: nargs])
    # First run the RC2 version
    _ = pathwidth_order(gph,
                        verbose = args.verbose,
                        minz = args.minz,
                        exhaust = args.exhaust,
                        adapt = args.adapt,
                        stratified = args.stratified)
    # Now try the MIP solver
    model = pyomo_pathwidth_model(gph)
    for solver in args.solver:
        print(f"Using solver {solver}")
        try:
            slv = pyo.SolverFactory(solver)
        except ValueError as msg:
            print(f"Unknown solver {solver}")
            continue
        res = slv.solve(model)
        print(res['Solver'])
