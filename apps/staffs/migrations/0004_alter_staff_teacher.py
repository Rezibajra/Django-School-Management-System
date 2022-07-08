# Generated by Django 3.2.13 on 2022-07-07 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staffs', '0003_staff_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='teacher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
