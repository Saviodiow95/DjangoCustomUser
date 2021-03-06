from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Os usuários devem ter um endereço de email')
        if not username:
            raise ValueError('Os usuários devem ter um nome de usuário')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(verbose_name='nome', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='sobrenome', max_length=150, blank=True)
    photo = models.ImageField(upload_to='user_photo', verbose_name='Foto', null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='data de entrada', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='ultimo login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    # Para verificar permissões. para simplificar todos os administradores têm TODAS as permissões
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Este usuário tem permissão para visualizar este aplicativo? (SEMPRE SIM POR SIMPLICIDADE)
    def has_module_perms(self, app_label):
        return True
