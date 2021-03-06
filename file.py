import tkinter as tk
from tkinter import ttk, font
from math import sqrt
import color
import logging
import sys

import widgets

logging.basicConfig(filename="color_wheel.log", level=logging.ERROR)


SCALE_360 = {
    "from_": 1,
    "to": 360,
    "length": 360,
    "orient": tk.HORIZONTAL,
}
SCALE_100 = {
    "from_": 1,
    "to": 100,
    "length": 360,
    "orient": tk.HORIZONTAL,
}
VOID = [""]


class Em:
    def __init__(self, value):
        self.value = value

    def __rmul__(self, other):
        return round(self.value*other)


em = Em(16)


IPAD = {"ipadx": 7, "ipady": 4}


class SelectAfterReturn:
    def select_changed_value(self):
        widget = self.master.focus_get()
        if isinstance(widget, ttk.Entry):
           index = len(widget.get())
           widget.select_range(0, index)


def _rounder(scale, variable):
    def round_value(self, event=None):
        value = scale.get()
        if round(value) != value:
            scale.set(round(value))
            variable.set(round(value))
    return round_value


class SettingsFrame(ttk.LabelFrame):
    def __init__(self, master, text):
        super().__init__(master, text=text)

        # number
        self.number_var = tk.IntVar(self, 360)
        self.number_var.min, self.number_var.max = 1, 360
        self.number_label = ttk.Label(self, text="Cantidad:")
        self.number_entry = ttk.Entry(
            self, textvariable=self.number_var, width=3, justify=tk.CENTER)
        self.number_scale = ttk.Scale(
            self, variable=self.number_var, **SCALE_360)

        # start
        self.start_var = tk.IntVar(self, 1)
        self.start_var.min, self.start_var.max = 1, 360
        self.start_label = ttk.Label(self, text="Empezar en:")
        self.start_entry = ttk.Entry(
            self, textvariable=self.start_var, width=3, justify=tk.CENTER)
        self.start_scale = ttk.Scale(
            self, variable=self.start_var, **SCALE_360)

        # saturation
        self.saturation_var = tk.IntVar(self, 50)
        self.saturation_var.min, self.saturation_var.max = 1, 100
        self.saturation_label = ttk.Label(self, text="Saturación:")
        self.saturation_entry = ttk.Entry(
            self, textvariable=self.saturation_var, width=3, justify=tk.CENTER)
        self.saturation_scale = ttk.Scale(
            self, variable=self.saturation_var, **SCALE_100)

        # luminosity
        self.luminosity_var = tk.IntVar(self, 50)
        self.luminosity_var.min, self.luminosity_var.max = 1, 100
        self.luminosity_label = ttk.Label(self, text="Luminosidad:")
        self.luminosity_entry = ttk.Entry(
            self, textvariable=self.luminosity_var, width=3, justify=tk.CENTER)
        self.luminosity_scale = ttk.Scale(
            self, variable=self.luminosity_var, **SCALE_100)

        self.set_events()

    def incrementer(self, variable):
        def increment(self, event=None):
            value = variable.get() + 1
            if value > variable.max:
                variable.set(variable.min)
            else:
                variable.set(value)
        return increment

    def decrementer(self, variable):
        def decrement(self, event=None):
            value = variable.get() - 1
            if value < variable.min:
                variable.set(variable.max)
            else:
                variable.set(value)
        return decrement

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)

        # number
        self.number_label.grid(row=0, column=0, sticky=tk.E, padx=(1*em, 0))
        self.number_entry.grid(row=0, column=1, **IPAD, padx=(1*em, 0))
        self.number_scale.grid(row=0, column=2, padx=1*em)

        # start
        self.start_label.grid(row=1, column=0, sticky=tk.E, padx=(1*em, 0), pady=(1*em, 0))
        self.start_entry.grid(row=1, column=1, **IPAD, padx=(1*em, 0), pady=(1*em, 0))
        self.start_scale.grid(row=1, column=2, padx=1*em, pady=(1*em, 0))

        # Saturation
        self.saturation_label.grid(row=2, column=0, sticky=tk.E, padx=(1*em, 0), pady=(1*em, 0))
        self.saturation_entry.grid(row=2, column=1, **IPAD, padx=(1*em, 0), pady=(1*em, 0))
        self.saturation_scale.grid(row=2, column=2, padx=1*em,  pady=(1*em, 0))

        # luminosity
        self.luminosity_label.grid(
            row=3, column=0, sticky=tk.E, padx=(1*em, 0), pady=1*em)
        self.luminosity_entry.grid(
            row=3, column=1, **IPAD, padx=(1*em, 0), pady=1*em)
        self.luminosity_scale.grid(
            row=3, column=2, padx=1*em, pady=1*em)

    def set_events(self):
        increment_number_var = self.incrementer(self.number_var)
        decrement_number_var = self.decrementer(self.number_var)
        increment_start_var = self.incrementer(self.start_var)
        decrement_start_var = self.decrementer(self.start_var)
        increment_saturation_var = self.incrementer(self.saturation_var)
        decrement_saturation_var = self.decrementer(self.saturation_var)
        increment_luminosity_var = self.incrementer(self.luminosity_var)
        decrement_luminosity_var = self.decrementer(self.luminosity_var)

        round_number_var = _rounder(self.number_scale, self.number_var)
        round_start_var = _rounder(self.start_scale, self.start_var)
        round_saturation_var = _rounder(self.saturation_scale, self.saturation_var)
        round_luminosity_var = _rounder(self.luminosity_scale, self.luminosity_var)

        self.number_scale.configure(command=round_number_var)
        self.start_scale.configure(command=round_start_var)
        self.saturation_scale.configure(command=round_saturation_var)
        self.luminosity_scale.configure(command=round_luminosity_var)

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


