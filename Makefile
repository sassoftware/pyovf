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

SUBDIRS = pyovf test


build: default-build

install: default-install

clean: default-clean

test: default-test

dist: archive

archive:
	hg archive --exclude .hgignore -t tbz2 pyovf-`hg id -i`.tar.bz2

export TOPDIR=$(shell pwd)
include $(TOPDIR)/Make.rules
include $(TOPDIR)/Make.defs
