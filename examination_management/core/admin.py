from django.contrib import admin
from django.db import models

from import_export.admin import ImportExportModelAdmin

from examination_management.core.models import Country, City, State, Address


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    model = Country


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    model = City


@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    model = State


@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    model = Address