class ViewFrame(ttk.LabelFrame):
    def __init__(self, master, text, command=None):
        super().__init__(master, text=text)

        # background
        self.background_var = tk.StringVar(self, "gray20")
        self.background_label = ttk.Label(self, text="Color de fondo:")
        self.background_entry = ttk.Entry(
            self, textvariable=self.background_var, width=11, justify=tk.CENTER)

        # outline
        self.outline_var = tk.IntVar(self)
        self.outline_checkbutton = ttk.Checkbutton(
            self, text=" Contorno",
            variable=self.outline_var, command=command)

        # color space
        spaces = " ".join(color.space.keys())
        self.color_space_var = tk.StringVar(self, "HSL")
        self.color_space_label = ttk.Label(self, text="Espacio de color:")
        self.color_space_combo = ttk.Combobox(
            self, textvariable=self.color_space_var, width=9,
            justify=tk.CENTER, values=spaces)
        self.color_space_combo.bind("<<ComboboxSelected>>", command)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.background_label.grid(
            row=0, column=0, padx=(1*em, 0), pady=(1*em, 0), sticky=tk.E)
        self.background_entry.grid(
            row=0, column=1, **IPAD, padx=(1*em, 0), pady=(1*em, 0))

        self.color_space_label.grid(
            row=1, column=0, padx=(1*em, 0), pady=1*em, sticky=tk.E)
        self.color_space_combo.grid(
            row=1, column=1, **IPAD, padx=(1*em, 0), pady=(1*em, 0))

        self.outline_checkbutton.grid(
            row=2, column=0, padx=1*em, pady=1*em)

    @property
    def background(self): return self.background_var.get()

    @property
    def outline(self): return self.outline_var.get()

    @property
    def space(self): return self.color_space_var.get()

    @background.setter
    def background(self, value): return self.background_var.set(value)

    @outline.setter
    def outline(self, value): return self.outline_var.set(value)

    @space.setter
    def space(self, value): return self.color_space_var.set(value)


class DataFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        _TREEVIEW_SETTINGS = {"show": "headings", "selectmode": "browse",
                              "height": 6}

        self.color_treeview = ttk.Treeview(
            self, columns=["Color"], **_TREEVIEW_SETTINGS)
        self.hexrgb_treeview = ttk.Treeview(
            self, columns=["Hex RGB"], **_TREEVIEW_SETTINGS)
        self.hexrgba_treeview = ttk.Treeview(
            self, columns=["Hex RGBA"], **_TREEVIEW_SETTINGS)
        self.r_treeview = ttk.Treeview(
            self, columns=["R"], **_TREEVIEW_SETTINGS)
        self.g_treeview = ttk.Treeview(
            self, columns=["G"], **_TREEVIEW_SETTINGS)
        self.b_treeview = ttk.Treeview(
            self, columns=["B"], **_TREEVIEW_SETTINGS)

        self.abs_rg_treeview = ttk.Treeview(
            self, columns=["abs(R - G)"], **_TREEVIEW_SETTINGS)
        self.abs_gb_treeview = ttk.Treeview(
            self, columns=["abs(G - B)"], **_TREEVIEW_SETTINGS)
        self.abs_br_treeview = ttk.Treeview(
            self, columns=["abs(B - R)"], **_TREEVIEW_SETTINGS)

        measure = font.Font(master).measure

        M1 = measure(" Color ")
        M2 = measure(" Hex RGB ")
        M3 = measure(" Hex RGBA ")
        M4 = measure(" 000 ")
        M5 = measure(" mmmmm ") - 1*em

        self.color_treeview.column("Color", width=M1)
        self.color_treeview.heading("Color", text="Color")

        self.hexrgb_treeview.column("Hex RGB", width=M2)
        self.hexrgb_treeview.heading("Hex RGB", text="Hex RGB")

        self.hexrgba_treeview.column("Hex RGBA", width=M3)
        self.hexrgba_treeview.heading("Hex RGBA", text="Hex RGBA")

        self.r_treeview.column("R", width=M4)
        self.r_treeview.heading("R", text=" R ")
        self.g_treeview.column("G", width=M4)
        self.g_treeview.heading("G", text=" G ")
        self.b_treeview.column("B", width=M4)
        self.b_treeview.heading("B", text=" B ")

        self.abs_rg_treeview.column("abs(R - G)", width=M5)
        self.abs_rg_treeview.heading("abs(R - G)", text="|R - G|")
        self.abs_gb_treeview.column("abs(G - B)", width=M5)
        self.abs_gb_treeview.heading("abs(G - B)", text="|G - B|")
        self.abs_br_treeview.column("abs(B - R)", width=M5)
        self.abs_br_treeview.heading("abs(B - R)", text="|B - R|")

        self.scroll = ttk.Scrollbar(self)
        self.scroll.configure(command=self.set_yview)

        self.color_treeview.configure(
            yscrollcommand=self.set_scroll, selectmode="none")
        self.hexrgb_treeview.configure(yscrollcommand=self.set_scroll)
        self.hexrgba_treeview.configure(yscrollcommand=self.set_scroll)
        self.r_treeview.configure(yscrollcommand=self.set_scroll)
        self.g_treeview.configure(yscrollcommand=self.set_scroll)
        self.b_treeview.configure(yscrollcommand=self.set_scroll)
        self.abs_rg_treeview.configure(yscrollcommand=self.set_scroll)
        self.abs_gb_treeview.configure(yscrollcommand=self.set_scroll)
        self.abs_br_treeview.configure(yscrollcommand=self.set_scroll)

        self.copy_hexrgb_data = self.copy_data(self.hexrgb_treeview)
        self.copy_hexrgba_data = self.copy_data(self.hexrgba_treeview)
        self.copy_r_data = self.copy_data(self.r_treeview)
        self.copy_g_data = self.copy_data(self.g_treeview)
        self.copy_b_data = self.copy_data(self.b_treeview)
        self.copy_abs_rg_data = self.copy_data(self.abs_rg_treeview)
        self.copy_abs_gb_data = self.copy_data(self.abs_gb_treeview)
        self.copy_abs_br_data = self.copy_data(self.abs_br_treeview)

        self.set_events()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.color_treeview.grid(row=0, column=0, sticky=tk.N + tk.S)
        self.hexrgb_treeview.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.hexrgba_treeview.grid(row=0, column=2, sticky=tk.N + tk.S)
        self.r_treeview.grid(row=0, column=3, sticky=tk.N + tk.S)
        self.g_treeview.grid(row=0, column=4, sticky=tk.N + tk.S)
        self.b_treeview.grid(row=0, column=5, sticky=tk.N + tk.S)
        self.abs_rg_treeview.grid(row=0, column=6, sticky=tk.N + tk.S)
        self.abs_gb_treeview.grid(row=0, column=7, sticky=tk.N + tk.S)
        self.abs_br_treeview.grid(row=0, column=8, sticky=tk.N + tk.S)
        self.scroll.grid(row=0, column=9, sticky=tk.N + tk.S)

    def set_yview(self, *args):
        self.color_treeview.yview(*args)
        self.hexrgb_treeview.yview(*args)
        self.hexrgba_treeview.yview(*args)
        self.r_treeview.yview(*args)
        self.g_treeview.yview(*args)
        self.b_treeview.yview(*args)
        self.abs_rg_treeview.yview(*args)
        self.abs_gb_treeview.yview(*args)
        self.abs_br_treeview.yview(*args)

    def set_scroll(self, x, y):
        self.set_yview("moveto", x)
        self.scroll.set(x, y)

    def insert(self, hex_val, R, G, B, i):
        rgb_val = hex_val.lstrip('#')
        self.color_treeview.insert("", "end", values=i, tags=[rgb_val])
        self.color_treeview.tag_configure(rgb_val, background=hex_val)
        self.hexrgb_treeview.insert("", "end", values=[rgb_val])
        self.hexrgba_treeview.insert("", "end", values=[rgb_val + "ff"])
        self.r_treeview.insert("", "end", values=[R])
        self.g_treeview.insert("", "end", values=[G])
        self.b_treeview.insert("", "end", values=[B])
        self.abs_rg_treeview.insert("", "end", values=[abs(R - G)])
        self.abs_gb_treeview.insert("", "end", values=[abs(G - B)])
        self.abs_br_treeview.insert("", "end", values=[abs(B - R)])

    def delete_all(self):
        trees = zip(self.color_treeview.get_children(),
                    self.hexrgb_treeview.get_children(),
                    self.hexrgba_treeview.get_children(),
                    self.r_treeview.get_children(),
                    self.g_treeview.get_children(),
                    self.b_treeview.get_children(),
                    self.abs_rg_treeview.get_children(),
                    self.abs_gb_treeview.get_children(),
                    self.abs_br_treeview.get_children())

        for t1, t2, t3, t4, t5, t6, t7, t8, t9 in trees:
            self.color_treeview.delete(t1)
            self.hexrgb_treeview.delete(t2)
            self.hexrgba_treeview.delete(t3)
            self.r_treeview.delete(t4)
            self.g_treeview.delete(t5)
            self.b_treeview.delete(t6)
            self.abs_rg_treeview.delete(t7)
            self.abs_gb_treeview.delete(t8)
            self.abs_br_treeview.delete(t9)

    def copy_data(self, tree):
        def copy_content(event):
            item = tree.selection()[0]
            value = tree.item(item, "values")[0]
            self.clipboard_clear()
            self.clipboard_append(value)
        return copy_content

    def set_events(self):
        self.hexrgb_treeview.bind("<Double-Button-1>", self.copy_hexrgb_data)
        self.hexrgba_treeview.bind("<Double-Button-1>", self.copy_hexrgba_data)
        self.r_treeview.bind("<Double-Button-1>", self.copy_r_data)
        self.g_treeview.bind("<Double-Button-1>", self.copy_g_data)
        self.b_treeview.bind("<Double-Button-1>", self.copy_b_data)
        self.abs_rg_treeview.bind("<Double-Button-1>", self.copy_abs_rg_data)
        self.abs_gb_treeview.bind("<Double-Button-1>", self.copy_abs_gb_data)
        self.abs_br_treeview.bind("<Double-Button-1>", self.copy_abs_br_data)


