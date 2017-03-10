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
        cls.app.destroy()
        del cls.app
        cls.root.update_idletasks()
        cls.root.destroy()
        del cls.root


class MainWidgetsSuite(BaseSuite):
    def test_main_application_instance(self):
        self.assertIsInstance(self.app, main.App)

    def test_that_app_is_visible(self):
        self.assertTrue(self.app.winfo_manager())


class ToolbarSuite(BaseSuite):
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


class GlobalEventsSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for tab_id in cls.app.notebook.tabs():
            index = cls.app.notebook.index(tab_id)
            cls.app.notebook.forget(index)

    def setUp(self):
        self.app.new_wheel()

    def tearDown(self):
        for tab_id in self.app.notebook.tabs():
            index = self.app.notebook.index(tab_id)
            self.app.notebook.forget(index)

    def test_new_event(self):
        self.app.event_generate("<Control-n>")
        self.assertEqual(len(self.app.notebook.tabs()), 2)

    def test_undo_event_with_one_element(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        self.app.event_generate("<Control-Key-z>")
        self.assertEqual(wheel.settings.number, 360)

    def test_redo_event_with_one_element(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        self.app.event_generate("<Control-Shift-Key-Z>")
        self.assertEqual(wheel.settings.number, 360)

    def test_undo_with_cursor_at_end(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        wheel.settings.number = 2
        wheel.draw_wheel()
        wheel.settings.number = 3
        wheel.draw_wheel()
        self.app.event_generate("<Control-Key-z>")
        self.assertEqual(wheel.settings.number, 2)
        self.app.event_generate("<Control-Shift-Key-Z>")
        self.assertEqual(wheel.settings.number, 3)

    def test_redo_with_cursor_at_end(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        wheel.settings.number = 2
        wheel.draw_wheel()
        wheel.settings.number = 3
        wheel.draw_wheel()
        self.app.event_generate("<Control-Shift-Key-Z>")
        self.assertEqual(wheel.settings.number, 3)

    def test_undo_with_cursor_at_middle(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        wheel.settings.number = 2
        wheel.draw_wheel()
        wheel.settings.number = 3
        wheel.draw_wheel()
        wheel.settings.number = 4
        wheel.draw_wheel()
        self.app.event_generate("<Control-Key-z>")
        self.app.event_generate("<Control-Key-z>")
        self.assertEqual(wheel.settings.number, 2)
        self.app.event_generate("<Control-Shift-Key-Z>")
        self.assertEqual(wheel.settings.number, 3)

    def test_redo_with_cursor_at_middle(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        wheel.settings.number = 2
        wheel.draw_wheel()
        wheel.settings.number = 3
        wheel.draw_wheel()
        wheel.settings.number = 4
        wheel.draw_wheel()
        self.app.event_generate("<Control-Key-z>")
        self.app.event_generate("<Control-Key-z>")
        self.app.event_generate("<Control-Shift-Key-Z>")
        self.assertEqual(wheel.settings.number, 3)
        self.app.event_generate("<Control-Key-z>")
        self.assertEqual(wheel.settings.number, 2)

    def test_append_after_redo(self):
        wheel, tab_id = self.app.get_wheel_and_tab_id()
        wheel.settings.number = 2
        wheel.draw_wheel()
        wheel.settings.number = 3
        wheel.draw_wheel()
        wheel.settings.number = 4
        wheel.draw_wheel()
        self.app.event_generate("<Control-Key-z>")
        self.app.event_generate("<Control-Key-z>")
        wheel.settings.number = 5
        wheel.draw_wheel()
        self.assertEqual(wheel.settings.number, 5)
        self.app.event_generate("<Control-Key-z>")
        self.assertEqual(wheel.settings.number, 2)



# atexti
# config

if __name__ == '__main__':
    unittest.main()
