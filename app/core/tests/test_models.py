from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_successful(self):
        email = 'user1@hotmail.com'
        password = 'password123'
        user_type = 'Anunciante'
        
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.user_type, user_type)

    def test_create_superuser_successful(self):
        email = 'super1@hotmail.com'
        password = 'password123'  
        user_type = 'Administrador'
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password,
            user_type = user_type,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.user_type, user_type)

    def test_new_user_email_normalized(self):
        """Teste email normalize"""
        email = 'test@HOTmail.com'
        user_type = 'Anunciante'
        user = get_user_model().objects.create_user(email, 'test123', user_type=user_type)

        self.assertEqual(user.email, email.lower())


    def test_create_user_fail(self):
        with self.assertRaises(ValueError):
            user_type = 'Anunciante'
            get_user_model().objects.create_user(None, 'test123', user_type=user_type)


    

