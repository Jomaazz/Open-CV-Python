#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Copyright 2017 Andreas PUSCH. All rights reserved.
'''

import sys
import cv2
import numpy as np

if __name__ == '__main__':
    # some default values ...
    cam_ID = 0
    video_width, video_height = 640, 480 # OpenCV default

    # camera ID
    if len(sys.argv) >= 2:
        cam_ID = int(sys.argv[1])
    
    # video resolution
    if len(sys.argv) == 4:
        video_width, video_height = int(sys.argv[2]), int(sys.argv[3])
        
    # open connexion to video camera
    cap = cv2.VideoCapture(cam_ID)
    # cap = cv2.VideoCapture("multiproj.mov")
    
    if not cap.isOpened():
        print "No camera found."
        sys.exit(0)
    else:
        # set video capturing resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)
        print "Video resolution:",\
            cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # general information about optional parameters
        print "Optional parameters: [cam_ID [video_width video_height]]"  
    
    while(True):
        # capture frame-by-frame
        ret, frame = cap.read()
        
        #patternSize = np.zeros((9,6))
        patternSize = (9,6)
        
        #found, corners = cv2.FindChessboardCorners(frame, patternSize, flags = cv2.CALIB_CB_ADAPTIVE_THRESH)
        found, corners = cv2.findChessboardCorners(frame, patternSize,\
            flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE +\
                    cv2.CALIB_CB_FAST_CHECK)
                    
        if found:
            cv2.Termcriteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
            corners = cv2.cornerSubPix(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), corners,(4, 3),(-1, -1), cv2.Termcriteria)
            cv2.drawChessboardCorners(frame, patternSize, corners, found)
          
          
        # display current frame
        cv2.imshow("Live camera data ...", frame)
        
        key_pressed = cv2.waitKey(1)
        
        if key_pressed in (ord('\x1b'), ord('q')): # quit application
            print "Quit ..."
            break
        
    # when everything done, release pending OpenCV processes
    cap.release()
    cv2.destroyAllWindows()