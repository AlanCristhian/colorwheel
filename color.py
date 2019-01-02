from math import radians, cos, sin, sqrt, radians, pow
import colorsys


from colormath.color_objects import (LCHuvColor, LCHabColor, HSLColor,
                                     HSVColor, IPTColor, sRGBColor,
                                     XYZColor, AdobeRGBColor)
from colormath.color_conversions import convert_color
from colorspacious import cspace_convert, CAM02UCS, CAM02SCD, CAM02LCD


def _rgb1_to_rgb255(r, g, b):
    return round(r*255), round(g*255), round(b*255)


def _hls_to_yiq(H, L, S):
    y = L/100
    i = S/100*cos(radians(H))
    q = S/100*sin(radians(H))
    return y, i, q


def yiq(start, amount, saturation, luminosity):
    step = 360/amount
    ans = ((start + i*step, luminosity, saturation) for i in range(amount))
    ans = (_hls_to_yiq(H, L, S) for H, L, S in ans)
    ans = (colorsys.yiq_to_rgb(y, i, q) for y, i, q in ans)
    ans = (_rgb1_to_rgb255(r, g, b) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


def yiq_mixer(color1, color2):
    rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
    x1, y1, z1 = colorsys.rgb_to_hls(rgb1)
    x2, y2, z2 = colorsys.rgb_to_hls(rgb2)
    ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
    ans = _hls_to_yiq(*ans)
    ans = colorsys.yiq_to_rgb(*ans)
    return "#%02x%02x%02x" % ans


def _hls_to_ycbcr(H, L, S):
    Y = L/100
    Cb = S/100*cos(radians(H))
    Cr = S/100*sin(radians(H))
    return Y, Cb, Cr


def _rgb1_to_rgb255(r, g, b):
    return round(r*255), round(g*255), round(b*255)


def _ycbcr_to_rgb(Y, Cb, Cr):
    r = Y - 0.000170345404941155*Cb +    1.40214249139129*Cr
    g = Y -    0.345602379281664*Cb -    0.71447536324549*Cr
    b = Y +     1.77101547535512*Cb + 9.48244798877522e-5*Cr
    r = 0 if r < 0 else 1 if r > 1 else r
    g = 0 if g < 0 else 1 if g > 1 else g
    b = 0 if b < 0 else 1 if b > 1 else b
    return r, g, b


def cat02(start, amount, saturation, luminosity):
    step = 360/amount
    ans = ((start + i*step, luminosity, saturation) for i in range(amount))
    ans = (_hls_to_ycbcr(H, L, S) for H, L, S in ans)
    ans = (_ycbcr_to_rgb(Y, Cb, Cr) for Y, Cb, Cr in ans)
    ans = (_rgb1_to_rgb255(r, g, b) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


def _ycbcr_to_rgb_2(Y, Cb, Cr):
    r = -7.65413663080094*Cb + 3.07695666724817*Cr + 5.909003314299*Y
    g = 11.3940532344494*Cb - 2.46426433976758*Cr - 9.14035819725992*Y
    b = -2.73991660364845*Cb + 0.387307672519408*Cr + 4.23135488296092*Y
    r = 0 if r < 0 else 1 if r > 1 else r
    g = 0 if g < 0 else 1 if g > 1 else g
    b = 0 if b < 0 else 1 if b > 1 else b
    return r, g, b


def ycbcr(start, amount, saturation, luminosity):
    step = 360/amount
    ans = ((start + i*step, luminosity, saturation) for i in range(amount))
    ans = (_hls_to_ycbcr(H, L, S) for H, L, S in ans)
    ans = (_ycbcr_to_rgb_2(Y, Cb, Cr) for Y, Cb, Cr in ans)
    ans = (_rgb1_to_rgb255(r, g, b) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


def yuv_mixer(color1, color2):
    rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
    x1, y1, z1 = colorsys.rgb_to_hls(rgb1)
    x2, y2, z2 = colorsys.rgb_to_hls(rgb2)
    ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
    ans = _hls_to_yuv(*ans)
    ans = _yuv_to_rgb(*ans)
    return "#%02x%02x%02x" % ans


def to_hex_rgb(gen):
    ans = ((v.clamped_rgb_r, v.clamped_rgb_g,v.clamped_rgb_b) for v in gen)
    ans = ((round(r*255), round(g*255), round(b*255)) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


def lchab(l, c, h):
    return convert_color(LCHabColor(l, c, h), sRGBColor, target_illuminant="d65")


def lchuv(l, c, h):
    return convert_color(LCHuvColor(l, c, h), sRGBColor, target_illuminant="d65")


def hsl(l, c, h):
    return convert_color(HSLColor(h, c/100, l/100), sRGBColor, target_illuminant="d65")


def hsv(l, c, h):
    return convert_color(HSVColor(h, c/100, l/100), sRGBColor, target_illuminant="d65")


def ipt(l, c, h):
    i = l/100
    p = c/100*cos(radians(h))
    t = c/100*sin(radians(h))
    return convert_color(IPTColor(i, p, t), sRGBColor, target_illuminant="d65")


def bt2020color(l, c, h):
    return convert_color(BT2020Color(h, c/100, l/100), sRGBColor, target_illuminant="d65")


def create_system(space):
    def hex_colors(start, amount, saturation, luminosity):
        k = 360/amount
        ans = (space(luminosity, saturation, start + i*k) for i in range(amount))
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
    return convert_color(sRGBColor(*values), space, target_illuminant="d65").get_value_tuple()


def create_mixer(space):
    def mix(color1, color2):
        x1, y1, z1 = hex_to_space(color1, space)
        x2, y2, z2 = hex_to_space(color2, space)
        color3 = space((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
        ans = convert_color(color3, sRGBColor, target_illuminant="d65")
        ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
        ans = tuple(round(i*255) for i in ans)
        return "#%02x%02x%02x" % ans
    return mix


def jch(start, amount, saturation, luminosity):
    k = 360/amount
    ans = ((luminosity, saturation, start + i*k) for i in range(amount))
    ans = (cspace_convert(color, "JCh", "XYZ1") for color in ans)
    ans = (XYZColor(*color.tolist()) for color in ans)
    ans = (convert_color(color, AdobeRGBColor, target_illuminant="d65") for color in ans)
    ans = ((color.clamped_rgb_r, color.clamped_rgb_g, color.clamped_rgb_b) for color in ans)
    ans = ((round(r*255), round(g*255), round(b*255)) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


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


def jmh(start, amount, saturation, luminosity):
    k = 360/amount
    ans = ((luminosity, saturation, start + i*k) for i in range(amount))
    ans = (cspace_convert(color, "JMh", "sRGB1") for color in ans)
    ans = (color.tolist() for color in ans)
    ans = (sRGBColor(*color) for color in ans)
    return to_hex_rgb(ans)


def jmh_mixer(color1, color2):
    rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
    x1, y1, z1 = cspace_convert(rgb1, "sRGB255", "JMh").tolist()
    x2, y2, z2 = cspace_convert(rgb2, "sRGB255", "JMh").tolist()
    ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
    ans = cspace_convert(ans, "JMh", "sRGB1").tolist()
    ans = sRGBColor(*ans)
    ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
    ans = tuple(round(i*255) for i in ans)
    return "#%02x%02x%02x" % ans


def jmh_mixer_2(*colors):
    n = len(colors)
    ans = (hex_to_rgb(color) for color in colors)
    ans = (cspace_convert(color, "sRGB255", "JMh") for color in ans)
    ans = (color.tolist() for color in ans)
    ans = zip(*ans)
    ans = (sum(items)/n for items in ans)
    return list(ans)


def create_cie_system(cie_string):
    def hex_colors(start, amount, saturation, luminosity):
        k = 360/amount
        ans = ((luminosity, saturation, start + i*k) for i in range(amount))
        ans = (cspace_convert(color, cie_string, "sRGB1") for color in ans)
        ans = (color.tolist() for color in ans)
        ans = (sRGBColor(*color) for color in ans)
        return to_hex_rgb(ans)
    return hex_colors


def create_cie_mixer(cie_string):
    def mix(color1, color2):
        rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
        x1, y1, z1 = cspace_convert(rgb1, "sRGB255", cie_string).tolist()
        x2, y2, z2 = cspace_convert(rgb2, "sRGB255", cie_string).tolist()
        ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
        ans = cspace_convert(ans, cie_string, "sRGB1").tolist()
        ans = sRGBColor(*ans)
        ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
        ans = tuple(round(i*255) for i in ans)
        return "#%02x%02x%02x" % ans
    return mix


def create_cam02_system(cie_string):
    def hex_colors(start, amount, saturation, luminosity):
        k = 360/amount
        ans = ((luminosity, saturation, start + i*k) for i in range(amount))
        ans = ((l, c*cos(radians(h)), c*sin(radians(h))) for l, c, h in ans)
        ans = (cspace_convert(color, cie_string, "sRGB1") for color in ans)
        ans = (color.tolist() for color in ans)
        ans = (sRGBColor(*color) for color in ans)
        return to_hex_rgb(ans)
    return hex_colors


def create_cam02_mixer(cie_string):
    def mix(color1, color2):
        rgb1, rgb2 = hex_to_rgb(color1), hex_to_rgb(color2)
        x1, y1, z1 = cspace_convert(rgb1, "sRGB255", cie_string).tolist()
        x2, y2, z2 = cspace_convert(rgb2, "sRGB255", cie_string).tolist()
        ans = ((x1 + x2)/2, (y1 + y2)/2 , (z1 + z2)/2)
        ans = cspace_convert(ans, cie_string, "sRGB1").tolist()
        ans = sRGBColor(*ans)
        ans = (ans.clamped_rgb_r, ans.clamped_rgb_g, ans.clamped_rgb_b)
        ans = tuple(round(i*255) for i in ans)
        return "#%02x%02x%02x" % ans
    return mix


RED = 0
YELLOW = 82.5
GREEN = 114.5
CYAN = 173
BLUE = 249
MAGENTA = 304
d_RY = YELLOW - RED
d_YG = GREEN - YELLOW
d_GC = CYAN - GREEN
d_CB = BLUE - CYAN
d_BM = MAGENTA - BLUE
d_M3 = 360 - MAGENTA
k_r = 0.299
k_g = 0.587
k_b = 0.114


def hsl1_to_rgb(h, s, l):
    s = s/100
    l = l/100
    c = (1 - abs(2*l - 1))*s
    m = l - c/2
    if RED  <= h <= YELLOW:
        x = c*(1 - abs((h/d_RY)%2 - 1))
        r, g, b = (c + m, x + m, m)
    elif YELLOW  < h <= GREEN:
        x = c*(1 - abs(((GREEN - h)/d_YG)%2 - 1))
        r, g, b = (x + m, c + m, m)
    elif GREEN < h <= CYAN:
        x = c*(1 - abs(((GREEN - h)/d_GC)%2 - 1))
        r, g, b = (m, c + m, x + m)
    elif CYAN < h <= BLUE:
        x = c*(1 - abs(((BLUE - h)/d_CB)%2 - 1))
        r, g, b = (m, x + m, c + m)
    elif BLUE < h <= MAGENTA:
        x = c*(1 - abs(((BLUE - h)/d_BM)%2 - 1))
        r, g, b = (x + m, m, c + m)
    elif MAGENTA < h <= 360:
        x = c*(1 - abs(((BLUE - h)/d_M3)%2 - 1))
        r, g, b = (c + m, m, x + m)
    else:
        r, g, b = (m, m, m)
    return r, g, b


def hsl2_to_rgb(h, s, l):
    l = 100 - l
    r, g, b = hsl1_to_rgb(h, s, l)
    l_perceived = (0.299*r**2 + 0.587*g**2 + 0.114*b**2)**0.5
    l_nivelated = 1 - (l_perceived**6*(l/100)**4)**(1/10)
    r, g, b = hsl1_to_rgb(h, s, l_nivelated*100)
    return r, g, b


def hsl2(start, amount, saturation, luminosity):
    step = 360/amount
    ans = ((start + i*step, saturation, luminosity) for i in range(amount))
    ans = (hsl2_to_rgb(h, s, l) for h, s, l in ans)
    ans = (_rgb1_to_rgb255(r, g, b) for r, g, b in ans)
    ans = (("#%02x%02x%02x" % (r, g, b), r, g, b) for r, g, b in ans)
    return ans


space = {
    "HSL": create_system(hsl),
    "HSL2": hsl2,
    "HSV": create_system(hsv),
    "YIQ": yiq,
    "cat02": cat02,
    "YCbCr": cat02,
    "LCHab": create_system(lchab),
    "LCHuv": create_system(lchuv),
    "IPT": create_system(ipt),
    "JCh": jch,
    "JMh": jmh,
    "CIELCHab": create_cie_system("CIELCh"),
    "CAM02-UCS": create_cam02_system("CAM02-UCS"),
    "CAM02-LCD": create_cam02_system("CAM02-LCD"),
    "CAM02-SCD": create_cam02_system("CAM02-SCD"),
    "IPT+JCh": ipt_jch,
}


mixer = {
    "HSL": create_mixer(HSLColor),
    "HSV": create_mixer(HSLColor),
    "YIQ": yiq_mixer,
    "LCHab": create_mixer(LCHabColor),
    "LCHuv": create_mixer(LCHuvColor),
    "IPT": create_mixer(IPTColor),
    # "BT2020": create_mixer(BT2020Color),
    "JCh": jch_mixer,
    "JMh": jmh_mixer,
    "CIELCHab": create_cie_mixer("CIELCh"),
    "CAM02-UCS": create_cam02_mixer("CAM02-UCS"),
    "CAM02-LCD": create_cam02_mixer("CAM02-LCD"),
    "CAM02-SCD": create_cam02_mixer("CAM02-SCD"),
}
