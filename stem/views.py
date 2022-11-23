from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from student.views import studentHome
from stem.mail import sendmail


import json
from .excelRead import extractData, givePassword
from .models import *


presets = {
    "u": "UG",
    "m": "PG",
    "p": "PHD",
}

degreeYears = {
    'UG' : 8,
    'PG' : 4,
}
# section of code for the administrator section

def breakRollNo(rollno):

    year = "20" + rollno[:2]
    degreetype = rollno[2:3]
    branch = branches.objects.get(rollnocode=rollno[3:5]).subcode
    return year, presets[degreetype], branch


def buildStudentProfile(data, rollnumber,newUser):

    year, dtype, branch = breakRollNo(rollnumber)
    studentProfile.objects.create(
        user = newUser,
        firstName=data["First Name"],
        lastName=data["Last name"],
        fatherName=data["Father Name"],
        MothersName=data["Mother Name"],
        rollNumber=rollnumber,
        admissionYear=year,
        branch=branch,
        degreeType=dtype,
    ).save()

@login_required
def administratorHome(request):
    
    if request.method == "POST":
        studentData = request.FILES["studentDetails"]
        fs = FileSystemStorage(location="media/enrollmentSheet")
        filename = fs.save(studentData.name, studentData)
        fetchedData = extractData("./media/enrollmentSheet/" + filename)
        for rollnumber in fetchedData.keys():
            newUser = User.objects.create_user(rollnumber,'',fetchedData[rollnumber]["password"])
            newUser.save()
            loginMode.objects.create(user=newUser, type="student").save()
            buildStudentProfile(fetchedData[rollnumber], rollnumber,newUser)
            sendmail(fetchedData[rollnumber]["First Name"] +" "+fetchedData[rollnumber]["Last name"] , rollnumber+"@lnmiit.ac.in",rollnumber,fetchedData[rollnumber]["password"])
        print("successful")
        return redirect('dashboard')

    # fetching stats to display on page
    scount = studentProfile.objects.filter(currentStudent=True).count()
    tcount = teacherProfile.objects.all().count()
    ccount = Subject.objects.all().count()
    data = {"scount": scount, "tcount": tcount, "ccount": ccount}
    return render(request, "admin.html", context=data)

@login_required
def fetchStudent(request):
    if request.method == "POST" and loginMode.objects.get(user = request.user).type == 'admin':
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

@login_required
def manageInstructor(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
        domains = branches.objects.all()
        teachers = teacherProfile.objects.all()
        if request.method == 'POST':
            print(request.POST)
            eid, fname,lname,department= request.POST.get('instructor'),request.POST.get('fname'), request.POST.get('lname'), request.POST.get('department')
            # print(eid,fname,lname,department)
            pswd = givePassword()
            newusr = User.objects.create_user(eid,'',pswd)
            branch = branches.objects.get(subcode = department)
            teacherProfile.objects.create(user = newusr,employeeId = eid, firstName = fname, lastName = lname, department = branch).save()
            sendmail(fname+" "+lname, eid+"@lnmiit.ac.in",eid, pswd)
            loginMode.objects.create(user = newusr, type = 'teacher').save()
            
            return redirect('instructor')
        return render(request, 'manageInstructor.html',context={'data':domains,'teacher':teachers})
    else:
        return redirect('error')

# Check if the written employee id is is conflict with someone.
@login_required
def duplicateEID(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
        data = request.body.decode('utf-8').split('=')[1]
        print(data)
        if teacherProfile.objects.filter(employeeId = data).count():
            return JsonResponse({'available' : False});
        return JsonResponse({'available' : True})

#Create new course and view all course of the institute.
@login_required
def manageCourse(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
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
    else:
        return redirect('error')

# To edit the corse using course ID. (aadhura kaam!!)
@login_required
def editCourse(request,cid):
    if loginMode.objects.get(user = request.user).type == 'admin':
        sub = Subject.objects.get(subjectId = cid)
        return render(request, 'cedit.html', context={'detail':sub})
    else:
        return redirect('error')


# for the registration access, that is allow admin to start registrations.
@login_required
def registrationSetup(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
        if request.method == 'POST':
            registrationStart = request.POST.get('startDateTime')
            semType = request.POST.get('semType')
            session = request.POST.get('session')
            degType = request.POST.get('deg')
            currentRegistrations.objects.create(registrationStart = registrationStart).save()
            if sessionYear.objects.get(year = int(session)) != None:
                sYear = sessionYear.objects.create(year = int(session))

            subjects = Subject.objects.all()
            for course in subjects:
                sessionSubject.objects.create(subject = course, remainingSeats = course.totalSeats, type = semType, sessionName = sYear)

            students = studentProfile.objects.filter(currentStudent = True, degreeType = degType)

            for student in students:
                sems = degreeYears[degType]
                print(sems)
                if student.currentSem < str(sems):
                    student.currentSem = str(int(student.currentSem) + 1)
                    student.currentSemRegister = True
                    student.save()


        return render(request, 'registration.html')
    else:
        return redirect('error')

@login_required
def stopRegistrations(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
        if request.method == 'POST':
            regs = currentRegistrations.objects.get(liveRegistration = True)
            for i in regs:
                regs.liveRegistration = False
                regs.save()
        
        return JsonResponse({'status':'Success'})


@login_required
def dashboard(request):
    if loginMode.objects.get(user = request.user).type == 'admin':
        return administratorHome(request)
    elif loginMode.objects.get(user = request.user).type == 'student':
        return studentHome(request)


def adminFeedback(request):
    return render(request, 'adminfeedback.html')