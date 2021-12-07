from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Demanda
from demanda import serializers
from .permissions import BlockAdministradorRequest

class DemandaGetInsertViewSet(viewsets.GenericViewSet, 
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, BlockAdministradorRequest)
    queryset = Demanda.objects.all()
    serializer_class = serializers.DemandaSerializer

    def get_queryset(self):
        """retona apenas demanadas do usuario"""
        return self.queryset.filter(anunciante=self.request.user).order_by('id')
    
    def perform_create(self, serializer):
        
        serializer.save(anunciante=self.request.user)

class DemandaFinilizarViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Demanda.objects.all()
    serializer_class = serializers.DemandaSerializer

    def get_queryset(self):
        """retona apenas demanadas do usuario"""
        return self.queryset.filter(anunciante=self.request.user).order_by('id')

    def update(self, request, **extra):
        data = self.get_queryset().get(id=extra['pk'])
        data.status_finalizacao = True
        data.save()
        serializer = self.serializer_class(data, many=False)
        return Response(serializer.data)

