# Generated by Django 4.2.7 on 2023-11-18 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0006_autocompleteoption_delete_suggestedtext'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AutocompleteOption',
        ),
    ]
