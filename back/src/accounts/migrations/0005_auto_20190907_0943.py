# Generated by Django 2.2.4 on 2019-09-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_lang_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lang_key',
            field=models.CharField(choices=[('RO', 'RO'), ('EN', 'EN')], default='RO', max_length=2),
        ),
    ]