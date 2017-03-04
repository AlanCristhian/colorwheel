from math import degrees, radians, isclose, pi, ceil, tau, cos, sin
import tkinter
from tkinter import filedialog
import pathlib
import configparser
import atexit
from tkinter import ttk
import utils

from colormath.color_objects import LCHuvColor, sRGBColor
from colormath.color_conversions import convert_color

from chain import given, ANS, unpack


BASE = pathlib.Path()

SETTINGS = configparser.ConfigParser()
if (BASE/".config").exists():
    SETTINGS.read(".config")
else:
    SETTINGS["default"] = {
        "current_directory": str(BASE.home()),
    }


@atexit.register
def _():
    with open(BASE/".config", "w") as settings_file:
        SETTINGS.write(settings_file)


def fix_values(r, g, b):
    if r > 255: r = 255
    if r < 0:   r = 0
    if g > 255: g = 255
    if g < 0:   g = 0
    if b > 255: b = 255
    if b < 0:   b = 0
    return r, g, b


def hex_colors(start, amount, saturation, luminosity):
    c = saturation
    l = luminosity
    k = 360/amount
    ans = (LCHuvColor(l, c, start + i*k) for i in range(amount))
    ans = (convert_color(color, sRGBColor) for color in ans)
    ans = (color.get_upscaled_value_tuple() for color in ans)
    ans = (fix_values(r, g, b) for r, g, b in ans)
    ans = ("#%02x%02x%02x" % (r, g, b) for r, g, b in ans)
    return ans


