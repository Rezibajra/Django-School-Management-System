# Generated by Django 3.2.13 on 2022-08-05 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0005_auto_20220803_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='exam_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='test_score',
            field=models.IntegerField(default=0),
        ),
    ]
