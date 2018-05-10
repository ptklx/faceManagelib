#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scipy import misc
import sys

import os
#import argparse
import tensorflow as tf
import numpy as np
import math
import cv2
import detect_face     #

import dlib
#sys.setrecursionlimit(10**10)  # set the maximum depth as 10的10次方

#import random
#from time import sleep


def to_rgb(img):
    w, h = img.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
    return ret
    
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])
    
def subListDir(filepath):
    path_list=[]
    files = os.listdir(filepath)
    files = sorted(files)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            path_list += subListDir(fi_d)
        else:
            path_list.append(os.path.join(filepath,fi_d))
    return path_list


def parseFile(args):
    output_dir = os.path.expanduser(args.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    leftEye_dir = os.path.join(output_dir, 'leftEye')
    if not os.path.exists(leftEye_dir):
        os.makedirs(leftEye_dir)
    rightEye_dir = os.path.join(output_dir,'rightEye')
    if not os.path.exists(rightEye_dir):
        os.makedirs(rightEye_dir)

    with open(args.input_dir,'r') as f:
        for lines in f.readlines():
            line = lines.split()
            print(line[0])
def getoldLoc():
    f=open('./modleData/lastReadLoc.txt','r')
    strf =f.readline()
    listf =[]
    if strf != '':
        listf= strf.split('_')
    lenf = len(listf)
    f.close()
    if lenf>2:
        personCount = int(listf[1]) if int(listf[1])>0 else 0
        picCount = int(listf[2]) if int(listf[2])>0 else 0
        return personCount ,picCount
    elif lenf>1:
        personCount = int(listf[1]) if int(listf[1])>0 else 0
        return personCount , 0
    return 0 , 0
def setoldLoc(num,locnum):
    f= open('./modleData/lastReadLoc.txt','w')
    f.write(str(0)+'_'+str(num)+'_'+str(locnum))
    f.close()
class MtcnnDlib():
 
    predictor_path = "./modleData/shape_predictor_68_face_landmarks.dat"
    readNumloc = 0   #person num
    readNumpic = 0 # num pic
    text_file = None
    bounding_boxes_filename=''
    def __init__(self, inputPath ,outPath,method,nwidth,nheight):
        self.saveflag1 = 0
        self.saveflag2 = 0
        self.Path = inputPath
        self.minsize = 20 # minimum size of face
        self.method = method
        self.width = nwidth
        self.height = nheight
       
        '''
        if self.method==1:
            try:
                tf.Graph().as_default()
                gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)#args.gpu_memory_fraction
                sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
                try: 
                    sess.as_default()
                    self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess, None)
                except:
                    return 
            except:
                return       
        else:
        '''    
        try:
            tf.Graph().as_default()
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)#args.gpu_memory_fraction
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            try: 
                sess.as_default()
                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess, None)
            except:
                pass
        except:
            pass       
    
        self.landmark_predictor = dlib.shape_predictor(MtcnnDlib.predictor_path)
        self.inputPath = inputPath
        if (outPath!='' and not os.path.exists(outPath)):
            os.makedirs(outPath)
        self.outPath = outPath
        self.imageDirPaths = sorted(os.listdir(self.inputPath))
        self.personNum =len(self.imageDirPaths)
        MtcnnDlib.readNumloc,MtcnnDlib.readNumpic = getoldLoc()   #
        self.firstflag = True
        self.minsize = 20 # minimum size of face
        self.threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
        self.factor = 0.709 # scale factor
        self.bb = np.zeros(4, dtype=np.int32)
        self.eye_bb = np.zeros(10, dtype=np.int32)
        self.shapebb = np.zeros(136,dtype=np.int32)
        #self.shape
    def setMethod(self,mehod):
        self.method = mehod

    def getPersonList(self):
        #for imageDirPath in imageDirPaths:
        if  self.firstflag :
            if MtcnnDlib.readNumloc>self.personNum-1:
                if(MtcnnDlib.text_file!=None):
                    MtcnnDlib.text_file.close()
                return 0,0
            self.firstflag = False
            imageFileDirPath = os.path.join(self.inputPath,self.imageDirPaths[MtcnnDlib.readNumloc])
            self.imagePathList = subListDir(imageFileDirPath)
            self.pathLen = len(self.imagePathList)
            MtcnnDlib.bounding_boxes_filename = os.path.join(self.outPath, 'featureDot_%06d.txt' % MtcnnDlib.readNumloc)
            if(MtcnnDlib.text_file!=None):
                MtcnnDlib.text_file.close()
            MtcnnDlib.text_file = open(MtcnnDlib.bounding_boxes_filename, "a")  #w  a+
            if self.pathLen>0:
                print(self.imagePathList[0])
            return self.pathLen,MtcnnDlib.readNumpic    
        else:    
            MtcnnDlib.readNumloc += 1
            if MtcnnDlib.readNumloc>self.personNum-1:
                if(MtcnnDlib.text_file!=None):
                    MtcnnDlib.text_file.close()
                return 0,0
            MtcnnDlib.readNumpic= 0
            imageFileDirPath = os.path.join(self.inputPath,self.imageDirPaths[MtcnnDlib.readNumloc])
            self.imagePathList = subListDir(imageFileDirPath)
            self.pathLen = len(self.imagePathList)
            MtcnnDlib.bounding_boxes_filename = os.path.join(self.outPath, 'featureDot_%06d.txt' % MtcnnDlib.readNumloc)
            if(MtcnnDlib.text_file!=None):
                MtcnnDlib.text_file.close()
            MtcnnDlib.text_file = open(MtcnnDlib.bounding_boxes_filename, "a")  #w  a+
            setoldLoc(MtcnnDlib.readNumloc,MtcnnDlib.readNumpic)
            if self.pathLen>0:
                print(self.imagePathList[0])
        return self.pathLen,MtcnnDlib.readNumpic

    def closeTxt(self):
        setoldLoc(MtcnnDlib.readNumloc,MtcnnDlib.readNumpic)
        if(MtcnnDlib.text_file!=None):
                MtcnnDlib.text_file.close()
                MtcnnDlib.text_file=None

    def detectFeature(self,mNum,exlight):
        MtcnnDlib.readNumpic = mNum
        self.saveflag1 = 0
        self.saveflag2 = 0
        self.image_path = self.imagePathList[MtcnnDlib.readNumpic]
        if os.path.isfile(self.image_path): #and '0_Light' in image_path:
            """try:
                img = cv2.imread(image_path)
            except (IOError, ValueError, IndexError) as e:
                errorMessage = '{}: {}'.format(image_path, e)
                print(errorMessage)
            else:"""
            img = cv2.imread(self.image_path,cv2.IMREAD_COLOR) #cv2.IMREAD_GRAYSCALE
            if img is None:
                return None
            else:
                flag = 0
                img = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_LINEAR)   #INTER_LINEAR  #INTER_AREA
                imgcopy = img.copy()
                if img.ndim<2:
                    #MtcnnDlib.text_file.write('erro %s\n' % (self.image_path))   ####
                    return img,imgcopy,flag
                if img.ndim == 2:
                    img = to_rgb(img)
                img = img[:,:,0:3]
                if self.method == 1 or self.method == 4:
                    bounding_boxes, points = detect_face.detect_face(img, self.minsize,self.pnet, self.rnet, self.onet, self.threshold, self.factor)
                    nrof_faces = bounding_boxes.shape[0]
                    if nrof_faces>0:
                        det = bounding_boxes[:,0:4]
                        img_size = np.asarray(img.shape)[0:2]
                        if nrof_faces>1:
                            bounding_box_size = (det[:,2]-det[:,0])*(det[:,3]-det[:,1])
                            img_center = img_size / 2
                            offsets = np.vstack([ (det[:,0]+det[:,2])/2-img_center[1], (det[:,1]+det[:,3])/2-img_center[0] ])
                            offset_dist_squared = np.sum(np.power(offsets,2.0),0)
                            index = np.argmax(bounding_box_size-offset_dist_squared*2.0) # some extra weight on the centering
                            det = det[index,:]
                            points = points[:, index]
                            
                        det = np.squeeze(det)
                        points = np.squeeze(points)
                        
                        #self.bb = np.zeros(4, dtype=np.int32)
                        #self.eye_bb = np.zeros(10, dtype=np.int32)
                        
                        self.bb[0] = np.maximum(det[0], 0)
                        self.bb[1] = np.maximum(det[1], 0)
                        self.bb[2] = np.minimum(det[2], img_size[1])
                        self.bb[3] = np.minimum(det[3], img_size[0])
                        for i in range(10):
                            self.eye_bb[i] = points[i]
                        #self.eye_bb =points[0:10]
                        self.saveflag1 = 1
                        flag = 1
                        if self.method ==4:
                            mouthdistance = self.eye_bb[4]-self.eye_bb[3]
                            starty = self.eye_bb[5]-mouthdistance
                            endy = self.eye_bb[8] + mouthdistance
                            startx = self.eye_bb[0]-int(mouthdistance/2)
                            endx = self.eye_bb[1]+int(mouthdistance/2)
                            temimg = img[starty:endy,startx:endx]
                            meanvalue = cv2.mean(temimg)
                            if(meanvalue[0]<exlight):  #85
                                return None, None , 0
                        else:
                            #cv2.circle(img,(self.bb[0],self.bb[1]),2,(0,255,255),-1)
                            #cv2.putText(img,"%d"%(1),(self.bb[0],self.bb[1]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                            #cv2.circle(img,(self.bb[2],self.bb[3]),2,(0,255,255),-1)
                            #cv2.putText(img,"%d"%(2),(self.bb[2],self.bb[3]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                            for kk in range(5):
                                cv2.circle(img,(self.eye_bb[kk],self.eye_bb[kk+5]),2,(0,255,255),-1)
                                cv2.putText(img,"%d"%(kk),(self.eye_bb[kk],self.eye_bb[kk+5]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                    return img,imgcopy,flag
                else:
                    bounding_boxes, points = detect_face.detect_face(img, self.minsize,self.pnet, self.rnet, self.onet, self.threshold, self.factor)
                    nrof_faces = bounding_boxes.shape[0]
                    if nrof_faces>0:
                        det = bounding_boxes[:,0:4]
                        img_size = np.asarray(img.shape)[0:2]
                        if nrof_faces>1:
                            bounding_box_size = (det[:,2]-det[:,0])*(det[:,3]-det[:,1])
                            img_center = img_size / 2
                            offsets = np.vstack([ (det[:,0]+det[:,2])/2-img_center[1], (det[:,1]+det[:,3])/2-img_center[0] ])
                            offset_dist_squared = np.sum(np.power(offsets,2.0),0)
                            index = np.argmax(bounding_box_size-offset_dist_squared*2.0) # some extra weight on the centering
                            det = det[index,:]
                            points = points[:, index]
                        det = np.squeeze(det)
                        points = np.squeeze(points)
                        #self.bb = np.zeros(4, dtype=np.int32)
                        #self.eye_bb = np.zeros(10, dtype=np.int32)

                        self.bb[0] = np.maximum(det[0], 0)
                        self.bb[1] = np.maximum(det[1], 0)
                        self.bb[2] = np.minimum(det[2], img_size[1])
                        self.bb[3] = np.minimum(det[3], img_size[0])
                        for i in range(10):
                            self.eye_bb[i] = points[i]
                        #self.eye_bb =points[0:10]
                        d_nose_xl = (2*self.eye_bb[2]-self.eye_bb[0]-self.eye_bb[3])/2
                        d_nose_xr = (self.eye_bb[1]+self.eye_bb[4]-2*self.eye_bb[2])/2
                        d_nose_yu = (2*self.eye_bb[7]-self.eye_bb[5]-self.eye_bb[6])/2
                        d_nose_yd = (self.eye_bb[8]+self.eye_bb[9]-2*self.eye_bb[7])/2

                        if((d_nose_xl<0) or (d_nose_xr<0) or (d_nose_yu<0) or (d_nose_yd<0)):
                            return img ,imgcopy,flag

                        eyeX = self.eye_bb[0:5]
                        eyeY = self.eye_bb[5:10]
                        eyeDist = math.sqrt((eyeX[0] - eyeX[1])*(eyeX[0] - eyeX[1]) + (eyeY[0] - eyeY[1])*(eyeY[0] - eyeY[1]))
                        #LocalFace
                        localFaceTopLeftX = np.maximum(int(eyeX[0] - 0.6 * eyeDist),0)
                        localFaceTopLeftY = np.maximum(int(eyeY[0] - 0.8 * eyeDist),0)
                        localFaceBottomRightX = np.minimum(int(eyeX[1] + 0.6 * eyeDist),img_size[1])
                        localFaceBottomRightY = np.minimum(int((eyeY[3] + eyeY[4]) / 2.0 + (eyeX[4] - eyeX[3])),img_size[0])
                        rt = dlib.rectangle(int(localFaceTopLeftX),int(localFaceTopLeftY),int(localFaceBottomRightX),int(localFaceBottomRightY))
                        self.shape = self.landmark_predictor(img,rt)
                        for i in range(self.shape.num_parts):
                            self.shapebb[2*i]= self.shape.part(i).x
                            self.shapebb[2*i+1]= self.shape.part(i).y
                        flag = 1
                        if self.method ==2:
                            self.saveflag2 = 1
                            for i in range(self.shape.num_parts):   #eye left 36_39  right 42_45   nose  31_35  27_30  eye brow left 17 _ 21 right 22_26 
                                pt=self.shape.part(i)
                                #plt.plot(pt.x,pt.y,'ro')
                                cv2.circle(img,(pt.x,pt.y),1,(0,0,255),-1)
                                cv2.putText(img,"%d"%(i),(pt.x,pt.y),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,0,0))
                        else:
                            self.saveflag1 = 1
                            self.saveflag2 = 1
                            #cv2.circle(img,(self.bb[0],self.bb[1]),2,(0,255,255),-1)
                            #cv2.putText(img,"%d"%(1),(self.bb[0],self.bb[1]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                            #cv2.circle(img,(self.bb[2],self.bb[3]),2,(0,255,255),-1)
                            #cv2.putText(img,"%d"%(2),(self.bb[2],self.bb[3]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                            for kk in range(5):
                                cv2.circle(img,(self.eye_bb[kk],self.eye_bb[kk+5]),2,(0,255,255),-1)
                                cv2.putText(img,"%d"%(kk),(self.eye_bb[kk],self.eye_bb[kk+5]),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,0))
                            for i in range(self.shape.num_parts):   #eye left 36_39  right 42_45   nose  31_35  27_30  eye brow left 17 _ 21 right 22_26 
                                pt=self.shape.part(i)
                                #plt.plot(pt.x,pt.y,'ro')
                                cv2.circle(img,(pt.x,pt.y),1,(0,0,255),-1)
                                cv2.putText(img,"%d"%(i),(pt.x,pt.y),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,0,0))
                    return img ,imgcopy, flag
                
                    #return 1
        else:
            return None
    def getDatas(self):
        parafive = [[],[]]
        para = [[],[]]
        if self.saveflag1:
                #for i in range(2):
                #parafive[0].append(self.bb[i*2])
                #parafive[1].append(self.bb[i*2+1]) 
                for i in range(5):
                    parafive[0].append(self.eye_bb[i])
                    parafive[1].append(self.eye_bb[i+5])
        if self.saveflag2:
                for i in range(68):
                    para[0].append(self.shapebb[2*i] ) 
                    para[1].append(self.shapebb[2*i+1])
          
        return parafive,para  

    def setCoords(self,flag,parafive,para):
        if flag:
            for i in range(len(parafive[0])):
                #if(i<2):
                #self.bb[i*2] = parafive[0][i] 
                #self.bb[i*2+1] = parafive[1][i]
                #else:
                self.eye_bb[i] = parafive[0][i] 
                self.eye_bb[i+5] = parafive[1][i] 
            for i in range(len(para[0])):
                self.shapebb[2*i] = para[0][i]
                self.shapebb[2*i+1] = para[1][i]
            self.saveflag1 = 1
            self.saveflag2 = 1
        else:
            self.saveflag1 = 0
            self.saveflag2 = 0
    def saveTxt(self ):
        if (MtcnnDlib.bounding_boxes_filename == ''):
            return 0
        if(MtcnnDlib.text_file==None):
            MtcnnDlib.text_file = open(MtcnnDlib.bounding_boxes_filename, "a")  #w  a+

        if self.method ==1 and self.saveflag1:
            MtcnnDlib.text_file.write('%s  %d %d %d %d %d %d %d %d %d %d\n' % (self.image_path,self.eye_bb[0], self.eye_bb[5], 
                                    self.eye_bb[1], self.eye_bb[6], self.eye_bb[2], self.eye_bb[7], self.eye_bb[3], self.eye_bb[8], self.eye_bb[4], self.eye_bb[9]))
            #MtcnnDlib.text_file.write('%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n' % (self.image_path, self.bb[0], self.bb[1], self.bb[2], self.bb[3], 
            #                    self.eye_bb[0], self.eye_bb[5], self.eye_bb[1], self.eye_bb[6], self.eye_bb[2], self.eye_bb[7], self.eye_bb[3], self.eye_bb[8], self.eye_bb[4], self.eye_bb[9]))
            #MtcnnDlib.text_file.write('%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d' % (self.image_path, self.bb[0], self.bb[1], self.bb[2], self.bb[3], 
            #                        self.eye_bb[0], self.eye_bb[1], self.eye_bb[2], self.eye_bb[3], self.eye_bb[4], self.eye_bb[5], self.eye_bb[6], self.eye_bb[7], self.eye_bb[8], self.eye_bb[9]))
        elif self.method ==2 and self.saveflag2:
            MtcnnDlib.text_file.write('%s'%(self.image_path))
            for i in range(68):
                MtcnnDlib.text_file.write(' %d %d' %(self.shapebb[2*i], self.shapebb[2*i+1]))
            MtcnnDlib.text_file.write('\n')
        elif self.method == 4 and self.saveflag1:
            MtcnnDlib.text_file.write('%s'%(self.image_path))
            for i in range(22):
                MtcnnDlib.text_file.write(' %d %d' %(self.shapebb[2*i], self.shapebb[2*i+1]))
            MtcnnDlib.text_file.write('\n') 
        elif self.saveflag1 and self.saveflag2:
            #MtcnnDlib.text_file.write('%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d' % (self.image_path, self.bb[0], self.bb[1], self.bb[2], self.bb[3], 
            #            self.eye_bb[0], self.eye_bb[1], self.eye_bb[2], self.eye_bb[3], self.eye_bb[4], self.eye_bb[5], self.eye_bb[6], self.eye_bb[7], self.eye_bb[8], self.eye_bb[9]))
            MtcnnDlib.text_file.write('%s  %d %d %d %d %d %d %d %d %d %d\n' % (self.image_path,self.eye_bb[0], self.eye_bb[5], 
                                    self.eye_bb[1], self.eye_bb[6], self.eye_bb[2], self.eye_bb[7], self.eye_bb[3], self.eye_bb[8], self.eye_bb[4], self.eye_bb[9]))

            for i in range(68):
                MtcnnDlib.text_file.write(' %d %d' %(self.shapebb[2*i], self.shapebb[2*i+1]))
            MtcnnDlib.text_file.write('\n')            
        else:
            return 0
        return 1  
    def notSave(self):
        self.saveflag1 = 0
        self.saveflag2 = 0

if __name__ == '__main__':
    #mainx(parse_arguments(sys.argv[1:]))
    #V:\\pt_data   test
    tface = MtcnnDlib('V:\\NIR_ALL','H:\\facedetection\\python\\faceImageManage\\pic' ,3,480,640)
    tface.setMethod(1)
    personNum = 0
    nNum = 0
    #str = input('please enter your method: ')
    #print ("Received input is : ", int(str))
    while(1):
        nNum , picnum = tface.getPersonList()
        if nNum == 0: 
            break
        personNum+=1
        print(personNum)
        for i in range(picnum,nNum):
            img,imgcopy,flag = tface.detectFeature(i)
            if img is not  None:
                cv2.imshow("personface",img)
                cv2.waitKey(0)
                tface.saveTxt()
    del tface
   
