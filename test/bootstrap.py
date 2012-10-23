#
# Copyright (c) rPath, Inc.
#
# This program is distributed under the terms of the MIT License as found 
# in a file called LICENSE. If it is not present, the license
# is always available at http://www.opensource.org/licenses/mit-license.php.
#
# This program is distributed in the hope that it will be useful, but
# without any waranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the MIT License for full details.

import os
import sys

testUtilDir = os.environ.get('TESTUTILS_PATH', '../testutils')
if os.path.exists(testUtilDir):
    sys.path.insert(0, testUtilDir)

try:
    import testrunner
except ImportError:
    raise RuntimeError('Could not find testrunner - set TESTUTILS_PATH')
