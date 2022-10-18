from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core import validators

from examination_management.core.behaviours import StatusMixin
from examination_management.grade.strategy.score_calculation_strategy import DefaultScoreCalculationStrategy
from examination_management.grade.strategy.score_calculator import ScoreCalculator


class Grade(StatusMixin, TimeStampedModel):
    semester_instance = models.ForeignKey('semester.SemesterInstance', on_delete=models.CASCADE,
                                          blank=True, null=True, related_name='semester_instance_grade')
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE,
                                blank=True, null=True, related_name='subject_grade')
    grade = models.CharField(_('Grade'), max_length=2, null=True, blank=True)

    score = models.IntegerField(_('Score'), null=True, blank=True, validators=[validators.MinValueValidator(0),
                                                                               validators.MaxValueValidator(100)])

    def save(self, *args, **kwargs):
        score_calculator = ScoreCalculator(DefaultScoreCalculationStrategy())

        # Ref: How to create/update scores:
        # 1. Get semester_instance and subtract the current subject's score
        # 2. Calculate the updated score
        # 3. Update the score in semester_instance
        # 4. Update the semester_instance status
        # 4. Save the semester_instance
        # 5. Save the grade instance

        old_score = self.score or 0
        self.score = score_calculator.calculate(self.subject.credit, self.grade)
        new_score = self.score
        self.semester_instance.update_cg_sum(old_subject_score=old_score, new_subject_score=new_score)

        super(Grade, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

