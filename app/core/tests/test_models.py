from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


CRED = {
    'email': 'test@hotmail.com',
    'password': 'testando123',
}


def sample_user(email=CRED['email'], password=CRED['password']):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_successful(self):

        user_type = 'Anunciante'
        
        user = get_user_model().objects.create_user(
            email=CRED['email'],
            password=CRED['password'],
        )

        self.assertEqual(user.email, CRED['email'])
        self.assertTrue(user.check_password(CRED['password']))
        self.assertEqual(user.groups.all()[0].name, user_type)

    def test_create_superuser_successful(self):
       
        user_type = 'Administrador'
        user = get_user_model().objects.create_superuser(
            email=CRED['email'],
            password=CRED['password'],

        )

        self.assertEqual(user.email, CRED['email'])
        self.assertTrue(user.check_password(CRED['password']))
        self.assertEqual(user.groups.all()[0].name, user_type)
        
    def test_new_user_email_normalized(self):
        """Teste email normalize"""
        email = 'test@HOTmail.com'

        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_create_user_fail(self):
        with self.assertRaises(ValueError):

            get_user_model().objects.create_user(None, 'test123')


    def test_demanda_str(self):
        """Testa a representação da string do model demanda"""
        demanda = models.Demanda.objects.create(
            anunciante=sample_user(),
            nome_peca='Nome peca',
            descricao_peca='Teste Desc',
            endereco='Rua test',
            info_contato='contato',
        )

        self.assertEqual(str(demanda), demanda.nome_peca)
