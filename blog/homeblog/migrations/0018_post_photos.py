# Generated by Django 3.1.3 on 2020-12-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeblog', '0017_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photos',
            field=models.ImageField(blank=True, upload_to='photos/'),
        ),
    ]