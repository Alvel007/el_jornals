# Generated by Django 5.0.1 on 2024-02-04 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0020_selecteddata_alter_disprecordmodel_powerline'),
    ]

    operations = [
        migrations.AddField(
            model_name='selecteddata',
            name='hand_over_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст "Приём ВЛ от диспетчера"'),
        ),
    ]