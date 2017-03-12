import unittest
from unittest import mock
import tkinter
from tkinter import ttk

import file


class BaseSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tkinter.Tk()

    @classmethod
    def tearDownClass(cls):
        cls.root.update_idletasks()
        cls.root.destroy()
        del cls.root


class SettingsFrameSuit(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.settings = file.SettingsFrame(cls.root, "Ajustes de la rueda")
        cls.settings.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.settings.destroy()
        del cls.settings
        super().tearDownClass()

    def test_settings_instance(self):
        self.assertIsInstance(self.settings, file.SettingsFrame)
        self.assertTrue(self.settings.winfo_manager())

    # number

    def test_number_var(self):
        self.assertIsInstance(self.settings.number_var, tkinter.IntVar)

    def test_number_label(self):
        self.assertIsInstance(self.settings.number_label, tkinter.Label)
        self.assertEqual(self.settings.number_label["text"], "Cantidad:")
        self.assertTrue(self.settings.number_label.winfo_manager())

    def test_number_entry(self):
        self.assertIsInstance(self.settings.number_entry, tkinter.Entry)
        self.assertTrue(self.settings.number_entry.winfo_manager())

    def test_number_scale(self):
        self.assertIsInstance(self.settings.number_scale, tkinter.Scale)
        self.assertTrue(self.settings.number_scale.winfo_manager())

    # start

    def test_start_var(self):
        self.assertIsInstance(self.settings.start_var, tkinter.IntVar)

    def test_start_label(self):
        self.assertIsInstance(self.settings.start_label, tkinter.Label)
        self.assertEqual(self.settings.start_label["text"], "Empezar en:")
        self.assertTrue(self.settings.start_label.winfo_manager())

    def test_start_entry(self):
        self.assertIsInstance(self.settings.start_entry, tkinter.Entry)
        self.assertTrue(self.settings.start_entry.winfo_manager())

    def test_start_scale(self):
        self.assertIsInstance(self.settings.start_scale, tkinter.Scale)
        self.assertTrue(self.settings.start_scale.winfo_manager())

    # saturation

    def test_saturation_var(self):
        self.assertIsInstance(self.settings.saturation_var, tkinter.IntVar)

    def test_saturation_label(self):
        self.assertIsInstance(self.settings.saturation_label, tkinter.Label)
        self.assertEqual(self.settings.saturation_label["text"],
                         "Saturación:")
        self.assertTrue(self.settings.saturation_label.winfo_manager())

    def test_saturation_entry(self):
        self.assertIsInstance(self.settings.saturation_entry, tkinter.Entry)
        self.assertTrue(self.settings.saturation_entry.winfo_manager())

    def test_saturation_scale(self):
        self.assertIsInstance(self.settings.saturation_scale, tkinter.Scale)
        self.assertTrue(self.settings.saturation_scale.winfo_manager())

    # luminosity

    def test_luminosity_var(self):
        self.assertIsInstance(self.settings.luminosity_var, tkinter.IntVar)

    def test_luminosity_label(self):
        self.assertIsInstance(self.settings.luminosity_label, tkinter.Label)
        self.assertEqual(self.settings.luminosity_label["text"],
                         "Luminosidad:")
        self.assertTrue(self.settings.luminosity_label.winfo_manager())

    def test_luminosity_entry(self):
        self.assertIsInstance(self.settings.luminosity_entry, tkinter.Entry)
        self.assertTrue(self.settings.luminosity_entry.winfo_manager())

    def test_luminosity_scale(self):
        self.assertIsInstance(self.settings.luminosity_scale, tkinter.Scale)
        self.assertTrue(self.settings.luminosity_scale.winfo_manager())


class ViewSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = file.ViewFrame(cls.root, text="Visualización")
        cls.view.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.view.destroy()
        del cls.view
        super().tearDownClass()

    # view frame

    def test_view_frame(self):
        self.assertIsInstance(self.view, tkinter.LabelFrame)
        self.assertEqual(self.view["text"], "Visualización")
        self.assertTrue(self.view.winfo_manager())

    # background

    def test_background_var(self):
        self.assertIsInstance(self.view.background_var, tkinter.StringVar)

    def test_background_label(self):
        self.assertIsInstance(self.view.background_label, tkinter.Label)
        self.assertEqual(self.view.background_label["text"], "Color de fondo:")
        self.assertTrue(self.view.background_label.winfo_manager())

    def test_background_entry(self):
        self.assertIsInstance(self.view.background_entry, tkinter.Entry)
        self.assertTrue(self.view.background_entry.winfo_manager())

    # outline

    def test_outline_var(self):
        self.assertIsInstance(self.view.outline_var, tkinter.IntVar)

    def test_outline_checkbutton(self):
        self.assertIsInstance(self.view.outline_checkbutton,
                              tkinter.Checkbutton)
        self.assertEqual(self.view.outline_checkbutton["text"],
                         " Contorno")
        self.assertTrue(self.view.outline_checkbutton.winfo_manager())


class SpaceSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.space = file.ColorSpaceFrame(cls.root, "Espacio de color")
        cls.space.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.space.destroy()
        del cls.space
        super().tearDownClass()

    def test_color_space_frame(self):
        self.assertIsInstance(self.space, file.ColorSpaceFrame)
        self.assertEqual(self.space["text"], "Espacio de color")
        self.assertTrue(self.space.winfo_manager())

    def test_color_space_var(self):
        self.assertIsInstance(self.space.color_space_var, tkinter.StringVar)

    def test_lchab_radiobutton(self):
        self.assertIsInstance(self.space.lchab_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.space.lchab_radiobutton["text"], "Lab")
        self.assertTrue(self.space.lchab_radiobutton.winfo_manager())

    def test_lchuv_radiobutton(self):
        self.assertIsInstance(self.space.lchuv_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.space.lchuv_radiobutton["text"], "Luv")
        self.assertTrue(self.space.lchuv_radiobutton.winfo_manager())

    def test_hsl_radiobutton(self):
        self.assertIsInstance(self.space.hsl_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.space.hsl_radiobutton["text"], "HSL")
        self.assertTrue(self.space.hsl_radiobutton.winfo_manager())

    def test_hsv_radiobutton(self):
        self.assertIsInstance(self.space.hsv_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.space.hsv_radiobutton["text"], "HSV")
        self.assertTrue(self.space.hsv_radiobutton.winfo_manager())

    def test_ipt_radiobutton(self):
        self.assertIsInstance(self.space.ipt_radiobutton, tkinter.Radiobutton)
        self.assertEqual(self.space.ipt_radiobutton["text"], "IPT")
        self.assertTrue(self.space.ipt_radiobutton.winfo_manager())


class DataSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = file.DataFrame(cls.root)
        cls.data.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.data.destroy()
        del cls.data
        super().tearDownClass()

    def setUp(self):
        self.data.delete_all()

    def test_data_frame(self):
        self.assertIsInstance(self.data, file.DataFrame)
        self.assertTrue(self.data.winfo_manager())

    def test_color_treeview(self):
        self.assertIsInstance(self.data.color_treeview, ttk.Treeview)
        self.assertTrue(self.data.color_treeview.winfo_manager())

    def test_hexrgb_treeview(self):
        self.assertIsInstance(self.data.hexrgb_treeview, ttk.Treeview)
        self.assertTrue(self.data.hexrgb_treeview.winfo_manager())

    def test_hexrgba_treeview(self):
        self.assertIsInstance(self.data.hexrgba_treeview, ttk.Treeview)
        self.assertTrue(self.data.hexrgba_treeview.winfo_manager())

    def test_r_treeview(self):
        self.assertIsInstance(self.data.r_treeview, ttk.Treeview)
        self.assertTrue(self.data.r_treeview.winfo_manager())

    def test_g_treeview(self):
        self.assertIsInstance(self.data.g_treeview, ttk.Treeview)
        self.assertTrue(self.data.g_treeview.winfo_manager())

    def test_b_treeview(self):
        self.assertIsInstance(self.data.b_treeview, ttk.Treeview)
        self.assertTrue(self.data.b_treeview.winfo_manager())

    def test_scroll(self):
        self.assertIsInstance(self.data.scroll, tkinter.Scrollbar)
        self.assertTrue(self.data.scroll.winfo_manager())

    def test_insert_method(self):
        self.data.insert("#aaaaaa", 255, 128, 64)
        for line in self.data.color_treeview.get_children():
            self.assertEqual(self.data.color_treeview.item(line)["tags"],
                             ["aaaaaa"])
            self.assertEqual(self.data.color_treeview.item(line)["values"],
                             [""])
        for line in self.data.hexrgb_treeview.get_children():
            self.assertEqual(self.data.hexrgb_treeview.item(line)["values"],
                             ["aaaaaa"])
        for line in self.data.hexrgba_treeview.get_children():
            self.assertEqual(self.data.hexrgba_treeview.item(line)["values"],
                             ["aaaaaaff"])
        for line in self.data.r_treeview.get_children():
            self.assertEqual(self.data.r_treeview.item(line)["values"], [255])
        for line in self.data.g_treeview.get_children():
            self.assertEqual(self.data.g_treeview.item(line)["values"], [128])
        for line in self.data.b_treeview.get_children():
            self.assertEqual(self.data.b_treeview.item(line)["values"], [64])

    def test_delete_all_method(self):
        self.data.insert("#aaaaaa", 255, 128, 64)
        self.data.delete_all()
        self.assertEqual(self.data.color_treeview.get_children(), ())
        self.assertEqual(self.data.hexrgb_treeview.get_children(), ())
        self.assertEqual(self.data.hexrgba_treeview.get_children(), ())
        self.assertEqual(self.data.r_treeview.get_children(), ())
        self.assertEqual(self.data.g_treeview.get_children(), ())
        self.assertEqual(self.data.b_treeview.get_children(), ())

    def test_copy_data_method(self):
        self.data.insert("#aaaaaa", 255, 128, 64)

        index = self.data.hexrgb_treeview.get_children()[0]
        self.data.hexrgb_treeview.selection_set(index)
        self.data.hexrgb_treeview.focus_set()
        self.data.hexrgb_treeview.focus(index)
        self.data.copy_hexrgb_data(None)
        self.assertEqual(self.data.clipboard_get(), "aaaaaa")

        index = self.data.hexrgba_treeview.get_children()[0]
        self.data.hexrgba_treeview.selection_set(index)
        self.data.hexrgba_treeview.focus_set()
        self.data.hexrgba_treeview.focus(index)
        self.data.copy_hexrgba_data(None)
        self.assertEqual(self.data.clipboard_get(), "aaaaaaff")

        index = self.data.r_treeview.get_children()[0]
        self.data.r_treeview.selection_set(index)
        self.data.r_treeview.focus_set()
        self.data.r_treeview.focus(index)
        self.data.copy_r_data(None)
        self.assertEqual(self.data.clipboard_get(), "255")

        index = self.data.g_treeview.get_children()[0]
        self.data.g_treeview.selection_set(index)
        self.data.g_treeview.focus_set()
        self.data.g_treeview.focus(index)
        self.data.copy_g_data(None)
        self.assertEqual(self.data.clipboard_get(), "128")

        index = self.data.b_treeview.get_children()[0]
        self.data.b_treeview.selection_set(index)
        self.data.b_treeview.focus_set()
        self.data.b_treeview.focus(index)
        self.data.copy_b_data(None)
        self.assertEqual(self.data.clipboard_get(), "64")

    def test_set_yview_method(self):
        self.data.set_yview("moveto", 1.0)
        self.assertEqual(self.data.color_treeview.yview(), (0.0, 1.0))
        self.assertEqual(self.data.hexrgb_treeview.yview(), (0.0, 1.0))
        self.assertEqual(self.data.hexrgba_treeview.yview(), (0.0, 1.0))
        self.assertEqual(self.data.r_treeview.yview(), (0.0, 1.0))
        self.assertEqual(self.data.g_treeview.yview(), (0.0, 1.0))
        self.assertEqual(self.data.b_treeview.yview(), (0.0, 1.0))

    def test_set_scroll_method(self):
        self.data.set_scroll(1, 1)
        self.assertEqual(self.data.scroll.get(), (1.0, 1.0))


class MixerSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mixer = file.MixerFrame(cls.root, "Mezclador de colores")
        cls.mixer.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.mixer.destroy()
        del cls.mixer
        super().tearDownClass()

    def test_mixer_instance(self):
        self.assertIsInstance(self.mixer, file.MixerFrame)
        self.assertTrue(self.mixer.winfo_manager())

    def test_color1_var(self):
        self.assertIsInstance(self.mixer.color1_var, tkinter.StringVar)

    def test_color2_var(self):
        self.assertIsInstance(self.mixer.color2_var, tkinter.StringVar)

    def test_color3_var(self):
        self.assertIsInstance(self.mixer.color3_var, tkinter.StringVar)

    def test_color1_entry(self):
        self.assertIsInstance(self.mixer.color1_entry, tkinter.Entry)
        self.assertTrue(self.mixer.color1_entry.winfo_manager())

    def test_color2_entry(self):
        self.assertIsInstance(self.mixer.color2_entry, tkinter.Entry)
        self.assertTrue(self.mixer.color2_entry.winfo_manager())

    def test_color3_entry(self):
        self.assertIsInstance(self.mixer.color3_entry, tkinter.Entry)
        self.assertTrue(self.mixer.color3_entry.winfo_manager())

    def test_color1_label(self):
        self.assertIsInstance(self.mixer.color1_label, tkinter.Label)
        self.assertEqual(self.mixer.color1_label["text"], "")
        self.assertTrue(self.mixer.color1_label.winfo_manager())

    def test_color2_label(self):
        self.assertIsInstance(self.mixer.color2_label, tkinter.Label)
        self.assertEqual(self.mixer.color2_label["text"], "")
        self.assertTrue(self.mixer.color2_label.winfo_manager())

    def test_color3_label(self):
        self.assertIsInstance(self.mixer.color3_label, tkinter.Label)
        self.assertEqual(self.mixer.color3_label["text"], "")
        self.assertTrue(self.mixer.color3_label.winfo_manager())

    def test_plus_label(self):
        self.assertIsInstance(self.mixer.plus_label, tkinter.Label)
        self.assertEqual(self.mixer.plus_label["text"], "+")
        self.assertTrue(self.mixer.plus_label.winfo_manager())

    def test_equal_label(self):
        self.assertIsInstance(self.mixer.equal_label, tkinter.Label)
        self.assertEqual(self.mixer.equal_label["text"], "=")
        self.assertTrue(self.mixer.equal_label.winfo_manager())

    # def test_mixer(self):
    #     self.mixer.color1_var.set("#98c345")
    #     self.mixer.color2_var.set("#00cb85")
    #     self.mixer.color1_entry.event_generate("<Return>")
    #     self.assertEqual(self.mixer.color3_var.get(), "#6dc767")


class FileSuite(BaseSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = file.File(cls.root)
        cls.app.grid(row=0, column=0)

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()
        del cls.app
        super().tearDownClass()

    def test_canvas(self):
        self.assertIsInstance(self.app.canvas, tkinter.Canvas)
        self.assertTrue(self.app.canvas.winfo_manager())

    def test_wheel_settings(self):
        self.assertIsInstance(self.app.settings, tkinter.LabelFrame)
        self.assertEqual(self.app.settings["text"],
                         "Ajustes de la rueda")
        self.assertTrue(self.app.settings.winfo_manager())

    def test_color_space(self):
        self.assertIsInstance(self.app.color_space, file.ColorSpaceFrame)
        self.assertEqual(self.app.color_space["text"], "Espacio de color")
        self.assertTrue(self.app.color_space.winfo_manager())

    def test_data(self):
        self.assertIsInstance(self.app.data, file.DataFrame)
        self.assertTrue(self.app.data.winfo_manager())

    def test_history(self):
        self.app.draw_wheel()
        expected = file.HistoryData(
            number=360,
            start=0,
            saturation=50,
            luminosity=50,
            background="gray20",
            color_space="HSL",
            outline=False,
        )
        self.assertEqual(self.app.history[0], expected)


if __name__ == '__main__':
    unittest.main()
