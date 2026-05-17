from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True, help_text="GPS latitude e.g. 44.4268")
    longitude = models.FloatField(null=True, blank=True, help_text="GPS longitude e.g. 26.1025")

    def __str__(self):
        return self.name


class SDCard(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sdcards')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    capacity_gb = models.PositiveIntegerField()
    tbw_limit_tb = models.FloatField(help_text="Manufacturer TBW rating in terabytes")
    pe_cycles = models.PositiveIntegerField(
        default=3000,
        help_text="Program/Erase cycles supported (e.g. 3000 MLC, 1000 TLC, 100000 SLC)"
    )
    write_amplification_factor = models.FloatField(
        default=1.5,
        help_text="Typically between 1.0 and 3.0"
    )
    installed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.device.name})"

    @property
    def theoretical_lifespan_gb(self):
        return (self.capacity_gb * self.pe_cycles) / self.write_amplification_factor

    @property
    def total_written_bytes(self):
        result = self.write_events.aggregate(total=models.Sum('bytes_written'))
        return result['total'] or 0

    @property
    def total_written_gb(self):
        return self.total_written_bytes / 1_000_000_000

    @property
    def health_percent(self):
        lifespan_gb = self.theoretical_lifespan_gb
        if lifespan_gb == 0:
            return 0
        return min(100.0, (self.total_written_gb / lifespan_gb) * 100)

    @property
    def estimated_lifespan_days(self):
        events = self.write_events.order_by('recorded_at')
        if events.count() < 2:
            return None
        first = events.first()
        last = events.last()
        days_elapsed = (last.recorded_at - first.recorded_at).days
        if days_elapsed == 0:
            return None
        gb_remaining = self.theoretical_lifespan_gb - self.total_written_gb
        daily_rate_gb = self.total_written_gb / days_elapsed
        if daily_rate_gb == 0:
            return None
        return int(gb_remaining / daily_rate_gb)


class WriteEvent(models.Model):
    sdcard = models.ForeignKey(SDCard, on_delete=models.CASCADE, related_name='write_events')
    bytes_written = models.BigIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sdcard} — {self.bytes_written} bytes at {self.recorded_at:%Y-%m-%d %H:%M}"


class AlertThreshold(models.Model):
    sdcard = models.OneToOneField(SDCard, on_delete=models.CASCADE)
    warn_at_percent = models.FloatField(default=80.0)
    critical_at_percent = models.FloatField(default=95.0)

    def __str__(self):
        return f"Thresholds for {self.sdcard}"


class Alert(models.Model):
    LEVEL_CHOICES = [('warn', 'Warning'), ('critical', 'Critical')]

    sdcard = models.ForeignKey(SDCard, on_delete=models.CASCADE, related_name='alerts')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField(blank=True)
    triggered_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.level.upper()}] {self.sdcard}"