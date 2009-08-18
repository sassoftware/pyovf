#!/usr/bin/python

import os
import sys
import unittest

import bootstrap

from testrunner import pathManager, testhelp


EXCLUDED_PATHS = ['scripts/.*', 'test/.*']


def setup():
    pathManager.addExecPath('XOBJ_PATH')
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    pathManager.addExecPath('PYOVF_PATH', path)
    pathManager.addResourcePath('TEST_PATH', path + '/test')


def main(argv=None, individual=True):
    if argv is None:
        argv = list(sys.argv)

    from conary.lib import coveragehook

    handlerClass = testhelp.getHandlerClass(testhelp.ConaryTestSuite,
            lambda handler, environ: os.getenv('PYOVF_PATH') + '/pyovf',
            lambda handler, environ: EXCLUDED_PATHS)

    handler = handlerClass(individual=individual)
    results = handler.main(argv)
    return results.getExitCode()


if __name__ == '__main__':
    setup()
    sys.exit(main(sys.argv, individual=False))
