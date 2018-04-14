from Xlib.display import Display
from Xlib.ext.xtest import fake_input
from Xlib import X
from ewmh import EWMH
import os
from Config import Keys
import classes.Window as Window
import classes.Screen as Screen

NewScreen = Screen.Screen
NewWindow = Window.Window

ewmh = EWMH()
display = Display()
root = display.screen().root

BUTTON_PRESS    = 2

desktops = []
keycodes = [Keys.mode, Keys.shrinkm, Keys.expandm, Keys.decm, Keys.incm]

def update_desktops():

    desktop = ewmh.getCurrentDesktop()
    if len(desktops) == 0 or len(list(filter(lambda x: x["number"] == desktop, desktops))):
        wrapper = {
            "number": desktop,
            "screen": NewScreen()
        }

def handle_event(event):

    keycode = event.detail
    if event.type == BUTTON_PRESS:
        if keycode == Keys.mode:
            pass
        if keycode == Keys.shrinkm:
            pass
        if keycode == Keys.expandm:
            pass
        if keycode == Keys.incm:
            pass
        if keycode == Keys.decm:
            pass

def grab_keycodes():

    root.change_attributes(event_mask = X.KeyPressMask)
    for keycode in keycodes:
        root.grab_key(keycode, Keys.modifier, 1, X.GrabModeAsync, X.GrabModeAsync)

def grab_events():

    event = root.display.next_event()
    handle_event(event)

def update():

    grab_events()

def main():

    grab_keycodes()
    while True:
        update()

main()
