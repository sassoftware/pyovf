#!/usr/bin/python

import os
import sys
import unittest

import bootstrap
from testrunner import testhelp
from testrunner import resources, testhandler

_setupPath = None

def setupPath(pathName):
    path = testhelp.getPath(pathName)
    os.environ[pathName] = path
    for p in path.split(':'):
        if not os.path.isdir(p):
            print '%s %s does not exist' % (pathName, path)
            sys.exit(1)
    testhelp.insertPath(path, updatePythonPath=True)


def setup():
    """
    Setup initializes variables must be initialized before the testsuite
    can be run.  Generally this means setting up and determining paths.
    """
    global _setupPath
    if _setupPath:
        return _setupPath

    path = setupPath('XOBJ_PATH')
    path = setupPath('PYOVF_PATH')

    from testrunner import testSetup
    testSetup.setup()

    from conary.lib import util
    sys.excepthook = util.genExcepthook(True, catchSIGUSR1=False)

    testhelp._conaryDir = resources.conaryDir
    _setupPath = True


def main(argv=None, individual=True):
    cfg = resources.cfg
    cfg.isIndividual = individual

    setup()

    cfg.cleanTestDirs = not individual
    cfg.coverageExclusions = ['scripts/.*', 'epdb.py', 'stackutil.py',
                              'test/.*']
    cfg.coverageDirs = [ os.environ['PYOVF_PATH'] ]

    if argv is None:
        argv = list(sys.argv)
    topdir = testhelp.getTestPath()
    if topdir not in sys.path:
        sys.path.insert(0, topdir)
    cwd = os.getcwd()
    if cwd != topdir and cwd not in sys.path:
        sys.path.insert(0, cwd)

    from conary.lib import util
    from conary.lib import coveragehook
    sys.excepthook = util.genExcepthook(True, catchSIGUSR1=False)

    handler = testhandler.TestSuiteHandler(cfg, resources)
    print "This process PID:", os.getpid()
    results = handler.main(argv)
    if results is None:
        sys.exit(0)
    sys.exit(not results.wasSuccessful())


if __name__ == '__main__':
    main(sys.argv, individual=False)
