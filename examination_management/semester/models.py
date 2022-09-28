from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Semester(StatusMixin, TimeStampedModel):
    # TODO:
    #   - Subject

    semester = models.IntegerField(_('Semester'), null=True, blank=True)

    STATUS_CHOICES = (('A', 'Appearing'), ('P', 'Passed'), ('R', 'Reappear'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, blank=True, null=True)

    def __str__(self):
        return str(self.semester)
