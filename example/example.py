#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2014 Steve Milner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
Example
"""

from __future__ import print_statement

# Make a logger
import logging
logger = logging.getLogger('flagon')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(name)s - %(levelname)s - %(msg)s'))
logger.handlers.append(handler)
logger.setLevel(logging.DEBUG)

# --- FLAGON SPECIFIC CODE ---
from flagon.backends.jsonfile import JSONFileBackend
# Make a backend
backend = JSONFileBackend('example/config.json')

# Make the decorator
feature = Feature(backend, logger)
# --- END FLAGON SPECIFIC CODE---

# Now to use flagon for feature flagging


@feature('test')
def t(a):
    print("FROM t()", a)

print("\n* Executing feature 'test' with 'asd': ")
t('asd')


@feature('off')
def o(a):
    print("FROM a()", a)


@feature('withdefault', default=t)
def v(a):
    print("FROM v()", a)

print("\n* Executing feature 'off' (which is turned off) with 'asd'")
try:
    o('asd')
except NameError, ne:
    print(type(ne), ne)

print(
    "\n* Executing feature 'withdefault' (which is turned off) "
    "which passed a default implementation of the t function.")
v('asd')

print("\n* Defining 'doesnotexist' (which is not a configured feature)")
