from django.urls import path
from . import views

urlpatterns = [
    # basic render
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),

    path('managestaff/', views.managestaff, name='managestaff'),
    path('updatevacancy/', views.updatevacancy, name='updatevacancy'),
    path('removevacancy/', views.removevacancy, name='removevacancy'),


    path('createaccount/registerusers', views.registerusers, name='registerusers'),
    path('doctor/welcome/', views.doctor_welcome, name='doctor_welcome'),
    path('staff/welcome/', views.staff_welcome, name='staff_welcome'),
    path('staff/register/', views.register_patient, name='register_patient'),
    path('staff/add_patient_data/', views.add_patient_data, name='add_patient_data'),
    path('staff/up_patient_data/', views.up_patient_data, name='up_patient_data'),
    path('doctor/patient_data/', views.view_patient_data, name='view_patient_data'),
    path('doctor/prediction/', views.view_prediction, name='view_prediction'),
    path('admin_welcome', views.admin_welcome, name='admin_welcome'),
    path('privacy', views.privacy, name='privacy'),
    path('manageprivacy', views.manageprivacy, name='manageprivacy'),

    # login 
    path('accountlogin/', views.accountlogin, name='accountlogin'),

    
]
