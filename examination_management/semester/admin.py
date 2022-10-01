from django.contrib import admin

from examination_management.semester.models import Semester, SemesterInstance


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    model = Semester


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(admin.ModelAdmin):
    model = SemesterInstance
