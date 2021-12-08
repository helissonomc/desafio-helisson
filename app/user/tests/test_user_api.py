from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

"""Setando variavel que será usada mutiplas vezes"""
CREATE_USER_URL = reverse('user:create')

TOKEN_URL = reverse('user:token')

CRED = {
    'email': 'test@hotmail.com',
    'password': 'testando123',
}


"""função para deixar a criação de user mais curta"""
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        """criando ussuário com sucesso"""
        res = self.client.post(CREATE_USER_URL, CRED)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(CRED['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """criando usuario que já existe"""

        create_user(**CRED)

        res = self.client.post(CREATE_USER_URL, CRED)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):

        res = self.client.post(
            CREATE_USER_URL,
            {
                'email': CRED['email'],
                'password': 'sd'
            }
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=CRED['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        create_user(**CRED)
        res = self.client.post(TOKEN_URL, CRED)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(
            email=CRED['email'],
            password='testando1234'
        )

        res = self.client.post(TOKEN_URL, CRED)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):

        res = self.client.post(TOKEN_URL, {'email': '', })
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reate_toke_missing_token(self):
        res = self.client.post(
            TOKEN_URL,
            {
                'email': CRED['email'],
                'password': ''
            }
        )
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)