# Generated by Django 4.1.2 on 2022-11-21 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="branches",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("branchName", models.CharField(max_length=50)),
                ("subcode", models.CharField(max_length=50)),
                ("rollnocode", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="evaluationScheme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("weightage", models.CharField(max_length=20)),
                ("max_score", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="gradeSheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isPassed", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="scoreCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Score", models.CharField(max_length=30)),
                (
                    "evaluationMethod",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stem.evaluationscheme",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sessionSubject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("remainingSeats", models.IntegerField(default=0)),
                (
                    "registrationStart",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("liveRegistration", models.BooleanField(default=False)),
                ("type", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "evaluation",
                    models.ManyToManyField(null=True, to="stem.evaluationscheme"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sessionYear",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="teacherProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstName", models.CharField(max_length=100)),
                ("lastName", models.CharField(max_length=100)),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "MobileNumber",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("employeeId", models.CharField(max_length=50)),
                ("email", models.CharField(blank=True, max_length=50, null=True)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="")),
                ("rating", models.FloatField(default=0)),
                ("department", models.CharField(blank=True, max_length=40, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subjectId", models.CharField(max_length=50)),
                ("subjectName", models.CharField(max_length=100)),
                ("credits", models.IntegerField()),
                ("subjectType", models.CharField(max_length=20)),
                ("offeredSem", models.CharField(max_length=20)),
                ("totalSeats", models.IntegerField(default=0)),
                (
                    "teachers",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stem.teacherprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="studentSessionsheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.CharField(blank=True, max_length=20, null=True)),
                ("grade", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "scoreSheet",
                    models.ManyToManyField(blank=True, null=True, to="stem.scorecard"),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stem.sessionsubject",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="studentProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstName", models.CharField(max_length=100)),
                ("lastName", models.CharField(max_length=100)),
                ("fatherName", models.CharField(blank=True, max_length=50, null=True)),
                ("MothersName", models.CharField(blank=True, max_length=50, null=True)),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "MobileNumber",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("rollNumber", models.CharField(max_length=50)),
                ("branch", models.CharField(default=None, max_length=10)),
                ("degreeType", models.CharField(default=None, max_length=15)),
                ("Address", models.TextField(blank=True, null=True)),
                ("email", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "parentContact",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("photo", models.ImageField(blank=True, null=True, upload_to="")),
                ("currentSem", models.CharField(default="0", max_length=20)),
                ("admissionYear", models.CharField(max_length=20)),
                ("currentStudent", models.BooleanField(default=True)),
                ("backlogs", models.IntegerField(default=0)),
                (
                    "scoreSheet",
                    models.ManyToManyField(blank=True, null=True, to="stem.gradesheet"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="sessionsubject",
            name="sessionName",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="stem.sessionyear"
            ),
        ),
        migrations.AddField(
            model_name="sessionsubject",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="stem.subject"
            ),
        ),
        migrations.CreateModel(
            name="loginMode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="gradesheet",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="stem.sessionyear"
            ),
        ),
        migrations.AddField(
            model_name="gradesheet",
            name="subjects",
            field=models.ManyToManyField(to="stem.studentsessionsheet"),
        ),
        migrations.CreateModel(
            name="feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("point", models.IntegerField(default=0)),
                ("description", models.TextField()),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stem.teacherprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="administrator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("employeeID", models.CharField(max_length=20)),
                ("mobileNumber", models.CharField(max_length=30)),
                ("email", models.CharField(max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
