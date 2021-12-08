from user.serializers import UserSerializer
from rest_framework import generics, authentication, permissions


class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user