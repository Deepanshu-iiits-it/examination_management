from django.contrib import admin

from examination_management.semester.models import Semester, SemesterInstance


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    model = Semester

    list_display = ('semester',)
    list_filter = ('semester',)


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(admin.ModelAdmin):
    model = SemesterInstance

    list_display = ('student.roll_no', 'semester.semester',)
    list_filter = ('student.roll_no', 'semester.semester',)
