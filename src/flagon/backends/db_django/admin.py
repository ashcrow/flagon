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
