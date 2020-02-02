# -*- coding: utf-8 -*-

import cv2;
import math;
import pickle;

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);

if(__name__=="__main__"):
    # list to store measured distance
    eye_distances = []; 
    middle_distances = [];
    
    # load cascade classifier
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml");
    mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml");

    # capture video stream from webcam
    cap = cv2.VideoCapture(0);
    while(True):
        ret,img = cap.read();
        if(ret):
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
            faces = face_cascade.detectMultiScale(gray, 1.3, 5);
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2);
                roi_gray = gray[y:y+h, x:x+w];
                roi_color = img[y:y+h, x:x+w];
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 9);
                mouth = mouth_cascade.detectMultiScale(roi_gray, 2, 5);
                
                eyes_detected = len(eyes) == 2;
                mouth_detected = len(mouth) == 1;
                
                # calculate the distance
                if(eyes_detected):
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2);
                    middle1 = (eyes[0][0]+eyes[0][2]/2, eyes[0][1]+eyes[0][3]/2);
                    middle2 = (eyes[1][0]+eyes[1][2]/2, eyes[1][1]+eyes[1][3]/2);
                    middle = ((middle1[0]+middle2[0])/2, (middle1[1]+middle2[1])/2);
                    
                if(mouth_detected):
                    for (mx, my, mw, mh) in mouth:
                        cv2.rectangle(roi_color, (mx,my), (mx+mw,my+mh),(0,255,0),2);
                    mouth_center = (mx+mw/2, my+mh/2);
                
                if(mouth_detected and eyes_detected):
                    eye_distance = calculate_distance(eyes[0][0] + eyes[0][2]/2, eyes[0][1] + eyes[0][3]/2, eyes[1][0] + eyes[0][2]/2, eyes[1][1] + eyes[1][3]/2);
                    middle_distance = calculate_distance(mouth_center[0], middle[0], mouth_center[1], middle[1]);
                    eye_distances.append(eye_distance);
                    middle_distances.append(middle_distance);

                    # save data
                    if(len(eye_distances) == 1000):
                        with open("distance.pkl", 'wb') as f:
                            pickle.dump(eye_distances, f);
                    if(len(middle_distances) == 500):
                        with open("mouth_distance.pkl", 'wb') as f:
                            pickle.dump(middle_distances, f);
                    
            cv2.imshow("img",img);
            key = cv2.waitKey(30) & 0xff;
            if(key == 27): break;
    
    cap.release();
    cv2.destroyAllWindows();