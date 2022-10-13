from django.contrib import admin
from django.contrib.admin import display

from examination_management.grade.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    model = Grade

    list_display = ('get_roll_no', 'get_code', 'grade')
    # list_filter = ('get_roll_no', 'get_code', 'grade')

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.student.roll_no

    @display(ordering='code', description='Code')
    def get_code(self, obj):
        return obj.student.code

