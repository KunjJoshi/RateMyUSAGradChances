from django.contrib import admin
from django.urls import path
from .student import *
from .university import *
from .score import *

urlpatterns = [
    path('api/user/login/',StudentLogin.as_view()),
    path('api/user/sendotp/',sendOTP.as_view()),
    path('api/user/verifyotp/',sendOTP.as_view()),
    path('api/user/createProfile/',UniversityStudent.as_view()),
    path('api/user/showProfile',UniversityStudent.as_view()),
    path('api/user/updateProfile/',UniversityStudent.as_view()),
    path('api/user/deleteProfile/',UniversityStudent.as_view()),
    path('api/university/show/',University.as_view()),
    path('api/university/add/',University.as_view()),
    path('api/university/delete/',University.as_view()),
    path('api/score/calculate/',calcProfileScore.as_view()),
    path('api/score/chances/', CalcChancesOfAdmit.as_view()),
    path('api/score/shortlist/',shortlistUnis.as_view())
]