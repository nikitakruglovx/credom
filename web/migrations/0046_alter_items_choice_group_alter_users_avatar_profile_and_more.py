# Generated by Django 4.0.3 on 2022-05-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0045_alter_items_choice_group_alter_users_avatar_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('frontendtamplate', 'html/css/js Frontend Шаблоны'), ('desktopsoft', 'Десктоп софт'), ('androidapp', 'Мобильные приложения для Android'), ('treedmodels', '3D модели'), ('bots', 'Онлайн боты'), ('logotype', 'Логотипы'), ('sitesandweb', 'Сайты/Веб-приложения'), ('scripts', 'Скрипты')], default='sitesandweb', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='avatar_profile',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatar/'),
        ),
        migrations.AlterField(
            model_name='users',
            name='background_profile',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatarback/'),
        ),
    ]