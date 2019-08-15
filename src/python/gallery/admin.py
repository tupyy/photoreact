from django.contrib import admin
from gallery.models.album import Album
from gallery.models.photo import Photo, Video
from gallery.models.category import Category, Tag

admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Tag)
