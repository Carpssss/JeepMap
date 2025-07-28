from django.urls import path
from . import views

app_name = 'waybill'

urlpatterns = [
    path('', views.WaybillListView.as_view(), name='list'),
    path('create/', views.WaybillCreateView.as_view(), name='create'),
    path('<int:pk>/', views.WaybillDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.WaybillUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.WaybillDeleteView.as_view(), name='delete'),
]