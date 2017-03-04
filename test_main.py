import unittest
import tkinter
from tkinter import ttk

import main
import file


class BaseSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tkinter.Tk()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()
        del cls.root


class FileSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = file.File(cls.root)

    # canvas
    # ======

    def test_canvas(self):
        self.assertIsInstance(self.app.canvas, tkinter.Canvas)
        self.assertTrue(self.app.canvas.winfo_manager())


    # ==============
    # wheel settings
    # ==============

    def test_wheel_settings(self):
        self.assertIsInstance(self.app.settings_frame, tkinter.LabelFrame)
        self.assertEqual(self.app.settings_frame["text"],
                         "Ajustes de la rueda")
        self.assertTrue(self.app.settings_frame.winfo_manager())

    # numbrer
    # =======

    def test_number_var(self):
        self.assertIsInstance(self.app.number_var, tkinter.IntVar)

    def test_number_label(self):
        self.assertIsInstance(self.app.number_label, tkinter.Label)
        self.assertEqual(self.app.number_label["text"], "Cantidad:")
        self.assertTrue(self.app.number_label.winfo_manager())

    def test_number_entry(self):
        self.assertIsInstance(self.app.number_entry, tkinter.Entry)
        self.assertTrue(self.app.number_entry.winfo_manager())

    def test_number_scale(self):
        self.assertIsInstance(self.app.number_scale, tkinter.Scale)
        self.assertTrue(self.app.number_scale.winfo_manager())

    # start
    # =====

    def test_start_var(self):
        self.assertIsInstance(self.app.start_var, tkinter.IntVar)

    def test_start_label(self):
        self.assertIsInstance(self.app.start_label, tkinter.Label)
        self.assertEqual(self.app.start_label["text"], "Empezar en:")
        self.assertTrue(self.app.start_label.winfo_manager())

    def test_start_entry(self):
        self.assertIsInstance(self.app.start_entry, tkinter.Entry)
        self.assertTrue(self.app.start_entry.winfo_manager())

    def test_start_scale(self):
        self.assertIsInstance(self.app.start_scale, tkinter.Scale)
        self.assertTrue(self.app.start_scale.winfo_manager())

    # saturation
    # ==========

    def test_saturation_var(self):
        self.assertIsInstance(self.app.saturation_var, tkinter.IntVar)

    def test_saturation_label(self):
        self.assertIsInstance(self.app.saturation_label, tkinter.Label)
        self.assertEqual(self.app.saturation_label["text"],
                         "Saturación:")
        self.assertTrue(self.app.saturation_label.winfo_manager())

    def test_saturation_entry(self):
        self.assertIsInstance(self.app.saturation_entry, tkinter.Entry)
        self.assertTrue(self.app.saturation_entry.winfo_manager())

    def test_saturation_scale(self):
        self.assertIsInstance(self.app.saturation_scale, tkinter.Scale)
        self.assertTrue(self.app.saturation_scale.winfo_manager())

    # luminosity
    # ==========

    def test_luminosity_var(self):
        self.assertIsInstance(self.app.luminosity_var, tkinter.IntVar)

    def test_luminosity_label(self):
        self.assertIsInstance(self.app.luminosity_label, tkinter.Label)
        self.assertEqual(self.app.luminosity_label["text"],
                         "Luminosidad:")
        self.assertTrue(self.app.luminosity_label.winfo_manager())

    def test_luminosity_entry(self):
        self.assertIsInstance(self.app.luminosity_entry, tkinter.Entry)
        self.assertTrue(self.app.luminosity_entry.winfo_manager())

    def test_luminosity_scale(self):
        self.assertIsInstance(self.app.luminosity_scale, tkinter.Scale)
        self.assertTrue(self.app.luminosity_scale.winfo_manager())

    # ==========
    # view frame
    # ==========

    def test_view_frame(self):
        self.assertIsInstance(self.app.view_frame, tkinter.LabelFrame)
        self.assertEqual(self.app.view_frame["text"], "Visualización")
        self.assertTrue(self.app.view_frame.winfo_manager())

    # background
    # ==========

    def test_background_var(self):
        self.assertIsInstance(self.app.background_var, tkinter.StringVar)

    def test_background_label(self):
        self.assertIsInstance(self.app.background_label, tkinter.Label)
        self.assertEqual(self.app.background_label["text"], "Color de fondo:")
        self.assertTrue(self.app.background_label.winfo_manager())

    def test_background_entry(self):
        self.assertIsInstance(self.app.background_entry, tkinter.Entry)
        self.assertTrue(self.app.background_entry.winfo_manager())

    # outline
    # =======

    def test_outline_var(self):
        self.assertIsInstance(self.app.outline_var, tkinter.IntVar)

    def test_outline_checkbutton(self):
        self.assertIsInstance(self.app.outline_checkbutton,
                              tkinter.Checkbutton)
        self.assertEqual(self.app.outline_checkbutton["text"],
                         " Dibujar contorno")
        self.assertTrue(self.app.outline_checkbutton.winfo_manager())

    # ===========
    # space frame
    # ===========

    def test_color_space_frame(self):
        self.assertIsInstance(self.app.color_space_frame, tkinter.LabelFrame)
        self.assertEqual(self.app.color_space_frame["text"], "Espacio de color")
        self.assertTrue(self.app.color_space_frame.winfo_manager())

    # color space
    # ===========

    def test_color_space_var(self):
        self.assertIsInstance(self.app.color_space_var, tkinter.StringVar)

    def test_lchab_radiobutton(self):
        self.assertIsInstance(self.app.lchab_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.app.lchab_radiobutton["text"], "Lab")
        self.assertTrue(self.app.lchab_radiobutton.winfo_manager())

    def test_lchuv_radiobutton(self):
        self.assertIsInstance(self.app.lchuv_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.app.lchuv_radiobutton["text"], "Luv")
        self.assertTrue(self.app.lchuv_radiobutton.winfo_manager())

    def test_hsl_radiobutton(self):
        self.assertIsInstance(self.app.hsl_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.app.hsl_radiobutton["text"], "HSL")
        self.assertTrue(self.app.hsl_radiobutton.winfo_manager())

    def test_hsv_radiobutton(self):
        self.assertIsInstance(self.app.hsv_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.app.hsv_radiobutton["text"], "HSV")
        self.assertTrue(self.app.hsv_radiobutton.winfo_manager())

    def test_ipt_radiobutton(self):
        self.assertIsInstance(self.app.ipt_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.app.ipt_radiobutton["text"], "IPT")
        self.assertTrue(self.app.ipt_radiobutton.winfo_manager())

    # ==========
    # data frame
    # ==========

    def test_data_frame(self):
        self.assertIsInstance(self.app.data_frame, tkinter.Frame)
        self.assertTrue(self.app.data_frame.winfo_manager())

    def test_color_treeview(self):
        self.assertIsInstance(self.app.color_treeview, ttk.Treeview)
        self.assertTrue(self.app.color_treeview.winfo_manager())

    def test_hexrgb_treeview(self):
        self.assertIsInstance(self.app.hexrgb_treeview, ttk.Treeview)
        self.assertTrue(self.app.hexrgb_treeview.winfo_manager())

    def test_hexrgba_treeview(self):
        self.assertIsInstance(self.app.hexrgba_treeview, ttk.Treeview)
        self.assertTrue(self.app.hexrgba_treeview.winfo_manager())

    def test_r_treeview(self):
        self.assertIsInstance(self.app.r_treeview, ttk.Treeview)
        self.assertTrue(self.app.r_treeview.winfo_manager())

    def test_g_treeview(self):
        self.assertIsInstance(self.app.g_treeview, ttk.Treeview)
        self.assertTrue(self.app.g_treeview.winfo_manager())

    def test_b_treeview(self):
        self.assertIsInstance(self.app.b_treeview, ttk.Treeview)
        self.assertTrue(self.app.b_treeview.winfo_manager())

    def test_data_scroll(self):
        self.assertIsInstance(self.app.data_scroll, tkinter.Scrollbar)
        self.assertTrue(self.app.data_scroll.winfo_manager())


"""
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
        self.app.

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
"""


if __name__ == '__main__':
    unittest.main()
