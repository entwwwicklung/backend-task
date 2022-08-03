from django_filters import rest_framework as filters
from .models import DicomMetadata

class DicomMetadataFilter(filters.FilterSet):

    min_acquisition_date = filters.DateFilter(field_name='acquisition_date', lookup_expr='gte')
    max_acquisition_date = filters.DateFilter(field_name='acquisition_date', lookup_expr='lte')
    min_acquisition_date_time = filters.DateTimeFilter(field_name='acquisition_date_time', lookup_expr='gte')
    max_acquisition_date_time = filters.DateTimeFilter(field_name='acquisition_date_time', lookup_expr='lte')
    min_exposure_time = filters.NumberFilter(field_name='exposure_time', lookup_expr='gte')
    max_exposure_time = filters.NumberFilter(field_name='exposure_time', lookup_expr='lte')
    min_detector_temperature = filters.NumberFilter(field_name='detector_temperature', lookup_expr='gte')
    max_detector_temperature = filters.NumberFilter(field_name='detector_temperature', lookup_expr='lte')

    class Meta:
        model = DicomMetadata
        fields = [
            'id',
            'patient_identity_removed',
            'acquisition_date',
            'acquisition_date_time',
            'exposure_time',
            'detector_temperature'
        ]
