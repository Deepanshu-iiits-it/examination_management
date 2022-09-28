from django.contrib import admin

from examination_management.student.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student

    list_display = ('name', 'roll_no',)
    list_filter = ('name', 'roll_no',)

