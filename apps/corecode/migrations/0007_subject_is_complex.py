# Generated by Django 3.2.13 on 2022-07-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0006_auto_20220715_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='is_complex',
            field=models.BooleanField(default=False),
        ),
    ]
