from django.shortcuts import render, redirect
from stem.models import *
from django.core.files.storage import FileSystemStorage


def edit_profile(request):
    if request.method == 'POST':
        photo = request.FILES['photo']
        fs = FileSystemStorage(location="media/profilePhoto/")
        filename = fs.save(photo.name, photo)
        teacher = teacherProfile.objects.get(user=request.user)
        teacher.firstName = request.POST.get('fname')
        teacher.lastName = request.POST.get('lname')
        teacher.dob = request.POST.get('dob')
        teacher.MobileNumber = request.POST.get('mobileNo')
        teacher.email = request.POST.get('secondaryEmail')
        teacher.photo = filename
        teacher.save()
        return redirect('editProfile')

    return render(request, 'teacherHome.html')
    # return render(request, 'teacher.html', context={'detail': teacherProfile.objects.get(user=request.user)})


def manage_courses(request):
    return render(request, 'manageCourses.html')


def show_feedback(request):
    return render(request, 'teacherFeedback.html')


def set_grading(request):
    return render(request, 'teacherGrading.html')
