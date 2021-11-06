# Celebrity Recognition using Video Intelligence API

Instructions on how to use the celebrity recognition module of the the VIdeo Intelligence API.


## Steps to trigger the job for celebrity recognition on GCP:

### Step 1: Create a request.json file which will have the following structure:
```sh
{
 "inputUri": "gs://poc-ml-metastorage-tmeg-1/darryl/comcast/cut.mp4",
 "outputUri": "gs://poc-ml-metastorage-tmeg-1/darryl/comcast/outputs/",
 "features": ["CELEBRITY_RECOGNITION"]
}
```
### Step 2: Trigger the job using the following command:
```sh
curl -X POST -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) -H "Content-Type: application/json; charset=utf-8" -d @request.json https://videointelligence.googleapis.com/v1p3beta1/videos:annotate
```
***Step 2*** will give you the job name: Please copy and keep it handy. 

### Step 3: Wait for sometime (at least for the duration equivalent to the input video)
This step is important, as if we procede before the video has been processed, the returned output will be blank.
### Step 4: Use the following command to get the output to be written to json/text file from the job:

```sh
curl -X GET -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) job_name_that_was_copied > sb205_celeb.json
```
#### Example:

```sh
curl -X GET -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) https://videointelligence.googleapis.com/v1/projects/847588923676/locations/us-west1/operations/8034134480688083078 > celeb.json
```
This will store the output of the celebrity recognition job into `celeb.json`.

### Step 5: Get the overlayed videos:

To get the overlay on videos, open the file `celeb_recognition.py` and change the path to the video on ***line 6***, also change the path to the generated JSON file which we obtained in **Step 4** on ***line 14***. Next fire the command,

```sh
python celeb_recognition.py
```
