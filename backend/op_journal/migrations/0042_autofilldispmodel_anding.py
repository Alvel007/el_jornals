# Generated by Django 5.0.1 on 2024-02-11 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0041_remove_autofilldispmodel_at_subst'),
        ('substation', '0002_alter_substation_dispatcher_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='autofilldispmodel',
            name='anding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='substation.substation', verbose_name='На подстанции'),
        ),
    ]
