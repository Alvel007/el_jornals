# Generated by Django 5.0.1 on 2024-02-01 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0008_alter_powerline_for_cus_dispatcher'),
        ('substation', '0002_alter_substation_dispatcher_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powerline',
            name='ending_1',
            field=models.ForeignKey(blank=True, limit_choices_to={'dispatch_point': False}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='powerline_ending_1', to='substation.substation', verbose_name='Заходит на ПС 1'),
        ),
    ]
