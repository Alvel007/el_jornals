# Generated by Django 5.0.1 on 2024-02-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0034_alter_powerline_third_party_object_1_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ManufacturerStaff',
        ),
        migrations.AlterField(
            model_name='thirdpartydispatchers',
            name='disp_name',
            field=models.CharField(max_length=64, null=True, unique=True, verbose_name='Фамилия И.О. персонала стороннего ДЦ'),
        ),
    ]
