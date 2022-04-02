import mediapipe as mp
import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt

# 防抖算法
def curr_dy(pre_dy, y_mean1, y_mean2, y_mean3):
    return (pre_dy + np.sign(y_mean2-y_mean1) + np.sign(y_mean3-y_mean2))/3

# 定长数组
def arry_stat(stat,num):
    if len(stat)>=6:
        del stat[0]  
    stat.append(num)
    
# 摇绳计数
def if_add(stat,swings):
    if stat[0]==1 and stat[1]==1 and stat[2]==1 and stat[3]==-1 and stat[4]==-1 and stat[5]==-1:
        return swings+1
    else:
        return swings

def JRcount(video_path):
    mp_drawing = mp.solutions.drawing_utils     # helps draw different detections from holistic models
    mp_holistic = mp.solutions.holistic         # import holistic models (this is just for point tracking with colors)
    mp_pose = mp.solutions.pose                 # mp pose

    # Store the input video specifics
    cap = cv2.VideoCapture(video_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))# 总帧数
    fps = int(cap.get(cv2.CAP_PROP_FPS))# 帧率信息
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    cap = cv2.VideoCapture(video_path)

    dyL_previous_round = 0
    dyR_previous_round = 0
    dyB_previous_round = 0
    # counter variables
    frame_count= 0
    jump_count = 0
    L_swings = 0
    R_swings = 0

    stat_L =[]
    stat_R =[]
    stat_B =[]
    posL = []
    posR = [] 
    posB = []

    # Initiate Pose model
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Ignoring empty camera frame.")
                break
                
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make Detections
            results = pose.process(image)
            
            # Recolor back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks 
            landmarksL = results.pose_landmarks.landmark
                
            # 甩绳 Wrists
            posL.append((landmarksL[mp_pose.PoseLandmark.LEFT_WRIST.value].y+landmarksL[mp_pose.PoseLandmark.LEFT_THUMB.value].y)/2)#wristL 
            posR.append((landmarksL[mp_pose.PoseLandmark.RIGHT_WRIST.value].y+landmarksL[mp_pose.PoseLandmark.RIGHT_THUMB.value].y)/2)#wristR

            #躯干
            Pshouder = landmarksL[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y + landmarksL[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
            Phip = landmarksL[mp_pose.PoseLandmark.LEFT_HIP.value].y + landmarksL[mp_pose.PoseLandmark.RIGHT_HIP.value].y
            posB.append((Pshouder+Phip)/4)
                    
            if frame_count>1:
                #当前轮的相对位置
                dyL_current_round = curr_dy(dyL_previous_round,posL[-1],posL[-2],posL[-3]) 
                dyR_current_round = curr_dy(dyR_previous_round,posR[-1],posR[-2],posR[-3])
                dyB_current_round = curr_dy(dyB_previous_round,posB[-1],posB[-2],posB[-3])
                
                #相较于上一轮是up or down
                arry_stat(stat_L, np.sign(dyL_current_round-dyL_previous_round))    
                arry_stat(stat_R, np.sign(dyR_current_round-dyR_previous_round))
                arry_stat(stat_B, np.sign(dyB_current_round-dyB_previous_round))
                dyL_previous_round = dyL_current_round
                dyR_previous_round = dyR_current_round
                dyB_previous_round = dyB_current_round                                                         
                if frame_count>9:
                    L_swings = if_add(stat_L,L_swings) 
                    R_swings = if_add(stat_R,R_swings)   
                    jump_count = if_add(stat_B,jump_count)
            
            # 改图
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    ) 
            cv2.putText(image,"swings: left: {}, right: {}".format(L_swings,R_swings),(5,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            cv2.putText(image,"jumps: {}".format(jump_count),(5,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            
            frame_count = frame_count+1
            cv2.imshow('Raw Webcam Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return time, 'jump rope', jump_count