class MixerFrame(ttk.LabelFrame, SelectAfterReturn):
    def __init__(self, master, text):
        super().__init__(master, text=text)

        self.color1_var = tk.StringVar(self, "#b3b3b3")
        self.color2_var = tk.StringVar(self, "#b3b3b3")
        self.color3_var = tk.StringVar(self, "#b3b3b3")

        self.color1_entry = ttk.Entry(
            self, textvariable=self.color1_var, width=7, justify=tk.CENTER)
        self.color2_entry = ttk.Entry(
            self, textvariable=self.color2_var, width=7, justify=tk.CENTER)
        self.color3_entry = ttk.Entry(
            self, textvariable=self.color3_var, width=7, justify=tk.CENTER)

        self.algorithm_var = tk.StringVar(self, "HSL")
        self.algorithm_label = ttk.Label(self, text="Algoritmo:")
        mixers = " ".join(color.mixer.keys())
        self.algorithm_combo = ttk.Combobox(
            self, textvariable=self.algorithm_var, width=9,
            values=mixers, justify=tk.CENTER)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self.mix_colors)

        self.color1_label = ttk.Label(
            self, width=7, justify=tk.CENTER, background="#b3b3b3",
            relief=tk.SUNKEN)
        self.color2_label = ttk.Label(
            self, width=7, justify=tk.CENTER, background="#b3b3b3",
            relief=tk.SUNKEN)
        self.color3_label = ttk.Label(
            self, width=7, justify=tk.CENTER, background="#b3b3b3",
            relief=tk.SUNKEN)
        self.plus_label = ttk.Label(self, text="+")
        self.equal_label = ttk.Label(self, text="=")

        self.set_events()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)

        self.algorithm_label.grid(
            row=0, column=0, padx=(1*em, 0), pady=1*em, sticky=tk.E)
        self.algorithm_combo.grid(
            row=0, column=1, padx=1*em, pady=1*em, **IPAD)

        self.color1_entry.grid(row=1, column=0, padx=(1*em, 0), **IPAD)
        self.color1_label.grid(row=1, column=1, padx=1*em, **IPAD)

        self.plus_label.grid(row=2, column=0, columnspan=2)

        self.color2_entry.grid(row=3, column=0, padx=(1*em, 0), **IPAD)
        self.color2_label.grid(row=3, column=1, padx=1*em, **IPAD)

        self.equal_label.grid(row=4, column=0, columnspan=2)

        self.color3_entry.grid(
            row=5, column=0, padx=(1*em, 0), pady=(0, 1*em), **IPAD)
        self.color3_label.grid(
            row=5, column=1, padx=1*em, pady=(0, 1*em), **IPAD)

    def mix_colors(self, event=None):
        color1 = self.color1_var.get()
        color2 = self.color2_var.get()
        name = self.algorithm_var.get()
        mixed_color = color.mixer[name](color1, color2)
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

        self.color3_entry.bind("<Return>", self.mix_colors)
        self.color3_entry.bind("<KP_Enter>", self.mix_colors)


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
        return (f"HistoryData(number={self.number}, "
                f"start={self.start}, "
                f"saturation={self.saturation}, "
                f"luminosity={self.luminosity}, "
                f"background={self.background}, "
                f"color_space={self.color_space}, "
                f"outline={self.outline})")


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
            logging.error(
                "ValueError: len(self) = %r; self.cursor = %s",
                len_self, self.cursor)

    def prev(self):
        len_self = len(self)
        if len_self == 1:
            return self[0]
        elif len_self - 1 >= self.cursor:
            if self.cursor >= 0:
                self.cursor -= 1
            return self[self.cursor]
        else:
            logging.error(
                "ValueError: len(self) = %r; self.cursor = %s",
                len_self, self.cursor)

    def next(self):
        len_self = len(self)
        if len_self == 1:
            return self[0]
        elif len_self - 1 == self.cursor:
            return self[self.cursor]
        elif len_self - 1 > self.cursor:
            self.cursor += 1
            return self[self.cursor]
        else:
            logging.error("ValueError: len(self) = %r; self.cursor = %s",
                          len_self, self.cursor)
            return self[-1]


