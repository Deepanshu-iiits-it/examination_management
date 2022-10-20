from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter

from examination_management.branch.models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    model = Branch

    list_display = ('branch', 'code',)
    list_filter = (
        ('branch', DropdownFilter),
        ('code', DropdownFilter),
    )
