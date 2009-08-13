#!/usr/bin/python

import os
import sys
import unittest
import bootstrap

_setupPath = None
_individual = False

def isIndividual():
    global _individual
    return _individual

from testrunner import pathManager

def setup():
    """
    Setup initializes variables must be initialized before the testsuite
    can be run.  Generally this means setting up and determining paths.
    """
    global _setupPath
    if _setupPath:
        return _setupPath

    pathManager.addExecPath('CONARY_PATH')
    pathManager.addExecPath('XOBJ_PATH')
    pathManager.addExecPath('PYOVF_PATH')
    pyovfTestPath = pathManager.addExecPath('PYOVF_TEST_PATH')
    pathManager.addExecPath('TEST_PATH',path=pyovfTestPath)

    from conary.lib import util
    sys.excepthook = util.genExcepthook(True, catchSIGUSR1=False)

    _setupPath = True





def main(argv=None, individual=True):
    global _individual
    _individual = individual

    setup()

    from conary.lib import util
    from conary.lib import coveragehook
    sys.excepthook = util.genExcepthook(True, catchSIGUSR1=False)

    from testrunner import testhandler,testhelp
    def getCoverageDirs():
        return [ pathManager.getPath('PYOVF_PATH') ]

    def getCoverageExclusions():
        return ['scripts/.*', 'epdb.py', 'stackutil.py',
                'test/.*']
    def sortTests(tests):
        order = {'smoketest': 0, 
                 'unit_test' :1,
                 'functionaltest':2}
        maxNum = len(order)
        tests = [ (test, test.index('test')) for test in tests]
        tests = sorted((order.get(test[:index+4], maxNum), test)
                       for (test, index) in tests)
        tests = [ x[1] for x in tests ]
        return tests
    handlerClass = testhelp.getHandlerClass(testhelp.ConaryTestSuite,
                                            getCoverageDirs,
                                            getCoverageExclusions,
                                            sortTests)
    handler = handlerClass(individual=individual, topdir=pathManager.getPath('PYOVF_TEST_PATH'),
                           testPath=pathManager.getPath('PYOVF_TEST_PATH'),
                           conaryDir=pathManager.getPath('CONARY_PATH'))

    print "This process PID:", os.getpid()

    if argv is None:
        argv = list(sys.argv)
    results = handler.main(argv)
    if results is None:
        sys.exit(0)
    sys.exit(not results.wasSuccessful())


if __name__ == '__main__':
    main(sys.argv, individual=False)
