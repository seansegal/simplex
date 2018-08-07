# Simplex Solver
Solves Linear Programs in Python using the Simplex Method.

### Dependencies
This program is written in Python 3 and uses NumPy.

### Command Line Interface
The program can be run by executing the following line in a terminal:
`./runMyLPSolver <command> x_FILEPATH A_FILEPATH b_FILEPATH c_FILEPATH [--verbose]`

where `<command>` can be one of the following:
* `dual` which outputs the dual of the given LP
* `solve` which solves the given LP.

and
* `x_FILEPATH` is the path to a file which defines the domains of each variable in the LP. It should be a file with a single line of tab separated sign constraints for the variables of the LP. In the file, `<` specifies that the variable is less than or equal to 0, `>` specifies that the variables is greater than or equal to 0 and `=` specifies that the variable is unconstrained.
* `A_FILEPATH` is the path to a file with the coefficients of the constraints. Each line represents a single constraint. Each line should contain tab-separated signed coefficients on each variable in the LP.
* `b_FILEPATH` is the path to the file with the right hand side of the constraints. Each line represents a single constraint. Each line should contain two values that should be separated by a single tab. The first value is the direction of the constraint (`>`, `<` or `=`). The second value should be the signed constant on the RHS of the constraint.
* `c_FILEPATH` is the path to a file which defines the objective function of the LP. There should be a single line which begins with either `max` or `min` followed by signed coefficients on each of the variables in the objective function.
(*Note:* Please see the `tests` folder for examples of each of the files.)

When run with the `--verbose` flag, the program will output for detailed error messages in the case of malformed input filed or invalid LPs. The program will also print out the table of the Simplex algorithm at each iteration.

#### CLI Program Output
The `dual` command will output the corresponding dual of the LP given as input. The LP will be in the same form as the input (The program will print each of the 4 input files required.)

The `solve` command will output either a single line or two lines of output depending on the given LP. If the LP is unbounded or infeasible, there will be a message indicating that this is the case. Otherwise, if the LP is feasible and unbounded the first line of output will contain the objective value at the optimal solution and the second will contain the values of each of the variables separated by tabs.

### Tests
Tests are located in the `tests` directory. The expected outputs are located in
the `testouts` directory.

For tests 1-16, odd numbered tests are the original tests and the even numbered tests are their duals.

Description of tests:
* Test 1 is an unbounded LP. Test 2 is the dual LP of Test 1 (infeasible).
* Test 3 is an infeasible LP. Test 4 is its dual (unbounded)
* Test 5 is the LP found this in [example](http://optlab.mcmaster.ca/feng/4O03/Two.Phase.Simplex.pdf). Test 6 is its dual.
* Test 7 is a LP that is unbounded. Test 8 is its dual.
* Test 9 is a situation in which degeneracy could cause cycling if Bland's rule was not properly implemented. Test 10 is its dual.
* Test 13 has multiple optimal solutions and we ensure that one is deterministically returned. Test 14 is its dual.
* Test 15 has all negative b values. Test 16 is its dual.

There is a `runtests` script which runs all tests and checks if `stdout` matches the files provided in `testouts`.

* Tests 16-19 test invalid and malformed LPs.
* Test 20 checks for that the program detects linearly dependent constraints.

### Checking Linearly Dependent Constraints
The program will check all LPs converted to standard for before solving to see if the
rows of the A matrix are linearly independent.
