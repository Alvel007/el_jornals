# Generated by Django 5.0.1 on 2024-02-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0021_selecteddata_hand_over_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteddata',
            name='hand_over_text',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Приём ВЛ от диспетчера"'),
        ),
    ]
