# -*- coding: utf-8 -*-

import sys;
import cv2;
import numpy as np; #openCV for image processing
import time;
import pygame; #play audio
from PyQt5.QtGui import *;  #QIcon,QFont
from PyQt5.QtCore import *; #QCoreApplication,Qt
from PyQt5.QtWidgets import *; 
#QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

#openCV for beeping warning 
warning_threshold=10;

#welcome button
welcome_button_text="Input box";
welcome_button_width=100;
welcome_button_height=20;
welcome_button_position_x=10;
welcome_button_position_y=10;

#input information dialog
start_word="Starting time:";
input_information_caption="Information input";
input_information_text="Input present time";
input_information_width=1500;
input_information_height=200;

#line edit
line_edit_width=200;
line_edit_height=20;
line_edit_position_x=120;
line_edit_position_y=10;

#webcam error window
webcam_error_caption="Warning";
webcam_error_text="Wencam error";

#show image window
image_title="Face Detection";
image_path=".\\Data\\haarcascade_frontalface_default.xml";
#path="C:\\Users\\JiangHao\\Desktop\\python_Qt\\Data\\haarcascade_frontalface_default.xml";
            
#window 
width=640;
height=480;
position_x=300;
position_y=300; 
img=".\\Data\\capture.png";
title="Qt with openCV";

#form window 
form_width=640;
form_height=480;
form_position_x=300;
form_position_y=300; 
form_img=".\\Data\\capture.png";
form_title="Instruction";

#form window instruction
instruction_text="click 'start' button to start";
instruction_font_style="SansSerif";
instruction_font_size=20;
instruction_width=450;
instruction_height=150; 

#form window button
form_window_button_width=100;
form_window_button_height=70; 
form_window_button_text="Back";

#main window button
button_num=3;
button_width=200;
button_height=120; 
button_text=["Instruction","Start","Quit"];
buttons=[]; #QPushButton list

#main window radio button
radio_button_text="allow to use webcam";
radio_button_width=200;
radio_button_height=120;

#main window label
label_font_style="SansSerif";
label_font_size=20;
label_width=500;
label_height=100; 
label_text="Welcome to Qt openCV"; 

#main window message box
message_box_title="Warning";
message_box_text="Please click the radio button";

#quit message box
quit_message_box_title="Message";
quit_message_box_text="Are you sure to quit?";
    
class Form1(QWidget):
    def __init__(self):
        super().__init__();
        
    def center(self):
        #get window
        qr=self.frameGeometry();
        #get screen center
        cp=QDesktopWidget().availableGeometry().center();
        
        qr.moveCenter(cp);
        self.move(qr.topLeft()); 
            
    def keyPressEvent(self,key_pressed):
        if(key_pressed.key()==Qt.Key_Escape):
            self.close();
            
    def closeWindow(self):
        self.close();
        
    def initUI(self):
        self.setGeometry(form_position_x,form_position_y,form_width,form_height);
        self.setWindowTitle(form_title);
        self.setWindowIcon(QIcon(form_img));
        self.center();
        
        #label
        form_label=QLabel(self);
        form_label.setFont(QFont(instruction_font_style,instruction_font_size));
        form_label.setText(instruction_text);
        form_label.resize(instruction_width,instruction_height);
        form_label.move(form_width/2-instruction_width/2,form_height/3-instruction_height/2); 
        
        #button
        form_button=QPushButton(self);
        form_button.setText(form_window_button_text);
        form_button.resize(form_window_button_width,form_window_button_height);
        form_button.move(form_width/2-form_window_button_width/2,form_height*2/3-form_window_button_height/2);
        
        form_button.clicked.connect(self.close);
              
        self.show();
        
