from django import forms
from django.contrib import admin
from django.db.models import Q
from .models import GroupSubstation, Substation
from staff.models import CustomUser
from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE
from .forms import SubstationForm


class GroupSubstationAdminForm(forms.ModelForm):
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE

    class Meta:
        model = GroupSubstation
        fields = '__all__'

class GroupSubstationAdmin(admin.ModelAdmin):
    form = GroupSubstationAdminForm
    list_display = ('name',
                    'get_include_substations',
                    'slug')
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE

    def get_include_substations(self, obj):
        return ", ".join([substation.name for substation in obj.substation_set.all()])

    get_include_substations.short_description = 'Включает в себя ПС'


class SubstationAdmin(admin.ModelAdmin):
    form = SubstationForm
    list_display = ('name', 'dispatch_point', 'address', 'group_substation', 'slug')

admin.site.register(GroupSubstation, GroupSubstationAdmin)
admin.site.register(Substation, SubstationAdmin)