class Wheel(tkinter.Frame):
    def __init__(self, root, height, width):
        super().__init__(root)
        self.settings = configparser.ConfigParser()
        self.file_path = None
        self.height = height
        self.width = width
        self.position = (20, 20, width - 20, height - 20)
        self.current_directory = SETTINGS["default"]["current_directory"]
        self.root = root
        self.create_widgets()
        self.distribute_widgets()
        self.draw_wheel()
        self.set_events()

    def create_widgets(self):
        self.number_label = tkinter.Label(self, text="Cantidad de colores [0° ... 360°]")
        self.number_var = tkinter.IntVar(self)
        self.number_var.set(360)
        self.number_entry = tkinter.Entry(self, textvariable=self.number_var, width=8)

        self.start_label = tkinter.Label(self, text="Empezar en el ángulo [0° ... 360°]")
        self.start_var = tkinter.DoubleVar(self)
        self.start_var.set(0)
        self.start_entry = tkinter.Entry(self, textvariable=self.start_var, width=8)

        self.saturation_label = tkinter.Label(self, text="Saturación de los colores [0% ... 100%]")
        self.saturation_var = tkinter.DoubleVar(self)
        self.saturation_var.set(50)
        self.saturation_entry = tkinter.Entry(self, textvariable=self.saturation_var, width=8)

        self.luminosity_label = tkinter.Label(self, text="Luminosidad de los colores [0% ... 100%]")
        self.luminosity_var = tkinter.DoubleVar(self)
        self.luminosity_var.set(50)
        self.luminosity_entry = tkinter.Entry(self, textvariable=self.luminosity_var, width=8)

        self.background_label = tkinter.Label(self, text="Color del fondo (hexadecimal)")
        self.background_var = tkinter.StringVar(self)
        self.background_var.set("#888888")
        self.background_entry = tkinter.Entry(self, textvariable=self.background_var, width=8)

        self.outline_var = tkinter.IntVar()
        self.outline_var.set("0")
        self.outline_checkbutton = tkinter.Checkbutton(self, text="Dibujar contorno", variable=self.outline_var, command=self.draw_wheel)

        self.draw_button = tkinter.Button(self, text="Dibujar Rueda de colores", command=self.draw_wheel)
        self.save_image_button = tkinter.Button(self, text="Guardar como imagen", command=self.save_image)
        self.save_wheel_button = tkinter.Button(self, text="Guardar nueva rueda de colores", command=self.save_wheel)
        self.save_changes_button = tkinter.Button(self, text="Guardar cambios", command=self.save_changes)
        self.open_wheel_button = tkinter.Button(self, text="Abrir Rueda de colores", command=self.open_wheel)
        self.canvas = tkinter.Canvas(self, width=650, height=650)

    def distribute_widgets(self):
        self.grid(padx=0, pady=0)

        self.canvas.grid(row=0, column=2, rowspan=50, padx=(10, 20), pady=20)

        self.number_label.grid(row=0, column=0, sticky=tkinter.E, padx=(20, 10), pady=(20, 0))
        self.number_entry.grid(row=0, column=1, padx=10, pady=(10, 0))

        self.start_label.grid(row=1, column=0, sticky=tkinter.E, padx=10, pady=(10, 0))
        self.start_entry.grid(row=1, column=1, padx=10, pady=(10, 0))

        self.saturation_label.grid(row=2, column=0, sticky=tkinter.E, padx=10, pady=(10, 0))
        self.saturation_entry.grid(row=2, column=1, padx=10, pady=(10, 0))

        self.luminosity_label.grid(row=3, column=0, sticky=tkinter.E, padx=(20, 10), pady=(10, 0))
        self.luminosity_entry.grid(row=3, column=1, padx=10, pady=(10, 0))

        self.background_label.grid(row=4, column=0, sticky=tkinter.E, padx=10, pady=(10, 0))
        self.background_entry.grid(row=4, column=1, padx=10, pady=(10, 0))

        self.outline_checkbutton.grid(row=5, column=0, columnspan=2, padx=(2, 10))

        self.draw_button.grid(row=6, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, padx=(20, 10))

        self.save_image_button.grid(row=7, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, padx=(20, 10))
        self.open_wheel_button.grid(row=8, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, padx=(20, 10))
        self.save_wheel_button.grid(row=9, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, padx=(20, 10))
        self.save_changes_button.grid(row=9, column=0, columnspan=2, sticky=tkinter.W+tkinter.E, padx=(20, 10))

    def draw_wheel(self, event=None):
        number = self.number_var.get()
        saturation = self.saturation_var.get()
        luminosity = self.luminosity_var.get()
        start = radians(self.start_var.get())
        step = 360/number
        background = self.background_var.get()
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=background, outline=background)

        if self.outline_var.get():
            for i, color in enumerate(hex_colors(start, number, saturation, luminosity)):
                self.canvas.create_arc(self.position, fill=color, start=(i*step), extent=step)
            self.canvas.create_oval(70, 70, self.width - 70, self.height - 70, fill=background)
        else:
            for i, color in enumerate(hex_colors(start, number, saturation, luminosity)):
                self.canvas.create_arc(self.position, fill=color, start=(i*step), extent=step, outline=color)
            self.canvas.create_oval(70, 70, self.width - 70, self.height - 70, fill=background, outline=background)

        self.canvas.update()

        self.select_changed_value()

    def select_changed_value(self):
        widget = self.root.focus_get()
        if isinstance(widget, tkinter.Entry):
           index = len(widget.get())
           widget.select_range(0, index)

    def save_image(self, event=None):
        dialog = filedialog.asksaveasfile(
            mode="wb",
            defaultextension=".ps",
            initialdir=self.current_directory,
            filetypes=[("postscript", ".ps")])
        if dialog is not None:
            self.canvas.postscript(file="temp.ps", colormode="color", width=self.width, height=self.height)
            with open("temp.ps", "br") as temp:
                dialog.write(temp.read())
                self.current_directory = str(pathlib.Path(dialog.name).parent)
                SETTINGS["default"]["current_directory"] = self.current_directory
                dialog.close()

    def save_changes(self, event=None):
        if self.file_path:
            with open(self.file_path, "w") as whell_file:
                context = {
                    "number": self.number_var.get(),
                    "start": self.start_var.get(),
                    "saturation": self.saturation_var.get(),
                    "luminosity": self.luminosity_var.get(),
                    "outline": self.outline_var.get()}
                text = "[wheel]\n" \
                       "number = {number}\n" \
                       "start = {start}\n" \
                       "saturation = {saturation}\n" \
                       "luminosity = {luminosity}\n" \
                       "outline = {outline}\n".format(**context)
                whell_file.write(text)

    def save_wheel(self, event=None):
        dialog = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".wheel",
            initialdir=self.current_directory,
            filetypes=[("color wheel", ".wheel")])
        if dialog is not None:
            context = {
                "number": self.number_var.get(),
                "start": self.start_var.get(),
                "saturation": self.saturation_var.get(),
                "luminosity": self.luminosity_var.get(),
                "outline": self.outline_var.get()}
            text = "[wheel]\n" \
                   "number = {number}\n" \
                   "start = {start}\n" \
                   "saturation = {saturation}\n" \
                   "luminosity = {luminosity}\n" \
                   "outline = {outline}\n".format(**context)
            dialog.write(text)

            self.current_directory = str(pathlib.Path(dialog.name).parent)
            SETTINGS["default"]["current_directory"] = self.current_directory
            self.file_path = dialog.name
            dialog.close()

    def open_wheel(self, event=None):
        dialog = filedialog.askopenfile(
            mode="r",
            defaultextension=".wheel",
            initialdir=self.current_directory,
            filetypes=[("color wheel", ".wheel")])
        if dialog is not None:
            path = pathlib.Path(dialog.name)
            if path in self.root.opened_files:
                dialog.close()
                self.select(self.root.opened_files[path])
            else:
                names = (path.name for path in self.root.opened_files.keys())
                if path.name in names:
                    name = "/".join(path.parts[-2:])
                    wheel = self.root.create_wheel(path=path, name=name)
                else:
                    wheel = self.root.create_wheel(path=path, name=path.name)
                wheel.settings.read(dialog.name)
                wheel.file_path = dialog.name
                dialog.close()
                wheel.number_var.set(wheel.settings["wheel"]["number"])
                wheel.start_var.set(wheel.settings["wheel"]["start"])
                wheel.saturation_var.set(wheel.settings["wheel"]["saturation"])
                wheel.luminosity_var.set(wheel.settings["wheel"]["luminosity"])
                wheel.outline_var.set(wheel.settings["wheel"]["outline"])
                wheel.draw_wheel()
                self.root.select(wheel)

        else:
            self.save_wheel()

    def set_events(self):
        self.number_entry.bind("<Return>", self.draw_wheel)
        self.number_entry.bind("<KP_Enter>", self.draw_wheel)
        self.start_entry.bind("<Return>", self.draw_wheel)
        self.start_entry.bind("<KP_Enter>", self.draw_wheel)
        self.luminosity_entry.bind("<Return>", self.draw_wheel)
        self.luminosity_entry.bind("<KP_Enter>", self.draw_wheel)
        self.background_entry.bind("<Return>", self.draw_wheel)
        self.background_entry.bind("<KP_Enter>", self.draw_wheel)
        self.root.bind("<Control-s>", self.save_changes)
        self.root.bind("<Control-i>", self.save_image)