class GUI(QWidget):
    def __init__(self):
        super().__init__();
        #radio button controlled variable
        self.allow_enter=False;
        #line edit
        self.line_edit=QLineEdit(self);
        self.line_edit_text="Welcome ";
        
        #main function
        self.initUI();
        
    def inputInformation(self):
        information_dialog=QInputDialog(self);
        information_dialog.resize(input_information_width,input_information_height);
        text,ok=QInputDialog.getText(self,input_information_caption,input_information_text);
        
        if(ok):
            information_box_text=start_word+str(text);
            self.line_edit.setText(information_box_text);
            
    #pop out when webcam is not allowed
    def messageShow(self):
        reply=QMessageBox.information(self,message_box_title,message_box_text,
                QMessageBox.Ok,QMessageBox.Ok);
        
    def soundPlay(self):
        sound_path=".\\Data\\alarm.mp3";
        sleep_time=0.25; #senconds
        
        pygame.init();
        pygame.mixer.init();
        
        try:
            pygame.mixer.music.load(sound_path);
        except Exception as error:  
            print(error); 
            sys.exit(app.exec_());
            
        pygame.mixer.music.play();
        time.sleep(sleep_time);
        pygame.mixer.music.stop();
        
        pygame.quit();
        
    def webcamError(self):
        reply=QMessageBox.information(self,webcam_error_caption,webcam_error_text,
                QMessageBox.Ok,QMessageBox.Ok);
        
    def showImage(self):
        if(self.allow_enter):
            face_cascade=cv2.CascadeClassifier(image_path);
            cap=cv2.VideoCapture(0);

            while (True):
                ret,img=cap.read();
                if(ret):
                    canvas_area=img.size; #numpy return width*height
                
                    kernal_size=5;
                    img=cv2.medianBlur(img,kernal_size); #median filer
                
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
                    face=face_cascade.detectMultiScale(gray,1.3,5);
                    for (x,y,w,h) in face:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2);
                        roi_grey=gray[y:y+h,x:x+w];
                        roi_color=img[y:y+h,x:x+w];
                    
                        face_area=w*h;
                        percent=face_area*100/canvas_area;
                        if(percent>warning_threshold):
                            self.soundPlay();
                    
                    cv2.imshow(image_title,img);
                    k=cv2.waitKey(30)&0xff;
                    
                    if(k==27):
                        break;
                else:
                    webcamError(self); #webcam error pop window
                    cap.release();
                    cv2.destroyAllWindows();
                    sys.exit(app.exec_()); #webcam error, quit the whole program
                           
            cap.release();
            cv2.destroyAllWindows();
        else:
            self.messageShow();
            
    #radio button controlled allowence
    def allow(self):
        self.allow_enter=not self.allow_enter;
        
    def center(self):
        #get window
        qr=self.frameGeometry();
        #get screen center
        cp=QDesktopWidget().availableGeometry().center();
        
        qr.moveCenter(cp);
        self.move(qr.topLeft());
        
    def closeEvent(self,event):
        reply=QMessageBox.question(self,quit_message_box_title,quit_message_box_text,
                QMessageBox.Yes | QMessageBox.No,QMessageBox.No);
        
        if(reply==QMessageBox.Yes):
            event.accept();
        else:
            event.ignore();
    
    def keyPressEvent(self,key_pressed):
        if(key_pressed.key()==Qt.Key_Escape):
            self.close();
            
    def initUI(self):
        #window
        self.setGeometry(position_x,position_y,width,height);
        self.setWindowTitle(title);
        self.setWindowIcon(QIcon(img));
        self.center();
        
        #welcome button
        #input user name, and start time
        welcome_button=QPushButton(self);
        welcome_button.setText(welcome_button_text);
        welcome_button.resize(welcome_button_width,welcome_button_height);
        welcome_button.move(welcome_button_position_x,welcome_button_position_y);
        welcome_button.clicked.connect(self.inputInformation);
        
        #line editor
        self.line_edit.resize(line_edit_width,line_edit_height);
        self.line_edit.move(line_edit_position_x,line_edit_position_y);
        self.line_edit.setText(self.line_edit_text);
        
        #label
        label=QLabel(self);
        label.setFont(QFont(label_font_style,label_font_size));
        label.setText(label_text);
        label.resize(label_width,label_height);
        label.move(width/2-label_width/2,height/3-label_height/2); 
        
        #button
        for i in range(0,3): #go through 0~2
            button=QPushButton(self);
            buttons.append(button);
            buttons[i].setText(button_text[i]);
            buttons[i].resize(button_width,button_height);
            
        buttons[2].clicked.connect(QCoreApplication.instance().quit);
        
        
        #buttons layout
        hbox=QHBoxLayout();
        hbox.addStretch(1);
        
        for i in range(0,3):
            hbox.addWidget(buttons[i]);
            
        vbox=QVBoxLayout();
        vbox.addStretch(1);
        vbox.addLayout(hbox);
        
        self.setLayout(vbox); 
        
        #radio button
        radio_button=QRadioButton(self);
        radio_button.setText(radio_button_text);
        radio_button.resize(radio_button_width,radio_button_height);
        radio_button.move(0,height-radio_button_height);
        radio_button.toggled.connect(self.allow);
        
        #show window
        self.show();

if __name__=="__main__":
    app=QApplication(sys.argv);
    
    gui=GUI();
    myForm=Form1(); 
    
    if(len(buttons)==button_num):
        buttons[0].clicked.connect(myForm.initUI);
        buttons[1].clicked.connect(gui.showImage);
    else:
        sys.exit(app.exec_());

    sys.exit(app.exec_());