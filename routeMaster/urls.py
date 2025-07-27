# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.route_list, name='route_list'),
    path('create/', views.route_create, name='route_create'),
    path('<int:route_id>/matrix/', views.fare_matrix, name='fare_matrix'),
    path('<int:route_id>/delete/', views.route_delete, name='route_delete'),

]
