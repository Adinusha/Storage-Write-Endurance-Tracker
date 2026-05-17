from django.contrib import admin
from .models import Device, SDCard, WriteEvent, AlertThreshold, Alert

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'location', 'created_at']
    search_fields = ['name', 'serial_number']

@admin.register(SDCard)
class SDCardAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'device', 'capacity_gb', 'tbw_limit_tb']
    list_filter = ['brand', 'device']

@admin.register(WriteEvent)
class WriteEventAdmin(admin.ModelAdmin):
    list_display = ['sdcard', 'bytes_written', 'recorded_at']
    list_filter = ['sdcard', 'recorded_at']

@admin.register(AlertThreshold)
class AlertThresholdAdmin(admin.ModelAdmin):
    list_display = ['sdcard', 'warn_at_percent', 'critical_at_percent']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['sdcard', 'level', 'triggered_at', 'acknowledged']
    list_filter = ['level', 'acknowledged']