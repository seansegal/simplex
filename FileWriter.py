import numpy as np

class FileWriter(object):
    '''Writes files accoding to model files. '''

    def __init__(self, delimiter='\t'):
        super(FileWriter, self).__init__()
        self.delim = delimiter

    def write_model_to_file(self, var_signs, A, directions, bvals, max_or_min, cvals, filename=None):
        ''' Writes a model to a file. If filename is None, it prints to stdout. 
        '''
        x_file = self._get_x_string(var_signs)
        A_file = self._get_A_string(A)
        b_file = self._get_b_string(directions, bvals)
        c_file = self._get_c_string(max_or_min, cvals)
        file_str = '### x_file ###\n{0}### A_file ###\n{1}### b_file ###\n{2}### c_file ###\n{3}'.format(x_file, A_file, b_file, c_file)
        if filename is None:
            print(file_str)
        else:
            with open(filename, 'w') as f:
                f.write(file_str)

    def _get_x_string(self, var_signs):
        string = ''
        for sign in var_signs:
            string += sign + self.delim
        string.strip()
        string += '\n'
        return string

    def _get_A_string(self, A):
        string = ''
        n, m = A.shape
        for i in range(n):
            for j in range(m):
                val = A[i,j]
                if val >= 0:
                    string += '+'
                string += str(val) + self.delim
            string += '\n'
        return string

    def _get_b_string(self, directions, bvals):
        assert len(directions) == len(bvals)
        string = ''
        for i in range(len(directions)):
            plus = '+' if bvals[i] >= 0 else ""
            string += '{0}\t{1}{2}\n'.format(directions[i], plus, str(bvals[i]))
        return string


    def _get_c_string(self, max_or_min, cvals):
        string = max_or_min + '\n'
        for val in cvals:
            plus = '+' if val >= 0 else ""
            string += (plus + str(val) + '\t')
        return string
