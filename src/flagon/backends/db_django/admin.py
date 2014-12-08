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
Admin configuration.
"""
from django.contrib import admin

from flagon.backends.db_django.models import FlagonParams, FlagonFeature


# Actions
def enable_features(modeladmin, request, queryset):
    queryset.update(active=True)

enable_features.short_description = 'Enable Features'


def disable_features(modeladmin, request, queryset):
    queryset.update(active=False)

disable_features.short_description = 'Disable Features'


class FlagonParamsAdmin(admin.ModelAdmin):
    list_display = ('key', 'type')


class FlagonFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'strategy')
    actions = [enable_features, disable_features]


# Register models to admin
admin.site.register(FlagonFeature, FlagonFeatureAdmin)
admin.site.register(FlagonParams, FlagonParamsAdmin)
