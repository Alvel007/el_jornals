# Generated by Django 5.0.1 on 2024-02-03 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0010_quickrecording_delete_autocompletedisp'),
        ('powerline', '0033_powerline_for_cus_dispatcher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickrecording',
            name='powerline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='powerline.powerline'),
        ),
    ]
