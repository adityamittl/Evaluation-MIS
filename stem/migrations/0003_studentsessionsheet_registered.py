# Generated by Django 4.1.2 on 2022-11-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stem", "0002_currentregistrations_remove_gradesheet_session_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentsessionsheet",
            name="registered",
            field=models.BooleanField(default=False),
        ),
    ]