import sys
sys.path.append('..')
import math
import os
from time import sleep
from utils import pytweening
from Config import Settings
from datetime import timedelta
from datetime import datetime
from ewmh import EWMH
ewmh = EWMH()

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

    def init(self, display, X_client, x=0, y=0, width=0, height=0):

        self.display = display
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

        command = "wmctrl -i -r " + str(hex(self.client.id)) + " -e 0," +str(self.x) + "," + str(self.y) + "," + str(self.width) + "," + str(self.height)
        os.popen(command)

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

    def set_last_update(self):

        self.lastUpdate = datetime.now()

    def revert(self):

        self.set(self.xoriginal, self.yoriginal, self.woriginal, self.horiginal)

    def debug(self):

        print("--------------")
        print("x: " + str( self.x ) + " next: "  + str(self.xnext))
        print("y: " + str( self.y ) + " next: " + str(self.ynext))
        print("w: " + str( self.width ) + " next: " + str(self.wnext) )
        print("h: " + str( self.height ) + " next: " + str(self.hnext))
        print(self.client)
        print(self.in_place())
        print("--------------")

