# Generated by Django 4.1.2 on 2022-11-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stem", "0005_remove_gradesheet_registered_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gradesheet",
            name="isPassed",
        ),
        migrations.AddField(
            model_name="studentsessionsheet",
            name="isPassed",
            field=models.BooleanField(default=False),
        ),
    ]
