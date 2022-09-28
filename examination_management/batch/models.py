import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class Batch(StatusMixin, TimeStampedModel):
    start = models.IntegerField(_('Start Year'), choices=year_choices(), default=current_year())
    end = models.IntegerField(_('End Year'), choices=year_choices(), default=current_year())
