# Generated by Django 5.0.1 on 2024-02-03 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0031_thirdpartydispatchers_disp_center'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='powerline',
            name='for_CUS_dispatcher',
        ),
    ]