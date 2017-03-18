import unittest
import tkinter as tk
from tkinter import ttk

import toolbar


class ToolBarSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master = tk.Tk()
        cls.toolbar = toolbar.ToolBar(cls.master)
        cls.toolbar.grid()

    @classmethod
    def tearDownClass(cls):
        cls.toolbar.destroy()
        del cls.toolbar
        cls.master.update_idletasks()
        cls.master.destroy()
        del cls.master

    def test_toolbar_instance(self):
        self.assertIsInstance(self.toolbar, ttk.Frame)

    def test_two_buttons_with_the_same_name(self):
        self.toolbar.append(name="name0")
        message = "The name 'name0' already exists."
        with self.assertRaisesRegex(ValueError, message):
            self.toolbar.append(name="name0")

    def test_button_instance(self):
        self.toolbar.append(name="name1")
        self.assertIsInstance(self.toolbar.button["name1"], tk.Button)

    def test_button_label(self):
        self.toolbar.append(name="name2", label="Button 2")
        self.assertEqual(self.toolbar.button["name2"]["text"], "Button 2")

    def test_button_image(self):
        self.toolbar.append(name="name3", label="Button 3",
                            image="new.png")
        self.assertIsInstance(self.toolbar.image["name3"], tk.PhotoImage)
        self.assertEqual(self.toolbar.button["name3"]["image"], "name3")

    def test_button_command(self):
        value = 5
        def function():
            nonlocal value
            value = 10
        self.toolbar.append(name="name4", label="Button 4", command=function)
        self.toolbar.button["name4"].invoke()
        self.assertEqual(value, 10)

    def test_visibility(self):
        self.toolbar.grid()
        for i in self.toolbar.button:
            with self.subTest(name=i):
                self.assertTrue(self.toolbar.button[i].winfo_manager())


if __name__ == '__main__':
    unittest.main()
