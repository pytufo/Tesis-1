from django.test import TestCase

import json

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User


class AccountTest(TestCase):
    def setUp(self):
        usr = User(
            username="vallejo",
            email="pytufo@mail.com",
        )
        usr.set_password("3Nano094")
        usr.save()

    def test_registro(self):
        client = APIClient()
        response = client.post(
            "/account/sign_up/",
            {"username": "test1", "email": "test@example.com", "password": "Ñ>123`fr~"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "username": "test1",
                "email": "test@example.com",
            },
        )

    def test_login(self):
        client = APIClient()
        response = client.post(
            "/account/login/",
            {"email": "pytufo@mail.com", "password": "3Nano094"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = json.loads(response.content)
        self.assertIn("access_token", result)
