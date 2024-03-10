# Generated by Django 5.0.1 on 2024-02-03 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0012_delete_quickrecording'),
        ('powerline', '0033_powerline_for_cus_dispatcher'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispRecordModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatchers', models.ManyToManyField(blank=True, to='powerline.thirdpartydispatchers', verbose_name='Диспетчеры')),
                ('powerline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='powerline.powerline')),
            ],
        ),
    ]
