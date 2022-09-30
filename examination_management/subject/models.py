from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Subject(StatusMixin, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    credit = models.IntegerField(_('Credit'), null=True, blank=True)
    code = models.CharField(_('Code'), max_length=100, unique=True,
                               null=True, blank=True, db_index=True)
    
    def __str__(self):
        return self.code
