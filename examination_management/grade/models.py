from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core import validators

from examination_management.core.behaviours import StatusMixin


class Grade(StatusMixin, TimeStampedModel):
    semester_instance = models.ForeignKey('semester.SemesterInstance', on_delete=models.CASCADE,
                                          blank=True, null=True, related_name='semester_instance_grade')
    subject = models.OneToOneField('subject.Subject', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='subject_grade')
    grade = models.CharField(_('Grade'), max_length=2, null=True, blank=True)

    score = models.IntegerField(_('Score'), null=True, blank=True, validators=[validators.MinValueValidator(0),
                                                                               validators.MaxValueValidator(100)])

    def __str__(self):
        return str(self.id)

