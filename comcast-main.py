import cv2
import shutil
import get_params
import comcast
import speech_to_text
#import comcast_od
from google.cloud import storage
import os
import subprocess

client = storage.Client()


def copy_gcs_to_local(full_path, target_folder):
    """ copy data from gcs bucket location to local
         Parameters
         ----------
         full_path (str): gcs bucket location
         target_folder (str): local path (relative)

         Return type
         -----------
         str - file_name
                 name of the file that was copied to the bucket
     """

    temp_path = str(full_path).replace("gs://", "").split("/")  # Split the gcs bucket path
    bucket_path = temp_path[0]
    file_path = temp_path[1]
    if len(temp_path) > 2:
        file_path = '/'.join(temp_path[1:])
    file_name = temp_path[-1]

    # Reaching the file path in bucket and downloading it into local/target_path
    bucket = client.get_bucket(bucket_path)
    blob = bucket.get_blob(file_path)
    target_path = os.path.join(target_folder, file_name)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    blob.download_to_filename(target_path)

    print("Copying done")
    print(target_path)
    return target_path


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    #bucket_name = "poc-ml-metastorage-tmeg-1/darryl/Comcast/"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def video_info(video_filepath):
    """ this function returns number of channels, bit rate, and sample rate of the video"""

    video_data = mediainfo(video_filepath)
    channels = video_data["channels"]
    bit_rate = video_data["bit_rate"]
    sample_rate = video_data["sample_rate"]

    return channels, bit_rate, sample_rate

def video_to_audio(video_filepath, audio_filename, video_channels, video_bit_rate, video_sample_rate):
    command = f"ffmpeg -i {video_filepath} -b:a {video_bit_rate} -ac {video_channels} -ar {video_sample_rate} -vn {audio_filename}"
    subprocess.call(command, shell=True)
    blob_name = f"{audio_filename}"
    upload_to_gcs("poc-ml-metastorage-tmeg-1/darryl/Comcast/", audio_filename, blob_name)
    


def main():
    input_uri = FLAGS.gcp_uri
    detection_type = FLAGS.type
    min_confidence = FLAGS.min_confidence
    file_name = FLAGS.save_results_txt

    local_path = "input_video/"
    path = copy_gcs_to_local(input_uri, local_path)
    #save_frames(path)

    if detection_type == 'logo_detection':
        features = 'logo'
        comcast.caller(input_uri , path , file_name , features , min_confidence)

    elif detection_type == 'od_ot':
        features = 'od'
        comcast.caller(input_uri , path , file_name , features , min_confidence)

    elif detection_type == 'video_subtitle':
        print("Getting Video Info....")
        channels, bit_rate, sample_rate = video_info(path)
        print("Summary:")
        print("Channel: "+str(channels))
        print("Bit Rate: "+str(bit_rate))
        print("sample_rate: "+str(sample_rate))
        print("Generating Audio File....")
        video_to_audio(path, "audio.wav", channels, bit_rate, sample_rate)
        audio_uri = 'poc-ml-metastorage-tmeg-1/darryl/Comcast/audio.wav'
        speech_to_text.caller(audio_uri , sample_rate , FLAGS.language_code , generated_subtitle)





if __name__ == '__main__':

    FLAGS = get_params.parse_arguments()
    main()
