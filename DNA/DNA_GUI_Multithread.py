# -*- coding: utf-8 -*-

import sys;
import pandas as pd;
from PyQt5.QtGui import *;  #QIcon,QFont
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class Match(QThread):
    def match(self,pAddr,cAddr,sheet):
        pair={}; # key: child name, value: parents name
        parent=pd.read_excel(pAddr,sheet_name="父母",header=[0],index_col=[0]);
        children=pd.read_excel(cAddr,sheet_name=sheet,header=[0],index_col=[0]);
        parent_name=[parent.columns[2*index][:-2] for index in range(len(parent.columns)//2)];
        children_name=[children.columns[2*index][:-2] for index in range(len(children.columns)//2)];
        
        for p_name in parent_name:
            parent[p_name+"-1"]=parent[p_name+"-1"].astype(str);
            parent[p_name]=parent[p_name+"-1"].str.cat(parent[p_name+"-2"].astype(str),sep=' ');
            parent.drop(columns=[p_name+"-1",p_name+"-2"],inplace=True);
            
        for c_name in children_name:
            children[c_name+"-1"]=children[c_name+"-1"].astype(str);
            children[c_name]=children[c_name+"-1"].str.cat(children[c_name+"-2"].astype(str),sep=' ');
            children[c_name+"-valid"]=children[c_name+"-1"].apply(lambda x:0 if(x=='x' or x=='X') else 1);
            for p_name in parent_name:
                children["temp1"]=children[c_name].str.cat(parent[p_name],sep=' ');
                children["temp2"]=children["temp1"].apply(lambda x:1 if("X X" in x or len(set(x.split(' ')[0:2]))+len(set(x.split(' ')[2:4]))!=len(set(x.split(' ')))) else 0);
                if(children["temp2"].sum()==40):
                    pair[sheet+' '+c_name]=p_name;
            children.drop(columns=[c_name+"-1",c_name+"-2","temp1","temp2",c_name+"-valid"],inplace=True);
        return pair;

class GUI(QWidget):
    def __init__(self):
        super().__init__();
        self.pAddr="";
        self.cAddr="";
        self.parentText=QLineEdit(self);
        self.childText=QLineEdit(self);
        self.initUI();
        
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
        
    def getParent(self):
        self.pAddr=QFileDialog.getOpenFileName(self,'Select file','./',"excel files(*.xlsx)")[0];
        if(self.pAddr):
            self.parentText.setText(self.pAddr);
    
    def getChild(self):
        self.cAddr=QFileDialog.getOpenFileName(self,'Select file','./',"excel files(*.xlsx)")[0];
        if(self.cAddr):
            self.childText.setText(self.cAddr);
    
    def match(self):
        if(self.cAddr and self.pAddr):
            thread1=Match(self);
            thread2=Match(self);
            thread3=Match(self);
            thread4=Match(self);
            pair1=thread1.match(self.pAddr,self.cAddr,"孩子1");
            pair2=thread2.match(self.pAddr,self.cAddr,"孩子2");
            pair3=thread3.match(self.pAddr,self.cAddr,"孩子3");
            pair4=thread4.match(self.pAddr,self.cAddr,"孩子4");
            
            thread1.wait();
            thread2.wait();
            thread3.wait();
            thread4.wait();
            
            thread1.finished.connect(thread1.deleteLater);
            thread2.finished.connect(thread2.deleteLater);
            thread3.finished.connect(thread2.deleteLater);
            thread4.finished.connect(thread2.deleteLater);
            pair=dict(pair1,**pair2,**pair3,**pair4);
            
            pair_df=pd.DataFrame(list(pair.items()),columns=["children","parents"]);
            writer=pd.ExcelWriter("Processed.xlsx");
            pair_df.to_excel(writer,"匹配结果");
            writer.save();
            reply=QMessageBox.information(self,"Success","Match success.",QMessageBox.Ok,QMessageBox.Ok);  
        else:
            reply=QMessageBox.information(self,"Error","Please select valid Excel files.",QMessageBox.Ok,QMessageBox.Ok);
        
    def initUI(self):
        # set window
        self.setFixedSize(QSize(640,480)); # width, height
        self.setWindowTitle("Matching program");
        
        # line edit
        self.parentText.move(40,40); 
        self.parentText.resize(400,80);
        self.parentText.setText("Select parent excel:");
        
        self.childText.move(40,200);
        self.childText.resize(400,80);
        self.childText.setText("Select children excel:");
        
        # button
        parentBtn=QPushButton(self);
        parentBtn.setText("...");
        parentBtn.move(500,40);
        parentBtn.resize(80,80);
        parentBtn.clicked.connect(self.getParent);
        
        childBtn=QPushButton(self);
        childBtn.setText("...");
        childBtn.move(500,200);
        childBtn.resize(80,80);
        childBtn.clicked.connect(self.getChild);
        
        matchBtn=QPushButton(self);
        matchBtn.setText("Match");
        matchBtn.move(200,360);
        matchBtn.resize(240,80);
        matchBtn.clicked.connect(self.match);
        
        # show window
        self.show();
        
if(__name__=="__main__"):
    app=QApplication(sys.argv);  
    gui=GUI();
    sys.exit(app.exec_());