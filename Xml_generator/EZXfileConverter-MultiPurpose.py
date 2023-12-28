# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:09:21 2023

@author: home
"""


# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 10:07:10 2023

@author: home
"""
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter import *
from tkinter import ttk
import customtkinter
#import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import operator
from datetime import date
import time
import os
import re
import math

"""Function to create sub element in xml file"""

def sub_element_one(member,jobname,prompt,element):
    child1 = ET.Element(member)
    child1.text = jobname+','+prompt
    return element.append(child1)

"""Function to create attachment element in xml file"""

def attachments(jobname,prompt,length,element):
    child = ET.Element('ATTACHMENT')
    sublength = ET.SubElement(child, "MEMBER_ID")
    sublength.text = jobname+','+prompt
    subchild1 = ET.SubElement(child, 'DISTANCE')
    subchild1.text = length
    subchild1.attrib = {'UNIT': 'IMPERIAL'}
    return element.append(child)

"""Function to create new element in xml file"""

def new_memberdata(jobname,prompt,element,Type,Name,doNotCut,length,height='0',width='0',acheight='0',acwidth='0'):
    child2 = ET.Element("MEMBER_DATA")
    memid = ET.SubElement(child2, "MEMBER_ID")
    memid.text = jobname+','+prompt
    memtype = ET.SubElement(child2, "TYPE")
    memtype.text = Type
    memname = ET.SubElement(child2, "NAME")
    memname.text = Name
    memdesc = ET.SubElement(child2, "DESCRIPTION")
    memdesc.text = doNotCut
    memheight = ET.SubElement(child2, "HEIGHT")
    memheight.text = height
    memheight.attrib = {'UNIT': 'IMPERIAL'}
    memweight = ET.SubElement(child2, "WIDTH")
    memweight.text = width
    memweight.attrib = {'UNIT': 'IMPERIAL'}
    memaheight = ET.SubElement(child2, "ACTUAL_HEIGHT")
    memaheight.text = acheight
    memaheight.attrib = {'UNIT': 'IMPERIAL'}
    memaweight = ET.SubElement(child2, "ACTUAL_WIDTH")
    memaweight.text = acwidth
    memaweight.attrib = {'UNIT': 'IMPERIAL'}
    memlength = ET.SubElement(child2, "LENGTH")
    memlength.text = length
    memlength.attrib = {'UNIT': 'IMPERIAL'}
    memstartcut = ET.SubElement(
        child2, "START_CUT_ANG")
    memstartcut.text = '0.0'
    memendcut = ET.SubElement(
        child2, "END_CUT_ELEV_ANG")
    memendcut.text = '0.0'
    memrankwall = ET.SubElement(
        child2, "IS_RAKED_WALL")
    memrankwall.text = 'N'
    memsideattach = ET.SubElement(
        child2, "SIDE_1_NUM_ATTACH")
    memsideattach.text = '0'
    memsidenumattach = ET.SubElement(
        child2, "SIDE_1_ATTACH")
    memsidenumattach.text = '0'
    element.append(child2)

"""Clcean the string (remove []',)"""

def clean_string(string):
   string1 = string.lstrip('[').rstrip(']').replace("'", "").replace(",", "")
   return string1

""""replace string"""

def stringReplace(mainSting,old,new):
   replacedString =  str(mainSting).replace(old,new)
   return replacedString

