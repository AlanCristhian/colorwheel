import tkinter
import _tkinter
from tkinter import ttk, messagebox
import pathlib
import platform

BASE = pathlib.Path()


def update_title(self, frame):
    parent = self.master
    while True:
        child = parent
        parent = parent.master
        if parent is None:
            child.title(frame.file_path if frame.file_path
                        else frame.temporary_name)
            break


def _in(a, b):
    return a in b


def _not_in(a, b):
    return a not in b


class ClosableNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, check_unsaved=False, confirm_close=None,
                 takefocus=True, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "ClosableNotebook"
        super().__init__(*args, **kwargs)

        self._active = None
        self._check_unsaved = check_unsaved
        self._confirm_close = confirm_close

        self.bind("<ButtonPress-1>", self.create_press_command("close"), True)
        self.bind("<ButtonRelease-1>", self.create_release_command("close"))

        self.bind(
            "<ButtonPress-2>",
            self.create_press_command("close", not_=True),
            True)
        self.bind(
            "<ButtonRelease-2>",
            self.create_release_command("close", not_=True),
            True)

        self.bind("<ButtonRelease-1>", self.on_tab_focus, True)

    def on_tab_focus(self, event):
        element = self.identify(event.x, event.y)
        if not "close" in element:
            tab_id = self.select()
            try:
                index = self.index(tab_id)
                key = self.tabs()[index].split(".")[2]
                wheel = self.children[key]
                update_title(self, wheel)
            except _tkinter.TclError as error:
                if error.args != ("Invalid slave specification ",):
                    raise

    def confirm_close(self, data):
        if self._confirm_close:
            self._confirm_close(data)

    def create_press_command(self, obj, not_=False):
        def on_close_press(event):
            """Called when the button is pressed over the close button"""
            element = self.identify(event.x, event.y)
            check = _not_in if not_ else _in
            if check(obj, element):
                index = self.index("@%d,%d" % (event.x, event.y))
                self.state(["pressed"])
                self._active = index
        return on_close_press

    def create_release_command(self, obj, not_=False):
        def on_close_release(event):
            """Called when the button is released over the close button"""
            if not self.instate(["pressed"]):
                return

            element =  self.identify(event.x, event.y)
            index = self.index("@%d,%d" % (event.x, event.y))

            if self._check_unsaved:
                check = _not_in if not_ else _in
                if check(obj, element) and self._active == index:
                    key = self.tabs()[index].split(".")[2]
                    wheel = self.children[key]
                    if wheel.saved:
                        self.forget(index)
                        self.event_generate("<<NotebookTabClosed>>")
                    else:
                        file_id = wheel.file_path if wheel.file_path\
                                  else "este documento sin título"
                        response = messagebox.askyesnocancel(
                            title="Individual",
                            message=f"¿Desea guardar los cambios en {file_id} "
                                    f"antes de cerrar?",
                            detail="Si cierra sin guardar se "
                                   "perderán los cambios realizados",
                            icon="warning")
                        if response is True:
                            self.confirm_close(data=index)
                            self.forget(index)
                            self.event_generate("<<NotebookTabClosed>>")
                        elif response is False:
                            self.forget(index)
                            self.event_generate("<<NotebookTabClosed>>")
            else:
                if obj in element and self._active == index:
                    self.forget(index)
                    self.event_generate("<<NotebookTabClosed>>")

            self.state(["!pressed"])
            self._active = None
        return on_close_release

    def __initialize_custom_style(self):
        style = ttk.Style()

        # Store images in the style database
        self.images = (
            tkinter.PhotoImage("img_close_default",
                               file=BASE/"images"/"close_default.png"),
            tkinter.PhotoImage("img_close_active",
                               file=BASE/"images"/"close_active.png"),
            tkinter.PhotoImage("img_close_pressed",
                               file=BASE/"images"/"close_pressed.png"))

        # Create the close button
        style.element_create(
            "close", "image", "img_close_default",
            ("pressed", "active", "!disabled", "img_close_pressed"),
            ("active", "!disabled", "img_close_active"),
            border=8, sticky="")

        # Copy the layout of the current theme
        notebook_layout = style.layout("TNotebook").copy()
        style.layout("ClosableNotebook", notebook_layout)


        if platform.system() != "Windows":
            # Copy the configuration of the current theme
            notebook_cfg = style.configure("TNotebook")
            style.configure(
                "ClosableNotebook", **notebook_cfg if notebook_cfg else {})
            tab_cfg = style.configure("TNotebook.Tab").copy()
            style.configure("ClosableNotebook.Tab", **tab_cfg)

        # Copy the map of the current theme
        notebook_map = style.map("TNotebook.Tab").copy()
        try:
            style.map("ClosableNotebook.Tab", **notebook_map)
        except IndexError as error:
            if error.args == ("list index out of range",):
                style.map("ClosableNotebook.Tab", notebook_map)
            else:
                raise

        # Copy the layout of the current theme
        tab_layout = style.layout("TNotebook.Tab").copy()

        # Add the close button to the layout
        ans = [("Notebook.label", {"side": "left", "sticky": ""}),
               ("Notebook.close", {"side": "left", "sticky": ""})]
        tab_layout[0][1]["children"][0][1]["children"][0][1]["children"] = ans

        # Add the layout to the current widget
        style.layout("ClosableNotebook.Tab", tab_layout)
        style.configure("ClosableNotebook.Tab", padding=(10, 3))
