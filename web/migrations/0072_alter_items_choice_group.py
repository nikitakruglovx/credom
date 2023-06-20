# Generated by Django 4.0.3 on 2022-06-04 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0071_alter_folder_password_folder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('sitesandweb', 'Сайты/Веб-приложения'), ('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('logotype', 'Логотипы'), ('treedmodels', '3D модели'), ('bots', 'Онлайн боты'), ('scripts', 'Скрипты'), ('androidapp', 'Мобильные приложения для Android'), ('books', 'Электронные книги'), ('courses', 'Обучающие курсы'), ('desktopsoft', 'Десктоп софт')], default='sitesandweb', max_length=50),
        ),
    ]