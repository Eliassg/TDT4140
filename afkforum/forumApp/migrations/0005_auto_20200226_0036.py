# Generated by Django 3.0.2 on 2020-02-25 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0004_remove_post_url'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
    ]
