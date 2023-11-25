from django.contrib import admin
from django.utils import timezone
from .models import MainPageOPJournal, AutocompleteOption

from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE

class MainPageOPJournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'real_date_format', 'pub_date_format', 'substation', 'user', 'comment', 'entry_is_valid', 'special_regime_introduced', 'emergency_event', 'short_circuit')
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
