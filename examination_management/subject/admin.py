from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter

from examination_management.subject.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    model = Subject

    list_display = ('name', 'code',)
    list_filter = (
        ('subject_semester__semester', DropdownFilter),
    )

    def subject_semester__semester(self, obj):
        return obj.subject_semester.semester
