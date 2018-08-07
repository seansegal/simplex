import numpy as np

class StandardFormLP(object):

    def __init__(self, signs, A, directions, bvals, max_or_min, cvals, standard_obj='max'):
         '''
            Constructs a StandardFormLP from a Generic LP.

            Standard LP has the form:
                max c^T x (can also be min, if standard_obj='min')
                s.t. Ax = b
                x >= 0
         '''
         assert max_or_min == 'max' or max_or_min == 'min'

         # Variables to transform a solution back to the original form.
         self.original_objective = max_or_min
         self.vars = {i: str(i) for i in range(A.shape[1])}
         self.standard_obj = standard_obj
         self.slacks = []

         # Variables of a Standard Form LP.
         self.A = A
         self.b = bvals
         self.c = cvals if max_or_min == standard_obj else -1*cvals
         self._fix_var_domains(signs)
         self._add_slack_vars(directions)


    def _fix_var_domains(self, signs):
        '''
            Alters the A and c matrix so that all variables have domain x >= 0.
        '''
        for i, sign in enumerate(signs):
                if sign == '<':
                    self.c[i] *= -1
                    self.A[:, i] *= -1
                    self.vars[i] = '-' + self.vars[i]
                elif sign == '=':
                    self.c = np.append(self.c, -1*self.c[i])
                    self.A = np.append(self.A, np.array([-1*self.A[:, i]]).T, 1)
                    self.vars[i] = self.vars[i] + '-' + str(self.A.shape[1] - 1)

    def _add_slack_vars(self, directions):
        '''
            Adds slack variables to transform inequalities to equalities.
        '''
        for i, dir in enumerate(directions):
            rows = self.A.shape[0]
            if dir == '>':
                self.A = np.append(self.A, -1*np.zeros(shape=[rows, 1]), 1)
                self.A[i, -1] = -1
                self.c = np.append(self.c, 0)
                self.slacks.append(self.A.shape[1] - 1)
            elif dir == '<':
                self.A = np.append(self.A, 1*np.zeros(shape=[rows, 1]), 1)
                self.A[i, -1] = 1
                self.c = np.append(self.c, 0)
                self.slacks.append(self.A.shape[1] - 1)

    def _get_table_with_artifical_vars(self):
        '''
            Generates a table for Phase 1 of the simplex algorithm. Adds artificial
            variables as needed.
        '''
        artificials = []
        bfs = []
        new_b = np.array(self.b)
        rows, cols = self.A.shape
        num_artificial = min(rows, cols)
        table = np.array(self.A)
        for row, col in enumerate(self.slacks):
            if table[row, col] == -1 and new_b[row] < 0:
                table[row] = -1*table[row]
                new_b[row] = -1*new_b[row]
                num_artificial -= 1
                bfs.append((row, col))
            elif table[row, col] == 1 and new_b[row] > 0:
                bfs.append((row, col))
                num_artificial -= 1


        table = np.append(table, np.zeros(shape=[rows, num_artificial]), 1)

        # Add artificial variables
        rows, cols = table.shape
        bfs_rows = set(map(lambda x: x[0], bfs))
        artificial_val = 0
        for i in range(rows):
            if i in bfs_rows:
                continue
            artificials.append((i, cols -num_artificial + artificial_val))
            bfs.append((i, cols -num_artificial + artificial_val))
            if table[i, -1] < 0:
                table[i, :] = -1*table[i, :]
            table[i, cols -num_artificial + artificial_val] = 1
            artificial_val +=1

        return np.column_stack((table, new_b)), artificials, bfs

    def are_dependent_constraints(self):
        n, m = self.A.shape
        if n <= m and n != np.linalg.matrix_rank(self.A):
            return True
        return False

    def convert_variables(self, x):
        '''Given a solution to the standard LP x, return the values of the original variables'''
        assert len(x) == self.A.shape[1]
        ans = np.zeros(len(self.vars))
        for i in range(len(self.vars)):
            standard_vars = self.vars[i].split('-')
            if standard_vars[0] != '':
                ans[i] += x[int(standard_vars[0])]
            if len(standard_vars) > 1:
                ans[i] -= x[int(standard_vars[1])]
        assert len(ans) == len(self.vars)
        return ans

    def convert_objective(self, obj):
        '''Given an objective value to the standard LP obj, return the values'''
        return obj if self.original_objective == self.standard_obj else -1*obj
