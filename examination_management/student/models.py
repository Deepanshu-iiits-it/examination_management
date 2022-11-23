from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Student(StatusMixin, TimeStampedModel):
    roll_no = models.CharField(_('Roll Number'), max_length=100, primary_key=True)
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True, unique=True)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, blank=True, null=True)
    fathers_name = models.CharField(_('Fathers Name'), max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.roll_no)

class SerialNo(StatusMixin, TimeStampedModel):
    serial_no = models.IntegerField(_("Serial No"), default = 2022)