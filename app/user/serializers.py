from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'min_length':5,
            }
        }

    def create(self, validate_data):
        """Cria novo usuario com senha encripitada e retorna"""

        return get_user_model().objects.create_user(**validate_data)

    def update(self, instance, validated_data):
        """Atualiza senha encripitada"""
        password = validated_data.pop('password', None)

        user  = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

        
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )
    #user_type = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        #user_type = attrs.get('user_type')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
            #user_type=user_type,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')


        attrs['user'] = user

        return attrs