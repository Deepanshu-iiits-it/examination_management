from django.contrib import admin
from django.contrib.admin import display
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

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


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin):
    resource_class = GradeResource

    list_display = ('get_roll_no', 'get_code', 'grade')
    # list_filter = ('get_roll_no', 'get_code', 'grade')

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.semester_instance.student.roll_no

    @display(ordering='code', description='Code')
    def get_code(self, obj):
        return obj.subject.code

