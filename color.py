from colormath.color_objects import (LCHuvColor, LCHabColor, HSLColor,
                                     HSVColor, IPTColor, sRGBColor)
from colormath.color_conversions import convert_color
from math import radians, cos, sin


def fix_values(r, g, b):
    if r > 255: r = 255
    if r < 0:   r = 0
    if g > 255: g = 255
    if g < 0:   g = 0
    if b > 255: b = 255
    if b < 0:   b = 0
    return r, g, b


def lchab(l, c, h):
    value = convert_color(LCHabColor(l, c, h), sRGBColor)
    return value.get_upscaled_value_tuple()


def lchuv(l, c, h):
    value = convert_color(LCHuvColor(l, c, h), sRGBColor)
    return value.get_upscaled_value_tuple()


def hsl(l, c, h):
    value = convert_color(HSLColor(h, c/100, l/100), sRGBColor)
    return value.get_upscaled_value_tuple()


def hsv(l, c, h):
    value = convert_color(HSVColor(h, c/100, l/100), sRGBColor)
    return value.get_upscaled_value_tuple()


def ipt(l, c, h):
    i = l/100
    p = c/100*cos(radians(h))
    t = c/100*sin(radians(h))
    value = convert_color(IPTColor(i, p, t), sRGBColor)
    return value.get_upscaled_value_tuple()


def create_system(space):
    def hex_colors(start, amount, saturation, luminosity):
        c = saturation
        l = luminosity
        k = 360/amount
        ans = (space(l, c, start + i*k) for i in range(amount))
        ans = (fix_values(r, g, b) for r, g, b in ans)
        ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
        return ans
    return hex_colors


space = {
    "Lab":create_system(lchab),
    "Luv":create_system(lchuv),
    "HSL":create_system(hsl),
    "HSV":create_system(hsv),
    "IPT": create_system(ipt),
}
