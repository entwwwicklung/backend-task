# backend-task


## Introduction

Just wanted to provide some information on how I've created these two endpoints.
Even tho it was mentioned that it is not needed to dive into how DICOM file works, I had to study it in order to better understand what needs to be done. Since there are too many metadata fields available I've decided for the sake of this task just to parse some of them, cause they represent different types of values (str, bool, float, int, date, etc...):
* PatientName
* PatientIdentityRemoved
* AcquisitionDate
* AcquisitionDateTime
* ExposureTime
* DetectorTemperature

## Usage

### `GET` `/api/documents/`

Returns a JSON list of dicom metadata objects.
Possible exact match filters (query params) are:
* `id`
* `patient_identity_removed`
* `acquisition_date`
* `acquisition_date_time`
* `exposure_time`
* `detector_temperature`

And some from your "bonus" section which are looking for greater/less than values
* `min_acquisition_date`
* `max_acquisition_date`
* `min_acquisition_date_time`
* `max_acquisition_date_time`
* `min_exposure_time`
* `max_exposure_time`
* `min_detector_temperature`
* `max_detector_temperature`

Due to the lack of time, I didn't implement ability to use `OR` in query params, but if it is necessary I could write up a class for that as well.

Also you can order results, here's list of fields that can be used for ordering:

* id
* patient_identity_removed
* acquisition_date
* exposure_time
* detector_temperature

Example query string for results in ascending order:
```
/api/documents?ordering=exposure_time
```
and for descending order:
```
/api/documents?ordering=-exposure_time
```


### `POST` `/api/documents/`

This endpoint accepts `multipart/form-data` request which should contain a DICOM file which will be parsed.


## Tests

 I've added just a couple of basic test cases since I didn't had much time, however if needed I can cover more cases and increase the tests coverage. 
 For POST requests tests are using DICOM files created in memory when making a call to client.

 ```Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 0.036s

OK
Destroying test database for alias 'default'...
```