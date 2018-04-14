from utils.Keycodes import keycodes, modifiers
import utils.pytweening as pytweening

class Keys():

    # Modifier key
    modifier = modifiers["Mod1"] # AltLeft as default modifier

    # Commands: mod + command
    mode     = keycodes["Space"] # Toggle mode: Master on the left, master on the top,  master on the right, master on the bottom and floating mode
    incm     = keycodes["."]
    decm     = keycodes[","] # Set next/previous window as master
    expandm  = keycodes["]"]
    shrinkm  = keycodes["["] # Expand or shrink master window area

    # List of keys to track when pressed
    keycodes     = [modifier, mode, incm, decm, expandm, shrinkm]

class Settings():

    # Margins from the edge of the screen
    # Useful when utilizing panels that won't put windows aside
    margin_top    = 0
    margin_bottom = 0
    margin_left   = 0
    margin_right  = 0

    # Useless gap between windows and screen edges
    # Adds to the margins
    gap = 0

    # Moving and resizing speed in seconds
    speed = 0.5

    # Expand/Shrink master area at rate in pixels
    master_resize_rate = 10




    # Easing modes
    easings = {
        # Default linear easing
        "linear":             pytweening.linear,
        # In/Out aliases
        "Quad":      pytweening.easeInOutQuad,
        "Quart":     pytweening.easeInOutQuart,
        "Cubic":     pytweening.easeInOutCubic,
        "Quint":     pytweening.easeInOutQuint,
        "Sine":      pytweening.easeInOutSine,
        "Expo":      pytweening.easeInOutExpo,
        "Back":      pytweening.easeInOutBack,
        "Elastic":   pytweening.easeInOutElastic,
        "Bounce":    pytweening.easeInOutBounce,
        # One-way easings
        "easeInQuad":         pytweening.easeInQuad,
        "easeOutQuad":        pytweening.easeOutQuad,
        "easeInCubic":        pytweening.easeInCubic,
        "easeOutCubic":       pytweening.easeOutCubic,
        "easeInQuart":        pytweening.easeInQuart,
        "easeOutQuart":       pytweening.easeOutQuart,
        "easeInQuint":        pytweening.easeInQuint,
        "easeOutQuint":       pytweening.easeOutQuint,
        "easeInSine":         pytweening.easeInSine,
        "easeOutSine":        pytweening.easeOutSine,
        "easeInExpo":         pytweening.easeInExpo,
        "easeOutExpo":        pytweening.easeOutExpo,
        "easeInCirc":         pytweening.easeInCirc,
        "easeOutCirc":        pytweening.easeOutCirc,
        "easeInOutCirc":      pytweening.easeInOutCirc,
        "easeInElastic":      pytweening.easeInElastic,
        "easeOutElastic":     pytweening.easeOutElastic,
        "easeInBack":         pytweening.easeInBack,
        "easeOutBack":        pytweening.easeOutBack,
        "easeInBounce":       pytweening.easeInBounce,
        "easeOutBounce":      pytweening.easeOutBounce
    }

    easing = easings["linear"]
