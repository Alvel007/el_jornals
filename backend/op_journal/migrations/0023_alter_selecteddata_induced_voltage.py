# Generated by Django 5.0.1 on 2024-02-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0022_alter_selecteddata_hand_over_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteddata',
            name='induced_voltage',
            field=models.BooleanField(blank=True, default=False, verbose_name='Наведенное напряжение'),
        ),
    ]
