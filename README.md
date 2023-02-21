# constraint-parser

Python parser for XML Representation of Constraint Networks Format XCSP 2.1

## Files

### problem_parser.py

<span style="color:red">**Edit at your own risk.**</span>

This is the main parser file, it handles most of the conversion from XML into objects. It will return a `ProblemInstance` object with fields `name`, `variables`, `constraints`, `predicates`, `relations`, and `domains`. This can parse enumerated and intension constraints. The structure of the `ProblemInstance` object can be changed, but this may have consequences for how `evaluate_vvd()` is evaluated. The current design may be slow, but is functional.

### intension_parser.py

<span style="color:red">**Do not edit.**</span>

This file was tested on all the benchmark files in `csp-benchmarks` and can parse all the files into the appropriate structure. If you wish to change the structure fo the `ProblemInstance` object change it in `problem_parser.py`

This is a standalone file which contains all of the object classes and preset functions for creating `CustomFunction` objects. These objects are parsed and created in `make_functions(predicates)` in `problem_parser.py`. All of the functions listed in [XML Representation of Constraint Networks
Format XCSP 2.1](https://arxiv.org/pdf/0902.2362v1.pdf) must be hard coded and their associated name included in `function_names`. The `evaluate(self, val_dict)` fuction recursively computes the value of this fuction by paring the `CustomFunction` arguments with the arguments in the val_dict and passing the `val_dict` to nested functions.

In `incomplete_ac_solver.py` the function `evaluate_vvd` has two parts. The first option checks if `reference_name` is in `ProblemObject.relations`. Relations can be checked by comparing the values in the variable value pair to the allowed pairs in the `ProblemObject`. The second option checks if `reference_name` is in `ProblemObject.predicates`. This evaluates the custom function defined by an intension relation which was generated in `intension_parser.py`.

### incomplete_ac_solver.py

This file is given as an example for how to call `problem_parser.py` and how to filter the domains with by enforcing node consistency. An important function in this file is `evaluate_vvd(vvd)`. This function is essential for determining if a pair of Variable Value Pairs are consistent. This checks the domains in the `ProblemInstance` for enumerated constraints and makes a call to the predicate's `CustomFuction` for intension constraints. If the structure of `ProblemInstance` is not altered then `evaluate_vvd(vvd)` should work as expected.

The most straightforward way to interact with the `ProblemInstance` is to use the `check(var1_name, val_1, var2_name, val_2)` function. This returns true if `val_2` of `var2_name` supports `val_1` in `var1_name`. If it is not supported then `val_1` should be removed from the domain of variable `var1_name`. This does not check if `val_1` in `var1_name` supports `val_2` of `var2_name`. This function assumes that `val_1` and `val_2` are within the appropriate domains of their respective variables so it may return true if values outside of the domains are entered if they statisfy the conditions.

Included are some functions with `TODOs` which outline the general structure used for this project. The use of a dynamically assigned functions such as `ac_strategy()`makes the structure of  `main` simpler and can be expanded when more functions are needed to determine assignment and backtracking.

```python
        if args.a == 'ac3':
            ac_strategy = ac_3
```

The code above is an example of how to dynamically assign a function. In this case if `-a ac3` is entered as a flag, then the `ac_strategy` will be set to the `ac_3()` function.

### csp_benchmarks

This file constains many of the XML files used for testing this parser. It should be able to parse all of these files into `ProblemInstance` objects.

## Examples

### Problem Parser

The user can call the problem_parser with a file path to a `.xml` file. The flag `-f` is expected before the file path. The flag `--pi` will print out the `ProblemInstance` object.

#### Problem Parser Input

`$python problem_parser.py -f csp-benchmarks\01_chain4-conflicts.xml --pi`

#### Problem Parser Output

```python
Instance name: orderchain
Variables:
Name: V1, initial-domain: {1, 2, 3, 4},                 constraints: {'C0'}, neighbors: {'V2'}
Name: V2, initial-domain: {1, 2, 3, 4},                 constraints: {'C0', 'C1'}, neighbors: {'V1', 'V3'}
Name: V3, initial-domain: {1, 2, 3, 4},                 constraints: {'C2', 'C1'}, neighbors: {'V2', 'V4'}
Name: V4, initial-domain: {1, 2, 3, 4},                 constraints: {'C2'}, neighbors: {'V3'}
Constraints:
Name: C0, variables: ['V1', 'V2'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}
Name: C1, variables: ['V2', 'V3'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}
Name: C2, variables: ['V3', 'V4'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}

```

### Solver

In general, a user should only need to call the solver. Expanding the functionality of the solver should happen within `solver.py` and should not require editing the problem parser or the intension parser.

#### Solver Output default

`$python incomplete_ac_solver.py -f csp-benchmarks\01_chain4-conflicts.xml`

```txt
Instance name: orderchain
time-setup: 0.0
cc: 0
cpu: 0.0
fVal: 0
iSize: 5.545177444479562
fSize: 5.545177444479562
fEffect: 0.0
```

#### Solver Output with `--pi`

`$python incomplete_ac_solver.py -f csp-benchmarks\01_chain4-conflicts.xml --pi`

```python
Instance name: orderchain
Variables:
Name: V1, initial-domain: {1, 2, 3, 4},                 constraints: {'C0'}, neighbors: {'V2'}
Name: V2, initial-domain: {1, 2, 3, 4},                 constraints: {'C1', 'C0'}, neighbors: {'V1', 'V3'}
Name: V3, initial-domain: {1, 2, 3, 4},                 constraints: {'C1', 'C2'}, neighbors: {'V4', 'V2'}
Name: V4, initial-domain: {1, 2, 3, 4},                 constraints: {'C2'}, neighbors: {'V3'}
Constraints:
Name: C0, variables: ['V1', 'V2'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}
Name: C1, variables: ['V2', 'V3'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}
Name: C2, variables: ['V3', 'V4'], definition: conflicts {(4, 4), (2, 4), (1, 2), (3, 4), (1, 1), (1, 4), (2, 3), (3, 3), (2, 2), (1, 3)}

Instance name: orderchain
time-setup: 0.0031003952026367188
cc: 0
cpu: 0.0
fVal: 0
iSize: 5.545177444479562
fSize: 5.545177444479562
fEffect: 0.0
```

#### Solver Output with `--csv`

`$python incomplete_ac_solver.py -f csp-benchmarks\01_chain4-conflicts.xml --csv`

```txt
01_chain4-conflicts.xml, None, orderchain, 0, 0.0, 0, 5.545177444479562, 5.545177444479562, 0.0
```
