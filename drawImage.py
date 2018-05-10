#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on Tue Jan 16 17:58:13 2018

@author: pengtao
"""
import numpy as np
import cv2 

class getMousePlace():
    def __init__(self, Image,method,scaleNum ):
        self.img =  Image.copy() # np.zeros((512,512,3),np.uint8)
        self.imgori = Image.copy()
        self.n_width = self.img.shape[1]
        self.n_height = self.img.shape[0]
        #self.font=cv2.InitFont(cv2.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 1, 0, 3, 8)
        self.method = method 

        self.para1len = 68
        if method == 4:
            self.para1len=22
            self.method=2
        self.para2len = 5   #  7
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.paraPt1=[[],[]]   #  sixty_eight      method 2
        self.paraPt2=[[],[]]    #seven  fourteen      method 1
       
        self.scaleNum = scaleNum
        if self.scaleNum>1.4 or self.scaleNum < 1.001:
            self.scaleNum=1.06
        self.drawing = False  
        self.ix ,self.iy = 0, 0
        self.changeFlag = False
        self.changeIndex1 = -1
        self.changeIndex2 = -1
    def draw_circle(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN and flags != 9:
            if self.changeFlag :
                self.changeFlag=False
                if self.changeIndex2 != -1:
                    self.paraPt2[0][self.changeIndex2]=x
                    self.paraPt2[1][self.changeIndex2]=y
                    self.changeIndex2 =-1
                elif self.changeIndex1 != -1:
                    self.paraPt1[0][self.changeIndex1]=x
                    self.paraPt1[1][self.changeIndex1]=y
                    self.changeIndex1 = -1
                self.img =self.imgori.copy()
                self.plotImg()
            else:
                if self.method == 1:
                    if(len(self.paraPt2[0]) < self.para2len):
                        self.paraPt2[0].append(x)
                        self.paraPt2[1].append(y)
                        numDot=len(self.paraPt2[0])
                        cv2.circle(self.img,(x,y),2,(0,0,255),-1)
                        cv2.putText(self.img, str(numDot), (x,y), self.font,0.5, (255,255,0),1)
                       
                    else:
                        pass
                        #cv2.putText(self.img, 'over range of seven', (int(self.img.shape[1]/2),int(self.img.shape[0]/2)), self.font,1, (255,255,0),1)
                elif self.method == 2:
                    if(len(self.paraPt1[1])<self.para1len):
                        self.paraPt1[0].append(x)
                        self.paraPt1[1].append(y)
                        numDot=len(self.paraPt1[1])
                        cv2.circle(self.img,(x,y),1,(255,0,255),-1)
                        cv2.putText(self.img, str(numDot), (x,y), self.font,0.4, (255,0,0),1)
                      
                    else:
                        pass
                        #cv2.putText(self.img, 'over range of sixty_eight', (int(self.img.shape[1]/2),int(self.img.shape[0]/2)), self.font,1, (255,0,0),1)
                else:
                    if(len(self.paraPt2[0]) < self.para2len):
                        self.paraPt2[0].append(x)
                        self.paraPt2[1].append(y)
                        numDot=len(self.paraPt2[0])
                        cv2.circle(self.img,(x,y),2,(0,0,255),-1)
                        cv2.putText(self.img, str(numDot), (x,y), self.font,0.5, (255,255,0),1)
                        
                    elif(len(self.paraPt1[1])<self.para1len):
                        self.paraPt1[0].append(x)
                        self.paraPt1[1].append(y)
                        numDot=len(self.paraPt1[1])
                        cv2.circle(self.img,(x,y),1,(255,0,255),-1)
                        cv2.putText(self.img, str(numDot), (x,y), self.font,0.4, (255,0,0),1)
                        
                    else:
                        pass
                        #cv2.putText(self.img, 'over range of all', (int(self.img.shape[1]/2),int(self.img.shape[0]/2)), self.font,1, (0,0,255),1)
            cv2.imshow('Face_big',self.img)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False                  #drawimg
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (255, 255,255), 1)
                cv2.imshow('Face', self.img)         
        elif event == cv2.EVENT_LBUTTONDOWN and flags == 9:
            len1 = len(self.paraPt1[0])
            len2 = len(self.paraPt2[0])
            tempIndex1 = -1
            tempIndex2 = -1
            tempIndex3 = -1
            tempIndex4 = -1
            step1 = 6
            step2 = 12
            if self.changeFlag==False:
                for i in range(len2):
                    if self.paraPt2[0][i]==x and self.paraPt2[1][i]==y:
                        self.changeFlag = True
                        self.changeIndex2 = i
                        self.paraPt2[0][i]=0
                        self.paraPt2[1][i]=0
                        break
                    if (x-step1)<self.paraPt2[0][i] and (x+step1)>self.paraPt2[0][i] and \
                            self.paraPt2[1][i]<(y+step1) and self.paraPt2[1][i]>(y-step1):
                            if tempIndex1 != -1: #and tempIndex2 ==-1
                                tempIndex2 = i
                            if tempIndex1 == -1:
                                tempIndex1 = i
                    if (x-step2)<self.paraPt2[0][i] and (x+step2)>self.paraPt2[0][i] and \
                            self.paraPt2[1][i]<(y+step2) and self.paraPt2[1][i]>(y-step2):
                            if tempIndex3 != -1: #and tempIndex2 ==-1
                                tempIndex4 = i
                            if tempIndex3 == -1:
                                tempIndex3 = i

                if self.changeIndex2 == -1 and tempIndex1 !=-1 and tempIndex2==-1:
                    self.changeFlag = True
                    self.changeIndex2 = tempIndex1
                    self.paraPt2[0][tempIndex1]=0
                    self.paraPt2[1][tempIndex1]=0
                if self.method == 1 and self.changeIndex2 == -1 and tempIndex3 !=-1 and tempIndex4==-1:
                    self.changeFlag = True
                    self.changeIndex2 = tempIndex3
                    self.paraPt2[0][tempIndex3]=0
                    self.paraPt2[1][tempIndex3]=0

                if self.changeFlag == False :
                    for i in range(len1):
                        if self.paraPt1[0][i]==x and self.paraPt1[1][i]==y:
                            self.changeFlag = True
                            self.changeIndex1 = i
                            self.paraPt1[0][i]=0
                            self.paraPt1[1][i]=0
                            break
                        if (x-step1)<self.paraPt1[0][i] and (x+step1)>self.paraPt1[0][i] and \
                            self.paraPt1[1][i]<(y+step1) and self.paraPt1[1][i]>(y-step1):
                            if tempIndex1 != -1: #and tempIndex2 ==-1
                                tempIndex2=i
                            if tempIndex1 == -1:
                                tempIndex1=i
                        if (x-step2)<self.paraPt1[0][i] and (x+step2)>self.paraPt1[0][i] and \
                            self.paraPt1[1][i]<(y+step2) and self.paraPt1[1][i]>(y-step2):
                            if tempIndex3 != -1: #and tempIndex2 ==-1
                                tempIndex4 = i
                            if tempIndex3 == -1:
                                tempIndex3 = i
                            
                if self.changeIndex2 == -1 and self.changeIndex1 == -1 and tempIndex1 !=-1 and tempIndex2==-1:
                    self.changeFlag = True
                    self.changeIndex1 = tempIndex1
                    self.paraPt1[0][tempIndex1]=0
                    self.paraPt1[1][tempIndex1]=0
                if self.changeIndex2 == -1 and self.changeIndex1 == -1 and tempIndex3 !=-1 and tempIndex4==-1:
                    self.changeFlag = True
                    self.changeIndex1 = tempIndex3
                    self.paraPt1[0][tempIndex3]=0
                    self.paraPt1[1][tempIndex3]=0
                if self.changeFlag:
                    self.img =self.imgori.copy()
                    self.plotImg()
                    cv2.imshow('Face_big',self.img)
        elif event == cv2.EVENT_MOUSEMOVE:
            tempImg = self.img.copy()
            loc = '('+ str(x)+','+str(y)+')'
            cv2.circle(tempImg,(x,y),1,(255,0,0),-1)
            cv2.putText(tempImg, loc, (x,y), self.font,0.6, (0,255,0),1)
            #cv2.rectangle(self.img,(self.ix,self.iy),(x,y),(0,255,0),0)
            cv2.imshow('Face_big',tempImg)
       
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.changeFlag == False:
                countNum = len(self.paraPt2[0])+len(self.paraPt1[0])
                if countNum>0:
                  
                    if self.method == 1:
                        numDot = len(self.paraPt2[0])
                        del self.paraPt2[0][numDot-1]
                        del self.paraPt2[1][numDot-1]
                        self.img =self.imgori.copy()
                        for i in range(0,(numDot-1)):
                            cv2.circle(self.img,(self.paraPt2[0][i],self.paraPt2[1][i]),2,(0,0,255),-1)
                            cv2.putText(self.img, str(i+1), (self.paraPt2[0][i],self.paraPt2[1][i]),self.font,0.5, (255,255,0),1)
                    elif self.method == 2:
                        numDot = len(self.paraPt1[1])
                        del self.paraPt1[0][numDot-1]
                        del self.paraPt1[1][numDot-1]
                        self.img =self.imgori.copy()
                        for i in range(0,numDot-1):
                            cv2.circle(self.img,(self.paraPt1[0][i],self.paraPt1[1][i]),1,(255,0,255),-1)
                            cv2.putText(self.img, str(i+1), (self.paraPt1[0][i],self.paraPt1[1][i]),self.font,0.4, (255,0,0),1)
                    else:
                        if len(self.paraPt1[0]) :
                            numDot = len(self.paraPt1[1])
                            del self.paraPt1[0][numDot-1]
                            del self.paraPt1[1][numDot-1]
                            self.img =self.imgori.copy()
                            for i in range(0,self.para2len):
                                cv2.circle(self.img,(self.paraPt2[0][i],self.paraPt2[1][i]),2,(0,0,255),-1)
                                cv2.putText(self.img, str(i+1), (self.paraPt2[0][i],self.paraPt2[1][i]),self.font,0.5, (255,255,0),1)
                            for i in range(0,(numDot-1)):
                                cv2.circle(self.img,(self.paraPt1[0][i],self.paraPt1[1][i]),1,(255,0,255),-1)
                                cv2.putText(self.img, str(i+1), (self.paraPt1[0][i],self.paraPt1[1][i]),self.font,0.4, (255,0,0),1)
                        elif len(self.paraPt2[0]):
                            numDot = len(self.paraPt2[0])
                            del self.paraPt2[0][numDot-1]
                            del self.paraPt2[1][numDot-1]
                            self.img =self.imgori.copy()
                            for i in range((numDot-1)):
                                cv2.circle(self.img,(self.paraPt2[0][i],self.paraPt2[1][i]),2,(0,0,255),-1)
                                cv2.putText(self.img, str(i+1), (self.paraPt2[0][i],self.paraPt2[1][i]),self.font,0.5, (255,255,0),1)
              
                #cv2.putText(self.img, 'num is zero', (int(self.img.shape[1]/2),int(self.img.shape[0]/2)), self.font,1, (0,0,255),1)
            cv2.imshow('Face_big',self.img)
    def plotImg(self):
        if self.method ==1:
            for i in range(len(self.paraPt2[0])):
                cv2.circle(self.img,(self.paraPt2[0][i],self.paraPt2[1][i]),2,(0,0,255),-1)
                cv2.putText(self.img, str(i+1), (self.paraPt2[0][i],self.paraPt2[1][i]),self.font,0.5, (255,255,0),1)
        elif self.method ==2:
            for i in range(len(self.paraPt1[0])):
                cv2.circle(self.img,(self.paraPt1[0][i],self.paraPt1[1][i]),1,(255,0,255),-1)
                cv2.putText(self.img, str(i+1), (self.paraPt1[0][i],self.paraPt1[1][i]),self.font,0.4, (255,0,0),1)
        else:
            for i in range(len(self.paraPt2[0])):
                cv2.circle(self.img,(self.paraPt2[0][i],self.paraPt2[1][i]),2,(0,0,255),-1)
                cv2.putText(self.img, str(i+1), (self.paraPt2[0][i],self.paraPt2[1][i]),self.font,0.5, (255,255,0),1)
            for i in range(len(self.paraPt1[0])):
                cv2.circle(self.img,(self.paraPt1[0][i],self.paraPt1[1][i]),1,(255,0,255),-1)
                cv2.putText(self.img, str(i+1), (self.paraPt1[0][i],self.paraPt1[1][i]),self.font,0.4, (255,0,0),1)

    def setPara(self,parafive,para1):
        if parafive != None or para1 != None:
            for i in range(len(parafive[0])):
                self.paraPt2[0].append(int(parafive[0][i]))
                self.paraPt2[1].append(int(parafive[1][i]))
            for i in range(len(para1[0])):
                self.paraPt1[0].append(int(para1[0][i]))
                self.paraPt1[1].append(int(para1[1][i]))
            if(len(parafive[0])==0 and len(para1[0])==0 ):
                self.readDot()
        else:
            self.readDot()
           
    def readDot(self):
        f=open('.\\modleData\\modleDot.txt','r')
        for index, line in enumerate(f.readlines()):
            #strf =f.readline()
            listf =[]
            if line != '':
                listf = line.split()  #default ' ' '\n' '\t'
            lenf = len(listf)
            if self.method == 1:
                if lenf ==self.para2len*2:
                    for i in range(self.para2len):
                        self.paraPt2[0].append(int(listf[2*i]))
                        self.paraPt2[1].append(int(listf[2*i+1]))
            elif self.method ==2:
                if lenf ==self.para1len*2:
                    for i in range(self.para1len):
                        self.paraPt1[0].append(int(listf[2*i]))
                        self.paraPt1[1].append(int(listf[2*i+1]))
            else:
                if lenf ==self.para2len*2:
                    for i in range(self.para2len):
                        self.paraPt2[0].append(int(listf[2*i]))
                        self.paraPt2[1].append(int(listf[2*i+1]))
                if lenf ==self.para1len*2:
                    for i in range(self.para1len):
                        self.paraPt1[0].append(int(listf[2*i]))
                        self.paraPt1[1].append(int(listf[2*i+1]))
        f.close()


    def moveDirect(self,mark):
        if self.method == 1:
            len2 = len(self.paraPt2[0])
            if len2<1:
                return 0
            nminx2 = min(self.paraPt2[0])
            nminy2 = min(self.paraPt2[1])
            nmaxx2 = max(self.paraPt2[0])
            nmaxy2 = max(self.paraPt2[1])
            if mark == 1: #up
                if nminy2>0:
                    for i in range(len2):
                        self.paraPt2[1][i] -=1
                else:
                    return 0
            elif mark == 2:#down
                if nmaxy2 < self.n_height:
                    for i in  range(len2):
                            self.paraPt2[1][i] +=1
                else:
                    return 0
            elif mark == 3:#left
                if nminx2>0:
                    for i in range(len2):
                        self.paraPt2[0][i] -=1
                else:
                    return 0
            elif mark == 4:#right
                if nmaxx2<self.n_width:
                    for i in range(len2):
                        self.paraPt2[0][i] +=1
                else:
                    return 0
        elif self.method ==2:
            len1 = len(self.paraPt1[0])
            if len1<1:
                return 0
            nminx1 = min(self.paraPt1[0])
            nminy1 = min(self.paraPt1[1])
            nmaxx1 = max(self.paraPt1[0])
            nmaxy1 = max(self.paraPt1[1])
            if mark == 1: #up
                if nminy1>0:
                    for i in range(len1):
                        self.paraPt1[1][i] -=1
                else:
                    return 0
            elif mark == 2:#down
                if nmaxy1<self.n_height:
                    for i in range(len1):
                        self.paraPt1[1][i] +=1
                else:
                    return 0
            elif mark == 3:#left
                if nminx1>0:
                    for i in range(len1):
                        self.paraPt1[0][i] -=1
                else:
                    return 0

            elif mark == 4:#right
                if nmaxx1<self.n_width:
                    for i in range(len1):
                        self.paraPt1[0][i] +=1
                else:
                    return 0
        else:
            len2 = len(self.paraPt2[0])
            if len2<1:
                return 0
            len1 = len(self.paraPt1[0])
        
            nminx2 = min(self.paraPt2[0])
            nminy2 = min(self.paraPt2[1])
            nmaxx2 = max(self.paraPt2[0])
            nmaxy2 = max(self.paraPt2[1])
            nminx1 = 1
            nminy1 = 1
            nmaxx1 = 1
            nmaxy1 = 1
            if len1>0:
                nminx1 = min(self.paraPt1[0])
                nminy1 = min(self.paraPt1[1])
                nmaxx1 = max(self.paraPt1[0])
                nmaxy1 = max(self.paraPt1[1])
            if mark == 1: #up
                if nminy2>0 and nminy1>0:
                    for i in range(len2):
                        self.paraPt2[1][i] -=1
                    for i in range(len1):
                        self.paraPt1[1][i] -=1
                else:
                    return 0
            elif mark == 2:#down
                if nmaxy2 < self.n_height and nmaxy1 < self.n_height:
                    for i in  range(len2):
                            self.paraPt2[1][i] +=1
                    for i in  range(len1):
                            self.paraPt1[1][i] +=1
                else:
                    return 0
            elif mark == 3:#left
                if nminx2>0 and  nminx1>0:
                    for i in range(len2):
                        self.paraPt2[0][i] -=1
                    for i in range(len1):
                        self.paraPt1[0][i] -=1
                else:
                    return 0
            elif mark == 4:#right
                if nmaxx2<self.n_width and nmaxx1<self.n_width:
                    for i in range(len2):
                        self.paraPt2[0][i] +=1
                    for i in range(len1):
                        self.paraPt1[0][i] +=1
                else:
                    return 0
    def amplifcationImg(self,flag):
        scale= self.scaleNum
        len2 = len(self.paraPt2[0])
        if len2<1:
            return 0
        if flag == 1:
            nmaxx2 = max(self.paraPt2[0])
            if int(nmaxx2*scale)> self.n_width-1:
                return
            for i in range(len2):
                self.paraPt2[0][i]= int(self.paraPt2[0][i]*scale)
            len1 = len(self.paraPt1[0])
            nmaxx1 = 1
            if len1>0:
                nmaxx1 = max(self.paraPt1[0])
                if int(nmaxx1*scale)> self.n_width-1:
                    return
                for i in range(len1):
                    self.paraPt1[0][i]= int(self.paraPt1[0][i]*scale)
        elif flag ==2:
            nmaxy2 = max(self.paraPt2[1])
            if int (nmaxy2*scale)>self.n_height-1: 
                return
            for i in range(len2):
                self.paraPt2[1][i]= int(self.paraPt2[1][i]*scale)
            len1 = len(self.paraPt1[1])
            nmaxy1 = 1
            if len1>0:
                nmaxy1 = max(self.paraPt1[1])
                if int (nmaxy1*scale)>self.n_height-1: 
                    return
                for i in range(len1):
                    self.paraPt1[1][i]= int(self.paraPt1[1][i]*scale)
        else:     
            #nminx2 = min(self.paraPt2[0])
            #nminy2 = min(self.paraPt2[1])
            nmaxx2 = max(self.paraPt2[0])
            nmaxy2 = max(self.paraPt2[1])
            if int(nmaxx2*scale)> self.n_width-1:
                return
            if int (nmaxy2*scale)>self.n_height-1: 
                return
            for i in range(len2):
                self.paraPt2[0][i]= int(self.paraPt2[0][i]*scale)
                self.paraPt2[1][i]= int(self.paraPt2[1][i]*scale)
            len1 = len(self.paraPt1[0])
            #nminx1 = 1
            #nminy1 = 1
            nmaxx1 = 1
            nmaxy1 = 1
            if len1>0:
                #nminx1 = min(self.paraPt1[0])
                #nminy1 = min(self.paraPt1[1])
                nmaxx1 = max(self.paraPt1[0])
                nmaxy1 = max(self.paraPt1[1])
                if int(nmaxx1*scale)> self.n_width-1:
                    return
                if int (nmaxy1*scale)>self.n_height-1: 
                    return
                for i in range(len1):
                    self.paraPt1[0][i]= int(self.paraPt1[0][i]*scale)
                    self.paraPt1[1][i]= int(self.paraPt1[1][i]*scale)

    def shrinkImg(self,flag):
        scale= self.scaleNum
        len2 = len(self.paraPt2[0])
        if len2<1:
            return 0
        if flag == 1:
            nminx2 = min(self.paraPt2[0])
            if int(nminx2/scale)< 1:
                return
            for i in range(len2):
                self.paraPt2[0][i]= int(self.paraPt2[0][i]/scale)
            len1 = len(self.paraPt1[0])
            nminx1 = 1
            if len1>0:
                nminx1 = min(self.paraPt1[0])
                if int(nminx1/scale)< 1:
                    return
                for i in range(len1):
                    self.paraPt1[0][i]= int(self.paraPt1[0][i]/scale)
        elif flag ==2:
            nminy2 = min(self.paraPt2[1])
            if int (nminy2/scale)< 1: 
                return
            for i in range(len2):
                self.paraPt2[1][i]= int(self.paraPt2[1][i]/scale)
            len1 = len(self.paraPt1[1])
            nminy1 = 1
            if len1>0:
                nminy1 = min(self.paraPt1[1])
                if int (nminy1/scale)< 1: 
                    return
                for i in range(len1):
                    self.paraPt1[1][i]= int(self.paraPt1[1][i]/scale)
        else:
            nminx2 = min(self.paraPt2[0])
            nminy2 = min(self.paraPt2[1])
            #nmaxx2 = max(self.paraPt2[0])
            #nmaxy2 = max(self.paraPt2[1])
            if int(nminx2/scale)< 1:
                return
            if int (nminy2/scale)< 1: 
                return
            for i in range(len2):
                self.paraPt2[0][i]= int(self.paraPt2[0][i]/scale)
                self.paraPt2[1][i]= int(self.paraPt2[1][i]/scale)
            len1 = len(self.paraPt1[0])
            nminx1 = 1
            nminy1 = 1
            #nmaxx1 = 1
            #nmaxy1 = 1
            if len1>0:
                nminx1 = min(self.paraPt1[0])
                nminy1 = min(self.paraPt1[1])
                #nmaxx1 = max(self.paraPt1[0])
                #nmaxy1 = max(self.paraPt1[1])
                if int(nminx1/scale)< 1:
                    return
                if int (nminy1/scale)< 1: 
                    return
                for i in range(len1):
                    self.paraPt1[0][i]= int(self.paraPt1[0][i]/scale)
                    self.paraPt1[1][i]= int(self.paraPt1[1][i]/scale)

    def drowMouse(self):
        cv2.namedWindow('Face_big',0)
        #cv2.resizeWindow('Face_big',720,858)  #480*1.5  572*1.5
        cv2.setMouseCallback('Face_big',self.draw_circle)
        b = 0
        while(1):
            if b== 0:
                self.plotImg()
                cv2.imshow('Face_big',self.img)
                b=1
            k = cv2.waitKey(1) & 0xFF
            if k == 255:
                continue
            if k == ord('q') : 
                break
            elif k==ord('d'):  
                self.img =self.imgori.copy()
                cv2.imshow('Face_big',self.img)
                del self.paraPt1[0][:]
                del self.paraPt1[1][:]
                del self.paraPt2[0][:]
                del self.paraPt2[1][:]
            elif k == ord('8'): #56  up
                self.img =self.imgori.copy()
                self.moveDirect(1)
                self.plotImg()
                cv2.imshow('Face_big',self.img)
            elif k == ord('2'):# down
                self.img =self.imgori.copy()
                self.moveDirect(2)
                self.plotImg()
                cv2.imshow('Face_big',self.img)
            elif k == ord('4'):  # 52 left
                self.img =self.imgori.copy()
                self.moveDirect(3)
                self.plotImg()
                cv2.imshow('Face_big',self.img)
            elif k == ord('6'):  #54  right
                self.img =self.imgori.copy()
                self.moveDirect(4)
                self.plotImg()
                cv2.imshow('Face_big',self.img)
            elif k ==ord('s'):
                cv2.imwrite('temptest.jpg',self.img)
            elif k == 27: #Esc
                break
            elif k == ord('+'):
                self.img =self.imgori.copy()
                self.amplifcationImg(3)
                self.plotImg()
            elif k == ord('-'):
                self.img =self.imgori.copy()
                self.shrinkImg(3)
                self.plotImg()
            elif k ==ord('v'):
                self.img =self.imgori.copy()
                self.amplifcationImg(1)
                self.plotImg()
            elif k ==ord('b'):
                self.img =self.imgori.copy()
                self.amplifcationImg(2)
                self.plotImg()
            elif k ==ord('n'):
                self.img =self.imgori.copy()
                self.shrinkImg(1)
                self.plotImg()
            elif k ==ord('m'):
                self.img =self.imgori.copy()
                self.shrinkImg(2)
                self.plotImg()

        cv2.destroyAllWindows()
        flag = 0
        if self.method == 1:
            if len(self.paraPt2[0]) == self.para2len:
                flag = 1
                del self.paraPt1[0][:]
                del self.paraPt1[1][:]
      
        elif self.method == 2:
            if len(self.paraPt1[1]) == self.para1len:
                flag = 1
                del self.paraPt2[0][:]
                del self.paraPt2[1][:]
        else:
            if(len(self.paraPt1[1]) == self.para1len):
                flag = 1              
        if flag == 0:
            del self.paraPt1[0][:]
            del self.paraPt1[1][:]
            del self.paraPt2[0][:]
            del self.paraPt2[1][:]
        return  flag ,self.paraPt2, self.paraPt1
               
 


if __name__ == "__main__":
    testpath = './modleData/3.jpg'   #./.temp/3.jpg
    colorImg = cv2.imread(testpath,cv2.IMREAD_COLOR) #cv2.IMREAD_COLOR  cv2.IMREAD_GRAYSCALE
    merged=colorImg  #
    if colorImg is not  None:
        #b = colorImg.copy()-
        #g = colorImg.copy()
        #r = colorImg.copy()
        #merged = cv2.merge([b,g,r])  
        #rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2GRAY)  #
        drowf = getMousePlace(merged,1,1.06)
        drowf.setPara(None,None)
        flag, para1,para2 = drowf.drowMouse()
        if flag:
            print('ok')

