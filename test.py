from Config import Keys
from Xlib.display import Display
from Xlib import X

display = Display()
root = display.screen().root

command_mode = False

def handle_event(event):

    keycode = event.detail
    if event.type == X.ButtonPress and keycode == Keys.modifier:
        print("Alt pressed")
        command_mode = True
    if event.type == X.ButtonRelease and keycode == Keys.modifier:
        print("Alt released")
        command_mode = False

    if command_mode:
        print(keycode)

def main():

    root.change_attributes(event_mask = X.KeyPressMask)
    for keycode in Keys.keycodes:
        root.grab_key(keycode, X.AnyModifier, 1, X.GrabModeAsync, X.GrabModeAsync)
    while True:
        event = root.display.next_event()
        handle_event(event)

main()
