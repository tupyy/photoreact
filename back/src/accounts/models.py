from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    USER = 1,
    ADMIN = 2,
    GUEST = 3
    ROLE_CHOICE = (
        (USER, "user"),
        (ADMIN, "admin"),
        (GUEST, "guest")
    )
    id = models.PositiveIntegerField(choices=ROLE_CHOICE, primary_key=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_photo_filepath = models.CharField(verbose_name="profile_photo")

    # True if the user has to reset its password upon next login
    reset_password = models.BooleanField(verbose_name="reset_password")
    roles = models.ManyToManyField(Role)

    class Meta:
        ordering = ('user__name',)
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return "User_{}_".format(self.user.username)

    @property
    def display_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_login)
