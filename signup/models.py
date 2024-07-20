from django.db import models 
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from domain.user import User


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")
        if not email:
            raise ValueError(_('Users must have an email address'))
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    objects = EmailUserManager()
    USERNAME_FIELD = 'email'

    @classmethod
    def signup(cls, user:User) -> None: # Domain User
        user_orm = cls(password=user.password, email=user.email)
        user_orm.save()
        user.id = user_orm.id