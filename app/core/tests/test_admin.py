from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

CRED = {
    'email': 'test@hotmail.com',
    'password': 'testando123',
}


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email=CRED['email'],
            password=CRED['password'],
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testauser@hotmail.com',
            password=CRED['password'],
        )

    def test_users_listed(self):
        """listagem de usuários em admin page"""
        url = reverse('admin:core_user_changelist')
       
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """acessar pagina do user edit page funciona"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)


        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """pagina de criar usuário"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)