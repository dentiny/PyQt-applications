# -*- coding: utf-8 -*-

import sqlite3;

# connect or create, if not, a database
connect=sqlite3.connect("test.db");
print("Open/create database successfully.");

c=connect.cursor();
c.execute( # SQL language # );
connect.commit();
connect.close();

# create table in the database
c.execute('''
        CREATE TABLE COMPANY
        (ID INT PRIMARY KEY NOT NULL,
        NAME TETX NOT NULL,
        AGE INT NOT NULL,
        ADDRESS CHAR(50),
        SALARY REAL);
        ''');
print("Create table successfully.");

# insert data
c.execute('''
          INSERT INTO COMPANY
          (ID,NAME,AGE,ADDRESS,SALARY)
          VALUES(1,"PAUL",32,"California",20000)
          ''');
c.execute('''
          INSERT INTO COMPANY
          (ID,NAME,AGE,ADDRESS,SALARY)
          VALUES(2,"ETHAN",22,"Shanghai",10000)
          ''');
c.execute('''
          INSERT INTO COMPANY
          (ID,NAME,AGE,ADDRESS,SALARY)
          VALUES({},"{}",{},"{}",{})
          '''.format(Id,name,age,address,company));
print("Insert successfully.");

# select data
cursor=c.execute('''
                SELECT ID,NAME,ADDRESS,SALARY
                FROM COMPANY                 
                 ''');
for row in cursor:
    print("ID=",row[0]);
    print("NAME=",row[1]);
    print("ADDRESS=",row[2]);
    print("SALARY=",row[3]);
print("Select successfully.");

# update data
c.execute('''
        UPDATE COMPANY
        SET SALARY=20000
        WHERE ID=2          
        ''');

# delete data
c.execute('''
          DELETE
          FROM COMPANY
          WHERE ID=1
          ''');

  # count
  c.execute('''
            SELECT COUNT(*)
            FROM COMPANY
            WHERE ID=1
            ''');
  result=c.fetchone()[0];
