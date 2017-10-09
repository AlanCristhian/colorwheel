import tkinter as tk
from tkinter import ttk


class ToolBar(ttk.Frame):
    initialized = False
    def __init__(self, master, relief=tk.RAISED, compound=tk.LEFT):
        super().__init__(master, relief=relief)
        if not self.initialized:
            self.initialized = True
            self.initialize_style()

        self.button = {}
        self.image = {}
        self.button_grid = {}
        self.compound = compound

    def append(self, *, name, label="", image=None, command=None):
        if name in self.button:
            raise ValueError(f"The name '{name}' already exists.")
        self.image[name] = None if image is None \
                           else tk.PhotoImage(file=image)
        button = ttk.Button(
            self, text=label, image=self.image[name], command=command,
            compound=self.compound, width=len(label), style="Flat.TButton")
        button.bind("<Enter>", self.on_enter, True)
        button.bind("<Leave>", self.on_leave, True)
        self.button[name] = button

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        for i, name in enumerate(self.button):
            self.button[name].grid(row=0, column=i, **self.button_grid)

    def on_enter(self, event):
        event.widget["style"] = "TButton"

    def on_leave(self, event):
        event.widget["style"] = "Flat.TButton"

    def initialize_style(self):
        s = ttk.Style()
        s.configure("Flat.TButton", relief="flat")
