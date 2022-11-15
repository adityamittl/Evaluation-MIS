from django.urls import path
from .views import *

urlpatterns = [
    path('teacher', teacher_func)
    # path('',administrator),
    # path('fetchstudent', fetchStudent),
    # path('instructor', manageInstructor),
    # path('duplicateEID', duplicateEID)
]
