from django.contrib import admin
from django.utils import timezone
from .models import MainPageOPJournal, AutocompleteOption, СommentOPJ
from django.template.defaultfilters import truncatechars

from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE

class SubstationFilter(admin.SimpleListFilter):
    title = 'Подстанция'
    parameter_name = 'substation'

    def lookups(self, request, model_admin):
        substation_values = MainPageOPJournal.objects.values_list('substation__name', flat=True).distinct()
        return [(substation, substation) for substation in substation_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(comment__substation__name=self.value())
        return queryset

class СommentOPJAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'real_date', 'user', 'mainpageopjournal', 'get_substation')
    list_display_links = ('id', 'text', 'real_date', 'user')
    search_fields = ('text', 'user__last_name', 'mainpageopjournal__text',)
    list_filter = (SubstationFilter, 'user')
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE

    def mainpageopjournal(self, obj):
        comment_text = obj.comment.first().text if obj.comment.exists() else None
        return truncatechars(comment_text, 20) if comment_text else None

    mainpageopjournal.short_description = 'Комментарий оставлен к записи'

    def get_substation(self, obj):
        return obj.comment.first().substation.name

    get_substation.short_description = 'Подстанция'


class MainPageOPJournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'real_date_format', 'pub_date_format', 'substation', 'user', 'comment', 'entry_is_valid', 'special_regime_introduced', 'emergency_event', 'short_circuit', 'file')
    list_display_links = ('id', 'short_text')
    search_fields = ('text', 'substation__name', 'user__last_name')
    list_filter = ('substation', 'entry_is_valid', 'special_regime_introduced', 'emergency_event')
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE
    
    def real_date_format(self, obj):
        return timezone.localtime(obj.real_date).strftime("%Y-%m-%d %H:%M:%S")
    real_date_format.short_description = 'Время создания записи пользователем'

    def pub_date_format(self, obj):
        return timezone.localtime(obj.pub_date).strftime("%Y-%m-%d %H:%M:%S")
    pub_date_format.short_description = 'Время выполнения действия'

    def short_text(self, obj):
        if len(obj.text) > 30:
            return obj.text[:30] + '...'
        else:
            return obj.text
    short_text.short_description = 'Содержание записи'
    
class AutocompleteOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)
    list_per_page = NUMBER_ENTRIES_OP_LOG_PAGE


admin.site.register(MainPageOPJournal, MainPageOPJournalAdmin)
admin.site.register(AutocompleteOption, AutocompleteOptionAdmin)
admin.site.register(СommentOPJ, СommentOPJAdmin)
