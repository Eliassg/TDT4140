# Generated by Django 3.0.3 on 2020-03-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0016_auto_20200316_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
