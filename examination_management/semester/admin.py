from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from django.utils.translation import gettext_lazy as _

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from examination_management.semester.api.v1.view import SemesterInstanceTemplateDownloadView, \
    SemesterTemplateDownloadView
from examination_management.semester.models import Semester, SemesterInstance
from examination_management.student.models import Student
from examination_management.subject.models import Subject


class SemesterResource(resources.ModelResource):
    subject = fields.Field(column_name='subject', attribute='subject',
                           widget=ManyToManyWidget(Subject, field='code', separator=','))

    class Meta:
        model = Semester
        exclude = ('id',)
        import_id_fields = ('code',)


@admin.register(Semester)
class SemesterAdmin(ImportExportModelAdmin):
    resource_class = SemesterResource

    list_display = ('code', 'semester',)
    list_filter = ('code', 'semester')

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
        import_id_fields = ('student', 'semester',)


class SemesterInstanceReappearListFilter(admin.SimpleListFilter):
    title = _('Reappear')
    parameter_name = 'reappear'

    def lookups(self, request, model_admin):
        return (
            ('odd', _('Odd semester')),
            ('even', _('Even semester'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'odd':
            return queryset.filter(status='R', semester__semester__iregex='[1357]')
        elif self.value() == 'even':
            return queryset.filter(status='R', semester__semester__iregex='[2468]')


@admin.register(SemesterInstance)
class SemesterInstanceAdmin(ImportExportModelAdmin):
    resource_class = SemesterInstanceResource

    list_display = ('get_name', 'get_roll_no', 'get_semester', 'get_batch', 'get_branch', 'status')
    list_filter = ('student__roll_no', 'semester__semester',
                   'student__batch__start', 'student__branch__code',
                   SemesterInstanceReappearListFilter,)

    change_list_template = 'semester/semester_instance_change_list.html'

    @display(ordering='name', description='Name')
    def get_name(self, obj):
        return obj.student.name

    @display(ordering='roll_no', description='Roll No')
    def get_roll_no(self, obj):
        return obj.student.roll_no

    @display(ordering='semester', description='Semester')
    def get_semester(self, obj):
        return obj.semester.semester

    @display(ordering='batch', description='Batch')
    def get_batch(self, obj):
        return obj.student.batch.start

    @display(ordering='branch', description='Branch')
    def get_branch(self, obj):
        return obj.student.branch.code

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
            path('download/', SemesterInstanceTemplateDownloadView.as_view(),
                 name='semester_instance_template_download'),
        ]
        return admin_urls + urls
