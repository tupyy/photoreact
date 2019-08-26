from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityLog(models.Model):
    ACTIVITY_TYPE = (
        ('C', 'CREATE'),
        ('D', 'DELETE'),
        ('V', 'VIEW'),
        ('U', 'UPDATE')
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(verbose_name='object id')
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateTimeField(verbose_name='activity date', auto_now_add=True)
    activity = models.CharField(max_length=1, choices=ACTIVITY_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date',)
        verbose_name = 'activity log'
        verbose_name_plural = 'activities log'

    def __str__(self):
        return '{}_{}_{}'.format(self.activity,
                                 str(self.object_id),
                                 str(self.content_type))
