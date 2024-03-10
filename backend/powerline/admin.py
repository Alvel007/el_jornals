from django.contrib import admin
from .models import PowerLine, AdmittingStaff, DispatchCompanies, ThirdPartyDispatchers

class DispatchCompaniesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'abbreviated_name')
    search_fields = ('full_name', 'abbreviated_name')


class ThirdPartyDispatchersAdmin(admin.ModelAdmin):
    list_display = ('disp_name',)
    search_fields = ('disp_name',)

class PowerLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'voltage','induced_voltage')
    list_filter = ('voltage', 'induced_voltage')
    search_fields = ('name', 'voltage')
    filter_horizontal = ('for_CUS_dispatcher', 'ending')


class AdmittingStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    filter_horizontal = ('for_CUS_dispatcher',)


admin.site.register(DispatchCompanies, DispatchCompaniesAdmin)
admin.site.register(ThirdPartyDispatchers, ThirdPartyDispatchersAdmin)
admin.site.register(PowerLine, PowerLineAdmin)
admin.site.register(AdmittingStaff, AdmittingStaffAdmin)