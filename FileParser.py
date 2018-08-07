import numpy as np

class FileParser(object):
    '''Parses files according to the project format.'''

    def __init__(self, delimiter='\t'):
        super(FileParser, self).__init__()
        self.delim = delimiter

    def parseAFile(self, filepath):
        ''' Parses the A file. Throws an Exception if the file is not formatted properly. '''
        with open(filepath, 'r') as f:
            lines = f.readlines()
            m = len(lines)
            if m == 0:
                raise ValueError('Empty A file found.')
            n = len(list(filter(lambda x: x.strip() != '', lines[0].split(self.delim))))
            A = np.zeros([m, n], dtype=np.float32)
            for i, line in enumerate(lines):
                vals = list(filter(lambda x: x.strip() != '', line.strip().split(self.delim)))
                A[i, :] = np.array(vals, dtype=np.float64)
            return A

    def parseXFile(self, filepath):
        ''' Parses the x file. Throws an Exception if the file is not formatted properly. '''
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                raise ValueError('Empty X file.')
            signs = lines[0].strip().split(self.delim)
            for sign in signs:
                if sign != '>' and sign != '<' and sign != '=':
                    raise ValueError('Poorly formed X file. Sign that is not <, > or = found.')
            return signs

    def parseBFile(self, filepath):
        ''' Parses the b file. Throws an Exception if the file is not formatted properly. '''
        with open(filepath, 'r') as f:
            lines = f.readlines()
            directions, bvals = [], np.zeros(len(lines), dtype=np.float64)
            for i, line in enumerate(lines):
                vals = line.strip().split(self.delim)
                if len(vals) != 2:
                    raise ValueError('Poorly formed B file. Should have exactly 2 columns.')
                directions.append(vals[0])
                bvals[i] = float(vals[1])
            return directions, bvals

    def parseCFile(self, filepath):
        ''' Parses the c file. Throws an Exception if the file is not formatted properly. '''
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2: # We use less than in case there are whitespace lines.
                raise ValueError('Poorly formed C file. Should have 2 lines.')
            opt = lines[0].strip()
            if opt != 'max' and opt != 'min':
                raise ValueError('Poorly formed C file. First line is not max or min.')

            # NOTE: This will throw an exception if they cannot be turned into floats,
            #  but that is okay since we catch the exception. 
            return opt, np.array(lines[1].split(self.delim), dtype=np.float64)
