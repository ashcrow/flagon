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
Database models.
"""

import six

from django.db import models


class FlagonParams(models.Model):
    """
    Parameters for a feature.
    """
    key = models.CharField(max_length=255)
    value = models.TextField()
    type = models.CharField(
        max_length=30,
        choices=(('bool', 'bool'), ('int', 'int'), ('str', 'str')))

    def __repr__(self):
        return six.u("%s=%s(%s)" % (self.key, self.type, self.value))

    __str__ = __repr__


class FlagonFeature(models.Model):
    """
    A feature.
    """
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    strategy = models.CharField(max_length=255, blank=True, null=True)
    params = models.ForeignKey(FlagonParams, null=True, blank=True)

    def __repr__(self):
        return six.u(self.name)

    __str__ = __repr__
