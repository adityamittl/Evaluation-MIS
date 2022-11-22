from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from stem.models import *
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage


# Create your views here.
@login_required
def studentHome(request):
    if loginMode.objects.get(user = request.user).type == 'student':
        if request.method == 'POST':
            dob = request.POST.get('dob')
            mno = request.POST.get('mob')
            address = request.POST.get('address')
            email = request.POST.get('email')
            pcno = request.POST.get('pmob')
            pphoto = request.FILES['pphoto']
            student = studentProfile.objects.get(user = request.user)
            fs = FileSystemStorage(location="media/profilePhoto")
            filename = fs.save(pphoto.name, pphoto)
            student.dob = dob
            student.MobileNumber = mno
            student.Address = address
            student.email = email
            student.parentContact = pcno
            student.photo = filename
            student.save()
        student = studentProfile.objects.get(user = request.user)
        return render(request,'studentHome.html', context={'data': student})
    
    else:
        return redirect('error')

@login_required
def courseRegistration(request):
    if loginMode.objects.get(user = request.user).type == 'student':
        student = studentProfile.objects.get(user = request.user)
        time_t = currentRegistrations.objects.all()[0].registrationStart

        if(student.currentSemRegister):
            return render(request, 'courseRegistraton.html', context={'start': False,'Registration':True})
        
        elif time_t >  now():
            return render(request, 'courseRegistraton.html', context={'start' : False,'time':str(time_t).split("+")[0]})
        
        else:
            sem = student.currentSem
            semType = 'even' if int(sem)%2 == 0 else 'odd'
            subjects = Subject.objects.filter(offeredSem = sem)

            # for F- Graded subjects!!

            sheets = student.scoreSheet.all()
            for score_sheet in sheets:
                if score_sheet.current == False:
                    subjs = score_sheet.subjects.all()
                    for i in subjs:
                        if i.isPassed == False:
                            sem = i.subject.subject.offeredSem
                            if int(sem)%2 == 0 and semType == 'even':
                                subjects = subject | sem.subject.subject
                            elif int(sem)%2 != 0 and semType == 'odd':
                                subjects = subject | sem.subject.subject
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
    else:
        return redirect('error')

@login_required
def currentSheet(request):
    if loginMode.objects.get(user = request.user).type == 'student':
        student = studentProfile.objects.get(user = request.user).scoreSheet.all()
        current = ''
        for i in student:
            if i.current == True:
                current = i
        
        y = i.subjects.all()
        return render(request,'currentSemScore.html', context={'subs':y})
    
    else:
        return redirect('error')

@login_required
def studentFeedback(request):
    if loginMode.objects.get(user = request.user).type == 'student':
        studentProfile.objects.get(user = request.user)
        if request.method == 'POST':
            star = list(request.POST)[2].split("_")[1]
            feedback.objects.create(point = star, teacher = teacherProfile.objects.get(employeeId = request.POST.get('teacher_name'), description = request.POST.get('feedback'))).save()
            return render(request,'studentFeedback.html')

        return render(request,'studentFeedback.html')
    else:
        return redirect('error')

@login_required
def pastData(request):
    return render(request, 'CumulativeResults.html')