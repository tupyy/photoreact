from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from gallery.models.album import Album


class PermissionLog(models.Model):
    ADD = 0
    DELETE = 1
    MODIFY = 2
    OPERATION_TYPES = (
        (ADD, "add"),
        (DELETE, "delete"),
        (MODIFY, "modify")
    )

    # Use content type here because permission can be given to an user or a group
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(verbose_name='object id')
    content_object = GenericForeignKey('content_type', 'object_id')

    # user receiving the permission
    user_from = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="log date", auto_now_add=True)
    operation = models.CharField(max_length=15, choices=OPERATION_TYPES, default=ADD)

    class Meta:
        ordering = ('date',)
        verbose_name = "Permission log"
        verbose_name_plural = "Permission logs"

    def __str__(self):
        return '{}_{}_{}_{}'.format(self.user_from.username,
                                    str(self.content_type),
                                    str(self.object_id),
                                    self.permission.verbose_name)