"""UI parts"""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.name : str
        self.description : str
        
        self.title("Genie ESTI Frame Formboard Manifest Multipurpose")
        self.geometry(f"{1100}x{600}") 

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.pack(side=LEFT,fill=BOTH)
        
        self.error_bar = customtkinter.CTkFrame(self,corner_radius=0)
        self.error_bar.pack(fill=Y,side=RIGHT,ipadx=100 )
        self.error_bar_title = customtkinter.CTkLabel(self.error_bar, text="Error Bar", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.error_bar_title.pack(side=TOP,padx=5,pady=5)
        
        self.error_bar_content = customtkinter.CTkLabel(self.error_bar, bg_color='white', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.error_bar_content.pack(pady=5 , fill= BOTH,expand =True,padx=5)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Genie ESTI \n Frame Formboard \n Manifest Multi", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side=TOP,padx=5,pady=10)
        
        
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(side=BOTTOM , padx=5, pady=20)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
        self.appearance_mode_label.pack(side=BOTTOM, padx=1, pady=10)
        
        self.entry1_changename = customtkinter.CTkEntry(self, placeholder_text="Rename",width=600)
        self.entry1_changename.place(x=240,y=50,relwidth=0.5,relheight=0.06)
        
        self.entry1_jobname = customtkinter.CTkEntry(self, placeholder_text="Jobname",width=600)
        self.entry1_jobname.place(x=240,y=100,relwidth=0.5,relheight=0.06)
        
        self.entry1_outputFileName = customtkinter.CTkEntry(self, placeholder_text="Outputfile name ",width=600)
        self.entry1_outputFileName.place(x=240,y=150,relwidth=0.5,relheight=0.06)
                
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Folder path",width=600)
        self.entry.place(x=240,y=200,relwidth=0.5,relheight=0.06)
        
        self.ab = customtkinter.CTkOptionMenu(self,values=["Do not cut","cut"])
        self.ab.place(x=460,y=250,relwidth=0.15,relheight=0.06)
        
        
        
        self.button = customtkinter.CTkButton(self,text='SELECT FOLDER',width=100,command=self.openfile)
        self.button.place(x=240,y=250,relwidth=0.15,relheight=0.06)
        
        self.button_create = customtkinter.CTkButton(self,text='CREATE',width=200,command=self.formboard,border_color='black',border_width=1,font=customtkinter.CTkFont(size=13, weight="bold"))
        self.button_create.place(x=240,y=380,relwidth=0.3,relheight=0.07)
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Rename XML", command=self.rename_file)
        self.sidebar_button_1.pack(side=TOP , padx=20, pady=30)
        
        self.desc = customtkinter.CTkEntry(self, placeholder_text="Description",width=60)
        self.desc.place(x=240,y=320,relwidth=0.5,relheight=0.05)
        
# =============================================================================
#     def cut_or_dontcut(self, val : str):
#         if val == 'cut':
#             self.desc = customtkinter.CTkEntry(self, placeholder_text="Description",width=60)
#             self.desc.place(x=240,y=300,relwidth=0.5,relheight=0.05)
#         else:
#             try:
#                 self.desc.after(1000, lambda:  self.desc.destroy() )
#             except:
#                 pass
# =============================================================================
            
        
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def openfile(self):
        self.entry.delete(0,'end')
        filepath = askdirectory( initialdir="/",
                                title='Please select a folder')
        self.entry.insert(0,filepath)
        
    def openfile1(self):
        self.entry1.delete(0,'end')
        filepath1 = askopenfilename( initialdir="/",
                                title='Please select a excel file')
        self.entry1.insert(0,filepath1)      
        
    def rename_file(self):
        if self.entry.get() == '':
            self.warning_label1 = customtkinter.CTkLabel(self.sidebar_frame,text_color='red', text='Please select a folder')
            self.warning_label1.pack()
            self.warning_label1.after(3000, lambda:  self.warning_label1.destroy() )
        else:
            listOf_files = os.listdir(self.entry.get())    
            for i in listOf_files:
                new_name = i.split(" ")
                find_num = re.findall('[0-9]+', new_name[-1])
                
                if len(str(find_num)) ==5:
                    replace = re.sub('[0-9]+','0'+str(clean_string(str(find_num))),i)
                    print(replace)
                    print(i)
                    os.rename(self.entry.get()+'\\'+i,self.entry.get()+'\\'+replace)
                    self.warning_label = customtkinter.CTkLabel(self.sidebar_frame,text_color='green', text='Floders name changed')
                    self.warning_label.pack()
                    self.warning_label.after(3000, lambda:  self.warning_label.destroy() )
                else:
                    self.warning_label = customtkinter.CTkLabel(self.sidebar_frame,text_color='red', text='Alredy in the format')
                    self.warning_label.pack()
                    self.warning_label.after(3000, lambda:  self.warning_label.destroy() )
                    break


    
    
#"""Xml generation starts from here"""

    def formboard(self):
        if self.entry.get() == "":
            self.folder_warning_label = customtkinter.CTkLabel(self,text_color='red', text='Please select a Folder.')
            self.folder_warning_label.place(x=240,y=290)
            self.folder_warning_label.after(3000, lambda:  self.folder_warning_label.destroy() )    
        else:
            
            if self.entry1_changename.get() == "":
                job = "FWB"
            else:
                job = self.entry1_changename.get()
                
            if self.entry1_outputFileName.get() == "":
                outputFileName = "WH BASS CFAASC TURNIPSEED FBW"
            else:
                outputFileName = self.entry1_outputFileName.get()
            
            output = askdirectory( initialdir="/",
                                    title='Please select a folder to save the xml files')
            
            list_file = os.listdir(self.entry.get())
            for filename in list_file:
                split = filename.split()
                lastword = split[-1]
                
                num = re.findall('[0-9]+', lastword)
                
               # print(num[0])
                
                jobname1 = job+str(num[0])
                print(jobname1)
                tree = ET.parse(self.entry.get()+'//'+filename)
                root =  tree.getroot()
                
                items = []
                
                
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        itemsName = (ezxPart.find('PartTypeName').text)
                        items.append(itemsName)
                
                my_dict = {i:items.count(i) for i in items}
                print(my_dict)
                listTp =[]
                
                
                #print(my_dict)
                bp_dict = {} 
                count = 0
                bpTopHeight = []
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        if ezxPart.find('PartTypeName').text == "SFBottomPlate":
                            count = count +1
                            bpHeight =  ezxPart.find('MaterialName').text
                               
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listBp = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    if ezxPoint2d.find('X').text== '-0':
                                        x=0
                                    listBp.append([x,y])
                
                            listBp.sort(key=operator.itemgetter((1)))
                            #print(listBp)
                            
                            
                            for i in range(0,len(listBp),4):
                
                                #print(i,"i")
                                x = (listBp[i][0])
                                y = (listBp[i][1])
                                x1 = (listBp[i+1][0])
                                y1 = (listBp[i+1][1])
                                x2 = listBp[i+2][0]
                                y2 = listBp[i+2][1]
                                x3 = listBp[i+3][0]
                                y3 = listBp[i+3][1]
# =============================================================================
#                                 plt.plot([x, x1],[y,y1],color='red')
#                                 plt.plot([x2,x3], [y2,y3],color='red') 
# =============================================================================
                                bpTopHeight.extend([x,x1,x2,x3])
                                bpLength = round(max(x,x1)-min(x,x1),2)
                                bpWidth = round(abs(y2-y1),2)
                                bpheight = int(bpHeight[2:4])
                                if bpheight == 8:
                                    bpActualheight = 7.25
                                elif bpheight == 10:
                                    bpActualheight = 9.25
                                else:
                                    bpActualheight = round(float(bpheight) - 0.5,2)
                                #print(bpHeight)
                                bp_dict[(count)] = list([bpLength,bpWidth,bpheight,bpActualheight])
                            
                headerTp_dict = {} 
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        if ezxPart.find('PartTypeName').text == "SFTopHeaderSill":
                            count = count +1
                            headerTpHeight =  ezxPart.find('MaterialName').text
                               
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listheaderTp = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    if ezxPoint2d.find('X').text== '-0':
                                        x=0
                                    listheaderTp.append([x,y])
                
                            listheaderTp.sort(key=operator.itemgetter((1)))
                            #print(listBp)
                            
                            
                            for i in range(0,len(listheaderTp),4):
                
                                #print(i,"i")
                                x = (listheaderTp[i][0])
                                y = (listheaderTp[i][1])
                                x1 = (listheaderTp[i+1][0])
                                y1 = (listheaderTp[i+1][1])
                                x2 = listheaderTp[i+2][0]
                                y2 = listheaderTp[i+2][1]
                                x3 = listheaderTp[i+3][0]
                                y3 = listheaderTp[i+3][1]
# =============================================================================
#                                 plt.plot([x, x1],[y,y1],color='red')
#                                 plt.plot([x2,x3], [y2,y3],color='red') 
# =============================================================================
                                headerTpLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                headerTpWidth = round(abs(y2-y1),2)
                                headerTpheight = int(headerTpHeight[2])
                                if headerTpheight == 8:
                                    headerTpActualheight = 7.25
                                else:
                                    headerTpActualheight = round(float(headerTpheight) - 0.5,2)
                                #print(bpHeight)
                                headerTp_dict[(count)] = list([headerTpLength,headerTpWidth,headerTpheight,headerTpActualheight,min(x,x1,x2,x3),max(x,x1,x2,x3)]) 
                print(headerTp_dict,"header top plate")                
                headerBp_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        if ezxPart.find('PartTypeName').text == "SFBottomHeaderSill":
                            count = count +1
                            headerBpHeight =  ezxPart.find('MaterialName').text
                               
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listheaderBp = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    if ezxPoint2d.find('X').text== '-0':
                                        x=0
                                    listheaderBp.append([x,y])
                
                            listheaderBp.sort(key=operator.itemgetter((1)))
                            #print(listBp)
                            
                            
                            for i in range(0,len(listheaderBp),4):
                
                                #print(i,"i")
                                x = (listheaderBp[i][0])
                                y = (listheaderBp[i][1])
                                x1 = (listheaderBp[i+1][0])
                                y1 = (listheaderBp[i+1][1])
                                x2 = listheaderBp[i+2][0]
                                y2 = listheaderBp[i+2][1]
                                x3 = listheaderBp[i+3][0]
                                y3 = listheaderBp[i+3][1]
# =============================================================================
#                                 plt.plot([x, x1],[y,y1],color='red')
#                                 plt.plot([x2,x3], [y2,y3],color='red') 
# =============================================================================
                                headerBpLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                headerBpWidth = round(abs(y2-y1),2)
                                headerBpheight = int(headerBpHeight[2])
                                if headerBpheight == 8:
                                    headerBpActualheight = 7.25
                                else:
                                    headerBpActualheight = round(float(headerBpheight) - 0.5,2)
                                #print(bpHeight)
                                headerBp_dict[(count)] = list([headerBpLength,headerBpWidth,headerBpheight,headerBpActualheight,min(x,x1,x2,x3),max(x,x1,x2,x3)])
                print(headerBp_dict,"header BP plate")
                headerTopplate_dict = headerTp_dict
                #print(bp_dict)
                headerLength =0
                header_dict = {}   
                count = 0    
                flag1 = 0
                headMin = []
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):            
                        
                        if ezxPart.find('PartTypeName').text == "Header" or ezxPart.find('PartTypeName').text == "SFTransom":
                            count +=1
                            flag1 =1
                            Headerheight =  ezxPart.find('MaterialName').text
                            if Headerheight == None:
                                Headerheight = '6x8'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listHeader = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listHeader.append([x,y])
                            listHeader.sort(key=operator.itemgetter((1)))   
                            for i in range(0,len(listHeader),4):
                                try:
                                
                                    #print(sum(listTp[i]))
                                    x = (listHeader[i][0])
                                    y = (listHeader[i][1])
                                    x1 = (listHeader[i+1][0])
                                    y1 = (listHeader[i+1][1])
                                    x2 = listHeader[i+2][0]
                                    y2 = listHeader[i+2][1]
                                    x3 = listHeader[i+3][0]
                                    y3 = listHeader[i+3][1]
                # =============================================================================
                #                                     plt.plot([x, x1],[y,y1],color = 'orange')
                #                                     plt.plot([x2,x3], [y2,y3],color = 'orange')
                # =============================================================================
                                    headMin.append(min(x,x1,x2,x3))

                                    headerHeight = int(Headerheight[2])
                                    headerLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                    print(headerLength)
                                    headerWidth = int(Headerheight[0])
                                    header_dict[count] = list([headerLength,headerWidth,headerHeight,min(x,x1,x2,x3),max(x,x1,x2,x3)])
                                except:
                                    pass
                                    print("pass executed")
                
                #print(header_dict)
                vtp_dict = {} 
                count = 0
                flag = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        if ezxPart.find('PartTypeName').text == "SFVeryTopPlate":
                            count = count +1
                            flag = 1
                            vtpHeight =  ezxPart.find('MaterialName').text
                               
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listVtp = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    if ezxPoint2d.find('X').text== '-0':
                                        x=0
                                    listVtp.append([x,y])
                
                            listVtp.sort(key=operator.itemgetter((1)))
                            #print(listBp)
                            
                            
                            for i in range(0,len(listVtp),4):
                
                                #print(i,"i")
                                x = (listVtp[i][0])
                                y = (listVtp[i][1])
                                x1 = (listVtp[i+1][0])
                                y1 = (listVtp[i+1][1])
                                x2 = listVtp[i+2][0]
                                y2 = listVtp[i+2][1]
                                x3 = listVtp[i+3][0]
                                y3 = listVtp[i+3][1]
# =============================================================================
#                                 plt.plot([x, x1],[y,y1],color='red')
#                                 plt.plot([x2,x3], [y2,y3],color='red') 
# =============================================================================
                                
                                vtpLength = round(max(x,x1,x2,x3)- min(x,x1,x2,x3),2)
                                vtpWidth = round(abs(y2-y1),2)
                                vtpheight = int(vtpHeight[2:4])
                                if vtpheight == 8:
                                    vtpActualheight = 7.25
                                elif vtpheight == 10:
                                    vtpActualheight = 9.25
                                else:
                                    vtpActualheight = round(float(vtpheight) - 0.5,2)
                                #print(bpHeight)
                                vtp_dict[(count)] = list([vtpLength,vtpWidth,vtpheight,vtpActualheight])
                                print('execute first block')
                                #print(vtp_dict)
                                
                try : 
                    if  my_dict['SFTopPlate'] ==1  :
                        tp_dict = {} 
                        count = 0
                        
                        for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                            for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                                if ezxPart.find('PartTypeName').text == "SFTopPlate" :
                                    count = count +1
                                    flag = 1
                                    tpHeight =  ezxPart.find('MaterialName').text
                                       
                                    for elevationPoints in ezxPart.findall('ElevationPoints'):
                                        listTp = []
                                        for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                            x = float(ezxPoint2d.find('X').text)
                                            y = float(ezxPoint2d.find('Y').text)
                                            if ezxPoint2d.find('X').text== '-0':
                                                x=0
                                            listTp.append([x,y])
                        
                                    listTp.sort(key=operator.itemgetter((1)))
                                    #print(listBp)
                                    
                                    
                                    for i in range(0,len(listTp),4):
                        
                                        #print(i,"i")
                                        x = (listTp[i][0])
                                        y = (listTp[i][1])
                                        x1 = (listTp[i+1][0])
                                        y1 = (listTp[i+1][1])
                                        x2 = listTp[i+2][0]
                                        y2 = listTp[i+2][1]
                                        x3 = listTp[i+3][0]
                                        y3 = listTp[i+3][1]
        # =============================================================================
        #                                 plt.plot([x, x1],[y,y1],color='red')
        #                                 plt.plot([x2,x3], [y2,y3],color='red') 
        # =============================================================================
                                        
                                        tpLength = round(max(x,x1),2)
                                        tpWidth = round(abs(y2-y1),2)
                                        tpheight = int(tpHeight[2:4])
                                        if tpheight == 8:
                                            tpActualheight = 7.25
                                        elif tpheight == 10:
                                            tpActualheight = 9.25
                                        else:
                                            tpActualheight = round(float(tpheight) - 0.5,2)
                                        #print(bpHeight)
                                        tp_dict[(count)] = list([tpLength,tpWidth,tpheight,tpActualheight])
                except:
                    if  my_dict['TopPlate'] ==1  :
                        tp_dict = {} 
                        count = 0
                        
                        for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                            for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                                if ezxPart.find('PartTypeName').text == "TopPlate" :
                                    count = count +1
                                    flag = 1
                                    tpHeight =  ezxPart.find('MaterialName').text
                                       
                                    for elevationPoints in ezxPart.findall('ElevationPoints'):
                                        listTp = []
                                        for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                            x = float(ezxPoint2d.find('X').text)
                                            y = float(ezxPoint2d.find('Y').text)
                                            if ezxPoint2d.find('X').text== '-0':
                                                x=0
                                            listTp.append([x,y])
                        
                                    listTp.sort(key=operator.itemgetter((1)))
                                    #print(listBp)
                                    
                                    
                                    for i in range(0,len(listTp),4):
                        
                                        #print(i,"i")
                                        x = (listTp[i][0])
                                        y = (listTp[i][1])
                                        x1 = (listTp[i+1][0])
                                        y1 = (listTp[i+1][1])
                                        x2 = listTp[i+2][0]
                                        y2 = listTp[i+2][1]
                                        x3 = listTp[i+3][0]
                                        y3 = listTp[i+3][1]
        # =============================================================================
        #                                 plt.plot([x, x1],[y,y1],color='red')
        #                                 plt.plot([x2,x3], [y2,y3],color='red') 
        # =============================================================================
                                        
                                        tpLength = round(max(x,x1),2)
                                        tpWidth = round(abs(y2-y1),2)
                                        tpheight = int(tpHeight[2])
                                        if tpheight == 8:
                                            tpActualheight = 7.25
                                        else:
                                            tpActualheight = round(float(tpheight) - 0.5,2)
                                        #print(bpHeight)
                                        tp_dict[(count)] = list([tpLength,tpWidth,tpheight,tpActualheight])
# =============================================================================
#                 if flag == 0:
#                       tp_dict = {} 
#                       count = 0
#                       
#                       for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
#                           for ezxPart in arrayOfEzxPart.findall('EzxPart'):
#                               if ezxPart.find('PartTypeName').text == "SFTopPlate":
#                                   count = count +1
#                                   flag = 1
#                                   tpHeight =  ezxPart.find('MaterialName').text
#                                      
#                                   for elevationPoints in ezxPart.findall('ElevationPoints'):
#                                       listTp = []
#                                       for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
#                                           x = float(ezxPoint2d.find('X').text)
#                                           y = float(ezxPoint2d.find('Y').text)
#                                           if ezxPoint2d.find('X').text== '-0':
#                                               x=0
#                                           listTp.append([x,y])
#                       
#                                   listTp.sort(key=operator.itemgetter((1)))
#                                   #print(listBp)
#                                   
#                                   
#                                   for i in range(0,len(listTp),4):
#                       
#                                       #print(i,"i")
#                                       x = (listTp[i][0])
#                                       y = (listTp[i][1])
#                                       x1 = (listTp[i+1][0])
#                                       y1 = (listTp[i+1][1])
#                                       x2 = listTp[i+2][0]
#                                       y2 = listTp[i+2][1]
#                                       x3 = listTp[i+3][0]
#                                       y3 = listTp[i+3][1]
#       # =============================================================================
#       #                                 plt.plot([x, x1],[y,y1],color='red')
#       #                                 plt.plot([x2,x3], [y2,y3],color='red') 
#       # =============================================================================
#                                       
#                                       tpLength = round(max(x,x1),2)
#                                       tpWidth = round(abs(y2-y1),2)
#                                       tpheight = int(tpHeight[2])
#                                       if tpheight == 8:
#                                           tpActualheight = 7.25
#                                       else:
#                                           tpActualheight = round(float(tpheight) - 0.5,2)
#                                       #print(bpHeight)
#                                       tp_dict[(count)] = list([tpLength,tpWidth,tpheight,tpActualheight])
# =============================================================================
                    #print(tp_dict,flag,"jjjjjjjjjj")
# =============================================================================
#                 print(headerTp_dict,'kjhjjhhj')
#                 #headerTp_dict = {}
#                 headerBp_dict = {}
#                 headerTopplate_dict ={}
#                 if flag ==0 and flag1 ==1:
#                     count=0
#                     newList = []
#                     newDict = {}
#                     for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
#                         for ezxPart in arrayOfEzxPart.findall('EzxPart'):
#                             listX = []
#                             listY = []
#                             
#                             if ezxPart.find('PartTypeName').text == "SFTopPlate":
#                                 count = count +1
#                                 tpHeight =  ezxPart.find('MaterialName').text
#                                    
#                                 for elevationPoints in ezxPart.findall('ElevationPoints'):
#                                     listBp = []
#                                     for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
#                                         x = float(ezxPoint2d.find('X').text)
#                                         y = float(ezxPoint2d.find('Y').text)
#                                         listX.append(x)
#                                         listY.append(y)
#                                         if ezxPoint2d.find('X').text== '-0':
#                                             x=0
#                                         listBp.append([x,y])
#                                 listX.sort()
#                                 listY.sort()
#                                 
#                                 newDict[(listY[2]-(listY[2]-listY[0]))] = [listX[0],listY[0],listX[2],listY[1],listX[1],listY[2],listX[3],listY[2]]
#                     # =============================================================================
#                     #             plt.plot([listX[0],listX[2]],[listY[0],listY[1]])
#                     #             plt.plot([listX[1],listX[3]],[listY[2],listY[2]])
#                     # =============================================================================
#     
#                     like = dict(sorted(newDict.items()))
#     
#                     headerTopplate_dict = {}
#                     tp_dict = {}
#                     i =1
#                     j=1
#                     flag =0
#                     vtp_dict ={}
#                     vtp = max(newDict.keys())
#     
#                     for key,value in like.items():
#                         length =round( value[2] - value[0],2)
#                         width = value[5] - value[1]
#                         height = tpHeight[2]
#                         
#                         if height == 8:
#                             Actualheight = 7.25
#                         else:
#                             Actualheight = round(float(height) - 0.5,2)
#                         
#                         #print(length)
#                         #print(headerLength)
#     
#                         if length == headerLength:
#                             headerTopplate_dict[i] = list([length,width,height],Actualheight)
#                             i+=1
#                             flag+=1
#                         elif vtp == key:
#                             vtp_dict[1] = list([length,width,height,Actualheight])
#                         else:
#                             tp_dict[j] = list([length,width,height,Actualheight])
#                             j+=1
#                             
# # =============================================================================
# #                     print('execute second block')
# # 
# #                     print(headerTopplate_dict)
# #                     print(tp_dict)
# #                     print(vtp_dict)
# # =============================================================================
# 
#                     headerTp_dict = dict(list(headerTopplate_dict.items())[len(headerTopplate_dict)//2:])
#                     headerBp_dict = dict(list(headerTopplate_dict.items())[:len(headerTopplate_dict)//2])
# =============================================================================
                
                try:
                    if my_dict['SFTopPlate'] == 2  :
                        Tp_dict = {} 
                        count = 0
                        differenciate_list = []
                        for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                            for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                                if ezxPart.find('PartTypeName').text == "SFTopPlate" :
                                    count = count +1
                                    tpHeight =  ezxPart.find('MaterialName').text
                                    #print(tpHeight)   
                                    for elevationPoints in ezxPart.findall('ElevationPoints'):
                                        listTp = []
                                        for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                            x = float(ezxPoint2d.find('X').text)
                                            y = float(ezxPoint2d.find('Y').text)
                                            if ezxPoint2d.find('X').text== '-0':
                                                x=0
                                            listTp.append([x,y])
    
                                    listTp.sort(key=operator.itemgetter((1)))
                                    #print(listTp)
                                    
                                    
                                    for i in range(0,len(listTp),4):
    
                                        #print(i,"i")
                                        x = (listTp[i][0])
                                        y = (listTp[i][1])
                                        x1 = (listTp[i+1][0])
                                        y1 = (listTp[i+1][1])
                                        x2 = listTp[i+2][0]
                                        y2 = listTp[i+2][1]
                                        x3 = listTp[i+3][0]
                                        y3 = listTp[i+3][1]
                        # =============================================================================
                        #                                 plt.plot([x, x1],[y,y1],color='red')
                        #                                 plt.plot([x2,x3], [y2,y3],color='red') 
                        # =============================================================================
                                        
                                        tpLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                        tpWidth = round(abs(y2-y1),2)
                                        tpheight = int(tpHeight[2])
                                        top = max(y,y1,y2,y3)
                                        differenciate_list.append(top)
                                        if tpheight == 8:
                                            tpActualheight = 7.25
                                        else:
                                            tpActualheight = round(float(tpheight) - 0.5,2)
                                        #print(bpHeight)
                                        Tp_dict[(count)] = list([tpLength,tpWidth,tpheight,tpActualheight,top])
                                        #print(Tp_dict)
                        d1 = dict(list(Tp_dict.items())[len(Tp_dict)//2:])
                        d2 = dict(list(Tp_dict.items())[:len(Tp_dict)//2])
    
                        vtp_dict ={}
                        tp_dict ={}
    
                        if len(Tp_dict) >=2:
                            if list(d1.values())[0][4] > list(d2.values())[0][4]:
                                vtpLength = list(d1.values())[0][0]
                                vtpWidth = list(d1.values())[0][1]
                                vtpHeight = list(d1.values())[0][2]
                                vtpActualheight = list(d1.values())[0][3]
                                
                                tpLength = list(d2.values())[0][0]
                                tpWidth = list(d2.values())[0][1]
                                tphieght = list(d2.values())[0][2]
                                tpActualheight = list(d2.values())[0][3]
                                
                                tp_dict[1] = list([tpLength,tpWidth,tphieght,tpActualheight])
                                vtp_dict[1] = list([vtpLength,vtpWidth,vtpHeight,vtpActualheight])
                            else:
                                vtpLength = list(d2.values())[0][0]
                                vtpWidth = list(d2.values())[0][1]
                                vtpHeight = list(d2.values())[0][2]
                                vtpActualheight = list(d2.values())[0][3]
                                
                                tpLength = list(d1.values())[0][0]
                                tpWidth = list(d1.values())[0][1]
                                tphieght = list(d1.values())[0][2]
                                tpActualheight = list(d1.values())[0][3]
                                
                                tp_dict[1] = list([tpLength,tpWidth,tphieght,tpActualheight])
                                vtp_dict[1] = list([vtpLength,vtpWidth,vtpHeight,vtpActualheight])
                            
                            
                        else:
                            tp_dict = Tp_dict
                except:
                    if my_dict['TopPlate'] == 2  :
                        Tp_dict = {} 
                        count = 0
                        differenciate_list = []
                        for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                            for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                                if ezxPart.find('PartTypeName').text == "TopPlate" :
                                    count = count +1
                                    tpHeight =  ezxPart.find('MaterialName').text
                                    #print(tpHeight)   
                                    for elevationPoints in ezxPart.findall('ElevationPoints'):
                                        listTp = []
                                        for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                            x = float(ezxPoint2d.find('X').text)
                                            y = float(ezxPoint2d.find('Y').text)
                                            if ezxPoint2d.find('X').text== '-0':
                                                x=0
                                            listTp.append([x,y])
    
                                    listTp.sort(key=operator.itemgetter((1)))
                                    #print(listTp)
                                    
                                    
                                    for i in range(0,len(listTp),4):
    
                                        #print(i,"i")
                                        x = (listTp[i][0])
                                        y = (listTp[i][1])
                                        x1 = (listTp[i+1][0])
                                        y1 = (listTp[i+1][1])
                                        x2 = listTp[i+2][0]
                                        y2 = listTp[i+2][1]
                                        x3 = listTp[i+3][0]
                                        y3 = listTp[i+3][1]
                        # =============================================================================
                        #                                 plt.plot([x, x1],[y,y1],color='red')
                        #                                 plt.plot([x2,x3], [y2,y3],color='red') 
                        # =============================================================================
                                        
                                        tpLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                        tpWidth = round(abs(y2-y1),2)
                                        tpheight = int(tpHeight[2])
                                        top = max(y,y1,y2,y3)
                                        differenciate_list.append(top)
                                        if tpheight == 8:
                                            tpActualheight = 7.25
                                        else:
                                            tpActualheight = round(float(tpheight) - 0.5,2)
                                        #print(bpHeight)
                                        Tp_dict[(count)] = list([tpLength,tpWidth,tpheight,tpActualheight,top])
                                        print(Tp_dict)
                        d1 = dict(list(Tp_dict.items())[len(Tp_dict)//2:])
                        d2 = dict(list(Tp_dict.items())[:len(Tp_dict)//2])
    
                        vtp_dict ={}
                        tp_dict ={}
    
                        if len(Tp_dict) >=2:
                            if list(d1.values())[0][4] > list(d2.values())[0][4]:
                                vtpLength = list(d1.values())[0][0]
                                vtpWidth = list(d1.values())[0][1]
                                vtpHeight = list(d1.values())[0][2]
                                vtpActualheight = list(d1.values())[0][3]
                                
                                tpLength = list(d2.values())[0][0]
                                tpWidth = list(d2.values())[0][1]
                                tphieght = list(d2.values())[0][2]
                                tpActualheight = list(d2.values())[0][3]
                                
                                tp_dict[1] = list([tpLength,tpWidth,tphieght,tpActualheight])
                                vtp_dict[1] = list([vtpLength,vtpWidth,vtpHeight,vtpActualheight])
                            else:
                                vtpLength = list(d2.values())[0][0]
                                vtpWidth = list(d2.values())[0][1]
                                vtpHeight = list(d2.values())[0][2]
                                vtpActualheight = list(d2.values())[0][3]
                                
                                tpLength = list(d1.values())[0][0]
                                tpWidth = list(d1.values())[0][1]
                                tphieght = list(d1.values())[0][2]
                                tpActualheight = list(d1.values())[0][3]
                                
                                tp_dict[1] = list([tpLength,tpWidth,tphieght,tpActualheight])
                                vtp_dict[1] = list([vtpLength,vtpWidth,vtpHeight,vtpActualheight])
                            
                            
                        else:
                            tp_dict = Tp_dict
                        
                    #print(tp_dict, "tpdict")
                    #print(vtp_dict, "vtpdict")
# =============================================================================
#                     for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
#                         for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
#                             if ezxPart.find('PartTypeName').text == "SFTopPlate":
#                                 tpHeight =  ezxPart.find('MaterialName').text
#                                 for elevationPoints in ezxPart.findall('ElevationPoints'):
#                                     for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
#                                         x = float(ezxPoint2d.find('X').text)
#                                         y = float(ezxPoint2d.find('Y').text)
#                                         listTp.append([x,y])
#                                 listTp.sort(key=operator.itemgetter((1)))   
#                                 
#                                 
#                                 for i in range(0,len(listTp)):
#                                     
#                                     try:
#                                         #print(sum(listTp[i]))
#                                         x = (listTp[i][0])
#                                         y = (listTp[i][1])
#                                         x1 = (listTp[i+1][0])
#                                         y1 = (listTp[i+1][1])
#                                         x2 = listTp[i+2][0]
#                                         y2 = listTp[i+2][1]
#                                         x3 = listTp[i+3][0]
#                                         y3 = listTp[i+3][1]
#                                         
#                                         x4 = (listTp[i+4][0])
#                                         y4 = (listTp[i+4][1])
#                                         x5 = (listTp[i+5][0])
#                                         y5 = (listTp[i+5][1])
#                                         x6 = listTp[i+6][0]
#                                         y6 = listTp[i+6][1]
#                                         x7 = listTp[i+7][0]
#                                         y7 = listTp[i+7][1]
#                                         
#     # =============================================================================
#     #                                     plt.plot([x, x1],[y,y1],color='green')
#     #                                     plt.plot([x2,x3], [y2,y3],color='green')      
#     #                                     plt.plot([x4, x5],[y4,y5])
#     #                                     plt.plot([x6,x7], [y6,y7])    
#     # =============================================================================
#                                         
#                                         tp = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
#                                         tpwidth = round(abs(y2 - y),2)
#                                         #print(tpwidth)
#                                         tpDside = min(y,y1)
#                                         
#                                         vtp = round(max(x4,x5,x6,x7) - min(x4,x5,x6,x7),2)
#                                         vtpDside = min(y4,y5)
#                                         
#                                         veryTop = max(tp,vtp)
#                                         
#                                         tpheight = max(y,y1,y2,y3)
#                                         vtpheight = max(y4,y5,y6,y7)
#                                         
#                                         tpLength =0
#                                         tpWidth = 0
#                                         tphieght = 0
#                                         tpDownSide = 0
#                                         
#                                         vtpLength =0
#                                         vtpHeight = 0
#                                         vtpWidth = 0
#                                         
#                                         
#                                         if vtpheight > tpheight:
#                                             vtpLength = vtp
#                                             vtpHeight = round(abs(y6 - y4),2)
#                                             if vtpHeight == 8:
#                                                 vtpActualheight = 7.25
#                                             else:
#                                                 vtpActualheight = round(float(vtpHeight) - 0.5,2)
#                                             vtpWidth = int(tpHeight[2])
#                                             
#                                             tpLength = tp
#                                             tphieght = int(tpHeight[2])
#                                             if tphieght == 8:
#                                                 tpActualheight = 7.25
#                                             else:
#                                                 tpActualheight = round(float(tphieght) - 0.5,2)
#                                             tpWidth = tpwidth
#                                             tpDownSide = tpDside
#                                         else:
#                                             vtpLength = tp
#                                             vtpHeight = int(tpHeight[2])
#                                             if vtpHeight == 8:
#                                                 vtpActualheight = 7.25
#                                             else:
#                                                 vtpActualheight = round(float(vtpHeight) - 0.5,2)
#                                             vtpWidth = tpwidth
#                                             
#                                             tpLength = vtp
#                                             tphieght = int(tpHeight[2])
#                                             if tphieght == 8:
#                                                 tpActualheight = 7.25
#                                             else:
#                                                 tpActualheight = round(float(tphieght) - 0.5,2)
#                                             tpWidth = round(abs(y6 - y4),2)
#                                             tpDownSide = vtpDside
#                                         
#                                     except:
#                                         tpLength =bpLength
#                                         tpWidth = 2
#                                         tphieght = 6
#                                         tpActualheight = 5.5
#                                         tpDownSide = 0
#                                         
#                                         vtpLength =bpLength
#                                         vtpHeight = 6
#                                         vtpWidth = 2
#                                         vtpActualheight = 5.5
#                                
#                     tp_dict ={}
#                     tp_dict[1] = list([tpLength,tpWidth,tphieght,tpActualheight])
#                     vtp_dict = {}
#                     vtp_dict[1] = list([vtpLength,vtpWidth,vtpHeight,vtpActualheight])
#                     #print(vtp_dict)
#                     print('execute third block')
# =============================================================================

                
                
                
                sill_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):                
                        if ezxPart.find('PartTypeName').text == "Sill":
                            count+=1
                            sillheight =  ezxPart.find('MaterialName').text
                            if sillheight == None:
                                sillheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listSill = []
                                
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listSill.append([x,y])
                            listSill.sort(key=operator.itemgetter((1)))    
                            for i in range(0,len(listSill),4):
                                
                                try:
                                    #print(sum(listTp[i]))
                                    x = (listSill[i][0])
                                    y = (listSill[i][1])
                                    x1 = (listSill[i+1][0])
                                    y1 = (listSill[i+1][1])
                                    x2 = listSill[i+2][0]
                                    y2 = listSill[i+2][1]
                                    x3 = listSill[i+3][0]
                                    y3 = listSill[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    
                                    sillLength = round(max(x,x1,x2,x3) - min(x,x1,x2,x3),2)
                                    sillWidth = abs(y2-y1)
                                    sillHeight = int(sillheight[2])
                                    if sillHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(sillHeight) - 0.5,2)
                                    sill_dict[count] = list([sillLength,sillWidth,sillHeight,min(x,x1,x2,x3),max(x,x1,x2,x3),Actualheight])
                                except:
                                    pass
                                    
                count =0                  
                #print(sill_dict) 
                blocking_dict = {}               
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):   
                        
                        if ezxPart.find('PartTypeName').text == "SFBlocking":
                            listBlocks = []
                            count = count+1
                            blockheight =  ezxPart.find('MaterialName').text
                            if blockheight  == None:
                                blockheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listBlocks.append([x,y])
                                    
                                
                            listBlocks.sort(key=operator.itemgetter((1)))        
                            for i in range(0,len(listBlocks),4):
                                
                                
                                try:
                                    #print(sum(listTp[i]))
                                    x = (listBlocks[i][0])
                                    y = (listBlocks[i][1])
                                    x1 = (listBlocks[i+1][0])
                                    y1 = (listBlocks[i+1][1])
                                    x2 = listBlocks[i+2][0]
                                    y2 = listBlocks[i+2][1]
                                    x3 = listBlocks[i+3][0]
                                    y3 = listBlocks[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    
                                    blockLength = round(max(x2,x1,x,x3) - min(x2,x1,x,x3),2)
                                    blockWidth = round(abs(y-y3),1)
                                    blockHeight = int(blockheight[2])
                                    dim = round(abs(y2-(abs(y2-y1)/2)),2)
                                    blocking_dict[count] = list([blockLength,blockWidth,blockHeight,dim])
                                    
                                except:
                                    pass
                                    
                                    
                               
                #print(listBlocks)                
                #print(len(blocking_dict))
                
                king_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "KingStud":
                            listKingStud = []
                            count+=1
                            kingheight =  ezxPart.find('MaterialName').text
                            if kingheight  == None:
                                kingheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listKingStud.append([x,y])
                            listKingStud.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(listKingStud),4):
                                try:
                                
                                    #print(sum(listTp[i]))
                                    x = (listKingStud[i][0])
                                    y = (listKingStud[i][1])
                                    x1 = (listKingStud[i+1][0])
                                    y1 = (listKingStud[i+1][1])
                                    x2 = listKingStud[i+2][0]
                                    y2 = listKingStud[i+2][1]
                                    x3 = listKingStud[i+3][0]
                                    y3 = listKingStud[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    KingLength = round(max(y,y1,y2,y3) - bpWidth,2)
                                    KingWidth = abs(x-x3)
                                    KingHeight = int(kingheight[2:4])
                                    if KingHeight == 8:
                                        Actualheight = 7.25
                                    elif KingHeight == 10:
                                        Actualheight = 9.25
                                    else:
                                        Actualheight = round(float(KingHeight) - 0.5,2)
                                    
                                    dimK = round(abs(x3-(abs(x-x3)/2)),2)
                                    king_dict[count] = list([KingLength,KingWidth,KingHeight,dimK,Actualheight])
                                except:
                                    pass
                
                
                holdown_dict = {}
                count = 0
                hold_dim = []
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "Wall Holdown":
                            listHoldown = []
                            holdownx = []
                            holdowny = []
                            count+=1   
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    
                                    #print(x , y)
                                    listHoldown.append([x,y])
                                    if  1.49 <= y <=1.75 :
                                        holdownx.append(x)
                                        #print(holdownx,"nothing")
                                      
                                    holdowny.append(y)
                            listHoldown.sort(key=operator.itemgetter((1)))
                            print(holdownx)
                            
                            height = max(holdownx) - min(holdownx)
                            #print(holdownx[0] ,"hello", holdownx[1]) 
                            dim = round(abs(holdownx[0] - height/2),2)
                            length = max(holdowny) - min(holdowny)
                            hold_dim.append(int(dim))
                            holdown_dict[count] = list([height,length,dim])
               
                #print(holdown_dict)
                
                bolt_dict = {}
                count =0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        text = ezxPart.find('MaterialName').text
                        
                        midval = 0
                        if ezxPart.find('PartTypeName').text == "Wall Anchor":# and ezxPart.find('MaterialName').text == text:
                            bolt = ezxPart.find('MaterialName').text
                            count+=1
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                if(len(elevationPoints) >10):
                                    for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                       
                                        try:
                                            if float(ezxPoint2d.find('Y').text) <0:
                                                
                                                x = float(ezxPoint2d.find('X').text)
                                                y = float(ezxPoint2d.find('Y').text)
                                                #print(x,y)
                                                midval = midval+x
                                        except:
                                            continue
                                    
                                    one = re.findall('([0-9]+).',text)
                                    print(one)
                                    #print(height)
                                    newheight = (one[0])
                                    
                                    #print(newheight)
                                    width = one[1]
                                    bolt_dict[count] = list([newheight,width,round(abs(midval/2),2)])
                                        
                #print(bolt_dict)
                
                
                leftstud_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "SFStudLeft":
                            listLeftstud = []
                            count+=1
                            leftstudheight =  ezxPart.find('MaterialName').text
                            if leftstudheight  == None:
                                leftstudheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listLeftstud.append([x,y])
                            listLeftstud.sort(key=operator.itemgetter((0))) 
                            try:
                                for i in range(0,len(listLeftstud),4):
                                    
                                    
                                        #print(sum(listTp[i]))
                                        x = (listLeftstud[i][0])
                                        y = (listLeftstud[i][1])
                                        x1 = (listLeftstud[i+1][0])
                                        y1 = (listLeftstud[i+1][1])
                                        x2 = listLeftstud[i+2][0]
                                        y2 = listLeftstud[i+2][1]
                                        x3 = listLeftstud[i+3][0]
                                        y3 = listLeftstud[i+3][1]
    # =============================================================================
    #                                     plt.plot([x, x1],[y,y1],color='black')
    #                                     plt.plot([x2,x3], [y2,y3],color='black')
    # =============================================================================
                                        #print(y,y1,y2,y3)
                                        leftstudLength = round(max(y,y1,y2,y3) - bpWidth,2)
                                        leftstudWidth = round(abs(x-x3),2)
                                        leftstudHeight = int(leftstudheight[2:4])
                                        if leftstudHeight == 8:
                                            Actualheight = 7.25
                                        elif leftstudHeight == 10:
                                            Actualheight = 9.25
                                        else:
                                            Actualheight = round(float(leftstudHeight) - 0.5,2)
                                        
                                        dimLS = round(abs(x3-(abs(x-x3)/2)),2)
                                        leftstud_dict[count] = list([leftstudLength,leftstudWidth,leftstudHeight,dimLS,Actualheight])    
                            except:
                                for i in range(0,len(listLeftstud),8):
                                    
                                    
                                        #print(sum(listTp[i]))
                                        x = (listLeftstud[i][0])
                                        y = (listLeftstud[i][1])
                                        x1 = (listLeftstud[i+1][0])
                                        y1 = (listLeftstud[i+1][1])
                                        x2 = listLeftstud[i+2][0]
                                        y2 = listLeftstud[i+2][1]
                                        x3 = listLeftstud[i+3][0]
                                        y3 = listLeftstud[i+3][1]
                                        x3 = listLeftstud[i+3][0]
                                        y3 = listLeftstud[i+3][1]
                                        x4 = listLeftstud[i+4][0]
                                        y4 = listLeftstud[i+4][1]
                                        y5 = listLeftstud[i+5][1]
                                        x5 = listLeftstud[i+5][0]
    # =============================================================================
    #                                     plt.plot([x, x1],[y,y1],color='black')
    #                                     plt.plot([x2,x3], [y2,y3],color='black')
    # =============================================================================
                                        #print(y,y1,y2,y3)
                                        leftstudLength = round(max(y,y1,y2,y3,y4,y5) - bpWidth,2)
                                        leftstudWidth = round(abs(max(x,x1,x2,x3,x4,x5) - min(x,x1,x2,x3,x4,x5)),2)
                                        leftstudHeight = int(leftstudheight[2:4])
                                        if leftstudHeight == 8:
                                            Actualheight = 7.25
                                        elif leftstudHeight == 10:
                                            Actualheight = 9.25
                                        else:
                                            Actualheight = round(float(leftstudHeight) - 0.5,2)
                                        
                                        dimLS = round(abs(max(x,x1,x2,x3,x4,x5)-abs(max(x,x1,x2,x3,x4,x5) - min(x,x1,x2,x3,x4,x5))/2),2)
                                        leftstud_dict[count] = list([leftstudLength,leftstudWidth,leftstudHeight,dimLS,Actualheight]) 
                                
                #print(leftstud_dict)
                
                rightstud_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "SFStudRight":
                            listrightstud = []
                            count+=1
                            rightstudheight =  ezxPart.find('MaterialName').text
                            if rightstudheight  == None:
                                rightstudheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    listrightstud.append([x,y])
                            listrightstud.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(listrightstud),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (listrightstud[i][0])
                                    y = (listrightstud[i][1])
                                    x1 = (listrightstud[i+1][0])
                                    y1 = (listrightstud[i+1][1])
                                    x2 = listrightstud[i+2][0]
                                    y2 = listrightstud[i+2][1]
                                    x3 = listrightstud[i+3][0]
                                    y3 = listrightstud[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1],color='black')
#                                     plt.plot([x2,x3], [y2,y3],color='black')
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    rightstudLength = round(max(y,y1,y2,y3) - bpWidth,2)
                                    rightstudWidth = round(abs(x-x3),2)
                                    rightstudHeight = int(rightstudheight[2])
                                    if rightstudHeight == 8:
                                        Actualheight = 7.25
                                    elif rightstudHeight == 10:
                                        Actualheight = 9.25
                                    else:
                                        Actualheight = round(float(rightstudHeight) - 0.5,2)
                                    dimRS = round(abs(x3-(abs(x-x3)/2)),2)
                                    rightstud_dict[count] = list([rightstudLength,rightstudWidth,rightstudHeight,dimRS,Actualheight])    
                                    
                #print(rightstud_dict)
                
                stud_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "Stud":
                            stud = []
                            count+=1
                            studheight =  ezxPart.find('MaterialName').text
                            if studheight  == None:
                                studheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    stud.append([x,y])
                            stud.sort(key=operator.itemgetter((0))) 
                            try:
                                for i in range(0,len(stud),4):
                                    
                                
                                    #print(sum(listTp[i]))
                                    x = (stud[i][0])
                                    y = (stud[i][1])
                                    x1 = (stud[i+1][0])
                                    y1 = (stud[i+1][1])
                                    x2 = stud[i+2][0]
                                    y2 = stud[i+2][1]
                                    x3 = stud[i+3][0]
                                    y3 = stud[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1],color='black')
#                                     plt.plot([x2,x3], [y2,y3],color='black')
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    studLength = round(max(y,y1,y2,y3) - bpWidth,2)
                                    studWidth = round(abs(x-x3),2)
                                    studHeight = int(studheight[2:4])
                                    if studHeight == 8:
                                        Actualheight = 7.25
                                    elif studHeight == 10:
                                        Actualheight = 9.25
                                    else:
                                        Actualheight = round(float(studHeight) - 0.5,2)
                                    dimS = round(abs(x3-(abs(x-x3)/2)),2)
                                    stud_dict[count] = list([studLength,studWidth,studHeight,dimS,Actualheight])    
                            except:
                                for i in range(0,len(stud),8):
                                    x = (stud[i][0])
                                    y = (stud[i][1])
                                    x1 = (stud[i+1][0])
                                    y1 = (stud[i+1][1])
                                    x2 = stud[i+2][0]
                                    y2 = stud[i+2][1]
                                    x3 = stud[i+3][0]
                                    y3 = stud[i+3][1]
                                    x4 = stud[i+4][0]
                                    y4 = stud[i+4][1]
                                    y5 = stud[i+5][1]
                                    x5 = stud[i+5][0]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1],color='black')
#                                     plt.plot([x2,x3], [y2,y3],color='black')
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    studLength = round(max(y,y1,y2,y3,y4,y5) - bpWidth,2)
                                    studWidth = round(abs(max(x,x1,x2,x3,x4,x5) - min(x,x1,x2,x3,x4,x5)),2)
                                    studHeight = int(studheight[2:4])
                                    if studHeight == 8:
                                        Actualheight = 7.25
                                    elif studHeight == 10:
                                        Actualheight = 9.25
                                    else:
                                        Actualheight = round(float(studHeight) - 0.5,2)
                                    dimS = round(abs(max(x,x1,x2,x3,x4,x5)-abs(max(x,x1,x2,x3,x4,x5) - min(x,x1,x2,x3,x4,x5))/2),2)
                                    stud_dict[count] = list([studLength,studWidth,studHeight,dimS,Actualheight])
                                    
                print(stud_dict, "stud dict")
                
                beam_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "SFSupportingBeam":
                            beam = []
                            count+=1
                            beamheight =  ezxPart.find('MaterialName').text
                            if beamheight  == None:
                                beamheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    beam.append([x,y])
                            beam.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(beam),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (beam[i][0])
                                    y = (beam[i][1])
                                    x1 = (beam[i+1][0])
                                    y1 = (beam[i+1][1])
                                    x2 = beam[i+2][0]
                                    y2 = beam[i+2][1]
                                    x3 = beam[i+3][0]
                                    y3 = beam[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    beamLength = round(max(y,y1,y2,y3) - bpWidth,2) 
                                    beamWidth = round(abs(x-x3),2)
                                    beamHeight = int(beamheight[2])
                                    if beamHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(beamHeight) - 0.5,2)
                                    dimB = round(abs((x3-(abs(x-x3)/2))),2)
                                    beam_dict[dimB] = list([beamLength,beamWidth,beamHeight,dimB,count,Actualheight])    
                                    
                #print(beam_dict)
                
                under_dict = {}
                under_count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "SFJackUnderOpening":
                            under = []
                            under_count+=1
                            underheight =  ezxPart.find('MaterialName').text
                            if underheight  == None:
                                underheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    under.append([x,y])
                            under.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(under),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (under[i][0])
                                    y = (under[i][1])
                                    x1 = (under[i+1][0])
                                    y1 = (under[i+1][1])
                                    x2 = under[i+2][0]
                                    y2 = under[i+2][1]
                                    x3 = under[i+3][0]
                                    y3 = under[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    underLength = round(max(y,y1,y2,y3) - bpWidth ,2)
                                    underWidth = round(abs(x-x3),1)
                                    underHeight = int(underheight[2])
                                    if underHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(underHeight) - 0.5,2)
                                    dimU = round(abs((x3-(abs(x-x3)/2))),2)
                                    under_dict[dimU] = list([underLength,underWidth,underHeight,dimU,under_count,Actualheight])    
                                    
                #print(under_dict)
                sunder_dict = dict(sorted(under_dict.items()))
                #print(under_dict)
                over_dict = {}
                count = under_count
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "SFJackOverOpening":
                            over = []
                            count+=1
                            overheight =  ezxPart.find('MaterialName').text
                            if overheight  == None:
                                overheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    over.append([x,y])
                            over.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(over),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (over[i][0])
                                    y = (over[i][1])
                                    x1 = (over[i+1][0])
                                    y1 = (over[i+1][1])
                                    x2 = over[i+2][0]
                                    y2 = over[i+2][1]
                                    x3 = over[i+3][0]
                                    y3 = over[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    overLength = round(max(y,y1,y2,y3) - min(y,y1,y2,y3),2)
                                    overWidth = round(abs(x-x3),1)
                                    overHeight = int(overheight[2])
                                    if overHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(overHeight) - 0.5,2)
                                    dimO = round(abs((x3-(abs(x-x3)/2))),2)
                                    over_dict[dimO] = list([overLength,overWidth,overHeight,dimO,count,Actualheight])    
                                    
                #print(over_dict)
                ounder_dict = dict(sorted(over_dict.items()))
               
                
               
                crippleBp_dict = {}
                crippleTp_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "Cripple":
                            cripple = []
                            count+=1
                            crippleheight =  ezxPart.find('MaterialName').text
                            if crippleheight  == None:
                                crippleheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    cripple.append([x,y])
                            cripple.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(cripple),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (cripple[i][0])
                                    y = (cripple[i][1])
                                    x1 = (cripple[i+1][0])
                                    y1 = (cripple[i+1][1])
                                    x2 = cripple[i+2][0]
                                    y2 = cripple[i+2][1]
                                    x3 = cripple[i+3][0]
                                    y3 = cripple[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1])
#                                     plt.plot([x2,x3], [y2,y3])
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    crippleLength = round(max(y,y1,y2,y3) - min(y,y1,y2,y3),2)
                                    crippleWidth = round(abs(x-x3),1)
                                    crippleHeight = int(crippleheight[2])
                                    if crippleHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(crippleHeight) - 0.5,2)
                                    dimC = round(abs((x3-(abs(x-x3)/2))),2)
                                    
                                    if y <= 1.5 or y1 <= 1.5 or y2 <= 1.5 or y3 <= 1.5:
                                        crippleBp_dict[dimC] = list([crippleLength,crippleWidth,crippleHeight,dimC,count,Actualheight])    
                                    else:
                                        crippleTp_dict[dimC] = list([crippleLength,crippleWidth,crippleHeight,dimC,count,Actualheight])    
                print(crippleBp_dict, "bp")
                print("_______________________________")
                print(crippleTp_dict,"tp")

                ounder_dict = dict(sorted(over_dict.items()))
               
                
               
                
                hssbeam_dict = {} 
                count = 0
               
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):
                        if ezxPart.find('PartTypeName').text == "Beam":
                            count = count +1
                            hssbeamHeight =  ezxPart.find('MaterialName').text
                               
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                listHSSBeam = []
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    if ezxPoint2d.find('X').text== '-0':
                                        x=0
                                    listHSSBeam.append([x,y])
                
                            listHSSBeam.sort(key=operator.itemgetter((1)))
                            #print(listBp)
                            
                            
                            for i in range(0,len(listHSSBeam),4):
                
                                #print(i,"i")
                                x = (listHSSBeam[i][0])
                                y = (listHSSBeam[i][1])
                                x1 = (listHSSBeam[i+1][0])
                                y1 = (listHSSBeam[i+1][1])
                                x2 = listHSSBeam[i+2][0]
                                y2 = listHSSBeam[i+2][1]
                                x3 = listHSSBeam[i+3][0]
                                y3 = listHSSBeam[i+3][1]
# =============================================================================
#                                 plt.plot([x, x1],[y,y1],color='red')
#                                 plt.plot([x2,x3], [y2,y3],color='red') 
# =============================================================================
                                
                                hssbeamLength = round(max(x,x1),2)
                                hssbeamWidth = round(abs(y2-y1),2)
                                hssbeamheight = int(hssbeamHeight.split()[0].split('x')[1])
                                print(hssbeamheight)
                                if hssbeamheight == 8:
                                    hssbeamActualheight = 7.25
                                else:
                                    hssbeamActualheight = round(float(hssbeamheight) - 0.5,2)
                                #print(bpHeight)
                                hssbeam_dict[(count)] = list([hssbeamLength,hssbeamWidth,hssbeamheight,hssbeamheight])
               
                
                print(hssbeam_dict, "hello beam")
                
                post_dict = {}
                count = 0
                for arrayOfEzxPart in root.findall('ArrayOfEzxPart'):
                    for ezxPart in arrayOfEzxPart.findall('EzxPart'):        
                        if ezxPart.find('PartTypeName').text == "Post":
                            post = []
                            count+=1
                            postheight =  ezxPart.find('MaterialName').text
                            if postheight  == None:
                                postheight = '2x6'
                            for elevationPoints in ezxPart.findall('ElevationPoints'):
                                for ezxPoint2d in elevationPoints.findall('EzxPoint2d'):
                                    x = float(ezxPoint2d.find('X').text)
                                    y = float(ezxPoint2d.find('Y').text)
                                    post.append([x,y])
                            post.sort(key=operator.itemgetter((0))) 
                            
                            for i in range(0,len(post),4):
                                
                                
                                    #print(sum(listTp[i]))
                                    x = (post[i][0])
                                    y = (post[i][1])
                                    x1 = (post[i+1][0])
                                    y1 = (post[i+1][1])
                                    x2 = post[i+2][0]
                                    y2 = post[i+2][1]
                                    x3 = post[i+3][0]
                                    y3 = post[i+3][1]
# =============================================================================
#                                     plt.plot([x, x1],[y,y1],color='black')
#                                     plt.plot([x2,x3], [y2,y3],color='black')
# =============================================================================
                                    #print(y,y1,y2,y3)
                                    postLength = round(max(y,y1,y2,y3) - bpWidth,2)
                                    postWidth = round(abs(x-x3),2)
                                    postHeight = int(postheight[2])
                                    if postHeight == 8:
                                        Actualheight = 7.25
                                    else:
                                        Actualheight = round(float(postHeight) - 0.5,2)
                                    dimPost = round(abs(x3-(abs(x-x3)/2)),2)
                                    post_dict[count] = list([postLength,postWidth,postHeight,dimPost,postHeight])    
                print("post",post_dict)
                #modelTree = ET.parse('C:\\Users\shafe\\OneDrive\\Desktop\\convert xml\\fbModel.xml')
                #modelTree = ET.parse('C:\\Users\\admin\\Desktop\\convert xml\\fbModel.xml')
                modelTree = ET.parse('C:\\Users\home\OneDrive\Desktop\estiframe\estiframe\\fbModel.xml')

                modelRoot =  modelTree.getroot()
             
                
                #print(modelRoot)
                for head in modelRoot.findall('HEADER_DATA'):
                    head.find('SENDING_PROGRAM').text = 'Estiframe'
                    head.find('COMPANY').text = 'Turnipseed'
                    head.find('DATE').text = str(date.today())
                    head.find('TIME').text = str(time.ctime())
                    head.find('JOB_NAME').text = self.entry1_jobname.get()
                
                for structuredata in modelRoot.findall('STRUCTURE_DATA'):
                    structuredata.find('STRUCTURE_ID').text
                    for memid in structuredata.findall('MEMBERS'):
                        pass
                    
                for key,value in bp_dict.items():
                    new_memberdata(jobname1, 'Bp'+str(key), modelRoot,'BOTTOM_PLATE','Bottom_plate',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 PT Bottom Plate',str(value[0]),str(value[1]+0.5),str(value[2]),str((value[1])),str(value[3]))
                    sub_element_one('MEMBER_ID', jobname1, 'Bp'+str(key), memid)
                    
                for key,value in tp_dict.items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Tp'+str(key), modelRoot,'TOP_PLATE','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    else:
                        new_memberdata(jobname1, 'Tp'+str(key), modelRoot,'TOP_PLATE','Top plate',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Top plate',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    sub_element_one('MEMBER_ID', jobname1, 'Tp'+str(key), memid)
                    
                for key,value in vtp_dict.items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Vtp'+str(key), modelRoot,'VERYTOP_PLATE','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    else:
                        new_memberdata(jobname1, 'Vtp'+str(key), modelRoot,'VERYTOP_PLATE','Very topplate',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Very topplate',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))

                    sub_element_one('MEMBER_ID', jobname1, 'Vtp'+str(key), memid)
                    
                for key,value in header_dict.items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Hd'+str(key), modelRoot,'HEADER','--','Do not cut',str(value[0]),str(value[1]),str(value[2]),str(float(value[1])-0.5),str(float(value[2])-0.5))
                    else:
                        new_memberdata(jobname1, 'Hd'+str(key), modelRoot,'HEADER','Header',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Header',str(value[0]),str(value[1]),str(value[2]),str(float(value[1])-0.5),str(float(value[2])-0.5))
                    sub_element_one('MEMBER_ID', jobname1, 'Hd'+str(key), memid)
                
                for key,value in sill_dict.items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Sl'+str(key), modelRoot,'SILL','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                    else:
                        new_memberdata(jobname1, 'Sl'+str(key), modelRoot,'SILL','Sill',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Sill',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                    sub_element_one('MEMBER_ID', jobname1, 'Sl'+str(key), memid)
                    
                for key,value in headerTp_dict.items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Hts'+str(key), modelRoot,'HEADERTOP_SILL','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    else:
                        new_memberdata(jobname1, 'Hts'+str(key), modelRoot,'HEADERTOP_SILL','Headertop_sill',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Headetop_sill',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    
                    sub_element_one('MEMBER_ID', jobname1, 'Hts'+str(key), memid)
                
                for key,value in headerBp_dict .items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Hbs'+str(key), modelRoot,'HEADERBOTTOM_SILL','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    else:
                        new_memberdata(jobname1, 'Hbs'+str(key), modelRoot,'HEADERBOTTOM_SILL','HeaderBottom_sill',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 HeaderBottom_plate',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))

                    sub_element_one('MEMBER_ID', jobname1, 'Hbs'+str(key), memid)
                    
                for key,value in hssbeam_dict .items():
                    if self.desc.get() == "":
                        new_memberdata(jobname1, 'Hssb'+str(key), modelRoot,'HSS_BEAM','--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))
                    else:
                        new_memberdata(jobname1, 'Hssb'+str(key), modelRoot,'HSS_BEAM','Hss_Beam',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Hss Beam',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[3])))

                    sub_element_one('MEMBER_ID', jobname1, 'Hssb'+str(key), memid)
                
                ET.indent(modelTree, '     ')
# =============================================================================
#                 modelTree.write("C:\\Users\\shafe\\OneDrive\\Desktop\\convert xml\\ezx.xml")
#                 finalTree = ET.parse("C:\\Users\\shafe\\OneDrive\\Desktop\\convert xml\\ezx.xml")
# =============================================================================
# =============================================================================
                 #modelTree.write("C:\\Users\\admin\\Desktop\\convert xml\\ezx.xml")
                modelTree.write("C:\\Users\home\OneDrive\Desktop\estiframe\estiframe\\ezx.xml")
                finalTree = ET.parse("C:\\Users\home\OneDrive\Desktop\estiframe\estiframe\\ezx.xml")
                 #finalTree = ET.parse("C:\\Users\\admin\\Desktop\\convert xml\\ezx.xml")
                finalRoot = finalTree.getroot()

                
                for structuredata in finalRoot.findall('STRUCTURE_DATA'):
                    structuredata.find('STRUCTURE_ID').text = jobname1
                    for memid in structuredata.findall('MEMBERS'):
                        pass
                    
                structuredata.find('MEMBER_QTY').text = str(len(bp_dict)+len(tp_dict)+len(vtp_dict)+len(header_dict)+len(sill_dict)+len(leftstud_dict)+len(rightstud_dict)+len(stud_dict)+len(king_dict)+len(beam_dict)+len(under_dict)+len(holdown_dict)+len(bolt_dict)+len(over_dict)+len(blocking_dict)+len(headerTp_dict)+len(headerBp_dict)+len(hssbeam_dict)+len(crippleBp_dict)+len(crippleTp_dict)+len(post_dict))
                #print(structuredata.find('MEMBER_QTY').text)
                #print(len(bp_dict) ,len(tp_dict) ,len(vtp_dict), len(header_dict), len(sill_dict) , len(leftstud_dict), len(rightstud_dict), len(stud_dict), len(king_dict) ,len(beam_dict), len(under_dict), len(holdown_dict), len(bolt_dict), len(over_dict), len(blocking_dict), len(headerTp_dict), len(headerBp_dict), len(hssbeam_dict))
                cripple_count = 0
                countHead = 0
                countHead1 = 0
                countHead2 =0
                countSill = 0
                for memberdata in finalRoot.findall('MEMBER_DATA'):
                    print(memberdata.find('TYPE').text)
                    if memberdata.find('TYPE').text == 'BOTTOM_PLATE':
# =============================================================================
#                         for membertype_text in memberdata.iter('DESCRIPTION'):
#                             a = str(self.desc.get())+'Bottom Plate'
#                             membertype_text.text = str(a)
# =============================================================================
                        for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                            a = ''
                            membertype_text.text = str(a)
                        for bottomplate_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                            count =0
                            for key,value in leftstud_dict.items():
                                attachments(jobname1, 'lst'+str(count+1), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'lst'+str(count+1), memid)        
                                if self.desc.get() == "":
                                    new_memberdata(jobname1, 'lst'+str(count+1), finalRoot, 'SLEFTSTUD', '--','Do not cut',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))
                                else:
                                    new_memberdata(jobname1, 'lst'+str(count+1), finalRoot, 'SLEFTSTUD', 'Leftstud',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Leftstud',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))

                                count = count + 1
                            count = 0
                            for key,value in rightstud_dict.items():
                                attachments(jobname1, 'Rst'+str(count+1), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'Rst'+str(count+1), memid)        
                                if self.desc.get() == "":
                                    new_memberdata(jobname1, 'Rst'+str(count+1), finalRoot, 'SRIGHTSTUD', '--','Do not cut',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))
                                else:
                                    new_memberdata(jobname1, 'Rst'+str(count+1), finalRoot, 'SRIGHTSTUD', 'Rightstud',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Rightstud',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))

                                count = count + 1
                            count = 0
                            for key,value in stud_dict.items():
                                attachments(jobname1, 'St'+str(count+1), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'St'+str(count+1), memid)        
                                if self.desc.get() == "":    
                                    new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'STUD', '--','Do not cut',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))
                                else:
                                    new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'STUD', 'Stud',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Stud',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))

                                count = count + 1
                            count = 0
                            for key,value in king_dict.items():
                                attachments(jobname1, 'Kst'+str(count+1), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'Kst'+str(count+1), memid)        
                                if self.desc.get() == "":    
                                    new_memberdata(jobname1, 'Kst'+str(count+1), finalRoot, 'SKINGSTUD', '--','Do not cut',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))
                                else:
                                    new_memberdata(jobname1, 'Kst'+str(count+1), finalRoot, 'SKINGSTUD', 'Skingstud',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Skingstud',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))

                                count = count + 1
                            count = 0    
                            for key,value in beam_dict.items():
                                attachments(jobname1, 'tr'+str(value[4]), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'tr'+str(value[4]), memid)        
                                if self.desc.get() == "":    
                                    new_memberdata(jobname1, 'tr'+str(value[4]), finalRoot, 'JTRIMMER', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                else:
                                    new_memberdata(jobname1, 'tr'+str(value[4]), finalRoot, 'JTRIMMER', 'Jtrimmer',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Jtrimmer',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                count = count + 1
                            count = 0  
                            count1 = 0
                            for key,value in sunder_dict.items():
                                if len(sill_dict) == 0:
                                    attachments(jobname1, 'tr'+str(value[4]), str(value[3]), bottomplate_memberdata)
                                    sub_element_one('MEMBER_ID', jobname1, 'tr'+str(value[4]), memid)        
                                    if self.desc.get() == "":    
                                        new_memberdata(jobname1, 'tr'+str(value[4]), finalRoot, 'JTRIMMER', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                    else:
                                        new_memberdata(jobname1, 'tr'+str(value[4]), finalRoot, 'JTRIMMER', 'Jtrimmer',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Jtrimmer',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                    count = count + 1
                                    
                                    
                                else:                 
                                    attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), bottomplate_memberdata)
                                    sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)        
                                    if self.desc.get() == "": 
                                        new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                    else:
                                        new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', 'Cripple',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Cripple',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))

                                    count1 = count1 + 1
                                    cripple_count = count1
                                    
                            count1 = cripple_count
                            for key,value in crippleBp_dict.items():
                                attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)        
                                if self.desc.get() == "": 
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                else:
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', 'Cripple',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Cripple',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))

                                count1 = count1 + 1
                                cripple_count = count1
                                
                            
                            count = 0    
                            for key,value in holdown_dict.items():
                                attachments(jobname1, 'H'+str(count+1), str(value[2]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'H'+str(count+1), memid)        
                                if self.desc.get() == "": 
                                    new_memberdata(jobname1, 'H'+str(count+1), finalRoot, 'HOLDOWN', '--','Do not cut',str(value[1]),str(value[0]),str(value[1]),str(value[0]),str(value[1]))
                                else:
                                    new_memberdata(jobname1, 'H'+str(count+1), finalRoot, 'HOLDOWN', 'Holdown',str(int(float(value[1])+0.5))+'x'+str(value[2])+' Holdown',str(value[1]),str(value[0]),str(value[1]),str(value[0]),str(value[1]))

                                count = count + 1
                            count = 0    
                            for key,value in bolt_dict.items():
                                attachments(jobname1, 'B'+str(count+1), str(value[2]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'B'+str(count+1), memid)        
                                if self.desc.get() == "": 
                                    new_memberdata(jobname1, 'B'+str(count+1), finalRoot, 'BANCHOR BOLT', '--','Do not cut',str(value[1]),str(value[0]),str(value[1]),str(value[0]),str(value[1]))
                                else:
                                    new_memberdata(jobname1, 'B'+str(count+1), finalRoot, 'BANCHOR BOLT', 'Banchor bolt',str(int(float(value[1])+0.5))+'x'+str(value[2])+' Banchor bolt',str(value[1]),str(value[0]),str(value[1]),str(value[0]),str(value[1]))
                                count = count + 1
                                
                            count = 0
                            for key,value in post_dict.items():
                                attachments(jobname1, 'P'+str(count+1), str(value[3]), bottomplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'P'+str(count+1), memid)        
                                if self.desc.get() == "":    
                                    new_memberdata(jobname1, 'P'+str(count+1), finalRoot, 'POST', '--','Do not cut',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))
                                else:
                                    new_memberdata(jobname1, 'P'+str(count+1), finalRoot, 'POST', 'Post',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Post',str(value[0]),str(int(math.ceil(value[1]))),str(value[2]),str((value[1])),str(float(value[4])))

                                count = count + 1
                        
                        memberdata.find('SIDE_1_NUM_ATTACH').text = str(len(leftstud_dict)+len(rightstud_dict)+len(stud_dict)+len(king_dict)+len(beam_dict)+len(under_dict)+len(crippleBp_dict)+len(holdown_dict)+len(bolt_dict)+len(post_dict))
                    #print(cripple_count)
                    if memberdata.find('TYPE').text == 'TOP_PLATE':
                        for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                            a = ''
                            membertype_text.text = str(a)
# =============================================================================
#                         if self.desc.get() != "":
#                             for membertype_text in memberdata.iter('DESCRIPTION'):
#                                 a = str(self.desc.get()) + 'Top Plate'
#                                 membertype_text.text = str(a)
# =============================================================================
                            
# =============================================================================
#                             for membertype_text in memberdata.iter('NAME'):
#                                 a = 'Top_plate'
#                                 membertype_text.text = str(a)
# =============================================================================
                            
                            membertype_text.text = str(a)
                        for topplate_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                            count =0
                            for key,value in leftstud_dict.items():
                                attachments(jobname1, 'lst'+str(count+1), str(value[3]), topplate_memberdata)
                                #sub_element_one('MEMBER_ID', jobname1, 'lst'+str(count+1), memid)        
                                #new_memberdata(jobname1, 'lst'+str(count+1), finalRoot, 'LEFTSTUD', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                count = count + 1
                            count = 0
                            for key,value in rightstud_dict.items():
                                attachments(jobname1, 'Rst'+str(count+1), str(value[3]), topplate_memberdata)
                                #sub_element_one('MEMBER_ID', jobname1, 'Rst'+str(count+1), memid)        
                                #new_memberdata(jobname1, 'Rst'+str(count+1), finalRoot, 'RIGHTSTUD', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                count = count + 1
                            count = 0
                            for key,value in stud_dict.items():
                                attachments(jobname1, 'St'+str(count+1), str(value[3]), topplate_memberdata)
                                #sub_element_one('MEMBER_ID', jobname1, 'St'+str(count+1), memid)        
                                #new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'STUD', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                count = count + 1
                            count = 0
                            for key,value in king_dict.items():
                                attachments(jobname1, 'Kst'+str(count+1), str(value[3]), topplate_memberdata)
                                #sub_element_one('MEMBER_ID', jobname1, 'Kst'+str(count+1), memid)        
                                #new_memberdata(jobname1, 'Kst'+str(count+1), finalRoot, 'KINGSTUD', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                count = count + 1
                            count = cripple_count  
                            for key,value in over_dict.items():
                                attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), topplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)        
                                if self.desc.get() == "": 
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                else:
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', 'Cripple',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Cripple',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))

                                count = count + 1    
                                
                            count = cripple_count  
                            for key,value in crippleTp_dict.items():
                                attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), topplate_memberdata)
                                sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)        
                                if self.desc.get() == "": 
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))
                                else:
                                    new_memberdata(jobname1, 'Cr'+str(value[4]), finalRoot, 'CRIPPLE', 'Cripple',str(int(float(value[1])+0.5))+'x'+str(value[2])+' SYP #2 Cripple',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[5])))

                                count = count + 1  
                        
                        memberdata.find('SIDE_1_NUM_ATTACH').text = str(len(leftstud_dict)+len(rightstud_dict)+len(stud_dict)+len(king_dict)+len(over_dict)+len(crippleTp_dict))
                    
                    print(len(headerTopplate_dict),"value")
                    if len(headerTopplate_dict) !=0:    
                        print("line executed")
                        if memberdata.find('TYPE').text == 'HEADERTOP_SILL':
                            print("line executed")
                            minandmax = list(header_dict.values())[0]
                            print(minandmax,"min and max")
                            countHead+=1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            countH =0
                            
                            for header_memberdata in memberdata.findall("SIDE_1_ATTACH"):  
                                
                                for key,value in over_dict.items():
                                    
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                                        
                                for key,value in crippleTp_dict.items():
                                    attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                    #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)
                                    
                                    
                            memberdata.find('SIDE_1_NUM_ATTACH').text = str((countH)+len(crippleTp_dict))
                            
                            
                        if memberdata.find('TYPE').text == 'HEADERBOTTOM_SILL':
                            minandmax = list(header_dict.values())[countHead1]
                            countHead1 += 1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            countH =0
                            for header_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                                for key,value in beam_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'tr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Be'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'BEAM', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                                if len(sill_dict) == 0:
                                    for key,value in under_dict.items():
                                        if key >= minandmax[3] and key<=minandmax[4]:
                                            
                                            attachments(jobname1, 'tr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                            #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count1+1), memid)        
                                            #new_memberdata(jobname1, 'Cr'+str(count1+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                            countH +=1
                                            
                                for key,value in crippleBp_dict.items():
                                    attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), header_memberdata)
                                    #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(value[4]), memid)
                                    countH +=1
                            
                            memberdata.find('SIDE_1_NUM_ATTACH').text = str((countH))
                    
                    
                    if  len(headerBp_dict) ==0 :
                        print("executed this part")
                        if memberdata.find('TYPE').text == 'HEADER':
                            minandmax = list(header_dict.values())[countHead2]
                            countHead2+=1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            countH =0
                            for header_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                                for key,value in beam_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'tr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Be'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'BEAM', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                                for key,value in over_dict.items():
                                    
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                            memberdata.find('SIDE_1_NUM_ATTACH').text = str((countH))
                    
                        
                        if memberdata.find('TYPE').text == 'SILL':
                            minandmax = list(sill_dict.values())[countSill]
                            countSill+=1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            
                            count1 = cripple_count
                            for sill_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                                for key,value in crippleBp_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(value[3]), sill_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count1+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count1+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        count1 +=1
                                
                                for key,value in under_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), sill_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count1+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count1+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        count1 +=1
                                
                            
                            memberdata.find('SIDE_1_NUM_ATTACH').text = str((count1))
                        
                    
                    else:
                        if memberdata.find('TYPE').text == 'HEADER':
                            minandmax = list(header_dict.values())[countHead]
                            countHead+=1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            countH =0
                            for header_memberdata in memberdata.findall("SIDE_1_ATTACH"):  
                                for key,value in over_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                                    
                                for key,value in beam_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'tr'+str(value[4]), str(round(value[3]-minandmax[3],2)), header_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Be'+str(count+1), memid)        
                                        #new_memberdata(jobname1, 'St'+str(count+1), finalRoot, 'BEAM', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        countH+=1
                            
                            memberdata.find('SIDE_1_NUM_ATTACH').text = str((countH))
                        
                        if memberdata.find('TYPE').text == 'SILL':
                            minandmax = list(sill_dict.values())[countSill]
                            countSill+=1
                            for membertype_text in memberdata.iter('SIDE_1_ATTACH'):
                                a = ''
                                membertype_text.text = str(a)
                            count = 0
                            for sill_memberdata in memberdata.findall("SIDE_1_ATTACH"):
                                for key,value in under_dict.items():
                                    if key >= minandmax[3] and key<=minandmax[4]:
                                        attachments(jobname1, 'Cr'+str(value[4]), str(round(value[3]-minandmax[3],2)), sill_memberdata)
                                        #sub_element_one('MEMBER_ID', jobname1, 'Cr'+str(count1+1), memid)        
                                        #new_memberdata(jobname1, 'Cr'+str(count1+1), finalRoot, 'CRIPPLE', '--',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str(int(value[1]+0.5)),str((value[2])))
                                        count +=1
                                    
                                            
                                memberdata.find('SIDE_1_NUM_ATTACH').text = str(count)
                    count = 0    
                for key,value in blocking_dict.items():
                    sub_element_one('MEMBER_ID', jobname1, 'Lb'+str(count+1), memid)        
                    new_memberdata(jobname1, 'lb'+str(count+1), finalRoot, 'BLOCK', '--','Do not cut',str(value[0]),str(int(value[1]+0.5)),str(value[2]),str((value[1])),str(float(value[2])-0.5))
                    count += 1
                
                
                
                ET.indent(finalTree, '     ')
                finalTree.write(output+"//"+outputFileName+str(num[0])+".xml")
            
            self.warning_label1 = customtkinter.CTkLabel(self,text_color='green', text='Completed !!',font=customtkinter.CTkFont(size=25, weight="bold"))
            self.warning_label1.place(x=380,y=480)
            self.warning_label1.after(6000, lambda:  self.warning_label1.destroy() )
            
            
            
if __name__ == "__main__":

    app = App()
    app.mainloop()  
