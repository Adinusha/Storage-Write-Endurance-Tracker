from .models import Alert, AlertThreshold


def check_thresholds(sdcard):
    health = sdcard.health_percent

    try:
        threshold = sdcard.alertthreshold
    except AlertThreshold.DoesNotExist:
        return

    open_alerts = Alert.objects.filter(sdcard=sdcard, acknowledged=False)

    if health >= threshold.critical_at_percent:
        if not open_alerts.filter(level='critical').exists():
            Alert.objects.create(
                sdcard=sdcard,
                level='critical',
                message=f"{sdcard} has reached {health:.1f}% of its TBW limit "
                        f"(critical threshold: {threshold.critical_at_percent}%)"
            )
    elif health >= threshold.warn_at_percent:
        if not open_alerts.filter(level='warn').exists():
            Alert.objects.create(
                sdcard=sdcard,
                level='warn',
                message=f"{sdcard} has reached {health:.1f}% of its TBW limit "
                        f"(warning threshold: {threshold.warn_at_percent}%)"
            )


def get_open_alerts():
    return (
        Alert.objects
        .filter(acknowledged=False)
        .select_related('sdcard', 'sdcard__device')
        .order_by('-triggered_at')
    )