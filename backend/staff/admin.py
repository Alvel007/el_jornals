from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username',
        'position',
        'last_name',
        'first_name',
        'middle_name',
        'birth_date',
        'employee_id',
        'electrical_safety_group',
        'get_operational_staff',
        'get_administrative_staff',
        'slug',
        'is_public',)
    search_fields = (
        'last_name',
        'employee_id',)
    filter_horizontal = (
        'operational_staff',
        'administrative_staff',
        'admin_opj',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Основная информация о пользователе', {
            'fields': (
                'last_name',
                'first_name',
                'middle_name',
                'position',
                'main_place_work',
                'substation_group',
                'birth_date',
                'employee_id',
                'electrical_safety_group',)}),
        ('Права пользователя', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_public',)}),
        ('Активность пользователя', {
            'fields': (
                'last_login',
                'date_joined',)}),
        ('Права пользователя по ведению оперативного журнала', {
            'fields': (
                'operational_staff',
                'administrative_staff',
                'admin_opj',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'last_name',
                'first_name',
                'middle_name',
                'birth_date',
                'position',
                'main_place_work',
                'substation_group',
                'employee_id',
                'electrical_safety_group',
                'operational_staff',
                'administrative_staff',
                'admin_opj', 'is_staff',
                'is_public',),
        }),
    )
    list_per_page = int(NUMBER_ENTRIES_OP_LOG_PAGE)

    def get_operational_staff(self, obj):
        return (", ".join([substation.name
                           for substation
                           in obj.operational_staff.all()]))

    def get_administrative_staff(self, obj):
        return (", ".join([substation.name
                           for substation
                           in obj.administrative_staff.all()]))

    get_operational_staff.short_description = 'Оперативный персонал'
    get_administrative_staff.short_description = 'Адм. технический персонал'


admin.site.register(CustomUser, CustomUserAdmin)
