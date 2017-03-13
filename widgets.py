import tkinter
from tkinter import ttk, messagebox


class ClosableNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, check_unsaved=False, confirm_close=None,
                 **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "ClosableNotebook"
        super().__init__(*args, **kwargs)

        self._active = None
        self._check_unsaved = check_unsaved
        self._confirm_close = confirm_close

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def confirm_close(self, data):
        if self._confirm_close:
            self._confirm_close(data)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(["pressed"])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(["pressed"]):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if self._check_unsaved:
            if "close" in element and self._active == index:
                key = self.tabs()[index].split(".")[2]
                frame = self.children[key]
                wheel = frame.winfo_children()[0]
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
                    if response is None:
                        pass
                    elif response is True:
                        self.confirm_close(data=index)
                        self.forget(index)
                        self.event_generate("<<NotebookTabClosed>>")
                    else:
                        self.forget(index)
                        self.event_generate("<<NotebookTabClosed>>")
        else:
            if "close" in element and self._active == index:
                self.forget(index)
                self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tkinter.PhotoImage("img_close", file="close.png"),
            tkinter.PhotoImage("img_closeactive", file="active.png"),
            tkinter.PhotoImage("img_closepressed", file="pressed.png")
        )

        style.element_create("close", "image", "img_close",
                            ("pressed", "active", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("ClosableNotebook", [("ClosableNotebook.client", {"sticky": "nswe"})])
        style.layout("ClosableNotebook.Tab", [
            ("ClosableNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("ClosableNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("ClosableNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("ClosableNotebook.label", {"side": "left", "sticky": ''}),
                                    ("ClosableNotebook.close", {"side": "left", "sticky": ''}),
                                    ]
                            })
                        ]
                    })
                ]
            })
        ])
        style.configure("ClosableNotebook.Tab", padding=(10, 3))
        style.configure("ClosableNotebook", background="#B3B3B3")

