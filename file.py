import tkinter
from tkinter import ttk, font
from math import sqrt
import color
import logging

logging.basicConfig(filename="color_wheel.log", level=logging.ERROR)



GRID_DIMENSIONS = {
    "sticky": tkinter.E,
    "padx": (15, 15),
}
ENTRY_DIMENSIONS = {
    "padx": 0,
    "ipady": 3,
    "ipadx": 6,
}
ENTRY_SETTINGS = {
    "width": 3,
    "justify": tkinter.CENTER,
}
SCALE_360 = {
    "from_": 0,
    "to": 360,
    "length": 360,
    "tickinterval": 45,
    "orient": tkinter.HORIZONTAL,
}
SCALE_100 = {
    "from_": 0,
    "to": 100,
    "length": 360,
    "tickinterval": 10,
    "orient": tkinter.HORIZONTAL,
}
FRAME_GRID = {
    "sticky": tkinter.NSEW,
    "padx": (15, 0),
    "pady": (15, 0)
}
RADIOBUTTON_GRID = {
    "ipadx": 6,
    "ipady": 3,
    "pady": (15, 7)
}
VOID = [""]
NORTH_SOUTH = tkinter.N + tkinter.S

class SelectAfterReturn:
    def select_changed_value(self):
        widget = self.root.focus_get()
        if isinstance(widget, tkinter.Entry):
           index = len(widget.get())
           widget.select_range(0, index)


class SettingsFrame(tkinter.LabelFrame):
    def __init__(self, master, text):
        super().__init__(master, text=text)

        # number
        self.number_var = tkinter.IntVar(self, 360)
        self.number_label = tkinter.Label(self, text="Cantidad:")
        self.number_entry = tkinter.Entry(
            self, textvariable=self.number_var, **ENTRY_SETTINGS)
        self.number_scale = tkinter.Scale(
            self, variable=self.number_var, **SCALE_360)

        # start
        self.start_var = tkinter.IntVar(self, 0)
        self.start_label = tkinter.Label(self, text="Empezar en:")
        self.start_entry = tkinter.Entry(
            self, textvariable=self.start_var, **ENTRY_SETTINGS)
        self.start_scale = tkinter.Scale(
            self, variable=self.start_var, **SCALE_360  )

        # saturation
        self.saturation_var = tkinter.IntVar(self, 50)
        self.saturation_label = tkinter.Label(self, text="Saturación:")
        self.saturation_entry = tkinter.Entry(
            self, textvariable=self.saturation_var, **ENTRY_SETTINGS)
        self.saturation_scale = tkinter.Scale(
            self, variable=self.saturation_var, **SCALE_100)

        # luminosity
        self.luminosity_var = tkinter.IntVar(self, 50)
        self.luminosity_label = tkinter.Label(self, text="Luminosidad:")
        self.luminosity_entry = tkinter.Entry(
            self, textvariable=self.luminosity_var, **ENTRY_SETTINGS)
        self.luminosity_scale = tkinter.Scale(
            self, variable=self.luminosity_var, **SCALE_100)

        self.set_events()

    def incrementer(self, variable):
        def increment(self, event=None):
            variable.set(variable.get() + 1)
        return increment

    def decrementer(self, variable):
        def decrement(self, event=None):
            variable.set(variable.get() - 1)
        return decrement

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)

        # number
        self.number_label.grid(row=0, column=0, **GRID_DIMENSIONS)
        self.number_entry.grid(row=0, column=1, **ENTRY_DIMENSIONS)
        self.number_scale.grid(row=0, column=2, **GRID_DIMENSIONS)

        # start
        self.start_label.grid(row=1, column=0, **GRID_DIMENSIONS)
        self.start_entry.grid(row=1, column=1, **ENTRY_DIMENSIONS)
        self.start_scale.grid(row=1, column=2, **GRID_DIMENSIONS)

        # Saturation
        self.saturation_label.grid(row=2, column=0, **GRID_DIMENSIONS)
        self.saturation_entry.grid(row=2, column=1, **ENTRY_DIMENSIONS)
        self.saturation_scale.grid(row=2, column=2, **GRID_DIMENSIONS)

        # luminosity
        self.luminosity_label.grid(row=3, column=0, **GRID_DIMENSIONS)
        self.luminosity_entry.grid(row=3, column=1, **ENTRY_DIMENSIONS)
        self.luminosity_scale.grid(row=3, column=2, **GRID_DIMENSIONS)

    def set_events(self):
        increment_number_var = self.incrementer(self.number_var)
        decrement_number_var = self.decrementer(self.number_var)
        increment_start_var = self.incrementer(self.start_var)
        decrement_start_var = self.decrementer(self.start_var)
        increment_saturation_var = self.incrementer(self.saturation_var)
        decrement_saturation_var = self.decrementer(self.saturation_var)
        increment_luminosity_var = self.incrementer(self.luminosity_var)
        decrement_luminosity_var = self.decrementer(self.luminosity_var)

        self.number_entry.bind("<Up>", increment_number_var)
        self.number_entry.bind("<Down>", decrement_number_var)
        self.start_entry.bind("<Up>", increment_start_var)
        self.start_entry.bind("<Down>", decrement_start_var)
        self.saturation_entry.bind("<Up>", increment_saturation_var)
        self.saturation_entry.bind("<Down>", decrement_saturation_var)
        self.luminosity_entry.bind("<Up>", increment_luminosity_var)
        self.luminosity_entry.bind("<Down>", decrement_luminosity_var)

    @property
    def number(self): return self.number_var.get()
    @property
    def start(self): return self.start_var.get()
    @property
    def saturation(self): return self.saturation_var.get()
    @property
    def luminosity(self): return self.luminosity_var.get()

    @number.setter
    def number(self, value): return self.number_var.set(value)
    @start.setter
    def start(self, value): return self.start_var.set(value)
    @saturation.setter
    def saturation(self, value): return self.saturation_var.set(value)
    @luminosity.setter
    def luminosity(self, value): return self.luminosity_var.set(value)


