import numpy as np

def convert_to_dual(var_signs, A, directions, bvals, max_or_min, cvals):

    directions_dual = []
    for var_sign in var_signs:
        if max_or_min == 'max':
            directions_dual.append(var_sign)
        else:
            if var_sign == '>':
                directions_dual.append('<')
            elif var_sign == '<':
                directions_dual.append('>')
            elif var_sign == '=':
                directions_dual.append('=')

    var_signs_dual = []
    for direction in directions:
        if max_or_min == 'max':
            if direction == '>':
                var_signs_dual.append('<')
            elif direction == '<':
                var_signs_dual.append('>')
            elif direction == '=':
                var_signs_dual.append('=')
        else:
            var_signs_dual.append(direction)
            
    max_or_min_dual = 'max' if max_or_min == 'min' else 'min'
    return var_signs_dual, A.T, directions_dual, cvals, max_or_min_dual, bvals
