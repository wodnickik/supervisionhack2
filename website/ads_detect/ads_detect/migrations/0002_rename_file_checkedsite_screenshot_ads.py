# Generated by Django 4.2.1 on 2023-05-21 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads_detect', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkedsite',
            old_name='file',
            new_name='screenshot_ads',
        ),
    ]
