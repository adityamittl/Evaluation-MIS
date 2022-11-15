from django.urls import path
from .views import *

urlpatterns = [
    path('',administrator),
    path('fetchstudent', fetchStudent),
    path('instructor', manageInstructor),
    path('duplicateEID', duplicateEID),
    path('course', manageCourse),
    path('course/edit/<str:cid>',editCourse),
    path('registrationSetup',registrationSetup)
]