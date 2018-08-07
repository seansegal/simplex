import numpy as np


class TwoPhaseSimplex:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, model):
        ''' Solves a simplex instance. '''

        table, artificial_vars, bfs = model._get_table_with_artifical_vars()
        n, m = table.shape

        # Phase 1 (Only if we have artificial variables)
        if len(artificial_vars) != 0:
            is_feasible, table_vals  = self._phase1(table, artificial_vars, bfs)
            table, bfs = table_vals
            if not is_feasible:
                return 'Infeasible', None, None

            # Remove artificial variables
            table = np.column_stack((table[:, 0:m-len(artificial_vars) - 1], table[:, -1]))


        # Phase 2
        table, obj, bfs, bounded = self._phase2(table, model.c, bfs)
        if bounded:
            num_vars = table.shape[1] - 1
            x = np.zeros(num_vars)
            for i, coord in enumerate(bfs):
                row, col = coord
                x[col] = table[row, -1]
            return 'Solved', obj[-1], x
        else:
            return 'Unbounded', None, None


    def _phase2(self, table, c, bfs):
        '''
            Phase 2 of the Two-Phase simplex algorithm. Assumes the table
            is starting at a BFS.
        '''
        if self.verbose:
            print('-------- PHASE 2 -----------')

        n, m = table.shape
        obj = self._calc_obj(table, c, bfs)
        table, obj, bfs, bounded = self._simplex(table, obj, bfs)
        return table, obj, bfs, bounded


    def _phase1(self, table, artificial_vars, bfs):
        '''
            Phase 1 of the Two-Phase Simplex Algorithm
        '''
        if self.verbose:
            print('-------- PHASE 1 -----------')
        n, m = table.shape

        # Create the objective function
        c = np.zeros(m - 1)
        artificial_cols = list(map(lambda x: x[1], artificial_vars))
        c[artificial_cols] = -1 #TODO: should be negative 1
        obj = self._calc_obj(table, c, bfs)
        table, obj, bfs, bounded = self._simplex(table, obj, bfs)

        # If the objective value is close enough to 0, it is feasible.
        if np.isclose(obj[-1], 0):
            return True, (table, bfs)
        else:
            return False, (None, None)

    def _simplex(self, table, obj, bfs):
        '''
            The simplex algorithm. Takes a bfs as input. Uses Bland's rule to
            avoid cycling. Should only take in feasible problems.
        '''

        while True:
            if self.verbose:
                print('------ TABLE --------')
                print(obj)
                print(table)

            # Find the variable to enter the basis. Using Bland's Rule (select the first)
            negatives = np.where(obj[:-1] < 0)[0]
            if len(negatives) == 0:
                break

            new_basis = negatives[0]

            # Find the variable to leave the basis. Using Bland's Rule (argmin automatically chooses the first in cases of ties.)
            row = -1
            min_cost = float('Inf')
            for i in range(table.shape[0]):
                if table[i, new_basis] > 0:
                    cost = table[i, -1]/table[i, new_basis]
                    if cost < min_cost:
                        row = i
                        min_cost = cost

            if row == -1:
                return table, obj, bfs, False

            to_leave = list(filter(lambda x: x[0] == row, bfs))
            table, obj = self._pivot(table, obj, row, new_basis)
            assert len(to_leave) == 1
            bfs.remove(to_leave[0])
            bfs.append((row, new_basis))
            if self.verbose:
                    print('Removing', to_leave[0], 'Adding', new_basis)

        return table, obj, bfs, True

    def _calc_obj(self, table, c, bfs):
        n, m = table.shape
        obj = np.append(c, 0)
        for coord in bfs:
            row, col = coord
            obj = obj - obj[col]*table[row, :]
        obj = -1*obj # TODO
        return obj

    def _pivot(self, table, obj, row, column):

        # Row Reduction
        table[row, :] = table[row, :]/table[row, column]
        rows, cols = table.shape
        for r in range(rows):
            if r != row:
                table[r, :] = table[r, :] - table[r, column]*table[row, :]
                obj = obj - obj[column]*table[row, :]

        return table, obj
