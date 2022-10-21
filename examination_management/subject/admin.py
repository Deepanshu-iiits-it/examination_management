from django.contrib import admin
from django.urls import path
from django_admin_listfilter_dropdown.filters import DropdownFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from examination_management.subject.api.v1.views import SubjectTemplateDownloadView
from examination_management.subject.models import Subject


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        exclude = ('id',)
        import_id_fields = ('code',)


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource

    list_display = ('name', 'code',)
    list_filter = ('subject_semester__semester',)

    change_list_template = 'subject/subject_change_list.html'

    def subject_semester__semester(self, obj):
        return obj.subject_semester.semester

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', SubjectTemplateDownloadView.as_view(), name='subject_template_download'),
        ]
        return admin_urls + urls
