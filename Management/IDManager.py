# -*- coding: utf-8 -*-

import sys;
import sqlite3; # database
from PyQt5.QtGui import *;  #QIcon,QFont
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class GUI(QWidget):
    def __init__(self):
        super().__init__();
    
        # document database connection
        self.connection=None; # connection
        self.c=None; # cursor
        
        # main function
        self.connectDatabase();
        self.initUI();
    
    # create / connect to database
    def connectDatabase(self):
        '''
        database: information.db
        table: VALIDTABLE
        member:
            USER:    CHAR(50) & PRIMARY KEY & NOT NULL
            ID:      CHAR(50) & NOT NULL
            START:   CHAR(50) & NOT NULL
            EXPIRE:  CHAR(50) & NOT NULL
        '''
        
        self.connection=sqlite3.connect("information.db");
        print("Open/Create database successfully.");
        self.c=self.connection.cursor();
    
    # add information to database
    def addToDb(self,user,ID,start,expire):
        if(self.connection and self.c):
            self.c.execute("INSERT INTO VALIDTABLE" \
                           "(USER,ID,START,EXPIRE)" \
                           "VALUES('{}','{}','{}','{}')".format(user,ID,start,expire)
                           );
            self.connection.commit();
            print("Insert successfully.");
        else:
            reply=QMessageBox.information(self,"Error","Database connection failure.",QMessageBox.Ok,QMessageBox.Ok);

    # delete information from database
    def deleteFrDb(self,user):
        if(self.connection and self.c):
            self.c.execute("DELETE FROM VALIDTABLE WHERE USER=?",(user,));
            self.connection.commit();
            print("Delete successfully.");
        else:
            reply=QMessageBox.information(self,"Error","Database connection failure.",QMessageBox.Ok,QMessageBox.Ok);
        
    # select by user
    def selectByUser(self,user):
        if(self.connection and self.c):
            cursor=self.c.execute("SELECT * FROM VALIDTABLE WHERE USER=?",(user,));
            for row in cursor:
                print("User=",row[0]);
                print("ID=",row[1]);
                print("Start date=",row[2]);
                print("Expire date=",row[3]);
            print("Select successfully.");
        else:
            reply=QMessageBox.information(self,"Error","Database connection failure.",QMessageBox.Ok,QMessageBox.Ok);
 
    # select all
    def selectAll(self):
        if(self.connection and self.c):
            cursor=self.c.execute('''
                           SELECT *
                           FROM VALIDTABLE
                           ''');
            for row in cursor:
               print("User=",row[0]);
               print("ID=",row[1]);
               print("Start date=",row[2]);
               print("Expire date=",row[3]);
            print("Select successfully.");
        else:
            reply=QMessageBox.information(self,"Error","Database connection failure.",QMessageBox.Ok,QMessageBox.Ok);
    
    # software hotkey
    def keyPressEvent(self,key_pressed):
        if(key_pressed.key()==Qt.Key_Escape):
            if(self.connection):
                self.connection.close();
            self.close();
    
    # close window
    def closeWindow(self):
        if(self.connection):
            self.connection.close();
        self.close();
    
    def initUI(self):
        # set window
        self.setFixedSize(QSize(640,480)); # width, height
        self.setWindowTitle("IPFS Demo");
        self.setWindowIcon(QIcon("Cephalometrics.ico"));
        
        # line edit
        userText=QLineEdit(self);
        userText.move(50,50); # position_x, position_y
        userText.resize(200,60); # width, height
        userText.setText("User name:");
        
        idText=QLineEdit(self);
        idText.move(50,160); # position_x, position_y
        idText.resize(200,60); # width, height
        idText.setText("ID:");
        
        startText=QLineEdit(self);
        startText.move(50,270); # position_x, position-y
        startText.resize(200,60); # width, height
        startText.setText("Start date:");
        
        expireText=QLineEdit(self);
        expireText.move(50,380); # position_x, position_y
        expireText.resize(200,60); # width, height
        expireText.setText("Expire date:");
        
        # add button
        addBtn=QPushButton(self);
        addBtn.setText("Add");
        addBtn.move(400,50); # position_x, position_y
        addBtn.resize(200,60); # width, height
        addBtn.clicked.connect(lambda:self.addToDb(userText.text(),idText.text(),startText.text(),expireText.text()));
        
        # delete button
        deleteBtn=QPushButton(self);
        deleteBtn.setText("Delete");
        deleteBtn.move(400,160); # position_x, position_y
        deleteBtn.resize(200,60); # width, height
        deleteBtn.clicked.connect(lambda:self.deleteFrDb(userText.text()));
        
        # select by user button
        selectBtn=QPushButton(self);
        selectBtn.setText("Select by user");
        selectBtn.move(400,270); # position_x, position_y
        selectBtn.resize(200,60); # width, height
        selectBtn.clicked.connect(lambda:self.selectByUser(userText.text()));
        
        # select all
        selectAllBtn=QPushButton(self);
        selectAllBtn.setText("Select all");
        selectAllBtn.move(400,380); # position_x, position_y
        selectAllBtn.resize(200,60); # width, height
        selectAllBtn.clicked.connect(self.selectAll);
        
        #show window
        self.show();
        
if(__name__=="__main__"):
    app=QApplication(sys.argv);  
    gui=GUI();
    sys.exit(app.exec_());