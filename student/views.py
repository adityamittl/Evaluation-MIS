from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stem.models import *
from django.utils.timezone import now
# Create your views here.
@login_required
def studentHome(request):
    if request.method == 'POST':
        dob = request.POST.get('dob')
        mno = request.POST.get('mob')
        address = request.POST.get('address')
        email = request.POST.get('email')
        pcno = request.POST.get('pmob')
        student = studentProfile.objects.get(user = request.user)
        student.dob = dob
        student.MobileNumber = mno
        student.Address = address
        student.email = email
        student.parentContact = pcno
        student.save()
    student = studentProfile.objects.get(user = request.user)
    return render(request,'studentHome.html', context={'data': student})

def courseRegistration(request):
    student = studentProfile.objects.get(user = request.user)
    time_t = currentRegistrations.objects.all()[0].registrationStart
    if(student.currentSemRegister):
        print("YOOOO")
        return render(request, 'courseRegistraton.html', context={'start': False,'Registration':True})
    elif time_t >  now():
        return render(request, 'courseRegistraton.html', context={'start' : False,'time':str(time_t).split("+")[0]})
    else:
        sem = student.currentSem
        subjects = Subject.objects.filter(offeredSem = sem)
        if request.method == 'POST':
            CoursesID = request.POST
            courses = list(CoursesID.keys())
            courses.remove('csrfmiddlewaretoken')
            print(courses)
            sheet = gradeSheet.objects.create()
            for subject in courses:
                sub = Subject.objects.get(subjectId = subject)
                sessionsub = sessionSubject.objects.get(subject = sub)
                print(sessionsub)
                sss = studentSessionsheet.objects.create(subject = sessionsub)
                sheet.subjects.add(sss)
                sheet.registered = True
                sheet.save()
                student.scoreSheet.add(sheet)
            student.save()
        return render(request, 'courseRegistraton.html', context={'start':True,'subjects':subjects})

def currentSheet(request):
    student = studentProfile.objects.get(user = request.user).scoreSheet.all()
    current = ''
    for i in student:
        if i.current == True:
            current = i
    
    y = i.subjects.all()
    print(y)

    return render(request,'currentSemScore.html', context={'subs':y})

def studentFeedback(request):
    if request.method == 'POST':
        star = list(request.POST)[2].split("_")[1]
        feedback.objects.create(point = star, teacher = teacherProfile.objects.get(employeeId = request.POST.get('teacher_name'), description = request.POST.get('feedback'))).save()
        return render(request,'studentFeedback.html')

    return render(request,'studentFeedback.html')

def pastData(request):
    return render(request, 'CumulativeResults.html')