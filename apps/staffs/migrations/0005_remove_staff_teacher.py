# Generated by Django 3.2.13 on 2022-07-07 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0004_alter_staff_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='teacher',
        ),
    ]
