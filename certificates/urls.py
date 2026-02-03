from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verify/', views.verify_page, name='verify_page'),
    path('generate-certificate/', views.generate_certificate, name='generate_certificate'),
]
