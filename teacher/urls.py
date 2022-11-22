from django.urls import path
from .views import *

urlpatterns = [
    path('teacher', edit_profile, name='editProfile'),
    path('manageCourses', manage_courses, name='manageCourses'),
    path('showFeedback', show_feedback, name='showFeedback'),
    path('grading', set_grading, name='grading')
    # path('',administrator),
    # path('fetchstudent', fetchStudent),
    # path('instructor', manageInstructor),
    # path('duplicateEID', duplicateEID)
]
