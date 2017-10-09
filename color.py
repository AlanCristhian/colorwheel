from math import radians, cos, sin

from colormath.color_objects import (LCHuvColor, LCHabColor, HSLColor,
                                     HSVColor, IPTColor, sRGBColor,
                                     XYZColor)
from colormath.color_conversions import convert_color
from colorspacious import cspace_convert


def to_hex_rgb(gen):
    ans = ((v.clamped_rgb_r, v.clamped_rgb_g,v.clamped_rgb_b) for v in gen)
    ans = ((round(r*255), round(g*255), round(b*255)) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


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
        k = 360/amount
        ans = (space(luminosity, saturation, start+i*k) for i in range(amount))
        return to_hex_rgb(ans)
    return hex_colors


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def hex_to_space(color, space):
    color_tuple = hex_to_rgb(color)
    values = list(i/255 for i in color_tuple)
    return convert_color(sRGBColor(*values), space).get_value_tuple()


def create_mixer(space):
    def mix(color1, color2):
        x1, y1, z1 = hex_to_space(color1, space)
        x2, y2, z2 = hex_to_space(color2, space)
        color3 = space((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
        ans = convert_color(color3, sRGBColor)
        ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
        ans = tuple(round(i*255) for i in ans)
        return "#%02x%02x%02x" % ans
    return mix


def jch(start, amount, saturation, luminosity):
    k = 360/amount
    ans = ((luminosity, saturation, start + i*k) for i in range(amount))
    ans = (cspace_convert(color, "JCh", "sRGB1") for color in ans)
    ans = (color.tolist() for color in ans)
    ans = (sRGBColor(*color) for color in ans)
    return to_hex_rgb(ans)


def jch_mixer(color1, color2):
    rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
    x1, y1, z1 = cspace_convert(rgb1, "sRGB255", "JCh").tolist()
    x2, y2, z2 = cspace_convert(rgb2, "sRGB255", "JCh").tolist()
    ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
    ans = cspace_convert(ans, "JCh", "sRGB1").tolist()
    ans = sRGBColor(*ans)
    ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
    ans = tuple(round(i*255) for i in ans)
    return "#%02x%02x%02x" % ans


def ipt_jch(start, amount, saturation, luminosity):
    # Generate colors
    k = 360/amount
    colors = [(luminosity, saturation, start + i*k) for i in range(amount)]

    # From lch to IPT
    ans = ((l/100, c/100*cos(radians(h)), c/100*sin(radians(h)))
           for l, c, h in colors)

    # From IPT to XYZ1
    ans = (convert_color(IPTColor(i, p, t), XYZColor, target_illuminant="d65")
           for i, p, t in ans)
    ipt_colors = (color.get_value_tuple() for color in ans)

    # From JCh to XYZ1
    ans = (cspace_convert(color, "JCh", "XYZ1") for color in colors)
    jch_colors = (color.tolist() for color in ans)

    # Compute average
    ans = (((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
           for (x1, y1, z1), (x2, y2, z2)
           in zip(ipt_colors, jch_colors))

    # From XYZ1 to sRGB1
    ans = (cspace_convert(color, "XYZ1", "sRGB1") for color in ans)
    ans = ((color.tolist() for color in ans))
    ans = (sRGBColor(*color) for color in ans)

    return to_hex_rgb(ans)


space = {
    "Lab": create_system(lchab),
    "Luv": create_system(lchuv),
    "HSL": create_system(hsl),
    "HSV": create_system(hsv),
    "IPT": create_system(ipt),
    "JCh": jch,
    "IPT+JCh": ipt_jch,
}


mixer = {
    "Lab": create_mixer(LCHabColor),
    "Luv": create_mixer(LCHuvColor),
    "HSL": create_mixer(HSLColor),
    "HSV": create_mixer(HSLColor),
    "IPT": create_mixer(IPTColor),
    "JCh": jch_mixer,
}
