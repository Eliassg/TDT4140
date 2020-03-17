# Generated by Django 3.0.3 on 2020-03-11 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forumApp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forumApp', '0009_auto_20200226_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forumApp.Post'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=forumApp.models.get_image_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
