# Generated by Django 2.2.3 on 2019-08-12 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20190812_1301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='tag',
            new_name='tags',
        ),
    ]
