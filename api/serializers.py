from rest_framework import serializers
from .models import DicomMetadata

class DicomMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicomMetadata
        fields = [
            'id',
            'patient_name',
            'patient_identity_removed',
            'acquisition_date',
            'acquisition_date_time',
            'exposure_time',
            'detector_temperature',
            'hash'
        ]

    id = serializers.IntegerField(read_only=True),
    patient_name = serializers.CharField(required=False)
    patient_identity_removed = serializers.BooleanField(required=False)
    acquisition_date = serializers.DateField(required=False)
    acquisition_date_time = serializers.DateTimeField(required=False)
    exposure_time = serializers.IntegerField(required=False)
    detector_temperature = serializers.FloatField(required=False)
