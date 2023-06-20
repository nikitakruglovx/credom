# Generated by Django 4.0.3 on 2022-05-21 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0065_rename_id_users_uu_id_alter_items_choice_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('scripts', 'Скрипты'), ('desktopsoft', 'Десктоп софт'), ('logotype', 'Логотипы'), ('books', 'Электронные книги'), ('bots', 'Онлайн боты'), ('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('courses', 'Обучающие курсы'), ('sitesandweb', 'Сайты/Веб-приложения'), ('treedmodels', '3D модели'), ('androidapp', 'Мобильные приложения для Android')], default='sitesandweb', max_length=50),
        ),
    ]
