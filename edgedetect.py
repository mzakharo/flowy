from kivy.clock import mainthread
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
import numpy as np
import cv2
from camera4kivy import Preview
import paho.mqtt.publish as publish

class EdgeDetect(Preview):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzed_texture = None
        self.capture = False


    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        # pixels : analyze pixels (bytes)
        # image_size   : analyze pixels size (w,h)
        # image_pos    : location of Texture in Preview (due to letterbox)
        # scale  : scale from Analysis resolution to Preview resolution
        # mirror : true if Preview is mirrored
        if self.capture:
            self.capture = False
            print('torch off', image_size)
            try:
                self.torch('off')
                publish.single("flowy/raw", pixels, hostname="nas.local")
            except Exception as e:
                print(e)

