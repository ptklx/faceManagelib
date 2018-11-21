#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
import os
import numpy as np
import cv2


class testShowImg():
    def __init__(self, path ,width, height):
        self.path = path
        self.oripath = ''
        self.bbxy=[[],[]]
        self.feature = 'featureDot_'
        self.personNum = 0
        self.path_list= []
        self.width = width
        self.height = height
        self.lastpath =''
    def searchFile(self,num):
        files = os.listdir(self.path)
        files = sorted(files)
        flagc = 1
        for fi in files:
            if(fi.find(num)) != -1:
                flagc=0
            if flagc:
                continue
            fi_d = os.path.join(self.path,fi)
            #if os.path.exists(fi_d):
            #dirflag = os.path.isdir(fi_d)
            if os.path.isfile(fi_d):
                if fi.find(self.feature) != -1:
                    self.path_list.append(fi_d)
        self.personNum= len(self.path_list)

    def whileFile(self):
        cv2.namedWindow('personOneFace')
        for i in range(self.personNum):
             if self.getOnePersonbb(self.path_list[i])== 0:
                break
        cv2.destroyAllWindows()

    def getOnePersonbb(self,inpath):
        print(inpath)
        f=open(inpath,'r')
        #dirpaht = os.path.dirname(inpaht)
        [dirname,filename] = os.path.split(inpath)
        dirname =  dirname +'\\test'  #'V:\\NIR_ALL_480x572labeltxt' #
        if not os.path.exists(dirname):                   #判断是否存在文件夹如果不存在则创建为文件夹  
            os.makedirs(dirname) 
        print(dirname+'\\'+filename)
        f1 = open(dirname+'\\'+filename,'w')  
        n = 0
        for index, line in enumerate(f.readlines()):
            
            #strf =f.readline()
            listf =[]  
            if line != '':
                listf = line.split()  #default ' ' '\n' '\t'
            lenf = len(listf)
            if lenf>0:
                oripath = listf[0]
                if self.lastpath== oripath:
                    continue
                self.lastpath = oripath
            else: 
                continue
            del listf[0]
            #if not(lenf ==11 or lenf ==45 or lenf ==15 or lenf == 137 or lenf == 147 or lenf ==151):
                #continue
            #bbloc[[],[]]
            for i in range(int((lenf-1)/2)):
                    if listf[2*i].isdigit() and listf[2*i+1].isdigit():
                        self.bbxy[0].append(int(listf[2*i]))
                        self.bbxy[1].append(int(listf[2*i+1]))
                    else:
                        break
            self.showimg(oripath)
            time = cv2.getTickCount()
            flag =True
            while(1):
                Time = (cv2.getTickCount() - time )/(cv2.getTickFrequency())
                #if(Time>20):
                    #break 
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q') or k ==27:   #Esc
                    f1.close()
                    f.close()
                    return 0
                elif k>45 and k <58:  #not save
                    flag =False
                    break
                elif k <255:
                    break
            del self.bbxy[0][:]
            del self.bbxy[1][:]
            if flag:
                f1.write(oripath)
                for i in range(int((lenf-1)/2)) :
                    f1.write(' %s %s' %(listf[2*i], listf[2*i+1]))
                f1.write('\n')  
        f.close()
        f1.close()
    def drawimg(self,img):
        for i in range(len(self.bbxy[0])):   #eye left 36_39  right 42_45   nose  31_35  27_30  eye brow left 17 _ 21 right 22_26 
            if len(self.bbxy[0])<8:
                cv2.circle(img,(self.bbxy[0][i],self.bbxy[1][i]),2,(0,255,255),-1)
                cv2.putText(img,"%d"%(i+1),(self.bbxy[0][i],self.bbxy[1][i]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
            elif len(self.bbxy[0])<69:
                cv2.circle(img,(self.bbxy[0][i],self.bbxy[1][i]),1,(0,0,255),-1)
                cv2.putText(img,"%d"%(i+1),(self.bbxy[0][i],self.bbxy[1][i]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,0,0))    
            else:
                if i<7:
                    cv2.circle(img,(self.bbxy[0][i],self.bbxy[1][i]),2,(0,255,255),-1)
                    cv2.putText(img,"%d"%(i+1),(self.bbxy[0][i],self.bbxy[1][i]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                else: 
                    cv2.circle(img,(self.bbxy[0][i],self.bbxy[1][i]),1,(0,0,255),-1)
                    cv2.putText(img,"%d"%(i+1),(self.bbxy[0][i],self.bbxy[1][i]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,0,0))  

        return img
    def showimg(self,inpathlist):
        #inpathlist= 'V'+ inpathlist[1:]
        #inpathlist = self.path[0:1]+inpathlist[1:]
       
        print(inpathlist)
        if os.path.splitext(inpathlist)[1] =='.bin':  #temp 2018 08 02
                img = xyshow(inpathlist,480,640)
        else:
            img = cv2.imread(inpathlist,cv2.IMREAD_COLOR) #cv2.IMREAD_GRAYSCALE
        
        if img is None: 
            return 0
        img = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_LINEAR) 
        img = self.drawimg(img)
        if img is None:
            return 0
        cv2.imshow("personOneFace",img)
        #cv2.waitKey(0)
def xyshow(filename, nx, nz):
    data = np.fromfile(filename,np.uint8)
    img = data.reshape(nz,nx)
    '''
    f = open(path, "rb")
    pic=np.zeros((nz,nx),np.uint8)
    for i in range(nz):
        for j in range(nx):
            data1 = f.read(1)
            pic[i][j]=ord(data1)
    f.close()
    '''
    return img


if __name__ == "__main__":
    testpath = 'V:\\NIR_ALLlabeltxt\\sixtyeight'   
    testImg = testShowImg(testpath,480,572) 
    testImg.searchFile()
    testImg.whileFile()



