from django.urls import path

from image_scanner import views

urlpatterns = [
    path('image/<str:image_name>', views.image_scan, name='image'),
    path('status/<str:status_id>', views.image_scan_status, name='status'),
    path('result/<str:result_id>', views.image_scan_result, name='result'),
]