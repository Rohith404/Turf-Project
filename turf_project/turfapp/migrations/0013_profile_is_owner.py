# Generated by Django 4.0.3 on 2022-04-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfapp', '0012_remove_post_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]