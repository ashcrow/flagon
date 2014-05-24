from django.contrib import admin

from flagon.backends.db_django.models import FlagonParams, FlagonFeature


class FlagonParamsAdmin(admin.ModelAdmin):
    list_display = ('key', 'type')


class FlagonFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'strategy')


admin.site.register(FlagonFeature, FlagonFeatureAdmin)
admin.site.register(FlagonParams, FlagonParamsAdmin)
