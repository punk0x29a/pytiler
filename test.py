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
BUTTON_RELEASE  = 3
command_mode    = False

desktops = []

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def update_desktops():

    desktop = ewmh.getCurrentDesktop()
    if len(desktops) == 0 or len(list(filter(lambda x: x["number"] == desktop, desktops))):
        wrapper = {
            "number": desktop,
            "screen": NewScreen()
        }

def handle_event(event):

    global command_mode
    global ewmh
    global root
    global display
    keycode = event.detail
    if event.type == BUTTON_PRESS:
        print(keycode)



def main():

    root.change_attributes(event_mask = X.KeyPressMask)
    for keycode in Keys.keycodes:
        root.grab_key(keycode, Keys.modifier, 1, X.GrabModeAsync, X.GrabModeAsync)
    while True:
        event = root.display.next_event()
        handle_event(event)


for window in ewmh.getClientList():
    dump(window)
    break

main()
