#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scipy import misc
import sys

import os
#import argparse
#import tensorflow as tf
import numpy as np
import math
import cv2

a = np.array([1,2,3,4,5,6])
b = a.reshape(2,3)
c= a.reshape(3,2)

path ='H:\\facedetection\\faceData\\originaldata\\dg\\0000001126\\NonGlass\\l_nc_1_bID_1_frame_1_exposure_73.bin'
data = np.fromfile(path,np.uint8)
img = data.reshape(640,480)

#cv2.imshow('test',img)
#cv2.waitKey(0)
#path ='H:\\facedetection\\faceData\\originaldata\\dg\\0000001126\\NonGlass\\l_nc_1_bID_1_frame_2_exposure_77.bin'
f = open(path, "rb")
pic=np.zeros((640,480),np.uint8)
for i in range(640):
    #pic.append([])
    for j in range(480):
        data1 = f.read(1)
        pic[i][j]=ord(data1)
        #pic[i].append(ord(data1))
f.close()


cv2.imshow('test1',pic)
cv2.waitKey(0)

d =0
