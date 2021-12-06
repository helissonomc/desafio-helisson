from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Demanda

from demanda.serializers import DemandaSerializer

DEMANDAS_URL = reverse('demanda:demanda-list')

PAYLOAD = {
    'email': 'test@hotmail.com',
    'password':'testando123',
}

DEMANDA_DATA = [
    {
        'nome_peca':'cNome peca1',
        'descricao_peca':'cTeste Desc1',
        'endereco':'Rua test1',
        'info_contato':'contato1',
    },

    {
        'nome_peca':'bNome peca2',
        'descricao_peca':'bTeste Desc2',
        'endereco':'Rua test2',
        'info_contato':'contato2',
    },

    {
        'nome_peca':'aNome peca3',
        'descricao_peca':'aTeste Desc3',
        'endereco':'Rua test3',
        'info_contato':'contato3',
    },

]

def destroy_url(demanda_id):
    return reverse('demanda:demanda-detail', args=[demanda_id])

def update_url(demanda_id):
    return reverse('demanda:finalizar-detail', args=[demanda_id])
class PublicDemandasApiTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(DEMANDAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        

class PrivateDemanddasApiTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            PAYLOAD['email'],
            PAYLOAD['password'],
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_demandas(self):
        Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[2]['nome_peca'],
            descricao_peca=DEMANDA_DATA[2]['descricao_peca'],
            endereco=DEMANDA_DATA[2]['endereco'],
            info_contato=DEMANDA_DATA[2]['info_contato'],
        )

        Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
            descricao_peca=DEMANDA_DATA[0]['descricao_peca'],
            endereco=DEMANDA_DATA[0]['endereco'],
            info_contato=DEMANDA_DATA[0]['info_contato'],
        )
        
        Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[1]['nome_peca'],
            descricao_peca=DEMANDA_DATA[1]['descricao_peca'],
            endereco=DEMANDA_DATA[1]['endereco'],
            info_contato=DEMANDA_DATA[1]['info_contato'],
        )

        

        res = self.client.get(DEMANDAS_URL)
        demandas = Demanda.objects.all().order_by('id')

        serializer = DemandaSerializer(demandas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_demandas_only_user(self):
        """teste que usuario só pode listar suas próprias demandas"""
        user2 = get_user_model().objects.create_user(
            'user2@hotmail.com',
            PAYLOAD['password'],
        )

        Demanda.objects.create(
            anunciante=user2,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
            descricao_peca=DEMANDA_DATA[0]['descricao_peca'],
            endereco=DEMANDA_DATA[0]['endereco'],
            info_contato=DEMANDA_DATA[0]['info_contato'],
        )

        demanda = Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[1]['nome_peca'],
            descricao_peca=DEMANDA_DATA[1]['descricao_peca'],
            endereco=DEMANDA_DATA[1]['endereco'],
            info_contato=DEMANDA_DATA[1]['info_contato'],
        )

        res = self.client.get(DEMANDAS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nome_peca'], demanda.nome_peca)

    def test_create_demanda_successful(self):
        res = self.client.post(DEMANDAS_URL, DEMANDA_DATA[0])
        
        exist = Demanda.objects.filter(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
        )


        self.assertEqual(exist.get().nome_peca, DEMANDA_DATA[0]['nome_peca'])
        self.assertTrue(exist.exists())

    def test_create_demanda_fail(self):
        res = self.client.post(DEMANDAS_URL, {'user':self.user, 'nome_peca':''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_demanda(self):
        
        demanda = Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
            descricao_peca=DEMANDA_DATA[0]['descricao_peca'],
            endereco=DEMANDA_DATA[0]['endereco'],
            info_contato=DEMANDA_DATA[0]['info_contato'],
        )
        
        res = self.client.delete(destroy_url(demanda.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


    def test_update_demanda(self):
        demanda = Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
            descricao_peca=DEMANDA_DATA[0]['descricao_peca'],
            endereco=DEMANDA_DATA[0]['endereco'],
            info_contato=DEMANDA_DATA[0]['info_contato'],
        )

        res = self.client.put(destroy_url(demanda.id))

    def test_finalizar(self):
        demanda = Demanda.objects.create(
            anunciante=self.user,
            nome_peca=DEMANDA_DATA[0]['nome_peca'],
            descricao_peca=DEMANDA_DATA[0]['descricao_peca'],
            endereco=DEMANDA_DATA[0]['endereco'],
            info_contato=DEMANDA_DATA[0]['info_contato'],
        )
        self.assertEqual(demanda.status_finalizacao , False)
        
        res = self.client.put(update_url(demanda.id))
        
        self.assertTrue(res.data['status_finalizacao'])