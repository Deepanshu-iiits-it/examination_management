from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Student(StatusMixin, TimeStampedModel):
    # TODO:
    #  - Add branch

    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True, unique=True)
    roll_no = models.CharField(_('Roll Number'), max_length=100, unique=True,
                               null=True, blank=True, db_index=True)
    batch = models.OneToOneField('batch.Batch', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.roll_no
