from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_list, name='admin_list'),
    path('create/', views.admin_create, name='admin_create'),
    path('<int:pk>/', views.admin_detail, name='admin_detail'),
    path('<int:pk>/update/', views.admin_update, name='admin_update'),
    path('<int:pk>/delete/', views.admin_delete, name='admin_delete'),
]