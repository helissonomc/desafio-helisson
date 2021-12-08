from user.serializers import UserSerializer
from rest_framework import generics, authentication, permissions


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer