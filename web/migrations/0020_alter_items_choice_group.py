# Generated by Django 4.0.3 on 2022-05-09 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_alter_items_choice_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='choice_group',
            field=models.CharField(choices=[('scripts', 'Скрипты'), ('sitesandweb', 'Сайты/Веб-приложения'), ('bots', 'Онлайн боты'), ('androidapp', 'Мобильные приложения для андроид')], default='sitesandweb', max_length=50),
        ),
    ]