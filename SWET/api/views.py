from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Device, SDCard, Alert, AlertThreshold
from .serializers import (
    WriteEventSerializer, DeviceSerializer, SDCardSerializer,
    AlertSerializer, AlertThresholdSerializer
)
from .services import check_thresholds, get_open_alerts
from .weather import get_weather


# ─── REST API views ───────────────────────────────────────────────

class WriteEventCreateAPIView(CreateAPIView):
    serializer_class = WriteEventSerializer

    def perform_create(self, serializer):
        event = serializer.save()
        check_thresholds(event.sdcard)


class APIDeviceList(ListCreateAPIView):
    queryset = Device.objects.prefetch_related('sdcards').all()
    serializer_class = DeviceSerializer


class APIDeviceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.prefetch_related('sdcards').all()
    serializer_class = DeviceSerializer


class APISDCardList(ListCreateAPIView):
    queryset = SDCard.objects.select_related('device').all()
    serializer_class = SDCardSerializer


class APISDCardDetail(RetrieveUpdateDestroyAPIView):
    queryset = SDCard.objects.select_related('device').all()
    serializer_class = SDCardSerializer


class APIAlertList(ListAPIView):
    serializer_class = AlertSerializer

    def get_queryset(self):
        if self.request.query_params.get('all'):
            return Alert.objects.select_related('sdcard').order_by('-triggered_at')
        return Alert.objects.filter(acknowledged=False).select_related('sdcard').order_by('-triggered_at')


class APIAcknowledgeAlert(APIView):
    def post(self, request, pk):
        alert = get_object_or_404(Alert, pk=pk)
        alert.acknowledged = True
        alert.save()
        return Response({'status': 'acknowledged'}, status=status.HTTP_200_OK)


class APIThresholdList(ListCreateAPIView):
    queryset = AlertThreshold.objects.select_related('sdcard').all()
    serializer_class = AlertThresholdSerializer


class APIThresholdDetail(RetrieveUpdateDestroyAPIView):
    queryset = AlertThreshold.objects.all()
    serializer_class = AlertThresholdSerializer


# ─── Web UI views ─────────────────────────────────────────────────

def dashboard(request):
    devices = Device.objects.prefetch_related('sdcards').all()
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    return render(request, 'dashboard.html', {
        'devices': devices,
        'open_alert_count': open_alert_count,
    })


def device_list(request):
    devices = Device.objects.all()
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    return render(request, 'devices/list.html', {
        'devices': devices,
        'open_alert_count': open_alert_count,
    })


def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    return render(request, 'devices/detail.html', {
        'device': device,
        'open_alert_count': open_alert_count,
    })


def device_create(request):
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    if request.method == 'POST':
        lat = request.POST.get('latitude') or None
        lng = request.POST.get('longitude') or None
        Device.objects.create(
            name=request.POST['name'],
            location=request.POST.get('location', ''),
            serial_number=request.POST['serial_number'],
            latitude=float(lat) if lat else None,
            longitude=float(lng) if lng else None,
        )
        return redirect('dashboard')
    return render(request, 'devices/form.html', {
        'open_alert_count': open_alert_count,
    })


def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard')
    return render(request, 'devices/confirm_delete.html', {
        'device': device,
        'open_alert_count': open_alert_count,
    })


def sdcard_detail(request, pk):
    card = get_object_or_404(SDCard, pk=pk)
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    events = card.write_events.order_by('recorded_at')
    chart_labels = [e.recorded_at.strftime('%Y-%m-%d %H:%M') for e in events]
    chart_data = [e.bytes_written for e in events]

    weather = None
    device = card.device
    if device.latitude is not None and device.longitude is not None:
        weather = get_weather(device.latitude, device.longitude)

    return render(request, 'sdcards/detail.html', {
        'card': card,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'open_alert_count': open_alert_count,
        'weather': weather,
    })


def sdcard_create(request, device_pk):
    device = get_object_or_404(Device, pk=device_pk)
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    if request.method == 'POST':
        SDCard.objects.create(
            device=device,
            brand=request.POST['brand'],
            model=request.POST['model'],
            capacity_gb=request.POST['capacity_gb'],
            tbw_limit_tb=request.POST['tbw_limit_tb'],
            pe_cycles=request.POST['pe_cycles'],
            write_amplification_factor=request.POST['write_amplification_factor'],
            installed_at=parse_datetime(request.POST['installed_at']),
        )
        return redirect('device_detail', pk=device.pk)
    return render(request, 'sdcards/form.html', {
        'device': device,
        'open_alert_count': open_alert_count,
    })


def sdcard_delete(request, pk):
    card = get_object_or_404(SDCard, pk=pk)
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    if request.method == 'POST':
        device_pk = card.device.pk
        card.delete()
        return redirect('device_detail', pk=device_pk)
    return render(request, 'sdcards/confirm_delete.html', {
        'card': card,
        'open_alert_count': open_alert_count,
    })


def alert_list(request):
    alerts = get_open_alerts()
    open_alert_count = Alert.objects.filter(acknowledged=False).count()
    return render(request, 'alerts/list.html', {
        'alerts': alerts,
        'open_alert_count': open_alert_count,
    })


def acknowledge_alert(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    if request.method == 'POST':
        alert.acknowledged = True
        alert.save()
    return redirect('alert_list')