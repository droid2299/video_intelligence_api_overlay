from google.cloud import videointelligence as videointelligence
from google.cloud import videointelligence_v1p3beta1 as videointelligenceBeta
import json

from moviepy.editor import *

gcs_uri="gs://poc-ml-metastorage-tmeg-1/darryl/Comcast/QCOM10798H_better_network_superiority_spanish.mp4"
JSON_dict={}

def object_tracking(gcs_uri):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligenceBeta.Feature.OBJECT_TRACKING]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": gcs_uri}
    )
    print("\nProcessing video for object annotations.")

    result = operation.result()
    print("\nFinished processing.\n")

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    OT={}

    for object_annotation in object_annotations:
        #print("Entity description: {}".format(object_annotation.entity.description))
        
        de=object_annotation.entity.description
        
        
        #if object_annotation.entity.entity_id:
        #    print("Entity id: {}".format(object_annotation.entity.entity_id))
        """
        print(
            "Segment: {}s to {}s".format(
                object_annotation.segment.start_time_offset.seconds
                + object_annotation.segment.start_time_offset.microseconds / 1e6,
                object_annotation.segment.end_time_offset.seconds
                + object_annotation.segment.end_time_offset.microseconds / 1e6,
            )
        )
        """
        
        start=object_annotation.segment.start_time_offset.seconds+(object_annotation.segment.start_time_offset.microseconds / 1e6)
        
        end=object_annotation.segment.end_time_offset.seconds+(object_annotation.segment.end_time_offset.microseconds/ 1e6)
            
            

        #print("Confidence: {}".format(object_annotation.confidence))
        
        if(object_annotation.confidence>0.70):
            OT[de]=['from: '+str(start)+' secs','to: '+str(end)+' secs']
        
    #print(OT)

    JSON_dict['objectTracking']=OT

def detect_logo_gcs(input_uri):

    client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.Feature.LOGO_RECOGNITION]

    operation = client.annotate_video(
        request={"features": features, "input_uri": input_uri}
    )

    #print(u"Waiting for operation to complete...")
    response = operation.result()

    # Get the first response, since we sent only one video.
    annotation_result = response.annotation_results[0]
    output_dict = {'Logo_Detections':[]}

    # Annotations for list of logos detected, tracked and recognized in video.
    for logo_recognition_annotation in annotation_result.logo_recognition_annotations:
        one_det = {}
        entity = logo_recognition_annotation.entity

        # Opaque entity ID. Some IDs may be available in [Google Knowledge Graph
        # Search API](https://developers.google.com/knowledge-graph/).
        #print(u"Entity Id : {}".format(entity.entity_id))

        #print(u"Description : {}".format(entity.description))
        one_det['Description'] = entity.description

        one_det['Timestamps'] = []
        # All logo tracks where the recognized logo appears. Each track corresponds
        # to one logo instance appearing in consecutive frames.
        for track in logo_recognition_annotation.tracks:
            
            """

            # Video segment of a track.
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    track.segment.start_time_offset.seconds,
                    track.segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    track.segment.end_time_offset.seconds,
                    track.segment.end_time_offset.microseconds * 1000,
                )
            )
            print(u"\tConfidence : {}".format(track.confidence))
            
            
            """
            one_det['Timestamps'].append({'Start Time':track.segment.start_time_offset.seconds + track.segment.start_time_offset.microseconds *1e-6,
                                          'End Time':track.segment.end_time_offset.seconds + track.segment.end_time_offset.microseconds *1e-6})
        
            # The object with timestamp and attributes per frame in the track.
            
            """
            for timestamped_object in track.timestamped_objects:
                # Normalized Bounding box in a frame, where the object is located.
                normalized_bounding_box = timestamped_object.normalized_bounding_box
                print(u"\n\t\tLeft : {}".format(normalized_bounding_box.left))
                print(u"\t\tTop : {}".format(normalized_bounding_box.top))
                print(u"\t\tRight : {}".format(normalized_bounding_box.right))
                print(u"\t\tBottom : {}".format(normalized_bounding_box.bottom))

                # Optional. The attributes of the object in the bounding box.
                for attribute in timestamped_object.attributes:
                    print(u"\n\t\t\tName : {}".format(attribute.name))
                    print(u"\t\t\tConfidence : {}".format(attribute.confidence))
                    print(u"\t\t\tValue : {}".format(attribute.value))

            # Optional. Attributes in the track level.
            for track_attribute in track.attributes:
                print(u"\n\t\tName : {}".format(track_attribute.name))
                print(u"\t\tConfidence : {}".format(track_attribute.confidence))
                print(u"\t\tValue : {}".format(track_attribute.value))
                
                """

        # All video segments where the recognized logo appears. There might be
        # multiple instances of the same logo class appearing in one VideoSegment.
        
        """
        for segment in logo_recognition_annotation.segments:
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    segment.start_time_offset.seconds,
                    segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    segment.end_time_offset.seconds,
                    segment.end_time_offset.microseconds * 1000,
                )
            )
        """
        output_dict['Logo_Detections'].append(one_det)
    #return output_dict
    JSON_dict['logoDetections']=output_dict['Logo_Detections']
    
