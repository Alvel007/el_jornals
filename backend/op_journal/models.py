import locale
from django.db import models
from django.utils import timezone
from staff.models import CustomUser
from substation.models import Substation
from powerline.models import PowerLine, ThirdPartyDispatchers, AdmittingStaff
import pytz
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from itertools import chain


class СommentOPJ(models.Model):
    text = models.TextField(
        verbose_name='Комментарий'
        )
    real_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время создания комментария',
        )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        default='Пользователь удален',
        verbose_name='Комментарий сделал',
        related_name='commentator'
        )
    user_signature = models.CharField(
        verbose_name='Подпись пользователя',
        max_length=255,
        blank=True,
        null=True,
        editable=False
        )

    class Meta:
        verbose_name = 'Комментарий к ОЖ'
        verbose_name_plural = 'Комментарии к ОЖ'

    def save(self, *args, **kwargs):
        if not self.pk:
            first_initial = (
                self.user.first_name[0] if self.user.first_name else ''
                )
            middle_initial = (
                self.user.middle_name[0] if self.user.middle_name else ''
                )
            fio = f'{self.user.last_name} {first_initial}.{middle_initial}.'
            position = self.user.position
            if self.user.main_place_work is None:
                post_user = self.user.substation_group.name_rp
            else:
                post_user = self.user.main_place_work
            self.user_signature = f'{fio} {position} {post_user}'
        super().save(*args, **kwargs)

    def __str__(self):
        real_date_formatted = self.real_date.strftime('%Y-%m-%d %H:%M')
        return (f'{real_date_formatted} {self.user_signature} '
                f'оставил комментарий "{self.text}".')


class MainPageOPJournal(models.Model):
    text = models.TextField(
        verbose_name='Содержание',
        )
    real_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время создания записи пользователем',
        )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время выполнения действия',
        )
    substation = models.ForeignKey(
        Substation,
        verbose_name='Подстанция',
        on_delete=models.PROTECT,
        blank=False,
        related_name='substation',
        )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Запись сделал',
        related_name='user',
        )
    comment = models.ForeignKey(
        СommentOPJ,
        verbose_name='Комментарий',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='comment',
        )
    entry_is_valid = models.BooleanField(
        verbose_name='Запись верна',
        default=True,
        )
    withdrawal_for_repair = models.BooleanField(
        verbose_name='Запись о выводе оборудования из работы',
        default=False
        )
    planned_completion_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Планируемая дата ввода в работу',
        blank=True,
        null=True,
        )
    permission_to_work = models.BooleanField(
        verbose_name='Запись о допуске к выполнению работ',
        default=False,
        )
    special_regime_introduced = models.BooleanField(
        verbose_name='Ввод особого режима (ОРР, РПГ, РВР)',
        default=False,
        )
    emergency_event = models.BooleanField(
        verbose_name='Аварийное событие',
        default=False,
        )
    short_circuit = models.BooleanField(
        verbose_name='КЗ в сети 6-35 кВ',
        default=False,
        )
    user_signature = models.CharField(
        verbose_name='Подпись пользователя',
        max_length=255,
        blank=True,
        null=True,
        )
    closing_entry = models.ManyToManyField(
        'self',
        blank=True,
        default=None,
        verbose_name='Закрыта записью',
        help_text='Выберете связанную запись, исключающую текущую '
                  'запись из отклонений',)

    class Meta:
        verbose_name = 'Запись опер. журнала'
        verbose_name_plural = 'Записи опер. журналов'

    def save(self, *args, **kwargs):
        if not self.pk:
            first_initial = (
                self.user.first_name[0]
                if self.user.first_name
                else '')
            middle_initial = (
                self.user.middle_name[0]
                if self.user.middle_name
                else '')
            fio = f'{self.user.last_name} {first_initial}.{middle_initial}.'
            position = self.user.position
            if self.user.main_place_work is None:
                post_user = self.user.substation_group.name_rp
            else:
                post_user = self.user.main_place_work
            self.user_signature = f'{fio} {position} {post_user}'
        moscow_timezone = pytz.timezone('Europe/Moscow')
        self.real_date = self.real_date.astimezone(moscow_timezone)
        self.pub_date = self.pub_date.astimezone(moscow_timezone)
        self.planned_completion_date = (
            self.planned_completion_date.astimezone(moscow_timezone))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class AutocompleteOption(models.Model):
    label = models.TextField(
        verbose_name='Сокращение, видимое при автовводе текста',
        blank=True,
        null=True,
        editable=False,
        )
    text = models.TextField(
        verbose_name='Текст автозаполнения',
        )
    substation = models.ManyToManyField(
        Substation,
        verbose_name='Для подстанции',
        default=None,
        blank=False,
        related_name='for_substation',
        )
    out_of_work = models.BooleanField(
        verbose_name='Допуск к работам',
        default=False,
        blank=True,
        null=True,
        )
    getting_started = models.BooleanField(
        verbose_name='Окончании работ',
        default=False,
        blank=True,
        null=True,
        )
    disabling = models.BooleanField(
        verbose_name='Выводе в ремонт/отключении',
        default=False,
        blank=True,
        null=True,
        )
    enabling = models.BooleanField(
        verbose_name='Включении оборудования',
        default=False,
        blank=True,
        null=True,
        )

    def save(self, *args, **kwargs):
        super(AutocompleteOption, self).save(*args, **kwargs)

        if len(self.text) > 55:
            self.label = self.text[:100] + '...'
        else:
            self.label = self.text
        super(AutocompleteOption, self).save(*args, **kwargs)

        def __str__(self):
            return self.text

    class Meta:
        verbose_name = 'Автозаполнение формы'
        verbose_name_plural = 'Автозаполнений форм'


