import classes.Window as Window
from ewmh import EWMH
from Xlib.display import Display

import time

ewmh = EWMH()

NewWindow = Window.Window

windows = []
try:
    for window in ewmh.getClientList():
        if ewmh.getWmDesktop(window) == 2:
                    windows.append(window)
except(TypeError):
    pass

display = Display()

window = NewWindow()
data = windows[0].get_geometry()
print(data)
window.init(display, windows[0], data.x, data.y, data.width, data.height)
window.debug()
window.set(300, 300, 200, 200)
window.set_last_update()
window.debug()
while True:
    time.sleep(0.1)
    window.update()
    window.debug()

