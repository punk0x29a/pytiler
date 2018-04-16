from Config import Settings
import classes.Window as Window

NewWindow = Window.Window

# Margins
mtop    = Settings.margin_top
mbottom = Settings.margin_bottom
mleft   = Settings.margin_left
mright  = Settings.margin_right
gap     = Settings.gap
master_resize_rate = Settings.master_resize_rate

class Workspace():

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

    def init(self, ewmh, display, width, height):

        self.ewmh = ewmh
        self.display = display
        self.width = width
        self.height = height

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
        self.update_condition()

    def expand_master(self):
        self.change_master(1)
        self.update_condition()

    def shrink_master(self):
        self.change_master(-1)
        self.update_condition()

    def increase_master(self):
        self.master = self.master + 1
        if self.master >= len(self.windows):
            self.master = 0
        self.update_condition()

    def decrease_master(self):
        if len(self.windows) == 0:
            return
        self.master = self.master - 1
        if self.master < 0:
            self.master = 0
        self.update_condition()

    def cycle_layout(self):

        index = self.layouts.index(self.layout)
        index = index + 1
        if index >= len(self.layouts):
            index = 0
        self.layout = self.layouts[index]
        self.update_condition()

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

    def adjust_for_decorations(self, width, height, client):

        frame = client
        while frame.query_tree().parent != self.ewmh.root:
            frame = frame.query_tree().parent
        data = frame.get_geometry()
        width_difference = data.width - width
        height_difference = data.height - height
        final_width = width - width_difference
        final_height = height - height_difference
        return final_width, final_height

    def set_tiling(self, sizes, coordinates, horizontal=True):

        master_width  = sizes[0]
        master_height = sizes[1]
        slaves_width  = sizes[2]
        slaves_height = sizes[3]

        xmaster = coordinates[0]
        ymaster = coordinates[1]
        xslave  = coordinates[2]
        yslave  = coordinates[3]

        for index, window in enumerate(self.windows):
            if index == self.master:
                master_width, master_height = self.adjust_for_decorations(master_width, master_height, window.client)
                window.set(xmaster, ymaster, master_width, master_height)
            else:
                slaves_width, slaves_height = self.adjust_for_decorations(slaves_width, slaves_height, window.client)
                window.set(xslave, yslave, slaves_width, slaves_height)
                if horizontal:
                    yslave = yslave + slaves_height + gap
                else:
                    xslave = xslave + slaves_width + gap

    def set_left(self):

        sizes = self.horizontal_tiling_sizes()
        coordinates = self.horizontal_tiling_positions(sizes, 1)
        self.set_tiling(sizes, coordinates, True)


    def set_right(self):

        sizes = self.horizontal_tiling_sizes()
        coordinates = self.horizontal_tiling_positions(sizes, -1)
        self.set_tiling(sizes, coordinates, True)

    def set_top(self):

        sizes = self.vertical_tiling_sizes()
        coordinates = self.vertical_tiling_positions(sizes, 1)
        self.set_tiling(sizes, coordinates, False)

    def set_bottom(self):

        sizes = self.vertical_tiling_sizes()
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

    def get_window_index(self, client):

        for index, window in enumerate(self.windows):
            if str(window.client.id) == str(client.id):
                return index
            else:
                pass
        return -1

    def update_condition(self):

        for window in self.windows:
            window.set_last_update()

    def add_window(self, client):

            window = NewWindow()
            data = client.get_geometry()
            window.init(self.display, client, data.x, data.y, data.width, data.height)
            self.windows.append(window)
            self.update_condition()

    def remove_closed_windows(self, fine_indexes):

        for index, window in enumerate(self.windows[:]):
            if index not in fine_indexes:
                self.update_condition()
                del self.windows[index]

    def allign_windows(self, clients):

        fine_indexes = []
        for client in clients:
            index = self.get_window_index(client)
            if index < 0:
                self.add_window(client)
                fine_indexes.append(len(self.windows)-1)
            else:
                fine_indexes.append(index)
        self.remove_closed_windows(fine_indexes)

    def update(self):

        self.update_layout()
        for window in self.windows:
            window.update()

    def debug(self):
        print(len(self.windows))
        for window in self.windows:
            window.debug()





