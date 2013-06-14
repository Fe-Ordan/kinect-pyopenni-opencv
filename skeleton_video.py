#!/usr/bin/python
# -*- coding: utf-8 -*- 
from openni import *
import cv2.cv as cv

pose_to_use = 'Psi'

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
imagem_binaria = cv.CreateImage((640,480), 8, 1)
cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Binária',1)
cv.MoveWindow('Binária',720,0)

ctx = Context()
ctx.init()
ctx.open_file_recording("MeuVideo.oni")

video = ctx.find_existing_node(NODE_TYPE_IMAGE)
depth = ctx.find_existing_node(NODE_TYPE_DEPTH)

user = UserGenerator()
user.create(ctx)

skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap

# Declare the callbacks
def new_user(src, id):
    print "1/4 User {} detected. Looking for pose..." .format(id)

    pose_cap.start_detection(pose_to_use, id)

def pose_detected(src, pose, id):
    print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
    pose_cap.stop_detection(id)
    skel_cap.request_calibration(id, True)

def calibration_start(src, id):
    print "3/4 Calibration started for user {}." .format(id)

def calibration_complete(src, id, status):
    if status == CALIBRATION_STATUS_OK:
        print "4/4 User {} calibrated successfully! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)

def lost_user(src, id):
    print "--- User {} lost." .format(id)

# Register them
user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)

# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
ctx.start_generating_all()


def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    cv.ShowImage('Video', imagem_cv)

tecla = -1
while (tecla < 0):
    ctx.wait_one_update_all(video)
    imagem = video.get_raw_image_map_bgr()
    processa_frame(imagem)
    #cv.ShowImage('Binária', imagem_binaria)

    # Extract head position of each tracked user
    for id in user.users:
        if skel_cap.is_tracking(id):
            head = skel_cap.get_joint_position(id, SKEL_HEAD)
            print "  {}: head at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=head.point, conf=head.confidence)
    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()
