from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model

PAYLOAD = {
    'email': 'test@hotmail.com',
    'password':'testando123',
}


class ModelTests(TestCase):

    def test_create_user_successful(self):
        user_type = 'Anunciante'
        
        user = get_user_model().objects.create_user(
            email = PAYLOAD['email'],
            password = PAYLOAD['password'],
        )

        self.assertEqual(user.email, PAYLOAD['email'])
        self.assertTrue(user.check_password(PAYLOAD['password']))
        self.assertEqual(user.groups.all()[0].name, user_type)

    def test_create_superuser_successful(self):
       
        user_type = 'Administrador'
        user = get_user_model().objects.create_superuser(
            email = PAYLOAD['email'],
            password = PAYLOAD['password'],

        )

        self.assertEqual(user.email, PAYLOAD['email'])
        self.assertTrue(user.check_password(PAYLOAD['password']))
        self.assertEqual(user.groups.all()[0].name, user_type)
        
    def test_new_user_email_normalized(self):
        """Teste email normalize"""
        email = 'test@HOTmail.com'

        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())



    def test_create_user_fail(self):
        with self.assertRaises(ValueError):

            get_user_model().objects.create_user(None, 'test123')


    

