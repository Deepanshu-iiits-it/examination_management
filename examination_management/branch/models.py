from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Branch(StatusMixin, TimeStampedModel):
    branch = models.CharField(_('Branch'), max_length=200, blank=True, null=True)
    code = models.CharField(_('Code'), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.code
