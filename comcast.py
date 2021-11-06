from google.cloud import videointelligence_v1 as vi
from datetime import timedelta
import cv2

'''
Function to detect  logos and track object

Params: video_uri: input gcs uri
        myfeatures: od or logo (in string)
        segments: part of the video to process (none = full video)

Returns: result in annotation format
'''
def detect_logos(video_uri: str, myfeatures: str , segments= None) -> vi.VideoAnnotationResults:
    print(myfeatures)
    video_client = vi.VideoIntelligenceServiceClient()
    if(myfeatures == 'od'):
      type = [vi.Feature.OBJECT_TRACKING]
    elif(myfeatures == 'logo'):
      type = [vi.Feature.LOGO_RECOGNITION]
    features = type #[vi.Feature.OBJECT_TRACKING]
    context = vi.VideoContext(segments=segments)
    request = vi.AnnotateVideoRequest(
        input_uri=video_uri,
        features=features,
        video_context=context,
    )
    print(f"Processing video: {video_uri}...")
    operation = video_client.annotate_video(request)
  
    return operation.result().annotation_results[0]
'''
Function to print a summary of the logos detected

Params: results: output of the detect_logos function

Returns: none
'''

def print_detected_logos(results: vi.VideoAnnotationResults):
    # First result only, as a single video is processed
    annotations = results.logo_recognition_annotations
    print(f" Detected logos: {len(annotations)} ".center(80, "-"))
    for annotation in annotations:
        entity = annotation.entity
        entity_id = entity.entity_id
        description = entity.description
        for track in annotation.tracks:
            confidence = track.confidence
            t1 = track.segment.start_time_offset.total_seconds()
            t2 = track.segment.end_time_offset.total_seconds()
            logo_frames = len(track.timestamped_objects)
            print(
                f"{confidence:4.0%}",
                f"{t1:>7.3f}",
                f"{t2:>7.3f}",
                f"{logo_frames:>3} fr.",
                f"{entity_id:<15}",
                f"{description}",
                sep=" | ",
            )
            entity_list.append(entity_id)

'''
Function to  print the bounding box coordinates and save then in a dictionary(logo_dict) and write them to the filename provided(default: results.txt)

Params: results: output of the detect_logos function
        entity_id: ID of the logo detected (part of the output of detect_logo)
        min_confidence: the minimum confidence required to print and save the results

Returns: none
'''
def print_logo_frames(results: vi.VideoAnnotationResults, entity_id: str, min_confidence):
    def keep_annotation(annotation: vi.LogoRecognitionAnnotation) -> bool:
        return annotation.entity.entity_id == entity_id
    #print("IN PRINT LOGO")
    # First result only, as a single video is processed
    annotations = results.logo_recognition_annotations
    annotations = [a for a in annotations if keep_annotation(a)]
    for annotation in annotations:
        description = annotation.entity.description
        for track in annotation.tracks:
            confidence = track.confidence
            if min_confidence > confidence:
               continue
            print(
                f" {description},"
                f" confidence: {confidence:.0%},"
                f" frames: {len(track.timestamped_objects)} ".center(80, "-")
            )
            for timestamped_object in track.timestamped_objects:
                t = timestamped_object.time_offset.total_seconds()
                box = timestamped_object.normalized_bounding_box
                print(
                    f"{t:>7.3f}",
                    f"({box.left:.5f}, {box.top:.5f})",
                    f"({box.right:.5f}, {box.bottom:.5f})",
                    sep=" | ",
                )
                
                temp_list = []
                #temp_list.append(timestamped_object.time_offset.total_seconds())
                temp_list.append(box.left) 
                temp_list.append(box.top)
                temp_list.append(box.right)
                temp_list.append(box.bottom)
                temp_list.append(description)
                temp_list.append(confidence)
                print(temp_list)
                print('\n')
                frame_no = int(float(timestamped_object.time_offset.total_seconds())*FPS)
                logo_dict[frame_no] = temp_list               

                
                f.write(f"{t},")
                f.write(f"{box.left}, {box.top},")
                f.write(f"{box.right}, {box.bottom},")
                f.write(f" {description},")
                f.write(f"{confidence}"+"\n")
                
                #   )
