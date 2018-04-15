from Xlib.display import Display
from Xlib.ext.xtest import fake_input
from Xlib import X
from ewmh import EWMH
import os
from Config import Keys
import classes.Window as Window
import classes.Workspace as Workspace

NewWorkspace = Workspace.Workspace

ewmh = EWMH()
display = Display()
root = display.screen().root

BUTTON_PRESS    = 2

desktop_number = 0
desktops = []
keycodes = [Keys.mode, Keys.shrinkm, Keys.expandm, Keys.decm, Keys.incm]

def current_desktop():

    for desktop in desktops:
        if desktop["number"] == desktop_number:
            return desktop

def add_desktop_if_new():

    global desktop_number
    desktop_number = ewmh.getCurrentDesktop()
    if not current_desktop():
        wrapper = {
            "number": desktop_number,
            "workspace": NewWorkspace()
        }
        desktops.append(wrapper)

def update_desktops():

    add_desktop_if_new()
    desktop = current_desktop()
    windows = []
    for window in ewmh.getClientList():
        if ewmh.getWmDesktop(window) == desktop_number:
            windows.append(window)
    desktop["workspace"].allign_windows(windows)

def handle_event(event):

    desktop = current_desktop()
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
    update_desktops()

def main():

    grab_keycodes()
    while True:
        update()


main()
