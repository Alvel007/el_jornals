# Generated by Django 5.0.1 on 2024-01-21 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0039_remove_mainpageopjournal_impl_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageopjournal',
            name='closing_entry',
            field=models.ManyToManyField(blank=True, help_text='Выберете связанную запись, исключающую текущую запись из отклонений', to='op_journal.mainpageopjournal', verbose_name='Закрыта записью'),
        ),
    ]
