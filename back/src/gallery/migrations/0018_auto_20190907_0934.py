# Generated by Django 2.2.4 on 2019-09-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0017_auto_20190902_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(verbose_name='creation_date'),
        ),
    ]