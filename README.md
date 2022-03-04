# constraint-parser
Python parser for XML Representation of Constraint Networks Format XCSP 2.1

## Files

### problem_parser.py
This is the main parser file, it handels most of the conversion from XML into objects. It will return a `ProblemInstance` object with fields `name`, `variables`, `constraints`, `predicates`, `relations`, and `domains`. This can parse enumerated and intension constraints.

### intension_parser.py
This is a standalone file which contains all of the object classes and preset functions for creating `CustomFunction` objects. These objects are parsed and created in `make_functions(predicates)` in `problem_parser.py`. All of the functions listed in [XML Representation of Constraint Networks
Format XCSP 2.1](https://arxiv.org/pdf/0902.2362v1.pdf) must be hard coded and their associated name included in `function_names`. The `evaluate(self, val_dict)` fuction recursively computes the value of this fuction by paring the `CustomFunction` arguments with the arguments in the val_dict and passing the `val_dict` to nested functions.

### incomplete_ac_solver.py
This file is given as an example for how to call `problem_parser.py` and how to filter the domains with by enforcing node consistency. An important function in this file is `evalueate_vvd(vvd)`. This function is essential for determining if a pair of Variable Value Pairs are consistent. This checks the domains in the `ProblemInstance` for enumerated constraints and makes a call to the predicate's `CustomFuction` for intension constraints.

To run an example where node consistency filters a domain with an intension constratin use:

`python incomplete_ac_solver.py -f csp-benchmarks\12_zebra-intension-nonbinary.xml`



### csp_benchmarks
This file constains many of the XML files used for testing this parser. It should be able to parse all of these files into `ProblemInstance` objects.
