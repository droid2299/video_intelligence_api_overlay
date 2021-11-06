import cv2
import collections
import cv2
import json

vidcap = cv2.VideoCapture('/home/darrylsf/Downloads/Comcast_Sizzle_040720.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
success, image = vidcap.read()
height, width, _ = image.shape
count = 0
success = True
writer = None

f = open("sizzle2.json", )
json_file = json.load(f)

'''
while success:
    success, frame = vidcap.read()
    count += 1
    # print("time stamp current frame:", count / fps)
'''


#width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
#height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = vidcap.get(cv2.CAP_PROP_FPS)

test = json_file['response']['annotationResults']
type(test)

for word in test:
    test1 = word

celeb_tracks = test1['celebrityRecognitionAnnotations']['celebrityTracks']
#print(celeb_tracks[4])
final_list =[]
final_dict={}
for words in celeb_tracks:
    temp_list = []
    celeb_list = []
    #print(len(words.keys()))
    if(len(words.keys())==2):
        for celebr in words["celebrities"]:
            celebr_name = celebr['celebrity']['displayName']
            #confidence = celebr['confidence']
            celeb_list.append(celebr_name)
            #celeb_list.append(confidence)
            #print(celeb_list)

        for bbox in words['faceTrack']['timestampedObjects']:
            #print("IN BBOX")
            #print(bbox)
            #print(celeb_list)
            try:

                top = bbox['normalizedBoundingBox']['top'] * height
                left = bbox['normalizedBoundingBox']['left'] * width
                bottom = bbox['normalizedBoundingBox']['bottom'] * height
                right = bbox['normalizedBoundingBox']['right'] * width
                # timeoffset = float(bbox['timeOffset'][:-1]) * fps -75
                timeoffset = float(bbox['timeOffset'][:-1]) * fps
                temp_list = [celeb_list[0],top,left,bottom,right]
                final_dict[round(timeoffset)] = temp_list
                final_list.append(temp_list)
            except:
                pass

print(final_dict)



frame_width = int(vidcap.get(3))
frame_height = int(vidcap.get(4))
size = (frame_width, frame_height)
print(size)
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Length in Frames: "+str(length))
   
out= cv2.VideoWriter('comcast.avi', cv2.VideoWriter_fourcc(*'MJPG'),fps, size)
count = 0
print("BEFORE OPENED")
if (vidcap.isOpened()== False):

    print("Error opening video stream or file")
while(vidcap.isOpened()):
       ret, frame = vidcap.read()
       if ret == True:
            if count in final_dict.keys():
                temp_list = final_dict[count] 
                print(count)
                print(temp_list)
                count += 1
            elif (count - 1) in final_dict.keys(): 
                temp_list = final_dict[count - 1]
                print(count)
                print(temp_list)
                count += 1 
            elif (count - 2) in final_dict.keys():
                temp_list = final_dict[count - 2]
                print(count)
                print(temp_list)
                count += 1
            else:
                print(count)
                count += 1
                print("nothing")
                out.write(frame)
                continue

            start_point = (int(temp_list[2]),int(temp_list[1]))
            end_point = (int(temp_list[4]),int(temp_list[3]))
            frame = cv2.rectangle(frame  , start_point , end_point , (255,0,255) , 4)
            print(type(temp_list[0]))
            print(temp_list)
            '''
            cv2.putText(frame , temp_list[0]
            #+","+i[6]              #uncomment for confidence
            , (temp_list[2],str(temp_list[1]-4)) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255,0,255) , 4 , cv2.LINE_AA)'''

            frame = cv2.putText(frame, temp_list[0], (int(temp_list[2])-10,int(temp_list[1])-10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,0,255), 4, cv2.LINE_AA)
            out.write(frame)
            if count == length - 1:
                print("in IF")
                break
cap.release()
out.release()


'''
test3 = {'celebrities': [
    {'celebrity': {'name': 'video-intelligence//m/0j27tl9', 'displayName': 'Lori Greiner'}, 'confidence': 0.85414344}],
    'faceTrack': {'segment': {'startTimeOffset': '2.002s', 'endTimeOffset': '2.502500s'}, 'timestampedObjects': [{
        'normalizedBoundingBox': {
            'left': 0.48671874,
            'top': 0.06111111,
            'right': 0.73046875,
            'bottom': 0.56527776},
        'timeOffset': '2.002s'},
        {
            'normalizedBoundingBox': {
                'left': 0.4859375,
                'top': 0.06111111,
                'right': 0.728125,
                'bottom': 0.5625},
            'timeOffset': '2.102100s'},
        {
            'normalizedBoundingBox': {
                'left': 0.48671874,
                'top': 0.06388889,
                'right': 0.725,
                'bottom': 0.55694443},
            'timeOffset': '2.202200s'},
        {
            'normalizedBoundingBox': {
                'left': 0.4875,
                'top': 0.06527778,
                'right': 0.7242187,
                'bottom': 0.5555556},
            'timeOffset': '2.302300s'},
        {
            'normalizedBoundingBox': {
                'left': 0.48828125,
                'top': 0.06666667,
                'right': 0.72578126,
                'bottom': 0.55694443},
            'timeOffset': '2.402400s'},
        {
            'normalizedBoundingBox': {
                'left': 0.4890625,
                'top': 0.06527778,
                'right': 0.728125,
                'bottom': 0.5611111},
            'timeOffset': '2.502500s'}]}}

test3.keys()

for celebr in test3["celebrities"]:
    celebr_name = celebr['celebrity']['displayName']

for bbox in test3['faceTrack']['timestampedObjects']:
    print(bbox)
bbox = {'normalizedBoundingBox': {'left': 0.4890625, 'top': 0.06527778, 'right': 0.728125, 'bottom': 0.5611111},
        'timeOffset': '2.502500s'}

bbox.keys()
top = bbox['normalizedBoundingBox']['top'] * width
left = bbox['normalizedBoundingBox']['left'] * height
bottom = bbox['normalizedBoundingBox']['bottom'] * width
right = bbox['normalizedBoundingBox']['right'] * height
timeoffset = float(bbox['timeOffset'][:-1]) * fps


len(final_list)
count = -1
#start_point = (int(top), int(left))
#end_point = (int(bottom), int(right))
color = (0, 200, 0)
thickness = 4

i =0
font = cv2.FONT_HERSHEY_SIMPLEX

temp_count =0
temp =0

print("hello")
print(final_list)
print(len(final_list))

while success:
    success, frame = vidcap.read()
    count = count + 1
    print(count)
    print(final_list[i][5])

    try:
        check_frame = final_list[i][5]
    except:
        pass
    
    if check_frame==0:
        check_frame =1
    #print("hello")
    #print(check_frame)
    #print(count)


    if count == check_frame or temp_count ==1:
        # frame = cv2.rectangle(frame, (top,left), (bottom,right), (255, 0, 0), 2)
        start_point = (int(final_list[i][3]),int(final_list[i][2]))
        end_point = (int(final_list[i][5]),int(final_list[i][4]))

        frame = cv2.rectangle(frame,start_point , end_point, color, thickness)

        
        frame = cv2.putText(frame, final_list[i][0], (int(final_list[i][3])-10,int(final_list[i][2])-10), font,
                            2, color, 8, cv2.LINE_AA)

        frame = cv2.putText(frame, str(round(final_list[i][1],2)), (int(final_list[i][5]+10),int(final_list[i][4])+10), font,
                            2, color, 8, cv2.LINE_AA)

        frame = cv2.putText(frame, final_list[i][0], (int(final_list[i][5] -200), int(final_list[i][4]) + 50), font,
                            1, color, 4, cv2.LINE_AA)

        frame = cv2.putText(frame, str(round(final_list[i][1], 2)),
                            (int(final_list[i][3])+170,int(final_list[i][2])+10), font,
                            1, color, 4, cv2.LINE_AA)
        # cv2.imwrite("outimage.jpg", image)
        temp = temp +1
        temp_count = 1
        if temp ==3:
            i = i+1
            temp_count =0
            temp = 0
    
    import os
    os.chdir("D:\\prabhu\\frames")
    filename = "frame"+str(count)+".jpg"
    cv2.imwrite(filename,frame)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter('output_video9.avi', fourcc, fps, (frame.shape[1], frame.shape[0]), True)
    if writer is not None:
        writer.write(frame)
        print("Writing frame", count)


writer.release()
vidcap.release()
'''