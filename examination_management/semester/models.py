from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.grade.models import Grade
from examination_management.core.behaviours import StatusMixin
from examination_management.semester.strategy.semester_status_context import SemesterStatusContext
from examination_management.semester.strategy.semester_status_strategy import DefaultSemesterStatusStrategy


class Semester(StatusMixin, TimeStampedModel):
    code = models.CharField(_('Code'), max_length=100, primary_key=True)
    semester = models.IntegerField(_('Semester'), null=True, blank=True)
    credit = models.IntegerField(_('Credit'), default=0)
    subject = models.ManyToManyField('subject.Subject', related_name='subject_semester')

    def update_credit(self):
        credit = 0
        for subject in self.subject.all():
            credit += subject.credit
        self.credit = credit

    def save(self, *args, **kwargs):
        self.update_credit()
        super(Semester, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.code)


class SemesterInstance(StatusMixin, TimeStampedModel):
    # TODO:
    #   - Calculate total cg_sum

    semester = models.ForeignKey('semester.Semester', on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name='semester_semester_instance')
    student = models.ForeignKey('student.Student', on_delete=models.SET_NULL, blank=True,
                                null=True, related_name='student_semester_instance')
    STATUS_CHOICES = (('A', 'Appearing'), ('P', 'Passed'), ('R', 'Reappear'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='A')
    cg_sum = models.IntegerField(_('CG Sum'), default=0)

    def save(self, *args, **kwargs):
        semester = self.semester.semester
        student = self.student.roll_no

        semester_instance = SemesterInstance.objects.get(semester__semester=semester, student__roll_no=student)
        if semester_instance.id != self.id:
            raise ValueError('Student already registered with in this semester.')
        super(SemesterInstance, self).save(*args, **kwargs)

    def update_cg_sum(self, old_subject_score, new_subject_score):
        # Ref: How to update cg_sum
        # 1. Subtract old subject score
        # 2. Add new subject score
        # 3. Update semester status

        self.cg_sum -= old_subject_score
        self.cg_sum += new_subject_score

        subject_instances = SemesterInstance.objects.get(id=self.id).semester.subject
        expected_grades = len(self.semester.subject.all())
        grades = []
        for subject in subject_instances.all():
            grades.append(Grade.objects.get(semester_instance=self.id, subject=subject.code).grade)
        
        if len(grades) == expected_grades:
            semester_status_context = SemesterStatusContext(DefaultSemesterStatusStrategy())
            self.status = semester_status_context.evaluate(grades)

        self.save()

    def __str__(self):
        return str(self.id)
