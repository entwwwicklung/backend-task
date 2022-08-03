from django.db import models

class DicomMetadata(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    patient_name = models.CharField(null=True, max_length=200)
    patient_identity_removed = models.BooleanField(null=True)
    acquisition_date = models.DateField(null=True)
    acquisition_date_time = models.DateTimeField(null=True)
    exposure_time = models.IntegerField(null=True)
    detector_temperature = models.FloatField(null=True)
    hash = models.CharField(max_length=64)
