# Metadata Generation using the Video Intelligence API

A repository to overlay bounding boxes and other information such as description and confidence from the output of Video Intelligence API on videos and to also generate JSON files for metadata generation. Currently, this script only includes

- Object detection and tracking
- Logo Detection
- Video Captioning (No translation)

****Note:*** For celebrity recognition, please refer `celebrity_detection.md`*

## Installation & Usage:

### Dependencies:
```sh
pip install -r requirements.txt
```

### Arguments:

- **- -gcp_uri:** GCP Bucket URI to the input video file to be processed. [REQUIRED]
- **- -type:** Type of detection required: logo_detection, object tracking or video captioning. [REQUIRED]
- **- -save_results_txt:** Path to save the bbox coordinates, coodrinates, time_offset and confidence in a txt file. 
- **- -min_confidence:** Minimum Confidence for overlaying on videos.
- **- -language_code:** Language that will be used to transcribe the audio in the video file.

****Note:*** By default the audio extracted from the video file will be uploaded to `poc-ml-metastorage-tmeg-1/darryl/Comcast/`. To change, edit ***line 78*** in file `comcast-main.py`. Please refer `get_params.py` for the default values.*

### Usage:

#### For overlaying videos, run:
```sh
python comcast-main.py [args]
```
Results will be saved in a video file called *comcast.avi*
#### For Generating JSON files, run:

```sh
python json_builder.py
```
JSON results will be saved in a folder called outputs with the same name as input video.



