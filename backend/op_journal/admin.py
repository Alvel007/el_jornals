from django.contrib import admin
from django.contrib.auth.models import Group
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.html import format_html
from el_journals.settings import (MAX_ATTACHED_FILES,
                                  NUMBER_ENTRIES_OP_LOG_PAGE, SUPER_ADMIN)

from .models import (AutocompleteOption, AutofillDispModel, FileModelOPJ,
                     MainPageOPJournal, СommentOPJ)


class FileModelOPJInline(admin.TabularInline):
    model = FileModelOPJ
    extra = 0

    def has_add_permission(self, request, obj=None):
        if not SUPER_ADMIN:
            max_file_size = getattr(MAX_ATTACHED_FILES, 0)
            files_count = obj.files.count() if obj else 0
            return files_count < max_file_size
        return True


class SubstationFilter(admin.SimpleListFilter):
    title = 'Подстанция'
    parameter_name = 'substation'

    def lookups(self, request, model_admin):
        substation_values = MainPageOPJournal.objects.values_list(
            'substation__name',
            flat=True
        ).distinct()
        return [(substation, substation) for substation in substation_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(comment__substation__name=self.value())
        return queryset


class СommentOPJAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'text',
                    'real_date',
                    'user',
                    'mainpageopjournal',
                    'get_substation')
    list_display_links = ('id',
                          'text',
                          'real_date',
                          'user')
    search_fields = ('text',
                     'user__last_name',
                     'mainpageopjournal__text',)
    list_filter = (SubstationFilter,
                   'user')
    list_per_page = int(NUMBER_ENTRIES_OP_LOG_PAGE)

    def mainpageopjournal(self, obj):
        comment_text = (
            obj.comment.first().text
            if obj.comment.exists()
            else None)
        return truncatechars(comment_text, 20) if comment_text else None
    mainpageopjournal.short_description = 'Комментарий оставлен к записи'

    def get_substation(self, obj):
        return obj.comment.first().substation.name
    get_substation.short_description = 'Подстанция'

    def get_readonly_fields(self, request, obj=None):
        if obj and not SUPER_ADMIN:
            return self.readonly_fields + ('text',
                                           'real_date',
                                           'user',
                                           'mainpageopjournal',
                                           'user_signature',
                                           )
        return self.readonly_fields


class MainPageOPJournalAdmin(admin.ModelAdmin):
    readonly_fields = ('get_files',)
    list_display = ('id',
                    'short_text',
                    'real_date_format',
                    'pub_date_format',
                    'substation', 'user',
                    'comment', 'entry_is_valid',
                    'special_regime_introduced',
                    'emergency_event',
                    'short_circuit',
                    'planned_completion_date'
                    )
    list_display_links = ('id',
                          'short_text',
                          )
    search_fields = ('text',
                     'substation__name',
                     'user__last_name',
                     )
    list_filter = ('substation',
                   'entry_is_valid',
                   'special_regime_introduced',
                   'emergency_event',
                   )
    list_per_page = int(NUMBER_ENTRIES_OP_LOG_PAGE)

    fieldsets = (
        ('Основная информация', {'fields': ('substation',
                                            'user',
                                            'user_signature',
                                            'text', 'pub_date',
                                            'real_date',
                                            'entry_is_valid')}),
        ('Особые отметки выбранной записи', {'fields':
                                             ('special_regime_introduced',
                                              'emergency_event',
                                              'short_circuit')}),
        ('Комментарий АТП к записи', {'fields': ('comment',)}),
        ('Запись вносит отклонение'
         'в нормальный режим Да/Нет', {'fields':
                                       ('withdrawal_for_repair',
                                        'planned_completion_date',
                                        'permission_to_work',
                                        'closing_entry',)}),
        ('Прикрепленные файлы', {'fields': ('get_files',)})
    )

    if SUPER_ADMIN:
        inlines = [FileModelOPJInline]

    def real_date_format(self, obj):
        return timezone.localtime(obj.real_date).strftime("%Y-%m-%d %H:%M:%S")
    real_date_format.short_description = 'Время создания записи пользователем'

    def pub_date_format(self, obj):
        return timezone.localtime(obj.pub_date).strftime("%Y-%m-%d %H:%M:%S")
    pub_date_format.short_description = 'Время выполнения действия'

    def planned_completion_date_format(self, obj):
        return timezone.localtime(obj.pub_date).strftime("%Y-%m-%d %H:%M:%S")
    planned_completion_date_format.short_description = ('Планируемое '
                                                        'время '
                                                        'окончания работ')

    def short_text(self, obj):
        if len(obj.text) > 30:
            return obj.text[:30] + '...'
        else:
            return obj.text
    short_text.short_description = 'Содержание записи'

    def get_files(self, obj):
        files = obj.files.all()
        file_links = []
        for file in files:
            file_link = '<a href="{0}">{1}</a>'.format(
                file.file.url, file.file.name)
            file_links.append(file_link)
        return format_html(', '.join(file_links))
    get_files.short_description = 'Прикрепленные файлы'

    def get_readonly_fields(self, request, obj=None):
        if obj and not SUPER_ADMIN:
            return self.readonly_fields + (
                'text',
                'real_date',
                'pub_date',
                'substation',
                'user',
                'comment',
                'entry_is_valid',
                'special_regime_introduced',
                'emergency_event',
                'short_circuit',
                'user_signature',
                'get_files',
                'closing_entry',
                'planned_completion_date',
                'withdrawal_for_repair',
                'permission_to_work'
            )
        return self.readonly_fields


class AutocompleteOptionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'text',
                    'get_substations')
    search_fields = ('text',)
    list_per_page = int(NUMBER_ENTRIES_OP_LOG_PAGE)
    list_display_links = ('text',)
    filter_horizontal = ('substation',)

    def get_substations(self, obj):
        return ", ".join([
            substation.name
            for substation
            in obj.substation.all()])

    get_substations.short_description = 'Подстанции'


class AutofillDispAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'dispatcher',
                    'admitting',
                    'ending',
                    'end_time',
                    'emergency_entry',
                    'hand_over_text',)
    readonly_fields = ('hand_over_text',
                       'prm_tolerances',
                       'prm_only',
                       'without_tripping',
                       'at_substation',
                       'and_work',
                       'submit_vl',)


admin.site.register(AutofillDispModel, AutofillDispAdmin)
admin.site.register(MainPageOPJournal, MainPageOPJournalAdmin)
admin.site.register(AutocompleteOption, AutocompleteOptionAdmin)
admin.site.register(СommentOPJ, СommentOPJAdmin)
admin.site.unregister(Group)
