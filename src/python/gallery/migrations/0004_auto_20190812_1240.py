# Generated by Django 2.2.3 on 2019-08-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20190812_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albumtag',
            name='album',
        ),
        migrations.RemoveField(
            model_name='albumtag',
            name='tag',
        ),
        migrations.AddField(
            model_name='album',
            name='categories',
            field=models.ManyToManyField(blank=True, to='gallery.Category'),
        ),
        migrations.DeleteModel(
            name='AlbumCategory',
        ),
        migrations.DeleteModel(
            name='AlbumTag',
        ),
    ]
