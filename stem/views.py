from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
# from django.core import serializers


import json
from .excelRead import extractData, givePassword
from .models import *


presets = {
    "u": "UG",
    "m": "PG",
    "p": "PHD",
}


# section of code for the administrator section


def breakRollNo(rollno):

    year = "20" + rollno[:2]
    degreetype = rollno[2:3]
    branch = branches.objects.get(rollnocode=rollno[3:5]).subcode
    return year, presets[degreetype], branch


def buildStudentProfile(data, rollnumber):

    year, dtype, branch = breakRollNo(rollnumber)
    studentProfile.objects.create(
        firstName=data["First Name"],
        lastName=data["Last name"],
        fatherName=data["Father Name"],
        MothersName=data["Mother Name"],
        rollNumber=rollnumber,
        admissionYear=year,
        branch=branch,
        degreeType=dtype,
    ).save()


def administrator(request):

    if request.method == "POST":
        studentData = request.FILES["studentDetails"]
        fs = FileSystemStorage(location="media/enrollmentSheet")
        filename = fs.save(studentData.name, studentData)
        fetchedData = extractData("./media/" + filename)
        for rollnumber in fetchedData.keys():
            newUser = User.objects.create_user(rollnumber)
            newUser.password = fetchedData[rollnumber]["password"]
            newUser.save()
            loginMode.objects.create(user=newUser, type="student").save()
            buildStudentProfile(fetchedData[rollnumber], rollnumber)

        print("successful")

    # fetching stats to display on page
    scount = studentProfile.objects.filter(currentStudent=True).count()
    tcount = teacherProfile.objects.all().count()
    ccount = Subject.objects.all().count()
    data = {"scount": scount, "tcount": tcount, "ccount": ccount}
    return render(request, "admin.html", context=data)


def fetchStudent(request):
    if request.method == "POST":
        rollno = json.loads(request.body.decode("utf-8"))["rollno"]
        student = studentProfile.objects.get(rollNumber=rollno)
        result = {
            "first Name": student.firstName,
            "last Name": student.lastName,
            "father Name": student.fatherName,
            "mother Name": student.MothersName,
            "dob": student.dob,
            "mobile": student.MobileNumber,
            "pmobile": student.parentContact,
            "rollNumber": student.rollNumber,
            "branch": student.branch,
            "degreeType": student.degreeType,
            "Address": student.Address,
            "email": student.email,
            "photo": student.photo.name,
        }
        return JsonResponse(result)

#Enroll new instructor into the institute.
def manageInstructor(request):
    if request.method == 'POST':
        eid, fname,lname,department= request.POST.get('instructor'),request.POST.get('fname'), request.POST.get('lname'), request.POST.get('department')
        pswd = givePassword()
        newusr = User.objects.create(eid)
        newusr.password = pswd
        newusr.save()

        loginMode.objects.create(user = newusr, type = 'teacher').save()
        
    return render(request, 'manageInstructor.html')

# Check if the written employee id is is conflict with someone.
def duplicateEID(request):
    data = request.body.decode('utf-8').split('=')[1]
    print(data)
    if teacherProfile.objects.filter(employeeId = data).count():
        return JsonResponse({'available' : False});
    return JsonResponse({'available' : True})

#Create new course and view all course of the institute.
def manageCourse(request):
    courses = Subject.objects.all()
    if request.method == 'POST':
        sid = request.POST.get('sid').upper()
        if Subject.objects.filter(subjectId = sid).count() >=1:
            return render(request, 'course.html', context={'messages': 'warning','message':'Failed! Course ID already Exist','subjects' : courses})
        sname = request.POST.get('sname')
        ctype = request.POST.get('ctype')
        credits = request.POST.get('credits')
        sem = request.POST.get('offeredSem')
        seats = request.POST.get('noseats')
        Subject.objects.create(subjectId = sid,  subjectName = sname, credits = credits, subjectType = ctype, offeredSem = sem, totalSeats = seats).save()

        return render(request, 'course.html', context={'messages': 'success','message':'Course has been introduced','subjects' : courses})

    return render(request,'course.html',context= {'subjects' : courses})

# To edit the corse using course ID. (aadhura kaam!!)
def editCourse(request,cid):
    sub = Subject.objects.get(subjectId = cid)
    return render(request, 'cedit.html', context={'detail':sub})


# for the registration access, that is allow admin to start registrations.

def registrationSetup(request):
    sessionYear.objects.create()
    subjects = Subject.objects.all()
    for course in subjects:
        sessionSubject.objects.create(subject = course, sessionName = )
    return render(request, 'registration.html')
