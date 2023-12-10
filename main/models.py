import uuid

from django.contrib.admin.models import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def uuid_generator():
    return uuid.uuid4().hex


class UserBase(AbstractUser):
    id = models.TextField(primary_key=True, default=uuid_generator)
    company_name = models.CharField(_("Company"), max_length=128)

    class Meta(AbstractUser.Meta):
        pass
