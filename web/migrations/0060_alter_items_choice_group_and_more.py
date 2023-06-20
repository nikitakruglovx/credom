# Generated by Django 4.0.3 on 2022-05-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0059_alter_items_choice_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('scripts', 'Скрипты'), ('logotype', 'Логотипы'), ('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('desktopsoft', 'Десктоп софт'), ('androidapp', 'Мобильные приложения для Android'), ('bots', 'Онлайн боты'), ('treedmodels', '3D модели'), ('sitesandweb', 'Сайты/Веб-приложения')], default='sitesandweb', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='background_profile',
            field=models.ImageField(blank=True, default='avatarback/cover.png', null=True, upload_to='avatarback/'),
        ),
    ]
