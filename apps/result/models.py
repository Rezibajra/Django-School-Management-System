from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student
from apps.corecode.models import Mark

# from .utils import score_grade


# Create your models here.
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.FloatField(default=0)
    exam_score = models.FloatField(default=0)
    performance_score = models.FloatField(default=0)
    speaking_score = models.FloatField(default=0)
    listening_score = models.FloatField(default=0)
    full_score = models.FloatField(default=0, null=True, blank=True)
    equivalent_score = models.FloatField(default=0, null=True, blank=True)
    
    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    def total_score(self):
        return self.test_score + self.exam_score + self.performance_score + self.listening_score + self.speaking_score

    # def grade(self):
    #     return score_grade(self.total_score())

    
class FinalResult(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    first = models.FloatField(default=0)
    second = models.FloatField(default=0)
    third = models.FloatField(default=0)
    total = models.FloatField(default=0)

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"
