from colorsys import hls_to_rgb
from random import random
from time import sleep

from neopixel import Color

RAINBOW = [
    Color(255, 0, 0),
    Color(255, 127, 0),
    Color(255, 255, 0),
    Color(127, 255, 0),
    Color(0, 255, 0),
    Color(0, 255, 127),
    Color(0, 255, 255),
    Color(0, 127, 255),
    Color(0, 0, 255),
    Color(127, 0, 255),
    Color(255, 0, 255),
    Color(255, 0, 127),
]


def gradient_color(pos, c1, c2, pixels):
    """Calculates the color for a given pixel in a gradient effect."""
    return Color(
        int(pos * (c2[0] - c1[0]) / pixels + float(c1[0])),
        int(pos * (c2[1] - c1[1]) / pixels + float(c1[1])),
        int(pos * (c2[2] - c1[2]) / pixels + float(c1[2])))


def rainbow_color_generator(brightness):
    """Returns an iterator with all the rainbow colors."""
    r = brightness
    g = 0
    b = 0

    yield (r, g, b)

    while True:
        for i in range(brightness):
            g += 1
            yield (r, g, b)
        for i in range(brightness):
            r -= 1
            yield (r, g, b)
        for i in range(brightness):
            b += 1
            yield (r, g, b)
        for i in range(brightness):
            g -= 1
            yield (r, g, b)
        for i in range(brightness):
            r += 1
            yield (r, g, b)
        for i in range(brightness):
            b -= 1
            yield (r, g, b)


def rainbow_wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def random_color():
    """Random color generator."""
    return [int(255 * x) for x in hls_to_rgb(random(), 0.5, 1)]


def save_pixels(strip):
    """Saves current pixel colors."""
    return [strip.getPixelColor(i) for i in range(strip.numPixels())]


def static_color_array(strip, color, wait_ms=0):
    """Instantly switches color from an array of colors."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color[i])
    strip.show()
    sleep(wait_ms / 1000.0)
