# runner.py
# 03-04-2021
# This file is for processing some .txt file and convert them to the string type.
# Also, it includes all static functions that other scripts may need.
#
# https://github.com/Yebulabula/String-Sanitization-Project
#
# Author Ye Mao
# King's College London
# Version 1.0


import time
import sys
from optparse import OptionParser
from model import solver
import warnings
import DataProcessing


def default(str):
    """
        The function to return default help message.
    """
    return str + ' [Default: %default]'


def readCommand(argv):
    usageStr = """
    USAGE:      python runner.py <options>
    EXAMPLES:   (1) python runner.py
                    - starts deletion strategy test case
                (2) python runner.py -m 2000
                    - select best deleted symbol by 2000 iterations. 
    """

    parser = OptionParser(usageStr)
    parser.add_option('-w', '--originalFile', dest='w_filename', type='string',
                      help=default('The string for sanitization(W)'), default='test/test_w.txt')
    parser.add_option('-z', '--sanitizedFile', dest='z_filename', type='string',
                      help=default('The string for sanitization(Z)'), default='test/test_z.txt')
    parser.add_option('-t', '--tau', dest='tau', type='int',
                      help=default('The tau value to identify spurious pattern'), default=1)
    parser.add_option('-o', '--omega', dest='omega', type='float',
                      help=default('The weight of non-spurious pattern'), default=1)
    parser.add_option('-s', '--sensitivePatterns', dest='sensitive_pat', type='string',
                      help=default('A file that consists of all sensitive patterns in W'),
                      default='test/sen_pattern_test.txt')

    parser.add_option('-k', dest='k', type='int',
                      help=default('The length of each pattern'), default=4)
    parser.add_option('-c', dest='c', type='int',
                      help=default('The exploration parameter for UCB1 formula'), default=20)
    parser.add_option('-d', '--delta', dest='delta', type='int',
                      help=default('The number of deletions'), default=5)
    parser.add_option('-e', '--E', dest='tolerance', type='int',
                      help=default('The pruning parameter for ELLS-ALGO'), default=10)
    parser.add_option('-m', '--max', dest='max_simulations', type='int',
                      help=default('The number of iterations per selection in ELLS-ALGO'), default=3)

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    args['w'] = DataProcessing.readFile(options.w_filename)
    args['k'] = options.k
    args['delta'] = options.delta
    args['z'] = DataProcessing.readFile(options.z_filename)
    args['sensitive_patterns'] = DataProcessing.readMultiLineFile(options.sensitive_pat)
    if args['sensitive_patterns'] is None: raise Exception(
        "The file " + options.w_filename + " cannot be found")
    args['tau'] = options.tau
    args['omega'] = options.omega
    args['c'] = options.c
    args['max_simulations'] = options.max_simulations
    args['tolerance'] = options.tolerance

    return args


if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    solver = solver(**args)

    d_baseline = solver._get_distortion(solver.baseline())
    sp, nsp = solver._get_distortion(solver.Z)
    print('Baseline Distortion Reduction\nSpurious:', sp - d_baseline[0], 'non-spurious:', nsp - d_baseline[1])
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    tick = time.time()
    print('---------------------------')
    d_csd_plus = solver._get_distortion(solver.run())
    tock = time.time()
    print('CSD-PLUS Distortion Reduction\nSpurious:', sp - d_csd_plus[0], 'non-spurious:', nsp - d_csd_plus[1])
    print('Time consumption in CSD-Plus is', tock - tick)

    # solver._exhaustive_search(lst=list(range(len(solver.Z))), n=solver.delta)
    # print('Exhaustive Search:', min(solver.EX))
