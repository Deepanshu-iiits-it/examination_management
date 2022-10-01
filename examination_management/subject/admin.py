from django.contrib import admin

from examination_management.subject.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    model = Subject

    # list_display = ('name', 'code',)
    # list_filter = ('name', 'code',)

