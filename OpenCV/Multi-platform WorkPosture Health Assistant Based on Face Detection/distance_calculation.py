# -*- coding: utf-8 -*-

import cv2;
import math;

def calculate_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2);

if(__name__=="__main__"):
    d1=50; # unit: cetimeter
    p1=94.3461939826908; # unit: pixel distance
    product=d1*p1;
    
    face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    eye_cascade=cv2.CascadeClassifier("haarcascade_eye.xml");
    mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml");
    cap=cv2.VideoCapture(0);
    while(True):
        ret,img=cap.read();
        if(ret):
            gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY);
            faces=face_cascade.detectMultiScale(gray,1.3,5);
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2);
                roi_gray=gray[y:y+h,x:x+w];
                roi_color=img[y:y+h,x:x+w];
                eyes=eye_cascade.detectMultiScale(roi_gray);
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2);
                if(len([i for i in eyes])==2):
                    eye_distance=calculate_distance(eyes[0][0]+eyes[0][2]/2,eyes[0][1]+eyes[0][3]/2,eyes[1][0]+eyes[0][2]/2,eyes[1][1]+eyes[1][3]/2);
                    print("%f cm" %(product/eye_distance));
            cv2.imshow("img",img);
            key=cv2.waitKey(30)&0xff;
            if(key==27):break;
    
    cap.release();
    cv2.destroyAllWindows();