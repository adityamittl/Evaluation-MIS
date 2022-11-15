from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

#Branches in that perticular institute
class branches(models.Model):
    branchName = models.CharField(max_length = 50)
    subcode = models.CharField(max_length = 50)
    rollnocode = models.CharField(max_length = 50)
    def __str__(self):
        return self.subcode

class administrator(models.Model):
    name = models.CharField(max_length = 50)
    employeeID = models.CharField(max_length = 20)
    mobileNumber = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class teacherProfile(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    dob = models.DateField(null = True, blank = True)
    MobileNumber = models.CharField(max_length = 50, null = True, blank = True)
    employeeId =  models.CharField(max_length = 50)
    email = models.CharField(max_length = 50,  null = True, blank = True)
    photo = models.ImageField(null = True, blank = True)
    rating = models.FloatField(default = 0)
    department = models.CharField(max_length = 40, null = True, blank = True)

class evaluationScheme(models.Model):
    name = models.CharField(max_length = 50)
    weightage = models.CharField(max_length = 20)
    max_score = models.CharField(max_length = 10)

class sessionYear(models.Model):
    year = models.IntegerField()

# Creating a subject, only addministrator can create this.
class Subject(models.Model):
    subjectId = models.CharField(max_length = 50)
    subjectName = models.CharField(max_length = 100)
    credits = models.IntegerField()
    teachers = models.ForeignKey(teacherProfile, on_delete = models.CASCADE, null=True, blank=True)
    subjectType = models.CharField(max_length = 20)
    offeredSem = models.CharField(max_length = 20)
    totalSeats = models.IntegerField(default = 0)

# year in the session.
class sessionSubject(models.Model):
    remainingSeats = models.IntegerField(default = 0)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    evaluation = models.ManyToManyField(evaluationScheme, null=True)
    sessionName = models.ForeignKey(sessionYear, on_delete = models.CASCADE)
    registrationStart = models.DateTimeField(default = now, blank=True)
    liveRegistration = models.BooleanField(default=False)
    type = models.CharField(max_length=20, null=True, blank=True)
    
# This table is to give score to each evalution module created by the instructor.
class scoreCard(models.Model):
    evaluationMethod = models.ForeignKey(evaluationScheme, on_delete = models.CASCADE)
    Score = models.CharField(max_length = 30)

# table to store the score of student's subject
class studentSessionsheet(models.Model):
    subject = models.ForeignKey(sessionSubject, on_delete = models.CASCADE)
    scoreSheet = models.ManyToManyField(scoreCard, null = True, blank = True)
    total = models.CharField(max_length = 20, null = True, blank = True)
    grade = models.CharField(max_length = 20, null = True, blank = True)
    # sessionYear = models.ForeignKey(sessionYear, on_delete = models.CASCADE)

# Score sheet, taking additional to 
class gradeSheet(models.Model):
    session = models.ForeignKey(sessionYear, on_delete = models.CASCADE)
    subjects = models.ManyToManyField(studentSessionsheet)
    isPassed = models.BooleanField(default=False)

# Building student profile, initially with name and email and then ask them to complete their profile
class studentProfile(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    fatherName = models.CharField(max_length = 50,null = True, blank = True)
    MothersName = models.CharField(max_length = 50,null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    MobileNumber = models.CharField(max_length = 50, null = True, blank = True)
    rollNumber = models.CharField(max_length = 50)
    branch = models.CharField(max_length = 10, default = None)
    degreeType = models.CharField(max_length = 15, default = None)
    Address = models.TextField(null = True, blank = True)
    email = models.CharField(max_length = 50, null = True, blank = True)
    parentContact = models.CharField(max_length = 50, null = True, blank = True)
    photo = models.ImageField(null = True, blank = True)
    scoreSheet = models.ManyToManyField(gradeSheet, null = True, blank = True)
    currentSem = models.CharField(max_length = 20, default = '0')
    admissionYear = models.CharField(max_length = 20)
    currentStudent = models.BooleanField(default = True)
    backlogs = models.IntegerField(default = 0)

    def __str__(self):
        return self.rollNumber


# Since we are using single login page for the authentication, this table helps in differentiating the type of user logging into the system, whether instructor, student or the administrator, and administrator has the complete priviliges to view, and change these fields
class loginMode(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    type = models.CharField(max_length = 20)


# Not taking student details to make the feedback completely anonymous.
class feedback(models.Model):
    point = models.IntegerField(default = 0)
    teacher = models.ForeignKey(teacherProfile, on_delete = models.CASCADE)
    description = models.TextField()
