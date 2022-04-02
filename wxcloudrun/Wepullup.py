import cv2
import mediapipe as mp
import os
import time
import datetime
import posemodule as pm
import math


def pullup(video_path):
    pTime = 0
   
    cap = cv2.VideoCapture(video_path)
    detector = pm.poseDetector()

    #up3 y500
    # down 1000
    # up15 1100
    #  down 1100
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


    count = 0

    f=0
    time.sleep(5)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        
        img = detector.findPose(img)
        lmlist = detector.getPosition(img,draw=False)
        #print(lmlist[3])
       
        
        if len(lmlist)!=0:
            cv2.circle(img,(lmlist[15][1],lmlist[15][2]),10,(0,0,255),cv2.FILLED)
            cv2.circle(img,(lmlist[3][1],lmlist[3][2]),10,(0,0,255),cv2.FILLED) 
            y1 = lmlist[3][2]
            y2 = lmlist[20][2]
            
            length = y2-y1
            if length>=0 and f==0:
                f=1
            elif length<0 and f==1:
                f=0
                count=count+1


            #print(length)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            if success:
                img = cv2.resize(img, (600,400))
                cv2.putText(img,"Total pull ups: {}".format(int(count)),(5,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                cv2.imshow("Image",img)
                #output.write(img)
            
            if cv2.waitKey(10) and 0xFF == ord('q') :
                cap.release()
                cv2.destroyAllWindows()
                break
            
            
            #calories = 1*count
        
    curtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(curtime, count)

    return curtime, 'pull up', count

# pullup("C:\\Users\yyg20\\OneDrive - zrmmg\\capstone\\test_vid\\pullup1.mp4")