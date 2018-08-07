import sys
import numpy as np
import os

from FileParser import FileParser
from StandardFormLP import StandardFormLP
from dual import convert_to_dual
from FileWriter import FileWriter
from TwoPhaseSimplex import TwoPhaseSimplex

def convert_to_signed_string(num):
    ''' Converts a floating point number to a signed string. '''
    string = '+' if num >= 0 else ''
    return string + str(num)

def check_valid_lp(var_signs, A, directions, bvals, max_or_min, cvals, verbose):
    '''
        Checks if an LP is valid. By valid we mean that the number constraints
        and variables match in all four files.
    '''
    num_constraints, num_vars = A.shape
    if len(var_signs) != num_vars:
        return False, 'Number of variables in A and x file do not match.'

    if len(directions) != num_constraints or len(bvals) != num_constraints:
        return False, 'Number of constraints in A and b do not match.'

    if len(cvals) != num_vars:
        return False, 'Number of variables in A and c file do not match.'
    return True, ''

def check_if_file_exits(file):
    '''
        Checks if a file exists. Prints an error and exits if it does not exist.
    '''
    if not os.path.exists(file):
        print('File \'{}\' does not exist'.format(file))
        exit()

def parse_files(parser):
    # Check if the files exist.
    for f in [x_file, a_file, b_file, c_file]:
        check_if_file_exits(f)

    # Parse the files.
    try:
        signs = parser.parseXFile(x_file)
        A = parser.parseAFile(a_file)
        directions, bvals = parser.parseBFile(b_file)
        max_or_min, cvals = parser.parseCFile(c_file)
        return signs, A, directions, bvals, max_or_min, cvals
    except Exception as e:
        if verbose:
            # Verbose messages may include a reason why the file is malformed.
            exit_with_message(str(e))
        else:
            exit_with_message('Malformed input file. Exiting.')

def exit_with_message(msg, exitcode=0):
    ''' Prints a message and exits. '''
    print(msg)
    exit(exitcode)

if __name__ == '__main__':



    # Check and parse arguments
    if len(sys.argv) == 7 and sys.argv[6] == '--verbose':
        verbose = True

        # It's useful to have a greater linewidth for verbose printing.
        np.set_printoptions(linewidth=200)
        _, command, x_file, a_file, b_file, c_file, _ = sys.argv
    elif len(sys.argv) == 6:
        verbose = False
        _, command, x_file, a_file, b_file, c_file = sys.argv
    else:
        print('Incorrect Number of Arguments.')
        exit_with_message('Usage: ./runMyLPSolver <command> x_FILEPATH A_FILEPATH b_FILEPATH c_FILEPATH')

    # Parse Files
    parser = FileParser()
    var_signs, A, directions, bvals, max_or_min, cvals = parse_files(parser)

    # Check if the LP is valid.
    valid, msg = check_valid_lp(var_signs, A, directions, bvals, max_or_min, cvals, verbose)
    if not valid:
        err_msg = msg if verbose else 'Invalid LP. Exiting.'
        exit_with_message(err_msg)

    # TODO(optional): Check if constraints are linearly indepdent. Should be pretty easy with NumPy.

    if command == 'dual':
        d_var_signs, d_A, d_directions, d_bvals, d_max_or_min, d_cvals = convert_to_dual(var_signs, A, directions, bvals, max_or_min, cvals)
        writer = FileWriter()
        # Prints model to stdout.
        writer.write_model_to_file(d_var_signs, d_A, d_directions, d_bvals, d_max_or_min, d_cvals)
    elif command == 'solve':
        model = StandardFormLP(var_signs, A, directions, bvals, max_or_min, cvals)
        if model.are_dependent_constraints():
            print('Dependent constraints. Exiting.')
            exit()
        solver = TwoPhaseSimplex(verbose=verbose)
        solution, obj, x = solver.solve(model)
        if solution == 'Infeasible':
            print('Infeasible problem. Exiting.')
        elif solution == 'Unbounded':
            print('Unbounded problem. Exiting.')
        elif solution == 'Solved':
            print(convert_to_signed_string(model.convert_objective(obj)))
            print('\t'.join(list(map(convert_to_signed_string, model.convert_variables(x)))))
        else:
            # Solutions should be either Infeasible, Unbounded or Solved.
            assert False
    else:
        exit_with_message('Unknown command. Exiting.')
