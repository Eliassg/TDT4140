# Generated by Django 3.0.4 on 2020-03-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0017_auto_20200313_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]