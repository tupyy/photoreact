from django.contrib.auth.models import User

from accounts.models import UserProfile, Role
from accounts.serializers import UserProfileSerializer
from tests.base_testcase import BaseTestCase


class AccountsTestCase(BaseTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('user', 'user@gallery', 'pass',
                                             first_name="john",
                                             last_name="Doe")
        self.user.save()

    def test_serializer(self):
        user_profile = UserProfile.objects.create(user=self.user,
                                                  photo_filename="foo.jpg")
        user_profile.save()
        role_user = Role.objects.create(id=1)
        user_profile.roles.add(role_user)

        serializer = UserProfileSerializer(user_profile)
        data = serializer.data
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertTrue(data["photo"] is not None)
        self.assertTrue(isinstance(data["roles"], list))
        self.assertTrue(data.get("password") is None)
        self.assertTrue(data.get("reset_password") is None)
