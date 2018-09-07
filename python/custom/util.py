from colorsys import hls_to_rgb
from random import random

from neopixel import Color


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def gradient_color(pos, c1, c2, pixels):
    """Calculates the color for a given pixel in a gradient effect."""
    r = int(pos * (c2[0] - c1[0]) / pixels + float(c1[0]))
    g = int(pos * (c2[1] - c1[1]) / pixels + float(c1[1]))
    b = int(pos * (c2[2] - c1[2]) / pixels + float(c1[2]))
    return Color(r, g, b)


def random_color():
    """Random color generator."""
    return [int(255 * x) for x in hls_to_rgb(random(), 0.5, 1)]
