from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"
    ROLE_CHOICE = (
        (USER, "user"),
        (ADMIN, "admin"),
        (GUEST, "guest")
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICE, default=USER)

    def __str__(self):
        return self.role


class UserProfile(models.Model):
    ROMANIAN = 'RO'
    ENGLISH = 'EN'
    LangKey = (
        (ROMANIAN, "RO"),
        (ENGLISH, "EN")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_filename = models.CharField(max_length=100, verbose_name="profile_photo")
    lang_key = models.CharField(max_length=2, choices=LangKey, default=ROMANIAN)

    # True if the user has to reset its password upon next login
    reset_password = models.BooleanField(verbose_name="reset_password", default=False, auto_created=True)
    roles = models.ManyToManyField(Role)

    class Meta:
        ordering = ('user__username',)
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return "<UserProfile: {}>".format(self.user.username)

    def __repr__(self):
        return "<UserProfile: {}>".format(self.user.username)

