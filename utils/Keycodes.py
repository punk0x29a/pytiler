from Xlib import X
keycodes = {
"F1":67,
"F2":68,
"F3":69,
"F4":70,
"F5":71,
"F6":72,
"F7":73,
"F8":74,
"F9":75,
"F10":76,
"F11":95,
"F12":96,
# Chars
"`":49,
"1":10,
"2":11,
"3":12,
"4":13,
"5":14,
"6":15,
"7":16,
"8":17,
"9":18,
"0":19,
"-":20,
"=":21,
"Q":24,
"W":25,
"E":26,
"R":27,
"T":28,
"Y":29,
"U":30,
"I":31,
"O":32,
"P":33,
"[":34,
"]":35,
"A":38,
"S":39,
"D":40,
"F":41,
"G":42,
"H":43,
"J":44,
"K":45,
"L":46,
";":47,
"'":48,
"Z":52,
"X":53,
"C":54,
"V":55,
"B":56,
"N":57,
"M":58,
",":59,
".":60,
"/":61,
"\\":51,
# Modifiers
"ShiftRight":62,
"ShiftLeft":50,
"AltLeft":64,
"AltRight":113,
"CtrlLeft":37,
"CtrlRight":109,
"LogoRight":116,
"LogoLeft":115,
# Keypad
"KP0":90,
"KP1":87,
"KP2":88,
"KP3":89,
"KP4":83,
"KP5":84,
"KP6":85,
"KP7":79,
"KP8":80,
"KP9":81,
"KP+":86,
"KP.":91,
"KP/":112,
"KP*":63,
"KP-":82,
"KPReturn":108,
# Arrows
"Up":98,
"Left":100,
"Down":104,
"Right":102,
# Miscellaneous
"Return":36,
"Delete":107,
"End":103,
"Page":105,
"Backspace":22,
"Insert":106,
"Home":97,
"PageUp":99,
"NumLock":77,
"Tab":23,
"Space":65,
"Menu":117,
"International":94,
"CapsLock":66,
"PrintScrn":111,
"ScrollLock":78,
"Pause":110,
"Esc":9,
}

modifiers = {
    "Shift": X.ShiftMask,
    "Control": X.ControlMask,
    "Lock": X.LockMask,
    "Mod1": X.Mod1Mask,
    "Mod2": X.Mod2Mask,
    "Mod3": X.Mod3Mask,
    "Mod4": X.Mod4Mask,
    "Mod5": X.Mod5Mask,
}
