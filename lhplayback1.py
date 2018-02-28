from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import pickle

w=320
h=240
fps=60

nbeams=3

with open('/home/pi/calib.txt','rb') as fp:
    lims=pickle.load(fp)

ms=[]
cs=[]
for l in lims:
    ms.append((l[1][1]-l[0][1])/(l[1][0]-l[0][0]))
    cs.append(l[0][1])
camera=PiCamera()
camera.resolution=(w,h)
camera.framerate=fps
rawCapture=PiRGBArray(camera,size=(w,h))

time.sleep(0.1)

cv2.namedWindow("playback")

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image=np.array(frame.array[:,:,1])
    imagec=np.array(frame.array)
    ret,image=cv2.threshold(image,240,255,cv2.THRESH_BINARY)
    contours,hierarchy=cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imagec,contours,-1,(0,0,255),1)
    #print(len(contours))
    for c in contours:
        #M=cv2.moments(c)
        #print(M)
        #x=int(M['m10']/M['m00'])
        #y=int(M['m01']/M['m00'])
        (x,y),radius=cv2.minEnclosingCircle(c)
        x=int(x)
        y=int(y)
        cv2.circle(imagec,(x,y),2,(255,0,0),2)
        for l in range(len(lims)):
            m=(y-lims[l][0][1])/(max(x-lims[l][0][0],0.001))
            c=y-m*x
            
            if m-ms[l]<3 and c-cs[l]<5:
                print(l)
    #print(M)
    #print(len(contours))
    #image=cv2.medianBlur(image,5)
    #detector=cv2.SimpleBlobDetector()
    #keypoints=detector.detect(image)
    #circles=cv2.HoughCircles(image,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=300,param2=12,minRadius=5,maxRadius=80)
    #print(circles)
    circles=None
    if circles!=None:
        circles=np.uint16(np.around(circles))
    
        for c in circles[0,:]:
            cv2.circle(imagec,(c[0],c[1]),c[2],(0,0,255),3)
    #print(circles)
    #print(keypoints)
    #image=cv2.drawKeypoints(image,keypoints,np.array([]),255)
    cv2.imshow("playback",imagec)
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key==ord('q'):
        break
