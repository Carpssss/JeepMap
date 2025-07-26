from django.urls import path
from . import views

app_name = 'scheduleMaster'

urlpatterns = [
    path('', views.schedule_list, name='list'),
    path('create/', views.schedule_create, name='create'),
    path('<int:pk>/', views.schedule_detail, name='detail'),
    path('<int:pk>/update/', views.schedule_update, name='update'),
    path('<int:pk>/delete/', views.schedule_delete, name='delete'),
    path('<int:pk>/duplicate/', views.schedule_duplicate, name='duplicate'),
    path('<int:pk>/toggle-status/', views.schedule_toggle_status, name='toggle_status'),
]
