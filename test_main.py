import unittest
import tkinter
from tkinter import ttk

import main
import file


class BaseSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tkinter.Tk()
        cls.app = main.App(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()
        del cls.root

class MainWidgetsSuite:
    def test_main_application_instance(self):
        self.assertIsInstance(self.app, main.App)

    def test_that_app_is_visible(self):
        self.assertTrue(self.app.winfo_manager())


class ToolbarSuite:
    def test_toolbar_property(self):
        self.assertIsInstance(self.app.toolbar, tkinter.Frame)

    def test_that_toolbar_is_visible(self):
        self.assertTrue(self.app.toolbar.winfo_manager())

    def test_new_button(self):
        self.assertIsInstance(self.app.new_button, tkinter.Button)
        self.assertTrue(self.app.new_button.winfo_manager())

    def test_open_button(self):
        self.assertIsInstance(self.app.open_button, tkinter.Button)
        self.assertTrue(self.app.open_button.winfo_manager())

    def test_save_button(self):
        self.assertIsInstance(self.app.save_button, tkinter.Button)
        self.assertTrue(self.app.save_button.winfo_manager())

    def test_save_as_button(self):
        self.assertIsInstance(self.app.save_as_button, tkinter.Button)
        self.assertTrue(self.app.save_as_button.winfo_manager())

    def test_undo_button(self):
        self.assertIsInstance(self.app.undo_button, tkinter.Button)
        self.assertTrue(self.app.undo_button.winfo_manager())

    def test_redo_button(self):
        self.assertIsInstance(self.app.redo_button, tkinter.Button)
        self.assertTrue(self.app.redo_button.winfo_manager())


class GlobalEventsSuite:
    def test_new_event(self):
        self.app.event_generate("<Control-n>")
        self.assertTrue(self.app.notebook.tabs())

    def test_open_event(self):
        self.app.event_generate("<Control-o>")

    def test_save_event(self):
        self.app.event_generate("<Control-s>")

    def test_save_as_event(self):
        self.app.event_generate("<Control-Shift-Key-S>")

    def test_undo_event(self):
        self.app.event_generate("<Control-z>")

    def test_redo_event(self):
        self.app.event_generate("<Control-Shift-Key-Z>")



class AllSuites(BaseSuite, MainWidgetsSuite, ToolbarSuite, GlobalEventsSuite):
    pass


# atexti
# config
# treeview

if __name__ == '__main__':
    unittest.main()