class App(utils.CustomNotebook):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.current_directory = SETTINGS["default"]["current_directory"]
        self.opened_tabs = {}
        self.opened_files = {}
        # self.set_events()
        self.create_wheel()
        self.pack()

    def create_wheel(self, event=None, *, path=pathlib.Path("untitled"), name="untitled"):
        frame = Wheel(self, height=650, width=650)
        self.add(frame, text=name)
        frame.draw_wheel()
        self.opened_files[path] = frame
        self.opened_tabs[self.index(self.select())] = frame
        return frame

    # @property
    # def selected_tab(self):
    #     return self.opened_tabs[self.index(self.select())]

    # def set_events(self):
    #     self.root.bind("<Control-o>", self.open_wheel)
    #     self.root.bind("<Control-Shift-Key-S>", self.save_wheel)
    #     self.root.bind("<Control-n>", self.create_wheel)

    # def save_wheel(self, event=None):
    #     dialog = filedialog.asksaveasfile(
    #         mode="w",
    #         defaultextension=".wheel",
    #         initialdir=self.current_directory,
    #         filetypes=[("color wheel", ".wheel")])
    #     if dialog is not None:
    #         context = {
    #             "number": self.number_var.get(),
    #             "start": self.start_var.get(),
    #             "saturation": self.saturation_var.get(),
    #             "luminosity": self.luminosity_var.get(),
    #             "outline": self.outline_var.get()}
    #         text = "[wheel]\n" \
    #                "number = {number}\n" \
    #                "start = {start}\n" \
    #                "saturation = {saturation}\n" \
    #                "luminosity = {luminosity}\n" \
    #                "outline = {outline}\n".format(**context)
    #         dialog.write(text)

    #         self.current_directory = str(pathlib.Path(dialog.name).parent)
    #         SETTINGS["default"]["current_directory"] = self.current_directory
    #         self.file_path = dialog.name
    #         dialog.close()

    # def open_wheel(self, event=None):
    #     dialog = filedialog.askopenfile(
    #         mode="r",
    #         defaultextension=".wheel",
    #         initialdir=self.current_directory,
    #         filetypes=[("color wheel", ".wheel")])
    #     if dialog is not None:
    #         path = pathlib.Path(dialog.name)
    #         if path in self.opened_files:
    #             dialog.close()
    #             self.select(self.opened_files[path])
    #         else:
    #             names = (path.name for path in self.opened_files.keys())
    #             if path.name in names:
    #                 name = "/".join(path.parts[-2:])
    #                 wheel = self.root.create_wheel(path=path, name=name)
    #             else:
    #                 wheel = self.root.create_wheel(path=path, name=path.name)
    #             wheel.settings.read(dialog.name)
    #             wheel.file_path = dialog.name
    #             dialog.close()
    #             wheel.number_var.set(wheel.settings["wheel"]["number"])
    #             wheel.start_var.set(wheel.settings["wheel"]["start"])
    #             wheel.saturation_var.set(wheel.settings["wheel"]["saturation"])
    #             wheel.luminosity_var.set(wheel.settings["wheel"]["luminosity"])
    #             wheel.outline_var.set(wheel.settings["wheel"]["outline"])
    #             wheel.draw_wheel()
    #             self.select(wheel)