class ViewFrame(tkinter.LabelFrame):
    def __init__(self, master, text, command=None):
        super().__init__(master, text=text)

        # background
        self.background_var = tkinter.StringVar(self, "gray20")
        self.background_label = tkinter.Label(self, text="Color de fondo:")
        self.background_entry = tkinter.Entry(
            self, textvariable=self.background_var, width=7,
            justify=tkinter.CENTER)

        # outline
        self.outline_var = tkinter.IntVar(self)
        self.outline_checkbutton = tkinter.Checkbutton(
            self, text=" Contorno",
            variable=self.outline_var, command=command)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.background_label.grid(row=0, column=0, pady=(15, 0),
                                   **GRID_DIMENSIONS)
        self.background_entry.grid(row=0, column=1, pady=(15, 0),
                                    **ENTRY_DIMENSIONS)
        self.outline_checkbutton.grid(row=0, column=2, pady=(15, 0),
                                    **GRID_DIMENSIONS)

    @property
    def background(self): return self.background_var.get()
    @property
    def outline(self): return self.outline_var.get()

    @background.setter
    def background(self, value): return self.background_var.set(value)
    @outline.setter
    def outline(self, value): return self.outline_var.set(value)


class ColorSpaceFrame(tkinter.LabelFrame):
    def __init__(self, master, text, command=None):
        super().__init__(master, text=text)
        self.color_space_var = tkinter.StringVar(self, "HSL")
        self.lchab_radiobutton = tkinter.Radiobutton(
            self, text="Lab", value="Lab", variable=self.color_space_var,
            command=command, indicatoron=0, highlightthickness=0, padx=6)
        self.lchuv_radiobutton = tkinter.Radiobutton(
            self, text="Luv", value="Luv", variable=self.color_space_var,
            command=command, indicatoron=0, highlightthickness=0, padx=6)
        self.hsl_radiobutton = tkinter.Radiobutton(
            self, text="HSL", value="HSL", variable=self.color_space_var,
            command=command, indicatoron=0, highlightthickness=0, padx=6)
        self.hsv_radiobutton = tkinter.Radiobutton(
            self, text="HSV", value="HSV", variable=self.color_space_var,
            command=command, indicatoron=0, highlightthickness=0, padx=6)
        self.ipt_radiobutton = tkinter.Radiobutton(
            self, text="IPT", value="IPT", variable=self.color_space_var,
            command=command, indicatoron=0, highlightthickness=0, padx=6)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.lchab_radiobutton.grid(row=0, column=0, padx=(15, 0),
                                    **RADIOBUTTON_GRID)
        self.lchuv_radiobutton.grid(row=0, column=1, **RADIOBUTTON_GRID)
        self.hsl_radiobutton.grid(row=0, column=2, **RADIOBUTTON_GRID)
        self.hsv_radiobutton.grid(row=0, column=3, **RADIOBUTTON_GRID)
        self.ipt_radiobutton.grid(row=0, column=4, **RADIOBUTTON_GRID)

    @property
    def space(self): return self.color_space_var.get()

    @space.setter
    def space(self, value): return self.color_space_var.set(value)


class DataFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.color_treeview = ttk.Treeview(
            self, columns=["Color"], show="headings", height=8,
            selectmode="none")
        self.hexrgb_treeview = ttk.Treeview(
            self, columns=["Hex RGB"], show="headings", height=8,
            selectmode="browse")
        self.hexrgba_treeview = ttk.Treeview(
            self, columns=["Hex RGBA"], show="headings", height=8,
            selectmode="browse")
        self.r_treeview = ttk.Treeview(
            self, columns=["R"], show="headings", height=8,
            selectmode="browse")
        self.g_treeview = ttk.Treeview(
            self, columns=["G"], show="headings", height=8,
            selectmode="browse")
        self.b_treeview = ttk.Treeview(
            self, columns=["B"], show="headings", height=8,
            selectmode="browse")

        measure = font.Font(master).measure

        M1 = measure(" Color")
        M2 = measure(" Hex RGB")
        M3 = measure(" Hex RGBA")
        M4 = measure(" 000")

        self.color_treeview.column("Color", width=M1)
        self.color_treeview.heading("Color", text="Color")

        self.hexrgb_treeview.column("Hex RGB", width=M2)
        self.hexrgb_treeview.heading("Hex RGB", text="Hex RGB")

        self.hexrgba_treeview.column("Hex RGBA", width=M3)
        self.hexrgba_treeview.heading("Hex RGBA", text="Hex RGBA")

        self.r_treeview.column("R", width=M4)
        self.r_treeview.heading("R", text="R")
        self.g_treeview.column("G", width=M4)
        self.g_treeview.heading("G", text="G")
        self.b_treeview.column("B", width=M4)
        self.b_treeview.heading("B", text="B")

        self.scroll = tkinter.Scrollbar(self)
        self.scroll.configure(command=self.set_yview)

        self.color_treeview.configure(
            yscrollcommand=self.set_scroll, selectmode="none")
        self.hexrgb_treeview.configure(yscrollcommand=self.set_scroll)
        self.hexrgba_treeview.configure(yscrollcommand=self.set_scroll)
        self.r_treeview.configure(yscrollcommand=self.set_scroll)
        self.g_treeview.configure(yscrollcommand=self.set_scroll)
        self.b_treeview.configure(yscrollcommand=self.set_scroll)

        self.copy_hexrgb_data = self.copy_data(self.hexrgb_treeview)
        self.copy_hexrgba_data = self.copy_data(self.hexrgba_treeview)
        self.copy_r_data = self.copy_data(self.r_treeview)
        self.copy_g_data = self.copy_data(self.g_treeview)
        self.copy_b_data = self.copy_data(self.b_treeview)

        self.set_events()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.color_treeview.grid(row=0, column=0, sticky=NORTH_SOUTH)
        self.hexrgb_treeview.grid(row=0, column=1, sticky=NORTH_SOUTH)
        self.hexrgba_treeview.grid(row=0, column=2, sticky=NORTH_SOUTH)
        self.r_treeview.grid(row=0, column=3, sticky=NORTH_SOUTH)
        self.g_treeview.grid(row=0, column=4, sticky=NORTH_SOUTH)
        self.b_treeview.grid(row=0, column=5, sticky=NORTH_SOUTH)
        self.scroll.grid(row=0, column=6, sticky=NORTH_SOUTH)

    def set_yview(self, *args):
        self.color_treeview.yview(*args)
        self.hexrgb_treeview.yview(*args)
        self.hexrgba_treeview.yview(*args)
        self.r_treeview.yview(*args)
        self.g_treeview.yview(*args)
        self.b_treeview.yview(*args)

    def set_scroll(self, x, y):
        self.set_yview("moveto", x)
        self.scroll.set(x, y)

    def insert(self, hex_val, R, G, B):
        rgb_val = hex_val.lstrip('#')
        self.color_treeview.insert("", "end", values=VOID, tags=[rgb_val])
        self.color_treeview.tag_configure(rgb_val, background=hex_val)
        self.hexrgb_treeview.insert("", "end", values=[rgb_val])
        self.hexrgba_treeview.insert("", "end", values=[rgb_val + "ff"])
        self.r_treeview.insert("", "end", values=[R])
        self.g_treeview.insert("", "end", values=[G])
        self.b_treeview.insert("", "end", values=[B])

    def delete_all(self):
        trees = zip(self.color_treeview.get_children(),
                    self.hexrgb_treeview.get_children(),
                    self.hexrgba_treeview.get_children(),
                    self.r_treeview.get_children(),
                    self.g_treeview.get_children(),
                    self.b_treeview.get_children())

        for t1, t2, t3, t4, t5, t6 in trees:
            self.color_treeview.delete(t1)
            self.hexrgb_treeview.delete(t2)
            self.hexrgba_treeview.delete(t3)
            self.r_treeview.delete(t4)
            self.g_treeview.delete(t5)
            self.b_treeview.delete(t6)

    def copy_data(self, tree):
        def copy_content(event):
            item = tree.selection()[0]
            value = tree.item(item)["values"][0]
            self.clipboard_clear()
            self.clipboard_append(value)
        return copy_content

    def set_events(self):
        self.hexrgb_treeview.bind("<Double-Button-1>", self.copy_hexrgb_data)
        self.hexrgba_treeview.bind("<Double-Button-1>", self.copy_hexrgba_data)
        self.r_treeview.bind("<Double-Button-1>", self.copy_r_data)
        self.g_treeview.bind("<Double-Button-1>", self.copy_g_data)
        self.b_treeview.bind("<Double-Button-1>", self.copy_b_data)


