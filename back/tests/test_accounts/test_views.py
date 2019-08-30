from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import UserProfile, Role
from tests.base_testcase import BaseTestCase


class AccountViewTest(BaseTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('user', 'user@gallery', 'pass',
                                             first_name="john",
                                             last_name="Doe")
        self.user.save()
        user_profile = UserProfile.objects.create(user=self.user,
                                                  photo_filename="foo.jpg")
        user_profile.save()
        role_user = Role.objects.create(id=1)
        user_profile.roles.add(role_user)

    def test_get_profile(self):
        """
        Description: Get profile
        API: /profile/
        Method: GET
        Date: 29/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: current user profile
        """
        self.login('user', 'pass')
        client = self.get_client()
        response = client.get(reverse('accounts-get_profile'))
        self.assertTrue(response.status_code, 200)
        data = response.data
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertTrue(data["photo"] is not None)
        self.assertTrue(isinstance(data["roles"], list))
        self.assertTrue(data.get("password") is None)
        self.assertTrue(data.get("reset_password") is None)

    def test_put_profile(self):
        """
        Description: Update test
        API: /profile/
        Method: PUT
        Date: 29/08/2019
        User: cosmin
        Expected return code: 200
        Expected values: updated user profile
        """
        self.login('user', 'pass')
        client = self.get_client()
        data = dict()
        data['first_name'] = "toto"
        data['last_name'] = 'toto'
        data['email'] = 'toto@toto.com'
        response = client.put(reverse('accounts-get_profile'), data=data, format='json')
        self.assertTrue(response.status_code, 200)
        profile = response.data
        self.assertEqual(profile['first_name'], data['first_name'])
        self.assertEqual(profile['last_name'], data['last_name'])
        self.assertEqual(profile['email'], data['email'])

    def test_put_profile2(self):
        """
        Description: Update model  with bad data
        API: /profile/
        Method: PUT
        Date: 29/08/2019
        User: cosmin
        Expected return code: 400
        Expected values:
        """
        self.login('user', 'pass')
        client = self.get_client()
        data = dict()
        data['first_name'] = ""
        data['last_name'] = 'toto'
        data['email'] = 'toto@toto.com'
        response = client.put(reverse('accounts-get_profile'), data=data, format='json')
        self.assertTrue(response.status_code, 400)

    def test_sign_photo(self):
        """
        Description: Test sign profile photo prior to S3 upload
        API: /accounts/photo/sign/
        Method: POST
        Date: 30/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login('user', 'pass')
        client = self.get_client()
        data = dict()
        data['filename'] = "foo.bar"
        response = client.post(reverse('accounts-photo-sign'), data=data, format="json")
        self.assertTrue(response.status_code, 200)
        self.assertTrue('foo.bar' in response.data['url'])

    def test_post_photo(self):
        """
        Description: Post photo after uploading to S3
        API: /accounts/photo/
        Method: POST
        Date: 30/08/2019
        User: cosmin
        Expected return code: 200
        Expected values:
        """
        self.login('user', 'pass')
        client = self.get_client()
        data = dict()
        data['filename'] = "foo.bar"
        response = client.post(reverse('accounts-save-photo'), data=data, format="json")
        self.assertTrue(response.status_code, 200)
