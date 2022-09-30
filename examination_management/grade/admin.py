from django.contrib import admin

from examination_management.grade.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    model = Grade

