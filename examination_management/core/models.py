from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin, AddressMixin, PhoneMixin


class Country(models.Model):
    country = models.CharField(_('Country'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.country


class State(models.Model):
    state = models.CharField(_('State'), max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='country_state')

    def __str__(self):
        return self.state


class City(models.Model):
    city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True, related_name='state_city')

    def __str__(self):
        return self.city


class Address(StatusMixin, AddressMixin, TimeStampedModel):
    mobile = models.CharField(_('Mobile No'), max_length=10, blank=True, null=True)
    latitude = models.CharField(_('Latitude'), max_length=40, blank=True, null=True)
    longitude = models.CharField(_('Longitude'), max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.id)