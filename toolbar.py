import tkinter as tk
from tkinter import ttk


class ToolBar(ttk.Frame):
    def __init__(self, master, relief=tk.RAISED, compound=tk.LEFT):
        super().__init__(master, relief=relief)
        self.button = {}
        self.image = {}
        self.button_grid = {}
        self.compound = compound

    def append(self, *, name, label=None, image=None, command=None):
        if name in self.button:
            raise ValueError(f"The name '{name}' already exists.")
        self.image[name] = None if image is None \
                           else tk.PhotoImage(file=image)
        self.button[name] = tk.Button(
            self, text=label, image=self.image[name], command=command,
            relief=tk.FLAT, overrelief=tk.RAISED, compound=self.compound)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        for i, name in enumerate(self.button):
            self.button[name].grid(row=0, column=i, **self.button_grid)
