# Generated by Django 4.2.7 on 2023-12-09 22:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0024_remove_mainpageopjournal_files_delete_filemodelopj'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModelOPJ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='OPJ/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])),
                ('main_page_op_journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='op_journal.mainpageopjournal')),
            ],
        ),
    ]
