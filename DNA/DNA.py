# -*- coding: utf-8 -*-

import pandas as pd;
pair={}; # key: child name, value: parents name
parent=pd.read_excel("DNA_copy.xlsx",sheet_name="父母",header=[0],index_col=[0]);
children=pd.read_excel("DNA_copy.xlsx",sheet_name="孩子",header=[0],index_col=[0]);
parent_name=[parent.columns[2*index][:-2] for index in range(len(parent.columns)//2)];
children_name=[children.columns[2*index][:-2] for index in range(len(children.columns)//2)];

for p_name in parent_name:
    parent[p_name+"-1"]=parent[p_name+"-1"].astype(str);
    parent[p_name]=parent[p_name+"-1"].str.cat(parent[p_name+"-2"].astype(str),sep=' ');
    parent.drop(columns=[p_name+"-1",p_name+"-2"],inplace=True);

for c_name in children_name:
    children[c_name+"-1"]=children[c_name+"-1"].astype(str);
    children[c_name]=children[c_name+"-1"].str.cat(children[c_name+"-2"].astype(str),sep=' ');
    for p_name in parent_name:
        children["temp1"]=children[c_name].str.cat(parent[p_name],sep=' ');
        children["temp2"]=children["temp1"].apply(lambda x:1 if(len(set(x.split(' ')[0:2]))+len(set(x.split(' ')[2:4]))!=len(set(x.split(' ')))) else 0);
        if(children["temp2"].sum()==40):
            pair[c_name]=p_name;
    children.drop(columns=[c_name+"-1",c_name+"-2"],inplace=True);
children.drop(columns=["temp1","temp2"],inplace=True); 
    
pair_df=pd.DataFrame(list(pair.items()),columns=["parents","children"]);
writer=pd.ExcelWriter("Processed.xlsx");
parent.to_excel(writer,"父母");
children.to_excel(writer,"孩子");
pair_df.to_excel(writer,"匹配结果");
writer.save();