class FileModelOPJ(models.Model):
    main_page_op_journal = models.ForeignKey(
        MainPageOPJournal,
        on_delete=models.PROTECT,
        related_name='files',
        )
    file = models.FileField(
        upload_to='OPJ/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])]
        )

    def clean(self):
        super().clean()
        if self.file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError(
                f'Размер файла не может превышать {settings.MAX_FILE_SIZE} МБ.'
                )
        if (self.main_page_op_journal.files.count() >
                settings.MAX_ATTACHED_FILES):
            raise ValidationError('Максимальное количество файлов: '
                                  f'{settings.MAX_ATTACHED_FILES}.')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Доп. файл'
        verbose_name_plural = 'Дополнительные материалы'


class AutofillDispModel(models.Model):
    name = models.ForeignKey(
        PowerLine,
        on_delete=models.PROTECT,
        verbose_name='Запись для ВЛ',
        )
    dispatcher = models.ForeignKey(
        ThirdPartyDispatchers,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name='Диспетчер',
        )
    admitting = models.ForeignKey(
        AdmittingStaff,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name='Допускающий',
        )
    ending = models.ForeignKey(
        Substation,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='На подстанции',
        )
    end_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Работы закончить до: ',
        )
    emergency_entry = models.CharField(
        max_length=100,
        verbose_name='Время аварийной готовности',
        blank=True,
        null=True,
        )
    cus_dispatcher = models.CharField(
        max_length=100,
        verbose_name='Экспл.ведение',
        )
    hand_over_text = models.TextField(
        verbose_name='Текст "Приём ВЛ от диспетчера"',
        blank=True,
        null=True,
        editable=False,
        )
    prm_tolerances = models.TextField(
        verbose_name='Текст "Команда на ПРМиД на ВЛ"',
        blank=True,
        null=True,
        editable=False,
        )
    prm_only = models.TextField(
        verbose_name='Текст "Команда на ПРМ"',
        blank=True,
        null=True,
        editable=False,
        )
    admission_omly = models.TextField(
        verbose_name='Текст "Команда на допуск"',
        blank=True,
        null=True,
        editable=False,
        )
    without_tripping = models.TextField(
        verbose_name='Текст "Команда на работы без отключения"',
        blank=True,
        null=True,
        editable=False,
        )
    at_substation = models.TextField(
        verbose_name='Текст "Команда на работы на линейном оборудовании ПС"',
        blank=True,
        null=True,
        editable=False,
        )
    and_work = models.TextField(
        verbose_name='Текст "Работы на ВЛ закончены".',
        blank=True,
        null=True,
        editable=False,
        )
    submit_vl = models.TextField(
        verbose_name='Текст "Передача ВЛ диспетчепу, в чьем она управлении".',
        blank=True,
        null=True,
        editable=False,
        )

    def save(self, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        months = ('января',
                  'февраля',
                  'марта',
                  'апреля',
                  'мая',
                  'июня',
                  'июля',
                  'августа',
                  'сентября',
                  'октября',
                  'ноября',
                  'декабря',
                  )
        end_time_formatted = (f'{self.end_time.strftime('%H-%M')} '
                              f'{self.end_time.day} '
                              f'{months[self.end_time.month - 1]} '
                              f'{self.end_time.year} года')
        endings = list(self.name.ending.values_list('name', flat=True))
        third_party_objects = list(chain(
            filter(None, [self.name.third_party_object_1,
                          self.name.third_party_object_2,
                          self.name.third_party_object_3])
                        ))
        combined_list = endings + third_party_objects

        if len(combined_list) > 1:
            combined_string = (', '.join(map(str, combined_list[:-1]))
                               + ' и ' + combined_list[-1])
        else:
            combined_string = combined_list[0]
        self.hand_over_text = settings.ISSUANCE_OF_CONFIRMATION.format(
            self.dispatcher.disp_post,
            self.name.disp_manage.abbreviated_name_rp,
            self.dispatcher,
            self.name,
            combined_string,
            end_time_formatted,
            self.emergency_entry,
            )
        self.prm_tolerances = settings.PREPARATION_AND_ADMISSION.format(
            self.admitting.position,
            self.admitting.organization,
            self.admitting.name,
            self.name,
            combined_string,
            end_time_formatted,
            self.emergency_entry,
            )
        VOLTAGE_MESSAGE = " находится под наведенным напряжением >25 В."
        if self.name.induced_voltage:
            self.prm_tolerances += (f'\n{self.name}{VOLTAGE_MESSAGE}')
        self.prm_only = settings.PRM_ONLY.format(
            self.admitting.position,
            self.admitting.organization,
            self.admitting.name,
            self.name,
            combined_string,
            )
        if self.name.induced_voltage:
            self.prm_only += (f'\n{self.name}{VOLTAGE_MESSAGE}')
        self.admission_omly = settings.ADMISSION_ONLY.format(
            self.admitting.position,
            self.admitting.organization,
            self.admitting.name,
            self.name,
            end_time_formatted,
            self.emergency_entry,
            )
        if self.name.induced_voltage:
            self.admission_omly += (f'\n{self.name}{VOLTAGE_MESSAGE}')
        self.without_tripping = settings.WITHOUT_TRIPPING.format(
            self.admitting.position,
            self.admitting.organization,
            self.admitting.name,
            self.name,
            combined_string,
            end_time_formatted,
            self.emergency_entry,
            )
        self.at_substation = settings.AT_SUBSTATION.format(
            self.ending,
            self.name,
            combined_string,
            end_time_formatted,
            self.emergency_entry,
            )
        if self.name.induced_voltage:
            self.at_substation += (f'\n{self.name}{VOLTAGE_MESSAGE}')
        self.and_work = settings.END_WORK.format(
            self.name,
            )
        self.submit_vl = settings.SUBMIT_VL.format(
            self.dispatcher.disp_post,
            self.name.disp_manage.abbreviated_name_rp,
            self.dispatcher,
            self.name,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Диспетчерская автозапись'
        verbose_name_plural = 'Диспетчерские автозаписи'