def detect_person_attributes(gcs_uri):
    """Detects people in a video."""

    client = videointelligence.VideoIntelligenceServiceClient()

    # Configure the request
    config = videointelligence.PersonDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=True,
        include_pose_landmarks=False,
    )
    context = videointelligence.VideoContext(person_detection_config=config)

    # Start the asynchronous request
    operation = client.annotate_video(
        request={
            "features": ['PERSON_DETECTION'],
            "input_uri": gcs_uri,
            "video_context": context,
            #"output_uri":output_uri
            
        }
    )

    #print("\nProcessing video for person detection annotations.")
    result = operation.result(timeout=1000000)

    #print("\nFinished processing.\n")
    
  

    # Retrieve the first result, because a single video was processed.
    annotation_result = result.annotation_results[0]
    #print(annotation_result)
    attributes_tag=[]
    for annotation in annotation_result.person_detection_annotations:
        #print("Person detected:")
        for track in annotation.tracks:
            """
            print(
                "Segment: {}s to {}s".format(
                    track.segment.start_time_offset.seconds
                    + track.segment.start_time_offset.microseconds / 1e6,
                    track.segment.end_time_offset.seconds
                    + track.segment.end_time_offset.microseconds / 1e6,
                )
            )
            """

            # Each segment includes timestamped objects that include
            # characteristics - -e.g.clothes, posture of the person detected.
            # Grab the first timestamped object
            count=0
            #print("Attributes:")
            for i in track.timestamped_objects:
                count+=1
                #timestamped_object = track.timestamped_objects
                """
                box = i.normalized_bounding_box
                print("Bounding box:")
                print("\tleft  : {}".format(box.left))
                print("\ttop   : {}".format(box.top))
                print("\tright : {}".format(box.right))
                print("\tbottom: {}".format(box.bottom))
                
                """

                # Attributes include unique pieces of clothing,
                # poses, or hair color.
                
                for attribute in i.attributes:
                    """
                    print(
                        "\t{}:{} {}".format(
                            attribute.name, attribute.value, attribute.confidence
                        )
                    )
                    """
                    if attribute.confidence>0.80:
                        #print("{}:{} {}".format(attribute.name, attribute.value, attribute.confidence))
                        attributes_tag.append(attribute.value)

                # Landmarks in person detection include body parts such as
                # left_shoulder, right_ear, and right_ankle
                """
                print("Landmarks:")
                for landmark in i.landmarks:
                    print(
                        "\t{}: {} (x={}, y={})".format(
                            landmark.name,
                            landmark.confidence,
                            landmark.point.x,  # Normalized vertex
                            landmark.point.y,  # Normalized vertex
                        )
                    )
            """
    if len(set(attributes_tag))>0:            
        JSON_dict['attireAttributes']=list(set(attributes_tag))
    else:
        JSON_dict['attireAttributes']=""
        
        
