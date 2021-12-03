from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

class UserManager(BaseUserManager):

    def create_user(self, email, password, user_type, **extra_fields):
        """ Cria e salva novos user"""
        if not email:
            raise ValueError("Must Have Email Adress")

        user = self.model(email=email.lower(), user_type=user_type,**extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, user_type='Administrador', **extra_fields):
        """Cria super user e atribui o grupo 'Administrador ao usuário'"""

        user = self.create_user(email, password, user_type)
        user.is_staff = True

        user.is_superuser = True
        user.save(using=self._db)
  
        return user

class User(AbstractBaseUser, PermissionsMixin):
    TYPES = (
        ('Administrador', 'Administrador'),
        ('Anunciante', 'Anunciante'),
    )


    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=100, choices=TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    objects = UserManager()

    USERNAME_FIELD = 'email'