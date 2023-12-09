from django.db import models
from django.utils import timezone
from staff.models import CustomUser
from substation.models import Substation
import pytz



class СommentOPJ(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    real_date = models.DateTimeField(default=timezone.now,
                                     verbose_name='Время создания комментария',)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_DEFAULT,
                             default='Пользователь удален',
                             verbose_name='Комментарий сделал',
                             related_name='commentator')
    
    class Meta:
        verbose_name = 'Комментарий к ОЖ'
        verbose_name_plural = 'Комментарии к ОЖ'
        
    def __str__(self):
        return f'{self.real_date} {self.user} написал комментарий {self.text}.'


class MainPageOPJournal(models.Model):
    text = models.TextField(verbose_name='Содержание')
    real_date = models.DateTimeField(default=timezone.now,
                                     verbose_name='Время создания записи пользователем',
                                     editable=False)
    pub_date = models.DateTimeField(verbose_name='Время выполнения действия')
    substation = models.ForeignKey(Substation,
                                   verbose_name='Подстанция',
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   related_name='substation')
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Запись сделал',
                             related_name='user')
    comment = models.ForeignKey(СommentOPJ,
                                verbose_name='Комментарий',
                                on_delete=models.SET_NULL,
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
    file = models.FileField(upload_to='files/',
                            verbose_name='Дополнительные файлы',
                            blank=True,
                            null=True)


    class Meta:
        verbose_name = 'Запись опер. журнала'
        verbose_name_plural = 'Записи опер. журналов'
        
    def save(self, *args, **kwargs):
        moscow_timezone = pytz.timezone('Europe/Moscow')
        self.real_date = self.real_date.astimezone(moscow_timezone)
        self.pub_date = self.pub_date.astimezone(moscow_timezone)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pub_date} {self.user} внес запись в ОЖ {self.substation}.'


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