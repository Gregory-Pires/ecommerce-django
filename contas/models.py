from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from cpf_field.models import CPFField

# Create your models here.

class MyContaManager(BaseUserManager):
    def create_user(self, nome, sobrenome, nome_usuário, email, numero_telefone, cpf,password=None):
        if not email:
            raise ValueError('Usuário deve ter um endereço de email')
      
        if not nome_usuário:
           raise ValueError('Usuário deve ter um nome de usuário')
        
        user = self.model(
           email = self.normalize_email(email),
           nome_usuário = nome_usuário,
           nome = nome,
           sobrenome = sobrenome,
           numero_telefone = numero_telefone,
           cpf = cpf,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nome, sobrenome, email, nome_usuário, password):
        user = self.create_user(
           email = self.normalize_email(email),
           nome_usuário = nome_usuário,
           password = password,
           nome = nome,
           sobrenome = sobrenome,        
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Conta(AbstractBaseUser):
    nome            = models.CharField(max_length=50)
    sobrenome       = models.CharField(max_length=50)
    nome_usuário    = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    numero_telefone = models.CharField(max_length=50)
    cpf             = models.CharField(max_length=11, unique=True)

    #requerid
    data_cadastro   = models.DateTimeField(auto_now_add=True)
    ultimo_login    = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuário', 'nome', 'sobrenome']

    objects = MyContaManager()

    def __str__(self):
     return self.email

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, add_label):
       return True