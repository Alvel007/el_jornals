# Generated by Django 5.0.1 on 2024-01-26 20:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0002_mainpageopjournal_permission_to_work_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageopjournal',
            name='real_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания записи пользователем'),
        ),
    ]