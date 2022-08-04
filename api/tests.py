from copy import deepcopy
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import DicomMetadata
from api.utils import create_dicom_file

class DocumentsTests(APITestCase):
    def test_create_document_201(self):
        data = {
            'PatientName': 'Johnatan',
            'ExposureTime': 40,
        }
        file = create_dicom_file(**data)
        response = self.client.post('/api/documents/', {'file': file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert DicomMetadata.objects.count() == 1
        assert DicomMetadata.objects.get().patient_name == data['PatientName']
        assert DicomMetadata.objects.get().exposure_time == data['ExposureTime']

    def test_not_accepting_duplicate_files(self):
        file = create_dicom_file()
        duplicate_file = deepcopy(file)
        # Create 1st record and make sure that it is created
        response = self.client.post('/api/documents/', {'file': file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert DicomMetadata.objects.count() == 1

        # Now try to create another record using the same file
        response = self.client.post('/api/documents/', {'file': duplicate_file}, format='multipart')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        # Making sure that there is still just one file
        assert DicomMetadata.objects.count() == 1

    def test_missing_file(self):
        response = self.client.post('/api/documents/', {}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert DicomMetadata.objects.count() == 0

    def test_send_broken_file(self):
        file = create_dicom_file(broken=True)

        response = self.client.post('/api/documents/', {'file': file}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert DicomMetadata.objects.count() == 0

    def test_list(self):
        metadata = DicomMetadata(
            patient_name = 'Test',
            patient_identity_removed = True,
            exposure_time = 4555,
        )
        metadata.save()
        response = self.client.get('/api/documents/', format='json')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['patient_name'] == metadata.patient_name
        assert data[0]['patient_identity_removed'] == metadata.patient_identity_removed
        assert data[0]['exposure_time'] == metadata.exposure_time

    def test_list_patient_identity_removed_filter(self):
        metadata = DicomMetadata(
            patient_name = 'Test',
            patient_identity_removed = True,
        )
        metadata.save()
        metadata_2 = DicomMetadata(
            patient_name = 'Test2',
            patient_identity_removed = False,
        )
        metadata_2.save()
        response = self.client.get(f'/api/documents/', {'patient_identity_removed': False}, format='json')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['patient_name'] == metadata_2.patient_name
        assert data[0]['patient_identity_removed'] == metadata_2.patient_identity_removed

    def test_list_patient_min_exposure_time_filter(self):
        metadata = DicomMetadata(
            patient_name = 'Test',
            exposure_time = 30
        )
        metadata.save()
        metadata_2 = DicomMetadata(
            patient_name = 'Test2',
            exposure_time = 40
        )
        metadata_2.save()
        response = self.client.get(f'/api/documents/', {'min_exposure_time': 35}, format='json')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['patient_name'] == metadata_2.patient_name
        assert data[0]['exposure_time'] == metadata_2.exposure_time
