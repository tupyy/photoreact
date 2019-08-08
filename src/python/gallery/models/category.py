from django.db import models

from gallery.models.album import Album


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class AlbumCategory(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "AlbumCategory" + self.album.name + "_" + self.category.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class AlbumTag(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return "AlbumTag: " + self.album.name + '_' + self.tag.name