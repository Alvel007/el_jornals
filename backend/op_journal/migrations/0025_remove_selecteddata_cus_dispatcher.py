# Generated by Django 5.0.1 on 2024-02-05 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0024_alter_selecteddata_cus_dispatcher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selecteddata',
            name='CUS_dispatcher',
        ),
    ]