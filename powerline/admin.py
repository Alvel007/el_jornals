from django.contrib import admin
from .models import PowerLine, AdmittingStaff, ManufacturerStaff

class PowerLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'voltage', 'ending_1', 'ending_2', 'ending_3', 'Induced_voltage')
    list_filter = ('voltage', 'Induced_voltage')
    search_fields = ('name', 'voltage')

admin.site.register(PowerLine, PowerLineAdmin)

class AdmittingStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')

admin.site.register(AdmittingStaff, AdmittingStaffAdmin)

class ManufacturerStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'oganization')
    search_fields = ('name', 'position', 'oganization')

admin.site.register(ManufacturerStaff, ManufacturerStaffAdmin)