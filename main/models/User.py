from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from main.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__spec_type_object = None

    def get_spec_type_object(self) -> 'BaseSpecType':
        if not self.__spec_type_object:
            self.__spec_type_object = self.basespectype.get_down_class()
        return self.__spec_type_object

    def is_executor(self) -> bool:
        return self.get_spec_type_object().is_executor()

    def is_customer(self) -> bool:
        return self.get_spec_type_object().is_customer()

    def is_private_customer(self) -> bool:
        return self.get_spec_type_object().is_private_customer()

    def is_corporate_customer(self) -> bool:
        return self.get_spec_type_object().is_corporate_customer()