# Generated by Django 5.0.1 on 2024-02-02 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0027_alter_thirdpartydispatchers_disp_center'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thirdpartydispatchers',
            name='disp_center',
        ),
    ]