# -*- coding: utf-8 -*-

import sys;
import cv2;
import math;
import time;
import datetime;
from PyQt5.QtGui import *; 
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *; 

class GUI(QWidget):
    def __init__(self):
        super().__init__();
        self.allow_enter = False; # cannot launch without users's allowence
        self.distance = QLineEdit(self);
        self.angle = QLineEdit(self);
        self.initUI();
    
    # calculate the pixel distance of two points
    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
    
    # OpenCV of face-detection, eye-detection and distance measurement
    def distanceMeasure(self):
        # use measure_time to insert pause to the detection and measurement
        measure_time = -1;
        
        if(self.allow_enter):
            start_time = datetime.datetime.now();

            # caliberation
            d1 = 50; # unit: cetimeter
            p1 = 94.3461939826908; # unit: pixel distance (eye pixel distance)
#            p2 = 66.61948598650947; # unit: pixel distance (middle pixel distance)
            p2 = 77.37193274161869; # unit: pixel distance (middle pixel distance)
            product1 = d1*p1;
            product2 = d1*p2;
            
            # load cascade classifier
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
            eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml");
            mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml");
            cap=cv2.VideoCapture(0);
            
            # set webcam resolution
            # my webcam resolution: 720 * 540
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540);
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720);
            
            # get image and calculate
            while(True):
                # detect and calculate every 8 times
                measure_time += 1; # measure_time is the counter
                if(measure_time % 2 != 0):
                    time.sleep(0.056); # magic number： 7 * 0.008
                    continue;
                if(measure_time >= 2): measure_time = 0;
                
                # detect and calculate
                ret,img = cap.read();
                if(ret):
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5);
                    for (x,y,w,h) in faces:
                        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2);
                        roi_gray = gray[y:y+h, x:x+w];
                        roi_color = img[y:y+h, x:x+w];
                        
                        # detect eyes and mouth
                        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 9);
#                        mouth = mouth_cascade.detectMultiScale(roi_gray, 2, 5);
                        mouth = mouth_cascade.detectMultiScale(roi_gray, 2, 3);
                        eyes_detected = len(eyes) == 2;
                        mouth_detected = len(mouth) == 1;
                        
                        # frame eyes and mouth
                        if(eyes_detected):
                            for (ex, ey, ew, eh) in eyes:
                                cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2);
                        
                        if(mouth_detected):
                            for(mx, my, mw, mh) in mouth:
                                cv2.rectangle(roi_color, (mx,my), (mx+mw,my+mh), (0,255,0), 2);
                        
                        # calculation
                        if(eyes_detected and mouth_detected):
                            eye_distance = self.calculate_distance(eyes[0][0] + eyes[0][2]/2, eyes[0][1] + eyes[0][3]/2, eyes[1][0] + eyes[0][2]/2, eyes[1][1] + eyes[1][3]/2);
                            distance1 = product1/eye_distance;
                            if(20 <= distance1 <= 150): self.distance.setText("distance: %f cm" %(distance1));
                            middle1 = (eyes[0][0]+eyes[0][2]/2, eyes[0][1]+eyes[0][3]/2);
                            middle2 = (eyes[1][0]+eyes[1][2]/2, eyes[1][1]+eyes[1][3]/2);
                            middle = ((middle1[0]+middle2[0])/2, (middle1[1]+middle2[1])/2);
                            mouth_center = (mx+mw/2, my+mh/2);
                            distance2 = self.calculate_distance(mouth_center[0], middle[0], mouth_center[1], middle[1]);
                            ratio = distance2/(product2/distance1);
                            ratio = ratio if(0 <= ratio <= 1) else 1;
                            angle = math.degrees(math.acos(ratio));
                            self.angle.setText("angle: %f °" %(angle));
                        
                    # alert when exceeds 20 minutes   
                    test_time = datetime.datetime.now();
                    if((test_time - start_time).seconds >= 1200): # magic number: 20 minutes -> 1200 seconds
                        QMessageBox.information(self, "Alert", "Have a rest.", QMessageBox.Ok, QMessageBox.Ok);
                        start_time = datetime.datetime.now();
                        
                   
                    cv2.imshow("img", img);
                    key = cv2.waitKey(30)&0xff;
                    if(key == 27):break;
                    
            cap.release();
            cv2.destroyAllWindows();
        
        # allowence from user not received
        else:
            QMessageBox.information(self, "Error", "Allow to use webcam first.", QMessageBox.Ok, QMessageBox.Ok);
            return;
            
    # radio button controlled allowence
    def allow(self):
        self.allow_enter = not self.allow_enter;
    
    # main UI framework
    def initUI(self):
        #window
        self.setFixedSize(QSize(320,240));
        self.setWindowTitle("Distance Measurement Program");
        
        # enter button
        enterBtn = QPushButton(self);
        enterBtn.move(120,40);
        enterBtn.resize(80,40);
        enterBtn.setText("Enter");
        enterBtn.clicked.connect(self.distanceMeasure);
        
        # distance lineedit
        self.distance.setText("");
        self.distance.move(20,100);
        self.distance.resize(150,30);
        
        self.angle.setText("");
        self.angle.move(20,140);
        self.angle.resize(150,30);
        
        # allowence radiobutton
        radioBtn = QRadioButton(self);
        radioBtn.setText("Allow to use PC webcam.")
        radioBtn.move(20,180);
        radioBtn.resize(200,40);
        radioBtn.toggled.connect(self.allow);
        
        #show window
        self.show();

if(__name__ == "__main__"):
    app = QApplication(sys.argv);  
    gui = GUI();
    sys.exit(app.exec_());