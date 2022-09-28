from django.contrib import admin

from examination_management.semester.models import Semester


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    model = Semester
