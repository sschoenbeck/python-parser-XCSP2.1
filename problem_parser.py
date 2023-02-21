"""
Homework 1
Due Feb 7, 2022
CSCE 421
Simon Schoenbeck

An implementation of the parser from XML file to ProblemInstance object.
"""

import copy
import argparse
import xml.etree.ElementTree as ElT
from intension_parser import CustomFunction, function_names


class ProblemInstance(object):
    """Object class for the whole ProblemInstance."""

    def __init__(self, name, variables, constraints, predicates, relations, domains):
        self.name = copy.copy(name)
        self.variables = copy.copy(variables)
        self.constraints = copy.copy(constraints)
        self.predicates = copy.copy(predicates)
        self.relations = copy.copy(relations)
        self.domains = copy.copy(domains)

    def print_info(self):
        """Prints out the structure of the Problem Instance"""
        print(f'Instance name: {self.name}')
        self.print_variables()
        self.print_constraints()
        print()

    def print_constraints(self):
        """Prints the constraints"""
        print('Constraints:')
        for name in self.constraints:
            reference = self.constraints[name].reference
            if reference in self.predicates:
                reference = f'intension function: {self.predicates[reference].function_str}, ' \
                            f'parameter_list: {self.predicates[reference].parameter_list}, ' \
                            f'custom_function: {self.predicates[reference].custom_function.execute}, ' \
                            f'params: {self.constraints[name].parameters}'
            elif reference in self.relations:
                reference = f'{self.relations[reference].semantics} {self.relations[reference].pairs}'
            print(f'Name: {name}, variables: {self.constraints[name].variables}, definition: {reference}')

    def print_variables(self):
        """Prints outs the varaibles"""
        print('Variables:')
        for variable in self.variables:
            var = self.variables[variable]
            print(
                f'Name: {var.name}, initial-domain: {self.domains[var.initial_domain].values}, \
                constraints: {var.constraints}, neighbors: {var.neighbors}')


class Variable(object):
    """Object class for Variable"""

    def __init__(self, name, domain):
        self.name = name
        self.initial_domain = copy.copy(domain)
        self.current_domain = copy.copy(domain)
        self.constraints = set()
        self.neighbors = set()

    def add_constraint(self, constraint):
        """Adds a constraint name (str) to the variable object"""
        self.constraints.add(constraint)

    def add_scope(self, scope):
        """Sets the scope (set of neighbors) to the variable object"""
        clean_scope = set(scope) - {self.name}
        self.neighbors.update(clean_scope)


class Constraint(object):
    """Object class for Constraints"""

    def __init__(self, name, arity, variables, reference, parameters):
        self.name = copy.copy(name)
        self.arity = copy.copy(arity)
        self.variables = copy.copy(variables)
        self.reference = copy.copy(reference)
        self.parameters = copy.copy(parameters)


class Predicate(object):
    """Object class for Constraints defined by instantiation"""

    def __init__(self, name, parameter_str, function_str):
        self.name = name
        self.parameter_str = copy.copy(parameter_str)
        self.function_str = copy.copy(function_str)
        self.parameter_list = list()
        self.custom_function = None


class Relation(object):
    """Object class for Constraints defined by enumeration"""

    def __init__(self, name, arity, nb_tuples, semantics, pairs):
        self.name = name
        self.arity = arity
        self.nbTuples = copy.copy(nb_tuples)
        self.semantics = copy.copy(semantics)
        self.pairs = copy.copy(pairs)


class Domain(object):
    """Object class for variable domains"""

    def __init__(self, name, size, values):
        self.name = copy.copy(name)
        self.size = copy.copy(size)
        self.values = copy.copy(values)


def text_to_domain_values(domain_text, domain_size):
    """Converts text of enumerated domain into a list of integers."""
    domain_values = set()
    text_parts = domain_text.split(' ')
    for text_part in text_parts:
        if '..' in text_part:
            start, end = text_part.split('..')
            for i in range(int(start), int(end) + 1):
                domain_values.add(i)
        else:
            domain_values.add(int(text_part))
    assert (len(domain_values) == domain_size)
    return domain_values


def parse_domains(domains_xml):
    """Creates domain objects"""
    domains = dict()
    for domain in domains_xml:
        name = domain.attrib['name']
        size = int(domain.attrib['nbValues'])
        values = text_to_domain_values(domain.text, size)
        domains[name] = Domain(name, size, values)
    return domains


def parse_variables(variables_xml):
    """Creates variable objects"""
    variables = dict()
    for variable in variables_xml:
        name = variable.attrib['name']
        domain = variable.attrib['domain']
        variables[name] = Variable(name, domain)
    return variables


def text_to_relation_pairs(relation_text, tuple_count):
    """Converts text into relation pairs"""
    if tuple_count == 1:
        return {int(relation_text)}
    relation_values = set()
    text_parts = relation_text.split('|')
    for text_part in text_parts:
        x, y = text_part.split(' ')
        relation_values.add((int(x), int(y)))
    assert (len(relation_values) == tuple_count)
    return relation_values


