# Generated by Django 3.1.1 on 2020-11-19 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20201117_2241'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsItem',
            new_name='News',
        ),
    ]