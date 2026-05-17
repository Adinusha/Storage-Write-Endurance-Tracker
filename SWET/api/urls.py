from django.urls import path
from . import views

urlpatterns = [
    # API
    path('api/write-event/', views.WriteEventCreateAPIView.as_view(), name='write_event_api'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Devices
    path('devices/', views.device_list, name='device_list'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('devices/add/', views.device_create, name='device_create'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),

    # SD Cards
    path('cards/<int:pk>/', views.sdcard_detail, name='sdcard_detail'),
    path('devices/<int:device_pk>/cards/add/', views.sdcard_create, name='sdcard_create'),
    path('cards/<int:pk>/delete/', views.sdcard_delete, name='sdcard_delete'),

    # Alerts
    path('alerts/', views.alert_list, name='alert_list'),
    path('alerts/<int:pk>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
]