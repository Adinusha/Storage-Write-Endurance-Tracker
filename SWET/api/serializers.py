from rest_framework import serializers
from .models import WriteEvent, SDCard, Device, Alert, AlertThreshold


class WriteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriteEvent
        fields = ['id', 'sdcard', 'bytes_written', 'recorded_at']
        read_only_fields = ['recorded_at']

    def validate_bytes_written(self, value):
        if value <= 0:
            raise serializers.ValidationError("bytes_written must be greater than 0.")
        return value

    def validate_sdcard(self, value):
        if not SDCard.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("SD card not found.")
        return value


class SDCardSerializer(serializers.ModelSerializer):
    health_percent = serializers.FloatField(read_only=True)
    total_written_bytes = serializers.IntegerField(read_only=True)
    estimated_lifespan_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = SDCard
        fields = [
            'id', 'device', 'brand', 'model', 'capacity_gb',
            'tbw_limit_tb', 'installed_at', 'health_percent',
            'total_written_bytes', 'estimated_lifespan_days',
        ]


class DeviceSerializer(serializers.ModelSerializer):
    sdcards = SDCardSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'location', 'serial_number', 'created_at', 'sdcards']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'sdcard', 'level', 'message', 'triggered_at', 'acknowledged']
        read_only_fields = ['triggered_at']


class AlertThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertThreshold
        fields = ['id', 'sdcard', 'warn_at_percent', 'critical_at_percent']