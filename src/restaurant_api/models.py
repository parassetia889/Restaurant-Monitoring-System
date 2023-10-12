from django.db import models


class BusinessHours(models.Model):
    class Meta:
        db_table = "business_hours"

    store_id = models.BigIntegerField()
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()


# Create your models here.
class Store(models.Model):
    class Meta:
        db_table = "store"

    store_id = models.BigIntegerField()
    status = models.TextField()
    timestamp_utc = models.DateTimeField(max_length=255, null=True)


class Timezones(models.Model):
    class Meta:
        db_table = "time_zones"

    store_id = models.BigIntegerField()
    timezone_str = models.CharField(max_length=255)


class Report(models.Model):
    class Meta:
        db_table = "report_status"

    report_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10)
    data = models.TextField(null=False)
