from django.urls import path
from . import views

app_name = 'vehicle_master'

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicle/new/', views.vehicle_create, name='vehicle_create'),
    path('vehicle/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('vehicle/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
]
