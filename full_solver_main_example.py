"""
Edited February 20, 2023
Simon Schoenbeck
This is the main function used for the completed solver that could select between multiple algorithms.
The functions used for solving are not included.
"""

import time
import copy
import argparse
from math import log
from problem_parser import main as parse_main
from problem_parser import ProblemInstance




def main():
    global problem, constraints, constrained_variable_pairs, variable_order, solving_start, solver, all_solving_end, dynamic_ordering
    problem = parse_main(args)

    constraints = problem.constraints
    var_count = len(problem.variables)
    get_constrained_variable_pairs()

    constrained_variable_pairs.sort(key=lambda x: x[0], reverse=False)
    solving_start = time.time()
    setup_domains()
    enforce_node_consistency()

    if dynamic_ordering:
        setup_datastructures()
        ordering_heuristic()
    else:
        ordering_heuristic()
        setup_datastructures()

    solver()
    all_solving_end = time.time()

    output_results()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing how to parse command line arguments')
    parser.add_argument('-f', metavar='file_path', help='file name for the CSP instance')
    parser.add_argument('-s', metavar='solver', help='algorithm for solving the CSP options: BT for backtrack search')
    parser.add_argument('-u', metavar='heuristic',
                        help='ordering heuristic for solving the CSP options: LX, LD, DEG, DD')
    parser.add_argument('--csv', dest='output_format', action='store_const', const=True, default=False,
                        help='changes the output format for easy conversion to csv '
                             'when \'csv\'')
    parser.add_argument('--pi', metavar='print_info', help='print out the CSP instance', nargs='?', const=True, default=False)
    args = parser.parse_args()
    if args.f is not None:
        # Setting up variables in the global scope
        problem = None  # The CSP instance being solved.
        constraints = dict()
        current_domains = dict()
        initial_domains = dict()
        constrained_variable_pairs = list()
        unary_constraints = list()
        ordering_heuristic = id_var_st
        consistent = True
        dynamic_ordering = False

        if args.s == 'CBJ':
            solver = default_CBJ
            solver_type = 'CBJ'
            setup_datastructures = setup_cbj_data_structures
            conf_set = list()
        elif args.s == 'FC':
            solver = default_FC
            solver_type = 'FC'
            setup_datastructures = setup_fc_data_structures
            reductions = dict()
            future_vars = set()
            past_vars = set()
        elif args.s == 'FCCBJ':
            solver = default_FC
            solver_type = 'FCCBJ'
            setup_datastructures = setup_fc_cbj_data_structures
            reductions = dict()
            future_vars = set()
            past_vars = set()
            conf_set = list()
            variable_order_dict = dict()
        else:
            solver = default_BT
            solver_type = 'BT'
            setup_datastructures = setup_bt_data_structures

        if args.u == 'dLD':
            ordering_heuristic = dynamic_ld_var_st
            heuristic = 'dLD'
            dynamic_ordering = True
        elif args.u == 'dDEG':
            ordering_heuristic = dynamic_deg_var_st
            heuristic = 'dDEG'
            dynamic_ordering = True
        elif args.u == 'dDD':
            ordering_heuristic = dynamic_ddr_var_st
            heuristic = 'dDD'
            dynamic_ordering = True
        elif args.u == 'LD':
            ordering_heuristic = ld_var_st
            heuristic = 'LD'
        elif args.u == 'DEG':
            ordering_heuristic = deg_var_st
            heuristic = 'DEG'
        elif args.u == 'DD':
            ordering_heuristic = ddr_var_st
            heuristic = 'DD'
        else:
            heuristic = 'LX'
        variable_order = None
        current_path_assignments = list()
        current_domain_array = list()
        setup_start = time.time()
        solving_start = time.time()
        single_solving_end = time.time()
        all_solving_end = time.time()
        status = None
        cc = 0
        cc_single = 0
        nv = 0
        nv_single = 0
        bt = 0
        bt_single = 0
        total_solutions = 0
        first_solution = None
        main()
    else:
        print('Error no file path given')