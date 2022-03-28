"""
Homework 2
Due Feb 21, 2022
CSCE 421
Simon Schoenbeck

A modular implementation of a CSP solver with AC-1 and AC-3.
"""

import time
import copy
import argparse
from math import log
from problem_parser import main as parse_main
from problem_parser import ProblemInstance


def calc_initial_size():
    """Calculates the initial total combinations of VVPs"""
    global iSize
    iSize = 1
    for var_name in problem.variables:
        d_size = problem.domains[problem.variables[var_name].initial_domain].size
        iSize = iSize * d_size


def calc_final_size():
    """Calculates the final total combinations of VVPs"""
    global fSize
    fSize = 1
    for var_name in problem.variables:
        d_size = len(current_domains[var_name])
        fSize = fSize * d_size


def evaluate_vvd(vvd):
    """Given a variable-value dictionary evaluate if this is allowed by the constraints"""
    relevant_constraint = None
    var1_name, var2_name = vvd.keys()
    result = True
    for constraint_n in problem.variables[var1_name].constraints:
        if constraint_n in problem.variables[var2_name].constraints:
            relevant_constraint = constraints[constraint_n]
            reference_name = relevant_constraint.reference
            if reference_name in problem.relations:
                """ Evaluate for enumerated constraints"""
                relation = problem.relations[relevant_constraint.reference]
                relation_type = relation.semantics
                variable_order = relevant_constraint.variables
                val_tuple = (vvd[variable_order[0]], vvd[variable_order[1]])
                if relation_type == 'supports':
                    result = result and val_tuple in relation.pairs
                elif relation_type == 'conflicts':
                    result = result and val_tuple not in relation.pairs
                else:
                    print(f'Found reference_name: {reference_name} in relations but type was "{relation_type}".')
            elif reference_name in problem.predicates:
                """ Evaluate for instantiated constraints"""
                predicate = problem.predicates[reference_name]
                cf = predicate.custom_function
                predicate_param_list = predicate.parameter_list
                constraint_param_list = constraints[constraint_n].parameters
                arg_dict = dict()
                param_count = len(predicate_param_list)
                for i in range(param_count):
                    if constraint_param_list[i] in vvd:
                        arg_dict[predicate_param_list[i]] = vvd[constraint_param_list[i]]
                    else:
                        arg_dict[predicate_param_list[i]] = constraint_param_list[i]
                evaluation = cf.evaluate(arg_dict)
                result = result and evaluation
    return result


def enforce_node_consistency():
    """Enforces node consistency over all unary constraints"""
    global constraints, unary_constraints, current_domains
    for unary_constraint in unary_constraints:
        var = constraints[unary_constraint].variables[0]
        reference_name = constraints[unary_constraint].reference
        if reference_name in problem.relations:
            """Enforces node consistency for enumerated constraints"""
            relation = problem.relations[reference_name]
            relation_type = relation.semantics
            if relation_type == 'supports':
                current_domains[var] = relation.pairs
            else:
                print('Node consistency not enforced with supports')

        elif reference_name in problem.predicates:
            """Enforces node consistency for intension constraints"""
            predicate = problem.predicates[reference_name]
            cf = predicate.custom_function
            predicate_param_list = predicate.parameter_list
            constraint_param_list = constraints[unary_constraint].parameters
            potential_values = list(current_domains[var])
            for potential_val in potential_values:
                vvd = {var: potential_val}
                arg_dict = dict()
                param_count = len(predicate_param_list)
                for i in range(param_count):
                    if constraint_param_list[i] in vvd:
                        arg_dict[predicate_param_list[i]] = vvd[constraint_param_list[i]]
                    else:
                        arg_dict[predicate_param_list[i]] = constraint_param_list[i]
                evaluation = cf.evaluate(arg_dict)
                if not evaluation:
                    current_domains[var].remove(potential_val)


def output_results():
    """Outputs the results of the AC algorithm"""
    global problem, cc, fVal, iSize, fSize, fEffect, domain_elimination, current_domains
    global setup_start, solving_start, solving_end
    calc_final_size()
    if domain_elimination:
        fEffect = False
        fSize = False
    else:
        fEffect = iSize / fSize
        fEffect = log(fEffect)
        fSize = log(fSize)
    iSize = log(iSize)
    if args.output_format:
        file_name = args.f.split('\\')[-1]
        print(
            f'{file_name}, {args.a}, {problem.name}, {cc}, {solving_end - solving_start}, {fVal}, {iSize}, {fSize}, {fEffect}')
    else:
        print(f'Instance name: {problem.name}\n'
              f'time-setup: {solving_start - setup_start}\n'
              f'cc: {cc}\n'
              f'cpu: {solving_end - solving_start}\n'
              f'fVal: {fVal}\n'
              f'iSize: {iSize}\n'
              f'fSize: {fSize}\n'
              f'fEffect: {fEffect}')


def get_constrained_variable_pairs():
    """Pairs up all the variables that share a constraint for use in a queue"""
    global constraints, constrained_variable_pairs, unary_constraints
    constrained_variable_pairs = []
    for constraint_name in constraints:
        variables = constraints[constraint_name].variables
        if len(variables) == 1:
            unary_constraints.append(constraint_name)
        for v1 in variables:
            for v2 in variables:
                if v1 is not v2:
                    # print(f'Adding {(v1, v2)}')
                    constrained_variable_pairs.append((v1, v2))


def setup_domains():
    """Initialized the current domains for all variables"""
    global problem, current_domains, constraints
    for var_name in problem.variables:
        current_domains[var_name] = copy.copy(problem.domains[problem.variables[var_name].initial_domain].values)
    # print(current_domains)


def main():
    global problem, constraints, queue, constrained_variable_pairs, solving_start, solving_end
    problem = parse_main(args)
    constraints = problem.constraints
    get_constrained_variable_pairs()

    constrained_variable_pairs.sort(key=lambda x: x[0], reverse=False)
    queue = copy.copy(constrained_variable_pairs)
    calc_initial_size()
    setup_domains()

    solving_start = time.time()
    enforce_node_consistency()
    solving_end = time.time()

    output_results()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This file is a base for an AC solver.')
    parser.add_argument('-f', metavar='file_path', help='file name for the CSP instance')
    parser.add_argument('--csv', dest='output_format', action='store_const', const=True, default=False,
                        help='changes the output format for easy conversion to csv '
                             'when \'csv\'')
    args = parser.parse_args()
    if args.f is not None:
        # Setting up variables in the global scope
        problem = None  # The CSP instance being solved.
        cpu_time = None # The value of CPU time that the solver has spent ‘working’ on the instance.
        cc = 0          # The number of times a constraint is accessed to check whether two variable-value pairs are consistent.
        fVal = 0        # The sum of the number of values removed by NC and AC1/AC3 from the domains of all variables.
        iSize = None    # The initial size of the CSP is the number of combinations of variable - value pairs for all
                        # variables, it is the product of the initial domain sizes
        fSize = None    # Tf the problem is arc consistent, the size of the filtered CSP after enforcing arc consistency.
        fEffect = None  # If the problem is arc consistent, the value of filtering effectiveness
                        # if given by filter otherwise it is false/undetermined.

        # These variables are defined in the global scope to allow for eastier information sharing between functions.
        constraints = dict()
        current_domains = dict()
        queue = list()
        constrained_variable_pairs = list()
        unary_constraints = list()
        domain_elimination = False
        setup_start = time.time()
        solving_start = time.time()
        solving_end = time.time()
        main()
    else:
        print('Error no file path given')
