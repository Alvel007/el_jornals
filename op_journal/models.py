from django.db import models
from django.utils import timezone
from staff.models import CustomUser
from substation.models import Substation
import pytz
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.exceptions import ValidationError



class СommentOPJ(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    real_date = models.DateTimeField(default=timezone.now,
                                     verbose_name='Время создания комментария',)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.PROTECT,
                             default='Пользователь удален',
                             verbose_name='Комментарий сделал',
                             related_name='commentator')
    user_signature = models.CharField(verbose_name='Подпись пользователя',
                                      max_length=255,
                                      blank=True,
                                      null=True,)

    
    class Meta:
        verbose_name = 'Комментарий к ОЖ'
        verbose_name_plural = 'Комментарии к ОЖ'
        
    def save(self, *args, **kwargs):
        if not self.pk:
            first_initial = self.user.first_name[0] if self.user.first_name else ''
            middle_initial = self.user.middle_name[0] if self.user.middle_name else ''  
            fio = f'{self.user.last_name} {first_initial}.{middle_initial}.'
            position = self.user.position
            if self.user.main_place_work == None:
                post_user = self.user.substation_group.name_rp
            else:
                post_user = self.user.main_place_work
            self.user_signature = f'{fio}. {position} {post_user}'
        super().save(*args, **kwargs)
        
    def __str__(self):
        real_date_formatted = self.real_date.strftime('%Y-%m-%d %H:%M')
        return f'{real_date_formatted} {self.user_signature} оставил комментарий "{self.text}".'


class MainPageOPJournal(models.Model):
    text = models.TextField(verbose_name='Содержание')
    real_date = models.DateTimeField(default=timezone.now,
                                     verbose_name='Время создания записи пользователем',
                                     editable=False)
    pub_date = models.DateTimeField(verbose_name='Время выполнения действия')
    substation = models.ForeignKey(Substation,
                                   verbose_name='Подстанция',
                                   on_delete=models.PROTECT,
                                   blank=False,
                                   related_name='substation')
    user = models.ForeignKey(CustomUser,
                             on_delete=models.PROTECT,
                             verbose_name='Запись сделал',
                             related_name='user')
    comment = models.ForeignKey(СommentOPJ,
                                verbose_name='Комментарий',
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name='comment')
    entry_is_valid = models.BooleanField(verbose_name='Запись верна',
                                         default=True)
    special_regime_introduced = models.BooleanField(verbose_name='Ввод особого режима (ОРР, РПГ, РВР)',
                                                    default=False)
    emergency_event = models.BooleanField(verbose_name='Аварийное событие',
                                          default=False)
    short_circuit = models.BooleanField(verbose_name='КЗ в сети 6-35 кВ',
                                        default=False)
    user_signature = models.CharField(verbose_name='Подпись пользователя',
                                      max_length=255,
                                      blank=True,
                                      null=True,)


    class Meta:
        verbose_name = 'Запись опер. журнала'
        verbose_name_plural = 'Записи опер. журналов'
        
    def save(self, *args, **kwargs):
        if not self.pk:
            first_initial = self.user.first_name[0] if self.user.first_name else ''
            middle_initial = self.user.middle_name[0] if self.user.middle_name else ''  
            fio = f'{self.user.last_name} {first_initial}.{middle_initial}.'
            position = self.user.position
            if self.user.main_place_work == None:
                post_user = self.user.substation_group.name_rp
            else:
                post_user = self.user.main_place_work
            self.user_signature = f'{fio}. {position} {post_user}'
                
        moscow_timezone = pytz.timezone('Europe/Moscow')
        self.real_date = self.real_date.astimezone(moscow_timezone)
        self.pub_date = self.pub_date.astimezone(moscow_timezone)
        super().save(*args, **kwargs)

    def __str__(self):
        pub_date_formatted = self.pub_date.strftime('%Y-%m-%d %H:%M')
        return f'{pub_date_formatted} {self.user_signature} внес запись в оперативный журнал {self.substation}.'


class AutocompleteOption(models.Model):
    text = models.CharField(max_length=4096,
                            verbose_name='Текст автозаполнения')
    substation = models.ManyToManyField(Substation,
                                        verbose_name='Для подстанции',
                                        default=None,
                                        blank=False,
                                        related_name='for_substation')

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Автозаполнение формы'
        verbose_name_plural = 'Автозаполнение форм'
        
class FileModelOPJ(models.Model):
    main_page_op_journal = models.ForeignKey(MainPageOPJournal,
                                             on_delete=models.PROTECT,
                                             related_name='files')
    file = models.FileField(upload_to='OPJ/',
                            validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])

    def clean(self):
        super().clean()
        if self.file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError(f'Размер файла не может превышать {settings.MAX_FILE_SIZE} МБ.')
        if self.main_page_op_journal.files.count() > settings.MAX_ATTACHED_FILES:
                raise ValidationError(f'Максимальное количество файлов: {settings.MAX_ATTACHED_FILES}.')

    def __str__(self):
        return self.file.name
    
    class Meta:
        verbose_name = 'Доп. файл'
        verbose_name_plural = 'Дополнительные материалы'