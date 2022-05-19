import re
import uuid as uuid
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
    _user_has_module_perms,
    _user_has_perm,
)


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        first_name,
        last_name,
        password,
        is_superuser,
        is_account_id,
    ):
        now = timezone.now()
        if not username:
            raise ValueError(_("The given username must be set"))
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            last_login=now,
            date_joined=now,
            is_superuser=is_superuser,
            is_account_id=is_account_id,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username,
        email=None,
        first_name=None,
        last_name=None,
        password=None,
        is_superuser=False,
        is_account_id=False,
    ):
        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            is_superuser,
            is_account_id,
        )

    def create_superuser(self, username, email, password):
        user = self._create_user(username, email, None, None, password, True, False)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uu = models.UUIDField(unique=True, default=uuid.uuid4)
    username = models.CharField(
        _("username"),
        max_length=100,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile("^[\w.@+-]+$"), _("Enter a valid username."), ("invalid")
            )
        ],
    )
    groups = models.ManyToManyField(
        Group, verbose_name=_("groups"), blank=True, related_query_name="user"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="tmp_user_set",
        related_query_name="user",
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, null=True, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_email_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class Company(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, related_name='company_user', null=True, blank=True, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.user}"
