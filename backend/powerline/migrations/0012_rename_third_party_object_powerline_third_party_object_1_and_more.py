# Generated by Django 5.0.1 on 2024-02-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0011_powerline_third_party_object'),
    ]

    operations = [
        migrations.RenameField(
            model_name='powerline',
            old_name='third_party_object',
            new_name='third_party_object_1',
        ),
        migrations.AddField(
            model_name='powerline',
            name='third_party_object_2',
            field=models.CharField(blank=True, help_text='Если ВЛ подключена к объектам третьих лиц, укажите ДН этого объекта', max_length=64, null=True, verbose_name='Сторонний объект'),
        ),
    ]
