# Generated by Django 3.0.4 on 2020-03-16 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0014_reportpost_post_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportpost',
            name='post_link',
        ),
    ]