class File(ttk.Frame, SelectAfterReturn):
    def __init__(self, master):
        super().__init__(master)
        self.default_sizes = True
        self.file_path = ""
        self.temporary_name = None
        self.history = History()
        self.update_history = True
        self.saved = True

        self.height = 500
        self.width = 500
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
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height)
        self.settings = SettingsFrame(self, text="Ajustes de la rueda")
        self.view = ViewFrame(
            self, text="Visualización", command=self.draw_wheel)
        self.data = DataFrame(self)
        self.mixer = MixerFrame(self, "Mezclador de colores")

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.canvas.grid(row=0, column=3, rowspan=3, padx=1*em, pady=1*em,
                         sticky=tk.N)
        self.settings.grid(
            row=0, column=0, columnspan=2, padx=(1*em, 0), pady=(1*em, 0))
        self.view.grid(
            row=1, column=0, padx=(1*em, 0), pady=(1*em, 0),
            sticky=tk.E+tk.W)
        self.mixer.grid(
            # row=1, column=1, rowspan=2, sticky=tk.N+tk.E+tk.W,
            row=1, column=1, sticky=tk.N+tk.E+tk.W,
            padx=(1*em, 0), pady=(1*em, 0))
        self.data.grid(row=2, columnspan=2, column=0, padx=(1*em, 0), pady=1*em)

    def draw_default_wheel(self, event=None):
        number = max(self.settings.number, 1)
        saturation = self.settings.saturation
        luminosity = self.settings.luminosity
        start = self.settings.start
        step = 360/number
        step_2 = round(step/2)
        background = self.view.background
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill=background, outline=background)
        name = self.view.space
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
            self.data.insert(hex_val, R, G, B, 1)
        else:
            for i, (hex_val, R, G, B) in enumerate(colors):
                self.canvas.create_arc(self.position, fill=hex_val,
                                       start=(start - step_2 + i*step), extent=step,
                                       outline="black" if outline else hex_val)
                self.data.insert(hex_val, R, G, B, i)

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
    master = tk.Tk()
    file = File(master)
    file.grid(padx=0, pady=0, row=0, column=0)
    master.mainloop()
