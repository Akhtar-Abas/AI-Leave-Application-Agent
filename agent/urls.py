from django.urls import path
from . import views

urlpatterns = [
    # Agar index function nahi hai, to is line ko comment kar dein ya delete karein
    # path('', views.index, name='index'), 
    
    path('generate/', views.generate_leave_application, name='generate'),
]