from django.contrib import admin

from examination_management.branch.models import Branch


@admin.register(Branch)
class StudentAdmin(admin.ModelAdmin):
    model = Branch

    list_display = ('branch', 'code',)
    list_filter = ('branch', 'code',)
