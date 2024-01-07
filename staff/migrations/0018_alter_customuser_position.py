# Generated by Django 4.2.7 on 2023-12-15 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0017_alter_customuser_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='position',
            field=models.CharField(choices=[('Электромонтер по обслуживанию', 'Электромонтер по обслуживанию'), ('Дежурный инженер', 'Дежурный инженер'), ('Дежурный инженер 2 кат.', 'Дежурный инженер 2 кат.'), ('Дежурный инженер 1 кат.', 'Дежурный инженер 1 кат.'), ('Диспетчер', 'Диспетчер'), ('Ведущий инженер', 'Ведущий инженер'), ('Ведущий инженер по ОП', 'Ведущий инженер по ОП'), ('Начальник', 'Начальник'), ('Начальник ООР', 'Начальник ООР'), ('АТП', 'АТП'), ('Зам. гл. инженера', 'Зам. гл. инженера'), ('Главный инженер', 'Главный инженер')], default='', max_length=120, null=True, verbose_name='Должность'),
        ),
    ]
