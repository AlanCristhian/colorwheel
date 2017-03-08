from colormath.color_objects import (LCHuvColor, LCHabColor, HSLColor,
                                     HSVColor, IPTColor, sRGBColor)
from colormath.color_conversions import convert_color
from math import radians, cos, sin


def lchab(l, c, h):
    return convert_color(LCHabColor(l, c, h), sRGBColor)


def lchuv(l, c, h):
    return convert_color(LCHuvColor(l, c, h), sRGBColor)


def hsl(l, c, h):
    return convert_color(HSLColor(h, c/100, l/100), sRGBColor)


def hsv(l, c, h):
    return convert_color(HSVColor(h, c/100, l/100), sRGBColor)


def ipt(l, c, h):
    i = l/100
    p = c/100*cos(radians(h))
    t = c/100*sin(radians(h))
    return convert_color(IPTColor(i, p, t), sRGBColor)


def create_system(space):
    def hex_colors(start, amount, saturation, luminosity):
        c = saturation
        l = luminosity
        k = 360/amount
        ans = (space(l, c, start + i*k) for i in range(amount))
        ans = ((v.clamped_rgb_r, v.clamped_rgb_g,v.clamped_rgb_b) for v in ans)
        ans = ((round(r*255), round(g*255), round(b*255)) for r, g, b in ans)
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