def detect_faces(gcs_uri):
    """Detects faces in a video."""

    client = videointelligenceBeta.VideoIntelligenceServiceClient()

    # Configure the request
    config = videointelligenceBeta.FaceDetectionConfig(
        include_bounding_boxes=True, include_attributes=True
    )
    context = videointelligenceBeta.VideoContext(face_detection_config=config)

    # Start the asynchronous request
    operation = client.annotate_video(
        request={
            "features": [videointelligenceBeta.Feature.FACE_DETECTION],
            "input_uri": gcs_uri,
            "video_context": context,
        }
    )

    print("\nProcessing video for face detection annotations.")
    result = operation.result()

    print("\nFinished processing.\n")

    # Retrieve the first result, because a single video was processed.
    annotation_result = result.annotation_results[0]
  
    facial_attributes=[]
    for annotation in annotation_result.face_detection_annotations:
        #print("Face detected:")
        for track in annotation.tracks:
            """
            print(
                "Segment: {}s to {}s".format(
                    track.segment.start_time_offset.seconds
                    + track.segment.start_time_offset.microseconds / 1e6,
                    track.segment.end_time_offset.seconds
                    + track.segment.end_time_offset.microseconds / 1e6,
                )
            )
            """
            
            # Each segment includes timestamped faces that include
            # characteristics of the face detected.
            # Grab the first timestamped face
            
            for i in track.timestamped_objects:
            #timestamped_object = track.timestamped_objects
                """
                box = i.normalized_bounding_box
                print("Bounding box:")
                print("\tleft  : {}".format(box.left))
                print("\ttop   : {}".format(box.top))
                print("\tright : {}".format(box.right))
                print("\tbottom: {}".format(box.bottom))
                """
                
           

                # Attributes include glasses, headwear, smiling, direction of gaze
                #print("Attributes:")
                for attribute in i.attributes:
                    #print(
                      #  "\t{}:{} {}".format(
                      #      attribute.name, attribute.value, attribute.confidence
                       # )
                      #  )
                        
                    if(attribute.confidence>0.15):
                        facial_attributes.append(attribute.name)
    if len(set(facial_attributes))>0:            
        JSON_dict['facialAttributes']=list(set(facial_attributes))
    else:
        JSON_dict['facialAttributes']=""
        
def detect_text_gcs(input_uri):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]

    operation = video_client.annotate_video(
        request={"features": features, "input_uri": input_uri}
    )

    #print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    annotation_result = result.annotation_results[0]
    detections = {'Text Detections':[]}

    for text_annotation in annotation_result.text_annotations:
        one_det = {}
        #print("\nText: {}".format(text_annotation.text))
        one_det['Text'] = text_annotation.text

        # Get the first text segment
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset
        """
        print(
            "start_time: {}, end_time: {}".format(
                start_time.seconds + start_time.microseconds * 1e-6,
                end_time.seconds + end_time.microseconds * 1e-6,
            )
        )
        """
        one_det['Start Time'] = start_time.seconds + start_time.microseconds * 1e-6
        one_det['End Time'] = end_time.seconds + end_time.microseconds * 1e-6

        #print("Confidence: {}".format(text_segment.confidence))
#       one_det['Confidence'] = text_segment.confidence

        # Show the result for the first frame in this segment.
        frame = text_segment.frames[0]
        time_offset = frame.time_offset
        """
        print(
            "Time offset for the first frame: {}".format(
                time_offset.seconds + time_offset.microseconds * 1e-6
            )
        )
       
#        one_det['Time offset for the first frame'] = time_offset.seconds + time_offset.microseconds * 1e-6

#        bbox = []
        
        print("Rotated Bounding Box Vertices:")
        for vertex in frame.rotated_bounding_box.vertices:
            print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))
#            bbox.append({'Vertex.x':vertex.x,'Vertex.y':vertex.y})
#        one_det['Rotated Bounding Box Vertices'] = bbox
        """
        detections['Text Detections'].append(one_det)
    return detections

        
detect_logo_gcs(gcs_uri)
object_tracking(gcs_uri)
detect_person_attributes(gcs_uri)
detect_faces(gcs_uri)
output = detect_text_gcs(gcp_uri)
JSON_dict['textRecognition']=output['Text Detections']
print(JSON_dict)

input_uri_path = gcs_uri
input_video_name = input_uri_path.split("/")[-1]
output_name = "outputs/"+input_video_name.split(".")[0]+".json"
import os
if not os.path.exists('outputs'):
    os.makedirs('outputs')

json_object = json.dumps(JSON_dict, indent = 4)
json_object = json_object.replace("Start Time", "startTime")
json_object = json_object.replace("End Time", "endTime")
with open(output_name, "w") as outfile: 
    outfile.write(json_object)
