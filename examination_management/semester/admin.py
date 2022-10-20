from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from examination_management.semester.api.v1.view import SemesterInstanceTemplateDownloadView
from examination_management.semester.models import Semester, SemesterInstance
from examination_management.student.models import Student


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    model = Semester

    list_display = ('code', 'semester',)
    list_filter = ('code', 'semester',)


class SemesterInstanceResource(resources.ModelResource):
    student = fields.Field(column_name='student', attribute='student', widget=ForeignKeyWidget(Student, 'roll_no'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'code'))

    class Meta:
        model = SemesterInstance


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(ImportExportModelAdmin):
    resource_class = SemesterInstanceResource

    list_display = ('get_roll_no', 'get_semester',)
    # list_filter = ('get_roll_no', 'get_semester',)

    change_list_template = 'semester/semester_instance_change_list.html'

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.student.roll_no

    @display(ordering='semester', description='Semester')
    def get_semester(self, obj):
        return obj.semester.semester

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', SemesterInstanceTemplateDownloadView.as_view(), name='semester_instance_template_download'),
        ]
        return admin_urls + urls
