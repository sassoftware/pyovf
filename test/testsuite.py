#!/usr/bin/python
#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


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
