#
# Copyright (c) 2008 rPath, Inc.
#
# This program is distributed under the terms of the MIT License as found 
# in a file called LICENSE. If it is not present, the license
# is always available at http://www.opensource.org/licenses/mit-license.php.
#
# This program is distributed in the hope that it will be useful, but
# without any waranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the MIT License for full details.
#

python_files = $(wildcard *.py)
override PYDEST = /xobj


build: default-build python-build

install: default-install python-install

clean: default-clean python-clean

test: default-test python-test


export TOPDIR=$(shell pwd)/..
include $(TOPDIR)/Make.rules
include $(TOPDIR)/Make.defs
