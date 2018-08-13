from time import sleep

from webcolors import name_to_rgb

from neopixel import Adafruit_NeoPixel
from util import *


class RGBController:
    strip = None

    def __init__(self):
        LED_COUNT = 300
        LED_PIN = 18
        LED_FREQ_HZ = 800000
        LED_DMA = 10
        LED_BRIGHTNESS = 255
        LED_INVERT = False
        LED_CHANNEL = 0
        STRIP_TYPE = 0x00081000  # GRB

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                                       LED_BRIGHTNESS, LED_CHANNEL, STRIP_TYPE)
        self.strip.begin()

    def color_wipe(self, color, wait_ms=0):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self):
        """Wipe 12 colors across display a pixel at a time."""
        while True:
            self.color_wipe(Color(255, 0, 0), 10)
            self.color_wipe(Color(255, 127, 0), 10)
            self.color_wipe(Color(255, 255, 0), 10)
            self.color_wipe(Color(127, 255, 0), 10)
            self.color_wipe(Color(0, 255, 0), 10)
            self.color_wipe(Color(0, 255, 127), 10)
            self.color_wipe(Color(0, 255, 255), 10)
            self.color_wipe(Color(0, 127, 255), 10)
            self.color_wipe(Color(0, 0, 255), 10)
            self.color_wipe(Color(127, 0, 255), 10)
            self.color_wipe(Color(255, 0, 255), 10)
            self.color_wipe(Color(255, 0, 127), 10)

    def gradient(self, c1, c2):
        """Gradient between 2 colors."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, gradient_color(i, c1, c2, self.strip.numPixels()))
        self.strip.show()

    def voltage_drop(self):
        """Voltage drop effect (white to orange)"""
        self.gradient((255, 255, 255), (255, 50, 0))

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, wheel((i + j) & 255))
                self.strip.show()
                sleep(wait_ms / 1000.0)

    def clear(self):
        """Clears the strip one by one."""
        self.color_wipe(Color(0, 0, 0))

    def instant_color(self, r, g, b, wait=0.0):
        """Instantly switches color."""
        self.instant_color_array([Color(r, g, b)] * self.strip.numPixels(), wait)

    def instant_color_array(self, color, wait=0.0):
        """Instantly switches color from an array of colors."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color[i])
        self.strip.show()
        sleep(wait)

    def instant_color_name(self, name, wait=0.0):
        """Instantly switches color from a color name."""
        try:
            rgb = name_to_rgb(name)
            self.instant_color(rgb.red, rgb.green, rgb.blue, wait)
        except ValueError:
            self.show_error()

    def show_error(self):
        """Flashes red twice."""
        colors = self.save_pixels()
        for i in range(2):
            self.instant_color(0, 0, 0)
            sleep(0.1)
            self.instant_color(255, 0, 0)
            sleep(0.1)

            self.instant_color(0, 0, 0)
        sleep(0.1)
        self.instant_color_array(colors)

    def save_pixels(self):
        """Saves current pixel colors"""
        return [self.strip.getPixelColor(i) for i in range(self.strip.numPixels())]

    def rainbow_fade(self):
        """Goes through all the colors (every led is the same color)"""
        r = 255
        g = 0
        b = 0
        while True:
            for i in range(255):
                g += 1
                self.instant_color(r, g, b, 0.01)
            for i in range(255):
                r -= 1
                self.instant_color(r, g, b, 0.01)
            for i in range(255):
                b += 1
                self.instant_color(r, g, b, 0.01)
            for i in range(255):
                g -= 1
                self.instant_color(r, g, b, 0.01)
            for i in range(255):
                r += 1
                self.instant_color(r, g, b, 0.01)
            for i in range(255):
                b -= 1
                self.instant_color(r, g, b, 0.01)

    def random_fade(self):
        """Randomly fades between colors."""
        old_r, old_g, old_b = random_color()

        self.instant_color(old_r, old_g, old_b)

        new_r, new_g, new_b = random_color()
        # TODO: continue

    def strobe(self):
        """Strobe effect."""
        pass
        # TODO: continue
