from django.contrib import admin

from examination_management.grade.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    model = Grade

    list_display = ('student.roll_no', 'subject.code', 'grade')
    list_filter = ('student.roll_no', 'subject.code', 'grade')