class MixerFrame(tkinter.LabelFrame, SelectAfterReturn):
    def __init__(self, master, text):
        super().__init__(master, text=text)
        self.root = master

        ENTRY_MIXER = {
            "justify": tkinter.CENTER,
            "width" : 7,
        }

        self.color1_var = tkinter.StringVar(self, "#B3B3B3")
        self.color2_var = tkinter.StringVar(self, "#B3B3B3")
        self.color3_var = tkinter.StringVar(self, "#B3B3B3")

        self.color1_entry = tkinter.Entry(
            self, textvariable=self.color1_var, **ENTRY_MIXER)
        self.color2_entry = tkinter.Entry(
            self, textvariable=self.color2_var, **ENTRY_MIXER)
        self.color3_entry = tkinter.Entry(
            self, textvariable=self.color3_var, **ENTRY_MIXER)

        self.color1_label = tkinter.Label(self, width=7, background="#B3B3B3")
        self.color2_label = tkinter.Label(self, width=7, background="#B3B3B3")
        self.color3_label = tkinter.Label(self, width=7, background="#B3B3B3")
        self.plus_label = tkinter.Label(self, text="+")
        self.equal_label = tkinter.Label(self, text="=")

        self.set_events()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)

        self.color1_entry.grid(row=0, column=0, padx=(15, 0), pady=(15, 0),
                               ipadx=6, ipady=3)
        self.color1_label.grid(row=0, column=1, padx=15, pady=(15, 0),
                               ipadx=6, ipady=3)

        self.plus_label.grid(row=1, column=0, columnspan=2)

        self.color2_entry.grid(row=2, column=0, padx=(15, 0), ipadx=6, ipady=3)
        self.color2_label.grid(row=2, column=1, padx=15, ipadx=6, ipady=3)

        self.equal_label.grid(row=3, column=0, columnspan=2)

        self.color3_entry.grid(row=4, column=0, padx=(15, 0), pady=(0, 15),
                               ipadx=6, ipady=3)
        self.color3_label.grid(row=4, column=1, padx=15, pady=(0, 15),
                               ipadx=6, ipady=3)

    def mix_colors(self, event=None):
        color1 = self.color1_var.get()
        color2 = self.color2_var.get()
        mixed_color = color.mixer["IPT"](color1, color2)
        self.color3_var.set(mixed_color)
        self.color1_label.configure(background=color1)
        self.color2_label.configure(background=color2)
        self.color3_label.configure(background=mixed_color)
        self.select_changed_value()

    def set_events(self):
        self.color1_entry.bind("<Return>", self.mix_colors)
        self.color1_entry.bind("<KP_Enter>", self.mix_colors)

        self.color2_entry.bind("<Return>", self.mix_colors)
        self.color2_entry.bind("<KP_Enter>", self.mix_colors)


