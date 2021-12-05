from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

"""Setando variavel que será usada mutiplas vezes"""
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reversed('user:me')

"""função para deixar a criação de user mais curta"""
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        payload = {
            'email': 'test@hotmail.com',
            'password':'testando123',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue (user.check_password(payload['password']))
        self.assertEqual(user.user_type, 'Anunciante')
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """criando usuario que já existe"""
        payload = {
            'email': 'test@hotmail.com',
            'password':'testando123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@hotmail.com',
            'password':'sd',

        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {
            'email': 'test@hotmail.com',
            'password':'testando123',

        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_token_invalid_credentials(self):
        create_user(email='test@hotmail.com', 
                    password='testando1234')

        
        payload = {
            'email': 'test@hotmail.com',
            'password':'testando123',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': 'test@hotmail.com',
            'password':'testando123',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reate_toke_missing_token(self):
        res = self.client.post(TOKEN_URL, {'email':'email', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)