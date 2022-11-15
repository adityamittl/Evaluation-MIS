from django.shortcuts import render
from stem.models import *
from django.core.files.storage import FileSystemStorage


def teacher_func(request):
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

    return render(request, 'teacher.html')
    # return render(request, 'teacher.html', context={'detail': teacherProfile.objects.get(user=request.user)})