def parse_relations(relations_xml):
    """Creates relation objects"""
    relations = dict()
    for relation in relations_xml:
        name = relation.attrib['name']
        arity = int(relation.attrib['arity'])
        nb_tuples = int(relation.attrib['nbTuples'])
        semantics = relation.attrib['semantics']
        pairs = text_to_relation_pairs(relation.text, nb_tuples)
        relations[name] = Relation(name, arity, nb_tuples, semantics, pairs)
    return relations


def parse_predicates(predicates_xml):
    """Creates domain object"""
    predicates = dict()
    for predicate in predicates_xml:
        name = predicate.attrib['name']
        parameters = predicate.findall('parameters')[0].text
        function = predicate.findall('expression')[0].findall('functional')[0].text
        predicates[name] = Predicate(name, parameters, function)
    return predicates


def parse_constraints(constraints_xml, predicates, relations):
    """Creates constraint objects"""
    constraints = dict()
    for constraint in constraints_xml:
        name = constraint.attrib['name']
        arity = constraint.attrib['arity']
        variables = list(constraint.attrib['scope'].split(' '))
        reference = constraint.attrib['reference']
        parameters = constraint.findall('parameters')
        if len(parameters) > 0:
            parameters = parameters[0].text.split(' ')
        constraints[name] = Constraint(name, arity, variables, reference, parameters)
    return constraints


def update_variables(variables, constraints):
    """Updates all variables with their neighboring variables and constraints."""
    for constraint in constraints:
        scope = constraints[constraint].variables
        for var in scope:
            variables[var].add_constraint(constraint)
            variables[var].add_scope(scope)
    return variables


def make_functions(predicates):
    """Parses the predicate text into callable CustomFuction objects."""
    for pred_name in predicates:

        # Parses the predicate text into a list of arguments
        parameter_str = predicates[pred_name].parameter_str
        function_str = predicates[pred_name].function_str
        parameter_list = parameter_str.split(' ')
        arg_type = list()
        arg_names = list()
        for i in range(len(parameter_list) // 2):
            arg_type.append(parameter_list[2 * i])
            arg_names.append(parameter_list[2 * i + 1])
        predicates[pred_name].parameter_list = arg_names
        
        # Parses the predicate text into tokens
        steps_down = function_str.split('(')
        level_pointer = 0
        args_levels = []
        for i in range(len(steps_down)):
            steps_up = steps_down[i].split(')')
            level_pointer = level_pointer + 2
            for step in steps_up:
                level_pointer = level_pointer - 1
                args = step.split(',')
                for arg in args:
                    args_levels.append((arg, level_pointer))


        # Creates CustomFunction objects from known token values.
        param_names = []
        prev_level = 0
        custom_fuctions = []
        function_levels = dict()
        for args_level in args_levels:
            arg_name, level = args_level
            arg_name = arg_name.strip()
            if arg_name in function_names:
                cf = CustomFunction(arg_name)
                function_levels[level] = cf
                custom_fuctions.append(cf)
                if prev_level != 0:
                    if level > prev_level:
                        pcf = function_levels[prev_level]
                        pcf.args.append(cf)
                    elif level == prev_level:
                        pcf = function_levels[prev_level - 1]
                        pcf.args.append(cf)
            else:
                if arg_name != '':
                    param_names.append(arg_name)
                    if prev_level != 0:
                        if level > prev_level:
                            pcf = function_levels[prev_level]
                            pcf.args.append(arg_name)
                        elif level == prev_level:
                            pcf = function_levels[prev_level - 1]
                            pcf.args.append(arg_name)

            prev_level = level


        # Nests CustomFuctions in correct order
        for cf in custom_fuctions:
            cf_args = cf.args
            arg_names = []
            for cf_arg in cf_args:
                if type(cf_arg) == type(cf):
                    arg_names.append(cf_arg.name)
                else:
                    arg_names.append(cf_arg)
        
        # Assigns CustomFuction to appropriate predicate
        predicates[pred_name].custom_function = custom_fuctions[0]
    return predicates


def main(args):
    file_path = args.f
    tree = ElT.parse(file_path)
    root = tree.getroot()

    domains = parse_domains(root.findall('domains')[0])
    variables = parse_variables(root.findall('variables')[0])

    relations = dict()
    relations_xml_list = root.findall('relations')
    if len(relations_xml_list) >= 1:
        relations = parse_relations(relations_xml_list[0])

    predicates = dict()
    predicates_xml_list = root.findall('predicates')
    if len(predicates_xml_list) >= 1:
        predicates = make_functions(parse_predicates(predicates_xml_list[0]))
    constraints = parse_constraints(root.findall('constraints')[0], predicates, relations)

    variables = update_variables(variables, constraints)

    presentation = root.findall('presentation')[0]
    instance_name = presentation.attrib['name']
    instance = ProblemInstance(instance_name, variables, constraints, predicates, relations, domains)

    if args.pi:
        instance.print_info()
    return instance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates ProblemInstance object from XML file.')
    parser.add_argument('-f', metavar='file_path', help='file name for the CSP instance', nargs='?')
    parser.add_argument('--pi', metavar='print_info', help='print out the CSP instance', nargs='?', const=True, default=False)
    args = parser.parse_args()
    
    if args.f is not None:
        main(args)
    else:
        print('Error no file path given')
