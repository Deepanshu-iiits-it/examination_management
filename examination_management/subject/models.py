from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core import validators

from examination_management.core.behaviours import StatusMixin


class Subject(StatusMixin, TimeStampedModel):
    code = models.CharField(_('Code'), max_length=100,primary_key=True)
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    credit = models.IntegerField(_('Credit'), null=True, blank=True, default=0,
                                 validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)])
    semester = models.ForeignKey('semester.Semester', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        # TODO: Find a way to find old and new credit
        old_credit = self.credit
        new_credit = kwargs.get('credit', 0)
        self.semester.update_credit(old_subject_credit=old_credit, new_subject_credit=new_credit)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.code)
