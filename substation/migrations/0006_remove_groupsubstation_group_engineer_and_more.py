# Generated by Django 4.2.7 on 2023-12-14 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substation', '0005_remove_groupsubstation_group_boss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupsubstation',
            name='group_engineer',
        ),
        migrations.RemoveField(
            model_name='substation',
            name='substation_boss',
        ),
    ]
