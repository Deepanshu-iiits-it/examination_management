from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Grade(StatusMixin, TimeStampedModel):
    student = models.OneToOneField('student.Student', on_delete=models.CASCADE, blank=True, null=True)
    subject = models.OneToOneField('subject.Subject', on_delete=models.CASCADE, blank=True, null=True)
    grade = models.CharField(_('Grade'), max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

