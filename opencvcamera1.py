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

lims=[]

camera=PiCamera()
camera.resolution=(w,h)
camera.framerate=fps
rawCapture=PiRGBArray(camera,size=(w,h))

time.sleep(0.1)

points=[]

def mouseCallback(event,x,y,flags,param):
    global points
    if event==cv2.EVENT_LBUTTONDOWN:
        print([x,y])
        if(len(points)==0):
            points.append((x,y))
        else:
            points.append((x,y))
            lims.append(points)
            points=[]
        #lims.append((x,y))
        print(lims)

cv2.namedWindow("calib")
cv2.setMouseCallback("calib",mouseCallback)

roi=[]

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image=np.array(frame.array)
    #ret,image=cv2.threshold(image,240,255,cv2.THRESH_BINARY)
    if(len(lims)>0):
        #if(len(lims)%2==0):
        for i in range(len(lims)):
            cv2.line(image,lims[i][0],lims[i][1],255)        #    for i in range(len(lims)/2-1):
        #        cv2.line(image,lims[2*i],lims[2*i+1],(0,255,0),thickness=1)
        
    cv2.imshow("calib",image)
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key==ord('s'):
        print('saving')
        with open('/home/pi/calib.txt','wb') as fp:
            pickle.dump(lims,fp)
        #for i in range(len(lims)):
            #img=np.zeros([h,w,1],dtype='uint8')
            #pix=[]
            #cv2.line(img,lims[i][0],lims[i][1],255)
            #cv2.imshow('img',img)
            #for i in range(h):
            #    for j in range(w):
            #        if(img[i][j])!=0:
            #           pix.append((j,i))
                       
            
        #    roi.append(pix)
        #print(roi)
                
            
    if key==ord('q'):
        break
