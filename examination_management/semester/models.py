from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Semester(StatusMixin, TimeStampedModel):
    # TODO:
    #   - Subject

    semester = models.IntegerField(_('Semester'), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class SemesterInstance(StatusMixin, TimeStampedModel):
    # TODO:
    #   - Result

    semester = models.ForeignKey('semester.Semester', on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name='semester_semester_instance')
    student = models.ForeignKey('student.Student', on_delete=models.SET_NULL, blank=True,
                                null=True, related_name='student_semester_instance')
    STATUS_CHOICES = (('A', 'Appearing'), ('P', 'Passed'), ('R', 'Reappear'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, blank=True, null=True)

    def __str__(self):
        return str(self.id)