# Memory efficient history storage.
#
# This use the key-sharing dictionary implementation
# and __slots__ to reduce the memory consumption
class HistoryData:
    __slots__ = ("number", "start", "saturation", "luminosity", "background",
                 "color_space", "outline")
    def __init__(self, number, start, saturation, luminosity, background,
                 color_space, outline):
        self.number = number
        self.start = start
        self.saturation = saturation
        self.luminosity = luminosity
        self.background = background
        self.color_space = color_space
        self.outline = outline

    def __eq__(self, other):
        if  self.number      == other.number      \
        and self.start       == other.start       \
        and self.saturation  == other.saturation  \
        and self.luminosity  == other.luminosity  \
        and self.background  == other.background  \
        and self.color_space == other.color_space \
        and self.outline     == other.outline:
            return True
        else:
            return False

    def __repr__(self):
        return (f'HistoryData(number={self.number}, '
                f'start={self.start}, '
                f'saturation={self.saturation}, '
                f'luminosity={self.luminosity}, '
                f'background={self.background}, '
                f'color_space={self.color_space}, '
                f'outline={self.outline})')


class History(list):
    def __init__(self):
        super().__init__()
        self.cursor = -1

    def append(self, data):
        len_self = len(self)
        if len_self - 1 == self.cursor:
            super().append(data)
            self.cursor += 1
        elif len_self - 1 > self.cursor:
            self.cursor += 1
            aux = self[:self.cursor] + [data]
            self.clear()
            self.extend(aux)
        else:
            logging.error("ValueError: len(self) = %r; self.cursor = %s",
                          len_self, self.cursor)

    def prev(self):
        len_self = len(self)
        if len_self == 1:
            result = self[0]
        elif len_self - 1 >= self.cursor:
            if self.cursor >= 0:
                self.cursor -= 1
            result = self[self.cursor]
        else:
            logging.error("ValueError: len(self) = %r; self.cursor = %s",
                          len_self, self.cursor)
        return result

    def next(self):
        len_self = len(self)
        if len_self == 1:
            result = self[0]
        elif len_self - 1 == self.cursor:
            result = self[self.cursor]
        elif len_self - 1 > self.cursor:
            self.cursor += 1
            result = self[self.cursor]
        else:
            logging.error("ValueError: len(self) = %r; self.cursor = %s",
                          len_self, self.cursor)
            result = self[-1]
        return result


