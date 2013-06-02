#!/usr/bin/python
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Profundidade',1)
cv.MoveWindow('Profundidade',650,0)

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
centro = (0,0)

hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

def gesture_detected(src, gesture, id, end_point):
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    return 

def update(src, id, pos, time):
    global centro
    centro = (int(pos[0]), int(pos[1]))

def destroy(src, id, time):
    return

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    cv.Circle(imagem_cv, centro, 16, cv.CV_RGB(0, 0, 255), 2, cv.CV_AA, 0)
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    ni.wait_any_update_all()
    imagem = video.get_raw_image_map_bgr()
    depth_frame = depth.get_raw_depth_map_8()
    processa_frame(imagem)
    processa_profundidade(depth_frame)

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


