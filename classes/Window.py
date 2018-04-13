import sys
sys.path.append('..')
import math
from time import sleep
from utils import pytweening
from Config import Settings
from datetime import timedelta
from datetime import datetime

speed  = Settings.speed
easing = Settings.easing

class Window():

    microseconds = 1000000 # One second
    client = False
    x=0
    y=0
    xoriginal = 0
    yoriginal = 0
    woriginal = 0
    horiginal = 0
    xlast  = 0
    xnext  = 0
    ylast  = 0
    ynext  = 0
    wnext  = 0
    wlast  = 0
    hlast  = 0
    hnext  = 0
    width  = 0
    height = 0
    delta  = 0
    lastUpdate = datetime.now()

    def init(self, X_client, x=0, y=0, width=0, height=0):

        self.client = X_client
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xoriginal = x
        self.yoriginal = y
        self.woriginal = width
        self.horiginal = height
        self.set(x, y, width, height)

    def set(self, x, y, width, height):

        self.xlast = self.x
        self.ylast = self.y
        self.wlast = self.width
        self.hlast = self.height
        self.xnext = x
        self.ynext = y
        self.wnext = width
        self.hnext = height
        self.lastUpdate = datetime.now()

    def current_value_between(self, origin, target):

        difference = origin - target
        delta = difference * easing(self.delta)
        return origin - math.floor(delta)

    def calculate_coordinates(self):

        self.x = self.current_value_between(self.xlast, self.xnext)
        self.y = self.current_value_between(self.ylast, self.ynext)

    def calculate_size(self):

        self.width  = self.current_value_between(self.wlast, self.wnext)
        self.height = self.current_value_between(self.hlast, self.hnext)

    def set_client(self):
        pass

    def in_place(self):

        return self.x == self.xnext and self.y == self.ynext and self.height == self.hnext and self.width == self.wnext

    def update(self):

        if self.in_place():
            pass
        else:
            now = datetime.now()
            delta = now - self.lastUpdate
            self.delta = (delta.microseconds / self.microseconds) / speed
            if self.delta > 1:
                self.delta = 1
            self.calculate_coordinates()
            self.calculate_size()
            self.set_client()

    def revert(self):
        self.set(self.xoriginal, self.yoriginal, self.woriginal, self.horiginal)

    def debug(self):

        print("--------------")
        print("x: " + str( self.x ))
        print("y: " + str( self.y ))
        print("w: " + str( self.width ))
        print("h: " + str( self.height ))
        print("--------------")

