import tkinter
from tkinter import ttk, filedialog, messagebox, font
import pathlib
import configparser
import itertools

import widgets
import file


TOOLBAR_IPAD = {"ipadx": file.IPAD["ipadx"],
                "ipady": round(file.IPAD["ipady"]*0.5)}
COUNTER = itertools.count().__next__
BASE = pathlib.Path()
SETTINGS = configparser.ConfigParser()
if (BASE/".config").exists():
    SETTINGS.read(".config")
else:
    SETTINGS["default"] = {
        "current_directory": str(BASE.home()),
        "opened_files": [],
    }


def wheel_name(text):
    name = pathlib.Path(text).resolve()
    parts = name.parent.parts
    if parts:
        return str(name.name)
    else:
        return "untitled-%s" % COUNTER()


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0)
        self.current_directory = SETTINGS["default"]["current_directory"]

        measure = font.Font(master).measure

        nuevo = "%rp" % measure("nuevo")
        abrir = "%rp" % measure("abrir")
        guardar = "%rp" % measure("guardar")
        guardar_como = "%rp" % measure("guardar como")
        deshacer = "%rp" % measure("deshacer")
        rehacer = "%rp" % measure("rehacer")

        # create the toolbar
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.grid(row=0, column=0, sticky=tkinter.W)

        self.new_button = ttk.Button(
            self.toolbar, text="nuevo", command=self.new_wheel,
            width=nuevo)
        self.new_button.grid(row=0, column=0, **TOOLBAR_IPAD)

        self.open_button = ttk.Button(
            self.toolbar, text="abrir", command=self.open_wheel,
            width=abrir)
        self.open_button.grid(row=0, column=1, **TOOLBAR_IPAD)

        self.save_button = ttk.Button(
            self.toolbar, text="guardar", command=self.save_changes,
            width=guardar)
        self.save_button.grid(row=0, column=2, **TOOLBAR_IPAD)

        self.save_as_button = ttk.Button(
            self.toolbar, text="guardar como", command=self.save_wheel,
            width=guardar_como)
        self.save_as_button.grid(row=0, column=3, **TOOLBAR_IPAD)

        self.undo_button = ttk.Button(
            self.toolbar, text="deshacer", command=self.undo,
            width=deshacer)
        self.undo_button.grid(row=0, column=4, **TOOLBAR_IPAD)

        self.redo_button = ttk.Button(
            self.toolbar, text="rehacer", command=self.redo,
            width=rehacer)
        self.redo_button.grid(row=0, column=5, **TOOLBAR_IPAD)

        # create an inner frame to center the widgets
        self.notebook = widgets.ClosableNotebook(
            master=self.master,
            check_unsaved=True,
            confirm_close=lambda data: self.save_changes(index=data))
        self.notebook.grid(row=1, column=0, sticky=tkinter.W, **TOOLBAR_IPAD)

        self.set_events()
        if SETTINGS["default"]["opened_files"]:
            for i in SETTINGS["default"]["opened_files"].split(","):
                self.open_wheel(path=i)
        else:
            self.new_wheel()

    def new_wheel(self, event=None, name=None):
        tab_name = "⚫ untitled-%r" % COUNTER() if name is None \
                   else wheel_name(name)
        frame = ttk.Frame(self.notebook)
        wheel = file.File(frame)
        if name is None:
            wheel.temporary_name = tab_name
        wheel.grid(row=0, column=0)
        if name:
            wheel.file_path = str(name)
        self.notebook.add(frame, text=tab_name)
        # set the focus in the new tab
        self.notebook.select(frame)
        wheel.draw_default_wheel()
        wheel.saved = False
        widgets.update_title(self, wheel)
        return wheel

    def get_wheel_and_tab_id(self, index=None):
        tab_id = None
        if index is None:
            tab_id = self.notebook.select()
            index = self.notebook.index(tab_id)
        key = self.notebook.tabs()[index].split(".")[2]
        frame = self.notebook.children[key]
        return frame.winfo_children()[0], tab_id

    def save_changes(self, event=None, index=None):
        wheel, tab_id = self.get_wheel_and_tab_id(index)
        if wheel.file_path:
            with open(wheel.file_path, "w") as wheel_file:
                wheel_file.write(
                    f"[wheel]\n"
                    f"number = {wheel.settings.number}\n"
                    f"start = {wheel.settings.start}\n"
                    f"saturation = {wheel.settings.saturation}\n"
                    f"luminosity = {wheel.settings.luminosity}\n"
                    f"background = {wheel.view.background}\n"
                    f"outline = {wheel.view.outline}\n"
                    f"color_space = {wheel.view.space}")
            wheel.saved = True
            text = self.notebook.tab(tab_id)["text"].replace("⚫ ", "")
            self.notebook.tab(tab_id, text=text)
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
                f"number = {wheel.settings.number}\n"
                f"start = {wheel.settings.start}\n"
                f"saturation = {wheel.settings.saturation}\n"
                f"luminosity = {wheel.settings.luminosity}\n"
                f"background = {wheel.view.background}\n"
                f"outline = {wheel.view.outline}\n"
                f"color_space = {wheel.view.space}")
            wheel.saved = True

            wheel_path = pathlib.Path(dialog.name)
            self.current_directory = str(wheel_path.parent)
            SETTINGS["default"]["current_directory"] = self.current_directory
            self.file_path = dialog.name
            dialog.close()
            wheel.file_path = str(wheel_path)
            new_text = wheel_path.name
            wheel.focus_set()
            tab_id = self.notebook.select()
            self.notebook.tab(str(tab_id), text=str(new_text))
            widgets.update_title(self, wheel)

    def open_wheel(self, event=None, path=None):
        if path:
            settings = configparser.ConfigParser()
            settings.read(path)
            wheel = self.new_wheel(name=path)
        else:
            dialog = filedialog.askopenfile(
                mode="r",
                defaultextension=".wheel",
                initialdir=self.current_directory,
                filetypes=[("color wheel", ".wheel")])
            if dialog is not None:
                settings = configparser.ConfigParser()
                settings.read(dialog.name)
                text = wheel_name(dialog.name)
                wheel = self.new_wheel(name=text)
                wheel.file_path = dialog.name
                dialog.close()
            else:
                return
        if "wheel" in settings:
            wheel.settings.number = settings["wheel"]["number"]
            wheel.settings.start = settings["wheel"]["start"]
            wheel.settings.saturation = settings["wheel"]["saturation"]
            wheel.settings.luminosity = settings["wheel"]["luminosity"]
            wheel.view.background = settings["wheel"]["background"]
            wheel.view.outline = settings["wheel"]["outline"]
            wheel.view.space = settings["wheel"]["color_space"]
            wheel.draw_wheel()
            wheel.focus_set()
            tab_id = self.notebook.select()
            text = self.notebook.tab(tab_id)["text"].replace("⚫ ", "")
            self.notebook.tab(tab_id, text=text)
        wheel.saved = True

    def undo(self, event=None):
        wheel, tab_id = self.get_wheel_and_tab_id()
        wheel.history.prev()
        data = wheel.history[wheel.history.cursor]
        wheel.settings.number = data.number
        wheel.settings.start = data.start
        wheel.settings.saturation = data.saturation
        wheel.settings.luminosity = data.luminosity
        wheel.view.background = data.background
        wheel.view.outline = data.outline
        wheel.view.space = data.color_space
        wheel.update_history = False
        wheel.draw_wheel()
        wheel.update_history = True

    def redo(self, event=None):
        wheel, tab_id = self.get_wheel_and_tab_id()
        wheel.history.next()
        data = wheel.history[wheel.history.cursor]
        wheel.settings.number = data.number
        wheel.settings.start = data.start
        wheel.settings.saturation = data.saturation
        wheel.settings.luminosity = data.luminosity
        wheel.view.background = data.background
        wheel.view.outline = data.outline
        wheel.view.space = data.color_space
        wheel.update_history = False
        wheel.draw_wheel()
        wheel.update_history = True

    def save_config(self):
        opened = []
        for tab in self.notebook.tabs():
            key = tab.split(".")[2]
            frame = self.notebook.children[key]
            wheel = frame.winfo_children()[0]
            wheel.focus_set()
            tab_id = self.notebook.select()
            index = self.notebook.index(tab_id)
            if wheel.file_path:
                opened.append(wheel.file_path)
            if not wheel.saved:
                file_id = wheel.file_path if wheel.file_path\
                          else "este documento sin título"
                response = messagebox.askyesnocancel(
                    title="Grupal",
                    message=f"¿Desea guardar los cambios en {file_id} "
                            f"antes de cerrar?",
                    detail="Si cierra sin guardar se "
                           "perderán los cambios realizados",
                    icon="warning")
                if response is None:
                    break
                elif response is True:
                    self.save_changes(index=index)
                    self.notebook.forget(index)
                else:
                    self.notebook.forget(index)
        else:
            SETTINGS["default"]["opened_files"] = ",".join(opened)

            with open(BASE/".config", "w") as settings_file:
                SETTINGS.write(settings_file)
            self.master.destroy()

    def mark_as_unsaved(self, event):
        if not event.widget.saved:
            tab_id = self.notebook.select()
            if tab_id:
                text = self.notebook.tab(tab_id)["text"]
                if not "⚫ " in text:
                    self.notebook.tab(tab_id, text="⚫ " + text)

    def set_events(self):
        self.master.bind("<Control-o>", self.open_wheel)
        self.master.bind("<Control-n>", self.new_wheel)
        self.master.bind("<Control-s>", self.save_changes)
        self.master.bind("<Control-Shift-Key-S>", self.save_wheel)
        self.master.bind("<Control-Key-z>", self.undo)
        self.master.bind("<Control-Shift-Key-Z>", self.redo)
        self.master.bind("<Control-Key-y>", self.redo)
        self.master.protocol("WM_DELETE_WINDOW", self.save_config)
        if self.master._windowingsystem == 'x11':
            # Pasting from the clipboard doesn't delete the current selection
            # on X11.
            # See issue #5124.
            for cls in 'Text', 'Entry', 'Spinbox':
                self.master.bind_class(cls, '<<Paste>>',
                                'catch {%W delete sel.first sel.last}\n' +
                                self.master.bind_class(cls, '<<Paste>>'))
        self.master.bind("<<WheelDrawed>>", self.mark_as_unsaved)


if __name__ == '__main__':
    master = tkinter.Tk()

    style = ttk.Style()
    style.configure("ClosableNotebook.Tab", padding=(10, 3))

    app = App(master)
    master.mainloop()
