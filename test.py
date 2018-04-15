from Xlib.display import Display
from Xlib.ext.xtest import fake_input
from Xlib import X
from ewmh import EWMH
import asyncio
import threading
import os
from Config import Keys
import classes.Window as Window
import classes.Workspace as Workspace

class PyTiler():

    NewWorkspace = Workspace.Workspace

    ewmh = EWMH()
    display = Display()
    root = display.screen().root

    BUTTON_PRESS    = 2

    desktop_number = 0
    desktops = []
    keycodes = [Keys.mode, Keys.shrinkm, Keys.expandm, Keys.decm, Keys.incm]

    def current_desktop(self):

        for desktop in self.desktops:
            if desktop["number"] == self.desktop_number:
                return desktop

    def add_desktop_if_new(self):

        self.desktop_number = self.ewmh.getCurrentDesktop()
        if not self.current_desktop():
            wrapper = {
                "number": self.desktop_number,
                "workspace": self.NewWorkspace()
            }
            wrapper["workspace"].init(self.ewmh.getDesktopGeometry()[0], self.ewmh.getDesktopGeometry()[1])
            self.desktops.append(wrapper)

    def update_desktops(self):

        self.add_desktop_if_new()
        desktop = self.current_desktop()
        windows = []
        try:
            for window in self.ewmh.getClientList():
                if self.ewmh.getWmDesktop(window) == self.desktop_number:
                            windows.append(window)
        except(TypeError):
            pass
        desktop["workspace"].allign_windows(windows)
        desktop["workspace"].update()

    def handle_event(self, event):

        workspace = self.current_desktop()["workspace"]
        keycode = event.detail
        if event.type == self.BUTTON_PRESS:
            if keycode == Keys.mode:
                workspace.cycle_layout()
            if keycode == Keys.shrinkm:
                workspace.shrink_master()
            if keycode == Keys.expandm:
                workspace.expand_master()
            if keycode == Keys.incm:
                workspace.increase_master()
            if keycode == Keys.decm:
                workspace.decrease_master()
                workspace.debug()


    def grab_keycodes(self):

        self.root.change_attributes(event_mask = X.KeyPressMask)
        for keycode in self.keycodes:
            self.root.grab_key(keycode, Keys.modifier, 1, X.GrabModeAsync, X.GrabModeAsync)

    def grab_events(self):

        while True:
            event = self.root.display.next_event()
            self.handle_event(event)

    def update(self):

        while True:
            self.update_desktops()
            self.display.flush()


    def main(self):

        self.grab_keycodes()
        update_loop = threading.Thread(name="update_loop", target=self.update)
        grab_events_loop = threading.Thread(name="grab_events_loop", target=self.grab_events)
        update_loop.start()
        grab_events_loop.start()


manager = PyTiler()
manager.main()
