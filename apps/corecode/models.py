from django.db import models
from ..users.models import CustomUser

# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    TERM_CHOICES = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
        ('Final Result', 'Final Result'),
    ]
    WEIGHTAGE_DIVISION_CHOICES = [
        ('10%', '10%'),
        ('20%', '20%'),
        ('30%', '30%'),
        ('40%', '40%'),
        ('50%', '50%'),
        ('60%', '60%'),
        ('70%', '70%'),
        ('80%', '80%'),
    ]
    name = models.CharField(
        max_length=20,
        choices=TERM_CHOICES,
    )
    current = models.BooleanField(default=True)
    first_weightage = models.CharField(
        max_length=4,
        choices=WEIGHTAGE_DIVISION_CHOICES,
        null=True,
        blank=True

    )
    second_weightage = models.CharField(
        max_length=4,
        choices=WEIGHTAGE_DIVISION_CHOICES,
        null=True,
        blank=True
    )
    third_weightage = models.CharField(
        max_length=4,
        choices=WEIGHTAGE_DIVISION_CHOICES,
        null=True,
        blank=True
    )
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Mark(models.Model):
    MARKS_DIVISION_CHOICES = [
        ('5%', '5%'),
        ('10%', '10%'),
        ('15%', '15%'),
        ('20%', '20%'),
        ('25%', '25%'),
        ('30%', '30%'),
        ('35%', '35%'),
        ('40%', '40%'),
        ('45%', '45%'),
        ('50%', '50%'),
        ('55%', '55%'),
        ('60%', '60%'),
        ('65%', '65%'),
        ('70%', '70%'),
        ('75%', '75%'),
        ('88%', '80%'),
        ('85%', '85%'),
        ('90%', '90%'),
        ('95%', '95%'),
        ('100%', '100%'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_score = models.CharField(
        max_length=4,
        choices=MARKS_DIVISION_CHOICES,
    )
    test_score = models.CharField(
        max_length=4,
        choices=MARKS_DIVISION_CHOICES,
        null=True,
        blank=True
    )
    performance_score = models.CharField(
        max_length=4,
        choices=MARKS_DIVISION_CHOICES,
        null=True,
        blank=True
    )
    listening_score = models.CharField(
        max_length=4,
        choices=MARKS_DIVISION_CHOICES,
        null=True,
        blank=True
    )
    speaking_score = models.CharField(
        max_length=4,
        choices=MARKS_DIVISION_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.subject)

class MarkAuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.mark}"