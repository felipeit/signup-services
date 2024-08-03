from asgiref.sync import sync_to_async
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from domain.user import User as DomainUser


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")
        if not email:
            raise ValueError(_("Users must have an email address"))
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
    USERNAME_FIELD = "email"

    @classmethod
    async def signup(cls, user: DomainUser) -> None:  # Domain User
        # results = await sync_to_async(sync_function, thread_sensitive=True)(pk=123)

        user_orm = await sync_to_async(cls)(password=user.password, email=user.email)
        await sync_to_async(user_orm.set_password)(user_orm.password)
        await sync_to_async(user_orm.save)()
        user.id = user_orm.id

    @classmethod
    def change_password(cls, user: DomainUser) -> None:
        u = User.objects.get(id=user.id)
        u.set_password(u.password)
        u.save()

    @classmethod
    def get_user_by_id(cls, id: int) -> DomainUser | None:
        if user_orm := cls.objects.filter(id=id).first():
            return DomainUser(
                email=user_orm.email,
                password=user_orm.password,
                id=user_orm.id,
            )
        return user_orm

    @classmethod
    def delete_user_by_id(cls, id: int) -> str:
        if user_orm := cls.objects.filter(id=id).first():
            user_orm.delete()
            return "Usuário deletado com sucesso!"
        return "Usuário não encontrado!"
