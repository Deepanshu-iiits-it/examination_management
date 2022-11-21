from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.grade.models import Grade
from examination_management.core.behaviours import StatusMixin
from examination_management.semester.strategy.semester_status_context import SemesterStatusContext
from examination_management.semester.strategy.semester_status_strategy import DefaultSemesterStatusStrategy
from examination_management.subject.models import Subject


class Semester(StatusMixin, TimeStampedModel):
    code = models.CharField(_('Code'), max_length=100, primary_key=True)
    semester = models.IntegerField(_('Semester'))
    subject = models.ManyToManyField('subject.Subject', related_name='subject_semester')

    def __str__(self):
        return str(self.code)


class SemesterInstance(StatusMixin, TimeStampedModel):
    # TODO:
    #   - Calculate total cg_sum

    semester = models.ForeignKey('semester.Semester', on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name='semester_semester_instance')
    student = models.ForeignKey('student.Student', on_delete=models.SET_NULL, blank=True,
                                null=True, related_name='student_semester_instance')
    elective = models.ManyToManyField('subject.Subject', related_name='elective_semester_instance')
    
    STATUS_CHOICES = (('A', 'Appearing'), ('P', 'Passed'), ('R', 'Reappear'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='A')
    cg_sum = models.IntegerField(_('CG Sum'), default=0)

    def save(self, *args, **kwargs):
        semester = self.semester.semester
        student = self.student.roll_no
        try:
            semester_instance = SemesterInstance.objects.get(student__roll_no=student, status='A',
                                                             semester__semester__lt=semester)
            if semester_instance:
                semester_instance[-1].status = 'P'
                semester_instance[-1].save()

        except SemesterInstance.DoesNotExist:
            pass

        super(SemesterInstance, self).save(*args, **kwargs)

    def check_electives(self, semester_code):
        elective_instances = Subject.objects.filter(subject_semester__code=semester_code, is_elective=True)
        for elective in self.elective.all():
            if elective not in elective_instances.all():
                raise ValueError(f'The elective with code {elective.code} does not exist in semester {self.semester.semester}')

    def update_cg_sum(self, old_subject_score, new_subject_score):
        # Ref: How to update cg_sum
        # 1. Subtract old subject score
        # 2. Add new subject score
        # 3. Update semester status

        self.cg_sum -= old_subject_score
        self.cg_sum += new_subject_score

        has_reappear = False
        try:
            grades = Grade.objects.filter(semester_instance=self.id)
            for grade in grades.all():
                if grade.grade == 'F':
                    has_reappear = True
        except Grade.DoesNotExist:
            pass

        safe_status = 'A'
        if not has_reappear:
            try:
                semester_instances = SemesterInstance.objects.get(student=self.student, semester__semester__gt=self.semester.semester)
                if len(semester_instances.all()):
                    safe_status = 'P'
            except SemesterInstance.DoesNotExist:
                pass
        self.status = 'R' if has_reappear else safe_status
        self.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = (('student', 'semester'),)
