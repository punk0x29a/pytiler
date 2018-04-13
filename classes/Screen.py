import sys
sys.path.append('..')
from Config import Settings
import Window

# Margins
mtop    = Settings.margin_top
mbottom = Settings.margin_bottom
mleft   = Settings.margin_left
mright  = Settings.margin_right
gap     = Settings.gap
master_resize_rate = Settings.master_resize_rate

class Screen():

    # Dimensions
    width  = 0
    height = 0

    master_extra_vertical   = 0
    master_extra_horizontal = 0

    # Current master window and present windows list
    master = 0
    windows = []

    # Current layout
    layouts = ["Left", "Right", "Top", "Bottom", "Floating"]
    layout = layouts[0]

    def change_master(self, direction):

        if self.layout == "Left" or self.layout == "Right":
            self.master_extra_horizontal = self.master_extra_horizontal + master_resize_rate * direction
        if self.layout == "Top" or self.layout == "Bottom":
            self.master_extra_vertical = self.master_extra_vertical + master_resize_rate * direction

        if self.master_extra_horizontal < 0:
            self.master_extra_horizontal = 0
        if self.master_extra_vertical < 0:
            self.master_extra_vertical = 0

        if self.master_extra_horizontal > self.width - mleft - mright - 2*gap:
            self.master_extra_horizontal = self.width - mleft - mright - 2*gap
        if self.master_extra_vertical > self.height - mtop - mbottom - 2*gap:
            self.master_extra_vertical = self.height - mtop - mbottom - 2*gap

    def expand_master(self):
        self.change_master(1)

    def shrink_master(self):
        self.change_master(-1)

    def increase_master(self):
        self.master = self.master + 1
        if self.master >= len(self.windows):
            self.master = 0

    def decrease_master(self):
        if len(self.windows) == 0:
            return
        self.master = self.master - 1
        if self.master < 0:
            self.master = 0

    def cycle_layout(self):

        index = self.layouts.index(self.layout)
        index = index + 1
        if index >= len(self.layouts):
            index = 0
        self.layout = self.layouts[index]

    def x_available_space(self):

        return self.width - mleft - mright

    def y_available_space(self):

        return self.height - mtop - mbottom

    def set_floating(self):

        for window in self.windows:
            window.revert()

    def horizontal_tiling_sizes(self):

        master_height = self.y_available_space() - 2*gap
        master_width  = self.x_available_space()/2 + self.master_extra_horizontal - 2*gap
        slaves_width  = master_width - self.master_extra_horizontal
        # Check if other windows are present
        # If not, master takes all the available screen
        try:
            slaves_height = self.y_available_space()/(len(self.windows)-1)
        except(ZeroDivisionError):
            master_width = self.x_available_space() - 2*gap
            slaves_height = 0
        return (master_width, master_height, slaves_width, slaves_height)

    def vertical_tiling_sizes(self):

        master_width = self.x_available_space() - 2*gap
        master_height = self.y_available_space()/2 + self.master_extra_vertical - 2*gap
        slaves_height = master_height - self.master_extra_vertical
        # Check if other windows are present
        # If not, master takes all the available screen
        try:
            slaves_width = self.x_available_space()/(len(self.windows)-1)
        except(ZeroDivisionError):
            master_height = self.y_available_space() - 2*gap
            slaves_width = 0
        return (master_width, master_height, slaves_width, slaves_height)

    def horizontal_tiling_positions(self, sizes, direction):

        master_width = sizes[0]
        if direction > 0:
            xmaster = mleft + gap
        else:
            xmaster = self.width - mright - master_width
        ymaster = mtop + gap
        xslave  = xmaster + master_width * direction + gap * direction
        yslave  = ymaster
        return (xmaster, ymaster, xslave, yslave)

    def vertical_tiling_positions(self, sizes, direction):

        master_height = sizes[1]
        if direction > 0:
            ymaster = mtop + gap
        else:
            ymaster = self.height - master_height - gap
        xmaster = mleft + gap
        xslave = xmaster
        yslave = ymaster + master_height * direction + gap * direction
        return (xmaster, ymaster, xslave, yslave)

    def set_tiling(self, sizes, coordinates, horizontal=True):

        master_width  = sizes[1]
        master_height = sizes[2]
        slaves_width  = sizes[3]
        slaves_height = sizes[4]

        xmaster = coordinates[1]
        ymaster = coordinates[2]
        xslave  = coordinates[3]
        yslave  = coordinates[4]

        for index, window in enumerate(self.windows):
            if index == self.master:
                window.set(xmaster, ymaster, master_width, master_height)
            else:
                window.set(xslave, yslave, slaves_width, slaves_height)
                if horizontal:
                    yslave = yslave + slaves_height + gap
                else:
                    xslave = xslave + slaves_width + gap

    def set_left(self):

        sizes = self.horizontal_tiling_sizes(1)
        coordinates = self.horizontal_tiling_positions(sizes, 1)
        self.set_tiling(sizes, coordinates, True)


    def set_right(self):

        sizes = self.horizontal_tiling_sizes(-1)
        coordinates = self.horizontal_tiling_positions(sizes, -1)
        self.set_tiling(sizes, coordinates, True)

    def set_top(self):

        sizes = self.vertical_tiling_sizes(1)
        coordinates = self.vertical_tiling_positions(sizes, 1)
        self.set_tiling(sizes, coordinates, False)

    def set_bottom(self):

        sizes = self.vertical_tiling_sizes(-1)
        coordinates = self.vertical_tiling_positions(sizes, -1)
        self.set_tiling(sizes, coordinates, False)

    def update_layout(self):

        if len(self.windows) == 0:
            return
        if self.layout == "Floating":
            self.set_floating()
        if self.layout == "Left":
            self.set_left()
        if self.layout == "Right":
            self.set_right()
        if self.layout == "Top":
            self.set_top()
        if self.layout == "Bottom":
            self.set_bottom()



