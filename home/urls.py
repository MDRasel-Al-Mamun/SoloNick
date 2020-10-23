from django.urls import path
from .import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('services/', views.servicesView, name='services'),
    path('contacts/', views.contactView, name='contacts'),
]
