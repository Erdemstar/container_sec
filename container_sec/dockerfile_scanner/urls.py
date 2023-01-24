from django.urls import path

from dockerfile_scanner import views

urlpatterns = [
    path('scanner', views.scanner, name='scanner'),
    path('detail_scanner', views.detail_scanner, name='scanner'),
]