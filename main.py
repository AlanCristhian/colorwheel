import tkinter
from tkinter import ttk
from tkinter import filedialog
import pathlib
import configparser
import atexit
import itertools

import widgets
import file


counter = itertools.count().__next__


BASE = pathlib.Path()

SETTINGS = configparser.ConfigParser()
if (BASE/".config").exists():
    SETTINGS.read(".config")
else:
    SETTINGS["default"] = {
        "current_directory": str(BASE.home()),
    }


@atexit.register
def save_config():
    with open(BASE/".config", "w") as settings_file:
        SETTINGS.write(settings_file)


class AppWidgets(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.grid(row=0, column=0)
        self.current_directory = SETTINGS["default"]["current_directory"]

        # create the toolbar
        self.toolbar = tkinter.Frame(self.root)
        self.toolbar.grid(row=0, column=0, sticky=tkinter.W)

        self.new_button = tkinter.Button(
            self.toolbar, text="nuevo", command=self.new_wheel,
            highlightthickness=0)
        self.new_button.grid(row=0, column=0)

        self.open_button = tkinter.Button(
            self.toolbar, text="abrir", highlightthickness=0)
        self.open_button.grid(row=0, column=1)

        self.save_button = tkinter.Button(
            self.toolbar, text="guardar", highlightthickness=0)
        self.save_button.grid(row=0, column=2)

        self.save_as_button = tkinter.Button(
            self.toolbar, text="guardar como", highlightthickness=0)
        self.save_as_button.grid(row=0, column=3)

        self.undo_button = tkinter.Button(
            self.toolbar, text="deshacer", highlightthickness=0)
        self.undo_button.grid(row=0, column=4)

        self.redo_button = tkinter.Button(
            self.toolbar, text="rehacer", highlightthickness=0)
        self.redo_button.grid(row=0, column=5)

        # create an inner frame to center the widgets
        padding = (0, 4, 0, 0)
        self.notebook = widgets.ClosableNotebook(self.root, padding=padding)
        self.notebook.grid(row=1, column=0, sticky=tkinter.W)

        self.set_events()
        self.new_wheel()

    def new_wheel(self, event=None, name=None):
        name = "untitled-%r" % counter() if name is None else name
        frame = tkinter.Frame(self.notebook)
        wheel = file.File(frame)
        self.notebook.add(frame, text=name)
        # set the focus in the new tab
        self.notebook.select(frame)
        return wheel

    def get_tabs(self):
        tab_id = self.notebook.select()
        index = self.notebook.index(tab_id)
        key = self.notebook.tabs()[index].split(".")[2]
        return self.notebook.children[key]

    def get_wheel_and_tab_id(self):
        tab_id = self.notebook.select()
        index = self.notebook.index(tab_id)
        key = self.notebook.tabs()[index].split(".")[2]
        frame = self.notebook.children[key]
        return frame.winfo_children()[0], tab_id

    def save_changes(self, event=None):
        wheel, tab_id = self.get_wheel_and_tab_id()
        if wheel.file_path:
            with open(wheel.file_path, "w") as wheel_file:
                wheel_file.write(
                    f"[wheel]\n"
                    f"number = {wheel.number_var.get()}\n"
                    f"start = {wheel.start_var.get()}\n"
                    f"saturation = {wheel.saturation_var.get()}\n"
                    f"luminosity = {wheel.luminosity_var.get()}\n"
                    f"background = {wheel.background_var.get()}\n"
                    f"color_space = {wheel.color_space_var.get()}\n"
                    f"outline = {wheel.outline_var.get()}")
        else:
            self.save_wheel(wheel=wheel, tab_id=tab_id)

    def save_wheel(self, event=None, wheel=None, tab_id=None):
        if wheel is None:
            wheel, tab_id = self.get_wheel_and_tab_id()

        dialog = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".wheel",
            initialdir=self.current_directory,
            filetypes=[("color wheel", ".wheel")])

        if dialog is not None:
            dialog.write(
                f"[wheel]\n"
                f"number = {wheel.number_var.get()}\n"
                f"start = {wheel.start_var.get()}\n"
                f"saturation = {wheel.saturation_var.get()}\n"
                f"luminosity = {wheel.luminosity_var.get()}\n"
                f"background = {wheel.background_var.get()}\n"
                f"color_space = {wheel.color_space_var.get()}\n"
                f"outline = {wheel.outline_var.get()}")

            wheel_path = pathlib.Path(dialog.name)
            self.current_directory = str(wheel_path.parent)
            SETTINGS["default"]["current_directory"] = self.current_directory
            self.file_path = dialog.name
            dialog.close()
            wheel.file_path = str(wheel_path)
            new_text = pathlib.Path() / wheel_path.parent.parts[-1] /\
                       wheel_path.name
            self.notebook.tab(str(tab_id), text=str(new_text))

    def open_wheel(self, event=None):
        dialog = filedialog.askopenfile(
            mode="r",
            defaultextension=".wheel",
            initialdir=self.current_directory,
            filetypes=[("color wheel", ".wheel")])
        if dialog is not None:
            settings = configparser.ConfigParser()
            settings.read(dialog.name)
            name = pathlib.Path(dialog.name)
            text = pathlib.Path()/name.parent.parts[-1]/name.name
            wheel = self.new_wheel(name=text)
            wheel.file_path = dialog.name
            dialog.close()
            wheel.number_var.set(settings["wheel"]["number"])
            wheel.start_var.set(settings["wheel"]["start"])
            wheel.saturation_var.set(settings["wheel"]["saturation"])
            wheel.luminosity_var.set(settings["wheel"]["luminosity"])
            wheel.background_var.set(settings["wheel"]["background"])
            wheel.outline_var.set(settings["wheel"]["outline"])
            wheel.color_space_var.set(settings["wheel"]["color_space"])
            wheel.draw_wheel()


    def set_events(self):
        self.root.bind("<Control-o>", self.open_wheel)
        self.root.bind("<Control-n>", self.new_wheel)
        self.root.bind("<Control-s>", self.save_changes)
        self.root.bind("<Control-Shift-Key-S>", self.save_wheel)


class App(AppWidgets):
    pass


if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)
    root.configure(background="gray80")
    root.mainloop()
