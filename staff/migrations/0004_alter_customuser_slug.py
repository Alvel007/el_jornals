# Generated by Django 4.2.7 on 2023-11-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(editable=False, unique=True, verbose_name='Слаг'),
        ),
    ]
