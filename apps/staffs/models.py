from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save  #Added
from django.contrib.auth import get_user_model  #Added
from django.contrib.auth.models import Group
from .utils import create_default_password      #Added

User = get_user_model()                         #Added
class Staff(models.Model):
    
    STATUS = [("active", "Active"), ("inactive", "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})

#Added entire block till last
def post_staff_created_signal(sender, instance, created, **kwargs):
    if created:
        default_password = create_default_password(instance)
        group = Group.objects.get(name='Teacher')
        user = User.objects.create_user(username = str(instance).strip(), password = default_password, member_id = instance.id)
        user.groups.add(group)

post_save.connect(post_staff_created_signal, sender=Staff)
