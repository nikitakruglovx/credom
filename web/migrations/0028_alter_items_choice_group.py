# Generated by Django 4.0.3 on 2022-05-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_remove_users_address_alter_items_choice_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('logotype', 'Логотипы'), ('desktopsoft', 'Десктоп софт'), ('treedmodels', '3D модели'), ('scripts', 'Скрипты'), ('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('sitesandweb', 'Сайты/Веб-приложения'), ('bots', 'Онлайн боты'), ('androidapp', 'Мобильные приложения для Android')], default='sitesandweb', max_length=50),
        ),
    ]