class Main(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        frame = tkinter.Frame(root)
        frame.pack(fill="both", expand=True)
        self.app = App(frame)
        self.place(in_=self.app, relx=0.5, rely=0.5, anchor='c')
        self.root.minsize(width=self.app.winfo_reqwidth(),height=self.app.winfo_reqheight())
        # self.root.bind("<Control-o>", self.app.open_wheel)
        # self.root.bind("<Control-Shift-Key-S>", self.app.save_wheel)
        # self.root.bind("<Control-n>", self.app.create_wheel)

        # self.root.bind("<Control-s>", self.app.selected_tab.save_changes)
        # self.root.bind("<Control-i>", self.app.selected_tab.save_image)
        self.root.bind("<<NotebookTabClosed>>", self.clean_tabs)

    def clean_tabs(self, event):
        tabs_names = self.app.tabs()
        tabs_index = [self.app.index(name) for name in tabs_names]
        for path, value in list(self.app.opened_files.items()):
            name = repr(value).replace("<__main__.Wheel object ", "").replace(">", "")
            if name not in tabs_names:
                del self.app.opened_files[path]
        for tab in list(self.app.opened_tabs.keys()):
            if tab not in tabs_index:
                del self.app.opened_tabs[tab]


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("Color Wheel")
    Main(root).root.mainloop()
