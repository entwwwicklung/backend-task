import hashlib
import io
import numpy as np
import pydicom
import random
import pydicom._storage_sopclass_uids
from pydicom.dataset import Dataset
from pydicom.filebase import DicomFileLike


def sha256sum(file):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    while n := file.readinto(mv):
        h.update(mv[:n])

    return h.hexdigest()

def create_dicom_file(broken=False, *args, **kwargs):
    if broken:
        return io.BytesIO(bytes([random.randrange(0, 256) for _ in range(0, 100)]))

    x = np.arange(16).reshape(16,1)
    pixel_array = (x + x.T) * 32
    pixel_array = np.tile(pixel_array,(16,16))
    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  
    ds = Dataset()
    ds.file_meta = meta
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    ds.PatientName = kwargs.get("PatientName") or "Test"
    ds.PatientIdentityRemoved = kwargs.get("PatientIdentityRemoved") or "NO"
    ds.PatientID = "123456"
    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15
    ds.ImagesInAcquisition = "1"
    ds.Rows = pixel_array.shape[0]
    ds.Columns = pixel_array.shape[1]
    ds.InstanceNumber = 1
    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1
    ds.DetectorTemperature = kwargs.get("DetectorTemperature") or round(random.uniform(10,100), 1) # random float
    ds.ExposureTime = kwargs.get("ExposureTime") or random.randint(10,100)

    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)

    ds.PixelData = pixel_array.tobytes()

    with io.BytesIO() as buffer:
        memory_dataset = DicomFileLike(buffer)
        memory_dataset.seek(0)
        pydicom.dcmwrite(memory_dataset, ds, write_like_original=False)
        memory_dataset.seek(0)
        return io.BytesIO(memory_dataset.read())
