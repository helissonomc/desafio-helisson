from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

"""Setando variavel que será usada mutiplas vezes"""
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reversed('user:me')

PAYLOAD = {
    'email': 'test@hotmail.com',
    'password':'testando123',
}


"""função para deixar a criação de user mais curta"""
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        

        res = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue (user.check_password(PAYLOAD['password']))
        self.assertEqual(user.user_type, 'Anunciante')
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """criando usuario que já existe"""

        create_user(**PAYLOAD)

        res = self.client.post(CREATE_USER_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):


        res = self.client.post(CREATE_USER_URL, {'email':PAYLOAD['email'], 'password':'sd'})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        
        user_exists = get_user_model().objects.filter(
            email=PAYLOAD['email']
        ).exists()
        
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):


        create_user(**PAYLOAD)
        res = self.client.post(TOKEN_URL, PAYLOAD)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_token_invalid_credentials(self):
        create_user(email=PAYLOAD['email'], 
                    password='testando1234')

        

        res = self.client.post(TOKEN_URL, PAYLOAD)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):

        res = self.client.post(TOKEN_URL, PAYLOAD)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reate_toke_missing_token(self):
        res = self.client.post(TOKEN_URL, {'email':PAYLOAD['email'], 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
'''
    def test_retrieve_user_unauthorized(self):
        
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Testa requests que precisam de atorização"""

    def setUp(self):
        self.user = create_user(
            email='test@hotmail.com',
            password='teste123'
        )

        self.client = APIClient()

        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_profile_success(self):
        
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'email':self.user.email
        })

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):

        payload = {'password':'newpassword123'}  

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password'])) 
        self.assertEqual(res.status_code, status.HTTP_200_OK)'''