from django.urls import path
from . import views

app_name = 'crew_master'

urlpatterns = [
    path('', views.crew_list, name='list'),
    path('create/', views.crew_create, name='create'),
    path('<int:pk>/', views.crew_detail, name='detail'),
    path('<int:pk>/update/', views.crew_update, name='update'),
    path('<int:pk>/delete/', views.crew_delete, name='delete'),
    path('<int:pk>/toggle-status/', views.crew_toggle_status, name='toggle_status'),
    path('<int:pk>/change-password/', views.crew_password_change, name='change_password'),
    path('<int:pk>/download-qr/', views.download_qr_code, name='download_qr'),
    path('<int:pk>/regenerate-qr/', views.regenerate_qr_code, name='regenerate_qr'),
]
