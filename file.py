import tkinter
from tkinter import ttk, font
from math import sqrt
import color


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

def luma(R, G, B):
    return 0.299*R + 0.587*G + 0.114*B


class File(tkinter.Frame):
    def __init__(self, root, ):
        super().__init__(root)
        self.root = root
        self.default_sizes = True
        self.file_path = ""

        self.height = 630
        self.width = 750
        self.set_position()

        self.create_widgets()
        self.distribute_widgets()
        self.draw_wheel()
        self.set_events()

    def set_position(self):
        diameter = min(self.width, self.height) - 40
        x1 = (self.width - diameter)//2
        y1 = (self.height - diameter)//2
        x2 = self.width - x1
        y2 = self.height - y1
        self.position = (x1, y1, x2, y2)

    def create_widgets(self):
        # canvas
        # ======
        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height)

        # ========
        # settings
        # ========

        self.settings_frame = tkinter.LabelFrame(
            master=self, text="Ajustes de la rueda")

        # number
        # ======
        self.number_var = tkinter.IntVar(self.settings_frame, 360)
        self.number_label = tkinter.Label(self.settings_frame,
                                          text="Cantidad:")
        self.number_entry = tkinter.Entry(
            self.settings_frame, textvariable=self.number_var,
            **ENTRY_SETTINGS)
        self.number_scale = tkinter.Scale(
            self.settings_frame, variable=self.number_var, **SCALE_360)

        # start
        # =====
        self.start_var = tkinter.IntVar(self.settings_frame, 0)
        self.start_label = tkinter.Label(self.settings_frame,
                                         text="Empezar en:")
        self.start_entry = tkinter.Entry(
            self.settings_frame, textvariable=self.start_var, **ENTRY_SETTINGS)
        self.start_scale = tkinter.Scale(
            self.settings_frame, variable=self.start_var, **SCALE_360  )

        # Saturation
        # ==========
        self.saturation_var = tkinter.IntVar(self.settings_frame, 50)
        self.saturation_label = tkinter.Label(self.settings_frame,
                                              text="Saturación:")
        self.saturation_entry = tkinter.Entry(
            self.settings_frame, textvariable=self.saturation_var,
            **ENTRY_SETTINGS)
        self.saturation_scale = tkinter.Scale(
            self.settings_frame, variable=self.saturation_var, **SCALE_100)

        # luminosity
        # ==========
        self.luminosity_var = tkinter.IntVar(self.settings_frame, 50)
        self.luminosity_label = tkinter.Label(self.settings_frame,
                                              text="Luminosidad:")
        self.luminosity_entry = tkinter.Entry(
            self.settings_frame, textvariable=self.luminosity_var,
            **ENTRY_SETTINGS)
        self.luminosity_scale = tkinter.Scale(
            self.settings_frame, variable=self.luminosity_var, **SCALE_100)

        # ==========
        # view frame
        # ==========
        self.view_frame = tkinter.LabelFrame(self, text="Visualización")

        # background
        # ==========
        self.background_var = tkinter.StringVar(self, "gray20")
        self.background_label = tkinter.Label(
            self.view_frame, text="Color de fondo:")
        self.background_entry = tkinter.Entry(
            self.view_frame, textvariable=self.background_var, width=7,
            justify=tkinter.CENTER)

        # outline
        # =======
        self.outline_var = tkinter.IntVar(self)
        self.outline_checkbutton = tkinter.Checkbutton(
            self.view_frame, text=" Dibujar contorno",
            variable=self.outline_var, command=self.draw_wheel)


        # ===========
        # space frame
        # ===========

        self.color_space_frame = tkinter.LabelFrame(
            self, text="Espacio de color")

        # color space
        # ===========
        self.color_space_var = tkinter.StringVar(self, "HSL")
        self.lchab_radiobutton = tkinter.Radiobutton(
            self.color_space_frame, text="Lab", value="Lab",
            variable=self.color_space_var, command=self.draw_wheel,
            indicatoron=0, highlightthickness=0, padx=6)
        self.lchuv_radiobutton = tkinter.Radiobutton(
            self.color_space_frame, text="Luv", value="Luv",
            variable=self.color_space_var, command=self.draw_wheel,
            indicatoron=0, highlightthickness=0, padx=6)
        self.hsl_radiobutton = tkinter.Radiobutton(
            self.color_space_frame, text="HSL", value="HSL",
            variable=self.color_space_var, command=self.draw_wheel,
            indicatoron=0, highlightthickness=0, padx=6)
        self.hsv_radiobutton = tkinter.Radiobutton(
            self.color_space_frame, text="HSV", value="HSV",
            variable=self.color_space_var, command=self.draw_wheel,
            indicatoron=0, highlightthickness=0, padx=6)
        self.ipt_radiobutton = tkinter.Radiobutton(
            self.color_space_frame, text="IPT", value="IPT",
            variable=self.color_space_var, command=self.draw_wheel,
            indicatoron=0, highlightthickness=0, padx=6)

        # ==========
        # data frame
        # ==========
        self.data_frame = tkinter.Frame(self)

        # data treeview
        # =============
        self.color_treeview = ttk.Treeview(self.data_frame,
                                          columns=["Color"],
                                          show="headings")
        self.hexrgb_treeview = ttk.Treeview(self.data_frame,
                                            columns=["Hex RGB"],
                                            show="headings")
        self.hexrgba_treeview = ttk.Treeview(self.data_frame,
                                             columns=["Hex RGBA"],
                                             show="headings")

        self.r_treeview = ttk.Treeview(self.data_frame, columns=["R"],
                                       show="headings")
        self.g_treeview = ttk.Treeview(self.data_frame, columns=["G"],
                                       show="headings")
        self.b_treeview = ttk.Treeview(self.data_frame, columns=["B"],
                                       show="headings")

        def measure(text):
            return font.Font(self.root).measure(text)

        M1 = measure(" Color ")
        M2 = measure(" Hex RGB ")
        M3 = measure(" Hex RGBA ")
        M4 = measure("mmm")

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

        self.data_scroll = tkinter.Scrollbar(self.data_frame)
        self.data_scroll.configure(command=self.set_yview)

        self.color_treeview.configure(yscrollcommand=self.set_scroll,
                                      selectmode="none")
        self.hexrgb_treeview.configure(yscrollcommand=self.set_scroll)
        self.hexrgba_treeview.configure(yscrollcommand=self.set_scroll)
        self.r_treeview.configure(yscrollcommand=self.set_scroll)
        self.g_treeview.configure(yscrollcommand=self.set_scroll)
        self.b_treeview.configure(yscrollcommand=self.set_scroll)

    def distribute_widgets(self):
        self.grid(padx=0, pady=0)

        # canvas
        # ======
        self.canvas.grid(row=0, column=3, rowspan=5, padx=15, pady=15)

        # ========
        # settings
        # ========
        self.settings_frame.grid(row=0, column=0, **FRAME_GRID)

        # number
        # ======
        self.number_label.grid(row=0, column=0, **GRID_DIMENSIONS)
        self.number_entry.grid(row=0, column=1, **ENTRY_DIMENSIONS)
        self.number_scale.grid(row=0, column=2, **GRID_DIMENSIONS)

        # start
        # =====
        self.start_label.grid(row=1, column=0, **GRID_DIMENSIONS)
        self.start_entry.grid(row=1, column=1, **ENTRY_DIMENSIONS)
        self.start_scale.grid(row=1, column=2, **GRID_DIMENSIONS)

        # Saturation
        # ==========
        self.saturation_label.grid(row=2, column=0, **GRID_DIMENSIONS)
        self.saturation_entry.grid(row=2, column=1, **ENTRY_DIMENSIONS)
        self.saturation_scale.grid(row=2, column=2, **GRID_DIMENSIONS)

        # luminosity
        # ==========
        self.luminosity_label.grid(row=3, column=0, **GRID_DIMENSIONS)
        self.luminosity_entry.grid(row=3, column=1, **ENTRY_DIMENSIONS)
        self.luminosity_scale.grid(row=3, column=2, **GRID_DIMENSIONS)

        # ==========
        # view frame
        # ==========
        self.view_frame.grid(row=1, column=0, **FRAME_GRID)

        # background
        # ==========
        self.background_label.grid(row=0, column=0, **GRID_DIMENSIONS)
        self.background_entry.grid(row=0, column=1, **ENTRY_DIMENSIONS)

        # outline
        # =======
        self.outline_checkbutton.grid(row=0, column=2, **GRID_DIMENSIONS)

        # ===========
        # space frame
        # ===========
        self.color_space_frame.grid(row=2, column=0, **FRAME_GRID)

        # color space
        # ===========
        self.lchab_radiobutton.grid(row=0, column=0, padx=(15, 0),
                                    **RADIOBUTTON_GRID)
        self.lchuv_radiobutton.grid(row=0, column=1, **RADIOBUTTON_GRID)
        self.hsl_radiobutton.grid(row=0, column=2, **RADIOBUTTON_GRID)
        self.hsv_radiobutton.grid(row=0, column=3, **RADIOBUTTON_GRID)
        self.ipt_radiobutton.grid(row=0, column=4, **RADIOBUTTON_GRID)

        # ==========
        # data frame
        # ==========

        self.data_frame.grid(row=3, column=0, **FRAME_GRID)

        # data treeview
        # =============
        self.color_treeview.grid(row=0, column=0, sticky=tkinter.N+tkinter.S)
        self.hexrgb_treeview.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
        self.hexrgba_treeview.grid(row=0, column=2, sticky=tkinter.N+tkinter.S)

        self.r_treeview.grid(row=0, column=3, sticky=tkinter.N+tkinter.S)
        self.g_treeview.grid(row=0, column=4, sticky=tkinter.N+tkinter.S)
        self.b_treeview.grid(row=0, column=5, sticky=tkinter.N+tkinter.S)

        self.data_scroll.grid(row=0, column=6, sticky=tkinter.N+tkinter.S)

    def select_changed_value(self):
        widget = self.root.focus_get()
        if isinstance(widget, tkinter.Entry):
           index = len(widget.get())
           widget.select_range(0, index)

    def draw_wheel(self, event=None):
        number = max(self.number_var.get(), 1)
        saturation = self.saturation_var.get()
        luminosity = self.luminosity_var.get()
        start = self.start_var.get()
        step = 360/number
        background = self.background_var.get()
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill=background, outline=background)
        name = self.color_space_var.get()
        colors = color.space[name](start, number, saturation, luminosity)
        outline = bool(self.outline_var.get())

        tree1 = self.color_treeview.get_children()
        tree2 = self.hexrgb_treeview.get_children()
        tree3 = self.hexrgba_treeview.get_children()
        tree4 = self.r_treeview.get_children()
        tree5 = self.g_treeview.get_children()
        tree6 = self.b_treeview.get_children()

        self_canvas_create_arc = self.canvas.create_arc
        self_color_treeview_insert = self.color_treeview.insert
        self_color_treeview_tag_configure = self.color_treeview.tag_configure
        self_hexrgb_treeview_insert = self.hexrgb_treeview.insert
        self_hexrgba_treeview_insert = self.hexrgba_treeview.insert
        self_r_treeview_insert = self.r_treeview.insert
        self_g_treeview_insert = self.g_treeview.insert
        self_b_treeview_insert = self.b_treeview.insert

        for t1, t2, t3, t4, t5, t6 \
        in zip(tree1, tree2, tree3, tree4, tree5, tree6):
            self.color_treeview.delete(t1)
            self.hexrgb_treeview.delete(t2)
            self.hexrgba_treeview.delete(t3)
            self.r_treeview.delete(t4)
            self.g_treeview.delete(t5)
            self.b_treeview.delete(t6)

        for i, (hex_val, R, G, B) in enumerate(colors):
            self_canvas_create_arc(self.position, fill=hex_val,
                                   start=(i*step), extent=step,
                                   outline="black" if outline else hex_val)

            self_color_treeview_insert("", "end", values=VOID, tags=(hex_val,))
            self_color_treeview_tag_configure(hex_val, background=hex_val)

            self_hexrgb_treeview_insert("", "end", values=[hex_val])
            self_hexrgba_treeview_insert("", "end", values=[hex_val + "ff"])
            self_r_treeview_insert("", "end", values=[R])
            self_g_treeview_insert("", "end", values=[G])
            self_b_treeview_insert("", "end", values=[B])

        x1, y1, x2, y2 = self.position
        self.canvas.create_oval(x1 + 50, y1 + 50, x2 - 50, y2 - 50,
                                fill=background,
                                outline="black" if outline else background)
        self.canvas.update()
        self.select_changed_value()

    def set_yview(self, *args):
        self.color_treeview.yview(*args)
        self.hexrgb_treeview.yview(*args)
        self.hexrgba_treeview.yview(*args)
        self.r_treeview.yview(*args)
        self.g_treeview.yview(*args)
        self.b_treeview.yview(*args)

    def set_scroll(self, x, y):
        self.color_treeview.yview("moveto", x)
        self.hexrgb_treeview.yview("moveto", x)
        self.hexrgba_treeview.yview("moveto", x)
        self.r_treeview.yview("moveto", x)
        self.g_treeview.yview("moveto", x)
        self.b_treeview.yview("moveto", x)
        self.data_scroll.set(x, y)

    def copy_data(self, tree):
        def copy_content(event):
            item = tree.selection()[0]
            value = tree.item(item)["values"][0]
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
        return copy_content

    def resize_canvas(self, event):
        if self.default_sizes:
            settings_w = self.settings_frame.winfo_width()
            root_w = self.root.winfo_width()
            root_h = self.root.winfo_height()

            self.width = root_w - settings_w
            self.height = root_h
            self.default_sizes = False
        else:
            self.width = 650
            self.height = 650
            self.default_sizes = True

        # self.root.unbind("<Configure>")

        self.canvas.destroy()
        self.settings_frame.destroy()
        self.view_frame.destroy()
        self.color_space_frame.destroy()
        self.data_frame.destroy()

        self.set_position()
        self.create_widgets()
        self.distribute_widgets()
        self.draw_wheel()
        self.set_events()

    def set_events(self):
        # self.root.bind("<Configure>", self.resize_canvas)
        self.number_entry.bind("<Return>", self.draw_wheel)
        self.number_entry.bind("<KP_Enter>", self.draw_wheel)
        self.number_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.start_entry.bind("<Return>", self.draw_wheel)
        self.start_entry.bind("<KP_Enter>", self.draw_wheel)
        self.start_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.luminosity_entry.bind("<Return>", self.draw_wheel)
        self.luminosity_entry.bind("<KP_Enter>", self.draw_wheel)
        self.luminosity_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.saturation_entry.bind("<Return>", self.draw_wheel)
        self.saturation_entry.bind("<KP_Enter>", self.draw_wheel)
        self.saturation_scale.bind("<ButtonRelease-1>", self.draw_wheel)

        self.background_entry.bind("<Return>", self.draw_wheel)
        self.background_entry.bind("<KP_Enter>", self.draw_wheel)

        copy_color_data = self.copy_data(self.color_treeview)
        copy_hexrgb_data = self.copy_data(self.hexrgb_treeview)
        copy_hexrgba_data = self.copy_data(self.hexrgba_treeview)
        copy_r_data = self.copy_data(self.r_treeview)
        copy_g_data = self.copy_data(self.g_treeview)
        copy_b_data = self.copy_data(self.b_treeview)

        self.color_treeview.bind("<Double-Button-1>", copy_color_data)
        self.hexrgb_treeview.bind("<Double-Button-1>", copy_hexrgb_data)
        self.hexrgba_treeview.bind("<Double-Button-1>", copy_hexrgba_data)
        self.r_treeview.bind("<Double-Button-1>", copy_r_data)
        self.g_treeview.bind("<Double-Button-1>", copy_g_data)
        self.b_treeview.bind("<Double-Button-1>", copy_b_data)


if __name__ == '__main__':
    root = tkinter.Tk()
    file = File(root)
    root.mainloop()
