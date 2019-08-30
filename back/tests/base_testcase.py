import json

from django.test import TestCase
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    token = None

    def login(self, username, password):
        client = APIClient()
        response = client.post('/api/token/',
                               data=json.dumps({"username": username,
                                               "password": password}),
                               content_type="application/json")
        if response.status_code == 200:
            self.token = response.data['access']
            return True
        return False

    def get_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return client
