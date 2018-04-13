
from Xlib.display import Display
from Xlib import X

alt  = 64
space = 65

keys = [alt,space]

display = Display()
root = display.screen().root

def handle_event(event):
    keycode = event.detail
    print(keycode)

def main():
    root.change_attributes(event_mask = X.KeyPressMask)
    for keycode in keys:
        root.grab_key(keycode, X.AnyModifier, 1, X.GrabModeAsync, X.GrabModeAsync)
    while True:
        event = root.display.next_event()
        handle_event(event)

main()
