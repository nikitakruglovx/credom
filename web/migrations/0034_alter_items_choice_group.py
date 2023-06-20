# Generated by Django 4.0.3 on 2022-05-11 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0033_alter_items_choice_group_alter_items_file_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('androidapp', 'Мобильные приложения для Android'), ('sitesandweb', 'Сайты/Веб-приложения'), ('treedmodels', '3D модели'), ('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('logotype', 'Логотипы'), ('desktopsoft', 'Десктоп софт'), ('scripts', 'Скрипты'), ('bots', 'Онлайн боты')], default='sitesandweb', max_length=50),
        ),
    ]
