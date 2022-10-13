from django.contrib import admin
from django.contrib.admin import display

from examination_management.semester.models import Semester, SemesterInstance


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    model = Semester

    list_display = ('semester',)
    list_filter = ('semester',)


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(admin.ModelAdmin):
    model = SemesterInstance

    list_display = ('get_roll_no', 'get_semester',)
    # list_filter = ('get_roll_no', 'get_semester',)

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.student.roll_no

    @display(ordering='semester', description='Semester')
    def get_semester(self, obj):
        return obj.semester.semster
