from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from django_admin_listfilter_dropdown.filters import DropdownFilter
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from examination_management.semester.api.v1.view import SemesterInstanceTemplateDownloadView, \
    SemesterTemplateDownloadView
from examination_management.semester.models import Semester, SemesterInstance
from examination_management.student.models import Student
from examination_management.subject.models import Subject


class SemesterResource(resources.ModelResource):
    subject = fields.Field(column_name='subject', attribute='subject', widget=ManyToManyWidget(Subject, field='code', separator=','))

    class Meta:
        model = Semester
        exclude = ('id',)
        import_id_fields = ('code',)


@admin.register(Semester)
class SemesterAdmin(ImportExportModelAdmin):
    resource_class = SemesterResource

    list_display = ('code', 'semester',)
    list_filter = (
        ('code', DropdownFilter),
        ('semester', DropdownFilter),
    )
    change_list_template = 'semester/semester_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', SemesterTemplateDownloadView.as_view(), name='semester_template_download'),
        ]
        return admin_urls + urls


class SemesterInstanceResource(resources.ModelResource):
    student = fields.Field(column_name='student', attribute='student', widget=ForeignKeyWidget(Student, 'roll_no'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'code'))

    class Meta:
        model = SemesterInstance


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(ImportExportModelAdmin):
    resource_class = SemesterInstanceResource

    list_display = ('get_roll_no', 'get_semester',)
    list_filter = (
        ('student__roll_no', DropdownFilter),
        ('semester__semester', DropdownFilter),
        ('student__batch__start', DropdownFilter),
        ('student__branch__code', DropdownFilter)
    )

    change_list_template = 'semester/semester_instance_change_list.html'

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.student.roll_no

    @display(ordering='semester', description='Semester')
    def get_semester(self, obj):
        return obj.semester.semester

    def student__roll_no(self, obj):
        return obj.student.roll_no

    def semester__semester(self, obj):
        return obj.semester.semester

    def student__batch__start(self, obj):
        return obj.student.batch.start

    def student__branch__code(self, obj):
        return obj.student.branch.code

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', SemesterInstanceTemplateDownloadView.as_view(), name='semester_instance_template_download'),
        ]
        return admin_urls + urls
