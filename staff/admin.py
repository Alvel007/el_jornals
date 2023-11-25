from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser
from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'position', 'last_name', 'first_name', 'middle_name', 'birth_date', 'employee_id', 'electrical_safety_group', 'get_operational_staff', 'get_administrative_staff', 'slug', 'is_public')
    search_fields = ('last_name', 'employee_id')
    filter_horizontal = ('operational_staff', 'administrative_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'position', 'birth_date', 'employee_id', 'electrical_safety_group')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('operational_staff', 'administrative_staff', 'is_public')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'last_name', 'first_name', 'middle_name', 'birth_date', 'employee_id', 'electrical_safety_group', 'operational_staff', 'administrative_staff', 'is_public'),
        }),
    )
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE

    def get_operational_staff(self, obj):
        return ", ".join([substation.name for substation in obj.operational_staff.all()])

    def get_administrative_staff(self, obj):
        return ", ".join([substation.name for substation in obj.administrative_staff.all()])

    get_operational_staff.short_description = 'Оперативный персонал'
    get_administrative_staff.short_description = 'Адм. технический персонал'

admin.site.register(CustomUser, CustomUserAdmin)
