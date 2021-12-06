from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """ Cria e salva novos user"""
        if not email:
            raise ValueError("Must Have Email Adress")

        user = self.model(email=email.lower(),**extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)

        new_group, created = Group.objects.get_or_create(name='Anunciante')

        new_group.user_set.add(user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Cria super user e atribui o grupo 'Administrador ao usuário'"""

        user = self.create_user(email, password, **extra_fields)
        
        user.groups.clear()
        new_group, created = Group.objects.get_or_create(name='Administrador')
        new_group.user_set.add(user)

        user.is_staff = True

        user.is_superuser = True
        user.save(using=self._db)
  
        return user



class User(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Demanda(models.Model):

    anunciante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    nome_peca = models.CharField(max_length=255, null=False)
    descricao_peca = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, null=False)
    info_contato = models.CharField(max_length=255, null=False)
    status_finalizacao  = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_peca