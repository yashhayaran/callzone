import uuid
from common.models import uuid_generator
from django.contrib.admin.models import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserBase(AbstractUser):
    id = models.TextField(primary_key=True, default=uuid_generator)
    company_name = models.CharField(_("Company"), max_length=128)

    class Meta(AbstractUser.Meta):
        pass
