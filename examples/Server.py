from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import numpy as np



import socket
import json

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

import SimpleHTTPServer
import SocketServer
import threading
#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from threading import Thread
PORT_NUMBER = 8080


KEEP_RUNNING= True

def ServerThread(server,ServerConnectionInst):
    #while keep_running():
    while ServerConnectionInst.Running:
        server.handle_request();


def MessagingThread(Frame,ComClass):
    ComClass.setRGBImage(Frame);


def dumbthread(myHandler):
    count = 1;
    while(1):
        count = count +1;
        myHandler.s = str(count);

def keep_running():
    return KEEP_RUNNING


"""
This class will form the string that is represented on the page

"""
class Communication():

    def __init__(self,RGBwidth=3840,RGBheight=2160,DepthWidth=512,DepthHeight=424):
        self.RGBwidth = RGBwidth
        self.RGBheight = RGBheight
        self.DepthWidth = DepthWidth
        self.DepthHeight = DepthHeight
    RGB_image = [];
    Depth_image = [];
    Skeleton_image = [];
    infrared_image = [];

    def setRGBImage(self,RGB):
        #print RGB.tobytes()
        #RGB_str = str(unicode(str(RGB),errors='replace'))
        self.RGB_image = RGB.tolist()
                     
    def getMessage(self):
        m = json.dumps({'RGBWidth':self.RGBwidth, 'RGBHeight': self.RGBheight,
                        'DepthWidht': self.DepthWidth,'DepthHeight': self.DepthHeight,
                        'Image': self.RGB_image, 'Depth': self.Depth_image})
   
        return m;
   

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    s = "Hallo welt";
    RGBmessage = []
    Depthmessage = []
    RGB = [];
          
          
    @staticmethod
    def updateMessage(self,ComClass):
        s = '{"type": "Kinect v2",\n + "RGBwidht":' + str(ComClass.RGBwidth) + "\n" +'"RGBImage":' + str(self.message) + '\n' +'}'
        self.message = s;
        print(s)
          
    def myHandler(self,string):
        self.s = string;
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(self.Depthmessage)
        self.wfile.write(self.s)
   #     self.wfile.write(self.img.tolist())
        if type(self.RGBmessage) is list or type(self.RGBmessage) is str:
            self.wfile.write(self.RGBmessage)    
        else:
            self.wfile.write(self.RGBmessage)
    
        
        return
    
    def rewrite(self,disp):
        self.s = disp;

class ServerConnection():
    Running = True;
    
    def lock(self):
        self.Running = False;
    def open(self):
        self.Running = True;
    
    def getlock():
        return Running;
    
# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]


class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Infrared)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        print(frame.size)
        del address
        target_surface.unlock()

    def run(self):
        # -------- Main Program Loop -----------
        server = HTTPServer((socket.gethostbyname(socket.gethostname()), PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        ServerConnectionInst = ServerConnection();
  
        process = Thread(target=ServerThread,args=[server,ServerConnectionInst])
        process.start();
                     
                     
                     
        ComClass = Communication(3840,2160);
        cnt = 0;
        while not self._done:
            # --- Main event loop
           # server = HTTPServer((socket.gethostbyname(socket.gethostname()), 8080), myHandler)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop
                    ServerConnectionInst.lock();
                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
 
            try:
               # --- Getting frames and drawing  
                # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
                if self._kinect.has_new_color_frame():
                    frame = self._kinect.get_last_color_frame()
                    self.draw_color_frame(frame, self._frame_surface)
                    tempRGB = ['{"type": "Kinect v2", "RGBWidth": ' + str(ComClass.RGBwidth) + '"RGBHeight": ' + str(ComClass.RGBheight) +'"RGBImage":']
                    #delete alpha channel
                    frame = np.delete(frame,np.arange(4,frame.size,4))
                    myHandler.RGBmessage = tempRGB + frame.tolist();#frame.tolist()
                    frame = None;
                if self._kinect.has_new_depth_frame():
     
                    depthframe = self._kinect.get_last_depth_frame();
                    tempDEPTH = ['"DepthWidth": ' + str(ComClass.DepthWidth) + '"DepthHeight": ' + str(ComClass.DepthHeight) +'"DepthImage":']
                    myHandler.Depthmessage = tempDEPTH + depthframe.tolist()

                    
                # --- Cool! We have a body frame, so can get skeletons
                if self._kinect.has_new_body_frame(): 
                    self._bodies = self._kinect.get_last_body_frame()
                    print self._bodies.bodies.all()
                # --- draw skeletons to _frame_surface
                if self._bodies is not None: 
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 
                        
                        joints = body.joints 
                        # convert joint coordinates to color space 
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                        self.draw_body(joints, joint_points, SKELETON_COLORS[i])
    
                # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
                # --- (screen size may be different from Kinect's color frame size) 
                h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
                target_height = int(h_to_w * self._screen.get_width())
                surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
                self._screen.blit(surface_to_draw, (0,0))
                surface_to_draw = None
                pygame.display.update()
    
                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()
    
                # --- Limit to 60 frames per second
                self._clock.tick(120)
            except KeyboardInterrupt:
                self._done = True
                ServerConnectionInst.lock();
        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()
        
        process.join(0.00000001);
     #   process.terminate();


__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();

