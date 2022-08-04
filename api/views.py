import pydicom
from datetime import datetime

from django.utils.datastructures import MultiValueDictKeyError
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import generics, status

from .filters import DicomMetadataFilter
from .models import DicomMetadata
from .serializers import DicomMetadataSerializer
from .utils import sha256sum


class DocumentsList(generics.ListCreateAPIView):
    queryset = DicomMetadata.objects.all()
    serializer_class = DicomMetadataSerializer
    filterset_class = DicomMetadataFilter
    ordering_fields = (
        'id',
        'patient_identity_removed',
        'acquisition_date',
        'exposure_time',
        'detector_temperature',
    )

    def post(self, request):
        try:
            f = request.FILES['file']
        except MultiValueDictKeyError:
            return Response({"error": "Missing file"}, status=status.HTTP_400_BAD_REQUEST)

        metadata, error = _parse_metadata(f)
        if error:
            return Response({"error": "Something went wrong while parsing file"}, status=status.HTTP_400_BAD_REQUEST)

        _hash = sha256sum(f)
        existing_file = DicomMetadata.objects.filter(hash=_hash)
        if existing_file:
            return Response({"error": "File already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = _extract_metadata(metadata)
        write_data, error = _normalize_values(data)
        if error:
            return Response({"error": "Something went wrong while parsing data"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        write_data['hash'] = _hash

        serializer = DicomMetadataSerializer(data=write_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid metadata"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

def _parse_metadata(f):
    try:
        metadata = pydicom.dcmread(f)
    except Exception as e:
        return None, str(e)   

    return metadata, None

def _extract_metadata(metadata):
    extracted_data = {}

    metadata_fields = [
        'PatientName',
        'PatientIdentityRemoved',
        'AcquisitionDate',
        'AcquisitionDateTime',
        'ExposureTime',
        'DetectorTemperature'
    ]

    for field in metadata_fields:
        try:
            extracted_data[_name_mapper(field)] = metadata.data_element(field).value
        except KeyError:
            pass

    return extracted_data

def _name_mapper(key):
    map = {
        'PatientName': 'patient_name',
        'PatientIdentityRemoved': 'patient_identity_removed',
        'AcquisitionDate': 'acquisition_date',
        'AcquisitionDateTime': 'acquisition_date_time',
        'ExposureTime': 'exposure_time',
        'DetectorTemperature': 'detector_temperature',
    }

    return map[key]

def _normalize_values(data):
    try:
        normalized_data = {}
        for k, v in data.items():
            normalized_data[k] = _normalize_value(k, v)
    except Exception as e:
        return normalized_data, str(e)

    return normalized_data, None

def _normalize_value(field, value):
    if field == 'patient_name':
        return str(value)

    if field == 'patient_identity_removed':
        return True if value == 'YES' else False

    if field == 'acquisition_date':
        return datetime.strptime(value, '%Y%m%d').date()

    if field == 'acquisition_date_time':
        return datetime.strptime(value, '%Y%m%d%H%M%S.%f')

    if field == 'exposure_time':
        return int(value)

    if field == 'detector_temperature':
        return float(value)

    return value
