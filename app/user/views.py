from django.shortcuts import render
from user.serializers import AuthTokenSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, serializers, authentication, permissions


class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES