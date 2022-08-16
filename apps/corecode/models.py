from django.db import models

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

    WEIGHTAGE_DIVISION_CHOICES = [
        ('10%', '10%'),
        ('20%', '20%'),
        ('30%', '30%'),
        ('60%', '60%'),
    ]
    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)
    weightage = models.CharField(
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
        ('45%', '45%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('90%', '90%')
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
