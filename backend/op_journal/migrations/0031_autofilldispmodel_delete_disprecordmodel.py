# Generated by Django 5.0.1 on 2024-02-06 05:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0030_selecteddata_emergency_entry_selecteddata_end_time'),
        ('powerline', '0033_powerline_for_cus_dispatcher'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutofillDispModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Работы закончить до: ')),
                ('emergency_entry', models.CharField(blank=True, max_length=100, null=True, verbose_name='Время аварийной готовности')),
                ('hand_over_text', models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Приём ВЛ от диспетчера"')),
                ('dispatcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='powerline.thirdpartydispatchers', verbose_name='Диспетчеры')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='powerline.powerline', verbose_name='Запись для ВЛ')),
            ],
            options={
                'verbose_name': 'Диспетчерская автозапись',
                'verbose_name_plural': 'Диспетчерские автозаписи',
            },
        ),
        migrations.DeleteModel(
            name='DispRecordModel',
        ),
    ]