'''
Function to print the summary of the objects detected, write to a dictionary(logo_dict) and write to a file(default = results.txt)

Params: results: output of the detect_logos function
        min_confidence: the minimum confidence to show and write the detected objects

Returns: none
'''
def print_detected_objects(
    results: vi.VideoAnnotationResults, min_confidence: float = 0.7
):
    annotations = results.object_annotations
    annotations = [a for a in annotations if min_confidence <= a.confidence]

    print(
        f" Detected objects: {len(annotations)}"
        f" ({min_confidence:.0%} <= confidence) ".center(80, "-")
    )
    for annotation in annotations:
        entity = annotation.entity
        description = entity.description
        entity_id = entity.entity_id
        confidence = annotation.confidence
        t1 = annotation.segment.start_time_offset.total_seconds()
        t2 = annotation.segment.end_time_offset.total_seconds()
        frames = len(annotation.frames)
        print(
            f"{description:<22}",
            f"{entity_id:<10}",
            f"{confidence:4.0%}",
            f"{t1:>7.3f}",
            f"{t2:>7.3f}",
            f"{frames:>2} fr.",
            sep=" | ",
        )
        for i in range(0 , len(annotation.frames)):
            frame = annotation.frames[i]
            box = frame.normalized_bounding_box
            t = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
            print('Time offset = {}'.format(t))
            print('Box = {}'.format(box))
            temp_list = []
                #temp_list.append(timestamped_object.time_offset.total_seconds())
            temp_list.append(box.left) 
            temp_list.append(box.top)
            temp_list.append(box.right)
            temp_list.append(box.bottom)
            temp_list.append(description)
            temp_list.append(confidence)
            print(temp_list)
            print('/n')
            frame_no = int(float(t)*FPS)
            logo_dict[frame_no] = temp_list

            f.write(f"{t},")
            f.write(f"{box.left}, {box.top},")
            f.write(f"{box.right}, {box.bottom},")
            f.write(f" {description},")
            f.write(f"{confidence}"+"\n")




'''
Main Caller function which calls the od/ot or logo detection function based on args. It reads the video file and draws the overlay to save the video at comcast.avi

Params: input_uri: GCS URI of the input file (default: cut.mp4)
        path: Path to the downloaded video file.
        filename: Name of th file to store the results (default: results.txt)
        features: Argument to decide od/ot or logo_detection
        min_confidence: minimum confidence to display and save results

returns: none
'''
def caller(input_uri , path , filename , features , min_confidence: float = 0.7):               

    video_uri = input_uri
    global entity_list , f , logo_dict , temp_list , FPS
    entity_list = []
    logo_dict = {}
    temp_list = []
    f = open(filename , 'w')

    #reading video from input path
    cap = cv2.VideoCapture(path)
    FPS = cap.get(cv2.CAP_PROP_FPS)

    #calling the required functions based on the feature
    if features == 'logo':
       response = detect_logos(video_uri , features)
       print("Got Response")
       #print(response)
       print_detected_logos(response)

    for entity in entity_list:
        print_logo_frames(response, entity , min_confidence)
    
    if features == 'od':
       response = detect_logos(video_uri , features)
       print("Got Response")
       #print(response)
       print_detected_objects(response , min_confidence)
    f.close()
   
    print(logo_dict)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    print(size)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Length in Frames: "+str(length))
   
    out= cv2.VideoWriter('comcast.avi', cv2.VideoWriter_fourcc(*'MJPG'),FPS, size)
    count = 0
    if (cap.isOpened()== False):
       print("Error opening video stream or file")

    while(cap.isOpened()):
       ret, frame = cap.read()
       if ret == True:
          if count in logo_dict.keys():
             temp_list = logo_dict[count] 
             print(count)
             count += 1
          elif (count - 1) in logo_dict.keys(): 
             temp_list = logo_dict[count - 1]
             print(count)
             count += 1 
          elif (count - 2) in logo_dict.keys():
             temp_list = logo_dict[count - 2]
             print(count)
             count += 1
          else:
             print(count)
             count += 1
             out.write(frame)
             continue

          x1 =int(float(temp_list[0])*frame.shape[1])
          y1 =int(float(temp_list[1])*frame.shape[0])
          x2 =int(float(temp_list[2])*frame.shape[1])
          y2 =int(float(temp_list[3])*frame.shape[0])
          cv2.rectangle(frame  , (x1, y1) , (x2,y2) , (255,0,255) , 4)
          cv2.putText(frame , temp_list[4]
            #+","+i[6]              #uncomment for confidence
            , (x1,y1-2) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255,0,255) , 4 , cv2.LINE_AA)
          out.write(frame)
          if count == length - 1:
             print("in IF")
             break
    cap.release()
    out.release()

