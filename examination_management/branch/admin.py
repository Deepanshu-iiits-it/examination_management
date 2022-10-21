from django.contrib import admin
from django.urls import path
from django_admin_listfilter_dropdown.filters import DropdownFilter

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from examination_management.branch.api.v1.views import BranchTemplateDownloadView
from examination_management.branch.models import Branch


class BranchResource(resources.ModelResource):
    class Meta:
        model = Branch


@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin):
    resource_class = BranchResource
    change_list_template = 'branch/branch_change_list.html'

    list_display = ('branch', 'code',)
    list_filter = (
        ('branch', DropdownFilter),
        ('code', DropdownFilter),
    )

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', BranchTemplateDownloadView.as_view(), name='branch_template_download'),
        ]
        return admin_urls + urls
