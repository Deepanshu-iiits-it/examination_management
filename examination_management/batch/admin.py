from django.contrib import admin
from django.urls import path

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from examination_management.batch.api.v1.views import BatchTemplateDownloadView
from examination_management.batch.models import Batch


class BatchResource(resources.ModelResource):
    class Meta:
        model = Batch


@admin.register(Batch)
class BatchAdmin(ImportExportModelAdmin):
    resource_class = BatchResource
    change_list_template = 'batch/batch_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', BatchTemplateDownloadView.as_view(), name='batch_template_download'),
        ]
        return admin_urls + urls