class File(tkinter.Frame, SelectAfterReturn):
    def __init__(self, root, ):
        super().__init__(root)
        self.root = root
        self.default_sizes = True
        self.file_path = ""
        self.temporary_name = None
        self.history = History()
        self.update_history = True
        self.saved = True

        self.height = 630
        self.width = 762
        self.set_position()

        self.create_widgets()
        self.set_events()

    def set_position(self):
        diameter = min(self.width, self.height) - 40
        x1 = (self.width - diameter)//2
        y1 = (self.height - diameter)//2
        x2 = self.width - x1
        y2 = self.height - y1
        self.position = (x1, y1, x2, y2)

    def create_widgets(self):
        self.canvas = tkinter.Canvas(
            self, width=self.width, height=self.height)
        self.settings = SettingsFrame(self, text="Ajustes de la rueda")
        self.view = ViewFrame(
            self, text="Visualización", command=self.draw_wheel)
        self.color_space = ColorSpaceFrame(
            self, text="Espacio de color", command=self.draw_wheel)
        self.data = DataFrame(self)
        self.mixer = MixerFrame(self, "Mezclador de colores")

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.canvas.grid(row=0, column=3, rowspan=5, padx=15, pady=15)
        self.settings.grid(row=0, column=0, columnspan=2, **FRAME_GRID)
        self.view.grid(row=1, column=0,  **FRAME_GRID)
        self.color_space.grid(row=2, column=0, **FRAME_GRID)
        self.mixer.grid(row=1, column=1, rowspan=2, **FRAME_GRID)
        self.data.grid(row=3, column=0, **FRAME_GRID)

    def draw_default_wheel(self, event=None):
        number = max(self.settings.number, 1)
        saturation = self.settings.saturation
        luminosity = self.settings.luminosity
        start = self.settings.start
        step = 360/number
        background = self.view.background
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill=background, outline=background)
        name = self.color_space.space
        colors = color.space[name](start, number, saturation, luminosity)
        outline = self.view.outline
        x1, y1, x2, y2 = self.position

        if self.update_history:
            self.history.append(HistoryData(
                number=number,
                start=start,
                saturation=saturation,
                luminosity=luminosity,
                background=background,
                color_space=name,
                outline=outline,
            ))

        self.data.delete_all()

        if number == 0 or number == 1:
            hex_val, R, G, B = next(colors)
            self.canvas.create_oval(x1 , y1 , x2 , y2 ,
                                    outline="black" if outline else hex_val,
                                    fill=hex_val)
            self.data.insert(hex_val, R, G, B)
        else:
            for i, (hex_val, R, G, B) in enumerate(colors):
                self.canvas.create_arc(self.position, fill=hex_val,
                                       start=(i*step), extent=step,
                                       outline="black" if outline else hex_val)
                self.data.insert(hex_val, R, G, B)

        self.canvas.create_oval(x1 + 50, y1 + 50, x2 - 50, y2 - 50,
                                fill=background,
                                outline="black" if outline else background)
        self.canvas.update()
        self.select_changed_value()

    def draw_wheel(self, event=None):
        self.draw_default_wheel()
        self.saved = False
        self.event_generate("<<WheelDrawed>>")

    def set_events(self):
        self.settings.number_entry.bind("<Return>", self.draw_wheel)
        self.settings.number_entry.bind("<KP_Enter>", self.draw_wheel)
        self.settings.number_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.settings.start_entry.bind("<Return>", self.draw_wheel)
        self.settings.start_entry.bind("<KP_Enter>", self.draw_wheel)
        self.settings.start_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.settings.luminosity_entry.bind("<Return>", self.draw_wheel)
        self.settings.luminosity_entry.bind("<KP_Enter>", self.draw_wheel)
        self.settings.luminosity_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.settings.saturation_entry.bind("<Return>", self.draw_wheel)
        self.settings.saturation_entry.bind("<KP_Enter>", self.draw_wheel)
        self.settings.saturation_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.view.background_entry.bind("<Return>", self.draw_wheel)
        self.view.background_entry.bind("<KP_Enter>", self.draw_wheel)


if __name__ == '__main__':
    root = tkinter.Tk()
    file = File(root)
    file.grid(padx=0, pady=0, row=0, column=0)
    root.mainloop()
