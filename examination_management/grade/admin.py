from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from examination_management.grade.api.v1.views import GradeTemplateDownloadView
from examination_management.grade.models import Grade
from examination_management.semester.models import SemesterInstance
from examination_management.student.models import Student
from examination_management.subject.models import Subject


class GradeResource(resources.ModelResource):
    student = fields.Field(column_name='student', attribute='student', widget=ForeignKeyWidget(Student, 'roll_no'))
    semester_instance = fields.Field(column_name='semester_instance', attribute='semester_instance',
                                     widget=ForeignKeyWidget(SemesterInstance, 'id'))
    subject = fields.Field(column_name='subject', attribute='subject', widget=ForeignKeyWidget(Subject, 'code'))

    class Meta:
        model = Grade

    def dehydrate_student(self, obj):
        if obj.semester_instance:
            return obj.semester_instance.student.roll_no


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin):
    resource_class = GradeResource

    list_display = ('student__roll_no', 'subject__code', 'grade')
    list_filter = ('semester_instance__semester__semester', 'semester_instance__student__branch__code',
                  'semester_instance__student__batch__start', 'subject__code')

    change_list_template = 'grade/grade_change_list.html'

    @display(ordering='roll_no', description='Roll No')
    def student__roll_no(self, obj):
        return obj.semester_instance.student.roll_no

    @display(ordering='code', description='Code')
    def subject__code(self, obj):
        return obj.subject.code

    def semester_instance__semester__semester(self, obj):
        return obj.semester_instance.semester.semester

    def subject__code(self, obj):
        return obj.subject.code

    def semester_instance__student__branch__code(self, obj):
        return obj.student.branch.code

    def semester_instance__student__batch__start(self, obj):
        return obj.student.batch.start

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', GradeTemplateDownloadView.as_view(), name='grade_template_download'),
        ]
        return admin_urls + urls

