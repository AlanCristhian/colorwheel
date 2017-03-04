import tkinter
from tkinter import ttk

import widgets


class AppWidgets(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.grid(row=0, column=0)

        # create the toolbar
        self.toolbar = tkinter.Frame(self.root)
        self.toolbar.grid(row=0, column=0)

        self.new_button = tkinter.Button(self.toolbar, text="nuevo")
        self.new_button.grid(row=0, column=0)

        self.open_button = tkinter.Button(self.toolbar, text="abrir")
        self.open_button.grid(row=0, column=1)

        self.save_button = tkinter.Button(self.toolbar, text="guardar")
        self.save_button.grid(row=0, column=2)

        self.save_as_button = tkinter.Button(self.toolbar, text="guardar como")
        self.save_as_button.grid(row=0, column=3)

        self.undo_button = tkinter.Button(self.toolbar, text="deshacer")
        self.undo_button.grid(row=0, column=4)

        self.redo_button = tkinter.Button(self.toolbar, text="rehacer")
        self.redo_button.grid(row=0, column=5)

        # create an inner frame to center the widgets
        self.notebook = widgets.ClosableNotebook(self.root)
        self.notebook.grid(row=1, column=0)


class App(AppWidgets):
    pass


root = tkinter.Tk()
root.geometry('{}x{}+0+0'.format(*root.maxsize()))

app = App(root)


if __name__ == '__main__':
    app.root.mainloop()
