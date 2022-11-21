from django.urls import path
from .views import *

urlpatterns = [
    path('courseregistration',courseRegistration),
    path('currentScore',currentSheet),
    path('feedback',studentFeedback),
    path('data',pastData)
]